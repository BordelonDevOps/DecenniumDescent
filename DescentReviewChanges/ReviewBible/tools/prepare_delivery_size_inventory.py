"""Read-only size screening; not an upload manifest or content/publication approval."""
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict
import hashlib
import json
import stat
import subprocess

R=Path(__file__).resolve().parents[1]
G=R.parents[1]
A=G/'docs/audit/2026-10-08/full-game'
CLONE=Path(r'C:\Users\cbord\Documents\ChatGPT\Decennium Descent\github-delivery')

def git(*args):
    return subprocess.run(['git',*args],cwd=CLONE,capture_output=True,text=True,encoding='utf-8',check=True).stdout.strip()

def main():
    out=A/'GITHUB_DELIVERY_SIZE_SCREENING_2026-10-11.json'
    assert not out.exists(),'Preserve existing screening'
    excluded=['node_modules','.git','__pycache__','.next','dist','build','.cache']
    args=['rg','--files','--hidden','--no-ignore',str(G)]
    for name in excluded:args.extend(['-g',f'!**/{name}/**'])
    listing=subprocess.run(args,capture_output=True,text=True,encoding='utf-8',check=True).stdout.splitlines()
    files=[];vanished=[];groups=defaultdict(lambda:{'files':0,'bytes':0,'above100MiB':0})
    for name in listing:
        p=Path(name)
        try:s=p.stat()
        except FileNotFoundError:vanished.append(name);continue
        if not stat.S_ISREG(s.st_mode):continue
        relative=p.relative_to(G).as_posix();n=s.st_size
        row={'path':relative,'bytes':n,'lastModifiedNs':s.st_mtime_ns}
        files.append(row)
        key=relative.split('/')[0]
        group=groups[key];group['files']+=1;group['bytes']+=n;group['above100MiB']+=n>100*1024*1024
    files.sort(key=lambda x:(-x['bytes'],x['path']))
    big=[x for x in files if x['bytes']>100*1024*1024]
    medium=[x for x in files if 50*1024*1024<x['bytes']<=100*1024*1024]
    assert git('remote','get-url','origin')=='https://github.com/BordelonDevOps/DecenniumDescent.git'
    assert git('status','--porcelain')==''
    head=git('rev-parse','HEAD');remote=git('ls-remote','origin','refs/heads/main').split()[0]
    assert head==remote
    report={
        'status':'Read-only size screen complete; final package selection and joint flow remain pending',
        'atUtc':datetime.now(timezone.utc).isoformat(),'root':str(G),'enumerator':'rg --files --hidden --no-ignore',
        'excludedDirectoryNamesAtAnyDepth':excluded,'notAGitIgnoreOrPublicationManifest':True,
        'fileCount':len(files),'totalBytes':sum(x['bytes'] for x in files),'vanishedDuringScan':vanished,
        'topLevelGroups':dict(sorted(groups.items(),key=lambda x:-x[1]['bytes'])),
        'above100MiB':big,'above50Through100MiB':medium,'largest30':files[:30],
        'githubConstraintEvidence':{
            'source':'https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github',
            'checkedDate':'2026-10-11','regularGitFileBlockAboveBytes':100*1024*1024,
            'regularGitWarningAboveBytes':50*1024*1024,
            'interpretation':'The listed oversized files cannot be delivered as ordinary Git blobs. Determine an authorized suitable distribution or local dependency treatment before the final upload; this screening chooses none.'},
        'assetSourceEvidence':{
            'readme':'Descent assets/README.md',
            'readmeSha256':hashlib.sha256((G/'Descent assets/README.md').read_bytes()).hexdigest(),
            'conversionNotes':'Descent assets/tools/README-conversion.md',
            'conversionSha256':hashlib.sha256((G/'Descent assets/tools/README-conversion.md').read_bytes()).hexdigest(),
            'readmeDescription':'Separate local character/GUI workbench using ripped disc assets; conversion notes identify SWTOR packs and portable Blender.',
            'publicationStatus':'The local experiment description is not evidence of redistribution permission. Preserve raw/imported assets and tooling locally while the actual final publication/dependency manifest and rights evidence are reconciled; no exclusion, upload or deletion has been applied.'},
        'deliveryCheckout':{'path':str(CLONE),'remote':'https://github.com/BordelonDevOps/DecenniumDescent.git',
                            'branch':git('branch','--show-current'),'head':head,'observedRemoteMain':remote,
                            'clean':True,'materializedWith':['git read-tree HEAD','git checkout-index --all'],
                            'notes':'Previously --no-checkout clone had an empty index. Only its existing remote snapshot was materialized; the authoring tree was not copied and no authoring commit or push was made.'},
        'sourceInformationDeleted':0,'filesMoved':0,'authoringFilesCopiedToDelivery':0,
        'newCommits':0,'pushPerformed':False,'cosmologyReviewed':False,
        'nextAction':'Finish authored candidate and final joint flow; resolve actual large-file/dependency/public-audience packaging with preserved source information, recheck remote and exact file list, then perform the already-authorized push.'}
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'files':len(files),'bytes':report['totalBytes'],'over100MiB':len(big),'over50Through100MiB':len(medium),
                      'largeFilesOutsideAssetLab':[x for x in big if not x['path'].startswith('Descent assets/')],
                      'groups':report['topLevelGroups'],'cleanDeliveryHead':head,'pushPerformed':False},indent=2))

if __name__=='__main__':main()
