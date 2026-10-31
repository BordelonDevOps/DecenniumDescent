from __future__ import annotations
import copy,hashlib,json,pathlib,shutil,zipfile
BASE=pathlib.Path('docs/audit/2026-10-08/full-game/director-spell-review-129')
OUT=BASE/'rank9_mass_phantom_killer_delta_298'; SRC=BASE/'rank9_psychicfear7_return234_received/DD_Rank9_PsychicFear3_Director_Return234_HELD.zip'
P297=BASE/'rank9_mass_phantom_killer_delta_297/DD_Rank9_MassPhantomKiller_ReviewDelta_297.zip'; D297=P297.parent

def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def h(x):return hashlib.sha256(canon(x)).hexdigest()
def fh(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def dump(rel,x):
 p=OUT/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8');return p
def ops(a,b):return ([{'op':'test','path':'','value':a},{'op':'replace','path':'','value':b}],[{'op':'test','path':'','value':b},{'op':'replace','path':'','value':a}])
def apply(s,os):
 x=s
 for o in os:
  assert o['path']==''
  if o['op']=='test':assert x==o['value']
  elif o['op']=='replace':x=o['value']
  else:raise AssertionError(o)
 return x
def event(i,k,t,d,b,a,src=None):
 f,r=ops(b,a);e={'id':i,'kind':k,'time':t,'detail':d,'before':b,'beforeSHA256':h(b),'after':a,'afterSHA256':h(a),'forward':f,'inverse':r}
 if src:e['sourceEventId']=src
 return e
def static(s,i,k,t):
 a=copy.deepcopy(s);a['time']=t
 for q in s:
  if q!='time':assert s[q]==a[q]
 d={'purpose':'authored static interface review only','providerId':None,'actorId':None,'gameplayActorTurn':False,'actionResolution':'none','expected':'elapsed time advances only; no gameplay mutation'}
 return a,event(i,'CONDITIONAL INTERFACE '+k,t,d,s,a)
def reversible(es,start,end):
 s=start
 for e in es:
  assert s==e['before'] and h(s)==e['beforeSHA256'];assert apply(s,e['forward'])==e['after'] and h(e['after'])==e['afterSHA256'];assert apply(e['after'],e['inverse'])==s;s=e['after']
 assert s==end
 for e in reversed(es):assert s==e['after'];s=apply(s,e['inverse']);assert s==e['before']
 assert s==start;return h(s)
def suffix(src,idx,s,ch):
 out=[];cur=copy.deepcopy(s)
 for old in src[idx:]:
  b=copy.deepcopy(old['before']);cmp=copy.deepcopy(cur);cmp['time']=b['time'];assert cmp==b,old['id']
  a=copy.deepcopy(old['after']);f,r=ops(cur,a);e=copy.deepcopy(old);e.update(before=cur,beforeSHA256=h(cur),after=a,afterSHA256=h(a),forward=f,inverse=r,sourceEventId=old['id'],sourceCaseSHA256=ch)
  assert apply(cur,f)==a and apply(a,r)==cur;out.append(e);cur=a
 return cur,out

with zipfile.ZipFile(SRC) as sz,zipfile.ZipFile(P297) as pz:
 paths=sorted(n for n in sz.namelist() if n.startswith('cases/') and 'MASS-PHANTOM-KILLER' in n and n.endswith('.json'))
 prior={n.split('return234/',1)[1]:n for n in pz.namelist() if n.startswith('return234/cases/') and 'MASS-PHANTOM-KILLER' in n and n.endswith('.json')}
 assert len(paths)==len(prior)==13
 cases={};casehashes={};rows=[];total=0
 for n in paths:
  raw=sz.read(n);assert pz.read(prior[n])==raw;c=json.loads(raw);s=c['initialState'];ih=h(s)
  for e in c['events']:
   assert s==e['before'] and h(s)==e['beforeSHA256'];assert apply(s,e['forward'])==e['after'] and h(e['after'])==e['afterSHA256'];assert apply(e['after'],e['inverse'])==s;s=e['after']
  assert s==c['finalState'];fhsh=h(s)
  for e in reversed(c['events']):assert s==e['after'];s=apply(s,e['inverse']);assert s==e['before']
  assert s==c['initialState'];casehashes[n]=hashlib.sha256(raw).hexdigest();rows.append({'sourceMember':n,'priorDelta297Member':prior[n],'caseSHA256':casehashes[n],'events':len(c['events']),'forwardReplay':'PASS','inverseReplay':'PASS','initialStateSHA256':ih,'finalStateSHA256':fhsh});total+=len(c['events']);cases[n]=c
 assert total==1183
# CI-02: valid manifested spell, static START/END between cast and unchanged turns/expiry.
a_path='cases/RANK9PSYCHICFEAR7-180-MASS-PHANTOM-KILLER-A.json';ac=cases[a_path];ae=ac['events'];fi=2;fork=copy.deepcopy(ae[fi]['after']);assert fork['time']==0.21 and fork['applications'] and not fork['spellOpportunityHistory']
ach=casehashes[a_path];es=[];cur=copy.deepcopy(fork)
for i,k,t in [('CI02-MPK-STATIC-START-01','START',0.3),('CI02-MPK-STATIC-END-01','END',0.4)]:cur,e=static(cur,i,k,t);es.append(e)
end,suf=suffix(ae,fi+1,cur,ach);es+=suf
assert es[2]['time']==0.8 and es[-1]['time']==60.21 and es[-1]['kind']=='absolute expiry before any further opportunity'
assert not any(x.get('active',False) for x in end['applications'])
for e in es[:2]:
 for k in ['spellOpportunityHistory','actorClockHistory','familyExposure','applications','actors','roots']:assert e['after'][k]==fork[k]
assert all(e['after']==ae[i]['after'] for e,i in zip(es[2:],range(fi+1,len(ae))))
ci02={'id':'CI-02-MPK-CONDITIONAL-START-END-LIFECYCLE-TRACE-298','scope':'Mass Phantom Killer; authored static interface review only; no gameplay turn/provider grant','source':{'member':a_path,'caseSHA256':ach,'priorDelta297Member':prior[a_path],'forkAfterEventId':ae[fi]['id'],'forkStateSHA256':h(fork),'forkTime':fork['time']},'injectedInputs':['CI02-MPK-STATIC-START-01','CI02-MPK-STATIC-END-01'],'assertions':{'inputsAdvanceOnlyRootElapsedTime':True,'additionalMPKDamageOpportunity':False,'injectedRegularEndSave':False,'injectedRechargeTick':False,'injectedReactionOrReadyReset':False,'resourceRefundOrCastMutation':False,'deadlineExtension':False,'originalRegularScheduleAndHistoryRetained':True,'originalExpiryStillAt60_21':True,'forwardAndFullInverseTraversal':'PASS','reverseRestoredForkStateSHA256':reversible(es,fork,end)},'conditionalInterfaceEvents':2,'sourceSuffixEvents':len(suf),'history':es,'finalStateSHA256':h(end)}

# CI-04: static inputs then original source-qualified companion phase once.
f_path='cases/RANK9PSYCHICFEAR7-180-MASS-PHANTOM-KILLER-B__source-qualified-attached-phase.json';fc=cases[f_path];fe=fc['events'];fi=11;ff=copy.deepcopy(fe[fi]['after']);assert ff['time']==2
fch=casehashes[f_path];ts=[];cur=copy.deepcopy(ff)
for i,k,t in [('CI04-MPK-STATIC-START-01','START',2.05),('CI04-MPK-STATIC-END-01','END',2.15)]:cur,e=static(cur,i,k,t);ts.append(e)
fend,fsuf=suffix(fe,fi+1,cur,fch);ts+=fsuf
assert [e['kind'] for e in ts[2:5]]==['attached START packet without Action grant','attached END independent WIS','actual regular END H']
for e in ts[:2]:
 for k in ['spellOpportunityHistory','familyExposure','actorClockHistory']:assert e['after'][k]==ff[k]
 assert e['after']['actors']['F']['attachedPhase']==ff['actors']['F']['attachedPhase'] and e['after']['actors']['F']['clockHistory']==ff['actors']['F']['clockHistory']
assert sum(1 for x in ts[2]['after']['spellOpportunityHistory'] if x.get('target')=='F' and x.get('time')==2.3)==1
assert ts[3]['after']['actors']['F']['attachedPhase']['lastPhaseEnd']==2.7 and ts[3]['after']['actors']['F']['attachedPhase']['spentControllerStarts'].count(2)==1
assert ts[3]['after']['familyExposure']==ff['familyExposure'] and fend['actors']['F']['clockHistory']==[] and fend['actors']['F']['calendar'] is None
ci04={'id':'CI-04-MPK-ATTACHED-PHASE-DEDUPLICATION-TRACE-298','scope':'Mass Phantom Killer; existing source-qualified companion evidence; inserted inputs static review only','source':{'member':f_path,'caseSHA256':fch,'priorDelta297Member':prior[f_path],'forkAfterEventId':fe[fi]['id'],'forkStateSHA256':h(ff),'forkTime':ff['time']},'injectedInputs':['CI04-MPK-STATIC-START-01','CI04-MPK-STATIC-END-01'],'assertions':{'conditionalInputsCreateNoOpportunityOrActorClock':True,'existingAttachedStartOccursOnceAt2_3':True,'existingAttachedEndOccursOnceAt2_7':True,'companionHasNoIndependentTurnOrCalendar':True,'noDuplicateFamilyExposure':fend['familyExposure']==ff['familyExposure'],'controllerRegularEndStillOccursAt2_8':ts[4]['time']==2.8,'forwardAndFullInverseTraversal':'PASS','reverseRestoredForkStateSHA256':reversible(ts,ff,fend)},'conditionalInterfaceEvents':2,'sourceSuffixEvents':len(fsuf),'history':ts,'finalStateSHA256':h(fend)}

# CI-01 providerless precommit gate: denial without payment or mutation.
initial=copy.deepcopy(ac['initialState']);assert initial['externalSources']==[] and initial['actors']['A']['RP']==68 and initial['actors']['A']['budgets']['Action']==1 and initial['actors']['A']['castHistory']==[]
req={'spellId':initial['spellId'],'requestedBy':'A','providerId':None,'providerEvidence':None,'gameplayActivationAttempt':True}
gate={'decision':'DENY','reason':'no source-qualified external provider evidence','phase':'precommit','payment':0,'stateMutation':False}
e=event('CI01-MPK-PROVIDERLESS-ACTIVATION-01','STATIC INTERFACE PRECOMMIT DENIAL',initial['time'],{'purpose':'authored static review only; does not execute gameplay','request':req,'gateResult':gate},initial,initial)
ci01={'id':'CI-01-MPK-PROVIDERLESS-GAMEPLAY-ACTIVATION-DENIAL-298','scope':'Static interface gate demonstration only; gameplay remains blocked pending source-qualified provider evidence','source':{'member':a_path,'caseSHA256':ach,'priorDelta297Member':prior[a_path],'precommitStateSHA256':h(initial)},'input':req,'result':gate,'before':initial,'after':initial,'beforeSHA256':h(initial),'afterSHA256':h(initial),'forward':e['forward'],'inverse':e['inverse'],'assertions':{'providerEvidenceMissing':True,'deniedBeforePayment':True,'noRPOrActionMutation':True,'noTimeOrHistoryMutation':True,'forwardAndInverseNoOpReplay':'PASS','reverseRestoredStateSHA256':reversible([e],initial,initial)}}
dump('CI-01_PROVIDERLESS_GAMEPLAY_ACTIVATION_DENIAL_298.json',ci01);dump('CI-02_CONDITIONAL_START_END_LIFECYCLE_TRACE_298.json',ci02);dump('CI-04_ATTACHED_PHASE_DEDUPLICATION_TRACE_298.json',ci04)
dump('FRESH_REPLAY_AUDIT_298.json',{'id':'RANK9-MPK-FRESH-FORWARD-INVERSE-REPLAY-298','sourceArchive':{'path':SRC.as_posix(),'bytes':SRC.stat().st_size,'sha256':fh(SRC)},'priorDelta297':{'path':P297.as_posix(),'bytes':P297.stat().st_size,'sha256':fh(P297)},'mpkCaseCount':13,'eventCount':total,'forwardEventCount':total,'inverseEventCount':total,'sourceCasePayloadsByteExactToDelta297':True,'allInitialStatesRestored':True,'method':'Canonical sorted-key UTF-8 SHA256; root JSON Patch test+replace; exact source-state comparison and full reverse traversal.','results':rows})

# Carry source map and exact limited Director ruling record.
shutil.copy2(D297/'SOURCE_REFRESH_MAP_297.json',OUT/'SOURCE_REFRESH_MAP_297.json');shutil.copy2(D297/'PF182_B02_EXTERNAL_PROVIDER_OBLIGATION_REVISION_REQUEST_297.json',OUT/'PF182_B02_EXTERNAL_PROVIDER_OBLIGATION_REVISION_REQUEST_297.json')
dump('PF297-MPK-EXTERNAL-PROVIDER-REVIEW-REVISION-01.json',{'id':'PF297-MPK-EXTERNAL-PROVIDER-REVIEW-REVISION-01','source':'Director ruling in Calibration review part 6; https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6adc506d-8770-83ea-b64c-0345d9b9b682','scope':'Mass Phantom Killer only','ruling':'Authored-procedure review may use explicitly conditional interface inputs. Actual gameplay still requires source-qualified provider evidence. No provider, ability, gameplay turn, or shared timing rule is created.','status':{'accepted':False,'applied':False,'spell':'HELD'},'excluded':{'CI-03':'Weird; no obligation or incapacity rule changed','otherIdentities':'no ruling or application'},'findings':['Chrono Collapse wording and draft lorebook do not establish operational grant/acquisition on submitted evidence; no universal absence claim.','Prior review checked payload hashes and case records but did not fresh-replay 1,183 events.']})

# Exact authority bytes requested by the Director, including current index + receipts.
AUTH=[('current/authored_review_index.json',pathlib.Path('DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json')),('current/catalog.json',pathlib.Path('DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json')),('current/CURRENT_SPELL_QUEUE_296.json',BASE/'CURRENT_SPELL_QUEUE_296.json'),('current/CURRENT_HANDOFF_296.json',BASE/'CURRENT_HANDOFF_296.json'),('current/CURRENT28_PENDING_IDENTITY_AUDIT_296.json',BASE/'CURRENT28_PENDING_IDENTITY_AUDIT_296.json'),('current/CURRENT_SPELL_REVIEW_SNAPSHOT_296.md',BASE/'CURRENT_SPELL_REVIEW_SNAPSHOT_296.md'),('current/PSYCHIC_SCREAM_ACCEPTANCE_296.json',BASE/'PSYCHIC_SCREAM_ACCEPTANCE_296.json'),('current/PSYCHIC_SCREAM_APPLICATION_296.json',BASE/'PSYCHIC_SCREAM_APPLICATION_296.json'),('current/PSYCHIC_SCREAM_APPLICATION_VALIDATION_296.json',BASE/'PSYCHIC_SCREAM_APPLICATION_VALIDATION_296.json'),('current/PSYCHIC_SCREAM_DIRECTOR_DECISION_296.json',BASE/'PSYCHIC_SCREAM_DIRECTOR_DECISION_296.json'),('current/PSYCHIC_SCREAM_RETURN296_RECEIPT.json',BASE/'PSYCHIC_SCREAM_RETURN296_RECEIPT.json'),('current/PSYCHIC_SCREAM_INDEX_OPERATIONS_296.json',BASE/'PSYCHIC_SCREAM_INDEX_OPERATIONS_296.json'),('current/PSYCHIC_SCREAM_CANDIDATE_PACKAGE_MANIFEST_296.json',pathlib.Path('DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank9psychicscream_reviewed_296/CANDIDATE_PACKAGE_MANIFEST.json'))]
bind=[]
for rel,src in AUTH:
 assert src.is_file(),src;t=OUT/rel;t.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,t);bind.append({'archivePath':rel,'sourcePath':src.as_posix(),'bytes':src.stat().st_size,'sha256':fh(src)})
