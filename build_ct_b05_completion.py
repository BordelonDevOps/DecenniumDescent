"""Build the exact adopted CT B05 P04 static witness. No game/runtime execution."""
from pathlib import Path
from copy import deepcopy as C
import json, hashlib, unicodedata, zlib, subprocess

ROOT=Path(__file__).resolve().parent
A='docs/audit/2026-10-08/full-game/director-spell-review-129/'
P=A+'collapse_timeline_b05_integration_preflight_2026-11-03/COLLAPSE_TIMELINE_B05_INTEGRATION_PREFLIGHT_04.json'
OUT=A+'collapse_timeline_b05_witness_2026-11-03/'
HEAD='980c498826c631a3e28a4dc308e534c75c884d35'
PH='d2a6a9b446a678f914ffae951f5dace6fc50de36b135fe0053f6734867769863'
BRANCHES=['CT-B05-BRANCH-COMPAT-01','CT-B05-BRANCH-INCOMPAT-01']
CAST='CT-B05-COLLAPSE-T-CAST-01'
EP='RANK9TIMEFATE6129-ETERNAL-PROPHECY-A-cast1'

SOURCE_BINDINGS={}
def raw(path):
    data=(ROOT/path).read_bytes()
    expected=SOURCE_BINDINGS.get(path)
    if expected and hashlib.sha256(data).hexdigest()!=expected:
        data=subprocess.check_output(['git','show',HEAD+':'+path],cwd=ROOT)
        assert hashlib.sha256(data).hexdigest()==expected,path
    return data
def read(path):return json.loads(raw(path))
def norm(x):
    if isinstance(x,str):return unicodedata.normalize('NFC',x)
    if isinstance(x,list):return [norm(y) for y in x]
    if isinstance(x,dict):return {norm(k):norm(v) for k,v in x.items()}
    return x
def canon(x):return json.dumps(norm(x),ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def h(x):return sha(canon(x))
def write(name,x):
    path=OUT+name;p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode());return bind(path)
def bind(path):
    b=raw(path);return {'path':path,'bytes':len(b),'sha256':sha(b),'crc32':f'{zlib.crc32(b):08x}'}
def esc(k):return k.replace('~','~0').replace('/','~1')
def delta(a,b,path=''):
    if a==b:return []
    if isinstance(a,dict) and isinstance(b,dict):
        ops=[]
        for k in sorted(a.keys()|b.keys()):
            p=path+'/'+esc(k)
            if k not in a:ops.append({'path':p,'beforeExists':False,'afterExists':True,'after':C(b[k])})
            elif k not in b:ops.append({'path':p,'beforeExists':True,'afterExists':False,'before':C(a[k])})
            else:ops.extend(delta(a[k],b[k],p))
        return ops
    return [{'path':path,'beforeExists':True,'afterExists':True,'before':C(a),'after':C(b)}]
def inverse(ops):
    return [dict(path=o['path'],beforeExists=o['afterExists'],afterExists=o['beforeExists'],
                 **({'before':C(o['after'])} if o['afterExists'] else {}),
                 **({'after':C(o['before'])} if o['beforeExists'] else {})) for o in reversed(ops)]
def apply(s,ops):
    s=C(s)
    for o in ops:
        keys=[k.replace('~1','/').replace('~0','~') for k in o['path'].split('/')[1:]]
        if not keys:
            assert s==o['before'];s=C(o['after']);continue
        parent=s
        for k in keys[:-1]:parent=parent[k]
        k=keys[-1];assert (k in parent)==o['beforeExists']
        if o['beforeExists']:assert parent[k]==o['before']
        if o['afterExists']:parent[k]=C(o['after'])
        else:del parent[k]
    return s
class Trace:
    def __init__(self,s):self.initial=C(s);self.state=C(s);self.events=[]
    def event(self,eid,t,fn):
        before=C(self.state);self.state['world']['nowMs']=t;fn(self.state)
        ops=delta(before,self.state);inv=inverse(ops)
        assert apply(before,ops)==self.state and apply(self.state,inv)==before
        self.events.append({'id':eid,'atMs':t,'beforeStateSHA256':h(before),'afterStateSHA256':h(self.state),
                            'beforeState':before,'afterState':C(self.state),'forward':ops,'inverse':inv})
    def audit(self):
        s=C(self.initial)
        for e in self.events:assert h(s)==e['beforeStateSHA256'];s=apply(s,e['forward']);assert h(s)==e['afterStateSHA256']
        terminal=C(s)
        for e in reversed(self.events):s=apply(s,e['inverse']);assert h(s)==e['beforeStateSHA256']
        assert s==self.initial
        return {'forwardPassed':True,'inversePassed':True,'restoredState':s,'restoredSHA256':h(s),
                'terminalSHA256':h(terminal),'eventCount':len(self.events),
                'forwardOperations':sum(len(e['forward']) for e in self.events),
                'inverseOperations':sum(len(e['inverse']) for e in self.events)}

