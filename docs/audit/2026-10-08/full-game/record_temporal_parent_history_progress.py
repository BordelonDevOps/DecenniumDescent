"""Reconcile current history review evidence; retain every earlier audit record."""
from pathlib import Path
import hashlib,json

audit=Path(__file__).resolve().parent;game=audit.parents[3]
root=game/'DescentReviewChanges/ReviewBible'
review=audit/'GPT_TEMPORAL_PARENT_HISTORY_REVIEW.md'
assert 'four reproducible defects' in review.read_text(encoding='utf-8')
submission=json.loads((audit/'TEMPORAL_PARENT_HISTORY_REPAIR_SUBMISSION.json').read_text())
for name,h in submission['hashes'].items():assert hashlib.sha256((root/name).read_bytes()).hexdigest()==h
report=json.loads((root/'docs/mechanics/TEMPORAL_PARENT_HISTORY_VALIDATION.json').read_text())
assert report['status']=='PASS' and report['testMethods']==55
for source,destination in (
    (root/'data/playtest/game_development_coverage.json',audit/'COVERAGE_BEFORE_PARENT_HISTORY_REPAIR.json'),
    (root/'docs/mechanics/TEMPORAL_PARENT_PLAYTEST.md',audit/'PARENT_GUIDE_BEFORE_HISTORY_REPAIR.md'),
    (game/'START_HERE.md',audit/'START_HERE_BEFORE_PARENT_HISTORY_REPAIR.md')):
    assert not destination.exists();destination.write_bytes(source.read_bytes())

status={
 'status':'CANDIDATE — four initial notebook findings addressed locally; exact 55-method repair under review',
 'testMethods':55,'hashes':submission['hashes'],
 'reviewedOriginal':'docs/audit/2026-10-08/full-game/CODEX_TEMPORAL_PARENT_HISTORY_REVIEW.md',
 'actualReview':'docs/audit/2026-10-08/full-game/GPT_TEMPORAL_PARENT_HISTORY_REVIEW.md',
 'repairSubmission':'docs/audit/2026-10-08/full-game/CODEX_TEMPORAL_PARENT_HISTORY_REPAIR.md',
 'findings':[
  {'issue':'Unbound stats and fabricated prices','repair':'Bound actual character roots and current ordinary quote; seven authority regression methods'},
  {'issue':'Unobserved Druid finite/recharge changes','repair':'Persistent finite fingerprint; cadence stays shared current state'},
  {'issue':'Unrelated mutations laundered into operation receipts','repair':'Exact operation/identity/target transition matrix and guarded save callbacks'},
  {'issue':'All outside events labeled casts','repair':'OUTSIDE_EVENT on generic history; OUTSIDE_CAST on actual cast-created receipt only'}],
 'parentRuntimeIntegrated':False,'fullTimeLoopOperational':False,'remainingMajorIntegrations':7,
 'wholeGameClosure':False,'githubPushed':False,
 'limitations':['Native ordinary operations and source history only; no restoration or geometry planning',
  'Host-owned actual character roots and target/component/save legality',
  'Ordinary undiscounted quotes only; all class cadence transactions still require their own integration',
  'Buffer adapter remains authoritative for shield grants and remaining amounts',
  'Ordinary numeric turn arguments are not replay-safe temporal wrappers']}
manifest=root/'docs/mechanics/TEMPORAL_PARENT_HISTORY_REVIEW_STATUS.json'
assert not manifest.exists();manifest.write_text(json.dumps(status,indent=2)+'\n',encoding='utf-8')

p=root/'docs/mechanics/TEMPORAL_PARENT_PLAYTEST.md';text=p.read_text(encoding='utf-8')
start=text.index('The first implementation layer is now ')
end=text.index('\n\nThis layer begins',start)
text=text[:start]+'''The first implementation layer is `tools/temporal_parent_history.py`: an observational journal over the actual Druid and transformation objects. The notebook's [initial 38-method review](../../../../docs/audit/2026-10-08/full-game/GPT_TEMPORAL_PARENT_HISTORY_REVIEW.md) identified four evidence gaps: unbound stats/prices, unobserved finite economy, unrelated lifecycle changes recorded as legitimate operations, and incorrect outside-cast labels. The [exact repair](../../../../docs/audit/2026-10-08/full-game/CODEX_TEMPORAL_PARENT_HISTORY_REPAIR.md) now passes [55 checks](TEMPORAL_PARENT_HISTORY_VALIDATION.json) and is under notebook review. Its [current status manifest](TEMPORAL_PARENT_HISTORY_REVIEW_STATUS.json) binds the submitted files and keeps the wider integration open.

The candidate binds current character stats and ordinary spell quotes, watches Druid-owned finite resources/rests/recharge, restricts lifecycle evidence to the actual operation and requested identities, and distinguishes outside events from real outside casts. A save callback cannot introduce unrelated parent changes. Shared casting cadence remains current; this does not implement all class casting hooks or authorize discounts/free copies. Shield-grant history remains the responsibility of the canonical Buffer adapter.''' +text[end:]
p.write_text(text,encoding='utf-8')

