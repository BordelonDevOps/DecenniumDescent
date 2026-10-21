"""Source-derived semantic delta review and exact authored-candidate acceptance; no application."""
from pathlib import Path
from datetime import datetime,timezone
from copy import deepcopy
from fractions import Fraction
import hashlib,json,re
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
P=A/'rank8-damage6-part5-cast-history-return-03';OLD=A/'rank8-damage6-part5-correction-return-02'
OUT=A/'RANK8_DAMAGE6_PART5_CAST_HISTORY_RETURN_03_SEMANTIC_REVIEW_75.json'
ACCEPT=A/'RANK8_DAMAGE6_PART5_EXACT_AUTHORING_ACCEPTANCE_75.json'
def read(p):return json.loads(p.read_bytes())
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def pointer(d,p):
 for k in p.split('/')[1:]:
  k=k.replace('~1','/').replace('~0','~');d=d[int(k)] if isinstance(d,list) else d[k]
 return d
assert not any(p.exists() for p in [OUT,ACCEPT,A/Path(__file__).name])
checks=[]
def ck(n,a,b=True):checks.append({'check':n,'actual':a,'expected':b,'passed':a==b})
def eq(n,a,b):ck(n,a==b)
m=read(P/'MODEL.json');old=read(OLD/'MODEL.json');d=read(P/'CAST_HISTORY_DIAGNOSTIC.json');num=read(P/'NUMERICAL_STATE_EVIDENCE.json')
priorp=A/'RANK8_DAMAGE6_PART5_CORRECTION_RETURN_02_SEMANTIC_RECONCILIATION_70.json';prior=read(priorp)
preflightp=A/'RANK8_DAMAGE6_PART5_CAST_HISTORY_RETURN_03_LOCAL_PREFLIGHT.json';preflight=read(preflightp)
cpfile=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK7_DEADLINE_SEMANTICS_74.json';cp=read(cpfile)
sources=[R/'data/public/class_playtests/wizard.json',R/'docs/mechanics/CLASS_PLAYTEST_RULES.md',R/'data/director/spell_review/accepted_interface_registry_06.json',R/'data/public/spell_playtests/catalog.json']
protected=[p for p in P.rglob('*') if p.is_file()]+sources+[cpfile,priorp,preflightp]
protected += [G/cp[k]['path'] for k in ['currentWorkQueue','currentAuthoredIndex','currentAcceptedInterfaceRegistry','decisionLedger']]
protected += [G/b['path'] for b in cp['canonicalHelperBaselinesUnchanged']]
before={p:info(p) for p in protected}
ck('Exact separate preservation result',[preflight['checkCount'],preflight['failures']],[1498,0])
ck('Prior semantic evidence retains its qualification',[prior['diagnosticCheckCount'],prior['diagnosticFailures']],[334,1])
for key in ['records','selectedSharedRules','reviewQuestionDispositions02','questions','authorityRouting02','proposedScopedRuleSelections02','reviewBoundaries02','riskCounts']:
 eq('Complete prior semantics unchanged '+key,m[key],old[key])
ck('Complete prior case inventory',[len(m['currentVectors']),sum(len(c['independentBranches']) for c in m['currentVectors'])],[12,42])
for i,(a,b) in enumerate(zip(m['currentVectors'],old['currentVectors'])):
 if i!=9:eq('Prior entire main case unchanged '+a['id'],a,b)
case=m['currentVectors'][9];oldcase=old['currentVectors'][9]
for a,b in zip([case]+case['independentBranches'],[oldcase]+oldcase['independentBranches']):
 actor=a['actorSheets']['anchorCaster'];prev=b['actorSheets']['anchorCaster'];restored=deepcopy(actor)
 ck(a['id']+' used family',actor['matrixFamiliesUsed'],['dimensional-anchor'])
 ck(a['id']+' full original cast history retained',actor['initialSetup'].startswith(prev['initialSetup']))
 ck(a['id']+' explicit same encounter','same actual encounter' in actor['initialSetup'] and 'no intervening encounter boundary' in actor['initialSetup'])
 restored['matrixFamiliesUsed']=prev['matrixFamiliesUsed'];restored['initialSetup']=prev['initialSetup'];eq(a['id']+' all other actor fields exact',restored,prev)
 eq(a['id']+' all independent timeline/outcome objects exact',{k:v for k,v in a.items() if k not in ['actorSheets','independentBranches']},{k:v for k,v in b.items() if k not in ['actorSheets','independentBranches']})
