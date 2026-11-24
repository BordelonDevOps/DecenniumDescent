"""Retain native initial rest/recovery assessment evidence; no module acceptance."""
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

PACKET=Path(__file__).resolve().parents[1]; ROOT=PACKET.parents[3]
ARTIFACTS=ROOT/'engine/artifacts/admitted-command-surface'; OUT=PACKET/'runtime-checkpoint-05'
OUT.mkdir(exist_ok=True)
def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

run=ARTIFACTS/'development-10';build=run/'run-20261124T040414643Z-f62dbcfd'
recovery=run/'recovery'
bishop=run/'bishop/chr03_bishop_connected_earned_funded_cure_aura_dispel_continue'
consecration=run/'consecration/chr05_consecration_genuine_paid_zone_rite_and_expiry'
paths={
 'candidate10-rest.json':build/'results.json',
 'candidate10-recovery.json':recovery/'results.json',
 'candidate10-bishop.json':run/'bishop/results.json',
 'candidate10-consecration.json':run/'consecration/results.json',
 'candidate10-package.json':run/'static-20261124T040607783Z-1fd90f8d/results.json',
 'long-rest-independent-review.json':ARTIFACTS/'long-rest-assessment-cross-review-01.json',
 'recovery-abilities-independent-review.json':ARTIFACTS/'recovery-abilities-assessment-cross-review-01.json',
 'source-candidate10.zip':build/'source-frozen.zip',
 'rest-assessment-facts.json':build/'saves/int05-rest-assessment-facts.json',
 'rest-before.ddsave':build/'saves/int05-rest-before.ddsave',
 'rest-pending.ddsave':build/'saves/int05-rest-pending.ddsave',
 'rest-interrupted.ddsave':build/'saves/int05-rest-interrupted.ddsave',
 'initial-rite-paid.ddsave':recovery/'chr02_cleric_connected_injury_payment_restore_and_continuation/cleric-paid.ddsave',
 'radiance-before.ddsave':recovery/'chr03_alternate_genuine_paid_radiance_and_continuation/cleric-before-radiance.ddsave',
 'radiance-after.ddsave':recovery/'chr03_alternate_genuine_paid_radiance_and_continuation/cleric-after-radiance.ddsave',
 'rest-first-funded.ddsave':recovery/'mgt03_long_rest_genuine_first_funding_and_paid_continuation/long-rest-first-funded.ddsave',
 'rest-paid-continuation.ddsave':recovery/'mgt03_long_rest_genuine_first_funding_and_paid_continuation/long-rest-paid-continuation.ddsave',
 'bishop-invocation-cure.ddsave':bishop/'invocation-cure.ddsave',
 'bishop-rite-radiance-aura.ddsave':bishop/'rite-radiance-aura.ddsave',
 'bishop-connected-facts.json':bishop/'bishop-connected-facts.json',
 'consecration-paid.ddsave':consecration/'consecration-paid.ddsave',
 'consecration-rite.ddsave':consecration/'consecration-rite.ddsave',
 'consecration-expired.ddsave':consecration/'consecration-expired.ddsave',
}
compiled=load(paths['candidate10-rest.json'])
assert compiled['status']=='PASS' and compiled['passed']==1 and compiled['testsDiscovered']==1
for name,count in [('candidate10-recovery.json',4),('candidate10-bishop.json',1),('candidate10-consecration.json',1)]:
 report=load(paths[name]);assert report['status']=='PASS' and len(report['cases'])==count and all(c['Passed'] for c in report['cases'])
assert load(paths['candidate10-package.json'])['status']=='PASS'
with zipfile.ZipFile(paths['source-candidate10.zip']) as z:
 assert len(z.namelist())==len(compiled['sourceHashes'])
 for row in compiled['sourceHashes']:
  assert sha(ROOT/'engine'/row['path'])==row['sha256'],row['path']
  assert hashlib.sha256(z.read('engine/'+Path(row['path']).as_posix())).hexdigest()==row['sha256']
for name in ['long-rest-independent-review.json','recovery-abilities-independent-review.json']:
 review=load(paths[name]);review_pins=review.get('sourcePins',review.get('currentPins',[]));assert len(review_pins)>0
 for row in review_pins: assert sha(ROOT/row['path'])==row['sha256'],row['path']
