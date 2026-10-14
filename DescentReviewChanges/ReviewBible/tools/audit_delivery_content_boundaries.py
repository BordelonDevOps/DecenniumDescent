"""Read-only content inventory and remote-history preservation evidence.

Creates audit reports only. No copy to delivery, removal, staging, commit or push.
Cosmology files are fingerprinted as opaque bytes, never interpreted.
"""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter,defaultdict
import hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
D=Path('C:/Users/cbord/Documents/ChatGPT/Decennium Descent/github-delivery')
def long(p):return Path('\\\\?\\'+str(p.resolve())) if os.name=='nt' else p
def sha(p):return hashlib.sha256(long(p).read_bytes()).hexdigest()
def rel(p):return p.relative_to(G).as_posix()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def git(*args):return subprocess.run(['git',*args],cwd=D,capture_output=True,check=True).stdout
def classify(name):
    parts=name.split('/');low=[p.lower() for p in parts]
    if any(p.startswith('.env') for p in low) or name.lower().endswith(('.pem','.key','.pfx','.p12')):return 'private-file-name-review; preserve locally'
    if re.search(r'(browser|screenshot|screen-proof|screenshot-proof).*\.(png|jpg|jpeg|webp)$',name,re.I):return 'browser-proof; preserve locally and review separate from game release'
    if low[0] in ['.cursor','.same']:return 'editor-context; inspect relevance before release'
    if low[0] in ['_preserved','archive','backups','decenniumdescentv6'] or 'incoming' in low:return 'preserved-history; maintain original identity'
    if name.startswith('docs/audit/'):return 'development-evidence; retain review provenance'
    if name.startswith('DescentReviewChanges/ReviewBible/'):return 'current-review-candidate; retain scoped statuses'
    return 'recovered-working-game-or-source; reconcile by canon manifest'
