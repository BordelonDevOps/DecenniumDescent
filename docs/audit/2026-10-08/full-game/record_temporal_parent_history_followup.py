"""Record actual four-finding confirmation and the subsequent two-finding repair."""
from pathlib import Path
import hashlib,json
audit=Path(__file__).resolve().parent;game=audit.parents[3];root=game/'DescentReviewChanges/ReviewBible'
review='docs/audit/2026-10-08/full-game/GPT_TEMPORAL_PARENT_HISTORY_REPAIR_REVIEW.md'
assert 'four prior findings are materially repaired' in (game/review).read_text(encoding='utf-8')
submission=json.loads((audit/'TEMPORAL_PARENT_HISTORY_TIME_PIN_SUBMISSION.json').read_text())
for name,h in submission['hashes'].items():assert hashlib.sha256((root/name).read_bytes()).hexdigest()==h
p=root/'docs/mechanics/TEMPORAL_PARENT_HISTORY_REVIEW_STATUS.json'
backup=audit/'PARENT_HISTORY_STATUS_BEFORE_TIME_PIN_REPAIR.json';assert not backup.exists();backup.write_bytes(p.read_bytes())
status=json.loads(p.read_text());status.update({
 'status':'CANDIDATE — four original findings confirmed repaired; two follow-up fixes pass 59 checks and await notebook review',
 'testMethods':59,'hashes':submission['hashes'],
 'latestActualReview':review,'originalFourFindingsConfirmedRepaired':True,
 'repairSubmission':'docs/audit/2026-10-08/full-game/CODEX_TEMPORAL_PARENT_HISTORY_TIME_PIN_REPAIR.md',
 'followupFindings':[
  {'issue':'Backdated evidence query time','repair':'Use actual scheduler time; reject mismatching or pre-history timestamps'},
  {'issue':'Deleted reference pins could hide replacement/lost historical references','repair':'Append-only object/slot/callback manifests checked on every validation'}]})
p.write_text(json.dumps(status,indent=2)+'\n')
p=root/'docs/mechanics/TEMPORAL_PARENT_PLAYTEST.md';text=p.read_text(encoding='utf-8')
text=text.replace('now passes [55 checks](TEMPORAL_PARENT_HISTORY_VALIDATION.json) and is under notebook review.',
 'passed 55 checks; the notebook [confirmed those four repairs and found two further gaps](../../../../docs/audit/2026-10-08/full-game/GPT_TEMPORAL_PARENT_HISTORY_REPAIR_REVIEW.md). The [subsequent exact fix](../../../../docs/audit/2026-10-08/full-game/CODEX_TEMPORAL_PARENT_HISTORY_TIME_PIN_REPAIR.md) binds current query time and append-only references, passes [59 checks](TEMPORAL_PARENT_HISTORY_VALIDATION.json), and is under review.')
p.write_text(text,encoding='utf-8')
for p in (game/'START_HERE.md',audit/'REVIEW_STATUS.md'):
    text=p.read_text(encoding='utf-8').replace('55-check repair','59-check repair')
    text=text.replace('Four parent-history findings repaired locally; exact 55-check candidate is',
      'Four initial parent-history repairs confirmed; two follow-up fixes pass 59 checks and are')
    p.write_text(text,encoding='utf-8')
p=root/'data/playtest/game_development_coverage.json';packet=json.loads(p.read_text(encoding='utf-8'))
for row in packet['aspects']:
    if any('55-method repair is under notebook review' in v for v in row['openIssues']):
        row['openIssues']=[v.replace('Initial parent-history review found four evidence gaps;55-method repair is under notebook review.',
            'Four initial parent-history repairs confirmed;two follow-up fixes for query time/reference pins pass59 checks and await review.') for v in row['openIssues']]
        row['reviewEvidence']=list(dict.fromkeys(row['reviewEvidence']+[review]))
p.write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Recorded actual 55-method disposition and pending59-method repair; full restoration stays open.')
