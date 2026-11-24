"""Retain the actual spell assessment candidate and its bounded qualification."""
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

PACKET=Path(__file__).resolve().parents[1]; ROOT=PACKET.parents[3]
ARTIFACTS=ROOT/'engine/artifacts/admitted-command-surface'; OUT=PACKET/'runtime-checkpoint-04'
OUT.mkdir(exist_ok=True)

def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

run=ARTIFACTS/'development-09'; build=run/'run-20261124T035309737Z-da766549'
spell=run/'spells'; bishop=run/'bishop/chr03_bishop_connected_earned_funded_cure_aura_dispel_continue'
paths={
 'candidate09-casting.json':build/'results.json',
 'candidate09-spells.json':spell/'results.json',
 'candidate09-bishop.json':run/'bishop/results.json',
 'candidate09-package.json':run/'static-20261124T035435896Z-d0747328/results.json',
 'independent-review.json':ARTIFACTS/'spell-cast-assessment-cross-review-01.json',
 'source-candidate09.zip':build/'source-frozen.zip',
 'cast-assessment-facts.json':build/'saves/int05-cast-assessment-facts.json',
 'int05-cast-before.ddsave':build/'saves/int05-cast-before.ddsave',
 'int05-cast-after.ddsave':build/'saves/int05-cast-after.ddsave',
 'spare-before.ddsave':spell/'tac08_genuine_spare_stabilizes_actual_combat_patient/tac08-spare-before-cast.ddsave',
 'spare-stable.ddsave':spell/'tac08_genuine_spare_stabilizes_actual_combat_patient/tac08-spare-stable-patient.ddsave',
 'purify-before.ddsave':spell/'tac08_genuine_purify_finite_water_and_measured_intake/tac08-before-purify.ddsave',
 'purify-after.ddsave':spell/'tac08_genuine_purify_finite_water_and_measured_intake/tac08-purified-water.ddsave',
 'purified-water-consumed.ddsave':spell/'tac08_genuine_purify_finite_water_and_measured_intake/tac08-purified-water-consumed.ddsave',
 'earned-aura-after.ddsave':spell/'int05_genuine_aura_focus_assessment_ordinary_context/int05-focus-after.ddsave',
 'bishop-guidance-detect.ddsave':bishop/'guidance-detect.ddsave',
 'bishop-guidance-dispelled.ddsave':bishop/'guidance-dispelled.ddsave',
 'bishop-continued.ddsave':bishop/'continued.ddsave',
 'bishop-connected-facts.json':bishop/'bishop-connected-facts.json',
}
compiled=load(paths['candidate09-casting.json'])
assert compiled['status']=='PASS' and compiled['passed']==1 and compiled['testsDiscovered']==1
for name,count in [('candidate09-spells.json',5),('candidate09-bishop.json',1)]:
 report=load(paths[name]);assert report['status']=='PASS' and len(report['cases'])==count and all(c['Passed'] for c in report['cases'])
assert load(paths['candidate09-package.json'])['status']=='PASS'
with zipfile.ZipFile(paths['source-candidate09.zip']) as z:
 assert len(z.namelist())==len(compiled['sourceHashes'])
 for row in compiled['sourceHashes']:
  assert sha(ROOT/'engine'/row['path'])==row['sha256'],row['path']
  assert hashlib.sha256(z.read('engine/'+Path(row['path']).as_posix())).hexdigest()==row['sha256']
review=load(paths['independent-review.json']);assert len(review['sourcePins'])>0
for row in review['sourcePins']: assert sha(ROOT/row['path'])==row['sha256'],row['path']
pins=[]
for name,source in paths.items():
 shutil.copyfile(source,OUT/name)
 pins.append({'path':(OUT/name).relative_to(ROOT).as_posix(),'original':source.relative_to(ROOT).as_posix(),'sha256':sha(source)})
summary={
 'status':'BOUNDED_SPELL_INITIAL_ASSESSMENT_CHECKPOINT_NOT_MODULE_ACCEPTANCE',
 'previousCheckpointCommit':'589fe8601a09cd7f8f671a4b3064e9189de08033',
 'contractAcceptance':'271baf94-22dd-57cb-a2ab-5f728e989b4d',
 'implemented':[
  'CastKnownSpell initial assessment shares the unchanged native repertoire, source acquisition, components, target, finite RP, strain and history guards with actual execution.',
  'Purify follows actual retained lot, vessel and physical placement; Bishop Dispel requires its current opaque aura and actual own prior Guidance provenance.',
  'All37 newly attached exact native guard coordinates refer to accepted67f3d201b. Existing native string adapters and ordering are preserved.',
  'Repeated owning reads do not execute effects, spend resources, advance time or draw stabilization dice; exact retries retain the original admission receipt distinction.'
 ],
 'currentNativeInitialAssessmentKinds':['EndSpellConcentration','GroundCastingStrain','FocusDetectedAura','CastKnownSpell'],
 'sourceInputs':len(compiled['sourceHashes']),
 'sourceArchiveSha256':sha(paths['source-candidate09.zip']),
 'dlls':[{'name':p.name,'sha256':sha(p)} for p in sorted(build.glob('*.dll'))],
 'rawEvidence':pins,
 'actualExits':{'compileAndCasting':0,'fiveSpellChecks':0,'bishopConnectedCampaign':0,'packageValidation':0},
 'currentCandidateChecks':{'newInt05CasePassed':1,'priorInt05CasePassed':1,'existingNamedCasesPassed':5,'totalPassed':7},
 'genuinePaths':[
  'Nine source/component/target denials agree with actual rejection and preserve bytes. Actual Sanctuary pays2RP and one Action once; save/restore and retry preserve the effect.',
  'Earned ordinary Guidance/Detect casts expose a real aura; the existing paid focus remains unchanged.',
  'An actual combat patient reaches dying; Spare pure assessment draws no dice; execution stabilizes with exactly the existing recovery d4 and authenticated replay.',
  'Actual Purify removes contamination from the same finite pint without creating stock, then continues through combat, pickup, measured consumption and restore.',
  'Actual earned/funded Bishop campaign reaches own Guidance/Detect; Dispel pure assessment precedes the actual paid effect ending, then retry and travel continuation.'
 ],
 'limits':[
  'Four native initial-assessment kinds do not complete the approved78 seat/two operator inventory.',
  'CommitFeasibility remains null. Shared post-resolution consequences and terminal validation are not predicted or certified.',
  'Complete public action/choice/result/cost/diagnostic/console surfaces, owning planning proof and remaining native paths are still open.',
  'Full accepted profile/branch/five-path/privacy/regression and actual GPT final runtime acceptance are still open; no successor or Unity work started.',
  'The independent review is static. The separate raw reports retain actual execution results. Prior accepted qualification is preserved, not restarted.'
 ],
 'runtimeAccepted':False,'successorStarted':False,'unityIntegration':False,
}
(PACKET/'IMPLEMENTATION_CHECKPOINT_04.json').write_bytes((json.dumps(summary,indent=2)+'\n').encode('utf8'))
print(json.dumps({'currentCandidatePassed':7,'compiledInputs':len(compiled['sourceHashes']),'sourceArchiveSha256':summary['sourceArchiveSha256'],'moduleAccepted':False},indent=2))