def main():
    inventory=A/'GITHUB_GAME_CONTENT_INVENTORY_2026-10-11.json';report=A/'GITHUB_DELIVERY_CONTENT_BOUNDARIES_2026-10-11.json'
    assert not inventory.exists() and not report.exists()
    assert git('status','--porcelain=v1')==b''
    head=git('rev-parse','HEAD').decode().strip();remote=git('remote','get-url','origin').decode().strip()
    live=git('ls-remote','--heads','origin','main').decode().strip().split()[0];assert head==live
    tree=[]
    for record in git('ls-tree','-r','--long','-z','HEAD').split(b'\0'):
        if not record:continue
        meta,name=record.split(b'\t',1);mode,kind,oid,size=meta.decode().split();name=name.decode('utf-8')
        row={'path':name,'mode':mode,'type':kind,'gitObject':oid,'bytes':None if size=='-' else int(size)}
        if kind=='blob':
            p=G/name
            if long(p).is_file():
                raw=long(p).read_bytes();blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
                row.update({'workingFilePresent':True,'workingSha256':hashlib.sha256(raw).hexdigest(),'workingGitBlob':blob,'comparison':'unchanged' if blob==oid else 'changed'})
            else:row.update({'workingFilePresent':False,'comparison':'not present at same recovered-root path; preserve tracked history'})
        else:
            row['comparison']='existing repository pointer; preserve unless explicitly reconciled'
            row['commitAvailableLocally']=git('cat-file','-t',oid).decode().strip()=='commit'
            row['isAncestorOfDeliveryHead']=subprocess.run(['git','merge-base','--is-ancestor',oid,head],cwd=D,capture_output=True).returncode==0
        tree.append(row)
    exclusions=['node_modules','.git','__pycache__','.next','dist','build','.cache','out']
    args=['rg','--files','--hidden','--no-ignore','-g','!Descent assets/**']
    for name in exclusions:args+=['-g',f'!**/{name}/**']
    names=subprocess.run(args,cwd=G,capture_output=True,text=True,encoding='utf-8',check=True).stdout.splitlines()
    entries=[];failed=[];byhash=defaultdict(list)
    for n,name in enumerate(names):
        name=name.replace('\\','/');p=G/name
        try:
            original=long(p).stat();h=sha(p);after=long(p).stat()
            assert original.st_size==after.st_size and original.st_mtime_ns==after.st_mtime_ns,'File changed during read'
            item={'path':name,'bytes':original.st_size,'sha256':h,'category':classify(name)}
            entries.append(item);byhash[h].append(name)
        except (OSError,AssertionError) as e:failed.append({'path':name,'error':str(e)})
        if n and n%3000==0:print(f'Fingerprinted {n} files...',flush=True)
    assert not failed,failed
    groups=defaultdict(lambda:{'files':0,'bytes':0})
    for row in entries:groups[row['category']]['files']+=1;groups[row['category']]['bytes']+=row['bytes']
    duplicates=[{'sha256':h,'paths':p} for h,p in byhash.items() if len(p)>1]
    write(inventory,{'atUtc':datetime.now(timezone.utc).isoformat(),'root':str(G),'scope':'All rg-enumerated files outside the separate Descent assets tree and named generated/dependency directories. Opaque bytes only; not publication selection or semantic/cosmology review.',
        'excludedDirectoryNamesAtAnyDepth':exclusions,'excludedTopLevelTree':'Descent assets','files':entries,'duplicateByteGroups':duplicates,'failed':failed,
        'duplicateMeaning':'Exact byte identity is not obsolescence or deletion approval. Preserve path, audience, source and historical roles.'})
    evidence_paths=['Descent assets/README.md','Descent assets/tools/README-conversion.md','Descent assets/readme.txt','Descent assets/web/public/assets/manifest.json','README.md','package.json','DescentReviewChanges/ReviewBible/package.json','.gitignore','DescentReviewChanges/ReviewBible/.gitignore','src/data/CONTINUITY_REPORT.md','src/data/CONTENT_GAPS.md','src/data/content-gap-report.json']
    source_evidence={name:{'sha256':sha(G/name),'bytes':long(G/name).stat().st_size} for name in evidence_paths}
    search=subprocess.run(['rg','-n','-i','--glob','*.{js,ts,tsx,json,mjs,cjs,md}','--glob','!package-lock.json','--glob','!bun.lock*','Descent assets|swtor|\\.tor\\b|\\.gr2\\b','src','scripts','tools','package.json','next.config.js'],cwd=G,capture_output=True,text=True,encoding='utf-8')
    assert search.returncode in [0,1]
    literal_hits=search.stdout.splitlines()
    app_images=[G/'public/banner-image.png',G/'Images/Banner Image.png',R/'public/banner-image.png',R/'Images/Banner Image.png']
    lab_images=[p for p in (G/'Descent assets/web/public/assets').rglob('*') if p.is_file() and p.suffix.lower() in ['.png','.jpg','.jpeg','.webp','.gif']]
    lab_hashes=defaultdict(list)
    for p in lab_images:lab_hashes[sha(p)].append(rel(p))
    image_comparison=[{'path':rel(p),'sha256':sha(p),'exactWorkbenchImageMatches':lab_hashes.get(sha(p),[])} for p in app_images]
    size=read(A/'GITHUB_DELIVERY_SIZE_SCREENING_2026-10-11.json')
    result={'atUtc':datetime.now(timezone.utc).isoformat(),'status':'Read-only delivery boundaries and preservation inventory; final joint package selection pending',
        'remote':remote,'verifiedRemoteMain':live,'deliveryHead':head,'deliveryClean':True,'trackedTreeEntries':len(tree),'trackedBlobFiles':sum(x['type']=='blob' for x in tree),'trackedRepositoryPointers':sum(x['type']=='commit' for x in tree),
        'trackedComparisonCounts':dict(Counter(x['comparison'] for x in tree)),'trackedTree':tree,'gitmodulesInCurrentHead':bool(git('ls-tree','HEAD','.gitmodules')),
        'nonAssetGameInventory':{'file':inventory.name,'sha256':sha(inventory),'files':len(entries),'bytes':sum(x['bytes'] for x in entries),'categories':dict(groups),'exactDuplicateByteGroups':len(duplicates),'above100MiB':[x['path'] for x in entries if x['bytes']>100*1024*1024]},
        'assetLab':{'previousSizeScreenAtUtc':size['atUtc'],'historicalBaseline':size['topLevelGroups']['Descent assets'],'filesTrackedInDeliveryHead':[x['path'] for x in tree if x['path'].startswith('Descent assets/')],
          'readmeFact':'Descent assets/README.md describes a separate local visual sketch workbench using ripped disc assets. Conversion notes describe .tor extraction, DDS conversion, Granny/GR2 conversion and portable Blender.',
          'existingProductBoundaryEvidence':['src/data/CONTINUITY_REPORT.md:15','src/data/CONTENT_GAPS.md:5','src/data/content-gap-report.json:4'],
          'candidateDisposition':'Keep the whole asset-lab tree preserved locally and account for it separately in final delivery. Do not silently copy its imported packs, converted textures or bundled software into the consolidated TTRPG Git package.',
          'finalDispositionConfirmed':False,'rightsDeterminationMade':False,'filesDeleted':0},
        'scopedMainProductLiteralScan':{'targets':['src','scripts','tools','package.json','next.config.js'],'matches':literal_hits,'scope':'Static literal matches only; returned references are existing continuity/toolkit metadata. Not a build dependency graph or proof of artwork ownership.'},
        'imageByteComparison':{'workbenchImagesCompared':len(lab_images),'mainImages':image_comparison,'scope':'Exact byte equality only; no match cannot establish origin, transformation history or permission.'},
        'readmeLicenseObservation':'The main README License section contains only the project description. No license is chosen or added by this audit; publication/license decisions remain distinct from the authorized later repository push.',
        'sourceEvidenceHashes':source_evidence,'preservationRules':['Retain existing tracked entries, including the ancestor commit pointer and tracked cache, until an explicit joint reconciliation permits any removal.','Do not infer obsolescence from identical bytes; source paths and audience may have distinct roles.','Browser screenshots require separate handling because some capture unrelated sidebar information. Task-only text verdict files are not automatically excluded merely because their name contains BROWSER.','Reviewed public and Director material keep their audience classifications; a Git delivery does not certify the current browser app audience filtering.'],
        'notPerformed':['No source moves or deletions','No copied authoring files in delivery checkout','No .gitignore changes','No new commit or push','No license/right-to-distribute conclusion','No source semantics or cosmology review','No whole-game acceptance or publication claim']}
    assert git('status','--porcelain=v1')==b''
    write(report,result)
    print(json.dumps({'trackedEntries':len(tree),'blobs':result['trackedBlobFiles'],'gitlinks':result['trackedRepositoryPointers'],'workingComparisons':result['trackedComparisonCounts'],'inventoryFiles':len(entries),'inventoryBytes':result['nonAssetGameInventory']['bytes'],'duplicateGroups':len(duplicates),'mainImages':image_comparison,'sourceChanges':0},indent=2))
if __name__=='__main__':main()