proposal=read(P);assert sha(raw(P))==PH
SOURCE_BINDINGS.update({b['path']:b['sha256'] for b in proposal['sourceBindings']})
spec=proposal['proposedTestOnlyInputSpecification']
for b in proposal['sourceBindings']:assert sha(raw(b['path']))==b['sha256'],b['path']
parent=read(proposal['sourceBindings'][16]['path'])['events'][2]['after']
assert h(parent)=='55de6c13eb5c86784933052e401d8f84ad600d6b1ec8830280eeb693d0c0347c'
epw=read(proposal['sourceBindings'][19]['path'])
obligation=C(epw['branches'][0]['transitions'][0]['forward'][1]['after'])
assert obligation['deadlineMs']==34560000100 and obligation['guaranteeProved'] is False

adoption=write('OWNER_AUTHORIZATION_CT_B05_P04_01.json',{
 'id':'OWNER-AUTHORIZATION-CT-B05-P04-01','classification':'RECORDED_USER_INSTRUCTION_SCOPED_TO_PREVIOUSLY_PRESENTED_PLAN',
 'status':'AUTHORIZED_FOR_EXACT_BOUNDED_CONSTRUCTION','proposal':bind(P),'sourceCommit':HEAD,
 'ownerInstructionExact':'then get it done',
 'context':'User instructed execution after the exact P04 PASS and the enumerated adoption, two-witness construction, evidence review, static identity decision and authorized application steps. This records that instruction in context; it does not assert verbatim delivery of the proposed I-adopt wording.',
 'adoptedProposalId':proposal['id'],'adoptedProposalSHA256':PH,'branchIds':BRANCHES,
 'adoptedInputs':C(proposal['proposedOwnerAdoptionBoundary']['adoptionIncludes']),
 'scope':'Only the two exact P04 TEST_ONLY branches; subsequent review/application limited to STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY.',
 'nativeGuaranteeAuthority':False,'canonChangeAuthorized':False,'runtimeChangeAuthorized':False,
 'campaignOccurrenceAsserted':False,'sealAuthorized':False,'blockerClosureAuthorized':False,
 'standingApplicationAuthority':'Complete pending identities in priority order and apply Director-accepted static authored-review batches.'})

def box(center,half):return {k:[center[i]-half[i],center[i]+half[i]] for i,k in enumerate('xyz')}
def actor_box(pos):return {'x':[pos[0]-2.5,pos[0]+2.5],'y':[pos[1]-2.5,pos[1]+2.5],'z':[pos[2],pos[2]+6]}
def fixture(s):
    s['ctTestOnly']={'proposalSHA256':PH,'planeId':'CT-B05-PLANE-01','guaranteeProved':False,
                     'resolvedEP':False,'resolvedCT':False,'pendingCast':None,'responseWindows':[],
                     'sourceBoundary':'Exact P04 projection; no EP prevention or exceptional terminal/restoration operands.',
                     'geometry':C(spec['closedFixtureProposedForThisPairOnly']['geometry']),
                     'unavailableLedger':{},'disclosures':[],'normalTurnOpen':{'W':True,'T':False}}
    for who in ['W','T']:s['actors'][who]['occupiedBoundsFt']=actor_box(s['actors'][who]['position'])
    book=s['items']['book-W'];book.update(heldBy='W',position=[0,-3.5,2.5],positionConvention='held geometric center',
                                        occupiedBoundsFt=box([0,-3.5,2.5],[.5,.5,.05]),supportedBy='W-held')
    s['items']['gate']['occupiedBoundsFt']=C(spec['closedFixtureProposedForThisPairOnly']['geometry']['gateVolume']['boundsFt'])
    for item in spec['closedFixtureProposedForThisPairOnly']['objects'][2:]:
        x=C(item);x['destroyed']=False
        if item['id']=='CT-B05-FOCUS-T-01':x.update(position=C(item['heldCenter']),occupiedBoundsFt=box(item['heldCenter'],[.5,.5,.05]))
        if item['id']=='CT-B05-SUPPORT-01':x.update(position=[15,0,0],owner='TEST_ONLY fixture owner',available=True)
        s['items'][item['id']]=x
