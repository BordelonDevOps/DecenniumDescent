from __future__ import annotations
import copy, hashlib, json, subprocess, sys, zipfile
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[5]
BASE = 'docs/audit/2026-10-08/full-game/director-spell-review-129'
PKG = ROOT / BASE / 'elemental_shell_b02_witness_482_repack01'
PRE = f'{BASE}/elemental_shell_b02_integrated_preflight_477_repack01/SHELL_B02_INTEGRATED_PREFLIGHT_477_REPACK01_TESTONLY.json'
READY = f'{BASE}/elemental_shell_b02_integrated_preflight_477_repack01/DIRECTOR_READBACK_477_REPACK01_SUCCESSOR_READY.json'
ADOPT = f'{BASE}/elemental_shell_b02_integrated_preflight_477_repack01/OWNER_DF218_B02_ADOPTION_477_REPACK01_TESTONLY.json'
W, T = PKG/'DF218_B02_WITNESS_482_TESTONLY.json', PKG/'B02_EVENT_TRACE_482.json'
V, R = PKG/'verify_shell_b02_witness_482.py', PKG/'INDEPENDENT_VALIDATION_482.json'
M, D, Z = PKG/'MANIFEST_482.json', PKG/'DELIVERY_482.json', PKG/'DD_ElementalShell_B02_Witness_482_TESTONLY.zip'
README = PKG/'README_482.md'
REF = 'refs/heads/main'

