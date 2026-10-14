from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
snapshot=json.loads((HERE/'CREATURE_LIFECYCLE_SOURCE_CANDIDATES.json').read_text(encoding='utf-8'))
parts=[(HERE/'CREATURE_LIFECYCLE_QUESTIONS.md').read_text(encoding='utf-8')]
issues=[]
for r in snapshot['classRecords']:
    live=json.loads((ROOT/r['path']).read_text(encoding='utf-8'))
    if r['kind']=='class-card':
        c=r['card'];name=c['id'];value=next(v for v in live['cards'] if v['id']==name)
        if value!=c:issues.append(name)
        proc={k:c.get(k) for k in ('name','activation','cost','rangeAndTarget','duration','frequency','effect')}
    else:
        name=f"{r['owner']}.engine[{r['engineIndex']}]";proc={'text':r['text']}
        if live['engine'][r['engineIndex']]!=r['text']:issues.append(name)
    parts+=['### '+name,'',r['path'],'',r.get('candidateOrigin','Original broad lifecycle inventory'),'',json.dumps(proc,ensure_ascii=False,indent=2),'']
for r in snapshot['supportingSources']:
    raw=(ROOT/r['sourcePath']).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=r['fullFileSha256']:issues.append(r['sourcePath'])
    parts+=['### Shared rule: '+r['paragraphPrefix'],'',r['text'],'']
maximum=(ROOT/'docs/mechanics/MAXIMUM_HP_PLAYTEST.md').read_text(encoding='utf-8')
parts+=['## Previously reviewed maximum-HP integration (not new source candidates)','']
for paragraph in maximum.split('\n\n'):
    if paragraph.startswith(('**New Wizard-specific stacking exception:**',
                             "Conjuration's amount",
                             '**New Familiar Bond interpretation:**',
                             'When a creature is initially created,')):
        parts+=[paragraph,'']
parts+=['Evidence: GPT_MAXIMUM_HP_FINAL_CLOSURE.md. Preserve these creation-versus-later-capacity distinctions.','']
assert len(snapshot['classRecords'])==100 and not issues,issues
(HERE/'CODEX_CREATURE_LIFECYCLE_CONFERENCE.md').write_text('\n'.join(parts),encoding='utf-8')
(HERE/'CREATURE_LIFECYCLE_SOURCE_VALIDATION.json').write_text(json.dumps({
    'result':'PASS','exactClassRecords':100,'originalCandidates':83,'semanticSupplements':17,
    'frozenSharedParagraphs':3,'status':'UNREVIEWED; conference prepared but not yet submitted',
    'issues':issues},indent=2)+'\n',encoding='utf-8')
print('Prepared exact 100+3 creature lifecycle conference; NOT submitted.')
