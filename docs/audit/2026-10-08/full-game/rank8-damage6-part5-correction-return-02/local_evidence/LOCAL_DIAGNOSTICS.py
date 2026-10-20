"""Independent numerical/geometry diagnostics and source-linked semantic findings.

Reads the preserved GPT package as data. Does not import its scripts or change it.
"""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction
import hashlib,json,math
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
P=A/'rank8-damage6-part5-conference-return-01'
OUT=A/'RANK8_DAMAGE6_PART5_RETURN_01_SEMANTIC_REVIEW_59.json'
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def read(p):return json.loads(p.read_bytes())
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
checks=[]
def ck(name,actual,expected):checks.append({'check':name,'actual':actual,'expected':expected,'passed':actual==expected})
def mixed(v):
 a={k:(x//2 if v['saveHalf'] else x) for k,x in v['raw'].items()}
 def resist():
  for k in v['resist']:a[k]//=2
 if v['stage']=='after':resist()
 total=sum(a.values());amount=min(v['flat'],total)
 if total:
  exact={k:Fraction(amount*x,total) for k,x in a.items()}
  assigned={k:int(x) for k,x in exact.items()}
  for k in sorted(a,key=lambda k:(-(exact[k]-assigned[k]),k))[:amount-sum(assigned.values())]:assigned[k]+=1
  a={k:x-assigned[k] for k,x in a.items()}
 if v['stage']=='before':resist()
 return a
def intersects(a,b,lo,hi):
 first,last=0.,1.
 for i in range(3):
  delta=b[i]-a[i]
  if delta==0:
   if not lo[i]<=a[i]<=hi[i]:return False
  else:
   u,v=(lo[i]-a[i])/delta,(hi[i]-a[i])/delta
   first=max(first,min(u,v));last=min(last,max(u,v))
   if first>last:return False
 return True

def main():
 assert not OUT.exists()
 model=read(P/'MODEL.json');casefile=read(P/'CASE_DISPOSITIONS.json');cases=casefile['allCases'];by={c['id']:c for c in cases}
 regpath=R/'data/director/spell_review/accepted_interface_registry_06.json';reg=read(regpath)
 preserved={p:p.read_bytes() for p in P.rglob('*') if p.is_file()}
 for p in [regpath,R/'data/public/spell_playtests/authored_review_index.json',R/'data/public/spell_playtests/catalog.json',R/'data/director/spell_review/remaining_work_queue_47.json']:preserved[p]=p.read_bytes()
 ck('Exact case mirrors',model['currentVectors'],cases)
 # Do not retain the two very large objects in this numerical check record.
 checks[-1]['actual']='MODEL/currentVectors';checks[-1]['expected']='CASE_DISPOSITIONS/allCases: full equality tested'
 for c in cases:
  for i,v in enumerate(c['arithmetic']):
   name=c['id']+'/arithmetic/'+str(i);k=v['kind']
   if k=='mixed':
    result=mixed(v);ck(name+' typed',result,v['expectedTyped']);ck(name+' total',sum(result.values()),v['expectedTotal'])
   elif k=='hp':ck(name,max(0,v['before']-v['damage']),v['expected'])
   elif k=='sum':ck(name,sum(v['faces']),v['expected'])
   elif k=='dc':ck(name,max(10,v['damage']//2),v['expected'])
   elif k=='temp_hp':
    post=max(0,v['damage']-v['temp']);ck(name,[max(0,v['hp']-post),max(0,v['temp']-v['damage']),post],[v['expectedHP'],v['expectedTemp'],v['expectedPostTemp']])
   elif k=='hp_chain':
    hp=v['initial'];states=[]
    for d in v['damage']:hp=max(0,hp-d);states.append(hp)
    ck(name,states,v['expectedStates'])
   elif k=='cell':
    w,d,h=v['body'];q=v['clearance'];ck(name,[math.ceil((w+2*q)/5)*5,math.ceil((d+2*q)/5)*5,math.ceil((h+q)/5)*5],v['expected'])
   elif k=='transfer':ck(name,[v['damage']-v['chosen'],v['chosen']],[v['expectedOriginal'],v['expectedTransferred']])
   elif k=='stand':ck(name,[v['Speed']//2,v['movementBefore']-v['Speed']//2],[v['expectedCost'],v['expectedMovementAfter']])
   elif k=='fall':ck(name,min(10,v['distance']//20),v['expectedDice'])
   elif k=='wallPoint':
    u,vv,w=v['local'];ck(name,abs(u)<=30 and vv>=0 and w>=0 and vv*vv+w*w<=900,v['expected'])
   else:raise ValueError(k)
  for i,rng in enumerate(c['rng']):
   if 'faces' in rng and 'total' in rng:ck(c['id']+'/rng/'+str(i),sum(rng['faces'])+rng.get('bonus',0),rng['total'])
 # Evidence-led diagnostics beyond the return's short arithmetic assertions.
 ready=by['RD8-03-B'];cover=next(b for b in by['RD8-06-B']['independentBranches'] if b['id']=='RD8-06-B-COVER')
 screen=cover['explicitChangedInputs']['actualStoneScreen'];origin=[0,30,0];witness=[10,40,20]
 ck('Claimed stone-screen occlusion of legal Hawk witness',intersects(origin,witness,screen['minimum'],screen['maximum']),True)
 ck('Ready Pyre has a supplied caster concentration RNG result',any('concentration' in r['kind'].lower() for r in ready['rng']),True)
 ck('Ready carrier natural STR save matches score18 and zero Wounds',ready['actorSheets']['carrier']['saveBonuses']['STR'],4)
 ck('Ready corpse initial anchor agrees across complete inputs',ready['actorSheets']['corpse']['anchor'],ready['geometry']['initialCorpseAnchor'])
 findings=[
 {'id':'RD8-LOCAL59-01','priority':2,'status':'CORRECTION_REQUIRED','caseIds':['RD8-03-B'],'title':'Ready Soul Pyre omits the self-damage concentration save','evidence':{'casePointer':'/allCases/5','casterDamage':32,'CONBonus':2,'requiredDC':16,'readyAuthority':reg['entries'][1]['exactAuthority'],'concentrationAuthority':reg['entries'][8]['exactAuthority'],'localDamageClause':'MODEL/selectedSharedRules/2: damage to a concentrating creature invokes its actual concentration procedure.','observed':'The main case retains paid Ready concentration through instantaneous resolution, includes the caster taking32, then ends the hold; no concentration RNG or outcome is supplied.'},'requestedCorrection':'Supply the actual DC16 CON save and resulting state before end-of-resolution cleanup. Include a failure branch and explicitly resolve what happens to the already-created instantaneous blast and spent corpse without a global Ready change. A passing main roll can preserve the intended damage totals; do not silently remove held concentration before resolution.'},
 {'id':'RD8-LOCAL59-02','priority':2,'status':'CORRECTION_REQUIRED','caseIds':['RD8-06-B-COVER'],'title':'The actual stone screen does not block the claimed line of effect','evidence':{'casePointer':'/allCases/11/independentBranches/1','screen':screen,'origin':origin,'legalBodyWitness':witness,'segmentIntersectsScreen':False,'analyticProof':'Along this ray at y32..34, x2..4 and z4..8. The screen starts at x5, so the ray misses it. The witness lies in the Hawk body and in the wall quarter-cylinder.'},'requestedCorrection':'Bind actual screen dimensions that block every relevant origin-to-body witness while leaving the Ram eligible, or revise the branch outcome. Do not override the supplied coordinates with coversHawkRelevantPaths=true. Do not claim complete visual occlusion unless the actual wall-image sight paths are also blocked; blocked LoE alone suffices for non-admission.'},
 {'id':'RD8-LOCAL59-03','priority':2,'status':'SOURCE_RECONCILIATION_REQUIRED','caseIds':['RD8-04-B-DISPEL'],'title':'Greater Dispel branch does not bind its complete captured source set','evidence':{'casePointer':'/allCases/7/independentBranches/2','baseline':'CloudA and CloudB have the same center [18,0,3] and radius20; both can still exist before7.2. The branch only introduces a dispeller, one face17 and an otherwise-lawful later Action.','authority':reg['entries'][40]['exactAuthority'],'observed':'The branch concludes one named cloud ends and mentions another uncaptured cloud, without removing/repositioning the coincident second cloud, fixing the exact Action time/center, or supplying its independent generating-cast check.'},'requestedCorrection':'Bind the actual time, legal dispeller opportunity/location, area center, all extant captured applications and one rank8 check per generating cast. Either preserve both co-located clouds and resolve both, or explicitly make this an independently reset one-cloud fixture. No selective Greater Dispel omission.'},
 {'id':'RD8-LOCAL59-04','priority':2,'status':'CORRECTION_REQUIRED','caseIds':['RD8-03-B','RD8-03-B-COUNTER','RD8-03-B-CONSUMER','RD8-03-B-OUTOFRANGE'],'title':'Ready carrier and corpse inputs contradict their own complete fixture','evidence':{'carrierSTR':18,'carrierSTRSave':0,'carrierWounds':0,'corpseActorAnchor':[10,0,1],'geometryInitialCorpseAnchor':[10,0,2]},'requestedCorrection':'Set the natural STR save to+4 unless an actual source supplies a different value, and use one explicit held-body anchor consistently. Reconcile all baseline/branch mirrors. Preserve legal150lb corpse plus gear carrying and the actual release anchor.'},
 {'id':'RD8-LOCAL59-05','priority':2,'status':'FIXTURE_CORRECTION_REQUIRED','caseIds':['RD8-01-B','RD8-02-A','RD8-04-A-IMMUNE','RD8-05-B','RD8-06-B'],'title':'Copied actor templates retain incompatible form or progression facts','evidence':{'DruidForms':'Hawk/Bear target sheets still claim can actually speak, one actual free hand and held focus, while the Druid engine prohibits Base-form speech, melds gear and prohibits casting before18. The Ironhorn form also cannot cast at15; its speech exception is distinct.','Wizard7':'anchorCaster inRD8-05-B has hero Spellbinder even though Wizard engine permits Hero paths only at10; it is an Arch Arcanist at7.','Ashen':'The fire-immunity branch supplies a full Storm target with lightning/thunder resistance, plus an outer Circle=Ashen Grove override. Its concrete replacement must not retain unrelated Storm grants.','HawkOrigin':'Hawk sheets bind height2 with footZ20 but a nominal spellOriginZ23; it is unused by these target-only cases, so state whether it is unavailable/nonoperative rather than presenting it as a current usable casting source.'},'requestedCorrection':'Reconcile complete form, school/path and component metadata with actual acquired sources, including copied branch sheets. Keep target damage/posture outcomes where unchanged; do not create new forms, casting permissions or dual Circle ownership.'},
 {'id':'RD8-LOCAL59-06','priority':2,'status':'OPPORTUNITY_CLARIFICATION_REQUIRED','caseIds':['RD8-04-A-ENTRY'],'title':'Off-turn voluntary departure lacks the stated legal opportunity','evidence':{'mainTargetStarts':[2,8,14,20],'casterSlot':[0,2],'branchMovement':'Leaves at7, reenters at9; a separate extra-turn opportunity is supplied only at10.','qualification':'The conditional branch qualifies the extra turn at10, not ordinary movement at7 during the caster next regular slot.'},'requestedCorrection':'Provide an actual source-qualified movement opportunity at7, or use a legal movement sequence on the target turn after8, with explicit positions/distance and remaining budget. Preserve the purpose: no entry/extra-turn pulse or exposure reset.'},
 {'id':'RD8-LOCAL59-07','priority':3,'status':'TEXT_CORRECTION_REQUIRED','caseIds':['RD8-01-B-STRAIN-BLOCK'],'title':'Blocked-strain qualification retains the wrong starting value','evidence':{'actorDissonance':17,'changedInput':17,'qualificationText':'Dissonance11 and preceding first use of this name are supplied chronological character state...'},'requestedCorrection':'Change this branch qualification to17; retain the valid limit11+6 bar, no payment, and all original history.'},
 {'id':'RD8-LOCAL59-08','priority':3,'status':'TIMING_CLARIFICATION_REQUIRED','caseIds':['RD8-06-A','RD8-06-B','RD8-06-B-NEWOBSERVER'],'title':'Wall establishment time should be explicit in the finite clock fixture','evidence':{'commitAt':1,'collapseConsequencesAt':1.1,'recordedDeadline':61,'procedure':'Concentration up to60seconds from establishment; immediate collapse when the spell manifests.'},'requestedCorrection':'Name the actual manifestation/establishment timestamp separately from prospective concentration commitment, and derive every deadline from it. If establishment is1.0 and subsequent resolution1.1, state that; if establishment is1.1, deadline is61.1. Do not reset duration at later observation, suppression or release bookkeeping.'}
 ]
 for p,b in preserved.items():assert p.read_bytes()==b,str(p)
 result={'id':'RANK8-DAMAGE6-PART5-SEMANTIC-REVIEW-59','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'verdict':'REQUIRES_BOUNDED_CORRECTIONS_AND_GPT_RECONCILIATION_NOT_ACCEPTED','package':info(A/'DD_Rank8_Damage_6_Part5_Conference_Return_01.zip'),'model':info(P/'MODEL.json'),'cases':info(P/'CASE_DISPOSITIONS.json'),'priorIntegrityReceipt':info(A/'RANK8_DAMAGE6_PART5_RETURN_01_LOCAL_PREFLIGHT.json'),'reviewCoverage':{'sixCompleteProceduresAndSixSharedClausesRead':True,'sixNativeAndCoreRowsAndClassAccessCompared':True,'questionDispositionsRead':20,'mainCasesRead':12,'independentBranchesRead':41,'inheritedInterfaces':'Bound current accepted contracts reused; targeted full Ready, concentration, Wounds, Falling, Prone, carrying, Greater Dispel and class-feature text inspected. This does not reopen every accepted source or certify all global engine interactions.'},'diagnosticChecks':checks,'diagnosticCheckCount':len(checks),'diagnosticFailures':sum(not c['passed'] for c in checks),'findings':findings,'findingsCount':len(findings),'sourceBindings':[info(regpath),info(R/'data/public/class_playtests/wizard.json'),info(R/'data/public/class_playtests/druid.json'),info(R/'data/public/class_playtests/warrior.json'),info(R/'data/public/class_playtests/cleric.json')],'protectedFilesChecked':len(preserved),'sourceInformationDeleted':0,'downloadedCodeExecuted':False,'canonicalChanges':0,'newAcceptedIdentities':0,'acceptedButUnappliedUnchanged':39,'appliedCountsUnchanged':{'reviewed':525,'pending':323,'standalone':249,'interfaces':173},'scope':'Independent authored semantic review and isolated arithmetic/geometry diagnostics. Four deliberately exposed diagnostic failures document concrete gaps; numerical successes do not prove production engine behavior. No downloaded test script run; no runtime/human/balance/cosmology/release acceptance.','nextConference':'Prepare this bounded correction request; deliver after the currently responding Rank7IdentityCasting5 conference without interrupting it.'}
 OUT.write_bytes(enc(result))
 print(json.dumps({'review':info(OUT),'checks':len(checks),'diagnosticFailures':result['diagnosticFailures'],'findings':len(findings),'newAcceptedIdentities':0}))

if __name__=='__main__':main()
