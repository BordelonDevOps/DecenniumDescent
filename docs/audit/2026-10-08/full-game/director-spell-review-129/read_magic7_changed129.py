from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
D=Path(__file__).parent;E=D/'magic7_return03_received';P=D/'magic7_return02_received'
r=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def flat(cs):
 out={}
 def walk(c):
  out[c['id']]=c
  for b in c['branches']:walk(b)
 for c in cs:walk(c)
 return out
new=flat(r(E/'CASEBOOK.json')['completeCases']);old=flat(r(P/'CASEBOOK.json')['completeCases']);ops={o['eventId']:o['operations'] for o in r(E/'EVENT_REVERSIBLE_OPERATIONS.json')['events']}
def clean(v):
 if isinstance(v,dict):return {k:clean(x) for k,x in v.items() if k not in ('sourceBinding','currentIndexEntry','originalBinding')}
 if isinstance(v,list):return [clean(x) for x in v]
 return v
for cid in sys.argv[1:]:
 c=new[cid];prior=old[cid];print('CASE',cid,c['description']);print('ACTORS',json.dumps(c['actorDefinitions']));print('INITIAL',json.dumps(clean(c['initialState']),ensure_ascii=False) if '--initial' in sys.argv else 'not printed')
 oldevents={e['id']:e for e in prior['timeline']}
 for e in c['timeline']:
  if e==oldevents.get(e['id']):continue
  row={'id':e['id'],'time':e['time'],'event':e['event'],'inputs':e['inputs'],'observations':e['observations'],'changes':ops[e['id']]}
  print(json.dumps(clean(row),ensure_ascii=False))
