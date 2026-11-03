from pathlib import Path
import json,hashlib,unicodedata,subprocess,shutil
REPO=Path(r'C:\ep480fix');PKG=Path(r'C:\Users\cbord\AppData\Local\Temp\DD_Remaining_11_20261103');STAGE=Path(r'C:\Users\cbord\AppData\Local\Temp\DD11_STAGE_20261103');BASE='393452669c39791b2e60be6d62c0c5548bd49406';ROOT='docs/audit/2026-10-08/full-game/director-spell-review-129/dd_remaining_11_2026-11-03/faction-perfection_dd11_2026-11-03/'
def nfc(x):
 if isinstance(x,str):return unicodedata.normalize('NFC',x)
 if isinstance(x,list):return [nfc(y) for y in x]
 if isinstance(x,dict):return {nfc(k):nfc(v) for k,v in x.items()}
 return x
def canon(x):return json.dumps(nfc(x),ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def h(x):return hashlib.sha256(canon(x)).hexdigest()
def raw(c,p):return subprocess.check_output(['git','-C',str(REPO),'show',f'{c}:{p}'])
def read(p):return json.loads((STAGE/(ROOT+p)).read_text(encoding='utf-8'))
c=read('DIRECTOR_CONTRACT.json');src=read('SOURCE_BINDINGS.json');w=read('WITNESS_PACKET.json');profiles=read('ACTOR_PROFILES.json')['profiles'];branches={b['branchId']:b for b in w['branches']};checks=[]
def ck(n,v):checks.append({'check':n,'pass':bool(v)})
contract_bytes=(PKG/'contracts/faction-perfection.json').read_bytes();common=(PKG/'DIRECTOR_COMMON_CONTRACT_01.json').read_bytes()
ck('exact Director contract bytes and hash',hashlib.sha256(contract_bytes).hexdigest()=='c016301b74132cbf6d0a7c775bd5c15306319bbaa8d650736034f0cdf2e6b898' and src['directorContractSha256']==hashlib.sha256(contract_bytes).hexdigest())
ck('common model hash is exact',src['commonContractSha256']==hashlib.sha256(common).hexdigest())
ck('all four native level-17 rank-9 routes represented',set(profiles)=={'Cleric/Abjuration','Wizard/Abjuration','Druid/Abjuration','Mage/Abjuration'})
for route,p in profiles.items():ck('legal paid route '+route,p['singleClassLevel']==17 and p['classRankMaximum']==9 and p['maxRP']>=26 and p['targetSpell']['targetSpell']=='faction-perfection' and p['targetSpell']['paidRpCost']==26)
ck('four required case IDs and eight branches',set(x['id'] for x in c['requiredCases'])=={'FP-P1','FP-P2','FP-A1','FP-R'} and len(branches)==8 and all(x in {b['caseId'] for b in w['branches']} for x in ['FP-P1','FP-P2','FP-A1','FP-R']))
ck('fixtures are synthetic and noncanonical',all(b['status']=='TEST_ONLY' and b['startState']['canonical'] is False and b['startState']['faction']['status']=='TEST_ONLY_SYNTHETIC' for b in w['branches']))
for b in w['branches']:
 state=b['startState'];ck('start hash '+b['branchId'],h(state)==b['startHash']);last=-1;ordinals={}
 for e in b['events']:
  ck('event metadata '+e['id'],isinstance(e['timeMs'],int) and e['timeMs']>=last and e['sameTimeOrdinal']==ordinals.get(e['timeMs'],0)+1 and e['actorId']==b['startState']['caster']['id'] and e['castId'] and e['sourceId'] and e['receiptKey'] and 'causalParentEventId' in e);last=e['timeMs'];ordinals[e['timeMs']]=e['sameTimeOrdinal']
  ck('forward event precondition '+e['id'],state==e['before'] and h(state)==e['beforeHash'] and e['forward'][0]['op']=='test-and-replace-root' and e['forward'][0]['before']==state)
  state=e['forward'][0]['after'];ck('forward event result '+e['id'],state==e['after'] and h(state)==e['afterHash'])
 ck('forward terminal '+b['branchId'],state==b['terminalState'] and h(state)==b['terminalHash'])
 for e in reversed(b['events']):
  op=e['inverse'][0];ck('inverse precondition '+e['id'],state==op['before'] and h(state)==e['afterHash']);state=op['after'];ck('inverse restored snapshot '+e['id'],state==e['before'] and h(state)==e['beforeHash'])
 ck('inverse restores branch '+b['branchId'],state==b['startState'] and h(state)==b['startHash'])
# All four class paths pay the exact cast action/RP.
for route,bid in [('Cleric/Abjuration','FP-P1-CLERIC'),('Wizard/Abjuration','FP-P2-WIZARD'),('Druid/Abjuration','FP-R-DRUID'),('Mage/Abjuration','FP-R-MAGE')]:
 b=branches[bid];a=b['terminalState']['caster'];ev=next(e for e in b['events'] if e['kind']=='CAST_COMMITMENT');paid=ev['after']['caster'];ck('paid route encounter '+route,a['spellHistory'][0]['rpPaid']==26 and a['spellHistory'][0]['status']=='resolved' and paid['actionBudget']['actionsSpent']==1 and paid['actionBudget']['actionAvailable'] is False and paid['resources']['RP']==profiles[route]['maxRP']-26)
# P1 full entitlement activation/damage; no fabricated membership.
p1=branches['FP-P1-CLERIC']['terminalState'];p1ev={e['kind']:e for e in branches['FP-P1-CLERIC']['events']};t=p1['target'];ent=t['benefitEntitlement']
ck('FP-P1 standing maximized with versioned history',t['factionStanding']['value']==3 and t['factionStanding']['version']==2 and t['standingHistory'][0]['oldValue']==-1 and t['standingHistory'][0]['newValue']==3 and t['conductHistory']==[{'id':'c1','kind':'TEST_ONLY prior conduct','status':'retained'}])
ck('FP-P1 grant key and one-day expiry',ent['id']=='FactionReserve-40' and ent['key']=='target-01:TEST-DD11-WARDENS:FactionReserve-40' and ent['deadlineMs']==86401000 and ent['deadlineMs']-ent['grantedAtMs']==86400000)
ck('FP-P1 real target Action consumes entitlement',t['actionBudget']['actionsSpent']==1 and t['actionBudget']['actionAvailable'] is False and t['activationReceipt']['entitlementConsumed'] is True and ent['status']=='consumed')
ck('FP-P1 17 post-mitigation damage absorbs from temporary HP only',t['temporaryHP']['amount']==23 and t['HP']=={'current':120,'maximum':120} and t['damageReceipt']['temporaryHPAbsorbed']==17 and t['damageReceipt']['normalHPLoss']==0)
ck('FP-P1 does not grant faction membership, office or invocation',t['membership'] is False and t['office'] is None and 'invocationPermission' not in t)
# P2 consumed history is durable and prevents a second grant.
p2=branches['FP-P2-WIZARD']['terminalState'];p2t=p2['target']
ck('FP-P2 cast paid but no new benefit after prior consumption',p2['caster']['resources']['RP']==profiles['Wizard/Abjuration']['maxRP']-26 and p2t['factionStanding']['value']==3 and p2t['activationAttempt']['allowed'] is False and p2t['activationAttempt']['newTempHP']==0)
ck('FP-P2 preserves old consumed record without another grant',len(p2t['benefitHistory'])==1 and p2t['benefitHistory'][0]['key']=='target-01:TEST-DD11-WARDENS:FactionReserve-40' and p2t['benefitHistory'][0]['status']=='consumed' and p2t['benefitEntitlement'] is None)
# A1 timeline honors standing revocation, resume, suppression and original deadline.
a1b=branches['FP-A1-TIMELINE'];a1=a1b['terminalState'];a1e={e['kind']:e for e in a1b['events']}
ck('FP-A1 plus-one standing suppresses but does not erase remaining pool',a1e['STANDING_DROPS_TO_PLUS_ONE']['after']['target']['factionStanding']['value']==1 and a1e['STANDING_DROPS_TO_PLUS_ONE']['after']['target']['temporaryHP']['amount']==23 and a1e['STANDING_DROPS_TO_PLUS_ONE']['after']['target']['effectiveTemporaryHP']==0)
ck('FP-A1 return to plus three re-enables exactly23, with no refill',a1e['STANDING_RETURNS_TO_PLUS_THREE']['after']['target']['resumedTempHP']==23 and a1e['STANDING_RETURNS_TO_PLUS_THREE']['after']['target']['effectiveTemporaryHP']==23 and a1e['STANDING_RETURNS_TO_PLUS_THREE']['after']['target']['temporaryHP']['amount']==23)
ck('FP-A1 suppression does not pause original one-day clock',a1e['BENEFIT_SUPPRESSED']['after']['target']['suppressionInput']['deadlineMs']==86401000 and a1e['INITIAL_DEADLINE_EXPIRY']['timeMs']==86401000 and a1['target']['benefitExpiredAtMs']==86401000)
ck('FP-A1 final expiry removes pool without rewriting standing/history',a1['target']['temporaryHP']['amount']==0 and a1['target']['effectiveTemporaryHP']==0 and a1['target']['factionStanding']['value']==3 and len(a1['target']['standingHistory'])==3 and a1['target']['benefitHistory'][-1]['status']=='expired-consumed')
# R adverse routes: callback idempotency, stronger pool and paid consent failure.
dr=branches['FP-R-DRUID']['terminalState'];drb=branches['FP-R-DRUID'];dre=next(e for e in drb['events'] if e['kind']=='SAME_KEY_RESOLUTION_RETRY')
ck('FP-R Druid duplicate resolution does not double grant or refresh clock',dre['after']['target']['duplicateResolution']['ignored'] and dre['after']['target']['duplicateResolution']['grantCount']==1 and dre['after']['target']['duplicateResolution']['deadlineBefore']==dre['after']['target']['duplicateResolution']['deadlineAfter'] and len(dr['target']['benefitHistory'])==1)
mg=branches['FP-R-MAGE']['terminalState']['target']
ck('FP-R Mage stronger temporary-HP pool retained while entitlement consumed',mg['temporaryHP']['amount']==60 and mg['temporaryHP']['source']=='preexisting-stronger-test-pool' and mg['activationReceipt']['priorTempHP']==60 and mg['activationReceipt']['resultTempHP']==60 and mg['benefitEntitlement']['status']=='consumed')
cons=branches['FP-R-CONSENT']['terminalState'];ck('FP-R consent revoked after commitment is paid failure',cons['caster']['resources']['RP']==profiles['Druid/Abjuration']['maxRP']-26 and cons['castFailure']['refundRp']==0 and cons['caster']['spellHistory'][0]['status']=='failed-paid' and cons['target']['factionStanding']['value']==1 and cons['target']['benefitEntitlement'] is None)
# A legal second paid cast resets neither the durable key nor its first deadline.
rb=branches['FP-R-WIZARD-RECAST'];r=rb['terminalState'];re={e['kind']:e for e in rb['events']};history=r['caster']['spellHistory'];
ck('FP-R recast pays two casts with repeated-spell Refrain',len(history)==2 and [x['rpPaid'] for x in history]==[26,26] and history[1]['refrain']==1 and r['caster']['resources']['RP']==12 and r['caster']['resources']['Dissonance']==1)
ck('FP-R recast restores standing but preserves conduct and single entitlement',r['target']['factionStanding']['value']==3 and len(r['target']['standingHistory'])==3 and len(r['target']['conductHistory'])==1 and sum(x['id']=='FactionReserve-40' for x in r['target']['benefitHistory'])==1 and re['RECAST_DEADLINE_AND_ENTITLEMENT_CHECK']['after']['target']['recastReceipt']['grantCount']==1)
ck('FP-R recast keeps first deadline and activation consumes original entitlement',re['RECAST_DEADLINE_AND_ENTITLEMENT_CHECK']['after']['target']['recastReceipt']['originalDeadlineMs']==re['RECAST_DEADLINE_AND_ENTITLEMENT_CHECK']['after']['target']['recastReceipt']['currentDeadlineMs']==86401000 and r['target']['benefitEntitlement']['status']=='consumed' and r['target']['temporaryHP']['amount']==40)
# Death leaves the ordinary corpse and equipment while ending the finite benefit.
dth=branches['FP-R-DEATH']['terminalState']['target'];ck('FP-R death ends benefit and retains corpse/equipment',dth['alive'] is False and dth['benefitEntitlement']['status']=='ended-on-death' and dth['temporaryHP']['amount']==0 and dth['corpse']['ordinaryBody'] is True and dth['equipment'][0]['owner']=='target-01')
# Validate exact native row/source hold and scope boundary.
cat=json.loads(raw(BASE,c['nativeBinding']['repositoryPath']));native=cat['spells'][int(c['nativeBinding']['pointer'].split('/')[-1])];hold=json.loads(raw(c['sourceBindings'][0]['commit'],c['sourceBindings'][0]['repositoryPath']));qual=json.loads(raw(c['retainedQualificationFiles'][0]['commit'],c['retainedQualificationFiles'][0]['repositoryPath']))
ck('native Faction Perfection row remains pending/operational null',native['id']=='faction-perfection' and native['status']=='blocked-pending-operational-review' and native['operational'] is None)
ck('AFP211-B04 and qualifications stay open',hold['status']=='OPEN' and hold['blockerId']=='AFP211-B04' and qual['qualificationIds'] and c['blockerRetainedOutsideStaticScope']=='AFP211-B04')
ck('no live institution, canon, campaign or runtime fact created',all(b['startState']['canonical'] is False and b['startState']['faction']['realInstitutionCreated'] is False for b in w['branches']) and w['scope']=='STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY')
result={'id':'FP-DD11-SEMANTIC-VALIDATION-01','identity':'faction-perfection','status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','scope':'STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY','checks':checks,'checksPassed':sum(x['pass'] for x in checks),'checksFailed':sum(not x['pass'] for x in checks),'branchCount':len(branches),'eventCount':sum(len(b['events']) for b in w['branches']),'runtimeExecuted':False,'unityExecuted':False,'sourceBlockerClosed':False}
(STAGE/ROOT/'SEMANTIC_VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
tool=STAGE/ROOT/'tools'/'verify_faction_perfection_dd11.py';tool.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(Path(__file__),tool);tb=tool.read_bytes();toolbind={'path':ROOT+'tools/verify_faction_perfection_dd11.py','bytes':len(tb),'sha256':hashlib.sha256(tb).hexdigest()}
replay={'id':'FP-DD11-REPLAY-VALIDATION-01','identity':'faction-perfection','status':result['status'],'scope':'STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY','branchCount':len(branches),'eventCount':result['eventCount'],'forwardOperationCount':result['eventCount'],'inverseOperationCount':result['eventCount'],'combinedOperationCount':2*result['eventCount'],'checksPassed':result['checksPassed'],'checksFailed':result['checksFailed'],'verificationScriptBinding':toolbind,'stateCanonicalization':'NFC-normalized, key-sorted compact UTF-8 JSON; serializer included in verification tool.','execution':'Forward/inverse root patches and serialized state hashes independently checked.','runtimeExecuted':False,'unityExecuted':False}
(STAGE/ROOT/'REPLAY_VALIDATION.json').write_text(json.dumps(replay,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':result['status'],'checksPassed':result['checksPassed'],'checksFailed':result['checksFailed'],'failures':[x for x in checks if not x['pass']]},indent=2))