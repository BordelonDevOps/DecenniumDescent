from pathlib import Path
import json,hashlib,copy,zipfile,sys
sys.stdout.reconfigure(encoding='utf-8')
D=Path(__file__).parent;E=D/'magic7_return02_received';G=Path(r'C:\Github\DecenniumDescent')
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda b:hashlib.sha256(b).hexdigest()
checks=[];errors=[]
def check(name,ok):
 checks.append(name)
 if not ok:errors.append(name)
def ptr(o,p):
 for t in p.strip('/').split('/') if p else []:
  t=t.replace('~1','/').replace('~0','~');o=o[int(t)] if isinstance(o,list) else o[t]
 return o
def apply(state,ops,rev=False):
 s=copy.deepcopy(state)
 for op in reversed(ops) if rev else ops:
  side='before' if rev else 'after';prior='after' if rev else 'before';parts=op['path'].split('/')[1:];node=s
  for t in parts[:-1]:node=node[int(t)] if isinstance(node,list) else node[t.replace('~1','/').replace('~0','~')]
  k=parts[-1].replace('~1','/').replace('~0','~');exists=k in node
  assert exists==op[prior+'Exists'] and (not exists or node[k]==op[prior])
  if op[side+'Exists']:node[k]=copy.deepcopy(op[side])
  else:del node[k]
 return s
for b in read(E/'MANIFEST.json')['files']:
 v=(E/b['path']).read_bytes();check('binding:'+b['path'],len(v)==b['bytes'] and sha(v)==b['sha256'])
with zipfile.ZipFile(D/'DD_Part6_Magic7_Continuation_129.zip') as z:
 for n in z.namelist():check('preserved-input:'+n,(E/'history/input129'/n).read_bytes()==z.read(n))
model=read(E/'MODEL.json');procs=read(E/'PROCEDURES.json')['spells'];candidate=read(E/'evidence/ORIGINAL_CANDIDATE.json')
current=read(G/'DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json');byid={s['id']:s for s in current['spells']}
for s in model['spells']:
 p=next(v for v in procs if v['spellId']==s['id']);o=next(v for v in candidate['records'] if v['spellId']==s['id'])
 check('native:'+s['id'],s['completeSourceAndAccess']==byid[s['id']]==p['completeCurrentCatalogSourceAndAccess'])
 check('procedure-mirror:'+s['id'],s['procedure']==p['procedure'])
 check('original-record:'+s['id'],p['completeOriginalRecordUnchanged']==o['completeOriginalRecordUnchanged'])
 check('runtime-disabled:'+s['id'],s['runtimeSelectionEnabled'] is False)
ops=read(E/'EVENT_REVERSIBLE_OPERATIONS.json')['events'];opmap={o['eventId']:o for o in ops};check('unique-op-events',len(opmap)==len(ops))
cases=read(E/'CASEBOOK.json')['completeCases'];allcases=[]
def visit(c):
 allcases.append(c)
 for b in c['branches']:visit(b)
for c in cases:visit(c)
events=[]
for c in allcases:
 prev=c['initialState']
 for e in c['timeline']:
  events.append(e);check('continuity:'+e['id'],e['before']==prev)
  check('monotone:'+e['id'],e['after']['time']==e['time'] and e['time']>=e['before']['time'])
  o=opmap[e['id']]
  try:check('forward:'+e['id'],apply(e['before'],o['operations'])==e['after']);check('reverse:'+e['id'],apply(e['after'],o['operations'],True)==e['before'])
  except Exception as exc:errors.append('operation:'+e['id']+':'+repr(exc))
  for ref in e['sourceReferences']:check('source-ref:'+e['id']+':'+ref['file'],(E/ref['file']).is_file())
  for aid,a in e['after']['actors'].items():
   check('resources:'+e['id']+':'+aid,0<=a['rp']<=a['maxRp'] and 0<=a['hp']<=a['maxHp'])
  prev=e['after']
 check('final-state:'+c['id'],prev==c['finalState'])
check('all-event-operations',set(opmap)=={e['id'] for e in events})
report={'status':'DATA_CHECKS_PASS_PENDING_SEMANTIC_REVIEW' if not errors else 'DATA_CHECK_FAILURE','mainCases':len(cases),'branches':len(allcases)-len(cases),'events':len(events),'checks':len(checks),'errors':errors,'canonicalChanges':False,'runtimeExecuted':False}
(D/'MAGIC7_INDEPENDENT_DATA_AUDIT_129.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2))
if errors:sys.exit(1)
