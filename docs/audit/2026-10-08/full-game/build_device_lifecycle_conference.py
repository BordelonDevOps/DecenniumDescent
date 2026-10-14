"""Prepare73 lexical object/command candidates plus one semantic supplement."""
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
all_rows=json.loads((HERE/'COMPANION_LIFECYCLE_SOURCE_CANDIDATES.json').read_text(encoding='utf-8'))['classRecords']
rows=[r for r in all_rows if r['owner'] in ('tinker','shaman')]
assert len(rows)==73
path=ROOT/'data/public/class_playtests/tinker.json'
card=next(c for c in json.loads(path.read_text(encoding='utf-8'))['cards'] if c['id']=='tinker.hero.artificer.magnetic-wall')
rows.append({'kind':'class-card','owner':'tinker','path':path.relative_to(ROOT).as_posix(),'card':card,
             'sourceObjectSha256':hashlib.sha256(json.dumps(card,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest(),
             'candidateOrigin':'Semantic supplement: operational wall interception text lacks lexical device/deploy/redirect terms.'})
shared=(ROOT/'docs/mechanics/CLASS_PLAYTEST_RULES.md').read_text(encoding='utf-8')
supports=[]
for prefix in ('Where a class card calls for a','One regular Action,','No damage/healing copy'):
    value=next(p for p in shared.split('\n\n') if p.startswith(prefix))
    supports.append({'sourcePath':'docs/mechanics/CLASS_PLAYTEST_RULES.md','paragraphPrefix':prefix,'text':value,
                     'fullFileSha256':hashlib.sha256((ROOT/'docs/mechanics/CLASS_PLAYTEST_RULES.md').read_bytes()).hexdigest()})
snapshot={'status':'UNREVIEWED_SOURCE_CANDIDATES','scope':'73 lexical Tinker/Shaman passages plus MagneticWall semantic supplement:74 exact passages;3 frozen shared-rule paragraphs. Other157 future lifecycle candidates stay separate.','classRecords':rows,'supportingSources':supports}
(HERE/'DEVICE_LIFECYCLE_SOURCE_CANDIDATES.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
header=(HERE/'DEVICE_LIFECYCLE_QUESTIONS.md').read_text(encoding='utf-8')
parts=[header]
for r in rows:
    if r['kind']=='class-card':
        c=r['card'];ident=c['id'];proc={k:c.get(k) for k in ('name','activation','cost','rangeAndTarget','duration','frequency','effect')}
    else:ident=f"{r['owner']}.engine[{r['engineIndex']}]";proc={'text':r['text']}
    parts+=['### '+ident,'',r['path'],'',json.dumps(proc,ensure_ascii=False,indent=2),'']
for source in supports:parts+=['### '+source['sourcePath'],'',source['text'],'']
(HERE/'CODEX_DEVICE_LIFECYCLE_CONFERENCE.md').write_text('\n'.join(parts),encoding='utf-8')
print('Prepared74 device/Totem candidates (73lexical+1semantic) plus3 shared paragraphs; NOT submitted.')
