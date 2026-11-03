from pathlib import Path
import json,hashlib,unicodedata,subprocess,shutil
REPO=Path(r'C:\ep480fix');PKG=Path(r'C:\Users\cbord\AppData\Local\Temp\DD_Remaining_11_20261103');STAGE=Path(r'C:\Users\cbord\AppData\Local\Temp\DD11_STAGE_20261103');BASE='a48937bb3ccb568497e270cac75eeddae52f338f';ROOT='docs/audit/2026-10-08/full-game/director-spell-review-129/dd_remaining_11_2026-11-03/imprisonment_dd11_2026-11-03/';ID='imprisonment'
def nfc(x):
 if isinstance(x,str):return unicodedata.normalize('NFC',x)
 if isinstance(x,list):return [nfc(y) for y in x]
 if isinstance(x,dict):return {nfc(k):nfc(v) for k,v in x.items()}
 return x
def canon(x):return json.dumps(nfc(x),ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def h(x):return sha(canon(x))
def raw(c,p):return subprocess.check_output(['git','-C',str(REPO),'show',f'{c}:{p}'])
def read(p):return json.loads((STAGE/(ROOT+p)).read_text(encoding='utf-8'))
c=read('DIRECTOR_CONTRACT.json');src=read('SOURCE_BINDINGS.json');w=read('WITNESS_PACKET.json');profiles=read('ACTOR_PROFILES.json')['profiles'];bs={b['branchId']:b for b in w['branches']};checks=[]
def ck(name,value):checks.append({'check':name,'pass':bool(value)})
cb=(PKG/'contracts/imprisonment.json').read_bytes();common=(PKG/'DIRECTOR_COMMON_CONTRACT_01.json').read_bytes();ret=(PKG/'DIRECTOR_RETURN_ALL_11.json').read_bytes()
ck('Exact Director contract bytes and hash',sha(cb)=='dfe3f2b1edae9e8dc76f9fde5e691c2ae6de0036de5f1a94a2a500aa8f4a8f7f' and src['directorContractSha256']==sha(cb))
ck('Exact common contract and combined Director return hashes',src['commonContractSha256']==sha(common) and src['directorReturnSha256']==sha(ret))
expected={'IM-P1-WIZARD','IM-P1-CLERIC','IM-P2-DRUID','IM-P2-MAGE','IM-A1-SUCCESSFUL-SAVE','IM-A1-COLLISION-PAID-FAIL','IM-A1-CASTER-DEATH','IM-A1-TARGET-DEATH','IM-A1-GROWTH-COLLISION','IM-A1-PHRASE-RELEASE','IM-A2-PARTIAL-SUPPRESSION-EXIT','IM-A2-OCCUPIED-RESUMPTION','IM-A2-ELIGIBLE-DISPEL','IM-A2-DUPLICATE-RELEASE','IM-A2-24H-DEADLINE','IM-A2-SAME-DIFFERENT-OWNER-RECAST','IM-A2-RESOLUTION-RACE'}
ck('All 17 Director-required isolated branches exist',set(bs)==expected and len(bs)==17)
ck('Four native class-school routes are covered',set(profiles)=={'Wizard/Necromancy','Cleric/Necromancy','Druid/Necromancy','Mage/Universal'})
for route,p in profiles.items():
 ck('Legal class17 rank9 route/cost '+route,p['singleClassLevel']==17 and p['classRankMaximum']==9 and p['maxRP']>=26 and p['targetSpell']['targetSpell']==ID and p['targetSpell']['rank']==9 and p['targetSpell']['school']==route.split('/')[1] and p['targetSpell']['acquiredAtClassLevel']==17 and p['targetSpell']['paidRpCost']==26 and p['targetSpell']['preparedOrKnown'])
for s in src['currentOperationalSourceBindings']:
 try:ck('Exact source blob '+s['path'],sha(raw(s['commit'],s['path']))==s['sha256'])
 except Exception:ck('Exact source blob '+s['path'],False)
for s in src['directorSources']+src['retainedQualifications']:
 try:ck('Exact Director source blob '+s['repositoryPath'],sha(raw(s['commit'],s['repositoryPath']))==s['sha256'])
 except Exception:ck('Exact Director source blob '+s['repositoryPath'],False)
nb=c['nativeBinding'];nativeRaw=raw(nb['commit'],nb['repositoryPath']);native=json.loads(nativeRaw);card=native['spells'][679];u=c['nativeCardUnmodified']
ck('Native card exact binding and pointer',sha(nativeRaw)==nb['sha256'] and nb['pointer']=='/spells/679')
ck('Native Imprisonment remains blocked and byte-equivalent in governed fields',card['id']==u['id'] and card['name']==u['name'] and card['schools']==u['schools'] and card['status']==u['status']=='blocked-pending-operational-review' and card['operational'] is None and card['classAccess']==u['classAccess'] and card['additionalRpCost']==u['additionalRpCost'])
for sb in c['sourceBindings']:
 try:ck('Prior Director source hash '+sb['repositoryPath'],sha(raw(sb['commit'],sb['repositoryPath']))==sb['sha256'])
 except Exception:ck('Prior Director source hash '+sb['repositoryPath'],False)
hold=json.loads(raw(c['sourceBindings'][0]['commit'],c['sourceBindings'][0]['repositoryPath']));qual=json.loads(raw(c['retainedQualificationFiles'][0]['commit'],c['retainedQualificationFiles'][0]['repositoryPath']))
ck('PC232-B02 remains OPEN',hold['status']=='OPEN' and hold['blockerId']=='PC232-B02' and c['blockerRetainedOutsideStaticScope']=='PC232-B02')
ck('All seven native qualification records remain retained',[x['id'] for x in qual['records']]==[f'PC232-Q{i:02d}' for i in range(1,8)])
# Reversible journal replay over every entire state snapshot.
for b in w['branches']:
 state=b['startState'];ck('Start snapshot hash '+b['branchId'],h(state)==b['startHash']);last=-1;ordinals={}
 for e in b['events']:
  ck('Event order/provenance '+e['id'],isinstance(e['timeMs'],int) and e['timeMs']>=last and e['sameTimeOrdinal']==ordinals.get(e['timeMs'],0)+1 and e['actorId'] and e['castId'] and e['sourceId'] and e['receiptKey']);last=e['timeMs'];ordinals[e['timeMs']]=e['sameTimeOrdinal']
  op=e['forward'][0];ck('Forward replay '+e['id'],state==e['before'] and h(state)==e['beforeHash'] and op['op']=='test-and-replace-root' and op['before']==state);state=op['after'];ck('Forward result '+e['id'],state==e['after'] and h(state)==e['afterHash'])
 ck('Terminal replay '+b['branchId'],state==b['terminalState'] and h(state)==b['terminalHash'])
 for e in reversed(b['events']):
  op=e['inverse'][0];ck('Inverse replay '+e['id'],state==op['before'] and h(state)==e['afterHash']);state=op['after'];ck('Inverse result '+e['id'],state==e['before'] and h(state)==e['beforeHash'])
 ck('Inverse restores exact branch start '+b['branchId'],state==b['startState'] and h(state)==b['startHash'])
# Common cell geometry, physical support, nonoverlapping panels, and no forced environmental slab.
inner=c['model']['fixture']['innerBounds']; panels=c['model']['fixture']['panels']
def overlap(a,b):return all(min(x[1],y[1])>max(x[0],y[0]) for x,y in zip(a,b))
def volume(box):return (box[0][1]-box[0][0])*(box[1][1]-box[1][0])*(box[2][1]-box[2][0])
ck('Five authored AABBs are pairwise nonoverlapping and enclose stated usable space',set(panels)=={'west','east','south','north','ceiling'} and all(not overlap(panels[x],panels[y]) for i,x in enumerate(panels) for y in list(panels)[i+1:]) and all(volume(panels[x])>0 for x in panels))
ck('Target starts fully within usable prison bounds',all(b['startState']['target']['body']['bounds'][i][0]>=inner[i][0] and b['startState']['target']['body']['bounds'][i][1]<=inner[i][1] for i in range(3)))
ck('Existing supported floor, no inserted slab, no needs/stasis or anti-plane privilege',all((b['startState']['site']['floor']['continuous'] and b['startState']['site']['floor']['supportsTarget'] and not b['startState']['site']['floor']['insertedSlab']) for b in w['branches']) and c['model']['commonCell']['needs'].find('no oxygen, food, water, sleep or aging suspension')>=0 and c['model']['commonCell']['boundary'].find('no new anti-teleport')>=0)
# Positive route witnesses, actual commitment/action/RP/save/geometry.
for route,bid in [('Wizard/Necromancy','IM-P1-WIZARD'),('Cleric/Necromancy','IM-P1-CLERIC'),('Druid/Necromancy','IM-P2-DRUID'),('Mage/Universal','IM-P2-MAGE')]:
 b=bs[bid];t=b['terminalState'];ce=next(e for e in b['events'] if e['kind']=='CAST_COMMITMENT');re=next(e for e in b['events'] if e['kind']=='INITIAL_TARGET_SAVE_AND_RESOLUTION');a=ce['after']['caster'];
 ck('One paid rank9 Action and 26 RP '+route,a['classLevel']==17 and a['spellRank']==9 and a['resources']['RP']==profiles[route]['maxRP']-26 and a['pendingCast']['rpPaid']==26 and not a['turn']['actionAvailable'] and a['turn']['actionsSpent']==1 and a['turn']['magicThisTurn'])
 ck('Valid V/S/F target admission, range, LoE and complete target bounds '+route,ce['details']['components']==['V','S','F'] and ce['details']['targetPerceivedWithin120FtLoE'] and ce['after']['target']['body']['bounds']==b['startState']['target']['body']['bounds'] and re['after']['saveReceipt']['roll']['DC']==profiles[route]['spellSaveDC'] and re['after']['saveReceipt']['cellFormed'] and re['after']['caster']['spellHistory'][0]['status']=='resolved-cell-formed-test-only')
 cell=re['after']['cell'];ck('Finite independent prison expression and source-owned panels '+route,cell['active'] and cell['deadlineMs']==86401000 and cell['concentration'] is False and cell['formedOnExistingFloor'] and cell['needsSuspended'] is False and cell['agingSuspended'] is False and cell['antiTeleportPrivilege'] is False and cell['antiPlanarPrivilege'] is False and not cell['conjuredMatterLootable'] and set(cell['panels'])==set(panels) and all(x['ownerKind']=='source-owned nonlootable prison matter' for x in cell['panels'].values()))
# P1: three actual panel attacks destroy only the north panel; actual movement fits its 7ft opening.
for bid in ['IM-P1-WIZARD','IM-P1-CLERIC']:
 b=bs[bid];t=b['terminalState'];att=[e for e in b['events'] if e['kind']=='TARGET_ATTACKS_STONE_PANEL'];m=next(e for e in b['events'] if e['kind']=='TARGET_MOVEMENT');north=t['cell']['panels']['north']
 ck('P1 three reachable lawful attack Actions, HP 60→40→20→0 '+bid,len(att)==3 and [e['after']['cell']['panels']['north']['currentHP'] for e in att]==[40,20,0] and all(e['actorId']=='target-01' and e['details']['actualAttackAction'] and e['details']['rangeAndLoEValid'] and e['after']['panelAttackReceipt']['roll']['hit'] and e['after']['panelAttackReceipt']['roll']['total']>=18 and e['after']['panelAttackReceipt']['roll']['damage']==20 for e in att) and t['target']['turn']['actionsSpent']==3)
 ck('P1 only north panel destroyed and opening stays open '+bid,north['destroyed'] and not north['active'] and north['currentHP']==0 and north['lootable'] is False and all(p['active'] for n,p in t['cell']['panels'].items() if n!='north') and t['cell']['active'])
 ck('P1 target exits by actual movement through 7ft opening '+bid,m['actorId']=='target-01' and m['details']['actualMovementBudgetSpent']==6 and m['after']['target']['movementReceipt']['distanceFt']==6 and m['after']['target']['body']['location']['y']==6 and m['after']['target']['body']['bounds'][0]==[17.5,22.5] and m['after']['target']['body']['bounds'][1]==[3.5,8.5] and m['after']['target']['inCell'] is False and m['after']['target']['turn']['movementFtAvailable']==24)
# P2: one failed initial save, then exactly 3 cumulative successes across four paid Actions.
for bid in ['IM-P2-DRUID','IM-P2-MAGE']:
 b=bs[bid];save=next(e for e in b['events'] if e['kind']=='INITIAL_TARGET_SAVE_AND_RESOLUTION');attempts=[e for e in b['events'] if e['kind']=='SIGIL_CELL_ESCAPE_SAVE_ATTEMPT'];t=b['terminalState'];
 ck('P2 four actual escape Actions, success/fail/success/success '+bid,len(attempts)==4 and [e['after']['escapeAttempt']['roll']['success'] for e in attempts]==[True,False,True,True] and [e['after']['escapeAttempt']['successes'] for e in attempts]==[1,1,2,3] and all(e['actorId']=='target-01' and e['after']['escapeAttempt']['actualActionSpent'] for e in attempts) and save['after']['cell']['saveStat']=='WIS' and save['after']['saveReceipt']['roll']['success'] is False)
 ck('P2 cumulative third success ends one source exactly once '+bid,not t['cell']['active'] and t['cell']['escapeProgress']=={'successes':3,'attempts':4} and t['sourceReceipts'][t['cell']['id']]['releaseCount']==1 and t['cell']['endReason']=='three cumulative WIS successes')
# A1 boundary cases.
b=bs['IM-A1-SUCCESSFUL-SAVE'];r=next(e for e in b['events'] if e['kind']=='INITIAL_TARGET_SAVE_AND_RESOLUTION');ck('A1 target success leaves no cell, with paid action and RP spent',r['after']['saveReceipt']['roll']['success'] and r['after']['cell'] is None and r['after']['caster']['resources']['RP']==b['startState']['caster']['resources']['RP']-26 and r['after']['caster']['spellHistory'][0]['status']=='resolved-no-cell-test-only')
b=bs['IM-A1-COLLISION-PAID-FAIL'];r=next(e for e in b['events'] if e['kind']=='INITIAL_TARGET_SAVE_AND_RESOLUTION');ck('A1 postcommit occupied formation fails paid, with no panel/cell or refund',r['after']['caster']['castFailure']['refundRp']==0 and r['after']['cell'] is None and r['after']['caster']['pendingCast'] is None and r['after']['caster']['spellHistory'][0]['status']=='failed-paid' and r['after']['geometryCollision']['positiveVolumeOverlap'])
b=bs['IM-A1-CASTER-DEATH'];t=b['terminalState'];ck('A1 caster death does not end or extend cell deadline',not t['caster']['health']['alive'] and t['cell']['active'] and t['cell']['continuesAfterOwnerDeath'] and t['cell']['deadlineMs']==86401000 and t['sourceReceipts'][t['cell']['id']]['deadlineMs']==86401000)
b=bs['IM-A1-TARGET-DEATH'];t=b['terminalState'];ck('A1 target corpse and carried gear stay inside; no soul/corpse fabrication',not t['target']['health']['alive'] and t['target']['corpse']['sameOriginalBody'] and t['target']['corpse']['gearRemains'] and t['targetCorpseInCell'] and not t['cell']['soulCreated'] and not t['cell']['corpseClaimedAsLoot'])
b=bs['IM-A1-GROWTH-COLLISION'];t=b['terminalState'];ck('A1 cell ends before legal body growth can collide',t['growthReceipt']['wouldOverlapBeforeEnd'] and t['growthReceipt']['cellEndedBeforeMutation'] and not t['growthReceipt']['crushed'] and not t['cell']['active'] and t['target']['body']['growthReceipt']['growthAfterPrisonEnd'])
b=bs['IM-A1-PHRASE-RELEASE'];t=b['terminalState'];ck('A1 helper communicates hidden key; target spends Action to release',t['site']['helper']['knowsPhrase'] and t['target']['knownReleasePhrase']==t['site']['declaredPhrase']=='open-test-cell-11' and t['phraseReleaseReceipt']['actualActionSpent'] and t['phraseReleaseReceipt']['releaseCount']==1 and not t['cell']['active'] and t['target']['turn']['actionsSpent']==1)
# A2 persistence/suppression/release/expiry/recast/race.
b=bs['IM-A2-PARTIAL-SUPPRESSION-EXIT'];t=b['terminalState'];ck('A2 only covered panel suppressed; target exits; deadline retains original value',t['cell']['panels']['north']['suppressed'] is False and t['cell']['panels']['north']['active'] and t['cell']['suppressedPanelIds']==['north'] and t['cell']['deadlineMs']==86401000 and t['cell']['active'] and not t['target']['inCell'] and not t['cell']['suppressionProviderInput']['providerCastCertified'])
b=bs['IM-A2-OCCUPIED-RESUMPTION'];t=b['terminalState'];ck('A2 occupied panel resumption terminates before insertion and avoids crushing',t['cell']['resumptionOverlapCheck']['positiveVolumeOverlap'] and not t['cell']['active'] and t['cell']['noCrushReceipt']['panelNotInserted'] and t['cell']['noCrushReceipt']['targetKeptAtActualPosition'])
b=bs['IM-A2-ELIGIBLE-DISPEL'];t=b['terminalState'];ck('A2 TEST_ONLY eligible source dispel ends one cell once',not t['cell']['active'] and not t['eventInputs'][0]['providerCastCertified'] and t['sourceReceipts'][t['cell']['id']]['releaseCount']==1)
b=bs['IM-A2-DUPLICATE-RELEASE'];t=b['terminalState'];ck('A2 duplicate release is idempotent',t['duplicateReleaseResult']['existingReceiptReturned'] and not t['duplicateReleaseResult']['newActionSpent'] and t['duplicateReleaseResult']['newReleaseCount']==0 and t['sourceReceipts'][t['cell']['id']]['releaseCount']==1)
b=bs['IM-A2-24H-DEADLINE'];t=b['terminalState'];ck('A2 24-hour deadline is exactly elapsed, unpaused and unextended',t['deadlineReceipt']['deadlineMs']-t['deadlineReceipt']['createdAtMs']==86400000 and t['deadlineReceipt']['elapsedMs']==86400000 and not t['deadlineReceipt']['paused'] and not t['deadlineReceipt']['extended'] and not t['cell']['active'])
b=bs['IM-A2-SAME-DIFFERENT-OWNER-RECAST'];t=b['terminalState'];ck('A2 same/different-owner recast rejected before commitment/cost',len(t['recastAttempts'])==2 and all(x['status']=='rejected-before-commitment' and x['rpDelta']==0 and x['actionDelta']==0 for x in t['recastAttempts']) and t['cell']['active'] and len(t['sourceReceipts'])==1)
b=bs['IM-A2-RESOLUTION-RACE'];t=b['terminalState'];o=t['otherCasters'][0];ck('A2 resolution race revalidates second paid cast without second cell',t['cell']['active'] and o['spellHistory'][-1]['status']=='failed-paid-race' and o['castFailure']['refundRp']==0 and not o['castFailure']['partialCellCreated'] and len(t['sourceReceipts'])==1 and o['resources']['RP']==22)
ck('All events remain static TEST_ONLY authored evidence; no runtime/canon/campaign/provider claims',w['scope']=='STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY' and all(b['status']=='TEST_ONLY' and b['startState']['canonical'] is False for b in w['branches']) and all(e['details'].get('providerCastCertified') is not True for b in w['branches'] for e in b['events']) and 'No runtime' in w['limitations'] and 'campaign' in w['limitations'] and 'source-blocker closure' in w['limitations'])
case=read('CASE_EVIDENCE_BINDINGS.json');ck('Case crosswalk binds all four Director cases and branch hashes',{x['caseId'] for x in case['requiredCases']}=={'IM-P1','IM-P2','IM-A1','IM-A2'} and all(x['status']=='PASS_STATIC_TEST_ONLY' and all(caseBranch in bs for caseBranch in x['branchIds']) and all(x['branchHashes'][bid]==h(bs[bid]) for bid in x['branchIds']) for x in case['requiredCases']))
result={'id':'IM-DD11-SEMANTIC-VALIDATION-01','identity':ID,'status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','scope':'STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY','checks':checks,'checksPassed':sum(x['pass'] for x in checks),'checksFailed':sum(not x['pass'] for x in checks),'branchCount':len(bs),'eventCount':sum(len(b['events']) for b in w['branches']),'runtimeExecuted':False,'unityExecuted':False,'sourceBlockerClosed':False}
(STAGE/ROOT/'SEMANTIC_VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
tool=STAGE/ROOT/'tools'/'verify_imprisonment_dd11.py';tool.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(Path(__file__),tool);tb=tool.read_bytes();bind={'path':ROOT+'tools/verify_imprisonment_dd11.py','bytes':len(tb),'sha256':sha(tb)}
replay={'id':'IM-DD11-REPLAY-VALIDATION-01','identity':ID,'status':result['status'],'scope':'STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY','branchCount':len(bs),'eventCount':result['eventCount'],'forwardOperationCount':result['eventCount'],'inverseOperationCount':result['eventCount'],'combinedOperationCount':2*result['eventCount'],'checksPassed':result['checksPassed'],'checksFailed':result['checksFailed'],'verificationScriptBinding':bind,'stateCanonicalization':'NFC-normalized, key-sorted compact UTF-8 JSON.','execution':'All serialized forward and inverse root patches independently replayed and checked.','runtimeExecuted':False,'unityExecuted':False}
(STAGE/ROOT/'REPLAY_VALIDATION.json').write_text(json.dumps(replay,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':result['status'],'checksPassed':result['checksPassed'],'checksFailed':result['checksFailed'],'failures':[x for x in checks if not x['pass']]},indent=2))

