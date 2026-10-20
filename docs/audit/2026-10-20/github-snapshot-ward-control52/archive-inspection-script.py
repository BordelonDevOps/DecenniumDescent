"""Inspect the exact Ready return beyond the general backup recursion bound; execute no content."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import importlib.util, io, json, stat, zipfile
HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('backup52',HERE/'deliver_progress_2026_10_20_ward_control52.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
NAME='docs/audit/2026-10-08/full-game/DD_Part5_Copy_Ready_Preparation_Only_Successor_01.zip'
EXPECTED='41d19bad1b9b2b33b423fd989ddedd919d6a8c9647ec43c43214ddff63ce24d8'
policy=b.h.p.policy
members=[];archives=[];expanded=0;issues=[]

def inspect(name,raw,depth=0):
    global expanded
    assert depth<=12,'separate archive inspection bound exceeded'
    why=policy.reason(name)
    if why and not why.startswith('generated'):
        issues.append({'path':name,'reason':why})
    if Path(name).suffix.lower() in policy.TEXT:
        if b.h.raw_capture(raw):issues.append({'path':name,'reason':'unrelated raw browser capture'})
        if any(rx.search(raw) for rx in policy.SECRET):issues.append({'path':name,'reason':'credential pattern'})
    if Path(name).suffix.lower()!='.zip':return
    archives.append({'path':name,'depth':depth,'bytes':len(raw),'sha256':b.digest(raw)})
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        names=set()
        for item in z.infolist():
            parts=PurePosixPath(item.filename)
            assert not parts.is_absolute() and '..' not in parts.parts and '\\' not in item.filename and ':' not in item.filename,item.filename
            assert item.filename not in names,item.filename
            names.add(item.filename)
            assert not stat.S_ISLNK(item.external_attr>>16),item.filename
            if item.is_dir():continue
            assert not item.flag_bits&1,'encrypted member'
            expanded+=item.file_size
            assert expanded<=1024**3 and len(members)<50000,'expanded inspection bound exceeded'
            content=z.read(item)
            assert len(content)==item.file_size
            full=name+' :: '+item.filename
            members.append({'path':full,'bytes':len(content),'sha256':b.digest(content)})
            inspect(item.filename,content,depth+1)

def main():
    planpath=b.W/'plan.json';plan=json.loads(planpath.read_bytes())
    assert b.git('status','--porcelain=v1','-z')==b''
    assert not (b.W/'ready-archive-additional-review.json').exists()
    original=next(x for x in plan['excluded'] if x['path']==NAME)
    assert 'nested archive depth' in original['reason']
    raw=b.lp(b.G/NAME).read_bytes()
    assert b.digest(raw)==EXPECTED==original['sha256'] and len(raw)==39831317
    inspect(NAME,raw)
    assert not issues,issues
    receipt={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'scope':'Read-only exact immutable Ready archive inspection beyond general depth5 threshold. No downloaded content executed.','archive':original,'maxDepthInspected':max(x['depth'] for x in archives),'archivesInspected':archives,'membersInspected':len(members),'expandedBytesInspected':expanded,'memberBindings':members,'issues':issues,'sourceChanged':False}
    report=b.W/'ready-archive-additional-review.json';b.write_new(report,b.jsraw(receipt))
    row={k:v for k,v in original.items() if k!='reason'}
    row['changedFromBaseline']=b.h.oldtree(b.BASE).get(NAME,{}).get('oid')!=row['gitBlob']
    plan['excluded']=[x for x in plan['excluded'] if x['path']!=NAME]
    plan['included']=sorted(plan['included']+[row],key=lambda x:x['path'])
    plan['separatelyReviewedArchives']=[{'originalScannerDisposition':original,'additionalInspectionReceipt':str(report),'receiptSha256':b.digest(report.read_bytes()),'currentDisposition':'Included unchanged after complete bounded recursive inspection; zero policy or credential issues.'}]
    planpath.write_bytes(b.jsraw(plan))
    changed=[x['path'] for x in plan['included'] if x['changedFromBaseline']]
    (b.W/'changed-source-paths.json').write_bytes(b.jsraw(changed))
    print(json.dumps({'includedArchive':NAME,'archivesInspected':len(archives),'maxDepthInspected':receipt['maxDepthInspected'],'membersInspected':len(members),'expandedBytesInspected':expanded,'issues':0,'includedFiles':len(plan['included']),'changedFiles':len(changed)}))

if __name__=='__main__':main()
