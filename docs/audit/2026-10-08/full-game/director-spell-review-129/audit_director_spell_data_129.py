"""Fresh independent data-only inspector for a complete director return in the observed schema.
No acceptance, no gameplay execution, no supplied modules/scripts. Unexpected schema fails visibly.
"""
from pathlib import Path
import argparse,json,hashlib,copy,sys
sys.stdout.reconfigure(encoding='utf-8')
p=argparse.ArgumentParser();p.add_argument('directory');p.add_argument('report');p.add_argument('identities',nargs='+');a=p.parse_args()
D=Path(__file__).parent.resolve();E=(D/a.directory).resolve();assert E.parent==D
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible'
r=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda b:hashlib.sha256(b).hexdigest()
checks=[];errors=[];timing=[]
def check(n,v):
 checks.append(n)
 if not v:errors.append(n)
def apply(s,ops,reverse=False):
 s=copy.deepcopy(s)
 for op in reversed(ops) if reverse else ops:
  new='before' if reverse else 'after';old='after' if reverse else 'before';path=op['path']
  if path=='':
   assert s==op[old] and op[old+'Exists'] and op[new+'Exists'];s=copy.deepcopy(op[new]);continue
  parts=[t.replace('~1','/').replace('~0','~') for t in path.split('/')[1:]];node=s
  for t in parts[:-1]:node=node[int(t)] if isinstance(node,list) else node[t]
  k=int(parts[-1]) if isinstance(node,list) else parts[-1]
  exists=0<=k<len(node) if isinstance(node,list) else k in node
  assert exists==op[old+'Exists'] and (not exists or node[k]==op[old])
  if op[new+'Exists']:
   if isinstance(node,list) and not exists:assert k==len(node);node.append(copy.deepcopy(op[new]))
   else:node[k]=copy.deepcopy(op[new])
  else:del node[k]
 return s
manifest=r(E/'MANIFEST.json')['files'];actual={p.relative_to(E).as_posix() for p in E.rglob('*') if p.is_file()}
check('complete-unique-manifest',len(manifest)==len({b['path'] for b in manifest}) and {b['path'] for b in manifest}==actual-{'MANIFEST.json'})
for b in manifest:
 p=(E/b['path']).resolve();assert p.is_relative_to(E);raw=p.read_bytes();check('binding:'+b['path'],len(raw)==b['bytes'] and sha(raw)==b['sha256'])
m=r(E/'MODEL.json');procs=r(E/'PROCEDURES.json')['spells'];catalog=r(R/'data/public/spell_playtests/catalog.json');native={s['id']:s for s in catalog['spells']}
check('exact-identity-set',len(m['spells'])==len(a.identities) and {s['id'] for s in m['spells']}==set(a.identities));access=0
for s in m['spells']:
 sid=s['id'];proc=next(v for v in procs if v['spellId']==sid)
 check('complete-current-native:'+sid,s['completeSourceAndAccess']==native[sid]==proc['completeCurrentCatalogSourceAndAccess'])
 check('procedure-mirror:'+sid,s['procedure']==proc['procedure']);check('runtime-disabled:'+sid,s['runtimeSelectionEnabled'] is False);access+=len(native[sid]['classAccess'])
cases={};mains=r(E/'CASEBOOK.json')['completeCases']
def walk(c):
 assert c['id'] not in cases;cases[c['id']]=c
 for b in c['branches']:walk(b)
for c in mains:walk(c)
ops=r(E/'EVENT_REVERSIBLE_OPERATIONS.json')['events'];opmap={e['eventId']:e for e in ops};check('unique-operation-events',len(ops)==len(opmap));events=[]
for cid,c in cases.items():
 if 'forkBinding' in c:
  f=c['forkBinding'];parent=next(e for e in cases[f['parentCase']]['timeline'] if e['id']==f['parentEvent']);check('exact-fork:'+cid,c['initialState']==parent[f['side']])
 prior=c['initialState']
 for e in c['timeline']:
  events.append(e);eid=e['id'];check('continuous:'+eid,prior==e['before']);check('event-time:'+eid,e['after']['time']==e['time'] and e['time']>=e['before']['time'])
  try:
   o=opmap[eid]['operations'];check('forward:'+eid,apply(e['before'],o)==e['after']);check('reverse:'+eid,apply(e['after'],o,True)==e['before'])
  except Exception as ex:errors.append('operations:'+eid+':'+repr(ex))
  for ref in e['sourceReferences']:
   p=(E/ref['file']).resolve();check('source-ref:'+eid+':'+ref['file'],p.is_relative_to(E) and p.is_file())
  for aid,v in e['after']['actors'].items():
   check('resources:'+eid+':'+aid,0<=v['rp']<=v['maxRp'] and 0<=v['hp']<=v['maxHp'])
   before=e['before']['actors'][aid]
   if all(k in before for k in ['wallet','phase','body']):
    phase=before['phase'];start=phase['lastStart'];end=phase['lastEnd'];active=start is not None and (end is None or start>end) and start<=e['time']<=start+phase['turnSeconds']
    spent=[k for k in ['action','bonusAction'] if before['wallet'][k] and not v['wallet'][k]];moved=before['body']!=v['body']
    if (spent or moved) and not active:timing.append({'event':eid,'actor':aid,'time':e['time'],'eventDescription':e['event'],'spent':spent,'moved':moved,'phase':phase,'classification':'Requires independent review: may be legal forced movement, outside-initiative event, or actual defect.'})
  prior=e['after']
 check('final-state:'+cid,prior==c['finalState'])
check('unique-events',len(events)==len({e['id'] for e in events}));check('event-operation-coverage',set(opmap)=={e['id'] for e in events})
result={'status':'DATA_CHECKS_PASS_PENDING_SEMANTIC_REVIEW' if not errors else 'DATA_CHECK_FAILURE','identities':a.identities,'nativeAccessRows':access,'mainCases':len(mains),'branches':len(cases)-len(mains),'events':len(events),'checks':len(checks),'errors':errors,'timingCandidatesForSemanticReview':timing,'canonicalChanges':False,'runtimeExecuted':False,'suppliedCodeExecuted':False}
out=(D/a.report).resolve();assert out.parent==D and not out.exists();out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2))
if errors:sys.exit(1)
