"""Reconcile completed original qualification; never execute, resume or replace workers."""
import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import subprocess
import zipfile

ROOT=Path(__file__).resolve().parents[5]
PACKET=Path(__file__).resolve().parents[1]
SOURCE='7261052ae4dec908f8c0ac38e0a2c5f4b831065b'
MODES={'ConsoleUninterrupted','ConsoleRestored','TypedUninterrupted','TypedRestored','ReceiptReplay'}
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
lines=lambda p:p.read_text(encoding='utf-8-sig').splitlines()

def check_archive(base,record):
    path=base/record['path']
    assert path.stat().st_size==record['bytes'] and digest(path)==record['sha256']
    with zipfile.ZipFile(path) as z:
        assert sorted(z.namelist())==sorted(x['path'] for x in record['members'])
        for row in record['members']:
            data=z.read(row['path']);assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']

def check_bindings(folder):
    before,after=(read(folder/('execution-sources.'+part+'.json')) for part in ('before','after'))
    assert after['status']=='PASS' and before['files']==after['files'] and before['pid']==after['pid']
    for row in after['files']:
        path=ROOT/row['path'];assert path.stat().st_size==row['bytes'] and digest(path)==row['sha256'],row['path']
    return after['files']

def check_assemblies(rows,expected):
    if isinstance(rows,list):rows={x['name']:x for x in rows}
    assert set(rows)=={'Core','Persistence','LabModel'}
    for part,row in rows.items():assert row['sha256']==expected['Decennium.Foundation.'+part+'.dll']

def historical_pins():
    source=read(PACKET.parent/'2026-11-16-tac03-declared-geometry/SOURCE_BINDINGS.json')
    rows=source['sources'];assert len(rows)==131
    specs=''.join(x['revision']+':'+x['path']+'\n' for x in rows).encode()
    identities=subprocess.check_output(['git','cat-file','--batch-check'],input=specs,cwd=ROOT).decode().splitlines()
    assert len(identities)==len(rows)
    for row,line in zip(rows,identities):
        blob,kind,size=line.split();assert blob==row['gitBlob'] and kind=='blob' and int(size)==row['bytes']
    payload=subprocess.check_output(['git','cat-file','--batch'],input=''.join(x['gitBlob']+'\n' for x in rows).encode(),cwd=ROOT)
    stream=io.BytesIO(payload)
    for row in rows:
        blob,kind,size=stream.readline().decode().split();assert blob==row['gitBlob'] and kind=='blob'
        data=stream.read(int(size));assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
        assert stream.read(1)==b'\n'
    assert not stream.read()
    return len(rows)

