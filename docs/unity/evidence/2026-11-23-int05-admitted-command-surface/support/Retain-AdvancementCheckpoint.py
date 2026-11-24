"""Retain advancement initial-assessment evidence, not module acceptance."""
import hashlib,json,shutil,zipfile
from pathlib import Path
PACKET=Path(__file__).resolve().parents[1];ROOT=PACKET.parents[3]
ARTIFACTS=ROOT/'engine/artifacts/admitted-command-surface';OUT=PACKET/'runtime-checkpoint-09'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
run=ARTIFACTS/'development-15';build=run/'run-20261124T052126992Z-88f695a0'
cleric=run/'advancement/chr03_primary_genuine_earned_settlement'
bishop=run/'bishop/chr03_bishop_connected_earned_funded_cure_aura_dispel_continue'
paths={
 'candidate15-initial.json':build/'results.json',
 'candidate15-advancement.json':run/'advancement/results.json',
 'candidate15-bishop.json':run/'bishop/results.json',
 'candidate15-package.json':run/'static-20261124T052235224Z-349b2a59/results.json',
 'source-candidate15.zip':build/'source-frozen.zip',
 'source-independent-review.json':ARTIFACTS/'advancement-source-cross-review-01.json',
 'routing-independent-review.json':ARTIFACTS/'advancement-routing-cross-review-01.json',
 'native-soldier-advanced.ddsave':build/'saves/int05-native-soldier-advanced.ddsave',
 'cleric-objective.ddsave':cleric/'cleric-objective.ddsave',
 'cleric-awarded.ddsave':cleric/'cleric-awarded.ddsave',
 'cleric-advanced.ddsave':cleric/'cleric-advanced.ddsave',
 'cleric-continued.ddsave':cleric/'cleric-primary-continued.ddsave',
 'bishop-departure.ddsave':bishop/'departure-complete.ddsave',
 'bishop-earned3.ddsave':bishop/'earned3.ddsave',
}
compiled=load(paths['candidate15-initial.json']);assert compiled['status']=='PASS' and compiled['passed']==1 and compiled['testsDiscovered']==1
for name,count in [('candidate15-advancement.json',4),('candidate15-bishop.json',1)]:
 r=load(paths[name]);assert r['status']=='PASS' and len(r['cases'])==count and all(x['Passed'] for x in r['cases'])
assert load(paths['candidate15-package.json'])['status']=='PASS'
with zipfile.ZipFile(paths['source-candidate15.zip']) as z:
 assert len(z.namelist())==len(compiled['sourceHashes'])
 for row in compiled['sourceHashes']:
  assert sha(ROOT/'engine'/row['path'])==row['sha256'],row['path']
  assert hashlib.sha256(z.read('engine/'+Path(row['path']).as_posix())).hexdigest()==row['sha256']
for name in ['source-independent-review.json','routing-independent-review.json']:
 r=load(paths[name]);assert r['sourcePins']
 for row in r['sourcePins']:assert sha(ROOT/row['path'])==row.get('sha256',row.get('currentSha256')),row['path']
OUT.mkdir(exist_ok=True);pins=[]
for name,source in paths.items():
 shutil.copyfile(source,OUT/name);pins.append({'path':(OUT/name).relative_to(ROOT).as_posix(),'original':source.relative_to(ROOT).as_posix(),'sha256':sha(source)})
previous=load(PACKET/'IMPLEMENTATION_CHECKPOINT_08.json')
summary={
 'status':'BOUNDED_ADVANCEMENT_INITIAL_ASSESSMENT_NOT_MODULE_ACCEPTANCE',
 'previousCheckpointCommit':'73c87084dda44bc59a4316fd6230b07a3471955f',
 'contractAcceptance':'271baf94-22dd-57cb-a2ab-5f728e989b4d',
 'implemented':[
  'AwardCharacterMilestone and AdvanceCharacterLevel share exact Cleric2 and Bishop3 prerequisites with actual execution, including actual objective/departure, unconsumed award, class/card/source choices and existing resource bases.',
  'Native fallback shares existing Soldier prerequisites and current HP/runtime bases. The read path constructs no future level, character, progression record or execution carrier and does not compute future HP. Existing native execution retains its original future-capacity calculations.',
  'Haven meal and route-travel outer guards are shared at original dispatch positions. Common care/recovery prefix remains bounded to stabilization and advancement; no universal reordering.',
  'Actual connected Cleric/Bishop award and advancement perform repeated pure assessments before unchanged transactions. No grant or profile is widened.'
 ],
 'currentNativeInitialAssessmentKinds':previous['currentNativeInitialAssessmentKinds']+['AwardCharacterMilestone','AdvanceCharacterLevel'],
 'sourceInputs':len(compiled['sourceHashes']),'sourceArchiveSha256':sha(paths['source-candidate15.zip']),
 'dlls':[{'name':p.name,'sha256':sha(p)} for p in sorted(build.glob('*.dll'))],'rawEvidence':pins,
 'actualExits':{'compileAndInitial':0,'fourAdvancementChecks':0,'bishopCampaign':0,'packageValidation':0},
 'currentCandidateChecks':{'newInt05CasePassed':1,'priorInt05CasePassed':1,'existingNamedCasesPassed':4,'totalPassed':6},
 'genuinePaths':[
  'Four authentic factory advancement denials match actual unchanged execution; existing native Soldier fixture separately checks pure reads followed by actual award/advancement and strict restore, without claiming admission to a connected profile.',
  'Cleric objective completion, separate award, exact earned settlement, preserved current HP/resources and actual continuation remain qualified by the existing connected scenario.',
  'Bishop actual departure and award precede exact earned3 transaction; funded healing, cure, spell and continuation scenario still passes.',
  'Existing Soldier fixed-average and level4 Constitution ASI checks retain current health, prior dice and historical compatibility. Prior stabilization outer-order denials remain passing.'
 ],
 'limits':[
  'Twenty native initial kinds do not complete78 seat/two operator coverage or any complete public V1 surface.',
  'CommitFeasibility remains null. No future progression, healing, pool funding, outcome or terminal validation is certified by assessment.',
  'Two independent reviews are static only; actual reports are separate. Complete profile/branch/privacy/transitive/five-path/regression qualification, public APIs, console and planning proof remain open.',
  'Actual final GPT runtime acceptance and accepted push remain open. Finish INT05 only, then stop; no successor, Unity, storage or Support work.'
 ],
 'runtimeAccepted':False,'successorStarted':False,'unityIntegration':False
}
(PACKET/'IMPLEMENTATION_CHECKPOINT_09.json').write_bytes((json.dumps(summary,indent=2)+'\n').encode())
print(json.dumps({'checksPassed':6,'sourceInputs':len(compiled['sourceHashes']),'moduleAccepted':False}))
