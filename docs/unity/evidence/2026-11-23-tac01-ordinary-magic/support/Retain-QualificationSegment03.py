"""Retain completed evidence, original failed controls, and the superseded partial run."""
from pathlib import Path
import hashlib, json, zipfile

repo=Path('.').resolve()
base=repo/'engine/artifacts/ordinary-magic-qualification'
packet=repo/'docs/unity/evidence/2026-11-23-tac01-ordinary-magic'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda b:hashlib.sha256(b).hexdigest()
required={
 'candidate-02/compatibility-01/result.json':'PASS',
 'candidate-02/boundaries-02/result.json':'PASS',
 'candidate-02/producer-ties-03/result.json':'PASS',
 'candidate-02/pending-02/result.json':'PASS',
 'candidate-02/partition-01/comparison.json':'PASS',
 'candidate-02/five-paths-01/comparison.json':'PASS',
 'candidate-02/carried-outside-02/result.json':'PASS',
 'candidate-02/work-timing-01/cleric-01/result.json':'PASS',
 'candidate-01/compatibility-01/result.json':'PASS',
 'candidate-01/SUPERSEDED_RUN_DISPOSITION.json':'INTERRUPTED_SUPERSEDED_BY_FINAL_CANDIDATE02',
}
for rel,status in required.items():
    assert read(base/rel)['status']==status, rel
folders01=['authentic-legacy','compatibility-01','worker-0','worker-1','worker-2','worker-3']
folders02=['acceptance-inventory','boundaries-01','boundaries-02','capacity-01','capacity-focus-01',
 'carried-outside-01','carried-outside-02','compatibility-01','consumers','controls-01','controls-02','controls-03',
 'five-paths-01','forgery-01','incapacity-01','incapacity-02','incapacity-03','partition-01',
 'pending-01','pending-02','producer-ties-01','producer-ties-02','producer-ties-03','revocation-01',
 'tactical-discovery','work-timing-01']
files=[]
for candidate,folders in [('candidate-01',folders01),('candidate-02',folders02)]:
    for folder in folders:
        directory=base/candidate/folder
        assert directory.is_dir(),directory
        files.extend(p for p in directory.rglob('*') if p.is_file())
files.extend([base/'candidate-01/SUPERSEDED_RUN_DISPOSITION.json',base/'candidate-02/CURRENT_SOURCE_RECONCILIATION.json',base/'candidate-02/parent-facts.json'])
static=repo/'engine/artifacts/static-20261123T161129770Z-1999ee6e'
assert read(static/'results.json')['status']=='PASS'
files.extend(p for p in static.rglob('*') if p.is_file())
files=sorted(set(files),key=lambda p:p.relative_to(repo).as_posix())
archive=packet/'QUALIFICATION_SEGMENT_03.zip'
assert not archive.exists(),'Never overwrite retained evidence'
members=[]
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for path in files:
        content=path.read_bytes();name=path.relative_to(repo).as_posix()
        z.writestr(name,content)
        members.append({'member':name,'bytes':len(content),'sha256':sha(content)})
with zipfile.ZipFile(archive) as z:
    assert len(z.namelist())==len(members)
    for m in members:
        content=z.read(m['member']);assert len(content)==m['bytes'] and sha(content)==m['sha256']
index={'status':'RETAINED_AND_EVERY_MEMBER_REVERIFIED','archive':archive.name,'bytes':archive.stat().st_size,
 'sha256':sha(archive.read_bytes()),'memberCount':len(members),'members':members,
 'requiredTerminalResults':required,
 'runtimeSourceBinding':'QUALIFICATION_CANDIDATE_02.json; exact four DLLs and481 input files already retained in DEVELOPMENT_EVIDENCE_02.zip. Individual new runs retain actual input/DLL hashes.',
 'excludedRunningQualification':'candidate-02/worker-0..3 still running; no final regression pass or module acceptance claimed.',
 'supersededQualification':'candidate-01 worker reports are last actual partial outputs; separate explicit interruption disposition controls their status.993 passes/zero failures do not complete1591 cases.',
 'scope':'Completed final-runtime focused/path/compatibility/partition evidence, detached allocated supplement, original failed probes with corrections, and historical partial regression. Raw hypotheses are JSON only; malformed forgeries are named negative controls, not campaign saves.'}
(packet/'QUALIFICATION_SEGMENT_03_INDEX.json').write_text(json.dumps(index,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:index[k] for k in ['status','archive','bytes','sha256','memberCount']},indent=2))
