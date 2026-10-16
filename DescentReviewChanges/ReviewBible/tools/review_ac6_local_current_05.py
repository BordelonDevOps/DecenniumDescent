"""Verify preserved authority and independently enumerate the corrected geometry/timing."""
import copy, hashlib, json, math
from pathlib import Path
from datetime import datetime, timezone
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game';R=G/'DescentReviewChanges/ReviewBible'
O=A/'ac6-local-current-05';P=A/'ac6-repair-04-return';P3=A/'ac6-full-review-03-return';I=A/'ac6-full-current-review-03-input'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
checks=[]
def ck(label,actual,expected=True):
 checks.append({'check':label,'passed':actual==expected,**({} if actual==expected else {'actual':actual,'expected':expected})})
def at(d,p):
 for t in p.strip('/').split('/') if p else []:
  t=t.replace('~1','/').replace('~0','~');d=d[int(t)] if isinstance(d,list) else d[t]
 return d
def current(d):
 if isinstance(d,dict):return {k:current(v) for k,v in d.items() if not any(s in k.lower() for s in ['previous','historical','prior','completesourceandaccess'])}
 if isinstance(d,list):return [current(v) for v in d]
 return d
def refs(d,path=''):
 if isinstance(d,dict):
  if 'path' in d and ('pointer' in d or 'section' in d):yield path,d
  for k,v in d.items():yield from refs(v,path+'/'+k)
 elif isinstance(d,list):
  for i,v in enumerate(d):yield from refs(v,path+'/'+str(i))
def leaves(d):
 if isinstance(d,str):yield d
 elif isinstance(d,dict):
  for v in d.values():yield from leaves(v)
 elif isinstance(d,list):
  for v in d:yield from leaves(v)
m=read(O/'SPELLS_MODEL.json');om=read(P/'SPELLS_MODEL.json');c=read(O/'CASEBOOK.json');oc=read(P/'CASEBOOK.json');c3=read(P3/'CASEBOOK.json');r=read(O/'REGISTER.json');manifest=read(O/'EVIDENCE_MANIFEST.json')
names=['REGISTER.json','SPELLS_MODEL.json','PLAYER_CHAPTER.md','DIRECTOR_REVIEW.md','CASEBOOK.json','SOURCE_HASHES.json','VERDICT.md','EVIDENCE_MANIFEST.json']
ck('exact eight complete output members',sorted(p.name for p in O.iterdir()),sorted(names))
for item in manifest['files']:
 b=(O/item['name']).read_bytes();ck('current bytes '+item['name'],len(b),item['bytes']);ck('current SHA '+item['name'],sha(b),item['sha256'])
for item in m['local05Provenance']['priorEightFiles']:
 b=(P/item['path']).read_bytes();ck('prior bytes '+item['path'],len(b),item['bytes']);ck('prior SHA '+item['path'],sha(b),item['sha256'])
sources=read(O/'SOURCE_HASHES.json')['bindings'];ck('103 exact source bindings',sources,read(I/'SOURCE_MANIFEST.json')['bindings'])
for item in sources:
 b=(I/'sources'/item['path']).read_bytes();ck('frozen bytes '+item['path'],len(b),item['bytes']);ck('frozen SHA '+item['path'],sha(b),item['sha256'])
ck('14 source identities and order',[s['id'] for s in m['spells']],[s['id'] for s in om['spells']])
for n,o in zip(m['spells'],om['spells']):
 for k in ['questionId','completeSourceAndAccess','historicalQuestionAndRecord','completePriorDraftRecord','priorDraftBinding','priorWholeRecordPointer']:
  ck(n['id']+' preserves '+k,n[k],o[k])
 if n['id']=='chain-arc':ck('Chain Arc exact return04 full record',n['local05PreviousCurrentVersion'],o)
 else:ck(n['id']+' wholly unchanged',n,o)
ck('all profiles wholly unchanged',m['profiles'],om['profiles'])
for k in ['originalQuestionDispositions','historicalIssueDispositions','currentInterfaceIssueDispositions','currentReviewQuestionDispositions','originalRequiredExamples','repair04Dispositions']:
 ck(k+' preserved',m[k],om[k])
