"""Retain completed development evidence. This is not module qualification."""
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
PACKET=HERE.parent
BASELINE='72692c02c1e3fbb05f2cd8daff32472f34dc0958'
BUILD=ROOT/'engine/artifacts/ferry-wraith/development/compile-20261117T052731317Z-7de51296'
PROBE=ROOT/'engine/artifacts/ferry-wraith/development/genesis-probe-20261117T052747067Z'
OUT=PACKET/'genesis-checkpoint'
def digest(data): return hashlib.sha256(data).hexdigest()
def read(path): return json.loads(path.read_text(encoding='utf-8-sig'))
def main():
    assert not OUT.exists(),'Use the retained checkpoint; do not overwrite it.'
    report=read(PROBE/'RESULT.json');build=read(BUILD/'results.json')
    assert report['status']=='PASS_DEVELOPMENT_GENESIS_ONLY' and len(report['checks'])==7
    assert build['status']=='PASS' and all(x=='PASS' for x in build['compilation'].values())
    assert build['tests']=='NOT RUN' and build['unityCompilation']=='NOT RUN'
    assert digest((BUILD/'results.json').read_bytes())==report['compilationReport']['sha256']
    for row in build['sourceHashes']:
        assert digest((ROOT/'engine'/row['path']).read_bytes())==row['sha256'],row['path']
    for row in report['assemblies']:
        assert digest((BUILD/('Decennium.Foundation.'+row['name']+'.dll')).read_bytes())==row['sha256']
    for row in report['executedSources']:
        assert digest((ROOT/row['path']).read_bytes())==row['sha256']
    saves=['typed-genesis.ddsave','typed-restored.ddsave','console-genesis.ddsave','console-restored.ddsave','typed-after-probes.ddsave']
    assert all(digest((PROBE/n).read_bytes())==report['genesisSha256'] for n in saves)
    assert not (PROBE/'stderr.txt').read_bytes()
    changed=set(subprocess.check_output(['git','diff',BASELINE,'--name-only','--','engine'],cwd=ROOT).decode().splitlines())
    for p in ['Runtime/Core/CreatureActorRecords.cs','Runtime/Core/FerryWraithRecords.cs','Runtime/Persistence/FerryWraithCodec.cs','Laboratory/Model/ActorNumericFacts.cs','Laboratory/Model/SharedFerryWraith.cs']:
        for suffix in ['', '.meta']:changed.add('engine/com.decennium.foundation/'+p+suffix)
    assert len(changed)==20,(len(changed),sorted(changed))
    members={}
    def add(name,path):
        assert name not in members,name
        members[name]=path.read_bytes()
    for row in report['assemblies']:add('selected-build/Decennium.Foundation.'+row['name']+'.dll',BUILD/('Decennium.Foundation.'+row['name']+'.dll'))
    add('selected-build/results.json',BUILD/'results.json')
    for p in PROBE.iterdir():
        if p.is_file():add('genesis-probe/'+p.name,p)
    for p in sorted((ROOT/'engine/artifacts/ferry-wraith/development').glob('compile-*/results.json')):
        if p.parent!=BUILD:add('earlier-builds/'+p.parent.name+'/results.json',p)
    for d in sorted((ROOT/'engine/artifacts/ferry-wraith/development').glob('genesis-*')):
        if d==PROBE or d.name.startswith('genesis-probe-'):continue
        for p in d.iterdir():
            if p.is_file():add('earlier-genesis/'+d.name+'/'+p.name,p)
    for name in sorted(changed):add('changed-source/'+name,ROOT/name)
    for p in [Path(__file__),HERE/'Probe-FerryGenesis.ps1']:add('support/'+p.name,p)
    manifest=[dict(path=n,bytes=len(b),sha256=digest(b)) for n,b in sorted(members.items())]
    OUT.mkdir()
    archive=OUT/'development-genesis.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,raw in sorted(members.items()):
            info=zipfile.ZipInfo(name,(2026,11,17,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o100644<<16;z.writestr(info,raw)
    with zipfile.ZipFile(archive) as z:
        assert z.namelist()==[x['path'] for x in manifest]
        for row in manifest:assert digest(z.read(row['path']))==row['sha256']
    result=dict(status='PASS_RETAINED_DEVELOPMENT_CHECKPOINT_NOT_MODULE_ACCEPTANCE',sourceBaseline=BASELINE,
        acceptedPredecessorEngine='7261052ae4dec908f8c0ac38e0a2c5f4b831065b',selectedBuild=BUILD.relative_to(ROOT).as_posix(),
        probe=PROBE.relative_to(ROOT).as_posix(),compiledSourceInputs=len(build['sourceHashes']),changedEngineFiles=len(changed),
        genesisChecks=len(report['checks']),genesisSha256=report['genesisSha256'],archiveSha256=digest(archive.read_bytes()),
        members=len(manifest),uncompressedBytes=sum(x['bytes'] for x in manifest),newHeadlessSuite=False,
        newConnectedEncounter=False,fullRegression=False,moduleAccepted=False,toolSha256=digest(Path(__file__).read_bytes()))
    (OUT/'MEMBERS.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    (OUT/'RETENTION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))
if __name__=='__main__':main()
