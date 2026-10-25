from pathlib import Path
import json,hashlib,math
A=Path(r'C:\Github\DecenniumDescent\docs\audit\2026-10-08\full-game');P=A/'rank7-mechanics16-partC-120';O=A/'spell-review-resume-116'
def read(p):return json.loads(p.read_bytes())
checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)})
def walk(x):
 if isinstance(x,dict):
  yield x
  for v in x.values():yield from walk(v)
 elif isinstance(x,list):
  for v in x:yield from walk(v)
for f in read(P/'MANIFEST.json')['files']:
 b=(P/f['path']).read_bytes();ck('manifest '+f['path'],len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'])
m=read(P/'MODEL_PART_C.json');cb=read(P/'CASEBOOK_PART_C.json');cases=[x for c in cb['cases'] for x in [c,*c['independentBranches']]];by={c['id']:c for c in cases}
for k,n in [('all16CompleteDraftProceduresUnchanged','PROCEDURES.json'),('sixSharedClausesUnchanged','SHARED_RULES.json'),('all33QuestionDispositionsUnchanged','QUESTION_DISPOSITIONS.json')]:
 ck('literal '+n,m[k]==read(A/'rank7-mechanics16-partA-117'/n)==read(P/'inherited'/n))
ck('model casebook',m['currentPartCCases']==cb['cases']);ck('actual counts',(len(cb['cases']),len(cases),sum(len(c['timeline']) for c in cases))==(8,13,77))
saves=casts=0
for c in cases:
 prev=c['initialState']
 for e in c['timeline']:
  tag=c['id']+'/'+str(e['index']);pre=e['stateAtEventAfterScheduledProcessing'];post=e['after']
  ck(tag+' continuity',e['before']==prev);ck(tag+' chronological',e['time']>=prev['time'] and post['time']==e['time'])
  for a in post['actors'].values():
   ck(tag+' bounds '+a.get('actorId',''),0<=a['HP']<=a['effectiveMaxHP']<=a['maxHP'] and 0<=a['RP']<=a['maxRP'] and a['tempHP']>=0)
   d=a.get('derived',{})
   if d.get('slowEnchantment'):
    ck(tag+' full Slow '+a['actorId'],a['Speed']==a['normalSpeed']/2 and a['AC']==a['normalAC']-2 and a['saveBonuses']['DEX']==a['nativeSaveBonuses']['DEX']-2 and d['fullActionCeiling']==1 and not d['noReactionsFromSlow'])
  for r in walk(e['resolution']):
   if r.get('kind')=='binary-save':
    saves+=1;a=pre['actors'][r['target']];ck(tag+' binary save '+r['target'],1<=r['natural']<=20 and r['natural']+r['modifier']==r['total'] and r['success']==(r['total']>=r['DC']) and r['modifier']==a['saveBonuses'][r['ability']])
   if r.get('status')=='committed' and 'actualBasePaid' in r:
    casts+=1;a=pre['actors'][r['caster']];b=post['actors'][r['caster']]
    ck(tag+' paid cast '+r['id'],a['RP']==r['before']['RP'] and a['RP']-r['actualBasePaid']-r['extrasPaid']==b['RP']==r['after']['RP'] and a['action'] and not b['action'] and a['regularTurnActive'])
    ck(tag+' cadence '+r['id'],r['before']['Dissonance']+r['baseDissonanceAdded']+r['RefrainAdded']==r['after']['Dissonance']==b['Dissonance'])
  prev=post
 ck(c['id']+' finalstate',prev==c['expectedFinalState'])
ck('actual save and cast totals',(saves,casts)==(23,20))
def event(cid,i):return by['R7M-'+cid]['timeline'][i]
ck('GI paid current7RP and original55.2',event('09-A',0)['after']['actors']['I']['RP']==41 and event('09-A',1)['after']['effects']['GI']['deadline']==55.2)
ck('untrained unarmed changed die explicitly',event('09-B',3)['resolution']['attack']['actualPBAdded']==0 and event('09-B',3)['resolution']['attack']['natural']==13 and event('09-B',3)['after']['actors']['T1']['HP']==93)
ck('Mindfog actual path25',math.dist(*by['R7M-11-A']['geometry']['exitPath'])==25)
ck('Mindfog outside body',22.5**2+2.5**2==512.5 and 512.5>20**2)
ck('dispel immutable2',event('11-B',4)['resolution']['immutableCapturedSet']==['MF1','MF2'])
for r in event('11-B',4)['resolution']['checks']:ck('dispel check '+r['root'],r['natural']+r['INT']+r['PB']+r['fogPenalty']==r['nativeTotal'] and (r['result']=='Success')==(r['nativeTotal']>=r['DC']))
for cid in ['10-A','10-B']:ck(cid+' whole positive prerequisite held',event(cid,0)['inputsAndSourceQualification']['unfulfilledPrerequisite']['status']=='UNFULFILLED_WHOLE_CASE_CONTENT_PREREQUISITE')
ck('Bear actual duration',event('10-B-UNRATED',1)['after']['actors']['T']['formDeadline']==-2.5+600)
for idx,expected in [(3,(659,59)),(8,(659,59))]:
 apps=event('12-A',idx)['after']['effects']['CHARM']['applications'];ck('independent sibling endpoints '+str(idx),(apps['A']['deadline'],apps['B']['deadline'])==expected)
ck('LC repeat payment strain',tuple(event('12-A',8)['after']['actors']['C'][k] for k in ['RP','Dissonance','Refrain'])==(14,3,1))
ck('LC body radius distances',17.5**2+7.5**2==362.5 and 127.5**2+7.5**2==16312.5 and 107.5**2+7.5**2==11612.5)
ck('Slow original clock extension',event('12-B',3)['after']['effects']['SLOW']['deadline']==60+600)
ck('Slow survives LC end',event('12-B',6)['after']['effects']['SLOW']['state']=='active' and event('12-B',6)['after']['actors']['T']['Speed']==15)
ck('Slow ending save cleanup',event('12-B',7)['after']['effects']['SLOW']['state']=='ended' and event('12-B',7)['after']['actors']['T']['Speed']==30)
ck('own Slow removed before capture',event('12-B-OWN',5)['resolution']['captured']==[] and event('12-B-OWN',5)['after']['effects']['OWN']['state']=='ended')
report={'id':'PART_C_LOCAL_INDEPENDENT_REVIEW_120','scope':'Fresh read-only JSON consistency, arithmetic, source-preservation and focused semantic checks; no downloaded code or case runner executed. Conditional positives remain conditional.','checks':checks,'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'semanticReviewComplete':False}
(O/'PART_C_LOCAL_INDEPENDENT_REVIEW_120.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(report['passed'],report['failed']);print([c for c in checks if not c['passed']])
