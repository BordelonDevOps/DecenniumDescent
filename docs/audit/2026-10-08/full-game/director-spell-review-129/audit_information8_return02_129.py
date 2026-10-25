"""Fresh independent data inspection of Information8. No supplied program is executed."""
from pathlib import Path
import json,hashlib,copy,sys,re,zipfile
sys.stdout.reconfigure(encoding='utf-8')
D=Path(__file__).parent;E=D/'information8_return02_received';G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda x:json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
checks=[];errors=[];timing=[];casts=[];snapshots=0;cache={}
def check(k,ok):
 checks.append(k)
 if not ok:errors.append(k)
def get(v,path):
 for k in path.split('/')[1:]:
  k=k.replace('~1','/').replace('~0','~');v=v[int(k)] if isinstance(v,list) else v[k]
 return v
def exists(v,path):
 try:get(v,path);return True
 except (KeyError,IndexError):return False
def apply(v,d):
 s=copy.deepcopy(v)
 for guard in d['absenceGuards']:assert guard['mustBeAbsent'] and not exists(s,guard['path'])
 for o in d['operations']:
  path=o['path'];parts=path.split('/')[1:]
  if not parts:
   assert o['op'] in ['test','replace']
   if o['op']=='test':assert s==o['value']
   else:s=copy.deepcopy(o['value'])
   continue
  n=get(s,'/'+ '/'.join(parts[:-1])) if len(parts)>1 else s
  k=parts[-1].replace('~1','/').replace('~0','~');k=int(k) if isinstance(n,list) else k
  has=0<=k<len(n) if isinstance(n,list) else k in n
  if o['op']=='test':assert has and n[k]==o['value']
  elif o['op']=='replace':assert has;n[k]=copy.deepcopy(o['value'])
  elif o['op']=='remove':assert has;del n[k]
  elif o['op']=='add':
   assert not has
   if isinstance(n,list):assert k==len(n);n.append(copy.deepcopy(o['value']))
   else:n[k]=copy.deepcopy(o['value'])
  else:raise ValueError(o['op'])
 return s
def resolve(ref):
 f=ref['file'];p=(E/f).resolve();assert p.is_relative_to(E.resolve()) and p.is_file()
 if not f.endswith('.json'):return None
 if f not in cache:cache[f]=read(p)
 v=cache[f]
 if 'pointer' in ref:return get(v,ref['pointer'])
 if 'key' in ref:return v[ref['key']]
 return v
native={s['id']:s for s in read(R/'data/public/spell_playtests/catalog.json')['spells']}
templates=read(E/'ACTOR_TEMPLATES.json');procs=read(E/'PROCEDURES.json')['spells'];original=read(E/'history/ORIGINAL_CANDIDATE.json');follow=read(E/'history/ORIGINAL_FOLLOWUPS.json')
ids=['arcane-eye','concordant-mindlink','faction-prophecy','faction-destiny','find-the-path','legend-lore','prophetic-frenzy','resonance-prophecy']
check('eight-exact-identities',[s['id'] for s in procs]==ids)
for s in procs:
 sid=s['id'];check('native:'+sid,s['completeNativeSourceAndAccess']==native[sid]);check('json-mirror:'+sid,read(E/'procedures'/f'{sid}.json')==s)
 check('markdown-mirror:'+sid,s['procedure'].strip() in (E/'procedures'/f'{sid}.md').read_text(encoding='utf-8'))
 row=next(x for x in original['records'] if x['spellId']==sid)
 check('original-procedure:'+sid,s['completeOriginalProcedureUnchanged']==row['completeOriginalRecordUnchanged']['procedure'])
