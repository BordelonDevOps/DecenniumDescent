"""Extract source evidence for the all-class draft without changing source books."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]; MAIN=ROOT.parents[1]
source=MAIN/'docs/reference/Player_Rulebook_v6_source_text.txt'
lines=source.read_text(encoding='utf-8').splitlines()
starts={'Bard':1788,'Cleric':1937,'Crimson Agent':2096,'Dragoon':2247,'Druid':2398,'Mage':2856,'Mirrorsage':3035,'Monk':3194,'Oracle':3357,'Paladin':3607,'Ranger':3803,'Shaman':3977,'Soldier':4157,'Thief':4337,'Tinker':4542,'Warrior':4752,'Wizard':5106}
out=ROOT/'data/playtest/class_sources';out.mkdir(parents=True,exist_ok=True)
matrix=json.loads((MAIN/'docs/audit/2026-10-08/ADVANCEMENT_MATRIX.json').read_text(encoding='utf-8'))
for n,(name,start) in enumerate(starts.items()):
 end=list(starts.values())[n+1]-1 if n+1<len(starts) else 5386
 rows=[{'line':i+1,'text':lines[i]} for i in range(start-1,end)]
 record={'class':name,'sourcePath':'docs/reference/Player_Rulebook_v6_source_text.txt','sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'bookLines':rows,'mainRegistry':next(c for c in matrix['main']['classes'] if c['class']==name),'v72Registry':next(c for c in matrix['v7_2']['classes'] if c['class']==name)}
 (out/(name.lower().replace(' ','-')+'.json')).write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Prepared 17 full book sections and both registry comparisons')
