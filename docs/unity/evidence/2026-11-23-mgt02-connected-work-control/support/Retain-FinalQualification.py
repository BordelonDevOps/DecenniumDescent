from pathlib import Path
import hashlib,json,subprocess,sys,zipfile
repo=Path(__file__).resolve().parents[5];packet=Path(__file__).resolve().parent.parent
art=repo/'engine/artifacts/connected-work-control';full=art/'full-01';build=art/'development-10/run-20261123T200453593Z-83a83fc6'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));h=lambda b:hashlib.sha256(b).hexdigest()
for script,args in [('Verify-FinalSource.py',[str(build)]),('Reconcile-Regression.py',[str(full),str(build)]),('Reconcile-QualifiedRegression.py',[]),('Reconcile-CommandCoverage.py',[str(art)]),('Verify-Forgeries.py',[str(art)])]:
    subprocess.run([sys.executable,str(packet/'support'/script),*args],cwd=repo,check=True)
assert read(art/'final-source-pins.json')['sourceArchiveSha256']=='3236481a62a4b3f28858c56bfba7fdc6bf471b4afee2b5f7f0254427f2603326'
assert read(packet/'DEVELOPMENT_CHECKPOINT_03.json')['build']['runtimeSourceInputsEqualDevelopment08']==365
raw=read(full/'REGRESSION_RECONCILIATION.json')
regr=read(full/'QUALIFIED_REGRESSION_RECONCILIATION.json');assert regr['status']=='PASS_WITH_REVIEWED_SINGLE_CASE_RECHECK' and regr['reconciledPassed']==1601 and not regr['unresolvedCases']
exits=read(art/'FINAL_PROCESS_EXITS.json');assert len(exits['workers'])==4
assert {x['worker'] for x in exits['workers']}=={0,1,2,3} and all(x['observedExitCode']==(1 if x['worker']==2 else 0) for x in exits['workers'])
for key,session_id,artifact in [('compatibility',32283,'compatibility-04/execution.json'),('consoleBranches',16544,'console-branches-01/result.json')]:
    observed=exits[key]
    assert observed['sessionId']==session_id and observed['observedExitCode']==0
    assert observed['artifact']==artifact and observed['artifactSha256']==h((art/artifact).read_bytes())
compat_execution=read(art/'compatibility-04/execution.json')
assert compat_execution['status']=='PASS'
assert {a['path'].replace('\\','/').rsplit('/',1)[-1]:a['sha256'] for a in compat_execution['assemblyHashes']}==regr['assemblyHashes']
compat=read(art/'compatibility-04/result.json');assert compat['status']=='PASS' and len(compat['cases'])==22
assert {x['wire'] for x in compat['cases']}==set(range(95,117))
assert all(x['canonicalEqual'] and x['continuedReplay'] and x['rejectedByWorkControl'] and x['strictRestoredObservationsEqual'] for x in compat['cases'])
comparison=read(art/'five-paths-02/comparison.json');assert comparison['status']=='PASS' and comparison['crossPathComparisons']==4256 and not comparison['mismatches']
observed_processes=read(art/'OBSERVED_PROCESS_EXITS.json')['completed']
assert len({p['name'] for p in observed_processes})==len(observed_processes)
observed_by_name={p['name']:p for p in observed_processes}
path_processes={'TypedUninterrupted':('fivepaths02-typed',13319),'TypedRestored':('fivepaths02-typed-restored',82915),'ConsoleUninterrupted':('fivepaths02-console',40832),'ConsoleRestored':('fivepaths02-console-restored',50432),'ReceiptReplay':('fivepaths02-receipt',36217)}
for mode in ['TypedUninterrupted','TypedRestored','ConsoleUninterrupted','ConsoleRestored','ReceiptReplay']:
    r=read(art/'five-paths-02'/mode/'result.json');assert r['status']=='PASS' and r['commands']==244 and r['checkpoints']==28
    assert {x['name']:x['sha256'] for x in r['assemblyHashes']}==regr['assemblyHashes']
    assert r['consoleSha256']==h((repo/'engine/tools/Open-ConnectedExpedition.ps1').read_bytes())
    process_name,session_id=path_processes[mode];observed=observed_by_name[process_name]
    assert observed['sessionId']==session_id and observed['observedExitCode']==0
    assert observed['artifact']==f'five-paths-02/{mode}/result.json'
    assert observed['artifactSha256']==h((art/observed['artifact']).read_bytes())
files=[]
for directory in [full]:
    files.extend(p for p in directory.rglob('*') if p.is_file())
files.extend(art/name for name in ['FINAL_PROCESS_EXITS.json','OBSERVED_PROCESS_EXITS.json','command-coverage.json','final-source-pins.json','final-work-ledger-counts.json','forgeries-reconciled.json'])
archive=packet/'FINAL_QUALIFICATION_05.zip';assert not archive.exists(),'Never overwrite retained final qualification'
members=[]
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(set(files)):
        data=p.read_bytes();name=p.relative_to(repo).as_posix();z.writestr(name,data);members.append({'path':name,'bytes':len(data),'sha256':h(data)})
assert archive.stat().st_size<95000000,'Split evidence before publishing an oversized Git blob'
with zipfile.ZipFile(archive) as z:
    for m in members:assert h(z.read(m['path']))==m['sha256']
