"""Retain actual target/check integration evidence without claiming TAC-10 acceptance."""
import hashlib
import io
import json
from pathlib import Path
import subprocess
import zipfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
BASELINE='a46eab14ef2ae9f0f1fef7153781d10a00028e4c'
SOURCE_COMMIT='9cbac60eefbe8f61b11b5e2adebde8b194961aad'
DEV=ROOT/'engine/artifacts/ferry-wraith/development'
BUILD=DEV/'run-20261117T060652093Z-58120be8'
PROBE=DEV/'target-probe-20261117T0611Z'
GENESIS=DEV/'genesis-probe-20261117T0610Z'
STATIC=ROOT/'engine/artifacts/static-20261117T060832368Z-b4733442'
INTERIM=DEV/'target-integration-before-order'
OUT=HERE.parent/'target-checkpoint'

def digest(raw):return hashlib.sha256(raw).hexdigest()
def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))

def main():
    assert not OUT.exists(),'Do not overwrite retained evidence.'
    build,probe,genesis,static=[read(p/n) for p,n in [(BUILD,'results.json'),(PROBE,'RESULT.json'),(GENESIS,'RESULT.json'),(STATIC,'results.json')]]
    assert build['status']=='PASS' and build['passed']==1 and build['failed']==0 and len(build['sourceHashes'])==465
    assert probe['status']=='PASS_DEVELOPMENT_TARGET_INTEGRATION_ONLY' and len(probe['cases'])==22
    assert [x['Name'] for x in probe['cases']]==probe['selected'] and all(x['Passed'] for x in probe['cases'])
    assert len(set(probe['selected']))==22 and build['cases'][0]['Name'] in probe['selected']
    assert genesis['status']=='PASS_DEVELOPMENT_GENESIS_ONLY' and len(genesis['checks'])==7 and static['status']=='PASS'
    frozen=zipfile.ZipFile(io.BytesIO(subprocess.check_output(['git','archive','--format=zip',SOURCE_COMMIT,'--','engine'],cwd=ROOT)))
    for row in build['sourceHashes']:
        assert digest(frozen.read('engine/'+row['path'].replace('\\','/')))==row['sha256'],row['path']
    for report in [probe,genesis]:
        assert report['compilationReport']['sha256']==digest((BUILD/'results.json').read_bytes())
        for row in report['assemblies']:
            assert digest((BUILD/('Decennium.Foundation.'+row['name']+'.dll')).read_bytes())==row['sha256']
    assert digest(Path(probe['executedScript']['path']).read_bytes())==probe['executedScript']['sha256']
    for row in genesis['executedSources']:assert digest((ROOT/row['path']).read_bytes())==row['sha256']
    for name in ['typed-genesis.ddsave','typed-restored.ddsave','console-genesis.ddsave','console-restored.ddsave','typed-after-probes.ddsave']:
        assert digest((GENESIS/name).read_bytes())==genesis['genesisSha256']
    interim=read(DEV/'run-20261117T060321900Z-2bf91cfb/results.json')
    assert interim['status']=='PASS' and interim['passed']==1
    for row in interim['sourceHashes']:
        name='engine/'+row['path'].replace('\\','/')
        path=INTERIM/name
        raw=path.read_bytes() if path.exists() else subprocess.check_output(['git','show',BASELINE+':'+name],cwd=ROOT)
        assert digest(raw)==row['sha256'],name
    failed=read(DEV/'target-probe-20261117T0610Z/RESULT.json')
    assert failed['status']=='FAIL' and failed['cases']==[] and 'Unexpected selected case count: 21' in failed['error']
    assert digest((DEV/'target-probe-20261117T0610Z/Probe-FerryTargets.failed.ps1').read_bytes())==failed['executedScript']['sha256']
    changed=subprocess.check_output(['git','diff',BASELINE,SOURCE_COMMIT,'--name-only','--','engine'],cwd=ROOT).decode().splitlines()
    assert len(changed)==12,changed
    review=read(HERE.parent/'GPT_DAMAGE_ORDER_REVIEW.json')
    assert review['responseId']=='8280e942-e79a-5b05-a17c-bea59dcaef4e'
    members={}
    def add(name,path):
        assert name not in members
        members[name]=path.read_bytes()
    for label,folder in [('selected-build',BUILD),('target-probe',PROBE),('genesis-probe',GENESIS),('static',STATIC),
        ('interim-source',INTERIM),('collector-failure',DEV/'target-probe-20261117T0610Z')]:
        for path in sorted(folder.rglob('*')):
            if path.is_file():add(label+'/'+path.relative_to(folder).as_posix(),path)
    add('interim-build/results.json',DEV/'run-20261117T060321900Z-2bf91cfb/results.json')
    for path in changed:members['changed-source/'+path]=frozen.read(path)
    for path in [Path(__file__),HERE/'Probe-FerryTargets.ps1',HERE/'Probe-FerryGenesis.ps1',ROOT/'engine/tools/Test-Foundation.ps1',
        ROOT/'engine/tools/Validate-Package.ps1',ROOT/'engine/tools/Open-ConnectedExpedition.ps1']:
        add('executed-support/'+path.name,path)
    add('review/GPT_DAMAGE_ORDER_REVIEW.json',HERE.parent/'GPT_DAMAGE_ORDER_REVIEW.json')
    manifest=[dict(path=n,bytes=len(b),sha256=digest(b)) for n,b in sorted(members.items())]
    OUT.mkdir();archive=OUT/'development-targets.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as output:
        for name,raw in sorted(members.items()):
            info=zipfile.ZipInfo(name,(2026,11,17,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
            output.writestr(info,raw)
    with zipfile.ZipFile(archive) as check:
        assert check.namelist()==[x['path'] for x in manifest]
        for row in manifest:assert digest(check.read(row['path']))==row['sha256']
    result=dict(status='PASS_RETAINED_TARGET_INTEGRATION_NOT_MODULE_ACCEPTANCE',sourceBaseline=BASELINE,sourceCommit=SOURCE_COMMIT,
        acceptedPredecessorEngine='7261052ae4dec908f8c0ac38e0a2c5f4b831065b',selectedBuild=BUILD.relative_to(ROOT).as_posix(),
        compiledSourceInputs=465,changedEngineFiles=len(changed),selectedUniqueCasesPassed=22,ferryCases=4,predecessorCases=18,
        genesisChecks=7,genesisSha256=genesis['genesisSha256'],reviewResponse=review['responseId'],
        members=len(manifest),archiveSha256=digest(archive.read_bytes()),archiveBytes=archive.stat().st_size,
        uncompressedBytes=sum(x['bytes'] for x in manifest),fullRegression=False,connectedCreatureEncounter=False,
        moduleAccepted=False,scriptSha256=digest(Path(__file__).read_bytes()))
    (OUT/'MEMBERS.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    (OUT/'RETENTION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))

if __name__=='__main__':main()
