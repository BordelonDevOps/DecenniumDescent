from pathlib import Path
import json,hashlib,unicodedata,subprocess,shutil
STAGE=Path(r'C:\Users\cbord\AppData\Local\Temp\DD11_STAGE_20261103'); PKG=Path(r'C:\Users\cbord\AppData\Local\Temp\DD_Remaining_11_20261103'); REPO=Path(r'C:\ep480fix'); BASE='abb75c6a5fb7349a4167f7375e53bc826fe96a83'; ROOT='docs/audit/2026-10-08/full-game/director-spell-review-129/dd_remaining_11_2026-11-03/alignment-ascension_dd11_2026-11-03/'
def nfc(x):
 if isinstance(x,str):return unicodedata.normalize('NFC',x)
 if isinstance(x,list):return [nfc(y) for y in x]
 if isinstance(x,dict):return {nfc(k):nfc(v) for k,v in x.items()}
 return x
def canon(x):return json.dumps(nfc(x),ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def h(x):return hashlib.sha256(canon(x)).hexdigest()
def read(p):return json.loads((STAGE/(ROOT+p)).read_text(encoding='utf-8'))
contract=read('DIRECTOR_CONTRACT.json');w=read('WITNESS_PACKET.json');profiles=read('ACTOR_PROFILES.json')['profiles']; state=read('STATE_START.json'); checks=[]
def ck(label,condition,detail=None):checks.append({'check':label,'pass':bool(condition),'detail':detail})
branches={b['branchId']:b for b in w['branches']}
ck('exact Director contract SHA-256',hashlib.sha256((PKG/'contracts/alignment-ascension.json').read_bytes()).hexdigest()=='dd898abf30bb569d56774a776b203a9a3e30949b2b00cb115cfcbc3fe7165449')
ck('native class routes all represented',set(w['routeCoverage'])=={'Wizard/Conjuration','Cleric/Divination','Druid/Conjuration','Mage/Conjuration'})
ck('legal rank-9 level-17 profile for every route',all(p['singleClassLevel']==17 and p['classRankMaximum']==9 and p['targetSpell']['rank']==9 and p['maxRP']>=26 for p in profiles.values()))
wp=profiles['Wizard/Conjuration']; led=wp['hpLedger']; later=led['laterLevelRolls']; hp= max(1,led['firstLevelBase']-1)+sum(max(1,x-1) for x in later)
ck('Wizard HP ledger yields max 80 without an unbound HP bonus',hp==80 and len(later)==16 and all(1<=x<=6 for x in later),{'derived':hp,'rolls':later,'CONModifier':-1})
ck('Wizard attack bonus uses INT, PB and Conjuration mastery',wp['spellAttackBonus']==13 and wp['abilityScores']['INT']==20 and wp['proficiencyBonus']==6)
for b in w['branches']:
 ck('branch start hash '+b['branchId'],h(b['startState'])==b['startHash'])
 current=b['startState']
 for e in b['events']:
  ck('event before hash '+e['id'],h(current)==e['beforeHash'] and current==e['before'])
  ck('forward root patch precondition '+e['id'],len(e['forward'])==1 and e['forward'][0]['op']=='test-and-replace-root' and e['forward'][0]['before']==current and e['forward'][0]['after']==e['after'])
  current=e['forward'][0]['after']
  ck('event after hash '+e['id'],h(current)==e['afterHash'] and current==e['after'])
 ck('forward chain reaches terminal '+b['branchId'],current==b['terminalState'] and h(current)==b['terminalHash'])
 inverse_current=b['terminalState']
 for e in reversed(b['events']):
  inv=e['inverse'][0]
  ck('inverse root patch '+e['id'],len(e['inverse'])==1 and inv['before']==inverse_current and inv['after']==e['before'] and h(inv['after'])==e['beforeHash'])
  inverse_current=inv['after']
 ck('full inverse replay restores branch start '+b['branchId'],inverse_current==b['startState'] and h(inverse_current)==b['restoredStartHash'])
def findkind(bid,kind):return next((e for e in branches[bid]['events'] if e['kind']==kind),None)
# Positive paid casts are independently checked from the terminal ledger, including all four native routes.
for route,bid in [('Wizard/Conjuration','AA-P1-WIZARD'),('Cleric/Divination','AA-P2-CLERIC'),('Druid/Conjuration','AA-R-DRUID'),('Mage/Conjuration','AA-R-MAGE')]:
 b=branches[bid]; a=b['terminalState']['actors']['caster']; cast=a['spellHistory'][0]
 ck('paid positive cast and correct route '+route,cast['route']==route and cast['status'] in ('expired','resolved') and cast['rpPaid']==26 and a['resources']['RP']==profiles[route]['maxRP']-26)
 ck('Action, first-distinct strain, and refrain accounted '+route,a['actionBudget']['actionsSpent']>=1 and a['turnState']['magicThisTurn'] is True and cast['dissonanceAfter']==0 and cast['refrainAfter']==0 and cast['lastSpell']=='alignment-ascension')
# P1 concrete body form, attack, ordinary damage, expiry, no restoration.
p1=branches['AA-P1-WIZARD']; p1start=p1['startState']; p1end=p1['terminalState']; strike=findkind('AA-P1-WIZARD','ENERGY_STRIKE')['after']['actors']['caster']['form']['energyStrike']
ck('AA-P1 energy strike attack hits using legal attack bonus',strike['attackBonus']==13 and strike['d20']==7 and strike['total']==20 and strike['targetAC']==15 and strike['hit'])
ck('AA-P1 radiant 4d10 recorded roll totals 24',strike['damageType']=='radiant' and strike['damageDice']==[6,6,6,6] and strike['rawDamage']==24)
ck('AA-P1 Lawful AC modifier exists during form',findkind('AA-P1-WIZARD','ORDINARY_DAMAGE')['after']['actors']['caster']['form']['ACBonus']==2)
ck('AA-P1 HP damage and expiry retain 46/80',p1end['actors']['caster']['resources']['HP']==46 and p1end['actors']['caster']['resources']['maxHP']==80)
ck('AA-P1 same body and real gear survive expiry',p1start['actors']['caster']['body']==p1end['actors']['caster']['body'] and p1start['actors']['caster']['inventory']==p1end['actors']['caster']['inventory'])
ck('AA-P1 no healing or replacement life',p1end['actors']['caster']['resources']['HP']==46 and p1end['actors']['caster']['form'] is None and p1end['effects']['ascension'] is None)
# P2 private insight.
p2=branches['AA-P2-CLERIC']['terminalState']; insight=p2['insightRecord']
ck('AA-P2 returns the permitted current axes',insight['axes']=={'Order':'Chaotic','Moral':'Neutral'} and insight['asOfMs']==2000)
ck('AA-P2 answer is private to caster and creates no sigil',insight['audience']==[p2['actors']['caster']['actorId']] and insight['publicSigil'] is False and p2['publicEvents']==[])
ck('AA-P2 one actual later Action, no extra cast/RP',p2['actors']['caster']['actionBudget']['actionsSpent']==2 and p2['actors']['caster']['resources']['RP']==profiles['Cleric/Divination']['maxRP']-26 and len(p2['actors']['caster']['spellHistory'])==1)
# A1 resolver: axes update live; lock and protection don't rewrite history.
a1=branches['AA-A1-LIVE-RESOLVER']; a1end=a1['terminalState']; kinds=[e['kind'] for e in a1['events']]
ck('AA-A1 all four resolver steps present',kinds[-4:]==['A1_LEGITIMATE_ORDER_CHANGE','A1_ACTIVE_LAWFUL_LOCK','A1_MORAL_PROTECTION','A1_UNDEFINED_ORDER'])
ck('AA-A1 lawful Lock affects effective axis only',findkind('AA-A1-LIVE-RESOLVER','A1_ACTIVE_LAWFUL_LOCK')['after']['actors']['caster']['alignment']['underlying']['Order']=='Chaotic' and findkind('AA-A1-LIVE-RESOLVER','A1_ACTIVE_LAWFUL_LOCK')['after']['actors']['caster']['alignment']['effective']['Order']=='Lawful')
ck('AA-A1 protected moral axis withholds strike without diagnosis',findkind('AA-A1-LIVE-RESOLVER','A1_MORAL_PROTECTION')['after']['actors']['caster']['form']['energyStrikeType'] is None and 'protected' in findkind('AA-A1-LIVE-RESOLVER','A1_MORAL_PROTECTION')['after']['actors']['caster']['form']['strikeUnavailableReason'])
ck('AA-A1 undefined Order receives no Neutral bonus',a1end['actors']['caster']['form']['modifiers']=={} and a1end['actors']['caster']['alignment']['effective']['Order']=='undefined')
ck('AA-A1 underlying history preserved',len(a1end['actors']['caster']['alignment']['history'])==2 and a1end['actors']['caster']['alignment']['underlying']['Order'] is None)
# A2 deadline continues during suppression and terminal callback is idempotent.
a2=branches['AA-A2-CLOCK']; end=a2['terminalState']
ck('AA-A2 suppresses then resumes a live expression',findkind('AA-A2-CLOCK','SUPPRESSION_START')['after']['effects']['ascension']['active'] is False and findkind('AA-A2-CLOCK','SUPPRESSION_END')['after']['effects']['ascension']['active'] is True)
ck('AA-A2 suppression does not pause original 60s clock',findkind('AA-A2-CLOCK','SUPPRESSION_END')['after']['effects']['ascension']['deadlineMs']==61000 and findkind('AA-A2-CLOCK','SUPPRESSION_END')['timeMs']==50000)
ck('AA-A2 expiry ends source and prevents replay',end['effects']['ascension'] is None and end['actors']['caster']['form'] is None and end['duplicateCallback']['newSourceCreated'] is False and end['actors']['caster']['concentration'] is None)
# AA-R route effects and the committed interrupted branch preserve cost without a result.
for route,bid in [('Druid/Conjuration','AA-R-DRUID'),('Mage/Conjuration','AA-R-MAGE')]:
 hit=findkind(bid,'ENERGY_STRIKE')['after']['actors']['caster']['form']['energyStrike'];ck('AA-R useful positive route strike '+route,hit['hit'] and hit['rawDamage']>0 and hit['damageType']=='radiant' and hit['actionSpent'])
ib=branches['AA-R-DRUID-INTERRUPTED']['terminalState']; ia=ib['actors']['caster']
ck('AA-R interrupted cast paid then clears pending concentration',ia['resources']['RP']==profiles['Druid/Conjuration']['maxRP']-26 and ia['pendingCast'] is None and ia['concentration'] is None and ia['form'] is None)
ck('AA-R interrupted cast has no refund and no resolved benefit',ia['spellHistory'][0]['status']=='interrupted-after-commitment' and ia['spellHistory'][0]['refundRp']==0 and ib['effects']['ascension'] is None)
ck('all required contract cases have executed branches',all(any(b['caseId']==c['id'] for b in w['branches']) for c in contract['requiredCases']))
ck('native card operational field remains null',contract['nativeCardUnmodified']['operational'] is None)
ck('branch records stay TEST_ONLY and noncanonical',all(b['status']=='TEST_ONLY' and b['startState']['canonical'] is False for b in w['branches']))
result={'id':'AA-DD11-SEMANTIC-VALIDATION-01','identity':'alignment-ascension','status':'PASS' if all(c['pass'] for c in checks) else 'FAIL','scope':'STATIC_AUTHORED_PROCEDURE_REVIEW_ONLY','checks':checks,'checksPassed':sum(c['pass'] for c in checks),'checksFailed':sum(not c['pass'] for c in checks),'branchCount':len(branches),'eventCount':sum(len(b['events']) for b in w['branches']),'testOnly':True,'nativeSourceBlockerClosed':False,'runtimeExecuted':False,'unityExecuted':False}
(STAGE/ROOT/'SEMANTIC_VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
tool_dest=STAGE/ROOT/'tools'/'verify_alignment_ascension_dd11.py';tool_dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(Path(__file__),tool_dest);tool_bytes=tool_dest.read_bytes();tool_binding={'path':ROOT+'tools/verify_alignment_ascension_dd11.py','bytes':len(tool_bytes),'sha256':hashlib.sha256(tool_bytes).hexdigest()}
replay=read('REPLAY_VALIDATION.json');replay.update({'verificationScriptBinding':tool_binding,'status':result['status'],'checksPassed':result['checksPassed'],'checksFailed':result['checksFailed'],'semanticValidationSha256':hashlib.sha256((STAGE/ROOT/'SEMANTIC_VALIDATION.json').read_bytes()).hexdigest(),'checkedSnapshots':2*sum(len(b['events']) for b in w['branches'])+len(branches),'checkedEventTransitions':sum(len(b['events']) for b in w['branches']),'forwardOperationCount':sum(len(e['forward']) for b in w['branches'] for e in b['events']),'inverseOperationCount':sum(len(e['inverse']) for b in w['branches'] for e in b['events']),'combinedOperationCount':2*sum(len(e['forward']) for b in w['branches'] for e in b['events']),'verificationScript':'tools/verify_alignment_ascension_dd11.py','execution':'Independent verifier reconstructed every event from serialized preconditions and inverse patches; no game runtime was executed.'})
(STAGE/ROOT/'REPLAY_VALIDATION.json').write_text(json.dumps(replay,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':result['status'],'checksPassed':result['checksPassed'],'checksFailed':result['checksFailed'],'failures':[x for x in checks if not x['pass']]},indent=2))
