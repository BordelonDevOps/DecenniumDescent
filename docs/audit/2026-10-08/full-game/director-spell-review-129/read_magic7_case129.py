from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
D=Path(__file__).parent;E=D/'magic7_return02_received';r=lambda n:json.loads((E/n).read_text(encoding='utf-8-sig'))
cs=r('CASEBOOK.json')['completeCases'];ops={o['eventId']:o['operations'] for o in r('EVENT_REVERSIBLE_OPERATIONS.json')['events']}
def concise(v):
 if isinstance(v,dict):return {k:concise(x) for k,x in v.items() if k not in ('sourceBinding','currentIndexEntry','originalBinding')}
 if isinstance(v,list):return [concise(x) for x in v]
 return v
def show(c):
 print('\nCASE',c['id'],c['description'])
 print('ACTORS',json.dumps(c['actorDefinitions']))
 for e in c['timeline']:
  if e['event'].startswith(('actual regular START','actual regular END')) and not e['inputs']:
   special=[o for o in ops[e['id']] if not any(s in o['path'] for s in ['/wallet/','/phase/','/time'])]
   if not special:continue
  row={'id':e['id'],'time':e['time'],'event':e['event'],'inputs':e['inputs'],'observations':e['observations']}
  if len(sys.argv)<4:row['changes']=ops[e['id']]
  print(json.dumps(concise(row),ensure_ascii=False))
 for b in c['branches']:show(b)
for c in cs[int(sys.argv[1]):int(sys.argv[2])]:show(c)
