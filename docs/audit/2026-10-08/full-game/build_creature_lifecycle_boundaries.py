from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
shared=ROOT/'docs/mechanics/CLASS_PLAYTEST_RULES.md'
supports=[]
for prefix in ('Unless expressly stated,','No repeated hard denial'):
    text=next(v for v in shared.read_text(encoding='utf-8').split('\n\n') if v.startswith(prefix))
    supports.append({'sourcePath':shared.relative_to(ROOT).as_posix(),'paragraphPrefix':prefix,
                     'text':text,'fullFileSha256':hashlib.sha256(shared.read_bytes()).hexdigest()})
parts=[(HERE/'CREATURE_LIFECYCLE_BOUNDARY_QUESTIONS.md').read_text(encoding='utf-8')]
for record in supports:
    parts+=['## Additional exact frozen support','',json.dumps(record,ensure_ascii=False,indent=2),'']
for name,start,end in (
    ('COMBAT_ACTION_PLAYTEST.md','## Time and event ordering','## Standard Actions'),
    ('COMBAT_ACTION_PLAYTEST.md','## Cover, sight, Hide and Search','## Validation'),
    ('CONTROL_STATES_PLAYTEST.md','## Compulsion, action denial and initiative','## Hypermutation and systemic penalties'),
    ('CONDITIONS_PLAYTEST.md','## Charmed','## Choking')):
    raw=(ROOT/'docs/mechanics'/name).read_text(encoding='utf-8')
    begin=raw.index(start)
    finish=raw.find(end,begin+len(start))
    # Charmed section ends at the next H2 even if the named following heading differs.
    if finish<0:
        finish=raw.find('\n## ',begin+len(start))
    if finish<0:finish=len(raw)
    parts+=['## Already-reviewed interface: '+name,'',raw[begin:finish].strip(),'']
parts+=['## Adjacent source checks','',(HERE/'CREATURE_LIFECYCLE_ADJACENT_FINDINGS.md').read_text(encoding='utf-8'),'']
(HERE/'CREATURE_LIFECYCLE_SUPPORTING_SOURCES.json').write_text(json.dumps({
    'scope':'Two additional frozen targeting/hard-denial paragraphs; original three supports remain in the100-source inventory.',
    'supportingSources':supports},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(HERE/'CODEX_CREATURE_LIFECYCLE_BOUNDARIES.md').write_text('\n'.join(parts),encoding='utf-8')
print('Built creature boundary conference with two additional exact frozen paragraphs.')