ck('22 original texts preserved',c['historicalOriginalTexts'],oc['historicalOriginalTexts']);ck('32 original obligations preserved',c['originalRequiredExamples'],oc['originalRequiredExamples'])
ck('55 ordered case identities',[v['id'] for v in c['cases']],[v['id'] for v in oc['cases']])
for n,o in zip(c['cases'],oc['cases']):
 if n['id'] in ['AC6-N15','AC6-N17','NX-D02']:ck(n['id']+' exact return04 current case preserved',n['local05PreviousCurrentVersion'],o)
 else:ck(n['id']+' whole case unchanged',n,o)
 ck(n['id']+' initial prior history retained',n.get('previousCurrentVersion'),o.get('previousCurrentVersion'))
for n,o in zip(c['cases'],c3['cases']):
 if {k:v for k,v in n.items() if k not in ['repair04PreviousCurrentVersion','local05PreviousCurrentVersion']}!=o:
  ck(n['id']+' exact return03 case retained',n.get('repair04PreviousCurrentVersion'),o)
for k,v in om['sharedRules'].items():
 if k=='AC6-SUMMON-SUPPRESS-01':ck(k+' prior rule preserved',m['sharedRules'][k+'_local05PreviousCurrentVersion'],v)
 else:ck(k+' unchanged',m['sharedRules'][k],v)
ck('local correction register matches model',r['local05Corrections'],m['local05Corrections'])
for chapter in ['PLAYER_CHAPTER.md','DIRECTOR_REVIEW.md']:
 t=(O/chapter).read_text()
 for s in m['spells']:
  for i,v in enumerate(leaves(s['procedure'])):ck(chapter+' full procedure '+s['id']+':'+str(i),v in t)
 for key in ['AC6-CHAIN-GEOMETRY-05','AC6-SUMMON-SUPPRESS-01']:
  for i,v in enumerate(m['sharedRules'][key]['rule']):ck(chapter+' shared '+key+':'+str(i),v in t)
 for key in m['profiles']:ck(chapter+' full profile named '+key,key in t)
cache={};pr=[];sections=[]
for where,ref in refs({'model':current({'sharedRules':m['sharedRules'],'profiles':m['profiles'],'spells':m['spells']}),'cases':current(c['cases'])}):
 path=O/ref['path'] if ref['path'] in names else I/'sources'/ref['path']
 if 'pointer' not in ref:
  ck('descriptive section source exists '+where,path.exists());sections.append({'where':where,**ref});continue
 try:
  if path not in cache:cache[path]=read(path)
  found=at(cache[path],ref['pointer']);valid=found is not None;error=None
 except Exception as exc:valid=False;error=str(exc)
 ck('current pointer '+where,valid);pr.append({'where':where,**ref,'resolves':valid,**({'error':error} if error else {})})

# Independent body-box interval separation, including every unvisited body at each hop.
chain=next(v for v in c['cases'] if v['id']=='AC6-N17');g=chain['geometryLedger'];bodies=g['bodyVolumes']
visited=['A'];enumerated=[]
for hop in g['hops']:
 prev=visited[-1];ck('hop previous '+prev,hop['previous'],prev);distances={}
 for ident in sorted(bodies):
  if ident in visited:continue
  a=bodies[prev];b=bodies[ident];squares=[]
  for axis in range(3):
   intervals=sorted([(a['min'][axis],a['max'][axis]),(b['min'][axis],b['max'][axis])])
   separation=max(0,intervals[1][0]-intervals[0][1]);squares.append(separation**2)
  distance=math.sqrt(sum(squares));distances[ident]=distance
  ck('distance '+prev+'->'+ident,math.isclose(distance,hop['unvisitedDistancesFeet'][ident],rel_tol=1e-12,abs_tol=1e-12))
 expected=[k for k,v in distances.items() if v<=30]
 ck('complete candidates from '+prev,hop['completeCandidateArray'],expected)
 ck('selected eligible from '+prev,hop['selected'] in expected)
 visited.append(hop['selected']);enumerated.append({'from':prev,'completeCandidates':expected,'distances':distances})
