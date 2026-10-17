"""Preserve DE4 current03 and repair two fixtures as deterministic digital test vectors."""
from copy import deepcopy
from datetime import datetime,timezone
from pathlib import Path
import hashlib,json
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())
def at(obj,pointer):
 for part in pointer.strip('/').split('/') if pointer else []:
  key=part.replace('~1','/').replace('~0','~');obj=obj[int(key)] if isinstance(obj,list) else obj[key]
 return obj
oldpath=R/'data/director/spell_proposals/divination_enchantment_rank4_current_03.json'
newpath=R/'data/director/spell_proposals/divination_enchantment_rank4_current_04.json'
reportpath=A/'DE4_DIGITAL_FIXTURES_CHECK_04.json'
assert not newpath.exists() and not reportpath.exists()
old=read(oldpath);d=deepcopy(old);now=datetime.now(timezone.utc).isoformat();oldbinding=info(oldpath)
assert oldbinding['sha256']=='17c1a727dd7a8f959818875d9029e1873b31e9d1ca324a78688eb333f8cd8f3e'
for b in old['sourceBindings']:assert info(G/b['path'])==b,b['path']
d.update(id='DE4-CURRENT-PROCEDURES-04',recordedAtUtc=now,status='Unadopted authored video-game rules candidate; current04 corrects two test fixtures only.',previousDraft=oldbinding)
d['fixtureCorrections04']={'classification':'EXAMPLE ERROR','ruleChanges':0,'previousCases':[deepcopy(old['currentExamples'][23]),deepcopy(old['currentExamples'][24])],'findings':info(A/'accelerated-review-01/DE4_EXAMPLE_FINDINGS_04.json'),'previousWholeDraft':oldbinding,'purpose':'Exact source-qualified fixtures and deterministic expected states; no engine execution or numerical balance claim.'}
oldrel=oldpath.relative_to(G).as_posix();newrel=newpath.relative_to(G).as_posix()
for c in d['currentExamples']:
 for ref in c['sourceRefs']:
  if ref['path']==oldrel:ref['path']=newrel