reg=pathlib.Path('DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_06.json')
if reg.is_file():
 t=OUT/'current/accepted_interface_registry_06.json';shutil.copyfile(reg,t);bind.append({'archivePath':'current/accepted_interface_registry_06.json','sourcePath':reg.as_posix(),'bytes':reg.stat().st_size,'sha256':fh(reg)})
dump('CURRENT_AUTHORITY_298.json',{'id':'RANK9-MPK-CURRENT-AUTHORITY-298','spellReviewTotals':{'applied':820,'pending':28,'acceptedUnapplied':0,'completeStandaloneProcedures':544,'scopedInterfaces':173},'spellScope':{'Psychic Scream':'accepted/applied batch 296','Mass Phantom Killer':'held; no acceptance/application requested','remainingOrder':['Mass Phantom Killer adjudication','Weird / PF182-B02','Final Word / DR217-B01']},'embeddedExactAuthorityBytes':bind,'sourceRefreshMap':'SOURCE_REFRESH_MAP_297.json','sourceRefreshMapSHA256':fh(OUT/'SOURCE_REFRESH_MAP_297.json'),'runtimeEnabled':False})
(OUT/'REQUEST_298.txt').write_text('DIRECTOR REQUEST — DELTA298 COMPLETION RECHECK\n\nPlease adjudicate CI-01, CI-02 and CI-04 for Mass Phantom Killer only, then state the next remaining identity/order/count. CI-03 remains Weird and outside this ruling. The packet carries a fresh full forward/inverse replay of all 13 prior MPK cases (1,183 events), full conditional START/END traces with reverse traversal, exact current index/queue/handoff/pending audit and Psychic Scream acceptance/application receipts, and the current source-refresh map.\n\nMPK remains HELD. No acceptance or application is requested or implied. Conditional inputs are static review inputs only; they do not create a provider, ability, gameplay turn, or shared timing rule.\n',encoding='utf-8')
# Deterministic delivery manifest and ZIP; receipt remains outside archive to avoid self-hash.
files=[]
for p in sorted(OUT.rglob('*')):
 if p.is_file() and p.name not in ['DELIVERY_MANIFEST_298.json','SUBMISSION_RECEIPT_298.json','DD_Rank9_MassPhantomKiller_ReviewDelta_298.zip']:files.append({'path':p.relative_to(OUT).as_posix(),'bytes':p.stat().st_size,'sha256':fh(p)})
dump('DELIVERY_MANIFEST_298.json',{'id':'RANK9-MASS-PHANTOM-KILLER-REVIEW-DELTA-298','fileCountExcludingManifest':len(files),'files':files,'scope':'Focused MPK completion packet; no acceptance/application requested.'})
archive=OUT/'DD_Rank9_MassPhantomKiller_ReviewDelta_298.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for p in sorted(OUT.rglob('*')):
  if p.is_file() and p!=archive and p.name!='SUBMISSION_RECEIPT_298.json':z.write(p,p.relative_to(OUT).as_posix())
dump('SUBMISSION_RECEIPT_298.json',{'id':'SUBMISSION-RECEIPT-298','status':'READY_FOR_DIRECTOR_SUBMISSION','archive':archive.name,'bytes':archive.stat().st_size,'sha256':fh(archive),'acceptanceRequested':False,'applicationRequested':False})
print(json.dumps({'archive':archive.as_posix(),'bytes':archive.stat().st_size,'sha256':fh(archive),'mpkCases':13,'mpkEvents':total,'ci02Events':len(es),'ci04Events':len(ts),'embeddedCurrentFiles':len(bind),'replay':'PASS'},indent=2))
