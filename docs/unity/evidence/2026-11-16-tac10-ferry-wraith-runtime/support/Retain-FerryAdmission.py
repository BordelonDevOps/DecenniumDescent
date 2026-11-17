"""Retain the actual frozen paid-admission campaign; never treat it as complete creature gameplay."""
import hashlib
import io
import json
from pathlib import Path
import subprocess
import zipfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
SOURCE='84d0913c74ac9995a32476ad05ea97cb8cf2f492'
BASE='d9c67114b0a96bf6369d71c696a441ede6f11bee'
DEV=ROOT/'engine/artifacts/ferry-wraith/development'
BUILD=DEV/'run-20261117T063436982Z-cf71c6a4'
FOCUS=DEV/'run-20261117T063206319Z-e9a14f1a'
FAILED=DEV/'run-20261117T063047990Z-c17313e3'
OUT=HERE.parent/'admission-checkpoint'
def digest(raw):return hashlib.sha256(raw).hexdigest()
def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def main():
    assert not OUT.exists(),'Do not overwrite retained evidence.'
    build=read(BUILD/'results.json');focus=read(FOCUS/'results.json');failed=read(FAILED/'results.json')
    assert build['status']=='PASS' and build['passed']==1 and build['failed']==0 and len(build['sourceHashes'])==465
    assert build['cases'][0]['Name']=='tac10_ferry_paid_current_epoch_admission_from_fresh_campaign'
    assert focus['status']=='PASS' and focus['passed']==1 and failed['status']=='FAIL' and failed['testsDiscovered']==0
    frozen=zipfile.ZipFile(io.BytesIO(subprocess.check_output(['git','archive','--format=zip',SOURCE,'--','engine'],cwd=ROOT)))
    for row in build['sourceHashes']:
        assert digest(frozen.read('engine/'+row['path'].replace('\\','/')))==row['sha256'],row['path']
    changed=subprocess.check_output(['git','diff',BASE,SOURCE,'--name-only','--','engine'],cwd=ROOT).decode().splitlines()
    assert len(changed)==18
    start=read(BUILD/'started-source/SOURCE.json')
    assert [x['path'] for x in start['files']]==changed
    for row in start['files']:assert digest(frozen.read(row['path']))==row['sha256']
    facts=read(BUILD/'saves/ferry-paid-admission.json')
    assert facts['Revision']==346 and facts['FerryWraith']['Admission']['Epoch']['Origin']==facts['RuleClock']
    assert facts['FerryWraith']['Admission']['PreviousPartyEpochId']=='TEST_ONLY.post-recovery-calendar'
    assert len(facts['FerryWraith']['Contacts'])==1 and facts['FerryWraith']['Contacts'][0]['Failure']==''
    assert (BUILD/'saves/ferry-admitted.ddsave').is_file()
    members={}
    for label,folder in [('campaign',BUILD),('compile-failure',FAILED)]:
        for path in sorted(folder.rglob('*')):
            if path.is_file():members[label+'/'+path.relative_to(folder).as_posix()]=path.read_bytes()
    members['focused-build/results.json']=(FOCUS/'results.json').read_bytes()
    for path in changed:members['changed-source/'+path]=frozen.read(path)
    for path in [Path(__file__),ROOT/'engine/tools/Test-Foundation.ps1']:
        members['executed-support/'+path.name]=path.read_bytes()
    manifest=[dict(path=name,bytes=len(raw),sha256=digest(raw)) for name,raw in sorted(members.items())]
    OUT.mkdir();archive=OUT/'development-admission.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as output:
        for name,raw in sorted(members.items()):
            info=zipfile.ZipInfo(name,(2026,11,17,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
            output.writestr(info,raw)
    with zipfile.ZipFile(archive) as check:
        assert check.namelist()==[x['path'] for x in manifest]
        for row in manifest:assert digest(check.read(row['path']))==row['sha256']
    result=dict(status='PASS_RETAINED_PAID_ADMISSION_NOT_MODULE_ACCEPTANCE',sourceCommit=SOURCE,baseline=BASE,
        compiledSourceInputs=465,changedEngineFiles=18,selectedCampaignCasesPassed=1,selectedFocusedCasesPassed=1,
        finalRevision=facts['Revision'],finalClock=facts['RuleClock'],paidApproachEdges=9,
        finalSaveSha256=digest((BUILD/'saves/ferry-admitted.ddsave').read_bytes()),
        members=len(manifest),archiveSha256=digest(archive.read_bytes()),archiveBytes=archive.stat().st_size,
        fullRegression=False,creatureAttack=False,seal=False,moduleAccepted=False,scriptSha256=digest(Path(__file__).read_bytes()))
    (OUT/'MEMBERS.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    (OUT/'RETENTION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))
if __name__=='__main__':main()
