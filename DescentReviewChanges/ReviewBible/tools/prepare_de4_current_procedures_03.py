"""Repair identified DE4 draft semantics; preserve old records, adopt nothing."""
from copy import deepcopy
from datetime import datetime,timezone
import hashlib,json
from pathlib import Path

G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
oldpath=R/'data/director/spell_proposals/divination_enchantment_rank4_current_02.json'
newpath=R/'data/director/spell_proposals/divination_enchantment_rank4_current_03.json'
reportpath=A/'DE4_CURRENT_PROCEDURES_CHECK_03.json'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha(b)}
def enc(d):return (json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf8')
def ref(rel,pointer=None,section=None):return {'path':'DescentReviewChanges/ReviewBible/'+rel,**({'pointer':pointer} if pointer is not None else {'section':section})}
def at(d,p):
 for t in p.strip('/').split('/') if p else []:
  t=t.replace('~1','/').replace('~0','~');d=d[int(t)] if isinstance(d,list) else d[t]
 return d

assert not newpath.exists() and not reportpath.exists()
old=read(oldpath);d=deepcopy(old);now=datetime.now(timezone.utc).isoformat()
d.update(id='DE4-CURRENT-PROCEDURES-03',recordedAtUtc=now,status='Complete local replacement draft with explicit finite Compulsion proposal and corrected examples. Unsent and unadopted; joint review, all cross-system semantics and numerical playtesting remain open.',previousDraft=info(oldpath))
case={c['id']:c for c in d['currentExamples']};spell={s['spellId']:s for s in d['spells']}
d['previousChangedExamples']=[deepcopy(case[i]) for i in ['DE4-N05','DE4-N11','DE4-N13','DE4-N16','DE4-N24']]
for c in d['currentExamples']:
 for r in c['sourceRefs']:
  if r.get('path')==oldpath.relative_to(G).as_posix():r['path']=newpath.relative_to(G).as_posix()

# Use an ordinary, supported score fixture. The procedure still preserves an
# actually lawful higher score; this example no longer invents its source.
c=case['DE4-N05'];c['initialState']='Druid10 has current INT19,WIS20,M5 and a Buffer Reserve already recorded after its last beneficial Long Rest at2*10+5=25,currently17. An eligible caster applies Aspect; no rest occurs.'
c['actionsAndResolution'][0]='INT becomes20,modifier+5 instead of+4. WIS20 is already at this spell\'s cap and receives no increase; its modifier remains+5.'
c['sourceRefs'].append(ref('data/public/class_playtests/druid.json','/engine'))

c=case['DE4-N11']
c.update(title='Forecast portal creation eligibility, without inventing a traveler alignment gate',
 initialState='Independent branches start with F, a Cleric7 who actually knows/prepares Alignment Forecast, 21RP and no current price modifier; T is a Wizard9 who actually knows/prepares accepted Alignment Portal and has20RP. T has underlying LawfulEvil and another caster\'s live Alignment Lock snapshotNeutralGood, with known absolute expiry t30. Both axes and the relevant timing are established and unprotected. Actual different destination plane P/site S is personally known and its established Portal compatibility record admits NeutralGood only. Its clear supported portalPose and the valid clear supported origin pose are already recorded. At t10 F perceives T at20ft with clear LoE. All branches below are independent; one paid Forecast per branch, no accumulation of casts or resources between alternatives.',
 actionsAndResolution=[
  'Branch A asks about T creating a NEW Portal at t20 to reach P/S. F pays7RP,21→14. The supported t20 effective alignment is NeutralGood and the actual compatibility predicate passes. Forecast returns Favored for the alignment contribution only. If that stated cast actually occurs with all other prerequisites still legal, T pays10RP,20→10, forming the portal at t20 with deadline t80.',
  'Branch B instead asks about T creating a NEW Portal at t40. F independently pays7RP,21→14. The known t30 Lock expiry exposes T\'s actual underlying LawfulEvil, which the recorded site does not admit. Forecast returns Opposed. At the actual known-ineligible t40 preflight T cannot begin that portal cast and spends no10RP; no portal forms. This is not a claim that Forecast itself spends T\'s resources or guarantees future behavior.',
  'Branch C already has the legally formed Branch-A portal, snapshotNeutralGood and fixed deadline t80. At t30 the Lock expires; the portal remains. T\'s supported legal physical crossing at t40 is NOT barred by now being LawfulEvil: accepted Alignment Portal has no later traveler-alignment gate. On ordinary clear ground a fitting Medium T uses5 movement through the5x8ft aperture, subject to actual whole-body/ward checks. A new Forecast inquiry about that crossing returns Unaffected for the proposed alignment-change obstruction because that obstruction does not exist; it does not guarantee unrelated transit legality.',
  'Only Favored/Opposed/Unaffected is delivered by the relevant inquiry, not axes, destination coordinates, hidden identities or the causal explanation. Unknown/protected premises would instead require Indeterminate under the procedure. The historical ward-crossing premise is explicitly corrected, not silently treated as an accepted travel restriction.'
 ],costLedger={'forecastPerIndependentBranch':{'before':21,'cost':7,'after':14},'portalCreationAt20':{'before':20,'cost':10,'after':10},'knownIllegalPortalCreationAt40':{'before':20,'cost':0,'after':20},'existingPortalCrossingMovement':5},
 clockLedger={'inquiry':10,'compatibleCreation':20,'lockExpiry':30,'incompatibleCreationOrExistingPortalCrossing':40,'existingPortalDeadline':80},
 geometryLedger={'forecastRange':20,'forecastLoE':True,'portalApertureFeet':[5,8],'originAndDestination':'actual clear supported recorded poses on different planes; Medium body fits; no active blocker'},
 outcome='Caster compatibility is checked for formation. A known Lock expiry can change new-cast eligibility, but cannot invent a later traveler gate or close an established portal.')
c['sourceRefs'].extend([ref('data/public/spell_candidates/abjuration_conjuration_rank5_reviewed_05.json','/spells/15/procedure'),ref('data/public/spell_candidates/abjuration_conjuration_rank5_reviewed_05.json','/spells/15/completeSourceAndAccess/classAccess')])

c=case['DE4-N13']
c.update(title='Actual Wizard Dispel expenditure, separate Oracle RC and item charge',
 initialState='Wizard7 W has12 current ordinary RP, INT18/PB3, actual acquired Arch Dispel Magic /cards/19 ready with Recharge0, an available Action and no price modifier or blocking strain. W actually possesses the unique bonded Shard Pendant of Xi, with its legal item-bound charge1. An independently cast reviewed Light is active on a nonliving1lb stone fitting a1ft cube at20ft, unoccluded and perceived; its one-hour deadline has not elapsed. The Light is rank0 and no Seal, suppression or other nondispel protection applies. On the later inquiry turn F is a Cleric7 with acquired/prepared Resonance Divination,14RP and no price modifier, perceiving W at20ft/clear LoE. Independent comparison fixtures use Oracle6 O with its actual5RC and no RP pool, and a Wizard with a genuinely defined current RP pool0.',
 actionsAndResolution=[
  'W spends the actual Dispel Action and3RP:12→9, applies rank3 spell cadence under its actual class engine and sets that card\'s Recharge2. Its single perceived ongoing target is the rank0 Light, so its own automatic rank≤3 termination ends that Light. No check, borrowed ordinary Dispel price, item charge or invented RP expenditure is used.',
  'On F\'s later actual turn after that completed event, F pays7RP,14→7, and reads W\'s exact ordinary RP9 at resolution. Xi charge1 is a separate actual item ledger, so the answer is9, never10. The inquiry reveals no item inventory, class, maximum, spending history or recharge counter and consumes no Xi charge.',
  'In the separate Oracle6 fixture, F\'s lawful paid inquiry reports Indeterminate: the Oracle\'s actual5RC are not an ordinary RP pool. No multiclass or dual-resource Wizard/Oracle is fabricated. The separate readable actual RP0 fixture reports exactly0. Independent branches do not share F\'s spent RP/cadence.',
  'If actual information protection defeats the read, the result is Indeterminate without exposing the reason. These fixtures create no new pool, charge, refill or continuing feed.'
 ],costLedger={'wizardDispel':{'before':12,'cost':3,'after':9,'rank':3,'rechargeAfterUse':2},'reader':{'before':14,'cost':7,'after':7},'separateLedgers':{'wizardXiItemCharge':1,'independentOracle6RC':5,'oracleRP':'absent'}},
 clockLedger={'dispel':'W prior completed regular-turn Action','read':'later F regular-turn Action; one resolution snapshot','light':'ended before its original3600-second deadline; no reset'},
 geometryLedger={'dispelTargetRangeFeet':20,'lightStonePounds':1,'lightStoneCubeFeet':1,'inquiryTargetRangeFeet':20,'clearLoE':True},
 outcome='The actual3RP spell reduces the Wizard ledger12→9. Oracle RC and the unique relic charge stay separate, with zero distinguished from no RP pool.')
c['sourceRefs'].extend([ref('data/public/class_playtests/wizard.json','/cards/19'),ref('data/public/class_playtests/oracle.json','/cards/0'),ref('data/public/spell_playtests/authored_review_index.json','/entries/782'),ref('data/public/spell_playtests/candidate_low_rank_136.json','/spells/32/operationalCandidate'),ref('data/public/spell_playtests/catalog.json','/spells/782'),ref('docs/mechanics/COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md',section='Shard Pendant of Xi: actual one item-bound charge')])

c=case['DE4-N16']
c.update(title='Different-controller replacement and independent same-caster concentration loss',
 initialState='D1,D2,D3 are actual Wizard7 casters with acquired/prepared Dominate Person, INT18/PB3, spellDC15, available casting Actions and sufficient actual RP. T is a perceived Humanoid within60ft/LoE, no relevant immunity/protection, WIS save modifier0. In this same encounter D2 previously established Dominate Person on T at t-12, spending its D2/T hard guard, then voluntarily ended that concentration at t-6. D1 legally established its own application at t0, spending D1/T guard and7RP from14→7; it remains concentrated, original deadline t60. All required intervening END saves fail. D2 has7RP remaining after its earlier cast, D3 has14RP and unused D3/T hard guard. All relevant pre-cast Dissonance remains below the actual Limit9; ordinary new cadence/repeat history is still applied, not reset. Branches below are independent where described.',
 actionsAndResolution=[
  'At t6 D2 pays7RP,7→0. If T rolls16, the save succeeds and no new control establishes. In the independent failed-save branch T rolls10; D2/T history already blocks a second hard component, so no new control establishes. Either outcome leaves D1\'s still-live concentration/application and original t60 deadline intact: D2 committed no action that displaces D1\'s concentration slot.',
  'At t12 a separately eligible D3 pays7RP,14→7; T rolls8 against15. With D3/T guard unused, its hard component genuinely establishes, spends that guard and replaces the old same-spell D1 control. D3 has a new t72 maximum and its own saves. No old guard, RP, resolved order or source clock is refunded. Ending D1\'s last remaining effect ends that old concentration normally.',
  'Independent same-caster branch from the t0 state: D1 recasts at t6, paying its remaining7RP. Ordinary new concentration commitment ends D1\'s old control BEFORE the new save. A new success or failed-save guard block establishes no replacement; old control does not return. This branch has no still-live old application to preserve.',
  'For any later genuine order opportunity, the proposed same-plane conscious issuance channel applies. Different planes prevent a new order; no location/sensory feed or cross-plane network is added.'
 ],costLedger={'D1Initial':{'before':14,'cost':7,'after':7},'D2NewAttempt':{'before':7,'cost':7,'after':0},'D3NewAttempt':{'before':14,'cost':7,'after':7},'independentD1Recast':{'before':7,'cost':7,'after':0}},
 clockLedger={'oldD1Application':0,'oldD1Maximum':60,'differentD2Attempt':6,'successfulD3Replacement':12,'newD3Maximum':72,'independentSelfRecast':6},
 geometryLedger={'actualHumanoidTarget':True,'rangeAtEachCastFeet':'≤60','perceivedAndClearLoE':True},
 outcome='Failed establishment by another controller does not replace D1. D1\'s own ordinary recast ends old concentration at commitment even when its new control fails.')
c['sourceRefs'].append(ref('docs/mechanics/SPELL_INTEGRATION_RULES.md',section='Legal casting sequence: concentration commitment before resolution; shared hard-control history'))
spell['dominate-person']['procedure']+='\n\nCONCENTRATION/REPLACEMENT DISTINCTION: the failed-establishment no-replacement rule does not protect a caster\'s old concentration from that same caster starting a new concentration spell. Ordinary commitment ends the incompatible old concentration before resolution, with no restoration on a later successful save or blocked hard component. Another caster\'s failed attempt does not by itself displace the original caster\'s concentration.'

finite_rule=(
 'NEW DE4-COMPULSION-EXPIRY-03, scoped only to Compulsion: at successful failed-save establishment record one pending instruction, its application order, original timing basis and one finite latest opportunity marker. For a creature with a regular turn schedule, use its next future regular START, excluding a turn already underway. For an owner-attached chassis, use the attached-phase boundary after the next original-owner regular turn that has not begun; record the original regular owner END/attached-phase marker even if an actual phase may be unavailable then. If no such original schedule/marker exists, use application+6 elapsed seconds. These are spell-only timing records, not new creature turns. Preserve the original marker and its virtual elapsed-time mapping through initiative changes, absence, extra turns and relocation. '
 'Use at most one qualifying future actual movement opportunity within that window; an attached target can execute only in its real source-authorized original-owner regular attached phase. An already-underway owner turn supplies no newly compelled phase. A genuinely earlier qualifying opportunity after a schedule change can consume the instruction once, with only its actual remaining budget. A later rescheduling cannot carry the instruction past its original finite marker. At the recorded boundary, finish ordinary required START/phase processing before this instruction\'s sole eligibility/movement check; immediately after that check expire it whether movement was possible, blocked, suppressed or zero. This specifically typed expiry-after-opportunity ordering avoids expiring the instruction before its own simultaneous check; it is not a change to global phase0 duration expiry. '
 'When the actual lifecycle supplies no qualifying phase at the recorded boundary, perform an expiry-only bookkeeping check at that original marker and remove the instruction. This check grants no movement, Action, Reaction, recharge, control START, command or owner resource expenditure. An owner-attached target with no original schedule therefore expires at application+6 if no independently supplied lawful phase occurs first. A normal independent creature outside initiative can have the one expressly proposed ordinary movement opportunity by application+6 under the real shared behavior budget; establish initiative before hostile behavior. No phase, target physiology, missing movement mode or new budget is inferred from that fallback. A later repair, owner return, phase creation or suppression ending never replays an expired instruction. This is explicit NEW joint-review authorship, not an already accepted general timing rule.'
)
d['sharedRules']['DE4-COMPULSION-EXPIRY-03']=finite_rule
spell['compulsion']['procedure']=spell['compulsion']['procedure'].replace('It expires after this opportunity. Outside initiative resolve one ordinary movement opportunity within six elapsed seconds; establish initiative first when combat timing matters. A companion uses only movement in its next actual original-owner regular attached phase, with no extra phase, Action, offensive allowance or owner resource charge.', 'It has exactly one finite opportunity and expiry under DE4-COMPULSION-EXPIRY-03 below. A companion uses only movement in the real attached phase after the next original-owner regular turn that has not begun, bounded by the preserved original marker or six-second no-schedule fallback; it receives no extra phase, Action, offensive allowance or owner resource charge.')
spell['compulsion']['procedure']+='\n\n'+finite_rule
c=case['DE4-N24']
tinker=read(R/'data/public/class_playtests/tinker.json')
repair_index=next(i for i,v in enumerate(tinker['cards']) if v['name']=='Field Repair')
c.update(title='Finite expiry with an actually disabled drone and a separately absent-phase boundary',
 initialState='Actual Tinker5 INT18/PB3 has one owned Anacite Drone, AC17/HP14, ground-supported at a clear position, and4RP. The Drone is a Construct with the printed poison/psychic immunity and no charm; Compulsion is a movement instruction, not Charmed or psychic damage, so those facts alone do not exclude it. Tinker has the actual selected Field Repair card. Its regular turn runs t0..2, next t6..8, then t12..14; attached phases follow each complete turn. At t0.5 Tinker uses its actual available once/short-rest Bonus Action vent, routing2 current Dissonance into its own active drone5ft away: Dissonance2→0 and the device is disabled under the actual engine. At t2.5 Wizard7 with INT18/PB3, actual prepared Compulsion,14RP and no price modifier targets the perceived drone20ft away with clear LoE. Drone uses its actual owner-PB save modifier+3; natural7 gives10 againstDC15.',
 actionsAndResolution=[
  'Wizard pays7RP,14→7. The failed save establishes one instruction due at the original attached-phase boundary t8, after the next not-yet-started Tinker regular turn. Tinker does not repair it on that t6..8 turn. This spell supplies no unwilling owner BA or command and no replacement phase.',
  'At actual phase t8 the still-disabled drone cannot move under its real vent-disability source. The Compulsion eligibility/movement check executes once and spends0 movement, then the instruction expires immediately after that check at t8. It does not add an attack, offense, Reaction or second phase.',
  'At t12.5 Tinker spends the actual Field Repair Action and1RP,4→3, ending the device disability under its explicit repair interface. The same already-full-HP drone remains14HP; the expired Compulsion does not resume, and no prior owner command is replayed.',
  'Separate negative scheduling branch, explicitly conditional rather than a claim that venting deletes phases: if an actual independently established lifecycle supplies NO phase at the recorded t8 boundary, DE4-COMPULSION-EXPIRY-03 performs expiry-only bookkeeping at t8 and grants no execution. A phase restored at t8.1 cannot replay it. This branch defines the missing-phase contract; it does not invent a named source that removed the phase.',
  'Separate no-schedule fallback: an otherwise valid attached-target instruction established at t100 with no original owner schedule records expiry106. If no independently lawful phase occurs before or at106, it expires at106 without movement; later source activity grants no retry. A concrete available phase earlier in that window may consume the same instruction only once under its real remaining budget.'
 ],costLedger={'tinkerVent':{'bonusActions':1,'shortRestUses':1,'dissonanceBefore':2,'dissonanceAfter':0,'rp':0},'compulsion':{'rpBefore':14,'cost':7,'after':7},'laterActualRepair':{'actions':1,'rpBefore':4,'cost':1,'after':3},'compulsionOwnerCommandCost':0},
 clockLedger={'vent':0.5,'application':2.5,'originalOwnerNextStart':6,'originalOwnerPhaseMarker':8,'instructionExpiry':'t8 immediately after its sole check; expiry-only if phase absent','laterRepair':12.5,'separateNoScheduleApplication':100,'separateNoScheduleExpiry':106},
 geometryLedger={'droneGroundSupported':True,'droneHP':14,'ventRangeFeet':5,'compulsionRangeFeet':20,'realPhaseMovementWhileDisabled':0,'conditionalMissingPhaseBranch':'no fabricated source trigger or independent turn'},
 outcome='The real disability case expires after one zero-movement check. The explicit missing-phase and no-schedule branches expire at finite markers without inventing an execution event.')
c['sourceRefs'].extend([ref('data/public/class_playtests/tinker.json','/engine/1'),ref('data/public/class_playtests/tinker.json','/engine/7'),ref('data/public/class_playtests/tinker.json',f'/cards/{repair_index}'),ref('docs/mechanics/COMBAT_ACTION_PLAYTEST.md',section='Time and event ordering: preserved original markers'),ref('docs/mechanics/CONTROL_STATES_PLAYTEST.md',section='Typed (seconds,phase) expiry ordering'),{'path':newpath.relative_to(G).as_posix(),'pointer':'/sharedRules/DE4-COMPULSION-EXPIRY-03'}])
d['remainingJointChoices'].append('DE4-COMPULSION-EXPIRY-03 finite original marker/expiry-after-opportunity/no-phase and no-schedule fallback; owner already-started turn excluded. Requires actual joint review, not a global clock amendment.')
d['semanticCorrections']=[
 {'id':'DE4-L03-01','status':'Locally corrected; joint review pending','cases':['DE4-N11'],'result':'Actual new Portal formation compatibility at20 versus40; no later traveler-alignment gate. Original required premise preserved as unsupported.'},
 {'id':'DE4-L03-02','status':'Locally corrected; joint review pending','cases':['DE4-N16'],'result':'Different-controller failed establishment retains D1; same-caster normal concentration commitment independently ends D1 before outcome.'},
 {'id':'DE4-L03-03','status':'Locally corrected; joint review pending','cases':['DE4-N13'],'result':'Actual Wizard class Dispel removes reviewed Light for3RP; Oracle6 RC5 is an independent target, Xi actual charge is1, not invented2.'},
 {'id':'DE4-L03-04','status':'Explicit NEW local finite-clock proposal; joint review pending','cases':['DE4-N24'],'result':'One original opportunity marker or+6 fallback, expire after sole actual/expiry-only check. Source-qualified disabled-drone branch; genuinely missing-phase branch clearly conditional.'},
 {'id':'DE4-L03-05','status':'Local fixture correction; joint review pending','cases':['DE4-N05'],'result':'Use ordinary WIS20/M5 rather than an unsourced above20 score. Higher lawful source scores still obey the unchanged procedure.'}
]

new_sources=[oldpath,A/'DE4_CURRENT_DRAFT_02_SEMANTIC_NOTES.json',R/'data/public/spell_playtests/candidate_low_rank_136.json']
known={e['path'] for e in d['sourceBindings']}
for p in new_sources:
 if p.relative_to(G).as_posix() not in known:d['sourceBindings'].append(info(p))
checks=[]
def check(k,a,b=True): checks.append({'check':k,'passed':a==b,**({} if a==b else {'actual':a,'expected':b})})
check('15 identity/order preservation',[s['spellId'] for s in d['spells']],[s['spellId'] for s in old['spells']])
check('30 current IDs/order preservation',[c['id'] for c in d['currentExamples']],[c['id'] for c in old['currentExamples']])
for field in ['originalExamplesUnchanged','originalSharedProposalUnchanged','originalIssuesUnchanged','currentIssuesForJointDisposition','guardAmendment']:
 check('unchanged '+field,d[field],old[field])
for n,o in zip(d['spells'],old['spells']):
 for k in ['questionId','completeSourceAndAccess','originalQuestion','historicalProposalUnchanged']:
  check(n['spellId']+' preserved '+k,n[k],o[k])
 if n['spellId'] not in ['compulsion','dominate-person']:check(n['spellId']+' procedure unchanged',n['procedure'],o['procedure'])
for e in d['sourceBindings']:
 b=(G/e['path']).read_bytes();check('source length '+e['path'],len(b),e['bytes']);check('source hash '+e['path'],sha(b),e['sha256'])
for c in d['currentExamples']:
 for j,r in enumerate(c['sourceRefs']):
  path=G/r['path']
  if 'pointer' in r:
   obj=d if path==newpath else read(path)
   try:value=at(obj,r['pointer']);valid=value is not None
   except Exception:valid=False
   check(c['id']+' pointer '+str(j),valid)
  else:check(c['id']+' section source '+str(j),path.exists())
check('source reviewed Light',read(R/'data/public/spell_playtests/authored_review_index.json')['entries'][782]['id'],'light')
check('Light rank0',read(R/'data/public/spell_playtests/catalog.json')['spells'][782]['classAccess']['Wizard']['rank'],0)
check('Wizard class Dispel rank3',read(R/'data/public/class_playtests/wizard.json')['cards'][19]['spellRank'],3)
check('fixed expiry present in Compulsion',finite_rule in spell['compulsion']['procedure'])
for name,actual,expected in [('forecast cost',21-7,14),('portal cost',20-10,10),('portal deadline',20+60,80),('Dispel RP',12-3,9),('reader RP',14-7,7),('new domination deadline',12+60,72),('drone HP',5+4+5,14),('drone save',7+3,10),('DC',8+3+4,15),('repair RP',4-1,3),('no-schedule deadline',100+6,106),('Druid Buffer',2*10+5,25)]:check('worked arithmetic '+name,actual,expected)
assert all(x['passed'] for x in checks),[x for x in checks if not x['passed']]
newpath.write_bytes(enc(d))
report={'id':'DE4-CURRENT-PROCEDURES-CHECK-03','recordedAtUtc':now,'draft':info(newpath),'previousDraft':info(oldpath),'checkCount':len(checks),'failureCount':0,'checks':checks,'identities':15,'currentExamples':30,'historicalExamples':30,'sourceCount':len(d['sourceBindings']),'semanticCorrections':d['semanticCorrections'],'scope':'Static preservation, source references and selected arithmetic. Does not prove all semantics, runtime or balance. New finite clock and all DE4 rules require actual joint review.','newSpellAdoptions':0,'sourceInformationDeleted':0,'runtimeTestsExecuted':False,'humanPlaytested':False}
reportpath.write_bytes(enc(report))
print(json.dumps({'draft':info(newpath),'check':info(reportpath),'checks':len(checks),'failures':0,'sourceCount':len(d['sourceBindings']),'changedCases':5,'newSpellAdoptions':0}))