for row in read(E/'NATIVE_ACCESS_RECORDS.json'):check('native-access:'+row['id'],row['completeNativeSourceAndAccess']==native[row['id']])
for f,p in [('NATIVE_CATALOG.json','data/public/spell_playtests/catalog.json'),('CURRENT_INDEX.json','data/public/spell_playtests/authored_review_index.json'),('WIZARD_CLASS_FULL.json','data/public/class_playtests/wizard.json')]:check('current-source:'+f,read(E/'evidence'/f)==read(D/'authored_review_index.before_information4_129.json' if f=='CURRENT_INDEX.json' else R/p))
for f,p in [('DD_Information8_Director_Conference_127.zip',D.parent/'DD_Information8_Director_Conference_127.zip'),('DD_EyeJudgement1_Director_Conference_127_SOURCE_ONLY.zip',D.parent/'DD_EyeJudgement1_Director_Conference_127.zip'),('DD_Disintegrate_Applied_Context_129.zip',D/'DD_Disintegrate_Applied_Context_129.zip')]:check('source-archive:'+f,sha(zipfile.ZipFile(E/'history/DD_Information8_Director_Return01_131.zip').read('history/'+f))==sha(p.read_bytes()))
questions=original['questions']+follow['reviewRequirements'];q=read(E/'QUESTION_DISPOSITIONS.json')
check('unique-question-dispositions',len(q)==25 and len({x['id'] for x in q})==25)
check('exact-original-questions',{x['id']:x['completeOriginalQuestion'] for x in q}=={x['id']:x for x in questions})
mains=read(E/'CASEBOOK.json')['mainCases'];cases={}
def walk(c):
 assert c['id'] not in cases;cases[c['id']]=c
 for b in c['branches']:walk(b)
for c in mains:walk(c)
check('exact-16-original-case-ids',{c['id'] for c in mains}=={c['id'] for c in original['allOriginalScenarios']})
for c in mains:
 check('original-case:'+c['id'],c['originalScenarioCompleteUnchanged']==next(x for x in original['allOriginalScenarios'] if x['id']==c['id']))
 check('full-case-mirror:'+c['id'],c==read(E/'cases'/f"{c['id']}.json"))
