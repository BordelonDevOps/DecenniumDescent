"""Apply already-reviewed generic timing to the two unambiguous hostile riders."""
from pathlib import Path
import json
GAME=Path(__file__).resolve().parents[4]
ROOT=GAME/'DescentReviewChanges/ReviewBible'
p=ROOT/'data/playtest/custom_condition_bindings.json'
data=json.loads(p.read_text(encoding='utf-8'))
for d in data['definitions']:
    if d['mechanicalId'] in ('warrior.weakened','cleric.judged'):
        d['ending']='End of the second future regular target turn after application; an in-progress target turn is excluded. Preserve the original virtual marker across initiative changes. A legal reapplication refreshes without increasing the penalty.'
        decision='The reviewed combat timing overlay resolves the formerly ambiguous bare two-round hostile duration. Explicit source endpoints still take precedence.'
        if decision not in d['integrationDecisions']:
            d['integrationDecisions'].append(decision)
        for evidence in ['docs/audit/2026-10-08/full-game/GPT_COMBAT_EXACT_FINDINGS.md','docs/audit/2026-10-08/full-game/GPT_STRAIN_FIRST_REVIEW.md']:
            if evidence not in d['reviewEvidence']:
                d['reviewEvidence'].append(evidence)
data['openIssues']=[s.replace('Resolve remaining common round-marker endpoints.','Apply reviewed common round-marker defaults to every remaining source; resolve mark effects whose source/target clock is still ambiguous.') for s in data['openIssues']]
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Bound Warrior Weakened and Cleric Judged to reviewed hostile-duration clocks.')
