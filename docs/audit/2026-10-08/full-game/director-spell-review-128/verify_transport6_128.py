"""Fresh static inspection of delivered JSON. Does not import or execute supplied code."""
from pathlib import Path
import json,hashlib,zipfile,io,copy,math,datetime
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game';D=A/'director-spell-review-128';S=D/'transport6-return01'
def read(n):return json.loads((S/n).read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def canon(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
checks=0;findings=[]
def ck(v,label,details=None):
 global checks
 checks+=1
 if not v:findings.append({'check':label,'details':details})
def ptr(v,p):
 for k in p.strip('/').split('/'):
  k=k.replace('~1','/').replace('~0','~');v=v[int(k)] if isinstance(v,list) else v[k]
 return v
m=read('MODEL.json');b=read('CASEBOOK.json');pr=read('PROCEDURES.json');work=read('WORK_PHASE_HISTORY.json');refs=read('SOURCE_REFERENCES.json');orig=read('history/ORIGINAL_CANDIDATE.json');sel=m['selectedReview126']
for row in read('MANIFEST.json')['files']:
 raw=(S/row['path']).read_bytes();ck(len(raw)==row['bytes'] and sha(raw)==row['sha256'],'manifest/'+row['path'])
 if row['path'].endswith('.json'):json.loads(raw);ck(True,'json/'+row['path'])
with zipfile.ZipFile(A/'DD_Transport6_Director_Conference_126.zip') as z:
 for row in refs['outerBindings']:
  raw=z.read(row['member']);ck(len(raw)==row['bytes'] and sha(raw)==row['sha256'],'input/'+row['member'])
 raw=z.read(refs['originalArchive']['member']);ck(sha(raw)==refs['originalArchive']['sha256'],'nested archive')
 with zipfile.ZipFile(io.BytesIO(raw)) as nz:
  ck(nz.read('CANDIDATE.json')==(S/'history/ORIGINAL_CANDIDATE.json').read_bytes(),'complete original bytes')
  for row in refs['originalSourceBindings']:
   raw=nz.read(row['member']);ck(len(raw)==row['bytes'] and sha(raw)==row['sha256'],'source/'+row['member'])
out=copy.deepcopy(orig)
ops=read('EXACT_OPERATIONS_FROM_SOURCE.json')['operations']
for op in ops:
 parts=op['pointer'].strip('/').split('/');parent=out
 for k in parts[:-1]:parent=parent[int(k)] if isinstance(parent,list) else parent[k]
 ck(parts[-1] not in parent,'absent original '+op['pointer']);parent[parts[-1]]=copy.deepcopy(ptr(m,op['after']['pointer']))
ck(enc(out)==(S/'MODEL.json').read_bytes(),'full forward bytes')
for op in reversed(ops):
 parts=op['pointer'].strip('/').split('/');parent=out
 for k in parts[:-1]:parent=parent[int(k)] if isinstance(parent,list) else parent[k]
 del parent[parts[-1]]
ck(enc(out)==(S/'history/ORIGINAL_CANDIDATE.json').read_bytes(),'full inverse bytes')
ck(sel['casebook']==b,'complete casebook mirror');ck(sel['sharedRules']==pr['sharedRules'],'shared mirror')
ck(sel['questionDispositions']==read('QUESTION_DISPOSITIONS.json')['questions'],'question mirror')
ck(sel['actorTemplates']==read('ACTOR_TEMPLATES.json')['templates'],'actor mirror')
ck(sel['holds']==read('HOLD_REGISTER.json')['holds'],'hold mirror')
ck(len(pr['spells'])==6 and len(pr['sharedRules'])==6,'procedure/shared counts')
for i,(rec,p) in enumerate(zip(m['records'],pr['spells'])):
 ck(rec['selectedOperationalProcedure126']==p,'procedure mirror '+str(i))
 ck(p['completeOriginalRecordUnchanged']==orig['records'][i]['completeOriginalRecordUnchanged'],'old proposal exact '+str(i))
 ck(p['completeSourceAndAccess']==orig['records'][i]['completeCurrentCatalogSourceAndAccess'],'source/access exact '+str(i))
ck(sum(len(p['completeSourceAndAccess']['classAccess']) for p in pr['spells'])==42,'all42 native access')
questions=read('QUESTION_DISPOSITIONS.json')['questions'];ck(len(questions)==21 and len({q['id'] for q in questions})==21,'all21 answers')
for q in questions:ck(bool(q.get('selectedAnswer')),'answer '+q['id'])
cases=[]
def flatten(c):
 cases.append(c)
 for child in c['branches']:flatten(child)
for c in b['cases']:flatten(c)
ck(len(cases)==33,'33 main and branches');ck(sum(len(c['timeline']) for c in cases)==278,'278 events')
cast_summary=[];digest=[];states=0
def actor_invariants(a,label):
 for key,cap in [('hp','maxHp'),('rp','maxRp')]:ck(0<=a[key]<=a[cap],label+'/'+key)
 ck(a['tempHp']>=0 and a['wounds']>=0 and a['dissonance']>=0,label+'/nonnegative')
 ck(a['currentCarriedMassLb']<=a['carryCapacityLb'] and a['currentLoad']<=a['loadCapacity'],label+'/capacity')
 ck(a['movementSpent']<=a['speed']*(1+a['dashes'])+1e-8,label+'/movement budget')
 ck(a['regularStart']<=a['regularEnd']<a['nextRegularStart'],label+'/schedule')
for c in cases:
 before=c['initialState'];ck(c['status']!='','case status '+c['id']);last=-float('inf');lines=[]
 for ei,e in enumerate(c['timeline']):
  label=c['id']+'/'+str(ei);ck(e['before']==before,label+'/full continuity');ck(e['time']>=last,label+'/chronological');ck(e['after']['time']==e['time'],label+'/after time');last=e['time'];after=e['after'];states+=2
  for stage,state in [('before',before),('after',after)]:
   ck(len(state['eventsApplied'])==len(set(state['eventsApplied'])),label+'/'+stage+'/unique event receipts')
   for aid,a in state['actors'].items():actor_invariants(a,label+'/'+stage+'/'+aid)
  fresh=set(after['castLedger'])-set(before['castLedger'])
  for cid in fresh:
   x=after['castLedger'][cid];aa=before['actors'][x['caster']];bb=after['actors'][x['caster']]
   ck(x['rpBefore']==aa['rp'] and x['rpAfter']==bb['rp'] and aa['rp']-bb['rp']==x['paidRP'],label+'/'+cid+'/actual payment')
   ck(x['paidRP']==x['baseRP']+x['surcharge'],label+'/'+cid+'/price parts')
   ck(x['dissonanceBefore']==aa['dissonance'] and x['dissonanceAfter']==bb['dissonance'],label+'/'+cid+'/strain endpoints')
   ck(bb['dissonance']==aa['dissonance']+x['baseDissonance']+x['refrainAdded'],label+'/'+cid+'/strain sum')
   ck(bb['lastSpell']==x['spellId'],label+'/'+cid+'/latest history')
   ck(x['committedAt']==e['time'],label+'/'+cid+'/commit time')
   ck(x['surcharge']==max(0,aa['dissonance']-11),label+'/'+cid+'/surcharge',x)
   if x['class']=='Wizard':
    expected_base=0 if x['spellId'] not in aa['preparedFamiliesUsed'] and x['spellId']!='class-counterspell' else (0 if x['rank']<=3 else 1 if x['rank']<=5 else 2 if x['rank']<=7 else 3)
    expected_repeat=aa['refrain']+1 if aa['lastSpell']==x['spellId'] else 0
    ck(x['baseDissonance']==expected_base,label+'/'+cid+'/native Wizard baseD',{'actual':x['baseDissonance'],'expected':expected_base})
    ck(x['refrainAdded']==expected_repeat and bb['refrain']==expected_repeat,label+'/'+cid+'/repeat cadence')
   cast_summary.append({'case':c['id'],'event':e['id'],'cast':x})
  changes={}
  for aid,aa in before['actors'].items():
   bb=after['actors'][aid];dd={k:[aa.get(k),bb.get(k)] for k in ['position','hp','rp','dissonance','refrain','action','bonusAction','reaction','interaction','movementSpent','dashes','concentration','hands','carriedObjectIds','currentCarriedMassLb','currentLoad','fall'] if aa.get(k)!=bb.get(k)}
   if dd:changes[aid]=dd
  lines.append({'time':e['time'],'label':e['label'],'changes':changes,'observations':e['observations']})
  before=after
 ck(before==c['finalState'],c['id']+'/full final')
 digest.append({'id':c['id'],'description':c['description'],'premises':c['fixturePremises'],'initialActors':c['initialState']['actors'],'initialObjects':c['initialState']['objects'],'environment':c['initialState']['environment'],'timeline':lines,'finalSources':c['finalState']['sources']})
work_count=0
for tid,t in work['traces'].items():
 events=t['events'];ck(len(events)==200,tid+'/200 work markers');last=t['startedAt'];prior=None
 ck(abs(t['completedThrough']-t['startedAt']-600)<1e-7,tid+'/600 seconds')
 for ei,e in enumerate(events):
  work_count+=1;lab=tid+'/'+str(ei);ck(e['time']>=last,lab+'/time');last=e['time']
  if prior is not None:ck(e['before']==prior,lab+'/continuity')
  actor_invariants(e['before'],lab+'/before');actor_invariants(e['after'],lab+'/after')
  ck(e['before']['rp']==e['after']['rp'] and e['before']['hp']==e['after']['hp'],lab+'/no free resource or new charge')
  if e['kind']=='START':ck(not e['after']['action'],lab+'/work Action consumed')
  prior=e['after']
ck(work_count==1000,'1000 work phase records')
result={'id':'TRANSPORT6-INDEPENDENT-DATA-CHECKS-128','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'findings':findings,'counts':{'cases':len(cases),'events':sum(len(c['timeline']) for c in cases),'states':states,'castingCommitments':len(cast_summary),'workPhaseRecords':work_count},'runtimeExecuted':False,'meaning':'Independent full serialized state/source/cost checks; semantic/source review still required.'}
(D/'TRANSPORT6_DATA_CHECKS_128.json').write_bytes(enc(result));(D/'TRANSPORT6_CAST_DIGEST_128.json').write_bytes(enc(cast_summary));(D/'TRANSPORT6_CASE_DIGEST_128.json').write_bytes(enc(digest));print(json.dumps(result,indent=2)[:15000])
