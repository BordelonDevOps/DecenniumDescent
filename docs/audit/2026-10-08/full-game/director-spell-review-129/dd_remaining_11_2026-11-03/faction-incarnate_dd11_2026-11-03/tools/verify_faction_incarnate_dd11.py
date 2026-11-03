from pathlib import Path
import json,hashlib,unicodedata,subprocess,shutil
REPO=Path(r'C:\ep480fix');PKG=Path(r'C:\Users\cbord\AppData\Local\Temp\DD_Remaining_11_20261103');STAGE=Path(r'C:\Users\cbord\AppData\Local\Temp\DD11_STAGE_20261103');BASE='8c8aff462c1cf00ae230a0a4244fa67447bb8808';ROOT='docs/audit/2026-10-08/full-game/director-spell-review-129/dd_remaining_11_2026-11-03/faction-incarnate_dd11_2026-11-03/'
def nfc(x):
 if isinstance(x,str):return unicodedata.normalize('NFC',x)
 if isinstance(x,list):return [nfc(y) for y in x]
 if isinstance(x,dict):return {nfc(k):nfc(v) for k,v in x.items()}
 return x
def canon(x):return json.dumps(nfc(x),ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def h(x):return hashlib.sha256(canon(x)).hexdigest()
def raw(c,p):return subprocess.check_output(['git','-C',str(REPO),'show',f'{c}:{p}'])
def read(p):return json.loads((STAGE/(ROOT+p)).read_text(encoding='utf-8'))
c=read('DIRECTOR_CONTRACT.json');src=read('SOURCE_BINDINGS.json');w=read('WITNESS_PACKET.json');profiles=read('ACTOR_PROFILES.json');branches={b['branchId']:b for b in w['branches']};checks=[]
def ck(name,value,detail=None):checks.append({'check':name,'pass':bool(value),'detail':detail})
contract_bytes=(PKG/'contracts/faction-incarnate.json').read_bytes();common_bytes=(PKG/'DIRECTOR_COMMON_CONTRACT_01.json').read_bytes();director=json.loads((PKG/'DIRECTOR_RETURN_ALL_11.json').read_text(encoding='utf-8'))
ck('exact contract bytes and hash',hashlib.sha256(contract_bytes).hexdigest()=='497e42fee8ea5dcbd3609ffe1807f33ea67feaa302e3d3a56c89d5edcef2fbe8' and src['directorContractSha256']==hashlib.sha256(contract_bytes).hexdigest())
ck('common contract exact hash',src['commonContractSha256']==hashlib.sha256(common_bytes).hexdigest())
ck('Director execution order places Faction Incarnate fifth',director['executionOrder'][4]['spellId']=='faction-incarnate' and c['priority']==5)
expected={'Wizard/Conjuration','Druid/Conjuration','Mage/Conjuration'}
ck('all three legal native rank-9 routes',set(profiles['nativeRouteProfiles'])==expected)
for route,p in profiles['nativeRouteProfiles'].items():
 ck('level-17 rank-9 route '+route,p['singleClassLevel']==17 and p['totalCharacterLevel']==17 and p['classRankMaximum']==9 and p['maxRP']>=26 and p['targetSpell']['targetSpell']=='faction-incarnate' and p['targetSpell']['paidRpCost']==26)
ck('provider is separately selected as Cleric Saint level 17',profiles['healingProviderProfile']['singleClassLevel']==17 and profiles['healingProviderProfile']['classBuild'][9].count('Mass Healing Light')==1 and profiles['healingProviderProfile']['selectedProviderCard']=='Mass Healing Light')
source_path='DescentReviewChanges/ReviewBible/data/public/class_playtests/cleric.json';cleric=json.loads(raw(BASE,source_path));ml=cleric['cards'][33]
ck('actual Mass Healing Light source id and path',ml['id']=='cleric.hero.saint.mass-healing-light' and ml['name']=='Mass Healing Light' and src['massHealingLightSource']['pointers']==['/cards/33'])
ck('provider source permits action, cost, living allies and range',ml['activation']=='Action' and ml['cost']=='5 RP' and 'living allies within 30 feet' in ml['rangeAndTarget'] and ml['duration']=='Instantaneous')
rules=raw(BASE,'DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_RULES.md').decode('utf-8');guide=raw(BASE,'DescentReviewChanges/ReviewBible/docs/mechanics/classes/cleric.md').decode('utf-8')
ck('Cleric S and M levels are source-bound', '**S** is 1/2/3/4 at class levels 1/5/11/17' in rules and 'S = 1/2/3/4 at Cleric levels 1/5/11/17' in guide and 'M = max(1, Wisdom modifier)' in guide)
ck('required FI cases represented',set(x['id'] for x in c['requiredCases'])=={'FI-P1','FI-P2','FI-A1','FI-A2'} and {b['caseId'] for b in w['branches']}=={'FI-P1','FI-P2','FI-A1','FI-A2'})
ck('all eight isolated branches are TEST_ONLY and noncanonical',len(w['branches'])==8 and all(b['status']=='TEST_ONLY' and b['startState']['status']=='TEST_ONLY' and b['startState']['canonical'] is False for b in w['branches']))
# Every serialized event is independently replayed forward and backward from its full recorded patch.
for b in w['branches']:
 state=b['startState'];ck('start state hash '+b['branchId'],h(state)==b['startHash'])
 last_t=-1;ordinal_by_t={}
 for e in b['events']:
  ck('event metadata '+e['id'],isinstance(e['timeMs'],int) and e['timeMs']>=last_t and e['sameTimeOrdinal']==ordinal_by_t.get(e['timeMs'],0)+1 and e['actorId']==b['startState']['actors']['owner']['id'] and e['castId'] and e['sourceId'] and 'causalParentEventId' in e and e['receiptKey'])
  last_t=e['timeMs'];ordinal_by_t[e['timeMs']]=e['sameTimeOrdinal']
  ck('forward precondition '+e['id'],state==e['before'] and h(state)==e['beforeHash'] and len(e['forward'])==1 and e['forward'][0]['op']=='test-and-replace-root' and e['forward'][0]['before']==state)
  state=e['forward'][0]['after'];ck('forward after hash '+e['id'],state==e['after'] and h(state)==e['afterHash'])
 ck('forward terminal '+b['branchId'],state==b['terminalState'] and h(state)==b['terminalHash'])
 for e in reversed(b['events']):
  op=e['inverse'][0];ck('inverse precondition '+e['id'],state==op['before'] and h(state)==e['afterHash']);state=op['after'];ck('inverse restores event start '+e['id'],state==e['before'] and h(state)==e['beforeHash'])
 ck('inverse restores branch start '+b['branchId'],state==b['startState'] and h(state)==b['startHash'])
# Every route has an actual paid, successful positive witness.
for route,bid in [('Wizard/Conjuration','FI-P1-WIZARD'),('Druid/Conjuration','FI-P2-DRUID'),('Mage/Conjuration','FI-A1-MAGE')]:
 b=branches[bid];s=b['terminalState'];a=s['actors']['owner'];history=a['spellHistory'];commit_event=next(e for e in b['events'] if e['kind']=='CAST_COMMITMENT');cast_state=commit_event['after']['actors']['owner'];ck('paid positive route '+route,len(history)==1 and history[0]['status']=='resolved' and history[0]['rpPaid']==26 and a['resources']['RP']==profiles['nativeRouteProfiles'][route]['maxRP']-26 and cast_state['actionBudget']['actionsSpent']==1 and cast_state['actionBudget']['actionAvailable'] is False and cast_state['turnState']['lastSpell']=='faction-incarnate')
# P1: committed owner command, attached strike, shared offense ledger and no second turn.
p1=branches['FI-P1-WIZARD']['terminalState'];p1events={e['kind']:e for e in branches['FI-P1-WIZARD']['events']};attack=p1['manifestation']['body']['lastAttack'];a=p1['actors']['owner']
ck('FI-P1 command spends owner Bonus Action and executes after full turn',not p1events['OWNER_BONUS_ACTION_COMMAND']['after']['actors']['owner']['actionBudget']['bonusActionAvailable'] and p1events['ATTACHED_COMMAND_EXECUTION']['details']['actualAttachedPhase'] and p1['commandReceipt']['phase']=='attached-after-owner-turn')
ck('FI-P1 attack uses caster spell attack and exact hit/damage',attack['d20']==3 and attack['attackBonus']==profiles['nativeRouteProfiles']['Wizard/Conjuration']['spellAttackBonus'] and attack['total']>=attack['targetAC'] and attack['damageDice']==[5,5,5] and attack['rawDamage']==15 and attack['damageType']=='force' and p1['actors']['target']['resources']['HP']==85)
ck('FI-P1 offense and command counters are spent exactly once',a['companionCommandRoundUsed'] and a['companionOffenseRoundUsed'] and p1['manifestation']['body']['offenseRoundUsed'] and p1['commandReceipt']['status']=='executed')
ck('FI-P1 second offense attempt denied and no extra turn',p1['secondOffenseAttempt']['allowed'] is False and p1['secondOffenseAttempt']['extraTurnGranted'] is False and p1['manifestation']['body']['lastAttack']['rawDamage']==15 and p1['actors']['owner']['turnState']['regularTurn']==1)
ck('FI-P1 legal spawn and stable synthetic faction admission recorded',p1events['CAST_COMMITMENT']['before']['spawnAdmission']['empty'] and p1events['CAST_COMMITMENT']['before']['factions']['TEST-DD11-WARDENS']['version']==1 and p1events['CAST_COMMITMENT']['before']['actors']['owner']['factionStanding']['TEST-DD11-WARDENS']>=1 and p1events['CAST_COMMITMENT']['before']['actors']['owner']['invocationPermission']['active'])
# P2: physical pickup, supported movement, actual borrowed cargo and clean expiry.
p2=branches['FI-P2-DRUID']['terminalState'];p2b=branches['FI-P2-DRUID'];p2e={e['kind']:e for e in p2b['events']};attached_events=[e for e in p2b['events'] if e['kind']=='ATTACHED_COMMAND_EXECUTION'];item=next(x for x in p2['items'] if x['id']=='real-crate')
ck('FI-P2 pickup is commanded, in reach and not automatic',attached_events[0]['details']['action']=='pickup' and attached_events[0]['before']['items'][0]['custodian']=='TEST-ORIGINAL-CRATE-OWNER' and attached_events[0]['after']['items'][0]['custodian']==attached_events[0]['after']['manifestation']['body']['id'])
ck('FI-P2 cargo fit and real owner preserved',item['massLb']==40 and item['load']==2 and item['massLb']<=200 and item['load']<=10 and item['owner']=='TEST-ORIGINAL-CRATE-OWNER' and item['intrinsic'] is False and item['exists'] is True)
ck('FI-P2 20ft carry remains supported within courier speed',p2['routeMovement']=={'distanceFt':20,'clear':True,'supportedEveryStep':True,'speedFt':60} and p2['bodyHistory'][0]['status']=='created')
ck('FI-P2 expires at exactly successful resolution plus 60 seconds',p2e['CAST_RESOLUTION']['timeMs']==1000 and p2e['NATURAL_EXPIRY_AND_CARGO_SETTLEMENT']['timeMs']==61000 and p2e['CAST_RESOLUTION']['after']['manifestation']['deadlineMs']==61000 and p2['manifestation'] is None)
ck('FI-P2 borrowed crate persists on supported ground once',item['custodian']=='ground' and item['location']['x']==25 and item['supportedBy']=='TEST-DD11-FLOOR' and len(p2['cargoSettlements'])==1 and p2['cargoSettlements'][0]['count']==1 and p2['loot']==[] if 'loot' in p2 else item['custodian']=='ground' and len(p2['cargoSettlements'])==1)
# A1 guard/default/standing/revocation chain.
a1b=branches['FI-A1-MAGE'];a1=a1b['terminalState'];a1e={e['kind']:e for e in a1b['events']}
ck('FI-A1 guard grants typed +2 AC without offense',a1e['ATTACHED_COMMAND_EXECUTION']['after']['actors']['target']['AC']==17 and a1e['ATTACHED_COMMAND_EXECUTION']['after']['actors']['owner']['companionOffenseRoundUsed'] is False and a1e['ATTACHED_COMMAND_EXECUTION']['after']['guardEffect']['ACDelta']==2)
ck('FI-A1 next owner start expires guard; default action is Dodge',a1e['OWNER_START_AND_NO_COMMAND_PHASE']['after']['actors']['target']['AC']==15 and a1e['OWNER_START_AND_NO_COMMAND_PHASE']['after']['guardEffect']['active'] is False and a1e['OWNER_START_AND_NO_COMMAND_PHASE']['after']['manifestation']['body']['defaultAction']=='Dodge' and a1e['OWNER_START_AND_NO_COMMAND_PHASE']['after']['manifestation']['body']['defaultMovementFt']==0)
ck('FI-A1 standing loss denies new strike while body remains',a1e['STANDING_FALLS_BELOW_ONE']['after']['actors']['owner']['factionStanding']['TEST-DD11-WARDENS']==0 and a1e['STANDING_FALLS_BELOW_ONE']['after']['manifestation'] is not None and a1e['NEW_COMMAND_DENIED']['after']['deniedCommand']['allowed'] is False and a1e['NEW_COMMAND_DENIED']['after']['actors']['owner']['companionOffenseRoundUsed'] is False)
ck('FI-A1 permission revocation ends body immediately without refund',a1['manifestation'] is None and a1['actors']['owner']['resources']['RP']==profiles['nativeRouteProfiles']['Mage/Conjuration']['maxRP']-26 and a1['bodyHistory'][-1]['status']=='ended' and a1['bodyHistory'][-1]['atMs']==15000 and a1['factions']['TEST-DD11-WARDENS']['invocationPermission'] is False)
# A2 real healing provider, terminal cases, suppression, and replacement.
healb=branches['FI-A2-HEALING'];heal=healb['terminalState'];heale={e['kind']:e for e in healb['events']};body=heal['manifestation']['body'];provider=heal['actors']['healer'];hist=provider['cardHistory'][0]
ck('FI-A2 healing is a paid source-authorized action on eligible living ally',hist['sourceId']==ml['id'] and hist['costRP']==5 and hist['activation']=='Action' and hist['targetLiving'] and hist['targetAllyOfProvider'] and hist['targetDistanceFt']<=30 and provider['resources']['RP']==43 and provider['actionBudget']['actionsSpent']==1)
ck('FI-A2 healing formula derives S4 M5 and clamps 70+37 to100',hist['S']==4 and hist['M']==5 and hist['rawHealing']==37 and body['resourceLedger']['HP']==100 and body['healingReceipt']['overflow']==7 and body['resourceLedger']['wounds']==0)
ck('FI-A2 same-key duplicate healing callback has no second effect',heale['DUPLICATE_HEALING_CALLBACK_IGNORED']['after']['manifestation']['body']['resourceLedger']['HP']==100 and heale['DUPLICATE_HEALING_CALLBACK_IGNORED']['after']['duplicateCallback']['ignored'])
zero=branches['FI-A2-ZERO']['terminalState'];zerob=branches['FI-A2-ZERO'];zeroe={e['kind']:e for e in zerob['events']}
ck('FI-A2 ordinary zero HP terminates without corpse loot or death proc',zero['manifestation'] is None and zero.get('corpse') is None and zero.get('loot')==[] and zero.get('deathResourceProc') is False and zero['bodyHistory'][-1]['status']=='ended-zero-hp')
ck('FI-A2 duplicate zero-HP callback cannot revive source',zeroe['DUPLICATE_ZERO_HP_CALLBACK_IGNORED']['after']['manifestation'] is None and zeroe['DUPLICATE_ZERO_HP_CALLBACK_IGNORED']['after']['duplicateCallback']['sourceRemainsEnded'])
null=branches['FI-A2-NULL']['terminalState'];nulle={e['kind']:e for e in branches['FI-A2-NULL']['events']}
ck('FI-A2 qualifying Null input is explicitly hypothetical with no provider cast',null['nullInput']['qualified'] and null['nullInput']['providerCastCertified'] is False and null['nullInput']['status']=='TEST_ONLY_SOURCE_AUTHORIZED_TERMINAL_INPUT' and null['manifestation'] is None)
ck('FI-A2 duplicate Null callback is idempotent',nulle['DUPLICATE_NULL_CALLBACK_IGNORED']['after']['manifestation'] is None and nulle['DUPLICATE_NULL_CALLBACK_IGNORED']['after']['duplicateCallback']['ignored'])
sup=branches['FI-A2-SUPPRESSION']['terminalState'];supe={e['kind']:e for e in branches['FI-A2-SUPPRESSION']['events']}
ck('FI-A2 suppression is synthetic, source-locus scoped and clock continues',sup['suppressionInput']['status']=='synthetic_TEST_ONLY_interface' and sup['suppressionInput']['providerCastCertified'] is False and supe['SUPPRESSION_START']['timeMs']==20000 and sup['suppressionInput']['deadlineMs']==61000 and supe['DEADLINE_WHILE_SUPPRESSED']['timeMs']==61000)
ck('FI-A2 deadline ends suppressed source and resume does not restore it',sup['manifestation'] is None and sup['resumeAttempt']['restored'] is False and supe['DUPLICATE_DEADLINE_CALLBACK_IGNORED']['after']['manifestation'] is None)
recast=branches['FI-A2-RECAST-CARGO']['terminalState'];recastb=branches['FI-A2-RECAST-CARGO'];rece={e['kind']:e for e in recastb['events']};rh=recast['actors']['owner']['spellHistory'];ritem=recast['items'][0]
ck('FI-A2 recast performs two actual paid casts and one Refrain',len(rh)==2 and [x['rpPaid'] for x in rh]==[26,26] and rh[1]['refrain']==1 and recast['actors']['owner']['resources']['RP']==64-52 and recast['actors']['owner']['resources']['Dissonance']==1)
ck('FI-A2 recast replaces source, settles cargo once and does not reset command round',recast['manifestation']['sourceId']==rh[1]['castId'] and recast['bodyHistory'][-1]['status']=='created' and len(recast['cargoSettlements'])==1 and ritem['custodian']=='ground' and recast['actors']['owner']['companionCommandRoundUsed'] is True and recast['actors']['owner']['ownerRoundId']==2)
ck('FI-A2 duplicate recast resolution makes no extra body or settlement',rece['DUPLICATE_RECAST_RESOLUTION_IGNORED']['after']['duplicateCallback']['createdBodyCount']==1 and rece['DUPLICATE_RECAST_RESOLUTION_IGNORED']['after']['duplicateCallback']['cargoSettlements']==1)
ck('FI-A2 real cargo retains original owner and exists after recast',ritem['owner']=='TEST-ORIGINAL-CRATE-OWNER' and ritem['exists'] is True and ritem['intrinsic'] is False)
# Exact scope and limitations.
ck('native spell card and catalog remain blocked/unchanged',c['nativeCardUnmodified']['status']=='blocked-pending-operational-review' and c['nativeCardUnmodified']['operational'] is None and hashlib.sha256(raw(BASE,c['nativeBinding']['repositoryPath'])).hexdigest()==c['nativeBinding']['sha256'])
ck('native blocker and qualifications remain open',c['blockerRetainedOutsideStaticScope']=='AFP211-B03' and src['retainedQualifications']==c['retainedQualificationFiles'])
ck('no witness or campaign/runtime/canon side effect',all(b['startState']['canonical'] is False and b['startState']['status']=='TEST_ONLY' for b in w['branches']) and w['scope']=='STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY')
ck('external Null and suppression provider claims are withheld',w['fixtureLimits'].find('do not certify an external provider cast')>=0 and null['nullInput']['providerCastCertified'] is False and sup['suppressionInput']['providerCastCertified'] is False)
result={'id':'FI-DD11-SEMANTIC-VALIDATION-01','identity':'faction-incarnate','status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','scope':'STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY','checks':checks,'checksPassed':sum(x['pass'] for x in checks),'checksFailed':sum(not x['pass'] for x in checks),'branchCount':len(branches),'eventCount':sum(len(b['events']) for b in w['branches']),'runtimeExecuted':False,'unityExecuted':False,'sourceBlockerClosed':False}
(STAGE/ROOT/'SEMANTIC_VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
tool=STAGE/ROOT/'tools'/'verify_faction_incarnate_dd11.py';tool.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(Path(__file__),tool);tb=tool.read_bytes();toolbind={'path':ROOT+'tools/verify_faction_incarnate_dd11.py','bytes':len(tb),'sha256':hashlib.sha256(tb).hexdigest()}
replay={'id':'FI-DD11-REPLAY-VALIDATION-01','identity':'faction-incarnate','status':result['status'],'scope':'STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY','branchCount':len(branches),'eventCount':result['eventCount'],'forwardOperationCount':result['eventCount'],'inverseOperationCount':result['eventCount'],'combinedOperationCount':2*result['eventCount'],'checksPassed':result['checksPassed'],'checksFailed':result['checksFailed'],'verificationScriptBinding':toolbind,'stateCanonicalization':'NFC-normalized, key-sorted compact UTF-8 JSON; serializer is included in verification tool.','execution':'Forward and inverse root-patch operations and serialized event hashes independently verified.','runtimeExecuted':False,'unityExecuted':False}
(STAGE/ROOT/'REPLAY_VALIDATION.json').write_text(json.dumps(replay,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':result['status'],'checksPassed':result['checksPassed'],'checksFailed':result['checksFailed'],'failures':[x for x in checks if not x['pass']]},indent=2))