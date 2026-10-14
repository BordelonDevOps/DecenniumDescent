"""Check the currently operational78 spells for a missing recurrence interface."""
from pathlib import Path
import json,re,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
rows=[];seen=[]
for filename in ('batch_1.json','batch_2.json','batch_3.json','batch_healing_death.json'):
    path=ROOT/'data/playtest/spell_drafts'/filename
    data=json.loads(path.read_text(encoding='utf-8'))
    for spell in data['spells']:
        seen.append(spell['id'])
        text=' '.join(str(spell.get(k,'')) for k in ('activation','duration','effect','limitations','resolution'))
        if re.search(r'heal|regain.{0,30}HP|restore.{0,30}HP|regenerat|repair',text,re.I) and re.search(r'pulse|each.{0,20}turn|start of.{0,30}turn|zone|aura|maintenance',text,re.I):
            rows.append({'sourcePath':path.relative_to(ROOT).as_posix(),'sourceId':spell['id'],
                         'sourceObject':spell,'sourceObjectSha256':hashlib.sha256(json.dumps(spell,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()})
assert len(seen)==len(set(seen))==78
report={'status':'SOURCE_CANDIDATES','scannedOperationalIds':78,'scope':'Lexical recurrence/healing intersection in the78 currently operational spell drafts. Includes exclusions;770 unfinished catalog IDs not reviewed by this scan.','candidates':rows}
(HERE/'OPERATIONAL_SPELL_PULSE_SCAN.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Scanned78 operational spell drafts;',len(rows),'lexical candidates.')
for r in rows: print(r['sourceId'],r['sourceObject']['effect'])