def epdecline(s):s['ctTestOnly']['responseWindows'].append(C(epw['branches'][0]['transitions'][0]['forward'][4]['after']))
def epresolve(s):
    s['ctTestOnly']['resolvedEP']=True;s['obligations'][EP]=C(obligation)
    s['ctTestOnly']['obligationMapping']={'sourceCastId':EP,'soleObligationId':EP,'childId':'CT-B05-EP-OBLIGATION-CREATE-01','castOrPaymentRepeated':False}
def disclose(s):
    record={'id':'CT-B05-OBJECTIVE-DISCLOSURE-01','atMs':100,'speaker':'W','listener':'T',
            'text':spec['collapseCast']['objectiveKnowledgeAndChoice']['exactDisclosure'],'ordinarySpeechCost':0}
    s['actors']['T']['knowledge'].append(record);s['ctTestOnly']['disclosures'].append(C(record))
def marker(s,who,t,start):
    a=s['actors'][who]
    if start:
        assert t not in a['regularStarts'];a['regularStarts'].append(t)
        a['budget']={'Action':1,'BonusAction':1,'Reaction':1,'extraAction':0,'interaction':1,'movement':30}
        a.update(currentRegularStart=t,nextRegularEnd=t+1900,nextRegularStart=t+6000,spellsThisTurn=0)
        for k in a['recharge']:a['recharge'][k]=max(0,a['recharge'][k]-1)
    else:
        assert t not in a['regularEnds'];a['regularEnds'].append(t);a['nextRegularEnd']=None
        # Source engine keeps residual numeric budgets; closed turn prevents their use/banking.
        if not a['spellsThisTurn']:a['Dissonance']=max(0,a['Dissonance']-1);a['Refrain']=0
        if who=='T' and t==3900:
            # Exact adopted T START8000 pre-state expires these normal-turn counters.
            a['budget'].update(Action=0,BonusAction=0,extraAction=0,interaction=0,movement=0)
    s['ctTestOnly']['normalTurnOpen'][who]=start
    s['clockLedger'].append({'actor':who,'atMs':t,'type':'nextRegularStart' if start else 'nextRegularEnd',
                             'deathSaveRequired':False,'readyStatus':None,'rechargeAfter':C(a['recharge'])})
def admission(s):
    s['ctTestOnly']['admission']={'atMs':2000,'actor':'T','anchor':[5,5,0],'rangeFt':5,'samePlane':True,'lineOfEffect':True,
         'ActionAvailable':1,'RPAvailable':64,'components':{'V':True,'S':'right hand free','F':'CT-B05-FOCUS-T-01 left hand'},
         'objectiveDisclosedBeforePayment':True,'sourceVersionHashBeforeAdmission':h(s),
         'objectiveChoice':spec['collapseCast']['objectiveKnowledgeAndChoice']['selectedFeasibleObjective'],
         'riskDisclosure':spec['collapseCast']['objectiveKnowledgeAndChoice']['directorDisclosureBeforePayment']}
def ctcommit(s):
    a=s['actors']['T'];assert a['RP']==64 and a['budget']['Action']==1 and a['seenFamilies']==[]
    a['RP']=38;a['budget']['Action']=0;a['seenFamilies']=['collapse-timeline'];a['lastSpell']='collapse-timeline';a['spellsThisTurn']=1
    receipt=C(spec['collapseCast']['resourceAndHistoryCalculation']['castHistoryEntry']);receipt['id']=CAST
    a['resourceHistory'].append(C(receipt));s['casts'].append(C(receipt))
    s['ctTestOnly']['pendingCast']={'id':CAST,'atMs':2001,'status':'committed-awaiting-response'}
def ctdecline(s):
    assert s['ctTestOnly']['pendingCast']['id']==CAST
    s['ctTestOnly']['responseWindows'].append({'atMs':2001,'observer':'W','triggerCastId':CAST,
        'counterspellSourcePointer':'ACTOR_PROFILES.json#/Wizard/automaticCards/1','distanceFt':5,
        'sightAndLineOfEffect':True,'ReactionAvailable':1,'RPAvailable':38,'rechargeLockRecorded':False,
        'wouldCostRP':3,'wouldCostReaction':1,'wouldHaveDC':28,'outcome':'voluntary decline',
        'reactionSpent':False,'rpSpent':0,'rechargeSpent':False})
def ctresolve(s):
    s['ctTestOnly']['pendingCast']=None;s['ctTestOnly']['resolvedCT']=True
    s['transactions'].append({'id':CAST,'atMs':2001,'status':'resolved-successfully','paidRP':26,'historyRetained':True})