index={'archive':archive.name,'bytes':archive.stat().st_size,'sha256':h(archive.read_bytes()),'memberCount':len(members),'members':members}
(packet/'FINAL_QUALIFICATION_05_INDEX.json').write_bytes((json.dumps(index,indent=2)+'\n').encode())
(packet/'FINAL_RAW_REGRESSION_RECONCILIATION.json').write_bytes((json.dumps(raw,indent=2)+'\n').encode())
(packet/'FINAL_REGRESSION_RECONCILIATION.json').write_bytes((json.dumps(regr,indent=2)+'\n').encode())
criteria={
 'WC-A1':['GPT_SOURCE_API_ACCEPTANCE.json','SOURCE_API_CONTRACT.md','SOURCE_BINDINGS.json'],
 'WC-A2':['command-coverage.json:16included kinds;9console branches/50commands','five-paths-02:five full paths; typed/console/native query/discovery/work parity'],
 'WC-A3':['checkpoint03 principal fresh244-command lineage; actualdose1 heals5, earlierwasted dose0preserved','five-paths-02 finalexactcanonical matches genuineprincipal'],
 'WC-A4':['checkpoint03 branches-01:eight lifecycle branches48commands30restorepairs','checkpoint03 pending-model-01:four MODEL_ONLY cases; no genuinehostpending closure','terminal-retries-02:cancellation/qualityonceonly'],
 'WC-A5':['principal-work-01:Hero movement whileCompanionfill; active-worker magicdenied; pause/Guidance/resume60productive seconds','five-paths-02 orderedviews+RNG'],
 'WC-A6':['finitewater0.5; recipe4learned,actualblood/ingredients,packaging/doses; nativeage/stabilization boundaries','cancelbranches zero/positive distinctsettlement; finalworkledgercaps retained'],
 'WC-A7':['host-negative-03 exact25codes; terminal-retries-02; post-salecurrentownershipbeforeduplicate','full1601 includes actual32fill/128booking limits and labelledmechanical128reservations','filtered four-seat/bothactor observations and ordereddiscovery'],
 'WC-A8':['five-paths-02 strictrestore at28checkpoints; lifecycle30restorepairs','MODEL_ONLY duechecks withtruthfulownpolicy','forgeries-reconciled14 checksumvalid rejectionassertions inclvalid-decode InvalidSharedWorldReplay','backup237->244 withdisplacedprimarypreserved','compatibility-04 originalprofiles95–116 actualcontinuation andaccepted/current strict-restored observations'],
 'WC-A9':['five-paths-02 all5 complete244commands;4256exactcomparisons/0mismatches','console-branches-01 genuinebranchparents preserved'],
 'WC-A10':['frozen10 C#9warnings-as-errors486inputs/staticPASS','Raw full1601=1600PASS/1FAIL; actual worker exits0,0,1,0 retained. Actual GPT-reviewed exactsameDLL singlecase recheck gives1601 reconciled unique passing cases=1592predecessors+9new; no missingnames','final-source-pins:acceptedcontract/rules preserved','DEVELOPMENT_CHECKPOINT_03.json.build.runtimeSourceInputsEqualDevelopment08:365runtimeinputs stable08->10','FINAL_RUNTIME_REVIEW_PENDING']}
candidate={'status':'QUALIFIED_CANDIDATE_AWAITING_ACTUAL_GPT_FINAL_REVIEW','module':'MGT-02-CONNECTED-WORK-CONTROL','runtimeCommit':'748c6debca56fd7d1a8b89e8b2ad7de12e8da5eb','frozenBuild':build.relative_to(repo).as_posix(),'sourceArchiveSha256':'3236481a62a4b3f28858c56bfba7fdc6bf471b4afee2b5f7f0254427f2603326','compiledInputs':486,'tests':{'raw':{'total':1601,'passed':1600,'failed':1,'status':'FAIL'},'reconciled':{'status':regr['status'],'uniquePassingCases':1601,'reviewResponseId':regr['actualReviewResponseId']},'preservedPredecessors':1592,'newCases':regr['newCases']},'fivePaths':comparison,'compatibilityProfiles':22,'commandCoverage':read(art/'command-coverage.json'),'criteriaEvidence':criteria,'priorEvidence':'DEVELOPMENT_CHECKPOINT_03.zip SHA2568b8909e1fa3151e55f02c9a7134a337abde18f261d27089f922ee5545d7b651c retains frozen10 source/DLLs, genuine lineage/branches/model/negative/backup/forgery evidence and all corrected failures; checkpoints01/02 preserve earlier implementation failures and review resolutions','supplement04':{'archive':'QUALIFICATION_SUPPLEMENT_04.zip','sha256':'42a77c5eb41c23aa3326270b8b292dc388d4cd0c440e1cee0f6f8379c904e31a','contents':'Finalfrozen10 fivepaths, all16 consolecommands,22compatibility, rawIOfailure/recheck/triage'},'newArchive':{k:v for k,v in index.items() if k!='members'},'actualCheckpoint03Review':'5d95cccf-254c-5eca-8c13-5197e4acd0ac','runtimeAccepted':False,'genuineHostPendingChecks':'UNPROVED_REQUIRED_FOR_BROADER_ENGINE_COMPLETION','wholeWorkstreamComplete':False,'performanceQualified':False,'unityQualified':False,'successorAuthorized':False}
(packet/'FINAL_REVIEW_CANDIDATE.json').write_bytes((json.dumps(candidate,indent=2)+'\n').encode())
print(json.dumps(candidate['newArchive']))
