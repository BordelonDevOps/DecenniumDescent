"""Fresh independent local data inspector. Never executes supplied return code."""
from pathlib import Path
import json,hashlib,copy,zipfile,sys
sys.stdout.reconfigure(encoding='utf-8')
D=Path(__file__).parent;E=Path(sys.argv[1]) if len(sys.argv)>1 else D/'lifematter5_return01_received';G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda v:(json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode('utf-8')
checks=[];errors=[];timing=[];formatting=[]
def check(label,ok):
 checks.append(label)
 if not ok:errors.append(label)
def apply(state,ops):
 s=copy.deepcopy(state)
 for op in ops:
  parts=[k.replace('~1','/').replace('~0','~') for k in op['path'].split('/')[1:]]
  if not parts:
   assert op['op'] in ['test','replace']
   if op['op']=='test':assert s==op['value']
   else:s=copy.deepcopy(op['value'])
   continue
  n=s
  for k in parts[:-1]:n=n[int(k)] if isinstance(n,list) else n[k]
  k=int(parts[-1]) if isinstance(n,list) else parts[-1]
  exists=0<=k<len(n) if isinstance(n,list) else k in n
  action=op['op']
  if action=='test':assert exists and n[k]==op['value']
  elif action=='testAbsent':assert not exists
  elif action=='replace':assert exists;n[k]=copy.deepcopy(op['value'])
  elif action=='remove':assert exists;del n[k]
  elif action=='add':
   assert not exists
   if isinstance(n,list):assert k==len(n);n.append(copy.deepcopy(op['value']))
   else:n[k]=copy.deepcopy(op['value'])
  else:raise ValueError(action)
 return s
m=read(E/'MANIFEST.json');bindings=m['payload']+[m['bindingFile']]
actual={p.relative_to(E).as_posix() for p in E.rglob('*') if p.is_file()}
check('unique-complete-manifest',len(bindings)==len({b['path'] for b in bindings}) and {b['path'] for b in bindings}==actual-{'MANIFEST.json'})
check('cross-binding-payload',read(E/'ARTIFACT_BINDINGS.json')['bindings']==m['payload'])
for b in bindings:
 raw=(E/b['path']).read_bytes();check('binding:'+b['path'],len(raw)==b['bytes'] and sha(raw)==b['sha256'])
native={s['id']:s for s in read(R/'data/public/spell_playtests/catalog.json')['spells']}
model=read(E/'MODEL.json');procs=read(E/'PROCEDURES.json')['spells'];env=read(E/'PROPOSED_STANDALONE_ENVELOPE.json');ids=['awaken','bone-cage','contagion','disintegrate','telekinesis']
check('exact-five-identities',[s['id'] for s in procs]==ids)
check('model-envelope-procedure-mirrors',model['completeProcedures']==procs==env['spells'])
access=0
for s in procs:
 check('current-native:'+s['id'],s['completeSourceAndAccess']==native[s['id']]);access+=len(native[s['id']]['classAccess'])
 check('procedure-markdown-mirror:'+s['id'],s['procedure'].strip() in (E/'procedures'/f"{s['id']}.md").read_text(encoding='utf-8'))
for row in read(E/'NATIVE_ACCESS_RECORDS.json')['records']:check('native-record:'+row['spellId'],row['completeNativeAndAccessUnchanged']==native[row['spellId']])
check('runtime-not-claimed',model['runtimeExecuted'] is False and env['runtimeImplemented'] is False)
for name,relative in [('NATIVE_CATALOG.json','data/public/spell_playtests/catalog.json'),('CURRENT_INDEX_129.json','data/public/spell_playtests/authored_review_index.json'),('WIZARD_CLASS_FULL.json','data/public/class_playtests/wizard.json'),('RANGER_CLASS_FULL.json','data/public/class_playtests/ranger.json'),('WARRIOR_CLASS_FULL.json','data/public/class_playtests/warrior.json'),('CLERIC_CLASS_FULL.json','data/public/class_playtests/cleric.json'),('EXPEDITION_FULL.json','data/public/expedition_candidate/complete_candidate.json')]:
 same_bytes=(E/'evidence'/name).read_bytes()==(R/relative).read_bytes()
 if name=='CURRENT_INDEX_129.json' and not same_bytes and (D/'LIFEMATTER4_APPLICATION_VALIDATION_129.json').exists():
  app=read(D/'LIFEMATTER4_APPLICATION_VALIDATION_129.json');baseline=D/'authored_review_index.before_lifematter4_129.json'
  check('index-is-exact-authored-baseline-before-four-accepted-applications',(E/'evidence'/name).read_bytes()==baseline.read_bytes() and sha((R/relative).read_bytes())==app['index']['sha256'] and app['disintegrateUnchangedAndPending'])
  formatting.append({'file':name,'kind':'HISTORICAL_AUTHORING_BASELINE','sourceCounts':read(E/'evidence'/name)['authoredCounts'],'currentCounts':read(R/relative)['authoredCounts'],'authority':'LIFEMATTER4_APPLICATION_VALIDATION_129.json; all844 unrelated entries unchanged, including Disintegrate.','notSourceDrift':True});continue
 check('complete-current-source-json:'+name,read(E/'evidence'/name)==read(R/relative))
 if not same_bytes:formatting.append({'file':name,'currentJsonExact':True,'byteIdentical':False,'originalBytesStillPreservedInInputArchives':True})
for source in read(E/'SOURCE_PRESERVATION.json')['inputs']:
 p=E/source['path'];raw=p.read_bytes();check('input-archive:'+source['path'],len(raw)==source['bytes'] and sha(raw)==source['sha256'])
 with zipfile.ZipFile(p) as z:
  declared=source['allOriginalMembers'];check('input-member-list:'+p.name,{i.filename for i in z.infolist() if not i.is_dir()}=={b['member'] for b in declared})
  for b in declared:
   raw=z.read(b['member']);check('input-member:'+p.name+':'+b['member'],len(raw)==b['bytes'] and sha(raw)==b['sha256'])
original=read(E/'history/ORIGINAL_CANDIDATE.json');mains=read(E/'CASEBOOK.json')['mainCases'];cases={}
def walk(c):
 assert c['id'] not in cases;cases[c['id']]=c
 for b in c['branches']:walk(b)
for c in mains:walk(c)
check('all-original-cases',{c['id'] for c in mains}=={c['id'] for c in original['allOriginalScenarios']})
for c in mains:
 check('original-scenario:'+c['id'],c['originalScenario']==next(x for x in original['allOriginalScenarios'] if x['id']==c['id']))
 check('full-case-file:'+c['id'],c==read(E/'cases'/f"{c['id']}.json"))
opcases=read(E/'EVENT_OPERATIONS.json')['cases'];opmap={o['eventId']:o for c in opcases for o in c['events']};events=[]
for cid,c in cases.items():
 if 'forkBinding' in c:
  f=c['forkBinding'];p=next(e for e in cases[f['parentCase']]['timeline'] if e['id']==f['parentEvent']);check('exact-fork:'+cid,c['initialState']==p[f['side']])
 prior=c['initialState']
 for e in c['timeline']:
  eid=e['id'];events.append(eid);check('continuous:'+eid,prior==e['before']);check('time:'+eid,e['after']['time']==e['time'] and e['time']>=e['before']['time'])
  o=opmap[eid]
  try:
   check('forward:'+eid,apply(e['before'],o['forward'])==e['after']);check('inverse:'+eid,apply(e['after'],o['inverse'])==e['before'])
  except Exception as ex:errors.append('operations:'+eid+':'+repr(ex))
  check('before-hash:'+eid,sha(canon(e['before']))==o['beforeCanonicalDataSha256']);check('after-hash:'+eid,sha(canon(e['after']))==o['afterCanonicalDataSha256'])
  for ref in e['sourceReferences']:
   p=(E/ref['file']).resolve();check('source-ref:'+eid+':'+ref['file'],p.is_relative_to(E.resolve()) and p.is_file())
  for aid,v in e['after']['actors'].items():
   check('resource-bounds:'+eid+':'+aid,0<=v['rp']<=v['maxRp'] and 0<=v['hp']<=v['maxHp'] and v['tempHp']>=0)
   if aid not in e['before']['actors']:continue
   b=e['before']['actors'][aid];p=b['phase'];start=p['lastStart'];end=p['lastEnd'];active=start is not None and (end is None or start>end) and start<=e['time']<=start+p['turnSeconds']
   spent=[k for k in ['action','bonusAction'] if b['wallet'][k] and not v['wallet'][k]]
   moved=b['body']!=v['body']
   if (spent or moved) and not active:timing.append({'event':eid,'actor':aid,'time':e['time'],'description':e['event'],'spent':spent,'bodyChanged':moved,'phase':p,'note':'Manual classification required; forced motion/anatomy change/outside-initiative may be legal.'})
  prior=e['after']
 check('final:'+cid,prior==c['finalState'])
check('unique-complete-event-operations',len(events)==len(set(events))==len(opmap) and set(events)==set(opmap))
result={'status':'DATA_PASS_PENDING_SEMANTIC_REVIEW' if not errors else 'DATA_FINDINGS_REQUIRE_REVIEW','checks':len(checks),'errors':errors,'nativeAccessRows':access,'mainCases':len(mains),'branches':len(cases)-len(mains),'events':len(events),'timingCandidates':timing,'sourceFormattingDifferences':formatting,'eventHashEncoding':'UTF8 JSON insertion order, indent2, ensure_ascii=False, one terminal LF; independently matched actual event data. Prior inspector wrongly assumed sorted compact JSON.','canonicalChanges':False,'runtimeExecuted':False,'suppliedCodeExecuted':False}
out=Path(sys.argv[2]) if len(sys.argv)>2 else D/'LIFEMATTER5_RETURN01_INDEPENDENT_DATA_AUDIT_V2_129.json';assert not out.exists();out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k!='timingCandidates'},indent=2));print('Timing candidates requiring semantic classification:',len(timing))
if errors:sys.exit(1)
