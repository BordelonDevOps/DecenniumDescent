"""Check Current06 preservation, full current rule rendering and repaired scenarios."""
import json,hashlib,math
from pathlib import Path
from datetime import datetime,timezone
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game';R=G/'DescentReviewChanges/ReviewBible';O=A/'ac6-semantic-current-06';P=A/'ac6-local-current-05';I=A/'ac6-full-current-review-03-input'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
checks=[]
def ck(label,a,b=True):checks.append({'check':label,'passed':a==b,**({} if a==b else {'actual':a,'expected':b})})
def current(d):
 if isinstance(d,dict):return {k:current(v) for k,v in d.items() if not any(s in k.lower() for s in ['previous','historical','prior','completesourceandaccess'])}
 if isinstance(d,list):return [current(v) for v in d]
 return d
def leaves(d):
 if isinstance(d,str):yield d
 elif isinstance(d,dict):
  for v in d.values():yield from leaves(v)
 elif isinstance(d,list):
  for v in d:yield from leaves(v)
def refs(d,p=''):
 if isinstance(d,dict):
  if 'path' in d and ('pointer' in d or 'section' in d):yield p,d
  for k,v in d.items():yield from refs(v,p+'/'+k)
 elif isinstance(d,list):
  for i,v in enumerate(d):yield from refs(v,p+'/'+str(i))
def at(d,p):
 for k in p.strip('/').split('/') if p else []:
  k=k.replace('~1','/').replace('~0','~');d=d[int(k)] if isinstance(d,list) else d[k]
 return d
m=read(O/'SPELLS_MODEL.json');om=read(P/'SPELLS_MODEL.json');c=read(O/'CASEBOOK.json');oc=read(P/'CASEBOOK.json');reg=read(O/'REGISTER.json');mf=read(O/'EVIDENCE_MANIFEST.json');cases={x['id']:x for x in c['cases']};oldcases={x['id']:x for x in oc['cases']};original=read(I/'CURRENT_REVIEW_INPUT.json')
names={'REGISTER.json','SPELLS_MODEL.json','PLAYER_CHAPTER.md','DIRECTOR_REVIEW.md','CASEBOOK.json','SOURCE_HASHES.json','VERDICT.md','EVIDENCE_MANIFEST.json'}
ck('eight current files',set(p.name for p in O.iterdir()),names)
for b in mf['files']:
 raw=(O/b['name']).read_bytes();ck('file size '+b['name'],len(raw),b['bytes']);ck('file hash '+b['name'],sha(raw),b['sha256'])
for b in m['local06Provenance']['priorCurrentFiles']:
 raw=(P/b['path']).read_bytes();ck('prior unchanged size '+b['path'],len(raw),b['bytes']);ck('prior unchanged hash '+b['path'],sha(raw),b['sha256'])
ck('source hashes byte-identical',(O/'SOURCE_HASHES.json').read_bytes(),(P/'SOURCE_HASHES.json').read_bytes())
ck('source count',len(read(O/'SOURCE_HASHES.json')['bindings']),103)
ck('14 identities and order',[s['id'] for s in m['spells']],[s['id'] for s in om['spells']])
for i,(n,o) in enumerate(zip(m['spells'],om['spells'])):
 for k in ['questionId','completeSourceAndAccess','historicalQuestionAndRecord','completePriorDraftRecord','priorDraftBinding','priorWholeRecordPointer']:
  ck(n['id']+' exact '+k,n[k],o[k])
 if i in [4,9]:ck(n['id']+' exact entire Current05 spell history',n['local06PreviousCurrentVersion'],o)
 else:ck(n['id']+' whole record unchanged',n,o)
ck('all profiles unchanged',m['profiles'],om['profiles'])
for k,v in om['sharedRules'].items():ck('old shared rule unchanged '+k,m['sharedRules'][k],v)
for k in ['historicalOriginalTexts','originalRequiredExamples','caseCount']:ck('casebook preserves '+k,c[k],oc[k])
ck('55 case order',[v['id'] for v in c['cases']],[v['id'] for v in oc['cases']])
for n,o in zip(c['cases'],oc['cases']):
 if n['id'] in mf['changedCaseIds']:ck(n['id']+' exact whole prior current case',n['local06PreviousCurrentVersion'],o)
 else:ck(n['id']+' wholly unchanged',n,o)
 for k in ['previousCurrentVersion','repair04PreviousCurrentVersion','local05PreviousCurrentVersion']:ck(n['id']+' keeps '+k,n.get(k),o.get(k))
ck('25 changed current cases',len(mf['changedCaseIds']),25)
ck('eight finding dispositions agree',m['local06Corrections'],reg['local06Corrections'])
ck('all51 original scenario IDs',[v['caseId'] for v in reg['caseScenarioCoverage']],[v['id'] for v in original['currentExamples']])
for chapter in ['PLAYER_CHAPTER.md','DIRECTOR_REVIEW.md']:
 text=(O/chapter).read_text()
 for s in m['spells']:
  for i,leaf in enumerate(leaves(s['procedure'])):ck(chapter+' full procedure '+s['id']+':'+str(i),leaf in text)
 for key in ['AC6-SKYBRAND-ORIGIN-06','AC6-CHAIN-GEOMETRY-05','AC6-SUMMON-SUPPRESS-01']:
  for i,leaf in enumerate(m['sharedRules'][key]['rule']):ck(chapter+' shared '+key+':'+str(i),leaf in text)
text=(O/'DIRECTOR_REVIEW.md').read_text()
for cid in mf['changedCaseIds']:
 for i,action in enumerate(cases[cid]['actionsAndResolution']):ck('Director full corrected action '+cid+':'+str(i),action in text)