def loss(s):
    x=s['items']['CT-B05-SUPPORT-01'];x.update(position='off-scene-unavailable',custodian='CT-B05-UNAVAILABLE-LEDGER',available=False,providesSupport=False)
    s['ctTestOnly']['unavailableLedger'][x['id']]={
        'objectId':x['id'],'owner':x['owner'],'fromMs':4000,'unavailableThroughMs':34560000100,
        'availableAgainAtMs':34560000101,'noRecoveryTerms':spec['incompatibleCandidatePremise']['noRecoveryTerms'],
        'returnPosition':[15,0,0],'returnCustodian':'cache-site fixture','hypotheticalOnly':True,'returnNotExecutedWithinHorizon':True}
    s['custodyHistory'].append({'atMs':4000,'id':x['id'],'from':'cache-site fixture','to':'CT-B05-UNAVAILABLE-LEDGER','ownerUnchanged':True})
def move(s,dest,cost):
    a=s['actors']['W'];assert s['ctTestOnly']['normalTurnOpen']['W'] and a['budget']['movement']>=cost
    prior=C(a['position']);a['position']=C(dest);a['budget']['movement']-=cost;a['occupiedBoundsFt']=actor_box(dest)
    center=[dest[0],dest[1]-3.5,dest[2]+2.5];book=s['items']['book-W'];book['position']=center;book['occupiedBoundsFt']=box(center,[.5,.5,.05])
    s['outcomes'].append({'type':'ordinary-movement','actor':'W','atMs':6001,'from':prior,'to':dest,'movementSpentFt':cost})
def placement(s):
    a=s['actors']['W'];assert a['budget']['interaction']==1 and s['items']['CT-B05-SUPPORT-01']['available']
    a['budget']['interaction']=0;b=s['items']['book-W'];b.update(position=[15,0,0],positionConvention='bottom-contact footprint center',
        occupiedBoundsFt={'x':[14.5,15.5],'y':[-.5,.5],'z':[0,.1]},heldBy=None,custodian='cache',supportedBy='CT-B05-SUPPORT-01')
    s['custodyHistory'].append({'id':'book-W','atMs':6001,'from':'W','to':'cache','owner':'W','position':[15,0,0]})
    o=s['obligations'][EP];o.update(status='fulfilled',fulfilledAtMs=6001,fulfillmentMethod='ordinary paid movement and one Interaction',guaranteeProved=False)
def no_placement(s):s['outcomes'].append({'type':'no-placement','atMs':6001,'actor':'W','reason':'sole support absent','interactionSpent':0,'bookCustodian':'W'})

tr=Trace(parent)
for eid,t,fn in [('CT-B05-FIXTURE-OVERLAY',100,fixture),('CT-B05-EP-RESPONSE-01',100,epdecline),
                 ('CT-B05-EP-RESOLVE-AND-OBLIGATION-01',100,epresolve),('CT-B05-OBJECTIVE-DISCLOSURE-01',100,disclose),
                 ('W-END-1900',1900,lambda s:marker(s,'W',1900,False)),('T-START-2000',2000,lambda s:marker(s,'T',2000,True)),
                 ('CT-B05-ADMISSION',2000,admission),('CT-B05-COMMIT',2001,ctcommit),
                 ('CT-B05-W-COUNTER-DECLINE',2001,ctdecline),('CT-B05-RESOLVE',2001,ctresolve)]:tr.event(eid,t,fn)
common=C(tr.events);paid=C(tr.state);paidHash=h(paid)
branches=[]
for incompatible in [False,True]:
    tr=Trace(parent);tr.events=C(common);tr.state=C(paid)
    tr.event('T-END-3900',3900,lambda s:marker(s,'T',3900,False))
    if incompatible:tr.event('INCOMPAT-ONLY-SUPPORT-LOSS',4000,loss)
    tr.event('W-START-6000',6000,lambda s:marker(s,'W',6000,True))
    for n,(pt,cost) in enumerate([([0,10,0],10),([15,10,0],15),([15,5,0],5)]):tr.event('W-MOVE-'+str(n+1),6001,lambda s,p=pt,c=cost:move(s,p,c))
    tr.event('W-RETAIN-BOOK' if incompatible else 'W-PLACE-BOOK',6001,no_placement if incompatible else placement)
    tr.event('W-END-7900',7900,lambda s:marker(s,'W',7900,False))
    tr.event('T-START-8000',8000,lambda s:marker(s,'T',8000,True))
    tr.event('CANDIDATE-HORIZON-8001',8001,lambda s:None)
    audit=tr.audit();final=C(tr.state);branch=spec['proposedBranches'][int(incompatible)]
    branches.append({'id':branch['id'],'candidateId':branch['candidateId'],'commonPaidRootSHA256':paidHash,
                     'initialState':C(parent),'initialStateSHA256':h(parent),'commonPrefixEventCount':len(common),
                     'events':C(tr.events),'finalState':final,'finalStateSHA256':h(final),'audit':audit,
                     'disposition':'FILTERED_INCOMPATIBLE_NO_LIVE_WRITE' if incompatible else 'SELECTED_COMPATIBLE',
                     'candidateOnly':True,'policyPriority':2 if incompatible else 1,'witnessSealed':False})