def main():
    parser=argparse.ArgumentParser()
    for name in ('run','qualification','focused','output'):parser.add_argument('--'+name,type=Path,required=True)
    args=parser.parse_args()
    run,q,focused,output=(getattr(args,x).resolve() for x in ('run','qualification','focused','output'))
    bound_sources={}
    def bind(folder):
        for row in check_bindings(folder):
            path=ROOT/row['path']
            bound_sources[row['path']]=path
    assert not output.exists(),'Never replace final evidence'
    assert not subprocess.check_output(['git','diff',SOURCE,'--','engine'],cwd=ROOT).strip()
    launch=read(run/'launch.json')
    assert launch['runId']=='c961a29293a14693bf95e2db72465a9d' and launch['sourceCommit']==SOURCE and launch['sourceCommitted']
    assert launch['requiredCount']==1576 and launch['retainedPredecessors']==1570
    assert digest(Path(launch['runner']))==launch['runnerSha256']
    runner=Path(launch['runner'])
    bound_sources[runner.relative_to(ROOT).as_posix()]=runner
    compiled=read(run/'compiled-source-report.json')
    assert compiled['status']=='PASS' and len(compiled['sourceHashes'])==457
    assert digest(run/'compiled-source-report.json')==launch['compiledSourceReportSha256']
    for row in compiled['sourceHashes']:assert digest(ROOT/'engine'/row['path'])==row['sha256'],row['path']
    static=read(PACKET/'correction/static-results.json')
    assert static['status']=='PASS' and all(x['passed'] for x in static['checks'])
    for row in static['sourceHashes']:assert digest(ROOT/'engine'/row['path'])==row['sha256'],row['path']
    corrected=read(PACKET/'correction/RETENTION.json')
    for key in ('assemblies','evidence'):check_archive(PACKET/'correction',corrected[key])
    assert {x['path']:x['sha256'] for x in corrected['assemblies']['members']}==launch['assemblies']
    checkpoint=read(PACKET/'qualification-checkpoint/RETENTION.json')
    assert checkpoint['sourceCommit']==SOURCE and checkpoint['status']=='PASS_PARTIAL_QUALIFICATION_RETENTION'
    check_archive(PACKET/'qualification-checkpoint',checkpoint['archive'])
    supplemental={}
    with zipfile.ZipFile(PACKET/'qualification-checkpoint'/checkpoint['archive']['path']) as z:
        for name in ('trust','backup','spatial-controls-v2','bishop-baseline','exclusions/genesis','exclusions/continued'):
            report=json.loads(z.read(name+'/results.json').decode('utf-8-sig'))
            assert report['status']=='PASS';check_assemblies(report['assemblies'],launch['assemblies'])
            supplemental[name]=report
    assert len(supplemental['trust']['cases'])==6 and len(supplemental['backup']['checks'])==5
    assert len(supplemental['spatial-controls-v2']['rays'])==5 and len(supplemental['spatial-controls-v2']['actualCommandDenials'])==2
    assert supplemental['bishop-baseline']['commands']==457 and supplemental['bishop-baseline']['saves']==21
    for dll,sha in launch['assemblies'].items():assert digest(run/'execution-assemblies'/dll)==sha

    names=lines(run/'all-names.txt');new=[x for x in names if x.startswith('tac03_declared_geometry_')]
    prior=PACKET.parent/'2026-11-16-chr03-bishop-runtime/final/regression'
    assert len(names)==len(set(names))==1576 and len(new)==6
    assert [x for x in names if x not in new]==lines(prior/'all-names.txt')
    assert digest(run/'all-names.txt')==launch['inventorySha256']
    workers=read(run/'processes.json');assert len(workers)==6 and len({x['pid'] for x in workers})==6
    assert {x['group'] for x in workers}=={'shardA','shardB','shardC','shardD','shardE','shardF'}
    all_results=[];completions=[]
    for worker in workers:
        group=worker['group'];assigned=lines(run/(group+'-names.txt'))
        assert [x for x in assigned if x not in new]==lines(prior/(group+'-names.txt'))
        assert digest(run/(group+'-names.txt'))==launch['assignments'][group]
        start,end=(read(run/(group+suffix)) for suffix in ('.started.json','.execution.json'))
        assert start['runId']==end['runId']==launch['runId'] and start['pid']==end['pid']==worker['pid']
        assert start['assemblies']==end['assemblies']
        for dll,sha in launch['assemblies'].items():assert start['assemblies'][dll]['sha256']==sha
        for field,value in [('inventorySha256',launch['inventorySha256']),('assignmentSha256',launch['assignments'][group])]:assert start[field]==end[field]==value
        rows=[json.loads(x) for x in lines(run/(group+'.jsonl'))]
        assert [x['Name'] for x in rows]==assigned and len(rows)==end['cases']==worker['cases']
        assert all(x['Passed'] and not x['Error'] for x in rows)
        assert digest(run/(group+'.jsonl'))==end['journalSha256'] and lines(run/(group+'.done'))==['DONE']
        all_results.extend(rows);completions.append(end)
    assert len(all_results)==1576 and {x['Name'] for x in all_results}==set(names)
    focused_report=read(focused/'results.json')
    assert focused_report['status']=='PASS' and len(focused_report['cases'])==6
    assert {x['Name'] for x in focused_report['cases']}==set(new) and all(x['Passed'] and not x['Error'] for x in focused_report['cases'])
    assert focused_report['compiledReportSha256']==launch['compiledSourceReportSha256'] and focused_report['sourceHashes']==compiled['sourceHashes']
    assert {'Decennium.Foundation.'+part+'.dll':row['sha256'] for part,row in focused_report['assemblies'].items()}==launch['assemblies']
    bind(focused)
    expected_artifacts={
        'tac03_declared_geometry_connected_weighted_interrupts_and_continue':97,
        'tac03_declared_geometry_genesis_and_verified_restore':1,
        'tac03_declared_geometry_paid_dash_suspend_authority_and_restore':10,
        'tac03_declared_geometry_strain_dash_queries_cross_actual_start':22,
        'tac03_declared_geometry_support_cost_and_corner_controls':0,
        'tac03_declared_geometry_trusted_layout_and_terrain_rejection':0,
    }
    assert set(expected_artifacts)==set(new)=={x.name for x in (focused/'saves').iterdir() if x.is_dir()}
    for name,count in expected_artifacts.items():
        a,b=focused/'saves'/name,run/'saves'/name
        assert a.is_dir() and b.is_dir()
        left={x.relative_to(a).as_posix() for x in a.rglob('*') if x.is_file()}
        right={x.relative_to(b).as_posix() for x in b.rglob('*') if x.is_file()}
        assert left==right and len(left)==count,(name,count,len(left),len(right))
    focused_matches=[]
    for path in sorted((focused/'saves').rglob('*')):
        if path.is_file():
            relative=path.relative_to(focused/'saves');actual=run/'saves'/relative
            assert actual.stat().st_size==path.stat().st_size and digest(actual)==digest(path),str(relative)
            focused_matches.append(str(relative).replace('\\','/'))
    assert len(focused_matches)==sum(expected_artifacts.values())==130
    assert {Path(x).parts[0] for x in focused_matches}=={name for name,count in expected_artifacts.items() if count}

    reference,paths=q/'connected-reference',q/'connected-paths'
    manifest,result=read(reference/'manifest.json'),read(paths/'results.json')
    assert manifest['status']=='PASS_REFERENCE' and manifest['revision']==327 and len(manifest['marks'])==23
    assert result['status']=='PASS' and set(result['paths'])==MODES
    assert digest(reference/'inputs.jsonl')==result['traceSha256']
    check_assemblies(manifest['assemblies'],launch['assemblies']);check_assemblies(result['assemblies'],launch['assemblies'])
    bind(reference);bind(paths)
    probes=0
    for mark in manifest['marks']:
        expected={mark['name']:mark['sha256'],mark['name']+'.after-probes.ddsave':mark['sha256']}
        assert set(mark['views'])=={'Player','FirstOpponent','RecoveryOpponent'}
        expected.update({x['name']:x['sha256'] for x in mark['views'].values()})
        expected.update({x['request']['evidenceRead']:x['sha256'] for x in mark['probes']});probes+=len(mark['probes'])
        for filename,sha in expected.items():
            assert digest(reference/filename)==sha
            for mode in MODES:
                assert result['paths'][mode]['commands']==327 and digest(paths/mode/filename)==sha,(mode,filename)
                if not filename.endswith('.after-probes.ddsave'):assert result['paths'][mode]['checkpoints'][filename]==sha
    assert probes==1104

    suite=q/'compatibility-suite-v2';assert read(suite/'results.json')['status']=='PASS';bind(suite)
    legacy=suite/'compatibility95-110';compat=read(legacy/'results.json');bishop=read(legacy/'bishop-profile-results.json')
    assert compat['Status']=='PASS' and len(compat['Cases'])==28 and bishop['status']=='PASS' and len(bishop['rejections'])==28
    check_assemblies(bishop['assemblies'],launch['assemblies'])
    assert digest(legacy/'results.json')==bishop['compatibilityReportSha256']
    evidence=ROOT/'docs/unity/evidence'
    for i,(case,rejected) in enumerate(zip(compat['Cases'],bishop['rejections'])):
        folder=legacy/('case-'+str(i)+'-wire'+str(case['Wire']))
        assert digest(evidence/case['Source'])==case['SourceSha256']==case['RoundtripSha256']==case['ContinuedSha256']
        assert digest(evidence/case['Earlier'])==case['EarlierSha256'] and case['Commands']>0 and case['ToRevision']>case['FromRevision']
        assert digest(folder/'roundtrip.ddsave')==digest(folder/'continued.ddsave')==case['SourceSha256']
        assert rejected['source']==case['Source'] and digest(legacy/rejected['after'])==rejected['unchangedSha256']==bishop['beforeSha256']
    views=suite/'legacy95-110-views';view_report=read(views/'results.json')
    assert view_report['status']=='PASS' and len(view_report['cases'])==28
    assert digest(ROOT/'engine/tools/Open-ConnectedExpedition.ps1')==view_report['newConsoleSha256']
    assert digest(views/'accepted-predecessor-console.ps1')==view_report['oldConsoleSha256']
    old_console=subprocess.check_output(['git','show',view_report['predecessorCommit']+':engine/tools/Open-ConnectedExpedition.ps1'],cwd=ROOT)
    assert old_console.decode('utf-8-sig').splitlines()==lines(views/'accepted-predecessor-console.ps1')
    for i,case in enumerate(view_report['cases']):
        folder=views/('case-'+str(i)+'-wire'+str(case['wire']))
        assert digest(folder/'old.jsonl')==case['oldOutputSha256'] and digest(folder/'new.jsonl')==case['newOutputSha256']
        a,b=([json.loads(x) for x in lines(folder/name)] for name in ('old.jsonl','new.jsonl'))
        assert len(a)==len(b)==5 and a[2]['Response']==b[2]['Response']=='Restored' and all(a[j]==b[j] for j in (0,1,3,4))
    envelopes=[]
    for wire in (111,112):
        folder=suite/('wire'+str(wire));report=read(folder/'results.json')
        assert report['status']=='PASS';check_assemblies(report['currentAssemblies'],launch['assemblies'])
        accepted=evidence/('2026-11-16-exp07-post-recovery/implementation' if wire==111 else '2026-11-16-chr03-bishop-runtime/final')
        archive=accepted/'qualification-evidence.zip'
        assert digest(archive)==report['sourceArchiveSha256']
        accepted_spec='72def9d77ae66bd81f811bbfc74c4cbbaf7b1d25:'+archive.relative_to(ROOT).as_posix()
        assert subprocess.check_output(['git','hash-object',str(archive)],cwd=ROOT).strip()==subprocess.check_output(['git','rev-parse',accepted_spec],cwd=ROOT).strip()
        old_launch=read(accepted/'regression/launch.json')
        check_assemblies(report['oldAssemblies'],old_launch['assemblies'])
        for part in ('Core','Persistence','LabModel'):
            dll='Decennium.Foundation.'+part+'.dll'
            assert digest(folder/'accepted-assemblies'/dll)==old_launch['assemblies'][dll]
        marks=read(folder/'sources/marks.json');assert len(marks)==report['authenticCheckpoints']
        reference_prefix='qualification/campaigns/main/trace/' if wire==111 else 'qualification/reference/'
        with zipfile.ZipFile(archive) as z:
            original=json.loads(z.read(reference_prefix+'manifest.json').decode('utf-8-sig'))
            assert {x['name']:(x['revision'],x['sha256']) for x in marks}=={x['name']:(x['revision'],x['sha256']) for x in original['marks']}
            for mark in marks:
                data=z.read(reference_prefix+('reference/' if wire==111 else '')+mark['name'])
                assert hashlib.sha256(data).hexdigest()==mark['sha256']
        a,b=read(folder/('Accepted'+str(wire))/'results.json'),read(folder/'Current/results.json')
        assert a['status']==b['status']=='PASS' and a['artifacts']==b['artifacts']==report['artifacts']
        assert a['commands']==b['commands']==report['actualContinuationCommandsPerRole']
        for mark in marks:assert digest(folder/'sources'/mark['name'])==mark['sha256']
        for name,sha in report['artifacts'].items():assert digest(folder/('Accepted'+str(wire))/name)==digest(folder/'Current'/name)==sha
        if wire==112:
            bind(folder);bind(folder/'Current');bind(folder/'Accepted112')
        envelopes.append(dict(wire=wire,checkpoints=len(marks),continuedCommandsPerRole=a['commands'],canonicalAndViewComparisons=len(a['artifacts'])))
    rejections=q/'legacy-profile-rejections';denied=read(rejections/'results.json')
    assert denied['status']=='PASS' and len(denied['cases'])==28+sum(x['checkpoints'] for x in envelopes)
    check_assemblies(denied['assemblies'],launch['assemblies']);bind(rejections)
    stable=digest(rejections/'before.ddsave');assert digest(rejections/'after.ddsave')==stable
    for row in denied['cases']:assert row['error'] and row['unchangedSha256']==stable and digest(Path(row['source']))==row['sourceSha256']

    pinned=historical_pins()
    consumer_path=PACKET/'CONSUMER_RECONCILIATION.json';consumers=read(consumer_path)
    inventory_path=PACKET.parent/'2026-11-16-tac03-declared-geometry/API_CONSUMERS.json';inventory=read(inventory_path)
    assert consumers['status']=='PASS_SOURCE_INVENTORY_RECONCILIATION' and consumers['sourceCommit']==SOURCE
    assert consumers['inventorySha256']==digest(inventory_path) and set(consumers['searches'])==set(inventory['searches'])
    consumer_files=set();consumer_rows=0
    for name,group in consumers['searches'].items():
        original=inventory['searches'][name]
        assert group['files']==len(group['rows'])==original['matchedFiles']
        assert group['matchedLines']==sum(len(x['originalHits']) for x in group['rows'])==original['matchedLines']
        for row,old in zip(group['rows'],original['rows']):
            assert row['path']==old['path'] and row['originalHits']==old['hits'] and row['disposition'] and row['explanation']
            path=ROOT/row['path'];assert path.stat().st_size==row['currentBytes'] and digest(path)==row['currentSha256']
            consumer_files.add(row['path']);consumer_rows+=1
    assert len(consumer_files)==consumers['uniqueFiles']==100 and consumer_rows==127
    members={}
    def queue(folder,prefix):
        for path in sorted(folder.rglob('*')):
            if path.is_file() and path.suffix!='.dll':members[prefix+'/'+path.relative_to(folder).as_posix()]=path
    queue(run,'regression');queue(paths,'qualification/connected-paths');queue(suite,'qualification/compatibility-suite-v2');queue(rejections,'qualification/legacy-profile-rejections')
    for name,path in bound_sources.items():members['execution-sources/'+name]=path
    # Completed reference/trust/baseline controls remain in the verified checkpoint archive.
    output.mkdir();archive=output/'qualification-final.zip';index=[]
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,path in sorted(members.items()):
            data=path.read_bytes();z.writestr(name,data);index.append(dict(path=name,bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
    record=dict(path=archive.name,bytes=archive.stat().st_size,sha256=digest(archive),members=index);check_archive(output,record)
    report=dict(status='PASS_FINAL_EVIDENCE_RECONCILIATION',scope='Bounded TEST_ONLY geometry113 qualification; actual final GPT review and whole-engine completion remain open',
        at=datetime.now(timezone.utc).isoformat(),sourceCommit=SOURCE,runId=launch['runId'],passed=1576,failed=0,originalCompletions=completions,
        historicalSourcePins=pinned,compilationInputs=457,staticInputs=len(static['sourceHashes']),focusedArtifactsMatched=len(focused_matches),
        focusedCaseArtifacts=expected_artifacts,
        retainedExecutionSources=len(bound_sources),
        consumerReconciliation=dict(path='../CONSUMER_RECONCILIATION.json',sha256=digest(consumer_path),rows=consumer_rows,uniqueFiles=len(consumer_files)),
        connected=dict(commandsPerPath=327,paths=sorted(MODES),canonicalComparisons=115,filteredViewComparisons=345,readDenialDuplicateComparisons=5*probes),
        compatibility=dict(authentic95To110Cases=28,oldConsoleViews=112,envelopes=envelopes,declared113Rejections=len(denied['cases'])),
        supplemental=dict(inheritedCommands=457,inheritedSaves=21,hostileInputRejections=6,backupChecks=5,mechanicalChannelProbes=5,actualPublicMovementDenials=2,semanticExclusionCheckpoints=2),
        preservedCheckpoint=dict(path='../qualification-checkpoint/RETENTION.json',sha256=digest(PACKET/'qualification-checkpoint/RETENTION.json')),
        correctedAssemblies=dict(path='../correction/RETENTION.json',sha256=digest(PACKET/'correction/RETENTION.json')),
        archive={k:v for k,v in record.items() if k!='members'})
    (output/'QUALIFICATION_MEMBERS.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    (output/'FINAL_RECONCILIATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='originalCompletions'}))

if __name__=='__main__':main()