c=d['currentExamples'][23]
c['initialState']+=' Field Repair has Recharge0 initially and is not used before t12.5; ordinary starts keep its zero counter at zero. The Tinker has a free hand and actual unobstructed physical contact with the adjacent Drone at the repair operation. Wizard has Abjuration specialization, so its Enchantment Compulsion gets no specialist DC bonus; no other DC modifier applies.'
c['actionsAndResolution'][2]='At t12.5 the Tinker actually touches that same adjacent disabled Drone, checks the selected Field Repair counter is0, and spends its available Action plus1RP,4→3. Set Field Repair Recharge2. Its explicit protected-vent repair interface clears the disability. HP remains14/14: any nominal repair roll is capped to0 actual HP restored. No expired Compulsion, spent vent use, old owner command, ammunition or duration is restored; this use cannot reset its own Recharge2.'
c['costLedger']['laterActualRepair'].update(rechargeBefore=0,rechargeAfter=2,touchRequired=True,touchConfirmed=True)
c['geometryLedger'].update(repairActualTouch=True,repairAdjacentWithinFiveFeet=True,repairLineUnobstructed=True)
c['testVectors']=[{
 'id':'DE4-N24-DISABLED-DRONE-04','scope':'Concrete existing vent disability plus proposed finite Compulsion expiry; not the separately conditional missing-phase branch.',
 'initialState':{'tinker':{'classLevel':5,'intelligence':18,'pb':3,'rp':4,'maximumRp':6,'dissonance':2,'ventShortRestUsesAvailable':1,'fieldRepairSelected':True,'fieldRepairRecharge':0},'drone':{'identity':'D','hp':14,'maxHp':14,'ac':17,'saveModifier':3,'disabled':False,'groundSupported':True},'wizard':{'classLevel':7,'intelligence':18,'pb':3,'specialization':'Abjuration','rp':14,'spell':'compulsion','school':'Enchantment','dc':15,'prepared':True},'originalOwnerTurnStarts':[0,6,12,18,24],'attachedPhaseMarkers':[2,8,14,20,26],'actualRepairTouchAt12_5':True},
 'rng':{'compulsionWisD20':7,'repairNominal2d8IfEvaluated':[2,3]},
 'operations':[
  {'at':0.5,'operation':'Tinker protected vent; BA and one short-rest use','expected':{'dissonance':0,'ventShortRestUsesAvailable':0,'droneDisabled':True,'tinkerRp':4}},
  {'at':2.5,'operation':'Wizard Compulsion; Action,7RP; WIS7+3=10 versus15 fails','expected':{'wizardRp':7,'pendingInstruction':True,'originalOpportunity':8}},
  {'at':8,'operation':'Sole attached-phase movement check, then expiry','expected':{'droneDisabled':True,'movementSpent':0,'pendingInstruction':False,'extraActions':0}},
  {'at':12.5,'operation':'Actual touch, selected Field Repair Recharge0, Action and1RP','expected':{'tinkerRp':3,'fieldRepairRecharge':2,'droneDisabled':False,'droneHp':14,'actualHpRestored':0,'pendingInstruction':False}},
  {'at':18,'operation':'Next regular Tinker START recharge tick','expected':{'fieldRepairRecharge':1}},
  {'at':24,'operation':'Following regular Tinker START recharge tick','expected':{'fieldRepairRecharge':0}}
 ],
 'expectedFinalState':{'sameDroneIdentity':'D','droneHp':14,'droneDisabled':False,'tinkerRp':3,'wizardRp':7,'ventShortRestUsesAvailable':0,'compulsionMovement':0,'pendingInstruction':False,'replayedCommands':0,'fieldRepairRechargeAt24':0}
}]
c=d['currentExamples'][24]
c.update(title='Legal Monk Illusion recast preserves old Null provenance; separate Wizard Enchantment test',
 initialState='Independent branch A uses Monk18 C, DEX18/PB6/S4, ordinary spellDC18, current/maxRP18, Dissonance0, no previous spell name and actually learned Phantasmal Killer through the Monk Illusion access at rank4. C has an already-established unsuppressed Null Veil. No optional cost or DC modifier applies; an ordinary spell does not gain a Monk technique Ki reduction. Target T is an ordinary living creature at100/100HP with WIS save+0, no psychic/fear defense, no temporary HP and no healing blocker or relevant wound. H is a conscious capable helper holding one actual NULL-ANTIDOTE-DOSE, has an available hand/Action, and can feed willing C. All are ground-supported, same plane, with clear LoE. C,H,T have ordered regular slots[0,2],[2,4],[4,6], repeating every6seconds. Casting at t0 or12 occurs after that caster START processing. No one voluntarily moves or interrupts. Branch B is a separate Wizard7 W, INT18/PB3, Abjuration specialization, spellDC15,14 currentRP of24 maximum, prepared Enchantment Phantasmal Killer, no modifier and no Null Veil, facing an independent100HP target immune only to Frightened.',
 actionsAndResolution=[
  'Branch A t0: C spends its real Action and7RP,18→11. Initial WIS9 failsDC18. Create Illusion applicationA/rootR with actual caster Null snapshot true, maximum t60, and establish the independent damage and fear components. Engine RNG4d10[3,4,5,6]=18 resolves once: T100→82HP. Mark numbered-round1 exposure used. Ordinary cast cadence increases Dissonance0→1; Ki is untouched.',
  'At t3 H uses its own Action, available hand and actual accessible dose to feed willing C within5ft; dose1→0 and C Null Veil ends immediately. This is consumable administration, not a second spell or concentration replacement. RootR remains Null-marked. At T START4 the round1 exposure is already used, so no second packet. T END6 WIS8 fails18, maintaining both components.',
  'At T START10 in numbered round2, rootR supplies4d10[3,4,5,6]=18 and remains nullNonlethal=true despite purge. T82→64HP. T END12 WIS7 fails18 before the next C turn starts. No fictitious packet occurs at t6, which is C START, not T START.',
  'At t12 after its real START, C casts the same legally accessible Illusion mode again: Action and7RP,11→4. New concentration commitment ends applicationA; it does not wait for the save and cannot be restored by a later failure. This repeat adds base1 plus Refrain1, Dissonance1→3, below Limit12 before payment. WIS6 fails18. Create applicationB/rootS, caster currently unVeiled, nullNonlethal=false, maximum t72. Round3 has no prior exposure, so4d10[3,4,5,6]=18 resolves T64→46 and spends round3 exposure. OldR remains historical with true; no historical flag is rewritten. T START16 cannot generate a second round3 packet. The new ordinary packet is not a claim that this46HP target dies.',
  'Independent branch B t0: actual Wizard7 W can use Enchantment, not the Monk Illusion placement. Pay7RP,14→7. Initial WIS9 fails15. Create distinct unVeiled rootW, resolve4d10[3,4,5,6]=18 once, target100→82HP. Its actual fear-only immunity prevents Frightened without preventing the independent damage. No ongoing fear application remains and no repeat damage/save is queued. Wizard first-distinct prepared-family exemption sets baseD0; no Refrain, generic Ki discount, cross-branch resource sharing or dual-school access is invented.',
  'Both branches retain their separate target identities and RNG streams. Allocating a root alone causes no damage, kill, Wound, resource grant or claimed round exposure. Branch A deals at most18 in a packet against maximum100HP and never reaches0; no Wound threshold or death-save event is reached in this fixture.'
 ],
 costLedger={'monkFirstCast':{'rank':4,'before':18,'cost':7,'after':11,'dissonanceBefore':0,'dissonanceAfter':1},'monkRecast':{'rank':4,'before':11,'cost':7,'after':4,'precastDissonance':1,'limit':12,'baseD':1,'refrain':1,'dissonanceAfter':3},'helperDose':{'action':1,'doseBefore':1,'doseAfter':0,'rangeMaximumFeet':5},'independentWizardEnchantment':{'rank':4,'before':14,'cost':7,'after':7,'dc':15,'firstDistinctBaseD':0}},
 clockLedger={'schedulePeriodSeconds':6,'casterStarts':[0,6,12],'helperStarts':[2,8,14],'targetStarts':[4,10,16],'targetEnds':[6,12,18],'castAfterStart':0,'actualCasterPurge':3,'oldRootPacket':10,'newSameMonkIllusionCastAfterStart':12,'originalMaximum':60,'newMaximum':72,'round1NoSecondPacketAt':4,'round3NoSecondPacketAt':16,'independentWizardCastAfterStart':0},
 geometryLedger={'bodyAabbsFeet':{'C':[[-1,-1,0],[1,1,6]],'H':[[2,-1,0],[4,1,6]],'T':[[19,-1,0],[21,1,6]]},'casterTargetReferencePointDistanceFeet':20,'nearestBodyDistanceFeet':18,'castRangeFeet':60,'helperCasterNearestBodyDistanceFeet':1,'doseWithinFiveFeet':True,'actualWillingDoseContact':True,'clearLoE':True,'allGroundSupported':True,'independentWizardGeometry':'same clear20ft relative caster/target fixture; separate identities, no simultaneous other branch'},
 outcome='The legal Monk recast demonstrates old Null-root persistence and a genuinely new unVeiled root without fabricating cross-school access. The separate legal Wizard branch preserves Enchantment single-packet and fear-only immunity behavior. Both skipped duplicate START exposures are explicit.')
