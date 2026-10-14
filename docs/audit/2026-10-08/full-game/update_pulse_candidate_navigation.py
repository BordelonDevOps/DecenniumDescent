"""Record current candidate work without claiming notebook approval."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
path=ROOT/'data/playtest/game_development_coverage.json'
data=json.loads(path.read_text(encoding='utf-8'))
row=next(r for r in data['aspects'] if r['id']=='DD-24')
prefix='DescentReviewChanges/ReviewBible/'
for value,field in [('docs/mechanics/MAXIMUM_HP_PLAYTEST.md','draftEvidence'),('docs/mechanics/MAXIMUM_HP_PLAYTEST_VALIDATION.json','validationEvidence')]:
    evidence=prefix+value
    if evidence in row['sourceEvidence']:row['sourceEvidence'].remove(evidence)
    if evidence not in row[field]:row[field].append(evidence)
for field,value in [
    ('draftEvidence',prefix+'docs/mechanics/HEALING_PULSE_PLAYTEST.md'),
    ('validationEvidence',prefix+'docs/mechanics/HEALING_PULSE_PLAYTEST_VALIDATION.json'),
    ('validationEvidence',prefix+'docs/mechanics/HEALING_PULSE_SUPPORT_VALIDATION.json'),
    ('reviewEvidence','docs/audit/2026-10-08/full-game/GPT_HEALING_PULSE_BOUNDARIES.md')]:
    if value not in row[field]:row[field].append(value)
row['openIssues']=[v for v in row['openIssues'] if not v.startswith('100 recurring-healing/zone')]
row['openIssues'].append('100 pulse sources plus6 supporting passages discussed; candidate71 checks/301 partitions pass. Exact notebook review and EnhancedGarden entitlement clarification pending. Device/Totem lifecycle73-source packet prepared, including previously unsupplied MagneticWall transfer.')
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for path in (HERE/'README.md',HERE/'REVIEW_STATUS.md'):
    with path.open('a',encoding='utf-8') as f:
        f.write('\nThe [pulse boundary reply](GPT_HEALING_PULSE_BOUNDARIES.md) corrects Song upkeep, shared maintenance, preserved virtual clocks and target budgets. The [exact candidate review](CODEX_HEALING_PULSE_IMPLEMENTATION_REVIEW.md) is submitted with71 checks/301 partitions and100+6 verified passages; implementation approval remains pending. The next [73-source device/Totem packet](CODEX_DEVICE_LIFECYCLE_CONFERENCE.md) is prepared but not submitted.\n')
print('Updated candidate navigation; no new domain closure.')
