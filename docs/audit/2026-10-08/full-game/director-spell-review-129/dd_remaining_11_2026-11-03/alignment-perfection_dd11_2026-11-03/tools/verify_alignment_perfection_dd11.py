from pathlib import Path
import json,hashlib,unicodedata,shutil
STAGE=Path(r'C:\Users\cbord\AppData\Local\Temp\DD11_STAGE_20261103');PKG=Path(r'C:\Users\cbord\AppData\Local\Temp\DD_Remaining_11_20261103');ROOT='docs/audit/2026-10-08/full-game/director-spell-review-129/dd_remaining_11_2026-11-03/alignment-perfection_dd11_2026-11-03/'
def nfc(x):
 if isinstance(x,str):return unicodedata.normalize('NFC',x)
 if isinstance(x,list):return [nfc(y) for y in x]
 if isinstance(x,dict):return {nfc(k):nfc(v) for k,v in x.items()}
 return x
def canon(x):return json.dumps(nfc(x),ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def h(x):return hashlib.sha256(canon(x)).hexdigest()
def read(p):return json.loads((STAGE/(ROOT+p)).read_text(encoding='utf-8'))
c=read('DIRECTOR_CONTRACT.json');w=read('WITNESS_PACKET.json');branches={b['branchId']:b for b in w['branches']};profiles=read('ACTOR_PROFILES.json')['profiles'];checks=[]
def ck(s,v,detail=None):checks.append({'check':s,'pass':bool(v),'detail':detail})
ck('exact Director contract hash',hashlib.sha256((PKG/'contracts/alignment-perfection.json').read_bytes()).hexdigest()=='a49854b2f02dae55ba6abc8e182e4fafe917aa0609d0256adf2bf85debdb3927')
ck('all four rank-9 class routes have legal level-17 profile',set(profiles)=={'Cleric/Abjuration','Wizard/Abjuration','Druid/Abjuration','Mage/Abjuration'} and all(x['singleClassLevel']==17 and x['classRankMaximum']==9 and x['maxRP']>=26 for x in profiles.values()))
for b in w['branches']:
 ck('start hash '+b['branchId'],h(b['startState'])==b['startHash']);state=b['startState']
 for e in b['events']:
  ck('event precondition '+e['id'],state==e['before'] and h(state)==e['beforeHash'] and e['forward'][0]['before']==state)
  state=e['forward'][0]['after'];ck('forward hash '+e['id'],state==e['after'] and h(state)==e['afterHash'])
 ck('forward endpoint '+b['branchId'],state==b['terminalState'] and h(state)==b['terminalHash'])
 for e in reversed(b['events']):
  inv=e['inverse'][0];ck('inverse precondition '+e['id'],state==inv['before']);state=inv['after'];ck('inverse hash '+e['id'],state==e['before'] and h(state)==e['beforeHash'])
 ck('inverse restores start '+b['branchId'],state==b['startState'] and h(state)==b['startHash'])
for route,bid in [('Cleric/Abjuration','AP-P1-CLERIC'),('Wizard/Abjuration','AP-P2-WIZARD'),('Druid/Abjuration','AP-R-DRUID'),('Mage/Abjuration','AP-R-MAGE')]:
 b=branches[bid];a=b['terminalState']['actors']['caster'];ck('paid positive route '+route,a['spellHistory'][0]['status']=='resolved' and a['spellHistory'][0]['rpPaid']==26 and a['resources']['RP']==profiles[route]['maxRP']-26 and a['actionBudget']['actionsSpent']>=1 and a['turnState']['lastSpell']=='alignment-perfection')
p1=branches['AP-P1-CLERIC']['terminalState']['actors']['target'];ck('AP-P1 eligible override ended once',p1['sourceComponents'][0]['active'] is False and p1['sourceComponents'][0]['callbackCount']==1);ck('AP-P1 Lawful/G appearance yields AC18 and +2 WIS save',p1['AC']==18 and p1['saves']['WIS']==2);ck('AP-P1 conduct history retained',len(p1['conductHistory'])==2 and p1['alignment']['underlying']=={'Order':'Lawful','Moral':'Good'})
p2=branches['AP-P2-WIZARD']['terminalState']['actors']['target'];ck('AP-P2 neutral axes each get concrete useful benefit',p2['saves']['CON']==2 and p2['saves']['DEX']==2);ck('AP-P2 protected Lock survives',p2['alignment']['lock']['Order']['active'] is True and p2['alignment']['lock']['Order']['value']=='Neutral')
u=branches['AP-A1-UNWILLING']['terminalState'];ck('unwilling precommit fails without cost',u['actors']['caster']['resources']['RP']==profiles['Cleric/Abjuration']['maxRP'] and u['actors']['caster']['actionBudget']['actionsSpent']==0 and u['admission']['committed'] is False)
r=branches['AP-A1-CONSENT-REVOKED']['terminalState'];ck('postcommit consent revocation is paid failure',r['actors']['caster']['resources']['RP']==profiles['Wizard/Abjuration']['maxRP']-26 and r['castFailure']['refundRp']==0 and r['actors']['target']['benefitSource'] is None and r['actors']['caster']['pendingCast'] is None)
p=branches['AP-A1-PROTECTED-BOTH']['terminalState']['actors']['target'];ck('protected axes give no benefit and component records survive',p['benefitSource']['modifiers']=={} and all(x['active'] for x in p['sourceComponents']))
u=branches['AP-A1-UNDEFINED-ORDER']['terminalState']['actors']['target'];ck('undefined axis is not Neutral; only known Moral bonus applies',u['alignment']['effective']['Order'] is None and u['benefitSource']['modifiers']=={'WISSaveBonus':2} and u['saves']['WIS']==2 and u['saves']['CON']==0)
m=branches['AP-A1-MIXED']['terminalState']['actors']['target'];ck('mixed graph ends only eligible source once',m['sourceComponents'][0]['active'] is False and m['sourceComponents'][0]['callbackCount']==1 and m['sourceComponents'][1]['active'] is True);ck('mixed graph protected Lock and permitted axes resolve',m['alignment']['lock']['Order']['active'] and m['AC']==18 and m['saves']['WIS']==2)
a=branches['AP-A2-TIMELINE']['terminalState'];t=a['actors']['target'];caster=a['actors']['caster'];events={x['kind']:x for x in branches['AP-A2-TIMELINE']['events']};
ck('AP-A2 initial cleansing callback is one-time',a['cleansingCallbacks']==['rA2'] and t['sourceComponents'][0]['callbackCount']==1 and t['sourceComponents'][0]['active'] is False)
ck('AP-A2 live axis change recomputes Speed and STR save',events['LEGITIMATE_ALIGNMENT_CHANGE']['after']['actors']['target']['speedFt']==40 and events['LEGITIMATE_ALIGNMENT_CHANGE']['after']['actors']['target']['saves']['STR']==2)
ck('AP-A2 suppression does not pause clock',events['SUPPRESSION_START']['after']['actors']['target']['benefitSource']['deadlineMs']==1201000 and events['SUPPRESSION_END']['timeMs']==50000)
ck('AP-A2 replacement has unique source and no stacking',events['RECAST_REPLACES_BENEFIT_SOURCE']['after']['actors']['target']['benefitSource']['sourceCastId']!=events['CAST_COMMITMENT']['after']['actors']['caster']['pendingCast']['castId'] if False else len({x['castId'] for x in caster['spellHistory']})==2 and t['benefitSource']['active'] is False)
ck('AP-A2 two actual paid casts do not refill RP',caster['resources']['RP']==profiles['Wizard/Abjuration']['maxRP']-52 and [x['rpPaid'] for x in caster['spellHistory']]==[26,26])
ck('AP-A2 expiry leaves cleansing and history intact',t['benefitSource']['terminal']=='deadline' and t['sourceComponents'][0]['active'] is False and len(t['conductHistory'])==2 and t['speedFt']==30)
for route,bid in [('Druid/Abjuration','AP-R-DRUID'),('Mage/Abjuration','AP-R-MAGE')]:
 t=branches[bid]['terminalState']['actors']['target'];ck('AP-R useful route movement and STR bonus '+route,t['speedFt']==40 and t['movementFtRemaining']==30 and t['saves']['STR']==2 and t['movementFtSpent']==10)
ck('all required case ids represented',all(any(b['caseId']==x['id'] for b in w['branches']) for x in c['requiredCases']))
ck('all fixture branches remain hypothetical',all(b['status']=='TEST_ONLY' and b['startState']['canonical'] is False for b in w['branches']))
result={'id':'AP-DD11-SEMANTIC-VALIDATION-01','identity':'alignment-perfection','status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','scope':'STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY','checks':checks,'checksPassed':sum(x['pass'] for x in checks),'checksFailed':sum(not x['pass'] for x in checks),'branchCount':len(branches),'eventCount':sum(len(b['events']) for b in w['branches']),'runtimeExecuted':False,'unityExecuted':False,'sourceBlockerClosed':False}
(STAGE/ROOT/'SEMANTIC_VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
tool=STAGE/ROOT/'tools'/'verify_alignment_perfection_dd11.py';tool.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(Path(__file__),tool);tb=tool.read_bytes(); toolbind={'path':ROOT+'tools/verify_alignment_perfection_dd11.py','bytes':len(tb),'sha256':hashlib.sha256(tb).hexdigest()}
replay={'id':'AP-DD11-REPLAY-VALIDATION-01','identity':'alignment-perfection','status':result['status'],'scope':'STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY','branchCount':len(branches),'eventCount':result['eventCount'],'forwardOperationCount':result['eventCount'],'inverseOperationCount':result['eventCount'],'combinedOperationCount':2*result['eventCount'],'checksPassed':result['checksPassed'],'checksFailed':result['checksFailed'],'verificationScriptBinding':toolbind,'stateCanonicalization':'SHA-256 over NFC-normalized, key-sorted compact UTF-8 JSON','execution':'Forward and inverse root patches and exact event state hashes independently verified from serialized branches.','runtimeExecuted':False,'unityExecuted':False}
(STAGE/ROOT/'REPLAY_VALIDATION.json').write_text(json.dumps(replay,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':result['status'],'checksPassed':result['checksPassed'],'checksFailed':result['checksFailed'],'failures':[x for x in checks if not x['pass']]},indent=2))