c['testVectors']=[{
 'id':'DE4-N25-MONK-ILLUSION-04',
 'initialState':{'casterClass':'Monk','classLevel':18,'ability':'DEX','abilityScore':18,'pb':6,'school':'Illusion','rank':4,'rp':18,'maxRp':18,'dissonance':0,'lastSpellName':None,'nullVeil':True,'targetHp':100,'targetMaxHp':100,'targetWisModifier':0,'helperAntidoteDoses':1,'helperDoseLegal':True,'concentration':None},
 'rng':{'initialSaveD20':9,'endSaveAt6':8,'endSaveAt12':7,'recastSaveD20':6,'damageDiceByEvent':{'0':[3,4,5,6],'10':[3,4,5,6],'12':[3,4,5,6]}},
 'operations':[
  {'at':0,'operation':'Action cast after regular START','expected':{'rp':11,'dissonance':1,'root':'R','rootNull':True,'concentration':'A','targetHp':82,'exposureUsedRound':1}},
  {'at':3,'operation':'Helper administers actual Bittersap dose','expected':{'casterNullVeil':False,'rootRNull':True,'doseRemaining':0,'concentration':'A'}},
  {'at':4,'operation':'Target START round1','expected':{'newPackets':0,'targetHp':82}},
  {'at':6,'operation':'Target END repeat save before following C START','expected':{'saveTotal':8,'dc':18,'applicationAActive':True}},
  {'at':10,'operation':'Target START round2 periodic packet','expected':{'root':'R','rootNull':True,'targetHp':64,'exposureUsedRound':2}},
  {'at':12,'phase':'target-END','operation':'Repeat save before C next START','expected':{'saveTotal':7,'applicationAActive':True}},
  {'at':12,'phase':'caster-after-START-cast-commit','operation':'Same Monk casts same Illusion; replace concentration before save','expected':{'rp':4,'dissonance':3,'applicationAActive':False,'oldRootRHistoricalNull':True}},
  {'at':12,'phase':'new-cast-resolution','operation':'WIS6 fails18; new rootS and round3 packet','expected':{'concentration':'B','root':'S','rootNull':False,'targetHp':46,'exposureUsedRound':3}},
  {'at':16,'operation':'Target START round3','expected':{'newPackets':0,'targetHp':46}}
 ],
 'expectedFinalState':{'casterRp':4,'casterDissonance':3,'casterNullVeil':False,'rootRHistoricalNull':True,'rootSNull':False,'targetHp':46,'targetFrightened':True,'concentration':'B','oldApplicationEndedAt':12,'newApplicationMaximum':72,'helperDoseRemaining':0,'totalDamagePackets':3,'woundsAdded':0,'deathSaves':0}
},{
 'id':'DE4-N25-WIZARD-ENCHANTMENT-04','independentBranch':True,
 'initialState':{'casterClass':'Wizard','classLevel':7,'ability':'INT','abilityScore':18,'pb':3,'specialization':'Abjuration','school':'Enchantment','rank':4,'prepared':True,'rp':14,'maxRp':24,'dissonance':0,'firstDistinctFamily':True,'nullVeil':False,'targetHp':100,'targetMaxHp':100,'targetWisModifier':0,'targetFearImmune':True,'targetPsychicImmune':False},
 'rng':{'initialSaveD20':9,'damageDice':[3,4,5,6]},
 'operations':[{'at':0,'operation':'Legal Action Enchantment cast','expected':{'rp':7,'dc':15,'saveTotal':9,'saveFails':True,'root':'W','rootNull':False,'damage':18,'targetHp':82,'fearEstablished':False,'ongoingApplication':False}}],
 'expectedFinalState':{'casterRp':7,'casterDissonance':0,'targetHp':82,'damagePackets':1,'targetFrightened':False,'ongoingApplication':False,'repeatDamageQueued':0,'repeatSavesQueued':0}
}]
def ref(path,pointer=None,section=None):
 result={'path':(R/path).relative_to(G).as_posix()}
 if pointer is not None:result['pointer']=pointer
 if section is not None:result['section']=section
 return result
