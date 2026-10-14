"""Preserve the unclassified remainder of the original230 lexical candidates."""
from pathlib import Path
from collections import Counter
import json
HERE=Path(__file__).resolve().parent
def read(name):return json.loads((HERE/name).read_text(encoding='utf-8'))
def ident(row):
    return row['card']['id'] if row['kind']=='class-card' else f"{row['owner']}.engine[{row['engineIndex']}]"
broad=read('COMPANION_LIFECYCLE_SOURCE_CANDIDATES.json')
known={ident(r) for name in ('DEVICE_LIFECYCLE_SOURCE_CANDIDATES.json','CREATURE_LIFECYCLE_SOURCE_CANDIDATES.json')
       for r in read(name)['classRecords']}
rows=[r for r in broad['classRecords'] if ident(r) not in known]
assert len(rows)==74 and len({ident(r) for r in rows})==74
data={'status':'UNREVIEWED_SOURCE_CANDIDATES',
      'scope':'74 remaining exact passages from original230 lexical inventory after excluding previously supplied73 device/Totem and83 five-family creature passages. Contains incidental guards/tempHP and earlier-reviewed roles; no completeness or closure claim.',
      'counts':dict(Counter(r['owner'] for r in rows)),'classRecords':rows,
      'supportingSources':broad.get('supportingSources',[])}
(HERE/'REMAINING_LIFECYCLE_SOURCE_CANDIDATES.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Preserved74 remaining lexical candidates across9 families, unreviewed.')
