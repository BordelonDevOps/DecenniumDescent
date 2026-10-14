from pathlib import Path
import json,re,hashlib,zipfile
import xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent
GAME=HERE.parents[3]
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
pattern=re.compile(r'\b(?:resurrect\w*|reviv\w*|willing soul|return.{0,25}life|restore.{0,20}life|instant death|massive damage|healing|temporary hit points)\b',re.I)
result=[]
for rel in ('books/player/Decennium_Descent_Player_Rulebook_v6.docx','books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx'):
 p=GAME/rel
 with zipfile.ZipFile(p) as z:root=ET.fromstring(z.read('word/document.xml'))
 ps=[''.join(e.itertext()) for e in []] # text nodes, not XML whitespace
 ps=[''.join(t.text or '' for t in el.iter(W+'t')) for el in root.iter(W+'p')]
 matches=[{'paragraph':i,'text':s,'before':ps[max(0,i-2):i],'after':ps[i+1:i+3]} for i,s in enumerate(ps) if pattern.search(s)]
 result.append({'path':rel,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'paragraphIndex':'zero-based all w:p descendants','matches':matches})
(HERE/'HEALING_DEATH_CORE_EVIDENCE.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for b in result:
 print(b['path'],len(b['matches']))
 for m in b['matches']:
  if len(m['text'])>180 and ('hit point' in m['text'].lower() or 'dead' in m['text'].lower() or 'soul' in m['text'].lower()):
   print(m['paragraph'],m['text'])