selected=C(branches[0]['finalState'])
selected['futureEvidence']={'packetId':'CT-B05-P04-TESTONLY-WITNESSES-01','branchId':BRANCHES[0],
                          'completeCandidateTraceSHA256':h(branches[0]['events']),'fullStatesAndInversesInPacket':True}
selected['transactions'].append({'id':'CT-B05-SELECT-COMPAT-01','executionKey':'CT-B05-P04-SELECT-01','status':'applied',
                                'sourcePaidRootSHA256':paidHash,'candidateSHA256':branches[0]['finalStateSHA256'],'atMs':8001})
settle=delta(paid,selected);settleInv=inverse(settle)
assert apply(paid,settle)==selected and apply(selected,settleInv)==paid
reject={'id':'CT-B05-INCOMPAT-FILTER-01','candidateId':branches[1]['candidateId'],
        'candidateSHA256':branches[1]['finalStateSHA256'],'paidRootBeforeSHA256':paidHash,'paidRootAfterSHA256':paidHash,
        'reason':'Proposed closed fixture has no support/recovery through inclusive original deadline; protected objective is infeasible.',
        'evaluationStage':'postpayment candidate filter','candidateApplied':False,'refundRP':0}
retryBefore=C(selected)
def retry(state,key,sourceHash):
    receipt=next((r for r in state['transactions'] if r.get('executionKey')==key),None)
    if receipt:return C(state),{'outcome':'IDEMPOTENT_RECEIPT_RETURN','receipt':C(receipt),'newOperations':0}
    assert h(state)==sourceHash,'stale before first execution'
    return apply(state,settle),{'outcome':'APPLIED'}
retryAfter,retryReceipt=retry(selected,'CT-B05-P04-SELECT-01',paidHash)
assert retryAfter==retryBefore
fullRestored=apply(selected,settleInv)
for e in reversed(common):fullRestored=apply(fullRestored,e['inverse'])
assert fullRestored==parent
packet={'schemaVersion':1,'id':'CT-B05-P04-TESTONLY-WITNESSES-01','classification':'ADOPTED_SYNTHETIC_STATIC_TEST_ONLY',
        'sourceCommit':HEAD,'proposal':bind(P),'ownerAuthorization':adoption,'sourceBindings':C(proposal['sourceBindings']),
        'sourceParent':{'path':proposal['sourceBindings'][16]['path'],'pointer':'/events/2/after','stateSHA256':h(parent)},
        'hashDomain':'SHA256 of UTF-8 NFC recursive-key-sorted compact JSON; file bindings use unchanged raw Git bytes.',
        'commonPaidRoot':paid,'commonPaidRootSHA256':paidHash,'branches':branches,
        'selection':{'filteredCandidate':reject,'selectedCandidate':branches[0]['candidateId'],
                     'beforeStateSHA256':paidHash,'afterStateSHA256':h(selected),'afterState':selected,
                     'forward':settle,'inverse':settleInv,'rollbackState':apply(selected,settleInv),
                     'rollbackPreservesBothPayments':True,'sameKeyRetry':{'beforeSHA256':h(retryBefore),'afterSHA256':h(retryAfter),
                     'beforeState':retryBefore,'afterState':retryAfter,'receipt':retryReceipt}},
        'fullAudit':{'restoredState':fullRestored,'restoredSHA256':h(fullRestored),'exactSourceParentRestored':True,
                     'inFictionRefund':False,'inverseSequence':'selected settlement inverse, then common prefix inverses in reverse order'},
        'limits':{'runtimeExecuted':False,'campaignEvent':False,'witnessesSealed':False,'guaranteeProved':False,
                  'blockersClosed':[],'retainedOpenBlockers':['TF192-B05','TF192-B02'],'nativeAuthorityCreated':False,
                  'EPExceptionalOperationsImported':False,'queueChangedByWitness':False}}
b=write('CT_B05_P04_TESTONLY_WITNESS_PACKET_01.json',packet)
print(json.dumps({'witness':b,'branches':[{'id':x['id'],'events':len(x['events']),'operations':x['audit']['forwardOperations']} for x in branches]},indent=2))
