"""Retain the historical first genuine Ferry fire checkpoint before the Petrified correction."""
import hashlib
import io
import json
from pathlib import Path
import subprocess
import zipfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
SOURCE='37ce577fbb79398042c5a57e9b515bf09434c803'
BASE='84d0913c74ac9995a32476ad05ea97cb8cf2f492'
DEV=ROOT/'engine/artifacts/ferry-wraith/development'
BUILD=DEV/'run-20261117T064418448Z-0c786ff6'
PROBE=DEV/'controller-probe-20261117T0653Z'
STATIC=ROOT/'engine/artifacts/static-20261117T064727193Z-337769de'
OUT=HERE.parent/'controller-checkpoint'
def digest(raw):return hashlib.sha256(raw).hexdigest()
def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def main():
    assert not OUT.exists(),'Do not overwrite retained evidence.'
    build=read(BUILD/'results.json');probe=read(PROBE/'RESULT.json');static=read(STATIC/'results.json')
    assert build['status']=='PASS' and build['passed']==1 and len(build['sourceHashes'])==467
    assert probe['status']=='PASS_FIRST_GENUINE_CREATURE_FIRE_NOT_MODULE_ACCEPTANCE' and len(probe['checks'])==4
    assert probe['finalRevision']==351 and len(probe['commands'])==5 and static['status']=='PASS'
    driver='docs/unity/evidence/2026-11-16-tac10-ferry-wraith-runtime/support/Probe-FerryController.ps1'
    review='docs/unity/evidence/2026-11-16-tac10-ferry-wraith-runtime/GPT_TARGET_REVIEW.json'
    frozen=zipfile.ZipFile(io.BytesIO(subprocess.check_output(['git','archive','--format=zip',SOURCE,'--','engine',driver,review],cwd=ROOT)))
    for report in [build,static]:
        for row in report['sourceHashes']:
            assert digest(frozen.read('engine/'+row['path'].replace('\\','/')))==row['sha256'],row['path']
    assert len(static['sourceHashes'])==975
    assert probe['compilationReport']['sha256']==digest((BUILD/'results.json').read_bytes())
    for row in probe['assemblies']:assert row['sha256']==digest((BUILD/('Decennium.Foundation.'+row['name']+'.dll')).read_bytes())
    assert probe['script']['sha256']==digest(frozen.read(driver))
    admission=read(HERE.parent/'admission-checkpoint/RETENTION.json')
    assert probe['admissionSource']['sha256']==admission['finalSaveSha256']==digest((PROBE/'original-admission.ddsave').read_bytes())
    assert digest((PROBE/'first-fire-hit.ddsave').read_bytes())==digest((PROBE/'first-fire-hit-restored.ddsave').read_bytes())
    changed=subprocess.check_output(['git','diff',BASE,SOURCE,'--name-only','--','engine'],cwd=ROOT).decode().splitlines()
    assert len(changed)==10,changed
    members={}
    for label,folder in [('selected-build',BUILD),('controller',PROBE),('static',STATIC)]:
        for path in sorted(folder.rglob('*')):
            if path.is_file():members[label+'/'+path.relative_to(folder).as_posix()]=path.read_bytes()
    for suffix in ['0647','0648','0650','0651']:
        folder=DEV/('controller-probe-20261117T'+suffix+'Z');report=read(folder/'RESULT.json')
        assert report['status'].startswith('FAIL')
        script=folder/'Probe-FerryController.failed.ps1'
        if 'script' in report:assert report['script']['sha256']==digest(script.read_bytes())
        for path in sorted(folder.rglob('*')):
            if path.is_file():members['probe-failures/'+folder.name+'/'+path.relative_to(folder).as_posix()]=path.read_bytes()
    for path in changed:members['changed-source/'+path]=frozen.read(path)
    folder=DEV/'controller-retention-overscope-20261117T0703Z'
    for path in sorted(folder.iterdir()):members['collector-termination/'+path.name]=path.read_bytes()
    members['executed-support/Probe-FerryController.ps1']=frozen.read(driver)
    members['executed-support/Retain-FerryController.py']=Path(__file__).read_bytes()
    members['review/GPT_TARGET_REVIEW.json']=frozen.read('docs/unity/evidence/2026-11-16-tac10-ferry-wraith-runtime/GPT_TARGET_REVIEW.json')
    manifest=[dict(path=name,bytes=len(raw),sha256=digest(raw)) for name,raw in sorted(members.items())]
    OUT.mkdir();archive=OUT/'development-controller.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as output:
        for name,raw in sorted(members.items()):
            info=zipfile.ZipInfo(name,(2026,11,17,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
            output.writestr(info,raw)
    with zipfile.ZipFile(archive) as check:
        assert check.namelist()==[x['path'] for x in manifest]
        for row in manifest:assert digest(check.read(row['path']))==row['sha256']
    result=dict(status='PASS_RETAINED_FIRST_GENUINE_FIRE_KNOWN_POISON_DEFECT_NOT_ACCEPTANCE',sourceCommit=SOURCE,
        compiledSourceInputs=467,staticInputs=975,changedEngineFiles=10,selectedCasesPassed=1,controllerChecks=4,
        finalRevision=351,finalSaveSha256=digest((PROBE/'first-fire-hit.ddsave').read_bytes()),
        members=len(manifest),archiveSha256=digest(archive.read_bytes()),archiveBytes=archive.stat().st_size,
        knownDefectReview='c07a1951-79e1-5d4a-8952-d72d10e3e0fc',fullRegression=False,seal=False,moduleAccepted=False,
        scriptSha256=digest(Path(__file__).read_bytes()))
    (OUT/'MEMBERS.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    (OUT/'RETENTION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))
if __name__=='__main__':main()