c['sourceRefs'].extend([ref('data/public/class_playtests/monk.json','/engine/0'),ref('data/public/class_playtests/monk.json','/rpByClassLevel/17'),ref('data/public/class_playtests/monk.json','/maxSpellRankByClassLevel/17'),ref('data/public/class_playtests/wizard.json','/engine/7'),ref('data/public/class_playtests/wizard.json','/rpByClassLevel/6'),{'path':newrel,'pointer':'/spells/12/completeSourceAndAccess/classAccess'},ref('docs/mechanics/EQUIPMENT_ITEM_PROCEDURES.md',section='Opening consumable administration rule'),ref('docs/mechanics/COMBAT_ACTION_PLAYTEST.md',section='Time and event ordering'),ref('docs/mechanics/SPELL_INTEGRATION_RULES.md',section='Resolve a cast at the table')])
for p in [oldpath,A/'accelerated-review-01/DE4_EXAMPLE_FINDINGS_04.json']:
 if p.relative_to(G).as_posix() not in {x['path'] for x in d['sourceBindings']}:d['sourceBindings'].append(info(p))
checks=[]
def check(label,actual,expected=True):
 checks.append({'check':label,'passed':actual==expected,**({} if actual==expected else {'actual':actual,'expected':expected})})
check('same15 full spell/procedure records',d['spells'],old['spells'])
check('shared rules unchanged',d['sharedRules'],old['sharedRules'])
for key in ['originalExamplesUnchanged','originalSharedProposalUnchanged','originalIssuesUnchanged','currentIssuesForJointDisposition','guardAmendment','remainingJointChoices']:
 check('preserved '+key,d[key],old[key])
check('all30 case IDs and order',[c['id'] for c in d['currentExamples']],[c['id'] for c in old['currentExamples']])
for i in range(30):
 if i in [23,24]:continue
 expected=deepcopy(old['currentExamples'][i])
 for rr in expected['sourceRefs']:
  if rr['path']==oldrel:rr['path']=newrel
 check('unchanged case except current self-reference '+str(i),d['currentExamples'][i],expected)
for b in d['sourceBindings']:check('source hash '+b['path'],info(G/b['path']),b)
for case in d['currentExamples']:
 for i,rr in enumerate(case['sourceRefs']):
  source=d if rr['path']==newrel else read(G/rr['path']) if 'pointer' in rr else None
  if 'pointer' in rr:
   try:valid=at(source,rr['pointer']) is not None
   except Exception:valid=False
   check(case['id']+' pointer '+str(i),valid)
  else:check(case['id']+' descriptive section file '+str(i),(G/rr['path']).is_file())