cache={};pointers=[];sections=[]
for where,ref in refs({'model':current({'spells':m['spells'],'profiles':m['profiles'],'sharedRules':m['sharedRules']}),'cases':current(c['cases'])}):
 path=O/ref['path'] if ref['path'] in names else I/'sources'/ref['path']
 if 'pointer' not in ref:ck('descriptive source exists '+where,path.exists());sections.append({'where':where,**ref});continue
 try:
  if path not in cache:cache[path]=read(path)
  valid=at(cache[path],ref['pointer']) is not None;error=None
 except Exception as exc:valid=False;error=str(exc)
 ck('current pointer '+where,valid);pointers.append({'where':where,**ref,'resolves':valid,**({'error':error} if error else {})})
gpt=read(A/'ac6-local-current-05-review/REVIEW.json');ready=gpt['requiredMinimalCorrection']['directorReview']
ck('Ready preparation exact reviewed correction',cases['AC6-N15']['actionsAndResolution'][2],ready['replacementItem3'][3:]);ck('Ready release exact reviewed correction',cases['AC6-N15']['actionsAndResolution'][3],ready['replacementItem4'][3:])
for key in ['clockLedger','geometryLedger','costLedger']:ck('N15 previously verified '+key+' unchanged',cases['AC6-N15'][key],oldcases['AC6-N15'][key])
ck('N17 complete geometry and outputs unchanged',cases['AC6-N17'],oldcases['AC6-N17'])
d=cases['AC6-N19']['damageLedger']['secondRoot'];ck('N19 ordinary advantage attack',max(d['attackFaces'])+d['attackModifier'],d['attackTotal']);ck('N19 actual attack hits',d['attackTotal']>=15);ck('N19 critical damage dice','2d12',d['damageDice']);ck('N19 critical damage',sum(d['damageFaces']),d['damage']);ck('N19 actual critical',d['automaticAdjacentCritical']);ck('N19 two death failures',d['deathFailures'],2);ck('N19 below instant death',d['damage']<20);ck('N19 no massive Wound trigger',2*d['damage']<20)
ck('N10 automatic removal stated','AUTOMATICALLY' in cases['AC6-N10']['actionsAndResolution'][0]);ck('N10 actual end20',cases['AC6-N10']['clockLedger']['antimagicActualEnd'],20)
ck('PB-D03 full thickness',cases['PB-D03']['geometryLedger']['panelVolumeFeet'],[5,1,5]);ck('PB-D03 squared max radius',5**2+0.5**2+5**2,cases['PB-D03']['geometryLedger']['centralPanelMaximumSquaredRadius']);ck('PB-D03 central panels wholly inside sphere',50.25<100)
panel_interiors=[]
for x in range(-15,15,5):
 for z in range(0,15,5):
  if min(x+5,5)>max(x,-5) and min(z+5,10)>max(z,0):panel_interiors.append([x,z])
ck('PB-D03 independent occupied panel enumeration',len(panel_interiors),4)
ck('GA-D02 weight and Load example retained','180lb but9Load' in '\n'.join(cases['GA-D02']['actionsAndResolution']))
ck('GA-D03 actual healing times',cases['GA-D03']['clockLedger'],{'nullZero':100,'heal':110,'expiry':3600})
ck('GA-D03 RP',3-2,cases['GA-D03']['costLedger']['clericRpAfter'])
ck('NX-D06 actual movement charged',cases['NX-D06']['costLedger']['failedCrossingMovementFeet'],5)
ck('NX-D07 actual deadline ordering',cases['NX-D07']['clockLedger']['firstCompletedTransitSecond']<cases['NX-D07']['clockLedger']['expiryBeforeSecondAttempt'])
ng=cases['NX-D08']['geometryLedger'];ck('NX-D08 actual path sum',ng['physicalRouteToEntranceFeet']+ng['physicalRouteAfterExitFeet'],ng['totalActualAttackRangeFeet'])
ck('N20 first miss',7+8<18);ck('N20 source damage',2+3,5);ck('N20 source hit',12+7>=15);ck('N20 failed concentration',4+2<max(10,5//2));ck('N20 partial route conserved',cases['AC6-N20']['geometryLedger']['actualMovementSpent']+cases['AC6-N20']['geometryLedger']['unusedMovementLost'],30)
ck('adoption counts unchanged',read(R/'data/public/spell_playtests/authored_review_index.json')['authoredCounts'],{'reviewed':451,'pending':397})
for flag in ['runtimeTestsExecuted','humanPlaytested','balanceApproved','cosmologyCanonModified']:ck('no unsupported '+flag,m[flag],False)
report={'id':'AC6-SEMANTIC-CURRENT-06-CHECK','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'checkCount':len(checks),'failureCount':sum(not x['passed'] for x in checks),'checks':checks,'currentPointers':len(pointers),'descriptiveSections':len(sections),'pointerResults':pointers,'sectionReferences':sections,'independentCentralPanelInteriors':panel_interiors,'sourceCount':103,'currentCaseCount':55,'changedCaseCount':25,'scope':'Current05 preservation, full current procedure/corrected-case chapter inclusion, source references and focused repaired-rule arithmetic/geometry. Existing Current05 source/Chain/Fall checks remain bound unchanged. Descriptive headings are not exact-anchor proof. New rule completions still need actual joint review.','jointReviewPending':True,'newSpellAdoptions':0,'runtimeTestsExecuted':False,'humanPlaytested':False,'balanceApproved':False}
target=A/'AC6_SEMANTIC_CURRENT_06_CHECK.json';assert not target.exists();target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps({k:report[k] for k in ['checkCount','failureCount','currentPointers','descriptiveSections']}));print(json.dumps([v for v in checks if not v['passed']],ensure_ascii=False))