blocks=[json.loads(s) for s in re.findall(r'```json\n(.*?)\n```',(P/'DIRECTOR_REVIEW.md').read_text(encoding='utf-8'),re.S)]
eq('Director complete case mirror',blocks[0]['allCases'],m['currentVectors'])
eq('Director complete hold mirror',blocks[1],read(P/'HOLD_REGISTER.json'))
eq('Case dispositions complete mirror',read(P/'CASE_DISPOSITIONS.json')['allCases'],m['currentVectors'])
for row in read(P/'CAST_HISTORY_SOURCE_EVIDENCE.json')['completeExcerpts']:
 s=row['source'];p=P/s['path'];raw=p.read_bytes();ck('Full source binding '+s.get('pointer',s.get('heading')),[len(raw),hashlib.sha256(raw).hexdigest()],[s['bytes'],s['sha256']])
 if 'pointer' in s:eq('Complete source excerpt '+s['pointer'],pointer(json.loads(raw),s['pointer']),row['completeValue'])
 else:ck('Complete exact heading excerpt '+s['heading'],row['completeValue'] in raw.decode('utf-8') and row['completeValue'].startswith(s['heading']))
wiz=read(sources[0]);reg=read(sources[2]);a=d['initialActor'];base=case['actorSheets']['anchorCaster'];op=d['actualOpportunity'];geo=d['geometry'];calc=d['calculation']
eq('Independent actor preserves every supporting sheet field',{k:a[k] for k in base},base)
eq('Diagnostic initial full actor mirror',d['initialState']['actor'],a)
ck('Actual Wizard7 legal maximum RP/rank',[a['maxRP'],a['diagnosticActualRepertoire']['rank']],[wiz['rpByClassLevel'][6],wiz['maxSpellRankByClassLevel'][6]])
ck('Correct independent strain Limit',a['Limit'],max(4,2+a['PB']+max(0,(a['abilityScores']['INT']-10)//2)))
ck('Existing family and previous name',[a['matrixFamiliesUsed'],a['previousSpell'],a['Dissonance'],a['Refrain']],[['dimensional-anchor'],'Dimensional Anchor',0,0])
ck('Same actual prepared repertoire',all(a['diagnosticActualRepertoire'][k] for k in ['recordedInActualBook','actuallyPrepared']))
ck('No level7 Hero grant',a['hero'],None)
ck('SourceQualified existing spell','Action; range 60 feet; V/S/F.' in reg['entries'][22]['exactAuthority'] and 'concentration up to one minute' in reg['entries'][22]['exactAuthority'])
ck('Spell blocks transport but not this cast','spells generally' in reg['entries'][22]['exactAuthority'])
ck('Actual finite turn bounds',op['start']<op['commit']<op['establish']<op['end']<op['nextStart'])
ck('Actual opportunity not extra Action',[op['kind'],op['alreadyCommittedActionsThisTurn'],op['extraActionSource']],['actual-regular-own-turn',0,None])
distance=sum((Fraction(str(x))-Fraction(str(y)))**2 for x,y in zip(geo['spellOrigin'],geo['selectedPoint']))
ck('Independent exact squared distance',int(distance),109);ck('Actual point within source range',distance<=60**2)
ck('Actual components supplied',sorted(d['components']),['F','S','V'])
ck('Actual point perceived',geo['actualPointPerceived'])
ck('Source price for rank4',calc['baseRP'],[0,2,3,5,7,10,13,17,21,26][4])
ck('Precast zero below Limit means no surcharge',calc['strainSurcharge'],0)
ck('Repeated family does not waive base',[calc['familyAlreadyUsed'],calc['protectedBaseWaived'],calc['baseDissonance']],[True,False,1])
ck('Repeated name adds next Refrain',[calc['RefrainBefore'],calc['RefrainAddition'],calc['RefrainAfter']],[0,1,1])
ck('Independent resulting payment and strain',[calc['RPAfter'],calc['DissonanceAfter']],[17-7,0+1+1])
ck('Original omission counterfactual still repeats name',[d['originalOmissionComparator']['incorrectDissonanceAfter'],d['originalOmissionComparator']['correctDissonanceAfter']],[0+0+1,0+1+1])
# Rebuild every entire post-state from the disclosed initial state and actual source rules.
start=deepcopy(d['initialState']);eq('START state has no free reset',d['timeline'][0]['state'],start)
ck('First cast remains spent and paid',[d['prefix']['RPBefore'],d['prefix']['RPAfter'],d['prefix']['baseDissonance'],d['prefix']['field']['originalDeadline']],[24,24-7,0,-1+60])
commit=deepcopy(start);commit['at']=6.05
commit['actor'].update(RP=17-7,Dissonance=0+1+1,Refrain=1,actionAvailable=False,concentration='prospective actual Dimensional Anchor committed at6.05')
commit['field'].update(state='ended-by-incompatible-new-concentration',actualEndedAt=6.05)
commit.update(ordinaryActionCommittedThisTurn=True,RPspentThisDiagnostic=7,concentrationEndEvents=[{'sourceId':'anchor-prior-minus1','at':6.05,'cause':'new lawful concentration commitment','originalDeadline':59,'refund':False}])
eq('Entire commitment before state',d['timeline'][1]['before'],start);eq('Independently reconstructed entire commitment after',d['timeline'][1]['after'],commit)
resolved=deepcopy(commit);resolved['at']=6.1;deadline=float(Fraction('6.1')+60)
resolved['actor']['concentration']='new actual Anchor at[30,0,0],radius60,deadline66.1'
resolved['field']={'id':'anchor-repeat-6_1','spellId':'dimensional-anchor','owner':'anchorCaster','center':[30,0,0],'radius':60,'establishedAt':6.1,'originalDeadline':deadline,'state':'live','concentration':True}
eq('Entire resolution before state',d['timeline'][2]['before'],commit);eq('Independently reconstructed entire resolution after',d['timeline'][2]['after'],resolved)
final=deepcopy(resolved);final.update(at=8,regularTurnEnded=True)
eq('Entire END before state',d['timeline'][3]['before'],resolved);eq('Independently reconstructed END without idle recovery',d['timeline'][3]['after'],final);eq('Complete expected final state',d['expectedFinalState'],final)
for key,value in [('initialState',start),('independentlyComputedCommitment',commit),('independentlyComputedResolution',resolved),('independentlyComputedFinal',final)]:eq('Numerical evidence entire object '+key,num[key],value)
ck('Actual one Action no Reaction or BonusAction debit',[final['actor']['actionAvailable'],final['actor']['reactionAvailable'],final['actor']['bonusActionAvailable']],[False,True,True])
ck('Actual old ending only once with historical deadline',len(final['concentrationEndEvents']),1)
ck('No imaginary RNG',final['rngDraws'],0)
ck('No encounter reset',final['encounterBoundariesSinceMinus1'],[])
ck('Final health unchanged',[final['actor']['hp'],final['actor']['tempHP']],[44,0])
ck('No new original main branch outcome',[d['originalMainAndBranchOutcomesEdited'],d['conditionalBranchCountChanged'],d['runtimeExecuted'],d['newGlobalRule']],[False]*4)
holds=read(P/'HOLD_REGISTER.json');ck('Independent positive-case holds retained',holds['retainedIndependentWholePositiveCaseHolds'],['IN6-09-A','IN6-09-B','EN5-01-A','EN5-01-B','EN6-03-B'])
for p,b in before.items():assert info(p)==b,str(p)
failures=[c for c in checks if not c['passed']]
assert not failures,json.dumps(failures)
report={'id':'RANK8-DAMAGE6-CAST-HISTORY-SEMANTIC-REVIEW-75','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
 'verdict':'RD8_LOCAL70_01_RECONCILED_NO_REMAINING_IDENTIFIED_COHORT_CORRECTIONS','model':info(P/'MODEL.json'),'diagnostic':info(P/'CAST_HISTORY_DIAGNOSTIC.json'),
 'priorSemanticReview':info(priorp),'independentPreservation':info(preflightp),'diagnosticChecks':checks,'diagnosticCheckCount':len(checks),'diagnosticFailures':0,
 'inheritedEvidence':{'priorApplicableDiagnostics':334,'priorPasses':333,'priorQualification':'RD8-LOCAL70-01','qualificationNow':'Resolved by exact nine-sheet correction and independently reconstructed full later-cast states.','noDoubleCounting':'Prior333 diagnostics and1498 preservation checks are separate evidence, not counted as new semantic checks.','basis':'Only two supporting-actor fields change; all procedures/shared rules/questions/prior eight correction outcomes remain exact.'},
 'sourceBindings':[info(p) for p in sources],'downloadedCodeExecuted':False,'runtimeTestsExecuted':0,'implementationApplied':False,'sourceInformationDeleted':0,'humanPlaytests':0,'balanceApproval':False,'cosmologyChanges':0,'releaseApproval':False,
 'independentComputedStates':{'commitment':commit,'resolution':resolved,'final':final},'retainedHolds':holds}
OUT.write_bytes(enc(report))
accept={'id':'RANK8-DAMAGE6-PART5-EXACT-AUTHORING-ACCEPTANCE-75','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
 'status':'EXACT_AUTHORED_SUCCESSOR_ACCEPTED_WITH_DISCLOSED_QUALIFICATIONS_NOT_APPLIED',
 'scope':'Independent authored semantic acceptance of these exact six proposed procedures and source-qualified examples, including retained conditional external inputs and declared scoped Soul Pyre completion. This does not authorize or implement canonical integration, execute a production engine, validate numeric balance or approve release.',
 'selectedSuccessor':info(P/'MODEL.json'),'archive':info(A/'DD_Rank8_Damage_6_Part5_Cast_History_Return_03.zip'),'localSemanticReview':info(OUT),'localPreservation':info(preflightp),
 'actualGptFinal':info(A/'GPT_PART5_RANK8_CAST_HISTORY_RETURN_03_NATIVE.json'),'actualAssistantTurn':'d87b38d5-7614-46bb-825e-2da9141c7cdb',
 'priorSemanticReview':info(priorp),'identities':[r['spellId'] for r in m['records']],'identityCount':6,'selectedCaseCount':12,'selectedBranchCount':42,
 'holdRegister':info(P/'HOLD_REGISTER.json'),'retainedWholePositiveCaseHolds':holds['retainedIndependentWholePositiveCaseHolds'],
 'newAcceptedButUnappliedIdentities':6,'previousAcceptedButUnapplied':39,'resultingAcceptedButUnapplied':45,
 'appliedCountsUnchanged':{'reviewed':525,'pending':323,'standalone':249,'interfaces':173,'total':848},
 'sourceInformationDeleted':0,'canonicalFilesChanged':0,'implementationApplied':False,'ownerImplementationReservationRetained':True,'runtimeTestsExecuted':0,'humanPlaytests':0,'balanceApproval':False,'cosmologyApproval':False,'wholeGameComplete':False,'releaseApproval':False,
 'requiredLaterIntegration':'Owner separately authorizes integration. Use exact selected model and scoped interfaces with reciprocal Banishment slot/corpse/pulse/damage/Ready obligations. Preserve all holds and previous rules; do not count acceptance as applied catalog coverage.'}
ck('Six distinct exact identities',len(set(accept['identities'])),6)
assert checks[-1]['passed']
ACCEPT.write_bytes(enc(accept));(A/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
print(json.dumps({'semanticReview':info(OUT),'checks':report['diagnosticCheckCount'],'failures':0,'acceptance':info(ACCEPT),'acceptedUnapplied':45,'identities':accept['identities']}))
