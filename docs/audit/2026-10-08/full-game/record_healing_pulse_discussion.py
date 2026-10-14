"""Record100 source discussion roles; exact boundaries/implementation still open."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
text=(HERE/'GPT_HEALING_PULSE_FIRST_REVIEW_PARTIAL.md').read_text(encoding='utf-8')
roles={}
for line in text.splitlines():
    cells=[v.strip().strip(chr(96)) for v in line.strip('|').split('|')]
    if len(cells)==3 and '.' in cells[0] and not cells[0].startswith('#'):
        roles[cells[0]]=(cells[1],cells[2])
path=ROOT/'data/playtest/healing_pulse_bindings.json'
data=json.loads(path.read_text(encoding='utf-8'))
assert len(roles)==100 and set(roles)=={b['bindingId'] for b in data['bindings']}
for row in data['bindings']:
    role,disposition=roles[row['bindingId']]
    row['classification']=role
    row['status']='DISCUSSED; exact boundaries and implementation pending'
    row['operationalOverrides']=['FIRST PROPOSAL; read later source corrections before implementing: '+disposition]
    row['reviewEvidence']=['GPT_HEALING_PULSE_FIRST_REVIEW.md']
    row['openIssues']=['Ten source/timing/target-budget follow-ups submitted in CODEX_HEALING_PULSE_BOUNDARIES.md; no exact implementation closure. Wider card mechanics stay separately reviewed.']
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
path=ROOT/'data/playtest/game_development_coverage.json'
data=json.loads(path.read_text(encoding='utf-8'))
row=next(r for r in data['aspects'] if r['id']=='DD-24')
for field,value in [
    ('sourceEvidence','docs/audit/2026-10-08/full-game/HEALING_PULSE_SOURCE_CANDIDATES.json'),
    ('sourceEvidence','docs/audit/2026-10-08/full-game/HEALING_PULSE_SUPPORTING_SOURCES.json'),
    ('reviewEvidence','docs/audit/2026-10-08/full-game/GPT_HEALING_PULSE_FIRST_REVIEW.md'),
    ('validationEvidence','DescentReviewChanges/ReviewBible/docs/mechanics/HEALING_PULSE_SOURCE_VALIDATION.json')]:
    if value not in row[field]:row[field].append(value)
row['openIssues'].append('100 recurring-healing/zone lexical candidates classified individually; ten source-boundary corrections and exact scheduler review remain open.')
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for path in (HERE/'README.md',HERE/'REVIEW_STATUS.md'):
    with path.open('a',encoding='utf-8') as f:
        f.write('\n## Recurring healing and pulse discussion\n\nThe [100-source conference](CODEX_HEALING_PULSE_CONFERENCE.md) received a [complete first discussion](GPT_HEALING_PULSE_FIRST_REVIEW.md). The [follow-up](CODEX_HEALING_PULSE_BOUNDARIES.md) supplies five supporting source passages and challenges upkeep, Song/Burning Blood, virtual clocks, target budgets and delayed expiration. All100 candidates are classified; none is promoted to a complete card. The78 operational ordinary spell drafts contain no lexical recurring-healing intersection;770 unfinished spells remain open. A230-passage companion/device/form lifecycle inventory is prepared for later review.\n')
print('Recorded100 individual discussion roles; bounded scheduler still open.')
