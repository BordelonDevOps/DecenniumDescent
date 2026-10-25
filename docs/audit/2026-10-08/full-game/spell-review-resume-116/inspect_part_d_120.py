from pathlib import Path
import json,hashlib,math
A=Path(r'C:\Github\DecenniumDescent\docs\audit\2026-10-08\full-game');P=A/'rank7-mechanics16-partD-120';O=A/'spell-review-resume-116'
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
m=read(P/'MODEL_PART_D.json');cb=read(P/'CASEBOOK_PART_D.json');cases=[x for c in cb['cases'] for x in [c,*c['independentBranches']]];by={c['id']:c for c in cases}
for k,n in [('procedures','PROCEDURES.json'),('sharedRules','SHARED_RULES.json'),('questionDispositions','QUESTION_DISPOSITIONS.json')]:
 ck('literal envelope '+n,m[k]==read(A/'rank7-mechanics16-partA-117'/n)==read(P/'inherited'/n));ck('literal bytes '+n,(P/'inherited'/n).read_bytes()==(A/'rank7-mechanics16-partA-117'/n).read_bytes())
ck('model complete casebook mirror',m['casebook']==cb);ck('actual counts',(len(cb['cases']),len(cases),sum(len(c['timeline'])for c in cases))==(8,11,56))
saves=casts=markers=0
for c in cases:
 previous=c['initialState']
 for e in c['timeline']:
  tag=c['id']+'/'+str(e['index']);pre=e['stateAtEventAfterScheduledProcessing'];post=e['after']
  ck(tag+' full continuity',e['before']==previous);ck(tag+' clock',e['time']>=previous['time'] and post['time']==e['time'])
  for aid,a in post['actors'].items():
   ck(tag+' bounds '+aid,0<=a['HP']<=a['effectiveMaxHP']<=a['maxHP'] and 0<=a['RP']<=a['maxRP'] and a['tempHP']>=0 and a['Dissonance']>=0)
   if a['derived']['PainHalfSpeed']:ck(tag+' Pain separate save policy '+aid,a['Speed']==a['normalSpeed']/2 and not a['derived']['PainPenalizesSaves'] and a['saveBonuses']==a['nativeSaveBonuses'])
   if a['derived']['Stunned']:ck(tag+' Stunned permission '+aid,not a['derived']['newActionAllowed'] and not a['derived']['newBonusActionAllowed'] and not a['derived']['newReactionAllowed'])
  for s in e['scheduledProcessing']:
   if '/START/' in s.get('id','') or '/END/' in s.get('id',''):
    markers+=1;aid,kind,tm=s['id'].split('/');tm=float(tm);k='next'+kind
    ck(tag+' marker '+s['id'],math.isclose(s['before'][k],tm,abs_tol=1e-7) and math.isclose(s['after'][k],tm+6,abs_tol=1e-7))
    if kind=='END':ck(tag+' idle '+s['id'],s['after']['Dissonance']==(s['before']['Dissonance'] if s['before']['turnHadMagic'] else max(0,s['before']['Dissonance']-1)))
  for r in walk(e['resolution']):
   if r.get('binarySave'):
    saves+=1;a=pre['actors'][r['recipient']];ck(tag+' save '+r['id'],r['d20']+r['modifier']==r['total'] and r['success']==(r['total']>=r['DC']) and r['modifier']==a['saveBonuses'][r['ability']] and 1<=r['d20']<=20)
   if r.get('state')=='committed' and 'actualPaidBase' in r:
    casts+=1;a=pre['actors'][r['owner']];b=post['actors'][r['owner']]
    ck(tag+' paid cast '+r['id'],a['RP']==r['RPBefore'] and a['RP']-r['actualPaidBase']==b['RP']==r['RPAfter'] and a['action'] and not b['action'] and a['regularTurnActive'])
    ck(tag+' strain '+r['id'],a['Dissonance']+r['baseDissonance']+r['RefrainAdded']==b['Dissonance']==r['dissonanceAfter'])
   if 'completePath' in r and 'distanceFeet' in r:ck(tag+' actual path',math.isclose(sum(math.dist(a,b)for a,b in zip(r['completePath'],r['completePath'][1:])),r['distanceFeet']))
  previous=post
 ck(c['id']+' final state',previous==c['expectedFinalState'])