def raw(path): return subprocess.check_output(['git','-C',str(ROOT),'show',f'{REF}:{path}'])
def sha(b): return hashlib.sha256(b).hexdigest()
def blob(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def obj(v): return sha(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
def load(b): return json.loads(b.decode('utf-8-sig'))
def ptr(p): return [x.replace('~1','/').replace('~0','~') for x in p[1:].split('/')]
def get(o,p):
    for k in ptr(p): o=o[k]
    return o
def put(o,p,v,exists):
    a=ptr(p); q=o
    for k in a[:-1]: q=q[k]
    if exists: q[a[-1]]=copy.deepcopy(v)
    else: del q[a[-1]]
def diff(a,b,p=''):
    if type(a) is dict and type(b) is dict:
        out=[]
        for k in sorted(set(a)|set(b)):
            q=p+'/'+str(k).replace('~','~0').replace('/','~1')
            if k not in a: out.append({'op':'add','path':q,'beforeExists':False,'afterExists':True,'after':copy.deepcopy(b[k])})
            elif k not in b: out.append({'op':'remove','path':q,'beforeExists':True,'before':copy.deepcopy(a[k]),'afterExists':False})
            else: out += diff(a[k],b[k],q)
        return out
    if type(a) is type(b) and a==b: return []
    return [{'op':'replace','path':p,'beforeExists':True,'before':copy.deepcopy(a),'afterExists':True,'after':copy.deepcopy(b)}]
def invert(ops):
    out=[]
    for x in reversed(ops):
        if not x['beforeExists']: out.append({'op':'remove','path':x['path'],'beforeExists':True,'before':copy.deepcopy(x['after']),'afterExists':False})
        elif not x['afterExists']: out.append({'op':'add','path':x['path'],'beforeExists':False,'afterExists':True,'after':copy.deepcopy(x['before'])})
        else: out.append({'op':'replace','path':x['path'],'beforeExists':True,'before':copy.deepcopy(x['after']),'afterExists':True,'after':copy.deepcopy(x['before'])})
    return out
def apply(s,ops):
    s=copy.deepcopy(s)
    for x in ops:
        try: old=get(s,x['path']); exists=True
        except (KeyError,IndexError): old=None; exists=False
        assert exists==x['beforeExists'] and (not exists or json.dumps(old,sort_keys=True)==json.dumps(x['before'],sort_keys=True)),x['path']
        put(s,x['path'],x.get('after'),x['afterExists'])
    return s

PKG.mkdir(parents=True,exist_ok=True)
pre_raw, ready_raw=raw(PRE),raw(READY); pre,ready=load(pre_raw),load(ready_raw)
adopt_raw=(ROOT/ADOPT).read_bytes(); adoption=load(adopt_raw); ph=sha(pre_raw)
assert ready['status']=='READY_FOR_OWNER_ADOPTION' and ready['reviewedPreflight']['sha256']==ph==adoption['basis']['proposalSha256']
assert ph=='b673305a49eb10dcfd7da1de676ea883cbcb2f34abcc308310ef00fd0c549c64'
assert adoption['ownerAuthorization']['verbatim']=='Yes—adopt exact 477 Repack01'
prem=pre['proposedOwnerPremises']; facts=pre['sourceDerivedFacts']; sett=prem['proposedRollsAndSettlement']; geo=prem['geometryFeet']
corr={x['path']:x for x in ready['sourceByteCorrespondence']}; bindings=[]
for b in pre['sourceBindings']:
    rawb=raw(b['path']); c=corr[b['path']]
    assert c['declaredSha256']==b['sha256'] and c['declaredBytes']==b['bytes'] and sha(rawb)==c['gitSha256']
    if c['correspondence']=='BYTE_IDENTICAL': assert sha(rawb)==b['sha256']
    bindings.append({**b,'gitBlobSha1':blob(rawb),'gitSha256':sha(rawb),'gitBytes':len(rawb),'sourceByteCorrespondence':c['correspondence'],'verifiedAgainstReadbackPath':READY})
for p,b in [(PRE,pre_raw),(READY,ready_raw),(ADOPT,adopt_raw)]: bindings.append({'path':p,'bytes':len(b),'sha256':sha(b),'gitBlobSha1':blob(b),'gitSha256':sha(b),'gitBytes':len(b),'use':'Exact proposal, Director readiness and owner adoption decision binding.'})
profile_path=next(x['path'] for x in pre['sourceBindings'] if x['path'].endswith('/ACTOR_PROFILES.json'))
wprof=load(raw(profile_path))['Wizard18']; Mage,Wizard,Pet='Mage9-PROPOSED','Wizard18','GreaterFirePet-R2-PROPOSED'
branch='DF218-SHELL-B02-R2-PROPOSED'; scene=prem['scenario']['sceneId']; WF,MF='R2-WIZ-FOCUS-001','R2-FIRE-FOCUS-001'
PS,SS='PET-DF218-SHELL-B02-R2-001','SHELL-DF218-SHELL-B02-R2-001'

def caster(name, wiz):
    x=prem['startingStates']['Wizard18' if wiz else Mage]
    g=geo[name]
    stats=copy.deepcopy(wprof['stats']) if wiz else copy.deepcopy(x['abilityScores'])
    return {'id':name,'identity':'New branch-local hypothetical actor; no prior scene, actor state, inventory identity, custody or campaign history is imported.','class':'Wizard' if wiz else 'Mage','classLevel':18 if wiz else 9,'path':wprof['path'] if wiz else 'Arcanist at level 3','abilityScores':stats,'PB':6 if wiz else 4,'spellAttack':facts['wizard18']['spellAttack'] if wiz else facts['mage9']['spellAttack'],'spellDC':facts['wizard18']['spellDC'] if wiz else facts['mage9']['spellDC'],'boundsFeet':copy.deepcopy(g['bounds']),'centerFeet':copy.deepcopy(g['center']),'supportedByFloor':True,'conscious':True,'alive':True,'consent':{'selfShell':True,'controlledSparring':True},'vitals':{'HP':x['currentHP'],'maximumHP':x['maximumHP'],'RP':x['currentRP'],'maximumRP':x['maximumRP'],'AC':x['currentAC'],'Dissonance':x['dissonance'],'Refrain':x['refrain'],'DissonanceLimit':10 if wiz else x['dissonanceLimit'],'temporaryHP':0,'conditions':[],'nullState':'none','ArcaneWard':copy.deepcopy(x.get('ArcaneWard')) if wiz else None,'matrixModifications':copy.deepcopy(x.get('matrixModifications',{})),'otherFireDefense':'none as adopted test-only premise'},'turn':{'status':'NOT_STARTED','actionAvailable':False,'bonusActionAvailable':False,'reactionAvailable':True,'movementAvailableFeet':0,'startSeconds':None,'endSeconds':None,'magicThisTurn':False},'casting':{'spellAccess':'Adopted branch-local selection and preparation premise; spell identity remains held outside this witness.','activeConcentration':None,'pendingCast':None,'lastSpell':None,'preparedRankedCastFamiliesUsed':[],'castHistory':[],'resourceHistory':[],'activeEffects':[],'counterspell':{'cardId':'wizard.base.counterspell' if wiz else 'mage.arch.counterspell','available':True,'rechargeRounds':2 if wiz else 3,'responseHistory':[]}},'focus':{'id':WF if wiz else MF,'massPounds':1,'custodian':name,'sourceOrCampaignAcquisitionClaimed':False,'hand':'left' if wiz else 'right'},'damageLedger':[],'reflectionLedger':[],'companionControl':{'sharedCommandBudgetAvailable':False,'pendingCommand':None,'executedCommands':[]}}

w=caster(Wizard,True); m=caster(Mage,False)
p={'id':Pet,'identity':'New branch-local pet; absent until successful manifestation at 0.3.','exists':False,'alive':False,'profile':'AC5_ACCEPTED_SOURCE_MODEL.json#/profiles/AC5-PROFILE-GREATER-FIRE-PET-01','createdBy':Mage,'HP':None,'maximumHP':60,'RP':None,'maximumRP':None,'AC':17,'abilities':{'STR':14,'DEX':14,'CON':16,'INT':4,'WIS':10,'CHA':6},'conditions':[],'size':'Medium','weightLb':100,'speedFt':30,'boundsFeet':None,'centerFeet':None,'supportedByFloor':False,'resistances':[],'immunities':[],'nullState':'none','relationshipToWizard':'nonhostile; no hostile aura attempt eligible','auraProfile':{'radiusFt':5,'trigger':'qualifying hostile perceived recipient future regular START','thisBranch':'No hostile aura attempt against consenting Wizard; no aura tick at the final attached phase.'},'carriedItems':[],'sourceClock':None,'offensiveActionAllowance':{'available':False,'consumed':False},'pendingCommand':None,'executedCommandReceipts':[],'defensivePhaseReceipts':[],'damageLedger':[],'status':'NOT_YET_CREATED'}
initial={'schemaVersion':1,'branchId':branch,'classification':'HYPOTHETICAL_TEST_ONLY_BRANCH_STATE','campaignEvent':False,'timeSeconds':0.0,'phase':'BEFORE_MAGE_REGULAR_START','scenario':{'sceneId':scene,'plane':prem['scenario']['plane'],'relationship':prem['scenario']['relationship'],'participants':[Wizard,Mage,Pet],'noParentSceneImported':True},'scene':{'id':scene,'coordinateConvention':'feet; x east, y north, z up; axis-aligned occupied bounds; floor top z=0','floor':copy.deepcopy(geo['floor']),'geometry':copy.deepcopy(geo),'otherBodiesOrObstacles':[],'campaignLocationClaimed':False},'actors':{Wizard:w,Mage:m,Pet:p},'shellSource':{'id':SS,'exists':False,'status':'NOT_MANIFESTED','deadlineSeconds':None},'damageRoots':[],'consumedOnceOnlyKeys':[],'eventLog':[]}
s=copy.deepcopy(initial); timeline=prem['proposedTimelineSeconds']
kinds=['MAGE_START','SUMMON_COMMIT','WIZARD_COUNTERSPELL_DECLINE','PET_MANIFEST','MAGE_END_AFTER_CAST','PET_ATTACHED_DODGE','WIZARD_START','SHELL_COMMIT','MAGE_COUNTERSPELL_DECLINE','SHELL_MANIFEST','WIZARD_END_AFTER_CAST','MAGE_NEXT_START','PET_COMMAND','MAGE_END_AND_VENT','FIRE_STRIKE_AND_REFLECTION']
def event(i):
    t=timeline[i]['time']; eid=f'B02-E{i+1:03d}'; m=s['actors'][Mage]; w=s['actors'][Wizard]; p=s['actors'][Pet]; s['timeSeconds']=t; s['phase']=kinds[i]
    if i in (0,11):
        m['turn'].update({'status':'ACTIVE','actionAvailable':True,'bonusActionAvailable':True,'reactionAvailable':True,'movementAvailableFeet':30,'startSeconds':t,'endSeconds':None,'magicThisTurn':False})
        if i==0: m['companionControl']['sharedCommandBudgetAvailable']=True
    elif i==1:
        cid=sett['eventAndRootIdentity']['summonCastId']; m['vitals']['RP']=16; m['vitals']['Dissonance']=1; m['turn']['actionAvailable']=False; m['turn']['magicThisTurn']=True
        m['casting']['pendingCast']={'spellId':'summon-greater-fire-pet','rank':5,'castId':cid,'status':'PAID_COMMITTED_AWAITING_RESOLUTION','committedAt':t,'components':['V','S','F'],'focusId':MF,'actionSpent':True,'rpPaid':10,'concentrationSlotReserved':True}
        m['casting']['activeConcentration']={'spellId':'summon-greater-fire-pet','castId':cid,'status':'RESERVED_PENDING_SUCCESS'}; m['casting']['lastSpell']={'spellId':'summon-greater-fire-pet','rank':5,'castId':cid,'committedAt':t}
        m['casting']['preparedRankedCastFamiliesUsed'].append('summon-greater-fire-pet'); m['casting']['castHistory'].append({'castId':cid,'spellId':'summon-greater-fire-pet','rank':5,'committedAt':t,'rpPaid':10,'status':'COMMITTED_BEFORE_RESPONSE'}); m['casting']['resourceHistory'].append({'eventId':eid,'resource':'RP','before':26,'after':16,'paid':10})
    elif i in (2,8):
        actor=w if i==2 else m; cid=sett['eventAndRootIdentity']['summonCastId' if i==2 else 'shellCastId']; actor['casting']['counterspell']['responseHistory'].append({'timeSeconds':t,'triggeringCastId':cid,'decision':'DECLINED_ELIGIBLE_RESPONSE','activated':False,'rollMade':False,'rpSpent':0,'reactionSpent':False,'rechargeTriggered':False,'rangeBoundsFeet':57,'lineOfEffectClear':True})
    elif i==3:
        p.update({'exists':True,'alive':True,'HP':60,'boundsFeet':copy.deepcopy(geo[Pet]['bounds']),'centerFeet':copy.deepcopy(geo[Pet]['center']),'supportedByFloor':True,'sourceClock':{'sourceId':PS,'manifestedAt':t,'durationSeconds':60,'deadlineSeconds':60.3},'concentrationId':sett['eventAndRootIdentity']['summonCastId'],'offensiveActionAllowance':{'available':True,'consumed':False},'status':'CREATED_TEST_ONLY'}); m['casting']['pendingCast']=None; m['casting']['activeConcentration']={'spellId':'summon-greater-fire-pet','status':'ACTIVE','sourceId':PS,'deadlineSeconds':60.3}; m['casting']['castHistory'][-1].update({'resolvedAt':t,'status':'SUCCESSFULLY_MANIFESTED'})
    elif i==4: m['turn'].update({'status':'ENDED','endSeconds':t,'actionAvailable':False,'bonusActionAvailable':False,'movementAvailableFeet':0})
    elif i==5: p['defensivePhaseReceipts'].append({'timeSeconds':t,'action':'DODGE','reason':'No command pending at first attached phase.','offensiveAllowanceSpent':False,'attackMade':False,'hostileAuraAttempt':False})
    elif i==6: w['turn'].update({'status':'ACTIVE','actionAvailable':True,'bonusActionAvailable':True,'reactionAvailable':True,'movementAvailableFeet':30,'startSeconds':t,'endSeconds':None,'magicThisTurn':False})
    elif i==7:
        cid=sett['eventAndRootIdentity']['shellCastId']; family='WIZARD18-FIRST-DISTINCT-PREPARED-MATRIX-FAMILY-001'; w['vitals']['RP']=42; w['turn']['actionAvailable']=False; w['turn']['magicThisTurn']=True
        w['casting']['pendingCast']={'spellId':'elemental-shell','rank':9,'castId':cid,'status':'PAID_COMMITTED_AWAITING_RESOLUTION','committedAt':t,'components':['V','S','F'],'focusId':WF,'actionSpent':True,'rpPaid':26,'selectedElement':'fire'}; w['casting']['lastSpell']={'spellId':'elemental-shell','rank':9,'castId':cid,'committedAt':t,'selectedElement':'fire'}
        w['casting']['preparedRankedCastFamiliesUsed'].append(family); w['casting']['castHistory'].append({'castId':cid,'spellId':'elemental-shell','rank':9,'preparedFamilyKey':family,'committedAt':t,'rpPaid':26,'baseDissonance':0,'refrain':0,'status':'COMMITTED_BEFORE_RESPONSE'}); w['casting']['resourceHistory'].append({'eventId':eid,'resource':'RP','before':68,'after':42,'paid':26})
    elif i==9:
        w['casting']['pendingCast']=None; w['casting']['castHistory'][-1].update({'resolvedAt':t,'status':'SUCCESSFULLY_MANIFESTED'}); s['shellSource'].update({'exists':True,'status':'ACTIVE','manifestedAt':t,'durationSeconds':60,'deadlineSeconds':63.3,'spellId':'elemental-shell','bearer':Wizard,'selectedElement':'fire','concentrationRequired':False}); w['casting']['activeEffects'].append({'sourceId':SS,'spellId':'elemental-shell','selectedElement':'fire','manifestedAt':t,'deadlineSeconds':63.3,'preventsFireDamage':True,'concentrationRequired':False})
    elif i==10: w['turn'].update({'status':'ENDED','endSeconds':t,'actionAvailable':False,'bonusActionAvailable':False,'movementAvailableFeet':0})
    elif i==12:
        c={'commandId':'CMD-DF218-SHELL-B02-R2-FIRESTRIKE-001','issuedAt':t,'ownerId':Mage,'petId':Pet,'action':'Fire Strike','status':'PENDING_ATTACHED_PHASE','notSpellOrMagicalClassAbility':True}; m['turn']['bonusActionAvailable']=False; m['companionControl'].update({'sharedCommandBudgetAvailable':False,'pendingCommand':copy.deepcopy(c)}); p['pendingCommand']=copy.deepcopy(c)
    elif i==13: m['vitals']['Dissonance']=0; m['turn'].update({'status':'ENDED','endSeconds':t,'actionAvailable':False,'bonusActionAvailable':False,'movementAvailableFeet':0,'magicThisTurn':False})
    elif i==14:
        ids=sett['eventAndRootIdentity']; eid_attack=ids['fireStrikeEventId']; root=ids['originalDamageRootId']; refl=ids['reflectedDamageRootId']; key=ids['onceOnlyConsumedReflectionKey']; receipt={'commandId':'CMD-DF218-SHELL-B02-R2-FIRESTRIKE-001','attackEventId':eid_attack,'timeSeconds':t,'status':'EXECUTED_ONCE'}
        p['offensiveActionAllowance']={'available':False,'consumed':True,'consumedAt':t}; p['pendingCommand']=None; p['executedCommandReceipts'].append(receipt); m['companionControl']['pendingCommand']=None; m['companionControl']['executedCommands'].append(receipt)
        a=copy.deepcopy(sett['attack']); d=copy.deepcopy(sett['damage']); sh=copy.deepcopy(sett['shellCheckpoint']); rf=copy.deepcopy(sett['reflection']); r1={'rootId':root,'eventId':eid_attack,'parentRootId':None,'sourceActorId':Pet,'targetActorId':Wizard,'damageType':'fire','attackTotal':a['total'],'targetAC':a['bearerAC'],'hit':True,'damageDice':d['dice'],'dieResults':d['d10Results'],'rawDamage':d['preDefenseTotal'],'nullAtCreation':False,'shellCheckpointBeforeOwnImmunity':sh['preOwnImmunityBasis'],'originalDamageToBearer':0,'reflectedAmount':rf['petDamage'],'reflectedRootId':refl,'onceOnlyKey':key}
        r2={'rootId':refl,'parentRootId':root,'eventId':eid_attack,'sourceActorId':Wizard,'targetActorId':Pet,'damageType':'fire','amount':3,'nullAtCreation':False,'recursiveReflection':False,'onceOnlyKey':key}
        s['damageRoots'] += [r1,r2]; s['consumedOnceOnlyKeys'].append(key); w['damageLedger'].append({'rootId':root,'raw':7,'damageTaken':0,'hpBefore':110,'hpAfter':110}); p['damageLedger'].append({'rootId':refl,'parentRootId':root,'amount':3,'hpBefore':60,'hpAfter':57}); p['HP']=57; s['lastSettlement']={'attack':a,'damage':d,'shellCheckpoint':sh,'reflection':rf,'originalRoot':r1,'reflectedRoot':r2,'wizardHPAfter':110,'petHPAfter':57}
    s['eventLog'].append({'eventId':f'B02-E{i+1:03d}','timeSeconds':t,'kind':kinds[i],'detail':timeline[i]['event'],'sourceTimelineIndex':i,'campaignEvent':False})

snaps=[{'stateId':'S000','timeSeconds':0.0,'phase':s['phase'],'stateSha256':obj(s),'completeState':copy.deepcopy(s)}]; events=[]
for i in range(len(timeline)):
    before=copy.deepcopy(s); event(i); after=copy.deepcopy(s); f=diff(before,after); inv=invert(f); assert apply(before,f)==after and apply(after,inv)==before
    events.append({'eventId':f'B02-E{i+1:03d}','timeSeconds':timeline[i]['time'],'kind':kinds[i],'detail':timeline[i]['event'],'sourceTimelineIndex':i,'beforeStateId':f'S{i:03d}','afterStateId':f'S{i+1:03d}','beforeStateSha256':obj(before),'afterStateSha256':obj(after),'forwardOperations':f,'inverseOperations':inv})
    snaps.append({'stateId':f'S{i+1:03d}','timeSeconds':after['timeSeconds'],'phase':after['phase'],'stateSha256':obj(after),'completeState':after})
fw=[o for e in events for o in e['forwardOperations']]; iv=[o for e in reversed(events) for o in e['inverseOperations']]
assert apply(s,iv)==initial
replay={'classification':'COMPLETE_BRANCH_LOCAL_FORWARD_AND_INVERSE_STATE_REPLAY','initialStateId':'S000','finalStateId':snaps[-1]['stateId'],'initialStateSha256':snaps[0]['stateSha256'],'finalStateSha256':snaps[-1]['stateSha256'],'stateSnapshots':snaps,'eventTransitions':events,'completeForwardOperations':fw,'completeInverseOperations':iv,'inverseReplayResult':{'restoresExactInitialState':True,'restoredStateSha256':obj(initial),'expectedInitialStateSha256':obj(initial)}}
term=s
witness={'schemaVersion':1,'id':'DF218-B02-WITNESS-482-REPACK01','classification':'ADOPTED_HYPOTHETICAL_TEST_ONLY_REVERSIBLE_WITNESS','status':'CONSTRUCTED_FOR_DIRECTOR_REVIEW_NOT_SEALED','branchId':branch,'component':'DF218-B02','hypotheticalOnly':True,'noCampaignEventClaim':True,'adoption':{'path':ADOPT,'sha256':sha(adopt_raw),'proposalSha256':ph,'directorReadinessPath':READY,'directorReadinessSha256':sha(ready_raw),'ownerAuthorization':'Yes—adopt exact 477 Repack01'},'sourceProposal':{'path':PRE,'sha256':ph,'id':pre['id']},'sourceBindings':bindings,'adoptedScenario':{'scenario':copy.deepcopy(prem['scenario']),'adoptedPremises':copy.deepcopy(prem),'timeline':copy.deepcopy(timeline),'expectedSettlement':copy.deepcopy(sett),'stateIdentityConvention':'New stable IDs identify branch-local fixture objects only; no imported actor, object, campaign event or canonical rule is asserted.'},'stateTransitionReplay':replay,'terminalStateSummary':{'timeSeconds':7.0,'mage':{'HP':term['actors'][Mage]['vitals']['HP'],'RP':term['actors'][Mage]['vitals']['RP'],'Dissonance':term['actors'][Mage]['vitals']['Dissonance'],'concentration':term['actors'][Mage]['casting']['activeConcentration']},'wizard':{'HP':term['actors'][Wizard]['vitals']['HP'],'RP':term['actors'][Wizard]['vitals']['RP'],'Dissonance':term['actors'][Wizard]['vitals']['Dissonance'],'ArcaneWard':term['actors'][Wizard]['vitals']['ArcaneWard'],'Shell':term['shellSource']},'pet':{'exists':term['actors'][Pet]['exists'],'HP':term['actors'][Pet]['HP'],'deadlineSeconds':term['actors'][Pet]['sourceClock']['deadlineSeconds'],'offensiveActionAllowance':term['actors'][Pet]['offensiveActionAllowance'],'executedCommandReceipts':term['actors'][Pet]['executedCommandReceipts']},'settlement':term['lastSettlement'],'bothSourcesLiveAtTerminal':True},'decisionBoundary':{'B01WitnessChanged':False,'B01DispositionChanged':False,'B02WitnessConstructed':True,'B02DirectorPass':False,'B02Closed':False,'identityAcceptedOrApplied':False,'canonicalRuleChanged':False,'queueChanged':False,'runtimeOrGameplayUse':False,'campaignEventClaimed':False,'sealIssued':False}}
W.write_text(json.dumps(witness,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
T.write_text(json.dumps({'id':'DF218-B02-EVENT-TRACE-482','witnessPath':str(W.relative_to(ROOT)).replace('\\','/'),'witnessSha256':sha(W.read_bytes()),'events':[{'eventId':e['eventId'],'timeSeconds':e['timeSeconds'],'kind':e['kind'],'beforeStateId':e['beforeStateId'],'afterStateId':e['afterStateId'],'beforeStateSha256':e['beforeStateSha256'],'afterStateSha256':e['afterStateSha256'],'forwardOperationCount':len(e['forwardOperations']),'inverseOperationCount':len(e['inverseOperations'])} for e in events],'terminalStateSummary':witness['terminalStateSummary'],'inverseReplayResult':replay['inverseReplayResult'],'campaignEventClaimed':False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
README.write_text(f'''# Elemental Shell DF218-B02 witness 482\n\nReversible hypothetical TEST_ONLY witness for exact owner-adopted Proposal477 Repack01, SHA-256 `{ph}`. It follows all 15 adopted events from Mage START through the single commanded Fire Strike at tick 7.0. Each event has complete before/after states, forward operations and inverse operations; the full inverse sequence restores the exact branch-start state.\n\nThe packet records both paid cast commitments before the eligible Counterspell declines, the manifestation deadlines 60.3 and 63.3, Mage END/Dissonance handling, the Pet's first defensive Dodge, the single command, the 12+8 attack, 2d10 [3,4], Shell prevention of 7 fire and the once-only 3-point reflected root. GPT Director review is pending. No campaign event, B01 change, seal, identity acceptance/application, canon change, queue change or runtime use is claimed.\n''',encoding='utf-8',newline='\n')

# Independent replay verifier uses committed source bytes and the adopted file.
V.write_text(r'''import copy,hashlib,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent; REVIEW=HERE.parent; ROOT=REVIEW.parents[4]; BASE='docs/audit/2026-10-08/full-game/director-spell-review-129'
PRE=f'{BASE}/elemental_shell_b02_integrated_preflight_477_repack01/SHELL_B02_INTEGRATED_PREFLIGHT_477_REPACK01_TESTONLY.json'; READY=f'{BASE}/elemental_shell_b02_integrated_preflight_477_repack01/DIRECTOR_READBACK_477_REPACK01_SUCCESSOR_READY.json'; ADOPT=f'{BASE}/elemental_shell_b02_integrated_preflight_477_repack01/OWNER_DF218_B02_ADOPTION_477_REPACK01_TESTONLY.json'; W=HERE/'DF218_B02_WITNESS_482_TESTONLY.json'; T=HERE/'B02_EVENT_TRACE_482.json'
def raw(p): return subprocess.check_output(['git','-C',str(ROOT),'show',f'refs/heads/main:{p}'])
def sha(b): return hashlib.sha256(b).hexdigest()
def can(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def h(x): return sha(can(x))
def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def keys(p): return [x.replace('~1','/').replace('~0','~') for x in p[1:].split('/')]
def get(o,p):
 for k in keys(p): o=o[k]
 return o
def put(o,p,v,e):
 a=keys(p); q=o
 for k in a[:-1]: q=q[k]
 if e:q[a[-1]]=copy.deepcopy(v)
 else:del q[a[-1]]
def apply(s,ops):
 s=copy.deepcopy(s)
 for x in ops:
  try:o=get(s,x['path']); e=True
  except (KeyError,IndexError):o=None;e=False
  assert e==x['beforeExists'] and (not e or can(o)==can(x['before'])),x['path'];put(s,x['path'],x.get('after'),x['afterExists'])
 return s
w=load(W); t=load(T); a=load(ROOT/ADOPT); ready=json.loads(raw(READY)); pre=json.loads(raw(PRE)); r=w['stateTransitionReplay']; checks=[]
def ck(n,b):checks.append({'check':n,'passed':bool(b)});assert b,n
ck('proposal hash and readiness',sha(raw(PRE))==w['adoption']['proposalSha256']==ready['reviewedPreflight']['sha256'] and w['status']=='CONSTRUCTED_FOR_DIRECTOR_REVIEW_NOT_SEALED')
ck('exact owner adoption and seven premises',a['ownerAuthorization']['verbatim']=='Yes—adopt exact 477 Repack01' and len(a['scope']['adoptedPremises'])==7 and a['scope']['branchId']==w['branchId'])
decl={x['path']:x for x in pre['sourceBindings']}; corr={x['path']:x for x in json.loads(raw(READY))['sourceByteCorrespondence']}; bound={x['path']:x for x in w['sourceBindings']}
ck('17 exact source bindings',set(decl).issubset(bound) and len(decl)==17)
for p,b in decl.items():
 g=raw(p);ck('source '+p,sha(g)==corr[p]['gitSha256'] and len(g)==corr[p]['gitBytes'] and bound[p]['gitBlobSha1']==hashlib.sha1(b'blob '+str(len(g)).encode()+b'\0'+g).hexdigest())
ck('15 events and 16 snapshots',len(r['eventTransitions'])==15 and len(r['stateSnapshots'])==16)
sn={x['stateId']:x['completeState'] for x in r['stateSnapshots']};ck('snapshot hashes',all(x['stateSha256']==h(x['completeState']) for x in r['stateSnapshots']))
cur=copy.deepcopy(sn[r['initialStateId']])
for e in r['eventTransitions']:
 ck('forward '+e['eventId'],h(cur)==e['beforeStateSha256']);cur=apply(cur,e['forwardOperations']);ck('after '+e['eventId'],cur==sn[e['afterStateId']] and h(cur)==e['afterStateSha256']);ck('inverse '+e['eventId'],apply(cur,e['inverseOperations'])==sn[e['beforeStateId']]);cur=copy.deepcopy(sn[e['afterStateId']])
rev=copy.deepcopy(sn[r['finalStateId']])
for e in reversed(r['eventTransitions']):rev=apply(rev,e['inverseOperations'])
ck('complete inverse exact restoration',rev==sn[r['initialStateId']] and r['inverseReplayResult']['restoresExactInitialState'])
f=sn[r['finalStateId']];a=f['actors'];m=a['Mage9-PROPOSED'];wz=a['Wizard18'];p=a['GreaterFirePet-R2-PROPOSED']
ck('paid costs and declined Counterspells',m['vitals']['RP']==16 and wz['vitals']['RP']==42 and all(not x['activated'] and x['rpSpent']==0 and not x['reactionSpent'] for x in wz['casting']['counterspell']['responseHistory']+m['casting']['counterspell']['responseHistory']))
ck('Mage Dissonance remains at first END then vents at later END',next(x for x in r['stateSnapshots'] if x['timeSeconds']==0.9)['completeState']['actors']['Mage9-PROPOSED']['vitals']['Dissonance']==1 and m['vitals']['Dissonance']==0)
ck('original source deadlines live at terminal tick',f['timeSeconds']==7.0 and f['shellSource']['deadlineSeconds']==63.3 and p['sourceClock']['deadlineSeconds']==60.3)
ck('complete Pet profile and no aura tick',set(p['abilities'])=={'STR','DEX','CON','INT','WIS','CHA'} and p['RP'] is None and p['conditions']==[] and p['HP']==57 and not any(x.get('hostileAuraAttempt',False) for x in p['defensivePhaseReceipts']))
ck('attack, Shell settlement, one reflected root',f['lastSettlement']['attack']['total']==20 and f['lastSettlement']['damage']['preDefenseTotal']==7 and p['HP']==57 and len(f['consumedOnceOnlyKeys'])==1 and f['damageRoots'][1]['parentRootId']==f['damageRoots'][0]['rootId'] and not f['damageRoots'][1]['recursiveReflection'])
ck('no seal, identity, canon, queue, runtime or campaign change',not any(w['decisionBoundary'][k] for k in ('B02DirectorPass','B02Closed','identityAcceptedOrApplied','canonicalRuleChanged','queueChanged','runtimeOrGameplayUse','campaignEventClaimed','sealIssued')))
out={'id':'DF218-B02-WITNESS-482-INDEPENDENT-VALIDATION','status':'PASS','checksPassed':len(checks),'checksFailed':0,'proposalSha256':sha(raw(PRE)),'adoptionSha256':sha((ROOT/ADOPT).read_bytes()),'witnessSha256':sha(W.read_bytes()),'traceSha256':sha(T.read_bytes()),'eventCount':len(r['eventTransitions']),'snapshotCount':len(r['stateSnapshots']),'forwardInverseReplay':r['inverseReplayResult'],'queueAndIdentityUnchanged':True,'checks':checks}
(HERE/'INDEPENDENT_VALIDATION_482.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps(out,indent=2))
''',encoding='utf-8',newline='\n')
subprocess.check_call(['python',str(V)],cwd=ROOT)
files=[W,T,V,R,README,PKG/'build_shell_b02_witness_482.py']; manifest={'id':'DF218-B02-WITNESS-482-MANIFEST','classification':'TEST_ONLY_UNSEALED_REVIEW_PACKET','files':[{'path':str(p.relative_to(ROOT)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files],'adoptionPath':ADOPT,'adoptionSha256':sha(adopt_raw),'proposalPath':PRE,'proposalSha256':ph}
M.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
with zipfile.ZipFile(Z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in files+[M,ROOT/ADOPT]: z.write(p,arcname=str(p.relative_to(ROOT)).replace('\\','/'))
delivery={'id':'DF218-B02-WITNESS-482-DELIVERY','status':'READY_FOR_DIRECTOR_REVIEW_NOT_SEALED','branchId':branch,'proposalSha256':ph,'ownerAdoptionPath':ADOPT,'ownerAdoptionSha256':sha(adopt_raw),'witnessPath':str(W.relative_to(ROOT)).replace('\\','/'),'witnessSha256':sha(W.read_bytes()),'tracePath':str(T.relative_to(ROOT)).replace('\\','/'),'traceSha256':sha(T.read_bytes()),'validationPath':str(R.relative_to(ROOT)).replace('\\','/'),'validationStatus':json.loads(R.read_text(encoding='utf-8'))['status'],'manifestPath':str(M.relative_to(ROOT)).replace('\\','/'),'manifestSha256':sha(M.read_bytes()),'zipPath':str(Z.relative_to(ROOT)).replace('\\','/'),'zipSha256':sha(Z.read_bytes()),'decisionBoundary':json.loads(W.read_text(encoding='utf-8'))['decisionBoundary']}
D.write_text(json.dumps(delivery,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'witnessSha256':sha(W.read_bytes()),'validation':json.loads(R.read_text(encoding='utf-8'))['status'],'checksPassed':json.loads(R.read_text(encoding='utf-8'))['checksPassed'],'zipSha256':sha(Z.read_bytes()),'deliverySha256':sha(D.read_bytes())},indent=2))
