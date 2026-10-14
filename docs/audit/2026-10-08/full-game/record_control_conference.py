from pathlib import Path
import json
GAME=Path(__file__).resolve().parents[4]
ROOT=GAME/'DescentReviewChanges/ReviewBible'
p=ROOT/'data/playtest/game_development_coverage.json'
data=json.loads(p.read_text(encoding='utf-8'))
for row in data['aspects']:
    if row['number'] in (16,18):
        row['status']='control-source-conference-in-progress'
        additions={'sourceEvidence':['docs/audit/2026-10-08/full-game/CONTROL_STATE_SOURCE_PACKET.json'],
                   'reviewEvidence':['docs/audit/2026-10-08/full-game/CODEX_CONTROL_EXACT_CONFERENCE.md'],
                   'draftEvidence':['DescentReviewChanges/ReviewBible/docs/mechanics/CONTROL_STATE_COVERAGE.md','DescentReviewChanges/ReviewBible/data/playtest/control_state_coverage.json'],
                   'validationEvidence':['DescentReviewChanges/ReviewBible/docs/mechanics/CONTROL_STATE_SOURCE_VALIDATION.json']}
        for field,values in additions.items():
            for value in values:
                if value not in row[field]:
                    row[field].append(value)
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Recorded179-source control conference; all broader acceptance gates preserved.')