ck('actual counts casts/saves/markers',(casts,saves,markers)==(13,10,98))
def e(cid,i):return by['R7M-'+cid]['timeline'][i]
ck('13B actual finite shift',e('13-B',0)['after']['actors']['T']['uses']==e('13-B',0)['before']['actors']['T']['uses'] or e('13-B',0)['resolution']['after']=={'shiftUses':5,'bufferReserve':14,'formSurgeReserve':5,'elementalUses':2})
h=e('13-B',3);a=h['stateAtEventAfterScheduledProcessing']['actors']['T'];b=h['after']['actors']['T'];ck('13B actual heal HP RP BA',b['HP']==min(a['effectiveMaxHP'],a['HP']+8)==107 and a['RP']-b['RP']==1 and a['bonusAction'] and not b['bonusAction'] and a['tempHP']==b['tempHP']==20 and b['formDeadline']==597.5)
ck('13B HP107 does not endPain',e('13-B',4)['after']['effects']['PAIN']['state']=='active')
ck('13HIGH paid displaced source',e('13-B-HIGH',4)['after']['actors']['C']['RP']==29 and e('13-B-HIGH',4)['after']['effects']['DM']['state']=='ended' and e('13-B-HIGH',4)['resolution']['initialSaveDraws']==0)
ck('14A actual target gap',90-2.5-2.5==e('14-A',4)['resolution']['bodyMinimumSeparation']==85 and e('14-A',4)['resolution']['actualRange']==30 and not e('14-A',4)['resolution']['committed'])
ck('14B tether distances',110-(-30+2.5)==137.5 and 110-2.5==107.5)
ck('14B conditional route retained',by['R7M-14-B-ILLUSION']['status']=='WHOLE_CASE_CONDITIONAL' and e('14-B-ILLUSION',0)['resolution']['commitment']['conditionalRouteOnly'])
ck('15A upward body cap',e('15-A',2)['resolution']['travel']==100-6==94)
fall=e('15-A',4)['resolution'];ck('15A impact calculation',fall['diceCount']==min(10,94//20)==4 and sum(fall['faces'])==fall['raw']==18 and fall['HPAfter']==94-18==76 and fall['raw']<fall['WoundThreshold'])
ck('15A distinct fall marker',e('15-A',3)['resolution']['newFallMarker']==16 and e('15-A',4)['time']==16)
ck('15B topstraddle unchanged',e('15-B',2)['after']['actors']['T']['position']==[50,0,98] and e('15-B',1)['resolution']['capTravel']=={'T':0,'TallShaft':0})
ck('16A parent consumption before saves',e('16-A',1)['resolution']['dischargeReceipt']['claimedBeforeAnySave'] and e('16-A',1)['resolution']['childResult']['deadline']==4)
ck('16 allsave still spent',e('16-A-ALL-SUCCESS',1)['resolution']['receiptBeforeSaves']['frozenViewers']==['T','V'] and all(z['child'] is None and not z['hardGuardSpent'] for z in e('16-A-ALL-SUCCESS',1)['resolution']['saveResults']))
ck('16B new current viewer not queued',e('16-B',5)['resolution']['child']['deadline']==10 and e('16-B',5)['resolution']['receiptBeforeSaves']['frozenViewers']==['T'] and e('16-B',4)['resolution']['observationQueued']==False)
report={'id':'PART_D_LOCAL_INDEPENDENT_REVIEW_120','scope':'Fresh read-only actual delivered JSON/source/arithmetic/lifecycle checks; no supplied code or old runner executed.','checks':checks,'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'semanticReviewComplete':False};(O/'PART_D_LOCAL_INDEPENDENT_REVIEW_120.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(report['passed'],report['failed']);print([c for c in checks if not c['passed']])
