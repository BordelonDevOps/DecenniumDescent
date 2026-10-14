from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
GAME=HERE.parents[3]
ROOT=GAME/'DescentReviewChanges/ReviewBible'
path=ROOT/'data/playtest/game_development_coverage.json'
data=json.loads(path.read_text(encoding='utf-8'))
rev='DescentReviewChanges/ReviewBible/'
audit='docs/audit/2026-10-08/full-game/'
for row in data['aspects']:
 if row['number'] in (16,18):
  row['status']='control-candidate-implemented-exact-review-pending'
  additions={'sourceEvidence':[audit+'CONTROL_STATE_SUPPLEMENT_SOURCE_PACKET.json'],
   'reviewEvidence':[audit+'GPT_CONTROL_STATE_FIRST_REVIEW.md',audit+'GPT_CONTROL_COUNTEREXAMPLE_REVIEW.md',audit+'GPT_CONTROL_CLOCK_CORRECTIONS.md',audit+'CODEX_CONTROL_EXACT_REVIEW.md'],
   'draftEvidence':[rev+'docs/mechanics/CONTROL_STATES_PLAYTEST.md',rev+'docs/mechanics/CONTROL_SOURCE_BINDINGS.md',rev+'data/playtest/control_state_bindings.json'],
   'validationEvidence':[rev+'docs/mechanics/CONTROL_PLAYTEST_VALIDATION.json',rev+'docs/mechanics/CONTROL_BINDING_VALIDATION.json']}
  for field,values in additions.items():
   for value in values:
    if value not in row[field]:row[field].append(value)
 if row['number']==24:
  candidate=audit+'HEALING_DEATH_SOURCE_CANDIDATES.json'
  if candidate not in row['sourceEvidence']:row['sourceEvidence'].append(candidate)
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
coverage=ROOT/'data/playtest/control_state_coverage.json'
d=json.loads(coverage.read_text(encoding='utf-8'))
for row in d['candidates']:
 row['openIssues']=[s.replace('Exact clock/semantic corrections are under review; no whole-card completion implied.','Exact candidate implementation review is pending; no whole-card completion implied.') for s in row['openIssues']]
coverage.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Recorded implemented219-source control candidate and pending healing/death inventory; broad gates remain open.')