pins=[]
for name,source in paths.items():
 shutil.copyfile(source,OUT/name)
 pins.append({'path':(OUT/name).relative_to(ROOT).as_posix(),'original':source.relative_to(ROOT).as_posix(),'sha256':sha(source)})
summary={
 'status':'BOUNDED_REST_AND_RECOVERY_INITIAL_ASSESSMENT_NOT_MODULE_ACCEPTANCE',
 'previousCheckpointCommit':'dd9a8baeafcec57f92fc7d56f8778fa5514cad35',
 'contractAcceptance':'271baf94-22dd-57cb-a2ab-5f728e989b4d',
 'implemented':[
  'BeginLongRest and InterruptLongRest use their unchanged native guards. Both preserve their early branch before active-rest interruption, Sanctuary, Guidance and physical checks.',
  'UseHealingRite, UseDivineInvocation and UseConsecrate share exact initial guards with execution, including Radiance own-context/cure admission and original resource/action order.',
  '80 newly attached native guard identities match accepted67f3d201b. Existing strings, source eligibility, geometry, current journal/condition modes and actual execution remain unchanged.',
  'Core Invocation payload constraint becomes publicly callable by the trusted Lab adapter; its legacy wrapper and exact validation remain shared. No player DTO, grant, new assembly friend or save change.',
 ],
 'currentNativeInitialAssessmentKinds':['EndSpellConcentration','GroundCastingStrain','FocusDetectedAura','CastKnownSpell',
  'BeginLongRest','InterruptLongRest','UseHealingRite','UseDivineInvocation','UseConsecrate'],
 'sourceInputs':len(compiled['sourceHashes']),
 'sourceArchiveSha256':sha(paths['source-candidate10.zip']),
 'dlls':[{'name':p.name,'sha256':sha(p)} for p in sorted(build.glob('*.dll'))],
 'rawEvidence':pins,
 'actualExits':{'compileAndRest':0,'fourRecoveryChecks':0,'bishopConnectedCampaign':0,'consecrationConnectedScenario':0,'packageValidation':0},
 'currentCandidateChecks':{'newInt05CasePassed':1,'priorInt05CasePassed':1,'existingNamedCasesPassed':5,'totalPassed':7},
 'genuinePaths':[
  'Earned Cleric begins rest at196 after repeated pure reads. Real100seconds then interruption198 releases future occupancy, preserves1RP and unavailable Conviction; both receipts retry without fresh eligibility. Before/pending/interrupted strict restore retained.',
  'Initial Cleric heals genuine injury with2RP, one Action and actual d8; later insufficient-RP pure denial matches native execution. Existing continuation and strict restore retained.',
  'Earned Radiance eligibility is read without healing/drawing/settling; actual paid Rite and conditional additional healing continue and restore.',
  'Actual completed long rest still funds finite resources and permits paid continuation; no predicted recovery is substituted for its actual endpoint.',
  'Actual funded Bishop Invocation reads do not roll, heal, vent, cure or recharge; actual execution reaches two positive recipients and positive cure, then paid Rite/Radiance/Aura continuation.',
  'Actual Consecrate reads do not create terrain or consume RP/Action; actual zone payment, Rite/Ground/Radiance/Aura healing chain and source deadline/recharge still execute.'
 ],
 'limits':[
  'Nine native initial-assessment kinds do not complete78 seat/two operator coverage or public V1 APIs.',
  'CommitFeasibility remains null. Post-resolution validation, capacity outcomes and future healing/cure/ground/recovery are not predicted.',
  'Public descriptions/costs/choices/results/diagnostics/console, planning proof and complete transitive/profile/branch/five-path/regression/privacy qualification remain open.',
  'Two independent reviews are static only; executed reports are separate. Prior accepted module qualification and historical raw failures remain intact.',
  'Actual final GPT runtime acceptance remains open. No successor, Unity integration, storage cleanup or Support action.'
 ],
 'runtimeAccepted':False,'successorStarted':False,'unityIntegration':False,
}
(PACKET/'IMPLEMENTATION_CHECKPOINT_05.json').write_bytes((json.dumps(summary,indent=2)+'\n').encode('utf8'))
print(json.dumps({'currentCandidatePassed':7,'compiledInputs':len(compiled['sourceHashes']),'sourceArchiveSha256':summary['sourceArchiveSha256'],'moduleAccepted':False},indent=2))
