from pathlib import Path
import hashlib,json,zipfile
root=Path(__file__).resolve().parents[5]; packet=Path(__file__).resolve().parent.parent
art=root/'engine/artifacts/connected-work-control'; h=lambda b:hashlib.sha256(b).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
b08=art/'development-08/run-20261123T193756369Z-c92813b1';b10=art/'development-10/run-20261123T200453593Z-83a83fc6'
runtime=lambda p:{x['path'].replace('\\','/'):x['sha256'] for x in read(p/'results.json')['sourceHashes'] if '/Tests/' not in x['path'].replace('\\','/')}
assert runtime(b08)==runtime(b10)
assert read(art/'focused-04/results.json')['passed']==64
assert read(art/'pending-model-01/results.json')['passed']==4
comparison=read(art/'five-paths-01/comparison.json');assert comparison['status']=='PASS' and comparison['crossPathComparisons']==4256
branches=[read(p/'results.json') for p in sorted((art/'branches-01').iterdir()) if p.is_dir()]
assert len(branches)==8 and all(x['status']=='PASS' for x in branches)
assert sum(x['commands'] for x in branches)==48 and sum(x['strictRestorePairs'] for x in branches)==30
assert read(art/'host-negative-03/verified-exact-codes.json')['status']=='PASS'
assert read(art/'terminal-retries-02/result.json')['status']=='PASS'
assert len(read(art/'forgeries-reconciled.json')['cases'])==14
runs=['development-08','development-09','development-10','focused-04','pending-model-01',
 'principal-prefix-01','principal-prefix-02','principal-dose-01','principal-dose-02','principal-dose-03',
 'principal-fight-01','principal-work-01','five-paths-01','branches-01','host-negative-01','host-negative-02',
 'host-negative-03','terminal-retries-01','terminal-retries-02','forgeries-01','forgeries-02','forgeries-03',
 'forgeries-04','forgeries-05','old-view-baseline-01','compatibility-01','compatibility-02','compatibility-03',
 'static-20261123T200556036Z-bb0bc664']
files=sorted(p for run in runs for p in (art/run).rglob('*') if p.is_file())+[art/'forgeries-reconciled.json',art/'final-work-ledger-counts.json',root/'engine/tools/Open-ConnectedExpedition.ps1']
assert all(p.exists() for p in files)
members=[];archive=packet/'DEVELOPMENT_CHECKPOINT_03.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files:
  data=p.read_bytes();name=p.relative_to(root).as_posix();z.writestr(name,data);members.append({'path':name,'bytes':len(data),'sha256':h(data)})
with zipfile.ZipFile(archive) as z:
 for m in members:assert h(z.read(m['path']))==m['sha256']
index={'archive':archive.name,'bytes':archive.stat().st_size,'sha256':h(archive.read_bytes()),'memberCount':len(members),'members':members}
(packet/'DEVELOPMENT_CHECKPOINT_03_INDEX.json').write_text(json.dumps(index,indent=2)+'\n',encoding='utf-8')
report={'status':'PARTIAL_QUALIFICATION_CHECKPOINT_NOT_MODULE_ACCEPTANCE','module':'MGT-02-CONNECTED-WORK-CONTROL',
 'previousPublishedHead':'98fc5fbcc08a753f6d60aad0a04397f4f6d235ca','gptCheckpoint02Response':'754171b9-5367-5e66-a308-1334c4b6bddc',
 'contractSha256':'d65c7bcdf6c9ade960e70b527c82d71c367e4f883d180d91f0b299c8e13d8819',
 'runtimeChange':'New-profile-only Haven sale/meal query grant now matches existing narrow submission grant; no other runtime changes since98fc.',
 'build':{'sourceRun':str(b10.relative_to(root)),'compiledInputs':486,'newCases':9,'totalDiscovered':1601,'sourceArchiveSha256':h((b10/'source-snapshot.zip').read_bytes()),'static':'PASS',
   'runtimeSourceInputsEqualDevelopment08':len(runtime(b10)),'qualificationAt08':'64 selected PASS;5 complete244-command paths,28 checkpoints,4256 exact comparisons',
   'qualificationAt10':'4 allocated pending-check cases PASS;25 exact host-negative outcomes,3 terminal receipt retries,backup237->244,14 reconciled forged-save rejections',
   'fullRegression':'RUNNING_NOT_PASS','finalBuildFivePaths':'RUNNING_NOT_PASS','authenticCompatibility95To116':'RUNNING_NOT_PASS'},
 'principal':{'freshSelectedGenesis':True,'finalRevision':244,'finalSave':'engine/artifacts/connected-work-control/principal-work-01/final.ddsave','finalSha256':h((art/'principal-work-01/final.ddsave').read_bytes()),
   'actualSequence':['Explore and mine real finite material','Encounter/acquire blood,notes,charter;real sale/meal','Research recipe4 in existing absolute windows','Manufacture actual batch and resolve actual AwaitingChoice','Use resulting dose1:Hero21->26HP;retain earlier valid wasted dose0','Finish real encounter','Companion fills;Hero moves;active-worker magic denied;pause/Guidance/resume60productive seconds','Complete finite0.5-pint transfer and continue walking'],
   'counts':{'receipts':244,'lots':25,'bookings':31,'reservations':17},'workFamilyCapInventory':read(art/'final-work-ledger-counts.json')},
 'branches':{'count':8,'committedCommands':48,'strictRestorePairs':30,'cases':[x['case'] for x in branches]},
 'privacy':'Retained first five-path set:168 foreign-seat work observations disabled/empty; mining hidden at tactical checkpoints117/128/129/136/138. Independent evidence inspection, not a new host capability.',
 'pendingAllocation':'Four MODEL_ONLY cases: mining explicit/native advance and existing research/manufacturing due-check fixtures. All3 genuine host producers UNPROVED_REQUIRED_FOR_BROADER_ENGINE_COMPLETION.',
 'forgeries':'14 executed cases reconciled from11+2+1 before/after retained harness failures; all recomputed checksums and unchanged live state, including valid-decode shortened-labor rejection by policy replay. No claim failed driver processes passed.',
 'retainedCorrections':['Initial principal sale query exposed narrow grant mismatch; fixed with actual regression','Carried-vial route proposal rejected; selected profile uses existing worksite dose access','First actual dose healed0 on full-HP companion; retainedspent and later dose healsHero5',
 'New model test compile used nonexistent seed parameter; corrected to explicit SharedCombatFixture seed','Host-negative01/02 wrongly expected successful retry after actual sale; corrected current-authority denial and genuine pre-sale duplicate witness; fill worker property corrected',
 'Terminal retry01 used PowerShell automatic input variable; corrected caseSpec','Forgery root occurs twice: exact header offset; Harvest codec arity/empty generic material collection and immutable blood constructor corrected to exact negative-only blood-origin bytes',
 'Compatibility01/02 compared raw replay insertion order with canonical restored order; corrected to ordered strict-restored observations, retained raw observations; compatibility03 reused a capture filename across distinct profiles, corrected unique transient capture paths'],
 'remaining':['Full frozen1601 regression and observed four terminal results','Five full paths on frozen10 and exact comparisons','Authentic95–116 original-profile continuation and accepted-runtime ordered strict-restored observations','Final evidence/source reconciliation, actual GPT runtime review and concurrence'],
 'evidenceArchive':{k:v for k,v in index.items() if k!='members'},'runtimeAccepted':False,'successorAuthorized':False,'unityAuthorized':False}
(packet/'DEVELOPMENT_CHECKPOINT_03.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report['evidenceArchive']))
