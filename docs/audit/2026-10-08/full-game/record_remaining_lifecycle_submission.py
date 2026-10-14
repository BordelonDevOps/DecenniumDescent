from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
path=ROOT/'data/playtest/game_development_coverage.json'
data=json.loads(path.read_text(encoding='utf-8'))
for ident in ('DD-24','DD-35'):
    row=next(r for r in data['aspects'] if r['id']==ident)
    for field,value in (
        ('sourceEvidence','docs/audit/2026-10-08/full-game/REMAINING_LIFECYCLE_CONFERENCE_SOURCES.json'),
        ('draftEvidence','docs/audit/2026-10-08/full-game/CODEX_REMAINING_LIFECYCLE_CONFERENCE.md'),
        ('validationEvidence','DescentReviewChanges/ReviewBible/docs/mechanics/REMAINING_LIFECYCLE_SOURCE_VALIDATION.json')):
        if value not in row[field]:row[field].append(value)
    note='Remaining80+5 lifecycle source conference visibly submitted in Calibration Review; classification and substantive decisions pending. No implementation or source-role closure yet.'
    if note not in row['openIssues']:row['openIssues'].append(note)
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for name in ('README.md','REVIEW_STATUS.md'):
    path=HERE/name;text=path.read_text(encoding='utf-8')
    note='\n## Remaining lifecycle80+5 conference submitted\n\nThe [80-source packet](CODEX_REMAINING_LIFECYCLE_CONFERENCE.md) was visibly submitted in Chrome after the selected creature100+5 closure. It contains74 remaining original lexical passages+6 semantic supplements,5 frozen supports and relevant earlier healing/control dispositions. Integrity80+5 passes; classification, source exceptions and implementation remain pending. Full [form/tempHP candidate corpus](FORM_TEMP_HP_SOURCE_CANDIDATES.json) separately preserves124 passages, including all7engine+59card Druid sources; not reviewed yet.\n'
    if '## Remaining lifecycle80+5 conference submitted' not in text:text+=note
    path.write_text(text,encoding='utf-8')
print('Recorded actual80+5 conference submission; no premature closure.')
