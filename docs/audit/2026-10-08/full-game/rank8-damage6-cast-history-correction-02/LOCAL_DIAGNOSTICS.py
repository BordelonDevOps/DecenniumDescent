"""Independent data-only review of Rank8 correction02; never execute returned code."""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
import json,hashlib,math,itertools
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
P=A/'rank8-damage6-part5-correction-return-02';OUT=A/'RANK8_DAMAGE6_PART5_CORRECTION_RETURN_02_SEMANTIC_REVIEW_70.json'
def read(p):return json.loads(p.read_bytes())
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def bind(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
checks=[]
def ck(label,actual,expected=True):checks.append({'check':label,'actual':actual,'expected':expected,'passed':actual==expected})
def intersects(a,b,lo,hi):
 first,last=F(0),F(1)
 for i in range(3):
  delta=F(str(b[i]))-F(str(a[i]))
  if delta==0:
   if not lo[i]<=a[i]<=hi[i]:return False
  else:
   u,v=(F(str(lo[i]))-F(str(a[i])))/delta,(F(str(hi[i]))-F(str(a[i])))/delta
   first=max(first,min(u,v));last=min(last,max(u,v))
   if first>last:return False
 return True
def mixed(v):
 a={k:(x//2 if v['saveHalf'] else x) for k,x in v['raw'].items()}
 def resistance():
  for k in v['resist']:a[k]//=2
 if v['stage']=='after':resistance()
 total=sum(a.values());amount=min(v['flat'],total)
 if total:
  exact={k:F(amount*x,total) for k,x in a.items()};assigned={k:int(x) for k,x in exact.items()}
  for k in sorted(a,key=lambda k:(-(exact[k]-assigned[k]),k))[:amount-sum(assigned.values())]:assigned[k]+=1
  a={k:x-assigned[k] for k,x in a.items()}
 if v['stage']=='before':resistance()
 return a
def main():
 assert not OUT.exists() and not (A/Path(__file__).name).exists()
 model=read(P/'MODEL.json');old=read(P/'history/return01/MODEL.json');cases=model['currentVectors'];by={c['id']:c for c in cases}
 allcases=[s for c in cases for s in [c]+c['independentBranches']];allby={c['id']:c for c in allcases}
 protected=[P/'MODEL.json',P/'CASE_DISPOSITIONS.json',R/'data/public/spell_playtests/catalog.json',R/'data/public/spell_playtests/authored_review_index.json',R/'data/director/spell_review/accepted_interface_registry_06.json',R/'data/director/spell_review/remaining_work_queue_57.json',A/'ACTIVE_AUTHORING_CHECKPOINT_RANK8_RETURN_RANK7_DISPATCH_70.json']
 original={p:p.read_bytes() for p in protected}
 ck('Full case mirror',cases==read(P/'CASE_DISPOSITIONS.json')['allCases'])
 ck('Original main IDs', [c['id'] for c in cases],[c['id'] for c in old['currentVectors']])
 ck('Only new branch is actual concentration failure',sorted(set(allby)-{s['id'] for c in old['currentVectors'] for s in [c]+c['independentBranches']}),['RD8-03-B-CONCENTRATION-FAIL'])
 # Independently recalculate authored numerical inputs, including every supplied branch RNG.
 for c in allcases:
  for i,v in enumerate(c.get('arithmetic',[])):
   name=c['id']+'/arithmetic/'+str(i);kind=v['kind']
   if kind=='mixed':
    result=mixed(v);ck(name+' typed',result,v['expectedTyped']);ck(name+' total',sum(result.values()),v['expectedTotal'])
   elif kind=='hp':ck(name,max(0,v['before']-v['damage']),v['expected'])
   elif kind=='sum':ck(name,sum(v['faces']),v['expected'])
   elif kind=='dc':ck(name,max(10,v['damage']//2),v['expected'])
   elif kind=='temp_hp':
    post=max(0,v['damage']-v['temp']);ck(name,[max(0,v['hp']-post),max(0,v['temp']-v['damage']),post],[v['expectedHP'],v['expectedTemp'],v['expectedPostTemp']])
   elif kind=='hp_chain':
    hp=v['initial'];states=[]
    for d in v['damage']:hp=max(0,hp-d);states.append(hp)
    ck(name,states,v['expectedStates'])
   elif kind=='cell':
    w,d,h=v['body'];q=v['clearance'];ck(name,[math.ceil((w+2*q)/5)*5,math.ceil((d+2*q)/5)*5,math.ceil((h+q)/5)*5],v['expected'])
   elif kind=='transfer':ck(name,[v['damage']-v['chosen'],v['chosen']],[v['expectedOriginal'],v['expectedTransferred']])
   elif kind=='stand':ck(name,[v['Speed']//2,v['movementBefore']-v['Speed']//2],[v['expectedCost'],v['expectedMovementAfter']])
   elif kind=='fall':ck(name,min(10,v['distance']//20),v['expectedDice'])
   elif kind=='wallPoint':
    u,y,z=v['local'];ck(name,abs(u)<=30 and y>=0 and z>=0 and y*y+z*z<=900,v['expected'])
   else:raise ValueError(kind)
  for i,rng in enumerate(c.get('rng',[])):
   if 'faces' in rng and 'total' in rng:ck(c['id']+'/rng/'+str(i),sum(rng['faces'])+rng.get('bonus',0),rng['total'])
 # Required concentration happens while the hold is live; cleanup cannot erase it earlier.
 ready=by['RD8-03-B'];failure=allby['RD8-03-B-CONCENTRATION-FAIL']
 for c,passed in [(ready,True),(failure,False)]:
  timeline=c['timeline'];sheet=c['actorSheets']['caster'];final=c.get('finalState',c.get('intermediateAndFinalState'))
  creation=next(e for e in timeline if 'createdRoots' in e);damage=next(e for e in timeline if e.get('sequence')==1);save=next(e for e in timeline if e.get('sequence')==2);carrier=next(e for e in timeline if e.get('sequence')==3)
  amount=damage['before']['casterHP']-damage['after']['casterHP'];rng=save['rng']
  ck(c['id']+' concentration DC from actual damage',max(10,amount//2),rng['DC'])
  ck(c['id']+' concentration uses actual CON',rng['bonus'],sheet['saveBonuses']['CON'])
  ck(c['id']+' success from actual total',sum(rng['faces'])+rng['bonus']>=rng['DC'],passed)
  ck(c['id']+' held before self damage',damage['before']['concentration'],'paid Ready hold')
  ck(c['id']+' save before carrier',timeline.index(damage)<timeline.index(save)<timeline.index(carrier))
  ck(c['id']+' immediate save result',save['after']['concentration'],'paid Ready hold' if passed else None)
  ck(c['id']+' carrier event after result',carrier['before']['carrierHP']-carrier['damage'],carrier['after']['carrierHP'])
  ck(c['id']+' same two roots',len(creation['createdRoots']),final['rootCount'])
  ck(c['id']+' no additional payment',final['caster']['RP'],sheet['RP']-timeline[0]['price']['finalRP'])
  ck(c['id']+' final real Reaction spent',final['caster']['Reaction'],False)
  ck(c['id']+' consumed corpse retained',final['corpseState'],'consumed-spent-ash')
  ck(c['id']+' no duplicate hold cleanup',final['readyHoldCleanupCount'],int(passed))
  ck(c['id']+' caster HP arithmetic',sheet['hp']-sum(creation['sharedRaw'][k] for k in ['fire','necrotic']),final['caster']['HP'])
  ck(c['id']+' carrier half by type',c['actorSheets']['carrier']['hp']-sum(creation['sharedRaw'][k]//2 for k in ['fire','necrotic']),final['carrier']['HP'])
 findingdata=read(P/'FINDING_DISPOSITIONS.json')['findings'];newparagraph=findingdata[0]['newAuthorship']
 for filename in ['MODEL.json','SPELL_DISPOSITIONS.json','QUESTION_DISPOSITIONS.json','NEW_SCOPED_AUTHORSHIP.json']:
  ck('New Pyre paragraph retained in '+filename,newparagraph in json.dumps(read(P/filename),ensure_ascii=False).replace('\\n','\n'))
 for filename in ['PLAYER_CHAPTER.md','DIRECTOR_REVIEW.md']:ck('New Pyre full paragraph in '+filename,newparagraph in (P/filename).read_text(encoding='utf-8'))
 ck('Only Pyre procedure changes',[r['spellId'] for r,o in zip(model['records'],old['records']) if r['procedure']!=o['procedure']],['soul-pyre'])
 ck('Six shared clauses unchanged',model['selectedSharedRules']==old['selectedSharedRules'])
 # Analytic extrema: with positive numerator and y-30>0, ratio is monotone in x,z,y.
 cover=allby['RD8-06-B-COVER'];screen=cover['explicitChangedInputs']['actualStoneScreen'];origin=cover['geometry']['base'];body=cover['actorSheets']['hawk']['body']['closedAabb'];lo,hi=body
 xinterval=[F(str(lo[0]))*3/(F(str(hi[1]))-30),F(str(hi[0]))*3/(F(str(lo[1]))-30)]
 zinterval=[F(str(lo[2]))*3/(F(str(hi[1]))-30),F(str(hi[2]))*3/(F(str(lo[1]))-30)]
 ck('Full body x interval independently derived',list(map(str,xinterval)),cover['geometryProof']['hawkXAtPlane'])
 ck('Full body z interval independently derived',list(map(str,zinterval)),cover['geometryProof']['hawkZAtPlane'])
 ck('Entire analytic intervals inside real screen',screen['minimum'][1]<=33<=screen['maximum'][1] and screen['minimum'][0]<=xinterval[0]<=xinterval[1]<=screen['maximum'][0] and screen['minimum'][2]<=zinterval[0]<=zinterval[1]<=screen['maximum'][2])
 ck('Original witness actually misses original screen',intersects(origin,[10,40,20],[5,32,0],[15,34,25]),False)
 ck('Corrected screen blocks same witness',intersects(origin,[10,40,20],screen['minimum'],screen['maximum']))
 ck('Ram witness remains unblocked',intersects(origin,cover['geometryProof']['ramWitness'],screen['minimum'],screen['maximum']),False)
 ck('No boolean occlusion override','coversHawkRelevantPaths' not in screen and cover['explicitChangedInputs']['noTotalVisualOcclusionClaim'])
 ck('No admission damage to blocked Hawk',cover['finalState']['hawkHP'],cover['actorSheets']['hawk']['hp'])
 # Greater Dispel actual area capture is immutable and checks each generating cast.
 dispel=allby['RD8-04-B-DISPEL'];d=dispel['actorSheets']['dispelCaster'];geom=dispel['geometry'];inputs=dispel['explicitChangedInputs'];fin=dispel['finalState']
 ck('Separate full dispeller identical across mirrors',d==inputs['dispelCaster'])
 ck('Actual center range',sum((a-b)**2 for a,b in zip(d['spellOrigin'],geom['dispelCenter'])),geom['sourceToCenterDistance']**2)
 ck('Source within actual printed range',geom['sourceToCenterDistance']<=geom['rangeMaximum'])
 nearest=sum(max(low-q,0,q-high)**2 for q,low,high in zip(geom['bothCloudCenters'],*d['body']['closedAabb']))
 ck('Dispel body genuinely outside both damaging clouds',nearest>geom['radius']**2)
 ck('Both complete cloud spheres inside capture',geom['bothCloudCenters']==geom['dispelCenter'] and geom['radius']<=geom['dispelRadius'])
 ck('Complete captured source list',geom['capturedOngoingApplications'],['cloudA','cloudB'])
 opportunity=inputs['actualActionOpportunity'];ck('Real ordinary Action timing',opportunity['regularSTART']<=opportunity['commitAt']<opportunity['effectAt']<opportunity['regularEND'])
 bonus=(d['abilityScores']['INT']-10)//2+d['PB']
 for roll in inputs['castChecks']:
  ck('Dispel actual modifier '+roll['generatingCast'],bonus,roll['bonus']);ck('Dispel rank DC '+roll['generatingCast'],10+2*roll['recordedRank'],roll['DC']);ck('Dispel actual result '+roll['generatingCast'],roll['face']+bonus>=roll['DC'])
 ck('Single actual 10RP payment',fin['dispelCaster']['RP'],d['RP']-d['actualAcquisition']['baseRpCost'])
 ck('Action spent',fin['dispelCaster']['Action'],False);ck('No Counterspell-only recovery',fin['dispelCaster']['ArcaneFeedbackTriggered'],False)
 ck('Both field concentrations ended',all(fin[k]['state']=='ended' and fin[k]['concentration'] is None for k in ['cloudA','cloudB']))
 ck('Completed prior damage retained',fin['targetHP'],dispel['actorSheets']['target']['hp']-40)
 ck('No later cloud pulse survives',fin['futureCloudPulses'],[])
 # Correct all full carrier and form sheet occurrences, not just the main actor label.
 for c in [ready]+ready['independentBranches']:
  actor=c['actorSheets']['carrier'];corpse=c['actorSheets']['corpse'];carry=actor['carrying'];label=c['id']
  ck(label+' natural STR save',(actor['abilityScores']['STR']-10)//2,actor['saveBonuses']['STR'])
  ck(label+' one corpse anchor',corpse['anchor'],c['geometry']['initialCorpseAnchor'])
  ck(label+' held offset derives anchor',[x+y for x,y in zip(actor['body']['footCenter'],c['geometry']['heldCorpseOffsetFromCarrierFoot'])],corpse['anchor'])
  ck(label+' actual pounds conserved',carry['corpseMassLb']+carry['otherGearLb'],carry['totalLb']);ck(label+' mass fits capacity',carry['totalLb']<=carry['capacityLb'])
  ck(label+' actual Load conserved',carry['corpseBodyLoad']+carry['gearLoad'],carry['totalLoad']);ck(label+' Load fits capacity',carry['totalLoad']<=carry['LoadCapacity'])
 for point,expected in [(ready['geometry']['releaseCorpseAnchor'],226),(allby['RD8-03-B-OUTOFRANGE']['explicitChangedInputs']['corpseAtRelease'],626)]:ck('Actual corpse source distance '+str(point),sum((a-b)**2 for a,b in zip(point,ready['actorSheets']['caster']['spellOrigin'])),expected)
 forms=[];anchors=[]
 for c in allcases:
  for actorid,sheet in c['actorSheets'].items():
   if sheet.get('class')=='Druid' and sheet.get('form') in ['Hawk','Bear','Ironhorn Ram']:
    forms.append((c['id'],actorid,sheet));label=c['id']+'/'+actorid
    ck(label+' no form casting before18',sheet['spellcastingInCurrentForm']['permitted'],False);ck(label+' no operative casting origin',sheet['spellOrigin'],None)
    ck(label+' melded focus unavailable','melded' in sheet['components']['F'].lower() and 'unavailable' in sheet['components']['F'].lower())
    ck(label+' stage-correct speech','Speech is preserved' in sheet['components']['V'] if sheet['form']=='Ironhorn Ram' else 'does not preserve speech' in sheet['components']['V'])
   if actorid=='anchorCaster':anchors.append((c['id'],sheet));ck(c['id']+' actual Arch path gate',sheet['classLevel']==7 and sheet['stage']=='Arch Arcanist' and sheet['hero'] is None)
 ck('All17 form occurrences checked',len(forms),17);ck('All9 Anchor sheets checked',len(anchors),9)
 immune=allby['RD8-04-A-IMMUNE'];ash=immune['actorSheets']['target'];ck('Complete Ashen replacement mirror',ash==immune['explicitChangedInputs']['target'])
 ck('One actual Circle and no Storm resistances',ash['Circle']=='Ashen Grove' and not set(['lightning','thunder'])&set(ash['resistances']))
 ck('Actual14th-level fire immunity',ash['classLevel']>=14 and ash['immunities']==['fire'])
 # Movement is on the actual regular turn and the whole body clears the closed sphere.
 move=allby['RD8-04-A-ENTRY'];mi=move['explicitChangedInputs'];spent=0
 for j,leg in enumerate(mi['targetVoluntaryMovement']):
  distance=math.dist(leg['from'],leg['to']);spent+=distance
  ck('Leg actual geometry '+str(j),distance,leg['distanceFeet']);ck('Leg actual opportunity '+str(j),mi['targetRegularTurn']['start']<=leg['startAt']<leg['completeAt']<mi['targetRegularTurn']['end'])
  ck('Leg cumulative budget '+str(j),spent,leg['cumulativeSpent']);ck('Leg remaining budget '+str(j),mi['targetRegularTurn']['Speed']-spent,leg['remaining'])
 nearestx=mi['targetVoluntaryMovement'][0]['to'][0]-move['actorSheets']['target']['body']['dimensions'][0]/2
 ck('Whole target outside at furthest point',nearestx-move['geometry']['cloudCenter'][0]>move['geometry']['radius'])
 ck('No entry pulse or extra-turn pulse',move['finalState']['newEntryDamage']==move['finalState']['extraTurnDamage']==0)
 ck('Actual three-pulse damage chain',move['actorSheets']['target']['hp']-44-40//2-35,move['finalState']['targetHP'])
 ck('Extra turn remains externally conditional','CONDITIONAL' in move['qualification'] and not move['finalState']['extraTurnProviderImplemented'])
 block=allby['RD8-01-B-STRAIN-BLOCK'];ck('Correct strain17 wording','Dissonance17' in block['qualification'] and block['explicitChangedInputs']['casterPreDissonance']==11+6)
 ck('Blocked commitment still unspent',block['finalState']['Action'] and block['finalState']['casterRP']==block['actorSheets']['caster']['RP'])
 for c in [s for main in cases[10:] for s in [main]+main['independentBranches']]:
  clock=c['geometry']['sourceClock'];ck(c['id']+' duration from actual manifestation',F(str(clock['actualEstablishment']))+clock['durationSeconds'],F(str(clock['nominalExpiry'])))
  checks[-1]['actual']=str(checks[-1]['actual']);checks[-1]['expected']=str(checks[-1]['expected'])
  ck(c['id']+' prospective commit distinct',clock['paidCommitment']<clock['actualEstablishment']<clock['actualEarlierEnding']<clock['nominalExpiry'])
 ck('Independent True Seeing deadline unchanged','deadline58' in by['RD8-06-A']['intermediateAndFinalState']['target']['concentration'])
 ck('Independent Falling marker unchanged',by['RD8-06-B']['geometry']['FallMarker']==old['currentVectors'][11]['geometry']['FallMarker'])
 # Newly noticed state qualification: a known prior cast cannot silently retain unused-family state.
 wizard=read(R/'data/public/class_playtests/wizard.json');rule=next(x for x in wizard['engine'] if x.startswith('PROTECTED DISSONANCE INTERFACE.'))
 anchor=by['RD8-05-B']['actorSheets']['anchorCaster']
 ck('Anchor prior paid family recorded or an intervening encounter reset explicitly qualified',bool(anchor['matrixFamiliesUsed']) or any('encounter' in str(v).lower() and 'reset' in str(v).lower() for v in anchor.values()))
 findings=[{'id':'RD8-LOCAL70-01','priority':3,'status':'CAST_HISTORY_QUALIFICATION_REQUIRED','caseIds':[x[0] for x in anchors],
  'title':'Anchor support actor retains empty prepared-family history after its disclosed paid cast',
  'evidence':{'pointer':'/currentVectors/9/actorSheets/anchorCaster','initialSetup':anchor['initialSetup'],'previousSpell':anchor['previousSpell'],'matrixFamiliesUsed':anchor['matrixFamiliesUsed'],'liveConcentration':anchor['concentration'],'actualSourceRule':rule,'copies':9,'alreadyPresentInReturn01':True},
  'requestedCorrection':'Bind whether the actual Dimensional Anchor cast at-1 belongs to the encounter whose current history is supplied. If it does, include its actual family in matrixFamiliesUsed in all nine full actor sheets and mirrors. If an intervening legitimate encounter boundary resets that ledger, explicitly supply that boundary and its authority while retaining the spell lifetime and other actual history. Do not infer a free reset from time0, merely relabel the old first-use or grant a second exemption. Provide a later same-family check showing the correct outcome. No existing damage, RP, form or exile result needs to change for this clarification.',
  'scope':'This concrete qualification was noticed while checking corrected full Anchor metadata; it was not one of the eight original findings. Absence of a stated encounter boundary prevents treating either history choice as conclusively established.'}]
 for p,b in original.items():assert p.read_bytes()==b,str(p)
 dispositions=[{'findingId':f['id'],'localDisposition':'CORRECTION_SEMANTICALLY_RECONCILED_AT_SUPPLIED_INPUTS','sourceAndCorrectionRecord':{'path':bind(P/'FINDING_DISPOSITIONS.json')['path'],'pointer':'/findings/'+str(i)},'newRule':f['newAuthorship'] is not None} for i,f in enumerate(findingdata)]
 result={'id':'RANK8-CORRECTION02-INDEPENDENT-SEMANTIC-REVIEW-70','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'verdict':'EIGHT_SUBMITTED_FINDINGS_RECONCILED_ONE_NEW_CAST_HISTORY_QUALIFICATION_PENDING','archive':bind(A/'DD_Rank8_Damage_6_Part5_Correction_Return_02.zip'),'model':bind(P/'MODEL.json'),'priorSemanticReview':bind(A/'RANK8_DAMAGE6_PART5_RETURN_01_SEMANTIC_REVIEW_59.json'),'preservationReceipt':bind(A/'RANK8_DAMAGE6_PART5_CORRECTION_RETURN_02_LOCAL_PREFLIGHT.json'),'originalFindingDispositions':dispositions,'reviewCoverage':{'fullPriorReviewInheritedWithExactUnchangedProcedures':5,'changedFullProcedureRead':'Soul Pyre','fullCaseDeltaCoverage':8,'mainCases':12,'branches':42,'allEightCorrectionDispositionsRead':True,'classSourcesRead':['Druid engine0/3/cards9/53/58','Wizard engine1/protected Dissonance/cards22/57/60'],'scope':'Full correction semantic deltas and actual supplied state/arithmetic/geometry. Not all engine interactions or live scheduler behavior.'},'diagnosticChecks':checks,'diagnosticCheckCount':len(checks),'diagnosticFailures':sum(not x['passed'] for x in checks),'findings':findings,'findingsCount':len(findings),'newAcceptedIdentities':0,'acceptedButUnappliedUnchanged':39,'canonicalChanges':0,'downloadedCodeExecuted':False,'runtimeTestsExecuted':0,'sourceInformationDeleted':0,'nextAction':'Prepare the narrow Anchor-history qualification with full evidence. Confer after the active Rank7 correction12 response completes; do not interrupt or apply canonical changes.'}
 OUT.write_bytes(enc(result));(A/Path(__file__).name).write_bytes(Path(__file__).read_bytes());print(json.dumps({'report':bind(OUT),'checks':len(checks),'diagnosticFailures':result['diagnosticFailures'],'newFindings':len(findings),'failedChecks':[x['check'] for x in checks if not x['passed']]}))
if __name__=='__main__':main()
