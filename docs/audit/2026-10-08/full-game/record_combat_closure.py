from pathlib import Path
import json
GAME=Path(__file__).resolve().parents[4]
ROOT=GAME/'DescentReviewChanges/ReviewBible'
EVIDENCE='docs/audit/2026-10-08/full-game/GPT_STRAIN_FIRST_REVIEW.md'
p=ROOT/'data/playtest/game_development_coverage.json'
data=json.loads(p.read_text(encoding='utf-8'))
for row in data['aspects']:
    if row['number'] in (3,17,18,19,20,21):
        row['status']='bounded-scope-reviewed-and-reference-validated'
        scope='Supplied combat/action/timing/vision integration reviewed with GPT after marker, maneuver-budget and Ready-duration corrections;112 checks and285 movement-cost states pass. Broader domain acceptance gate remains open.'
        if scope not in row.setdefault('completedScopes',[]):
            row['completedScopes'].append(scope)
        if EVIDENCE not in row['reviewEvidence']:
            row['reviewEvidence'].append(EVIDENCE)
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=Path(__file__).resolve().parent/'REVIEW_STATUS.md'
text=p.read_text(encoding='utf-8').replace('Final bounded confirmation is pending; DD03/17/18/19/20/21 remain open.', 'The [GPT disposition](GPT_STRAIN_FIRST_REVIEW.md) closes this supplied scope as REVIEWED / reference-VALIDATED; DD03/17/18/19/20/21 remain open.')
p.write_text(text,encoding='utf-8')
print('Recorded bounded combat closure; all six broad domain rows remain open.')