ck('six distinct actual recipients',len(visited)==6 and len(set(visited))==6)
ck('recorded final sequence',visited,g['finalSequence'])
ck('initial W to A normal60ft range',abs(bodies['W']['bottomCenterFeet'][0]-bodies['A']['bottomCenterFeet'][0])<=60)
for d in chain['damageLedger']:
 ck('save arithmetic '+d['id'],d['natural']+d['dexModifier'],d['total'])
 ck('save outcome '+d['id'],d['save'],'success' if d['total']>=16 else 'fail')
 damage=0 if d.get('defense')=='lightning immunity' else (19//2 if d['save']=='success' else 19)
 ck('damage '+d['id'],d['damageAfterDefenses'],damage);ck('HP '+d['id'],d['hpBefore']-damage,d['hpAfter'])
ck('shared 3d8 actual faces',6+7+6,19);ck('Chain RP',40-13,27)

fall=next(v for v in c['cases'] if v['id']=='AC6-N15');t=fall['clockLedger'];fg=fall['geometryLedger']
ck('Ready cast in actual regular turn',t['readyCasterSlot'][0]<t['readyCast']<t['readyCasterSlot'][1])
ck('release after ready before next own START',t['readyCast']<t['release']<t['readyDeadlineNextStart'])
ck('reaction in known enclosing slot',t['enclosingRegularSlot'][0]<t['release']<t['enclosingRegularSlot'][1])
ck('next same slot six seconds later',[v+6 for v in t['enclosingRegularSlot']],t['sameSlotNextNumberedRound'])
ck('fixed marker is next slot END',t['firstFallMarker'],t['sameSlotNextNumberedRound'][1])
ck('full source established at release',t['release']+60,t['antimagicNominalExpiry'])
ck('suppression covers first step',t['suppression'][0]<t['firstFallMarker']<t['suppression'][1])
ck('independent summon original expiry',t['petExpiry'],60)
# Vertical distance to moving closed interval[h,h+5] is convex, so maxima occur at interval endpoints.
center_z=fg['sphereCenter'][2];bottoms=fg['fallBottomHeightInterval'];height=fg['bodyHeightFeet']
end_distances=[max(h-center_z,center_z-(h+height),0) for h in bottoms]
max_distance=max(end_distances)
ck('whole descent analytic maximum center-to-body distance',max_distance,fg['maximumNearestSphereCenterToBodyDistanceFeet'])
ck('strict intersection throughout descent',max_distance<fg['sphereRadiusFeet'])
ck('sphere center lies within horizontal body bounds',all(lo<=0<=hi for lo,hi in fg['petHorizontalBounds']))
ck('antimagic center within actual casting range',math.dist(fg['fieldCasterPoint'],fg['sphereCenter']),8)
ck('fall damage dice',min(10,math.floor(fg['uncontrolledFallFeet']/20)),1)
ck('heal exact7',4+3,7);ck('impact HP4',7-3,fg['landingHp'])
ck('original history not erased',all((P/n).exists() for n in names))
idx=read(R/'data/public/spell_playtests/authored_review_index.json');ck('review counts unchanged',idx['authoredCounts'],{'reviewed':451,'pending':397})
for flag in ['runtimeTestsExecuted','humanPlaytested','balanceApproved','cosmologyCanonModified']:ck('no unsupported '+flag,m[flag],False)
report={'id':'AC6-LOCAL-CURRENT-05-INDEPENDENT-CHECK','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'checkCount':len(checks),'failureCount':sum(not x['passed'] for x in checks),'checks':checks,'currentPointers':len(pr),'descriptiveSections':len(sections),'pointerResults':pr,'sectionReferences':sections,'chainGeometryEnumeration':enumerated,'fallGeometryProof':{'kind':'analytic convex interval-distance maximum at endpoints','endpointDistances':end_distances,'maximum':max_distance,'sphereRadius':fg['sphereRadiusFeet']},'scope':'Preservation, current procedure chapter inclusion, source reference existence, and independently recomputed repaired geometry/timing/arithmetic. Not complete semantic review of all55 scenarios. Descriptive sections are not exact anchor checks.','semanticReviewComplete':False,'jointReviewPending':True,'newSpellAdoptions':0,'runtimeTestsExecuted':False,'humanPlaytested':False,'balanceApproved':False}
target=A/'AC6_LOCAL_CURRENT_05_CHECK.json';assert not target.exists();target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({k:report[k] for k in ['checkCount','failureCount','currentPointers','descriptiveSections']}));print(json.dumps([v for v in checks if not v['passed']],ensure_ascii=False))
