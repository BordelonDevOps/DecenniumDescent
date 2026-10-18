"""Replay actual GPT nine operations into a preserved successor; no spell adoption."""
from copy import deepcopy
from datetime import datetime,timezone
import hashlib,json,zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded
from prepare_ac5_current_interfaces_01 import at
from prepare_de4_fate_guard_amendment_01 import parent

def read(p):return json.loads(p.read_bytes())
def canon(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def main():
 oldp=R/'data/director/spell_proposals/companion_life_10_current_04.json';out=oldp.with_name('companion_life_10_current_05.json');check=A/'COMPANION_LIFE_10_CURRENT_05_REPLAY_CHECK.json';receipt=A/'COMPANION_LIFE_10_CURRENT_05_PROPOSAL_APPLICATION.json'
 assert not any(p.exists() for p in [out,check,receipt]);pp=A/'companion-life10-current04-review/PROPOSED_CORRECTIONS.json';rp=A/'COMPANION_LIFE_10_CURRENT_04_RETURN_RECEIPT.json';proposal=read(pp);oldraw=oldp.read_bytes();old=json.loads(oldraw);cklist=[]
 def ck(n,v):cklist.append({'check':n,'passed':bool(v)});assert v,n
 ck('Actual input exact',info(oldp)==proposal['targetCandidate']);rr=read(rp);ck('Actual verified returned archive',info(G/rr['returnedArchive']['path'])==rr['returnedArchive']);ck('Actual assistant identity',rr['actualAssistantMessageId']=='a3ef8d40-93f2-475d-b8af-9eed34023d60')
 frozen={}
 with zipfile.ZipFile(A/'DD_Companion_Life_10_Current_04_Draft.zip') as z:
  manifest=json.loads(z.read('MANIFEST.json'));ck('63 frozen sources',len(manifest['files'])==63)
  for b in manifest['files']:
   raw=z.read(b['archivePath']);ck('Exact archived source '+b['path'],len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256']);frozen[b['path']]=raw
  ck('Actual candidate equals archived input',frozen[proposal['targetCandidate']['path']]==oldraw)
  for b in old['sourceBindings']+old['newSourceBindings']:
   raw=frozen[b['path']];ck('56 retained/additional source bindings '+b['path'],len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256'])
 d=deepcopy(old);ops=proposal['operations'];expected=['/records/1','/records/6','/records/8','/currentCases/3','/currentCases/12','/currentCases/13','/currentCases/16','/currentCases/23','/current04ReviewProposedLayer'];ck('Nine exact operation paths',[o['pointer'] for o in ops]==expected)
 for o in ops:
  ck('Source target '+o['id'],o['targetFile']==proposal['targetCandidate']['path']);par,key=parent(d,o['pointer'])
  if o['op']=='replace':
   ck('Complete exact before '+o['id'],o['expectedBefore']=={'present':True} and par[key]==o['completeBefore']);ck('Before canonical hash '+o['id'],canon(par[key])==o['beforeCanonicalSha256'])
  else:ck('One absent-field addition '+o['id'],o['op']=='add' and o['expectedBefore']=={'present':False} and key not in par)
  ck('Complete after canonical hash '+o['id'],canon(o['completeAfter'])==o['afterCanonicalSha256']);par[key]=deepcopy(o['completeAfter'])
 replay_hash=canon(d);reverse=deepcopy(d)
 for o in reversed(ops):
  par,key=parent(reverse,o['pointer']);ck('Exact reverse after '+o['id'],par[key]==o['completeAfter'])
  if o['op']=='replace':par[key]=deepcopy(o['completeBefore'])
  else:del par[key]
 ck('All nine operations reverse to entire Current04',reverse==old and canon(reverse)==canon(old))
 ck('Ten source/access and prior complete procedures retained',len(d['records'])==10 and all(all(a[k]==b[k] for k in a) for a,b in zip(old['records'],d['records'])))
 ck('Six shared rules unchanged',d['sharedRules']==old['sharedRules'] and len(d['sharedRules'])==6)
 ck('Full prior applied history and20 obligations unchanged',d['completePreservedAppliedLayer']==old['completePreservedAppliedLayer'] and d['originalObligationCoverage']==old['originalObligationCoverage'] and len(d['originalObligationCoverage'])==20)
 ck('27 main case IDs order retained',[c['id'] for c in d['currentCases']]==[c['id'] for c in old['currentCases']] and len(d['currentCases'])==27)
 ck('All37 old subbranches retained with one independent positive branch',sum(len(c.get('independentBranches',[])) for c in old['currentCases'])==37 and sum(len(c.get('independentBranches',[])) for c in d['currentCases'])==38)
 for n,(a,b) in enumerate(zip(old['currentCases'],d['currentCases'])):
  ck('Full old case recoverable '+a['id'],b.get('previousCurrent04Version')==a if n in [3,12,13,16,23] else a==b)
 layer=d['current04ReviewProposedLayer'];ck('Exact two content holds',layer['wholeCaseContentHolds']==['IN6-09-A','IN6-09-B'])
 for sel in layer['currentProcedureSelection']:
  ck('Exact selected full procedure '+sel['spellId'],isinstance(at(d,sel['pointer']),str) and len(at(d,sel['pointer']))>1000)
 refs=[ref for o in ops for ref in o.get('sourceRefs',[])]+[ref for rule in layer['newScopedRules'].values() for ref in rule.get('sourceRefs',[])]+d['currentCases'][3]['independentBranches'][3]['sourceRefs']
 for n,ref in enumerate(refs):
  path=ref['path'];ck('New operative reference has full frozen source '+str(n),path in frozen)
  if ref.get('pointer'):ck('New operative JSON pointer resolves '+str(n),at(json.loads(frozen[path]),ref['pointer']) is not None)
 # Independent checks of the newly introduced branch and corrected labels only.
 branch=d['currentCases'][3]['independentBranches'][3];actor=branch['actor'];op=branch['operation'];ex=branch['expected']
 ck('Real Wizard20 positive branch',actor['class']=='Wizard' and actor['classLevel']==20 and actor['RP']==0 and actor['maximumRP']==80 and actor['normalHP']==31 and actor['maximumHP']==6+2+19*(4+2)==122)
 ck('Actual finite waiver and paid HP',op['baseWaived']==7 and op['HPStillPaid']==20 and op['surcharge']==0 and op['recoveryChosen']==3 and actor['normalHP']-20==ex['HP']==11 and ex['RPAfterCommit']==0 and ex['RP']==3 and ex['ReservoirUseRemaining']==0)
 ck('No free second waiver or new concentration',ex['secondWaiverGranted'] is False and ex['concentrationCreated'] is False)
 ck('Zero-output comparator remains independent',d['currentCases'][3]['independentBranches'][2]['operation']==old['currentCases'][3]['independentBranches'][2]['operation'])
 ready=d['currentCases'][23]['events'][1];ck('Preparation and field establishment now distinct','t5' in ready['durationStart'] and 't6.1' in ready['durationStart'] and 't66.1' in ready['durationStart'] and 't13' in ready['durationStart'] and 'Do not select or establish' in ready['checks'])
 ck('Real paid command remains before release/phase',6.05<6.1<6.25<6.5 and 6.1+60==66.1)
 ck('Ghast cone actual witnesses and damage',18-12.5==5.5 and 1<5.5/2==2.75 and (3+4)//2==3 and 3+4==7)
 ck('Wraith real cargo separate from zero body mass',6*15==90 and 20<90 and 2<6/2 and 6/2==3)
 ck('Original source bytes still untouched',oldp.read_bytes()==oldraw)
 previous_meta={k:deepcopy(d[k]) for k in ['id','recordedAtUtc','status','caseCounts','countsUnchanged']}
 d.update(id='COMPANION-LIFE-10-CURRENT-05',recordedAtUtc=datetime.now(timezone.utc).isoformat(),status='UNADOPTED Current05: nine actual Current04 GPT operations exactly replayed/reversed. Codex concurs with four explicitly scoped choices and the Ready-field repair.27 complete main cases/38 independent subbranches;20 preserved original obligations. Two exactCR2 whole-case holds remain. Exact canonical integration review still required.',countsUnchanged={'reviewed':525,'pending':323})
 d['caseCounts']={**d['caseCounts'],'independentSubbranches':38,'clarificationDependentMainIDs':['IN6-09-A','IN6-09-B'],'fullyApprovedCurrentCases':0,'qualification':'The four scoped decisions have joint conference concurrence for drafting; no exact candidate adoption or runtime/human/balance proof.'}
 d['current04ConferenceApplication05']={'actualFinalReceipt':info(rp),'actualProposedOperations':info(pp),'previousCandidate':info(oldp),'previousMetadataUnchanged':previous_meta,'nineOperationReplayCanonicalSha256':replay_hash,'canonicalHashMeaning':'Hash binds full nine-operation result before successor metadata. Individual after hashes bind each returned change.','operationIds':[o['id'] for o in ops],'codexConcurrence':{'newScopedChoices':list(layer['newScopedRules']),'readyFieldCorrection':'CL10-C04-F01','basis':'All changed rule prose and complete changed-case differences locally inspected against supplied exact sources. Source-qualified finite choices preserve printed benefits, real costs, body/gear histories, actual scheduling and distinct holds.','scope':'Concurrence to author exact candidate; no adoption or broader numerical/cosmology conclusion.'},'separateContentSourceSearch':info(A/'COMMAND_UNDEATH_TARGET_SOURCE_SEARCH_01.json'),'historicalBacklinkLimitationRetained':read(A/'companion-life10-current04-review/REVIEW.json')['verificationLimitations'],'exactGPTAcceptance':False,'newRuleAdoptions':0}
 ck('No adoption/runtime/deletion',d['newRuleAdoptions']==d['runtimeTestsExecuted']==d['sourceInformationDeleted']==0 and d['domainGatesUnchanged']==75)
 out.write_bytes(encoded(d));check.write_bytes(encoded({'candidate':info(out),'original':info(oldp),'proposal':info(pp),'checks':cklist,'checkCount':len(cklist),'failures':0,'frozenSources':63,'nestedBindings':56,'operations':9,'mainCases':27,'independentSubbranches':38,'wholeCaseContentHolds':2,'exactReverseCanonicalSha256':canon(reverse),'scope':'Source/hash/reversible-replay/new-branch arithmetic checks only; no gameplay runtime, human playtest or exact acceptance.'}))
 receipt.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'ACTUAL_CONFERENCE_REPLAYED_TO_NEW_UNADOPTED_DRAFT','candidate':info(out),'source':info(oldp),'actualReviewReceipt':info(rp),'replayCheck':info(check),'operationsApplied':9,'originalReplaced':False,'scopedChoicesConcurredForDrafting':list(layer['newScopedRules']),'countsUnchanged':{'reviewed':525,'pending':323},'newRuleAdoptions':0,'sourceInformationDeleted':0,'nextStep':'Prepare full exact canonical model/cases/player/Director and source-convergence evidence. Preserve both Command Undeath whole-case holds and undertake a separate native NPC profile/source conference.'}))
 print(json.dumps({'candidate':info(out),'check':info(check),'receipt':info(receipt),'checks':len(cklist),'mainCases':27,'independentSubbranches':38,'contentHolds':2}))

if __name__=='__main__':main()