ops=read(E/'EVENT_OPERATIONS.json');check('unique-operation-records',len(ops)==len({o['eventId'] for o in ops}));opmap={o['eventId']:o for o in ops};events=[]
for cid,c in cases.items():
 if 'forkBinding' in c:
  f=c['forkBinding'];p=next(e for e in cases[f['parentCase']]['timeline'] if e['id']==f['parentEvent']);check('exact-fork:'+cid,c['initialState']==p[f['side']] and sha(canon(c['initialState']))==f['exactParentStateSha256'])
 prior=c['initialState']
 for e in c['timeline']:
  eid=e['id'];events.append(eid);o=opmap[eid];before=e['before'];after=e['after']
  check('continuity:'+eid,prior==before);check('time:'+eid,after['time']==e['time'] and e['time']>=before['time']);check('operation-identity:'+eid,o['caseId']==cid and e['operationRecordId']==eid)
  try:check('forward:'+eid,apply(before,o['forward'])==after);check('inverse:'+eid,apply(after,o['inverse'])==before)
  except Exception as ex:check('operation-error:'+eid+':'+repr(ex),False)
  check('before-hash:'+eid,sha(canon(before))==o['expectedBeforeSha256']==e['beforeStateSha256']);check('after-hash:'+eid,sha(canon(after))==o['expectedAfterSha256']==e['afterStateSha256'])
  for change in o['fullValueChanges']:
   path=change['path'];kind=change['kind']
   check('full-value-before:'+eid+path,(not exists(before,path)) if kind=='add' else get(before,path)==change['before'])
   check('full-value-after:'+eid+path,(not exists(after,path)) if kind=='remove' else get(after,path)==change['after'])
  for ref in e['sourceReferences']:
   try:resolve(ref);check('source-reference:'+eid+str(ref),True)
   except Exception as ex:check('source-reference:'+eid+str(ref)+repr(ex),False)
  for aid,a in after['actors'].items():
   snapshots+=1;t=templates[a['template']];expected='force' if a['classLevel']>=6 else None
   check('resource-bounds:'+eid+':'+aid,0<=a['rp']<=a['maxRp'] and 0<=a['hp']<=a['maxHp'] and a['tempHp']>=0)
   check('actual-Ward:'+eid+':'+aid,t['arcaneWard']==expected and a['resistances']==(['force'] if expected else []))
   if aid not in before['actors']:continue
   b=before['actors'][aid];p=b['phase'];start=p['lastStart'];end=p['lastEnd'];active=start is not None and (end is None or start>end) and start<=e['time']<=start+p['turnSeconds']
   spent=[k for k in ['action','bonusAction'] if b['wallet'][k] and not a['wallet'][k]];moved=b['body']!=a['body']
   if (spent or moved) and not active:timing.append({'event':eid,'actor':aid,'time':e['time'],'eventText':e['event'],'spent':spent,'bodyChanged':moved,'phase':p})
  for castid,x in after['castLedger'].items():
   if castid in before['castLedger']:continue
   k=eid+':'+castid;a=before['actors'][x['caster']];b=after['actors'][x['caster']];t=templates[a['template']];n=x['nativeAccess'];rank=n['rank'];sid=x['spellId'];act=x['actualAction'];casts.append({'event':eid,'id':castid,'spell':sid,'actor':x['caster'],'action':act,'rp':x['finalRPPaid']})
   check('cast-RP:'+k,a['rp']-b['rp']==x['finalRPPaid']==x['baseRP']+x['surcharge'])
   if a['phase']['active'] or act!='action':check('cast-wallet:'+k,a['wallet'][act] and not b['wallet'][act])
   else:check('outside-initiative-paid-action-spacing:'+k,a['lastPaidActionAt'] is None or e['time']-a['lastPaidActionAt']>=6)
   check('cast-level:'+k,a['classLevel']>=n['minimumClassLevel']);check('cast-life:'+k,a['life']=='living' and not any(q in a['conditions'] for q in ['Unconscious','Stunned','Incapacitated','Petrified']))
   ref=x['sourceBinding'];source=resolve(ref);check('cast-source-id:'+k,source.get('id',source.get('spellId'))==sid)
   if x['route']=='actual ordinary Wizard preparation':
    check('cast-native-placement:'+k,n==native[sid]['classAccess']['Wizard']);check('cast-native-baseRP:'+k,x['baseRP']==n['baseRpCost']);check('cast-repertoire:'+k,sid in (a['knownCantrips'] if rank==0 else a['prepared']) and (rank==0 or sid in a['book']))
   else:
    check('class-acquired:'+k,source in [q['completeCard'] for q in t['selectedAcquisition']]+t['automaticCards']);match=re.search(r'(\d+) RP',source['cost']);check('class-cost-rank:'+k,bool(match) and int(match[1])==x['baseRP'] and source['spellRank']==rank)
   refrain=min(3,a['refrain']+1) if a['lastSpell']==sid else 0
   base=0 if rank==0 or (a['phase']['active'] and sid not in a['familiesUsed']) else 1 if rank<=5 else 2
   check('cast-Refrain:'+k,x['RefrainAdded']==refrain==b['refrain']);check('cast-baseD:'+k,x['baseDissonance']==base);check('cast-D:'+k,b['dissonance']==a['dissonance']+base+refrain==x['dissonanceAfter']);check('cast-history:'+k,b['lastSpell']==sid and b['familiesUsed']==a['familiesUsed']+([] if sid in a['familiesUsed'] else [sid]))
   surcharge=0 if rank==0 or a['dissonance']<a['limit'] else 1 if a['dissonance']<a['limit']+3 else 2
   check('cast-strain:'+k,(rank==0 or a['dissonance']<a['limit']+6) and x['surcharge']==surcharge)
  prior=after
 check('final-state:'+cid,prior==c['finalState'])
check('all-event-operations',len(events)==len(set(events))==len(ops) and set(events)==set(opmap))
result={'status':'DATA_PASS_SEMANTIC_REVIEW_REQUIRED' if not errors else 'INDEPENDENT_DATA_FINDINGS','checks':len(checks),'errors':errors,'mainCases':len(mains),'branches':len(cases)-len(mains),'events':len(events),'actualCasts':len(casts),'actorAfterSnapshots':snapshots,'casts':casts,'timingCandidates':timing,'eventHashEncoding':'UTF8 sorted compact JSON, ensure_ascii=False, no terminal LF','canonicalChanges':False,'runtimeExecuted':False,'suppliedProgramsExecuted':False}
(D/'INFORMATION8_RETURN02_INDEPENDENT_DATA_AUDIT_129.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ['casts','timingCandidates']},indent=2));print('timingCandidates',len(timing))
if errors:sys.exit(1)
