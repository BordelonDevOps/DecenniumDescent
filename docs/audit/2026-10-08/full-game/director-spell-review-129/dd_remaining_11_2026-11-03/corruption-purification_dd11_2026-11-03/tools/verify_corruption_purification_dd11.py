from pathlib import Path
from copy import deepcopy
import json,hashlib,unicodedata,subprocess,shutil,math
REPO=Path(r'C:\ep480fix');PKG=Path(r'C:\Users\cbord\AppData\Local\Temp\DD_Remaining_11_20261103');STAGE=Path(r'C:\Users\cbord\AppData\Local\Temp\DD11_STAGE_20261103');BASE='e9bf6c82cc95f1b954e4ab7741931077066a4aa1';ROOT='docs/audit/2026-10-08/full-game/director-spell-review-129/dd_remaining_11_2026-11-03/corruption-purification_dd11_2026-11-03/'
def nfc(x):
 if isinstance(x,str):return unicodedata.normalize('NFC',x)
 if isinstance(x,list):return [nfc(y) for y in x]
 if isinstance(x,dict):return {nfc(k):nfc(v) for k,v in x.items()}
 return x
def canon(x):return json.dumps(nfc(x),ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def h(x):return hashlib.sha256(canon(x)).hexdigest()
def sha(b):return hashlib.sha256(b).hexdigest()
def raw(c,p):return subprocess.check_output(['git','-C',str(REPO),'show',f'{c}:{p}'])
def read(p):return json.loads((STAGE/(ROOT+p)).read_text(encoding='utf-8'))
c=read('DIRECTOR_CONTRACT.json');src=read('SOURCE_BINDINGS.json');w=read('WITNESS_PACKET.json');profiles=read('ACTOR_PROFILES.json')['profiles'];branches={b['branchId']:b for b in w['branches']};checks=[]
def ck(n,v):checks.append({'check':n,'pass':bool(v)})
contract_bytes=(PKG/'contracts/corruption-purification.json').read_bytes();common=(PKG/'DIRECTOR_COMMON_CONTRACT_01.json').read_bytes()
ck('exact Director contract bytes and hash',sha(contract_bytes)=='3d31fadf72859acc024d3665757323ec1ed057325f28086977fa605100306fb0' and src['directorContractSha256']==sha(contract_bytes))
ck('common Director contract hash is exact',src['commonContractSha256']==sha(common))
ck('returned eleven-contract package identity exact',src['directorReturnSha256']==sha((PKG/'DIRECTOR_RETURN_ALL_11.json').read_bytes()))
ck('four native Abjuration routes represented',set(profiles)=={'Cleric/Abjuration','Wizard/Abjuration','Druid/Abjuration','Mage/Abjuration'})
for route,p in profiles.items():ck('legal level17 rank9 paid profile '+route,p['singleClassLevel']==17 and p['classRankMaximum']==9 and p['maxRP']>=26 and p['targetSpell']['targetSpell']=='corruption-purification' and p['targetSpell']['paidRpCost']==26)
ck('all required case IDs and six TEST_ONLY branches',set(x['id'] for x in c['requiredCases'])=={'CP-P1','CP-P2','CP-A1','CP-R'} and len(branches)==6 and all(x['id'] in {b['caseId'] for b in w['branches']} for x in c['requiredCases']))
ck('all branches explicitly static and noncanonical',all(b['status']=='TEST_ONLY' and b['startState']['canonical'] is False and b['startState']['status']=='TEST_ONLY' for b in w['branches']) and w['scope']=='STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY')
# Byte-exact bindings are independently reopened from the committed source revisions.
for b in src['currentOperationalSourceBindings']:
 try:ck('source byte binding '+b['path'],sha(raw(b['commit'],b['path']))==b['sha256'])
 except Exception:ck('source byte binding '+b['path'],False)
for b in src['directorSources']+src['retainedQualifications']:
 try:ck('Director/qualification byte binding '+b['repositoryPath'],sha(raw(b['commit'],b['repositoryPath']))==b['sha256'])
 except Exception:ck('Director/qualification byte binding '+b['repositoryPath'],False)
nb=c['nativeBinding'];nativeRaw=raw(nb['commit'],nb['repositoryPath']);ck('native source binding byte hash',sha(nativeRaw)==nb['sha256'])
cat=json.loads(nativeRaw);row=cat['spells'][int(nb['pointer'].split('/')[-1])]
ck('native spell identity remains pending with no operational text',row['id']=='corruption-purification' and row['status']=='blocked-pending-operational-review' and row['operational'] is None)
holdb=c['sourceBindings'][0];hold=json.loads(raw(holdb['commit'],holdb['repositoryPath']));qualb=c['retainedQualificationFiles'][0];qual=json.loads(raw(qualb['commit'],qualb['repositoryPath']))
ck('AFP211-B05 source hold remains open',hold['status']=='OPEN' and hold['blockerId']=='AFP211-B05' and c['blockerRetainedOutsideStaticScope']=='AFP211-B05')
ck('all seven inherited AFP231 qualifications remain explicit',qual['qualificationIds']==[f'AFP231-Q{i:02d}' for i in range(1,8)])
# Forward and inverse root snapshots and event chain.
for b in w['branches']:
 state=b['startState'];ck('start hash '+b['branchId'],h(state)==b['startHash']);last=-1;ords={}
 for e in b['events']:
  ck('chronology/metadata '+e['id'],isinstance(e['timeMs'],int) and e['timeMs']>=last and e['sameTimeOrdinal']==ords.get(e['timeMs'],0)+1 and isinstance(e['after']['caster']['spellHistory'][-1]['committedAtMs'],int) and e['actorId']==b['startState']['caster']['id'] and e['castId'] and e['sourceId'] and e['receiptKey'] and 'causalParentEventId' in e);last=e['timeMs'];ords[e['timeMs']]=e['sameTimeOrdinal']
  op=e['forward'][0];ck('forward precondition '+e['id'],state==e['before'] and h(state)==e['beforeHash'] and op['op']=='test-and-replace-root' and op['before']==state)
  state=op['after'];ck('forward result '+e['id'],state==e['after'] and h(state)==e['afterHash'])
 ck('terminal hash '+b['branchId'],state==b['terminalState'] and h(state)==b['terminalHash'])
 for e in reversed(b['events']):
  op=e['inverse'][0];ck('inverse precondition '+e['id'],state==op['before'] and h(state)==e['afterHash']);state=op['after'];ck('inverse restoration '+e['id'],state==e['before'] and h(state)==e['beforeHash'])
 ck('inverse branch restoration '+b['branchId'],state==b['startState'] and h(state)==b['startHash'])
# Every successful route spends 26 RP/one action; no source provider cast is asserted.
for route,bid in [('Cleric/Abjuration','CP-P1-CLERIC'),('Wizard/Abjuration','CP-P2-WIZARD'),('Druid/Abjuration','CP-A1-DRUID'),('Mage/Abjuration','CP-R-MAGE-MIXED')]:
 b=branches[bid];start=b['startState']['caster'];t=b['terminalState']['caster'];commit=next(e for e in b['events'] if e['kind']=='CAST_COMMITMENT');paid=commit['after']['caster']
 ck('successful paid route '+route,t['spellHistory'][0]['rpPaid']==26 and t['spellHistory'][0]['status']=='resolved' and t['spellHistory'][0]['committedAtMs']==0 and paid['resources']['RP']==start['resources']['RP']-26 and paid['actionBudget']['actionsSpent']==1 and paid['actionBudget']['actionAvailable'] is False and t['pendingCast'] is None)
# P1 category-specific changes, once-only source callbacks, and preserved independent records.
p1b=branches['CP-P1-CLERIC'];p1=p1b['terminalState'];p1s=p1b['startState'];g=p1['sourceGraph'];apps=g['applications'];t=p1['target']
ck('CP-P1 ordinary Corrupted ended in graph and target condition',apps['app1']['active'] is False and apps['app1']['version']==2 and apps['app1']['removedAtMs']==1000 and next(x for x in t['conditions'] if x['id']=='app1')['active'] is False)
ck('CP-P1 reversible Unity Exposure current burden zero, history retained',apps['app2']['current']==0 and apps['app2']['historicalMaximum']==9 and apps['app2']['sourceHistory']==p1s['sourceGraph']['applications']['app2']['sourceHistory'] and apps['app2']['removedCurrentBurden']==7)
ck('CP-P1 PT current reversible stage and active symptom ended once',t['PT']['stage']==0 and t['PT']['history']==p1s['target']['PT']['history'] and apps['app3']['currentStage']==0 and apps['app3']['history']==p1s['sourceGraph']['applications']['app3']['history'] and apps['app3']['symptoms'][0]['active'] is False and apps['app3']['symptoms'][0]['callbackCount']==1)
ck('CP-P1 separately eligible symptom ended while KT stage/knowledge/history remain',apps['appKT-symptom']['active'] is False and apps['appKT-symptom']['callbackCount']==1 and t['knowledgeLedger']==p1s['target']['knowledgeLedger'] and next(x for x in t['conditions'] if x['id']=='appKT-symptom')['active'] is False)
ck('CP-P1 Oracle, Null Veil and protected component stay active',apps['sourceO']['active'] and apps['sourceN']['active'] and apps['protectedP']['active'] and apps['sourceN']['namedPurgeRoutes']==['mask confession','Archon temporary blessing','bittersap antidote'] and apps['sourceN']['purificationAuthorized'] is False)
ck('CP-P1 each source callback executed exactly once',len(g['callbacks'])==5 and all(x['count']==1 and x['status']=='executed' for x in g['callbacks'].values()) and g['cureReceipts'][p1['caster']['spellHistory'][0]['castId']]['changedIds']==['app1','app2','app3','appKT-symptom'])
ck('CP-P1 no collateral physical, custody or alignment edits',all(t[k]==p1s['target'][k] for k in ['HP','Wounds','dead','anatomyHistory','alignment','inventory']))
ck('successful Until-dispelled expression resolves without continuing ward or immunity',p1['purificationExpression']['cardDurationField']=='Until dispelled' and p1['purificationExpression']['resolution']=='completed' and p1['purificationExpression']['activeWardAfterResolution'] is False and p1['purificationExpression']['futureImmunity'] is False)
# P2 exact geometry is independently recomputed from the packet cell boxes.
def maxd2(box,c):return sum(max((box[i][0]-c[i])**2,(box[i][1]-c[i])**2) for i in range(3))
def mind2(box,c):return sum(0 if box[i][0]<=c[i]<=box[i][1] else min((box[i][0]-c[i])**2,(box[i][1]-c[i])**2) for i in range(3))
p2=branches['CP-P2-WIZARD']['terminalState'];a=p2['area'];center=a['center'];rad2=a['radiusFt']**2;cells={x['id']:x for x in a['cells']}
ck('CP-P2 independent exact sphere classifications',maxd2(cells['e1']['bounds'],center)<=rad2 and mind2(cells['e2']['bounds'],center)>rad2 and mind2(cells['e3']['bounds'],center)<=rad2<maxd2(cells['e3']['bounds'],center) and mind2(cells['e4']['bounds'],center)<=rad2<maxd2(cells['e4']['bounds'],center))
ck('CP-P2 inside/disjoint/partial mutation permissions',cells['e1']['active'] is False and cells['e2']['active'] is True and len(cells['e3']['partitions'])==2 and cells['e3']['partitions'][0]['active'] is False and cells['e3']['partitions'][1]['active'] is True and cells['e4']['active'] is True and a['parents']['r1']['active'] is True)
retry=branches['CP-P2-WIZARD']['terminalState']['retryResult'];ck('CP-P2 same-key retry returns existing receipt without callbacks or mutations',retry['sameKey'] and retry['duplicateCallbackCount']==0 and retry['stateMutationCount']==0 and retry['oldAppsRecreated'] is False and p2['areaReceipt']['callbackCount']==2 and p2['areaReceipt']['sameKeyRetryCount']==0)
# A1 includes the unwilling occupant before casting, proves later source exposure and dispel behavior.
a1b=branches['CP-A1-DRUID'];a1=a1b['terminalState'];a1s=a1b['startState'];occ=a1['areaOccupant']
ck('CP-A1 unwilling area occupant existed at admission and remains unpurified',a1s['areaOccupant']['willing'] is False and a1s['areaOccupant']['withinSphere'] and occ['purified'] is False and occ['conditions'][0]['active'] is True)
ck('CP-A1 live remote parent creates a distinct allowed app8 without immunity',a1['area']['parents']['r1']['active'] and a1['sourceGraph']['applications']['app8']['active'] and a1['sourceGraph']['applications']['app8']['sourceOwner']=='r1' and a1['sourceGraph']['applications']['app8']['distinctFromRemovedIds']==['e1','e3-inside'] and a1['sourceGraph']['applications']['app8']['purificationImmunity'] is False and a1['purificationImmunity'] is False)
ck('CP-A1 later dispel cannot recreate removed applications',a1['dispelAttempt']['removedApplicationsRecreated'] is False and a1['dispelAttempt']['activeSpellSource'] is False and all(not cellsx['active'] for cellsx in a1['area']['cells'] if cellsx['id']=='e1'))
# R adverse branches: protected-only paid neutral, countered no-refund/no-state-change, mixed preservation.
pr=branches['CP-R-DRUID-PROTECTED']['terminalState'];ck('CP-R Druid protected-only target is a paid neutral result',pr['sourceGraph']['applications']['protected-only']['active'] and pr['sourceGraph']['applications']['protected-only']['version']==1 and pr['sourceGraph']['callbacks']=={} and pr['purificationExpression']['removedIds']==[] and pr['sourceGraph']['cureReceipts'][pr['caster']['spellHistory'][0]['castId']]['callbackCount']==0)
co=branches['CP-R-WIZARD-COUNTERED'];cot=co['terminalState'];ck('CP-R countered commitment is paid, no refund and no provider certified',cot['caster']['resources']['RP']==co['startState']['caster']['resources']['RP']-26 and cot['castFailure']['refundRp']==0 and cot['castFailure']['sourceGraphChanged'] is False and cot['sourceGraph']==co['startState']['sourceGraph'] and cot['counterInput']['status']=='TEST_ONLY_COUNTER_RESULT' and cot['counterInput']['providerCastCertified'] is False and cot['caster']['spellHistory'][0]['status']=='failed-paid-countered')
mb=branches['CP-R-MAGE-MIXED'];mt=mb['terminalState'];ma=mt['sourceGraph']['applications']
ck('CP-R Mage mixed source graph ends eligible only and preserves protections',ma['eligible-app']['active'] is False and ma['protected-parent']['active'] and ma['sourceO']['active'] and mt['sourceGraph']['callbacks']['end-eligible-app']['count']==1)
ck('CP-R Mage preserves knowledge, body, possessions and alignment',all(mt['target'][k]==mb['startState']['target'][k] for k in ['knowledgeLedger','HP','Wounds','dead','anatomyHistory','inventory','alignment']))
# Reviewed identity is authoring-only; no provider, runtime, Unity or source blocker closure.
ck('all positive casts remain TEST_ONLY with source-provider events unclaimed',all(b['status']=='TEST_ONLY' for b in w['branches']) and w['scope']=='STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY' and w['fixtureLimits'].startswith('All source graphs') and all(not any(e['details'].get('providerCastCertified') is True for e in b['events']) for b in w['branches']))
result={'id':'CP-DD11-SEMANTIC-VALIDATION-01','identity':'corruption-purification','status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','scope':'STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY','checks':checks,'checksPassed':sum(x['pass'] for x in checks),'checksFailed':sum(not x['pass'] for x in checks),'branchCount':len(branches),'eventCount':sum(len(b['events']) for b in w['branches']),'runtimeExecuted':False,'unityExecuted':False,'sourceBlockerClosed':False}
(STAGE/ROOT/'SEMANTIC_VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
tool=STAGE/ROOT/'tools'/'verify_corruption_purification_dd11.py';tool.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(Path(__file__),tool);tb=tool.read_bytes();toolbind={'path':ROOT+'tools/verify_corruption_purification_dd11.py','bytes':len(tb),'sha256':sha(tb)}
replay={'id':'CP-DD11-REPLAY-VALIDATION-01','identity':'corruption-purification','status':result['status'],'scope':'STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY','branchCount':len(branches),'eventCount':result['eventCount'],'forwardOperationCount':result['eventCount'],'inverseOperationCount':result['eventCount'],'combinedOperationCount':2*result['eventCount'],'checksPassed':result['checksPassed'],'checksFailed':result['checksFailed'],'verificationScriptBinding':toolbind,'stateCanonicalization':'NFC-normalized, key-sorted compact UTF-8 JSON; serializer included in verification tool.','execution':'Forward/inverse root patches and serialized state hashes independently checked.','runtimeExecuted':False,'unityExecuted':False}
(STAGE/ROOT/'REPLAY_VALIDATION.json').write_text(json.dumps(replay,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':result['status'],'checksPassed':result['checksPassed'],'checksFailed':result['checksFailed'],'failures':[x for x in checks if not x['pass']]},indent=2))
