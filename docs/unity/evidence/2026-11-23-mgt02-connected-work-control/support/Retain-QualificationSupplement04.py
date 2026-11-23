from pathlib import Path
import hashlib,json,zipfile
repo=Path(__file__).resolve().parents[5];packet=Path(__file__).resolve().parent.parent;art=repo/'engine/artifacts/connected-work-control'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));h=lambda b:hashlib.sha256(b).hexdigest()
comparison=read(art/'five-paths-02/comparison.json');coverage=read(art/'command-coverage.json');compat=read(art/'compatibility-04/result.json');triage=read(art/'fill-cap-io-triage-01/result.json')
assert comparison['status']=='PASS' and comparison['crossPathComparisons']==4256 and not comparison['mismatches']
assert coverage['status'].startswith('PASS16_') and coverage['branchCommands']==50
assert compat['status']=='PASS' and len(compat['cases'])==22 and {x['wire'] for x in compat['cases']}==set(range(95,117))
assert triage['status']=='PASS_BOUNDED_TRIAGE' and not triage['failedCase']['Passed']
assert read(art/'fill-cap-io-recheck-01/results.json')['passed']==1
folders=[art/'five-paths-02',art/'console-branches-01',art/'compatibility-04',art/'fill-cap-io-recheck-01',art/'fill-cap-io-triage-01',art/'full-01/worker2/cases/mgt02_work_control_native_fill_record_and_booking_caps']
files=[p for folder in folders for p in folder.rglob('*') if p.is_file()]
files.extend(art/n for n in ['command-coverage.json','final-source-pins.json','source-pins-independent-review.json','OBSERVED_PROCESS_EXITS.json','final-work-ledger-counts.json'])
archive=packet/'QUALIFICATION_SUPPLEMENT_04.zip';assert not archive.exists(),'Never overwrite retained evidence'
members=[]
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(set(files)):
  data=p.read_bytes();name=p.relative_to(repo).as_posix();z.writestr(name,data);members.append({'path':name,'bytes':len(data),'sha256':h(data)})
with zipfile.ZipFile(archive) as z:
 for m in members:assert h(z.read(m['path']))==m['sha256']
index={'archive':archive.name,'bytes':archive.stat().st_size,'sha256':h(archive.read_bytes()),'memberCount':len(members),'members':members}
(packet/'QUALIFICATION_SUPPLEMENT_04_INDEX.json').write_bytes((json.dumps(index,indent=2)+'\n').encode())
report={'status':'COMPLETED_NONREGRESSION_EVIDENCE_WITH_ONE_RAW_REGRESSION_IO_FAILURE_UNDER_REVIEW','module':'MGT-02-CONNECTED-WORK-CONTROL','runtimeCommit':'748c6debca56fd7d1a8b89e8b2ad7de12e8da5eb','frozenBuild':'development-10/run-20261123T200453593Z-83a83fc6','compiledInputs':486,'sourceArchiveSha256':'3236481a62a4b3f28858c56bfba7fdc6bf471b4afee2b5f7f0254427f2603326','actualGptCheckpoint03Response':'5d95cccf-254c-5eca-8c13-5197e4acd0ac','fivePaths':comparison,'commandCoverage':coverage,'compatibility':compat,'ioFailureTriage':triage,'ioFailureDisposition':'PROPOSED_SINGLE_CASE_RECONCILIATION_REQUIRES_ACTUAL_GPT_AGREEMENT; raw case/worker failures must stay FAIL; no assertion of OS cause or broad persistence fix','remaining':['Full1601 raw regression completion and actual terminal results','Actual GPT disposition of exactsameDLL isolated fill-cap recheck versus retained File.Replace failure','Final transparent regression/source/evidence reconciliation and actual module review/concurrence'],'evidenceArchive':{k:v for k,v in index.items() if k!='members'},'runtimeAccepted':False,'successorAuthorized':False,'unityAuthorized':False}
(packet/'QUALIFICATION_SUPPLEMENT_04.json').write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report['evidenceArchive']))
