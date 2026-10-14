from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
path=ROOT/'data/playtest/creature_lifecycle_bindings.json'
data=json.loads(path.read_text(encoding='utf-8'))
data['status']='SOURCE CONFERENCE SUBMITTED; individual classification pending'
data['conferenceEvidence']='docs/audit/2026-10-08/full-game/CODEX_CREATURE_LIFECYCLE_CONFERENCE.md'
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
path=ROOT/'data/playtest/game_development_coverage.json'
data=json.loads(path.read_text(encoding='utf-8'))
for ident in ('DD-24','DD-35'):
    row=next(r for r in data['aspects'] if r['id']==ident)
    for field,value in (
        ('sourceEvidence','docs/audit/2026-10-08/full-game/CREATURE_LIFECYCLE_SOURCE_CANDIDATES.json'),
        ('reviewEvidence','docs/audit/2026-10-08/full-game/CODEX_CREATURE_LIFECYCLE_CONFERENCE.md'),
        ('draftEvidence','DescentReviewChanges/ReviewBible/docs/mechanics/CREATURE_LIFECYCLE_SOURCE_BINDINGS.md'),
        ('validationEvidence','DescentReviewChanges/ReviewBible/docs/mechanics/CREATURE_LIFECYCLE_SOURCE_VALIDATION.json')):
        if value not in row[field]:row[field].append(value)
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
path=HERE/'CREATURE_LIFECYCLE_SOURCE_VALIDATION.json'
data=json.loads(path.read_text(encoding='utf-8'))
data['status']='SOURCE CONFERENCE SUBMITTED; no semantic approval yet'
path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
note='\n## Creature companion source conference submitted\n\nThe [next conference](CODEX_CREATURE_LIFECYCLE_CONFERENCE.md) supplies100 exact Druid/Mage/Mirrorsage/Ranger/Wizard passages plus3 frozen shared paragraphs.83 came from the original230-row broad inventory;17 are semantic supplements, including omitted undead/familiar profiles and Druid retained-character rules. The original inventory is preserved. [Source integrity](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/CREATURE_LIFECYCLE_SOURCE_VALIDATION.json) passes; individual discussion is pending. The slice includes incidental form/tempHP guards, so100 does not mean100 complete creature abilities.\n'
for path in (HERE/'README.md',HERE/'REVIEW_STATUS.md'):
    text=path.read_text(encoding='utf-8')
    if '## Creature companion source conference submitted' not in text:path.write_text(text+note,encoding='utf-8')
print('Recorded submitted100+3 creature source conference; semantics pending.')
