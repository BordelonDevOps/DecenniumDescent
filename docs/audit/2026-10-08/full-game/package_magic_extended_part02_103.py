"""One-shot packaging recovery only; preserve successful review and failed tree."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,zipfile
G=Path(r'C:\Github\DecenniumDescent');A=G/'docs/audit/2026-10-08/full-game'
REPORT=A/'FEAT335_MAGIC_EXTENDED_PART02_CASEBOOK_REVIEW_103.json';ROOT=A/'mx103-package';ZIP=A/'DD_Feat335_Magic_Extended_Part02_103.zip';OUT=A/'FEAT335_MAGIC_EXTENDED_PART02_PACKAGE_RECOVERY_103.json';SAVED=A/Path(__file__).name
for p in (ROOT,ZIP,OUT,SAVED):assert not p.exists(),str(p)
def enc(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':sha(b)}
def put(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(b)
r=json.loads(REPORT.read_text(encoding='utf-8'));original=REPORT.read_bytes()
assert r['failed']==0 and all(x['pass'] for x in r['checks']) and len(r['numericAndStateCalculations'])==31
assert all(x['calculatedResult']==x['expectedResult'] for x in r['numericAndStateCalculations'])
sources={};mapping=[]
for ix,row in enumerate(r['sourceBindings']):
 p=G/row['path'];assert info(p)==row,row['path'];member=f'sources/{ix:02d}_{p.name}';sources[member]=p.read_bytes();mapping.append({'member':member,**row})
failed=A/'feat335-magic-extended-part02-103';failedfiles=sorted(p for p in failed.rglob('*') if p.is_file());failedbindings=[info(p) for p in failedfiles]
ROOT.mkdir();put(ROOT/'REVIEW.json',original);put(ROOT/'SOURCE_MAP.json',enc(mapping))
for member,b in sources.items():put(ROOT/member,b)
put(ROOT/'review_magic_extended_part02_103.py',(A/'review_magic_extended_part02_103.py').read_bytes())
put(ROOT/'package_magic_extended_part02_103.py',Path(__file__).read_bytes())
put(ROOT/'README.txt',b'Complete MX21-40 stated-case review, all31 complete source files mapped to original paths by SOURCE_MAP.json. Original full review completed; initial nested-path packaging failed with Windows WinError206. No successful review program rerun. Original report and partial tree preserved. This packaging-only successor uses short member names with exact byte/hash bindings. No runtime or whole-cohort acceptance. Do not run supplied scripts.\n')
members=sorted(p for p in ROOT.rglob('*') if p.is_file());manifest={'id':'MX103-RECOVERED-PACKAGE-MANIFEST','files':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in members]};put(ROOT/'MANIFEST.json',enc(manifest))
with zipfile.ZipFile(ZIP,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(ROOT.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(ZIP) as z:
 assert len(z.namelist())==len(set(z.namelist()))==len(manifest['files'])+1
 for row in manifest['files']:
  b=z.read(row['path']);assert len(b)==row['bytes'] and sha(b)==row['sha256'],row['path']
 for row in mapping:
  b=z.read(row['member']);assert len(b)==row['bytes'] and sha(b)==row['sha256'] and b==(G/row['path']).read_bytes(),row['path']
 assert z.read('REVIEW.json')==original==REPORT.read_bytes()
assert all(info(G/row['path'])==row for row in failedbindings)
report={'id':'MX103-PACKAGE-RECOVERY','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'COMPLETE_SOURCE_MAPPED_ARCHIVE_VERIFIED','originalFailure':'WinError206 while writing nested preserved source path after all review checks and full report creation; archive was not created.','originalReview':info(REPORT),'originalPartialTree':failed.relative_to(G).as_posix(),'preservedPartialFiles':failedbindings,'failedScript':info(A/'review_magic_extended_part02_103.py'),'archive':info(ZIP),'sourceMap':info(ROOT/'SOURCE_MAP.json'),'sourceFiles':len(mapping),'archiveMembers':len(manifest['files'])+1,'reviewChecks':r['passed'],'reviewFailures':r['failed'],'everyMemberExact':True,'everySourceUnchanged':True,'originalReportUnchanged':True,'successfulProgramsRerun':0,'downloadedScriptsExecuted':0,'runtimeTestsExecuted':0}
put(SAVED,Path(__file__).read_bytes());put(OUT,enc(report))
print(json.dumps({'report':info(REPORT),'recovery':info(OUT),'archive':info(ZIP),'fullSources':len(mapping),'members':len(manifest['files'])+1,'checks':r['passed'],'failed':0},indent=2))
