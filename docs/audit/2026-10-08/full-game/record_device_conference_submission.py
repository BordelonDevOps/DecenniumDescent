from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
path=ROOT/'data/playtest/game_development_coverage.json'
data=json.loads(path.read_text(encoding='utf-8'))
row=next(r for r in data['aspects'] if r['id']=='DD-24')
for field,value in [
    ('sourceEvidence','docs/audit/2026-10-08/full-game/DEVICE_LIFECYCLE_SOURCE_CANDIDATES.json'),
    ('reviewEvidence','docs/audit/2026-10-08/full-game/CODEX_DEVICE_LIFECYCLE_CONFERENCE.md'),
    ('validationEvidence','DescentReviewChanges/ReviewBible/docs/mechanics/DEVICE_LIFECYCLE_SOURCE_VALIDATION.json')]:
    if value not in row[field]:row[field].append(value)
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for path in (HERE/'README.md',HERE/'REVIEW_STATUS.md'):
    with path.open('a',encoding='utf-8') as f:
        f.write('\nThe [74-passage device/Totem source conference](CODEX_DEVICE_LIFECYCLE_CONFERENCE.md) has now been submitted to Calibration Review. [Source integrity](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/DEVICE_LIFECYCLE_SOURCE_VALIDATION.json) passes74 class records and3 frozen shared paragraphs; individual discussion is pending. Magnetic Wall is an explicit addition to the73 lexical passages, not part of the previous39-source redirection closure.\n')
print('Recorded device conference submission; semantics pending.')
