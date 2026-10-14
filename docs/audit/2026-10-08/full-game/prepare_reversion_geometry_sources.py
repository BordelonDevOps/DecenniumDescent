"""Verify geometry quotations against the original DOCX files; no new rule."""
from pathlib import Path
import hashlib
import json
import re
from zipfile import ZipFile
import xml.etree.ElementTree as ET
AUDIT=Path(__file__).resolve().parent;GAME=AUDIT.parents[3];ROOT=GAME/'DescentReviewChanges/ReviewBible'
prior=json.loads((AUDIT/'COMBAT_ACTION_VISION_SOURCE_PACKET.json').read_text(encoding='utf-8'))
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
records=[]
pattern=re.compile(r'squeez|two sizes|creature.s space|creatures occupy space|forced movement|combat uses feet',re.I)
for book in prior:
    path=GAME/book['path'];actual_hash=hashlib.sha256(path.read_bytes()).hexdigest()
    assert actual_hash==book['sha256'],('Original source file changed',str(path))
    with ZipFile(path) as z:xml=ET.fromstring(z.read('word/document.xml'))
    paras=[''.join(p.itertext()) for p in []]  # only w:t content below, excluding XML metadata
    paras=[''.join(t.text or '' for t in p.findall('.//w:t',ns)) for p in xml.findall('.//w:p',ns)]
    for passage in book['paragraphs']:
        if not pattern.search(passage['text']):continue
        p=passage['paragraph'];quoted=passage['text'];live=paras[p]
        normalize=lambda t:re.sub(r'\s+',' ',t).strip()
        assert normalize(live)==normalize(quoted),(book['path'],p)
        records.append({'path':book['path'],'sourceFileSha256':actual_hash,
                        'paragraphIndexConvention':'zero-based all XML w:p descendants, including table cells',
                        'paragraph':p,'exactText':live,'priorQuotedText':quoted})
data={'status':'PREPARED / general mandatory-reversion placement conference not yet submitted',
      'scope':'Verified existing movement/space/squeeze rules; they do not answer involuntary growth overlap by themselves',
      'verifiedPassages':len(records),'records':records,
      'openQuestions':'MANDATORY_REVERSION_GEOMETRY_PREPARATION.md'}
(AUDIT/'MANDATORY_REVERSION_GEOMETRY_SOURCES.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'verifiedPassages':len(records),'paragraphs':[(r['path'],r['paragraph']) for r in records]}))
