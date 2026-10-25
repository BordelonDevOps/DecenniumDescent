"""Read-only compact case view; outputs all non-marker observations and initial facts."""
from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
E=Path(__file__).parent/'lifematter5_return01_received'
d=json.loads((E/'CASEBOOK.json').read_text(encoding='utf-8-sig'))
def show(c):
 print('\nCASE',c['id'],c['description']);print('QUALIFICATION',c['wholeCaseQualification']);print('FORK',c.get('forkBinding'))
 for aid,a in c['initialState']['actors'].items():
  print('INITIAL_ACTOR',aid,json.dumps({k:a.get(k) for k in ['template','classLevel','abilities','PB','body','hp','maxHp','tempHp','wounds','injuries','life','conditions','rp','maxRp','dissonance','refrain','phase','concentration','ac','speed','inventory','resistances','immunities','recharge','uses','conviction','NullVeil','deathSaves','stableRecoveryDeadline','type']},ensure_ascii=False,separators=(',',':')))
 print('WORLD',json.dumps(c['initialState']['world'],ensure_ascii=False));print('OBJECTS',json.dumps(c['initialState']['objects'],ensure_ascii=False));print('SOURCES',json.dumps(c['initialState']['sources'],ensure_ascii=False))
 for e in c['timeline']:
  if e['observations'].get('marker') in ['START','END']:continue
  print(e['id'],e['time'],e['event']);print('OBS',json.dumps(e['observations'],ensure_ascii=False,separators=(',',':')))
  if e['inputs']:print('INPUT',json.dumps(e['inputs'],ensure_ascii=False,separators=(',',':')))
 for b in c['branches']:show(b)
for c in d['mainCases']:
 if c['id'] in sys.argv[1:]:show(c)