p=root/'data/playtest/game_development_coverage.json';packet=json.loads(p.read_text(encoding='utf-8'))
ids=('DD-03','DD-08','DD-09','DD-16','DD-18','DD-21','DD-35','DD-63','DD-64')
conferences=['docs/audit/2026-10-08/full-game/'+n for n in (
 'GPT_TEMPORAL_CONTROL_WORLD_CLOSURE.md','GPT_TEMPORAL_PARENT_BOUNDARIES.md',
 'GPT_TEMPORAL_PARENT_CADENCE_CLARIFICATION.md','GPT_TEMPORAL_PARENT_HISTORY_REVIEW.md')]
guide='DescentReviewChanges/ReviewBible/docs/mechanics/TEMPORAL_PARENT_PLAYTEST.md'
prefixes=('Time Loop: bounded foundational','Temporal control/pulse source conference',
 'The bounded live control/pulse transaction interface','Ten form/concentration/Druid parent cases')
for row in packet['aspects']:
    if row['id'] not in ids:continue
    row['reviewEvidence']=list(dict.fromkeys(row['reviewEvidence']+conferences))
    row['draftEvidence']=list(dict.fromkeys(row['draftEvidence']+[guide]))
    row['validationEvidence']=[v for v in row['validationEvidence'] if v not in conferences and v!=guide]
    row['validationEvidence']=list(dict.fromkeys(row['validationEvidence']+[
      'DescentReviewChanges/ReviewBible/docs/mechanics/TEMPORAL_PARENT_HISTORY_VALIDATION.json',
      'DescentReviewChanges/ReviewBible/docs/mechanics/TEMPORAL_PARENT_HISTORY_REVIEW_STATUS.json']))
    row['openIssues']=[v for v in row['openIssues'] if not v.startswith(prefixes)]
    row['openIssues'].append('Time Loop: bounded foundation, payment/output and live control/pulse checkpoints jointly reviewed (76+22+50 checks). Ten parent policies and Action/cadence clarification discussed;85 fields/26 Druid profiles inventoried. Initial parent-history review found four evidence gaps;55-method repair is under notebook review. Complete parent restoration, native temporal wrappers, source clocks/output application and all seven larger integrations remain open. Full playable activation stays disabled; no whole-domain closure.')
p.write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

p=game/'START_HERE.md';text=p.read_text(encoding='utf-8')
needle='their runtime integration remains next.'
assert needle in text
text=text.replace(needle,'their runtime integration remains next. The first [operation-history layer](DescentReviewChanges/ReviewBible/docs/mechanics/TEMPORAL_PARENT_HISTORY_REVIEW_STATUS.json) has a 55-check repair under notebook review after four initial evidence findings.')
p.write_text(text,encoding='utf-8')

note='''
## Parent operation history: four-finding repair under review

The notebook's [actual initial review](GPT_TEMPORAL_PARENT_HISTORY_REVIEW.md) found four evidence gaps in the 38-method candidate. Canonical stats/ordinary prices, persistent Druid finite-state checking, operation-qualified transition evidence and outside-event classification are addressed in the [exact 55-method repair](CODEX_TEMPORAL_PARENT_HISTORY_REPAIR.md), now submitted in Calibration Review. This is recorded as a candidate pending the actual response, not a joint closure. The first authority probes and original exact packet remain preserved.

The current guide and coverage ledger now distinguish source discussion, authored rules and executed validation evidence. Repeated temporal progress notes were consolidated; the entire earlier ledger is retained in COVERAGE_BEFORE_PARENT_HISTORY_REPAIR.json. No original game source was deleted. All seven major temporal integrations and final whole-game/GitHub gates remain open.
'''
for name in ('REVIEW_STATUS.md','TEMPORAL_PARENT_INTEGRATION_NEXT.md'):
    p=audit/name;p.write_text(p.read_text(encoding='utf-8')+note,encoding='utf-8')
print('Recorded candidate repairs and consolidated current temporal notes; historical originals preserved.')