monk=read(R/'data/public/class_playtests/monk.json');wizard=read(R/'data/public/class_playtests/wizard.json');tinker=read(R/'data/public/class_playtests/tinker.json');access=d['spells'][12]['completeSourceAndAccess']['classAccess']
check('Monk Illusion rank4 access',access['Monk'],{'rank':4,'minimumClassLevel':18,'school':'Illusion','baseRpCost':7})
check('Wizard Enchantment rank4 access',access['Wizard'],{'rank':4,'minimumClassLevel':7,'school':'Enchantment','baseRpCost':7})
check('Monk18 RP actual18',monk['rpByClassLevel'][17],18);check('Monk18 legalrank4',monk['maxSpellRankByClassLevel'][17],4);check('Wizard7 RP14 within actual maximum',14<=wizard['rpByClassLevel'][6]);check('Tinker5 RP4 within maximum',4<=tinker['rpByClassLevel'][4])
check('FieldRepair actual Action',tinker['cards'][7]['activation'],'Action');check('FieldRepair actual touch',tinker['cards'][7]['rangeAndTarget'],'One construct/device touched');check('FieldRepair actual recharge',tinker['cards'][7]['frequency'],'Recharge 2')
check('FieldRepair protected state exception','clears that disabled state' in tinker['cards'][7]['effect'])
for label,actual,expected in [('Monk DC',8+6+(18-10)//2,18),('Wizard DC',8+3+(18-10)//2,15),('Monk Limit',max(4,2+6+4),12),('Monk RP',18-7-7,4),('Monk D',1+1+1,3),('damage dice',sum([3,4,5,6]),18),('HP after3 packets',100-3*18,46),('HP separate Enchantment',100-18,82),('no threshold wound',2*18<100,True),('Tinker HP',5+4+5,14),('Tinker AC',13+4,17),('drone save failure',7+3<15,True),('repair RP',4-1,3),('repair cappedHP',min(14,14+sum([2,3])+4),14),('recharge18',max(0,2-1),1),('recharge24',max(0,2-2),0),('oldmaximum',0+60,60),('newmaximum',12+60,72)]:check('arithmetic '+label,actual,expected)
# Independent opportunity arithmetic: target starts4,10,16; one packet per numbered round.
used=set();actual=[]
for seconds,event in [(0,'initial'),(4,'periodic'),(10,'periodic'),(12,'newInitial'),(16,'periodic')]:
 rnd=int(seconds//6)+1;admitted=rnd not in used
 if admitted:used.add(rnd)
 actual.append({'at':seconds,'round':rnd,'packet':admitted})
check('round exposure schedule',actual,[{'at':0,'round':1,'packet':True},{'at':4,'round':1,'packet':False},{'at':10,'round':2,'packet':True},{'at':12,'round':3,'packet':True},{'at':16,'round':3,'packet':False}])
check('cast reference range',20<=60);check('nearest volume range',19-1,18);check('dose actual distance',2-1,1);check('dose within5',1<=5)
check('Null root old remains true',d['currentExamples'][24]['testVectors'][0]['expectedFinalState']['rootRHistoricalNull']);check('new root is ordinary',d['currentExamples'][24]['testVectors'][0]['expectedFinalState']['rootSNull'],False)
check('original file unchanged',info(oldpath),oldbinding)
assert all(c['passed'] for c in checks),[c for c in checks if not c['passed']]
newpath.write_bytes(encoded(d))
report={'id':'DE4-DIGITAL-FIXTURES-CHECK-04','recordedAtUtc':now,'draft':info(newpath),'previousDraft':oldbinding,'sourceCount':len(d['sourceBindings']),'identities':15,'currentExamples':30,'originalExamples':30,'newStructuredVectors':3,'changedCases':['DE4-N24','DE4-N25'],'checkCount':len(checks),'failureCount':0,'checks':checks,'scope':'Source/hash, full unchanged procedure/history comparison, JSON pointers and specific fixture arithmetic/opportunity checks. Descriptive section labels are file-existence references, not verified heading pointers. Test vectors specify expected engine behavior but do not execute the game engine.','newRuleAdoptions':0,'rulesChanged':0,'runtimeTestsExecuted':False,'humanPlaytested':False,'numericalBalanceApproved':False,'sourceInformationDeleted':0,'remaining':'All DE4 procedures and substantive proposed interfaces remain pending actual joint review; this repair does not accept the Fate guard or Compulsion timing proposal.'}
reportpath.write_bytes(encoded(report));print(json.dumps({'draft':info(newpath),'report':info(reportpath),'checks':len(checks),'failures':0,'sourceCount':len(d['sourceBindings']),'structuredVectors':3,'newRuleAdoptions':0}))
