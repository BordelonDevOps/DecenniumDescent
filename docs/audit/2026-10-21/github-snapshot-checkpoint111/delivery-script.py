"""Owner-requested preservation snapshot; never changes the shared Unity checkout."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import hashlib, io, json, os, re, subprocess, sys, zipfile

ROOT = Path('C:/Users/cbord/Documents/ChatGPT/Decennium Descent')
G = Path('C:/Github/DecenniumDescent')
D = ROOT / 'github-delivery'
W = ROOT / 'audit_work/github-snapshot-2026-10-21-checkpoint111'
REPO = W / 'isolated.git'
BASE = '9367b319e460134a3fc35b530da29ecbe6224b6a'
REMOTE = 'https://github.com/BordelonDevOps/DecenniumDescent.git'
REPORT = 'docs/audit/2026-10-21/github-snapshot-checkpoint111'
STATUS = 'SNAPSHOT_STATUS_2026-10-21_CHECKPOINT111.md'
A = 'docs/audit/2026-10-08/full-game'
CP = A + '/ACTIVE_AUTHORING_CHECKPOINT_JOINT_REVIEW_111.json'
SKIP = ['node_modules', '.git', '__pycache__', '.next', 'dist', 'build', '.cache', 'out']
TEXT = {'.json','.md','.txt','.js','.ts','.tsx','.jsx','.mjs','.cjs','.py','.ps1','.yml','.yaml','.toml','.html','.xml','.csv','.ini','.cfg','.sh'}
SECRET = [re.compile(x) for x in [rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',rb'gh[pousr]_[A-Za-z0-9]{30,}',rb'github_pat_[A-Za-z0-9_]{50,}',rb'sk-(?:proj-|svcacct-)[A-Za-z0-9_-]{40,}',rb'AKIA[0-9A-Z]{16}']]

def now(): return datetime.now(timezone.utc).isoformat()
def lp(p): return Path('\\\\?\\' + str(p.resolve()))
def sha(raw): return hashlib.sha256(raw).hexdigest()
def blob(raw): return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def js(v): return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def save(path,raw):
    path=lp(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as f:f.write(raw)
def git(*args,data=None,shared=False):
    where=['-C',str(D)] if shared else ['--git-dir='+str(REPO)]
    result=subprocess.run(['git','-c','core.longpaths=true','-c','core.autocrlf=false',*where,*args],input=data,capture_output=True)
    if result.returncode: raise RuntimeError(result.stderr.decode(errors='replace'))
    return result.stdout
def tree(ref,shared=False):
    result={}
    for row in git('ls-tree','-r','-z',ref,shared=shared).split(b'\0'):
        if row:
            meta,name=row.split(b'\t',1);mode,kind,oid=meta.decode().split()
            result[name.decode()]={'mode':mode,'oid':oid}
    return result
def reason(name):
    p=Path(name);low=name.lower();suffix=p.suffix.lower()
    if any(x.lower().startswith('.env') for x in p.parts) or suffix in ['.pem','.key','.pfx','.p12'] or p.name.lower() in ['.npmrc','credentials.json','id_rsa','id_ed25519']:return 'private configuration; preserved locally'
    if suffix in ['.tsbuildinfo','.pyc','.pyo'] or p.name=='next-env.d.ts':return 'generated compiler artifact; preserved locally'
    if suffix=='.pdf' and ('d&d 5e' in low or 'pathfinder-2e-gamemastery' in low):return 'third-party reference book; preserved locally'
    if suffix in ['.png','.jpg','.jpeg','.webp','.gif'] and (re.search(r'browser|screenshot|gpt[-_]|[-_]gpt[-_]',low) or ('docs/audit/' in low and len(p.parts)<=6 and 'character-sheet' not in low)):return 'browser capture may contain unrelated sidebar information; preserved locally'
    if suffix in ['.txt','.html'] and re.search(r'(?:_dom|browser_dom|dom_snapshot)\.',low):return 'raw browser DOM may contain unrelated sidebar information; task review evidence remains separately preserved'
    return None

archive_cache={}; archive_members=0
def inspect(name,raw,depth=0):
    global archive_members
    why=reason(name)
    if why and not why.startswith('generated'):return why
    suffix=Path(name).suffix.lower()
    if suffix in TEXT:
        if all(x in raw for x in [b'App navigation',b'Toggle sidebar',b'Chat actions']):return 'raw browser capture includes unrelated sidebar information; retained locally'
        if any(rx.search(raw) for rx in SECRET):return 'credential-pattern review required; retained locally'
    if suffix=='.zip':
        key=sha(raw)
        if key in archive_cache:return archive_cache[key]
        if depth>25:return 'nested archive exceeds bounded read-only inspection; retained locally'
        why=None
        try:
            with zipfile.ZipFile(io.BytesIO(raw)) as z:
                for item in z.infolist():
                    if item.is_dir():continue
                    archive_members+=1
                    why=inspect(item.filename,z.read(item),depth+1)
                    if why:
                        why='nested archive contains locally retained material: '+why;break
        except (zipfile.BadZipFile,RuntimeError) as e:why='archive inspection failed: '+type(e).__name__+'; retained locally'
        archive_cache[key]=why
        return why
    return None

def scan():
    assert not W.exists(), 'Preserve earlier run; do not overwrite.'
    assert git('ls-remote','origin','refs/heads/main',shared=True).decode().split()[0]==BASE
    W.mkdir(parents=True)
    save(W/'shared-checkout-before.nul',git('status','--porcelain=v1','-z',shared=True))
    baseline=tree(BASE,True)
    oldplan=json.loads((ROOT/'audit_work/github-snapshot-2026-10-20-material-forging72/plan.json').read_bytes())
    old={x['path']:x for x in oldplan['included']+oldplan['excluded']}
    args=['rg','--files','--hidden','--no-ignore','-g','!Descent assets/**']
    for part in SKIP:args+=['-g',f'!**/{part}/**']
    names=sorted(x.replace('\\','/') for x in subprocess.run(args,cwd=G,capture_output=True,text=True,encoding='utf8',check=True).stdout.splitlines())
    included=[];excluded=[];alerts=[];large=[]
    for i,n in enumerate(names):
        path=lp(G/n);assert not path.is_symlink(),n
        before=path.stat();raw=path.read_bytes();after=path.stat()
        assert (before.st_size,before.st_mtime_ns)==(after.st_size,after.st_mtime_ns),n
        row={'path':n,'bytes':len(raw),'sha256':sha(raw),'gitBlob':blob(raw)}
        changed=baseline.get(n,{}).get('oid')!=row['gitBlob']
        why=reason(n)
        prior=old.get(n)
        if not why and prior and prior['sha256']==row['sha256']:
            why=prior.get('reason')
        elif not why and changed:why=inspect(n,raw)
        if why:
            row['reason']=why;excluded.append(row)
            if 'credential-pattern' in why:alerts.append(n)
        else:
            row['changedFromBaseline']=changed
            if len(raw)>=100*1024*1024:
                row['delivery']='lossless split source';large.append(n)
            included.append(row)
        if i and i%5000==0:print(json.dumps({'filesInspected':i,'uniqueArchivesInspected':len(archive_cache)}),flush=True)
    plan={'createdAtUtc':now(),'ownerInstruction':'push what you have to github, confirm push afterwards','sourceRoot':str(G),'sharedCheckoutUntouched':str(D),'isolatedGitDirectory':str(REPO),'baseCommit':BASE,'checkpoint':CP,'included':included,'excluded':excluded,'excludedTreesPreservedLocally':['Descent assets',*SKIP],'credentialPatternAlerts':alerts,'oversizedSourcesDeliveredLosslessly':large,'uniqueChangedArchivesInspected':len(archive_cache),'archiveMembersInspected':archive_members,'trackedEntriesDeleted':0,'sourceInformationDeleted':0,'developmentPaused':True,'wholeGameComplete':False}
    save(W/'plan.json',js(plan))
    print(json.dumps({'included':len(included),'changed':sum(x['changedFromBaseline'] for x in included),'changedBytes':sum(x['bytes'] for x in included if x['changedFromBaseline']),'excluded':len(excluded),'reasons':dict(Counter(x['reason'] for x in excluded)),'credentialAlerts':alerts,'oversized':large}),flush=True)

def assemble():
    plan=json.loads((W/'plan.json').read_bytes());assert not plan['credentialPatternAlerts']
    assert not REPO.exists()
    subprocess.run(['git','-c','core.longpaths=true','clone','--bare','--shared',str(D),str(REPO)],check=True,capture_output=True)
    git('remote','set-url','origin',REMOTE)
    assert git('ls-remote','origin','refs/heads/main').decode().split()[0]==BASE
    git('read-tree',BASE)
    baseline=tree(BASE);expected={};staging=[];split=[]
    cp=json.loads(lp(G/CP).read_bytes())
    assert sha(lp(G/CP).read_bytes())=='69181f62c6273591f03daf2c5510e7777e8e4745b290f5cc2ac21c49ad3b5360'
    assert not cp['implementationApplied'] and not cp['wholeGameComplete']
    for binding in cp['canonicalHelperBaselinesUnchanged']:
        raw=lp(G/binding['path']).read_bytes();assert sha(raw)==binding['sha256'],binding['path']
    def extra(n,raw):
        p=W/'extra'/n;save(p,raw);staging.append((n,p,blob(raw)));expected[n]=blob(raw)
    for row in plan['included']:
        n=row['path'];expected[n]=row['gitBlob']
        if not row['changedFromBaseline']:continue
        raw=lp(G/n).read_bytes();assert sha(raw)==row['sha256'],n
        if row.get('delivery'):
            del expected[n]
            parts=[];prefix=REPORT+'/split-sources/'+row['sha256'][:16]+'/'+Path(n).name
            for i,start in enumerate(range(0,len(raw),48*1024*1024),1):
                piece=raw[start:start+48*1024*1024];pn=f'{prefix}.part{i:03}'
                extra(pn,piece);parts.append({'path':pn,'bytes':len(piece),'sha256':sha(piece)})
            assert sha(b''.join(lp(W/'extra'/p['path']).read_bytes() for p in parts))==row['sha256']
            split.append({'sourcePath':n,'bytes':len(raw),'sha256':row['sha256'],'parts':parts})
        else:staging.append((n,G/n,row['gitBlob']))
    notice=f'> **Latest backup — 21 October 2026:** Saved review work through checkpoint 111 is preserved. Video game only; development remains paused. Applied spell counts remain 525 reviewed / 323 pending, with 53 accepted identities awaiting integration. See [snapshot status]({STATUS}). Earlier notices remain history.\n\n'
    for n in ['README.md','START_HERE.md']:
        original=lp(G/n).read_bytes();extra(REPORT+'/source-before/'+n,original)
        staging[:]=[s for s in staging if s[0]!=n]
        extra(n,notice.encode()+original)
    status=f'''# Decennium Descent saved development — 21 October 2026

The owner requested this GitHub backup after development paused. Saved work through [checkpoint 111]({CP}) is included. Decennium Descent remains video-game-only. No new gameplay rule, canonical index, helper, or runtime implementation is applied by this delivery.

Applied spell accounting remains **525 reviewed / 323 pending / 249 standalone procedures / 173 interfaces**. **53 accepted identities remain unapplied.** This snapshot preserves the intervening source conferences, spell acceptance evidence, bestiary review and recovery records, feat casebooks and exact candidate maps, and the completed GPT response received at checkpoint 111.

The final GPT FXC07/08/09 review is preserved as the actual 53,957-byte archive, SHA256 `03db66fea6c2fe7493252824ad6c2d552a97ff6d516bed90b8ba8a96af85565b`. FXC07 and FXC08 evidence was covered. FXC09 still requires the Quickened Thought requirement-map timing correction: its maintained encounter bank persists across later actual turns; the next-START restriction belongs to the separate Bonus Action conversion. The underlying procedure is preserved. The full acquisition, gadget and maneuver evidence remains saved with its pending review status. The three empty requirement-text fields were repaired separately. No whole-feat or whole-game acceptance is claimed.

All prior tracked paths and Git history are preserved. [The manifest]({REPORT}/manifest.json) fingerprints the source snapshot and established locally retained exclusions. [Pre-push verification]({REPORT}/STAGED_VERIFICATION.json) records content verification. Dependencies, generated folders, the imported asset workbench, private configuration, external reference books, unrelated browser captures, and immutable archives containing those captures keep their established local-only treatment. Original files remain untouched. Any oversized deliverable is split losslessly with hashes and reconstruction instructions in [the split-source manifest]({REPORT}/SPLIT_SOURCES.json).

The separate Unity chat's uncommitted `engine/` and `docs/unity/` directories were not staged. This commit was assembled with an isolated Git index. The active authoring folder remains `C:\\Github\\DecenniumDescent`.

Resume from checkpoint 111 when requested. Source preservation, semantic acceptance, canonical integration, engine execution, human gameplay, balance, cosmology and final release approval remain distinct unfinished gates.
'''
    extra(STATUS,status.encode())
    extra(REPORT+'/SPLIT_SOURCES.json',js({'format':'Concatenate listed parts in order as binary bytes; verify original SHA256 before opening. Original source retained locally.','sources':split}))
    extra(REPORT+'/reassemble-sources.py',b'''"""Run with the repository root and an output folder; never overwrites an existing file."""\nfrom pathlib import Path\nimport hashlib,json,sys\nroot=Path(sys.argv[1]);out=Path(sys.argv[2])\nmanifest=json.loads(Path(__file__).with_name('SPLIT_SOURCES.json').read_bytes())\nfor source in manifest['sources']:\n    target=out/source['sourcePath'];target.parent.mkdir(parents=True,exist_ok=True)\n    digest=hashlib.sha256();size=0\n    with target.open('xb') as f:\n        for part in source['parts']:\n            raw=(root/part['path']).read_bytes()\n            assert len(raw)==part['bytes'] and hashlib.sha256(raw).hexdigest()==part['sha256']\n            f.write(raw);digest.update(raw);size+=len(raw)\n    assert size==source['bytes'] and digest.hexdigest()==source['sha256']\n    print(target)\n''')
    extra(REPORT+'/manifest.json',js(plan))
    extra(REPORT+'/delivery-script.py',Path(__file__).read_bytes())
    extra(REPORT+'/DELIVERY_CHECKPOINT.json',js({'recordedAtUtc':now(),'baseCommit':BASE,'activeCheckpoint':CP,'checkpointSha256':sha(lp(G/CP).read_bytes()),'authoredCounts':cp['authoredCounts'],'acceptedButUnapplied':cp['acceptedButUnapplied'],'implementationApplied':False,'developmentPaused':True,'wholeGameComplete':False,'sourceInformationDeleted':0,'sharedCheckoutModified':False}))
    finish(staging,expected,len(split),baseline)

def finish(staging,expected,split_count,baseline):
    inputs=''.join(json.dumps(p.resolve().as_posix(),ensure_ascii=False)+'\n' for _,p,_ in staging).encode()
    hashes=git('hash-object','-w','--stdin-paths',data=inputs).decode().splitlines()
    assert len(hashes)==len(staging)
    updates=[]
    for (n,p,oid),actual in zip(staging,hashes):
        assert actual==oid,n
        mode=baseline.get(n,{}).get('mode','100644')
        updates.append(f'{mode} {oid}\t{n}'.encode())
    git('update-index','-z','--index-info',data=b'\0'.join(updates)+b'\0')
    provisional=git('write-tree').decode().strip();actual=tree(provisional)
    assert set(baseline)<=set(actual)
    assert all(actual.get(n,{}).get('oid')==oid for n,oid in expected.items())
    changed=sum(baseline.get(n)!=v for n,v in actual.items())
    verify={'recordedAtUtc':now(),'baseCommit':BASE,'priorTrackedEntriesPreserved':len(baseline),'trackedEntriesDeleted':0,'expectedSourceAndDeliveryBlobsVerified':len(expected),'changedAndAddedEntriesBeforeThisReport':changed,'splitSourceOriginalHashesVerified':split_count,'canonicalHelperHashesUnchanged':True,'sharedUnityCheckoutNotModified':True,'developmentPaused':True,'wholeGameComplete':False}
    vn=REPORT+'/STAGED_VERIFICATION.json';vraw=js(verify);save(W/'staged-verification.json',vraw)
    vo=git('hash-object','-w','--stdin',data=vraw).decode().strip();expected[vn]=vo
    git('update-index','-z','--index-info',data=f'100644 {vo}\t{vn}\0'.encode())
    finaltree=git('write-tree').decode().strip()
    commit=git('commit-tree',finaltree,'-p',BASE,data=b'Preserve saved review work through checkpoint 111\n\nBack up sources, GPT review evidence and pending integration state. Development remains paused.\n').decode().strip()
    final=tree(commit)
    assert set(baseline)<=set(final) and all(final.get(n,{}).get('oid')==oid for n,oid in expected.items())
    git('update-ref','refs/heads/codex/checkpoint111-backup',commit)
    save(W/'expected-blobs.json',js(expected))
    save(W/'commit.json',js({'commit':commit,'tree':finaltree,'changedAndAddedEntries':changed+1,'totalEntries':len(final),'baseCommit':BASE}))
    print(json.dumps({'commit':commit,'changedAndAddedEntries':changed+1,'totalEntries':len(final),'priorTrackedEntriesPreserved':len(baseline),'splitSources':split_count,'verificationPassed':True}),flush=True)

def resume_assembly():
    assert not (W/'commit.json').exists()
    plan=json.loads((W/'plan.json').read_bytes());assert not plan['credentialPatternAlerts']
    baseline=tree(BASE);expected={};entries={}
    cp=json.loads(lp(G/CP).read_bytes())
    assert sha(lp(G/CP).read_bytes())=='69181f62c6273591f03daf2c5510e7777e8e4745b290f5cc2ac21c49ad3b5360'
    for b in cp['canonicalHelperBaselinesUnchanged']:assert sha(lp(G/b['path']).read_bytes())==b['sha256']
    for row in plan['included']:
        if row.get('delivery'):continue
        n=row['path'];expected[n]=row['gitBlob']
        if row['changedFromBaseline']:entries[n]=(n,G/n,row['gitBlob'])
    for p in (W/'extra').rglob('*'):
        if p.is_file():
            n=p.relative_to(W/'extra').as_posix();oid=blob(p.read_bytes())
            entries[n]=(n,p,oid);expected[n]=oid
    splits=json.loads((W/'extra'/REPORT/'SPLIT_SOURCES.json').read_bytes())['sources']
    for source in splits:
        raw=b''.join((W/'extra'/part['path']).read_bytes() for part in source['parts'])
        assert sha(raw)==source['sha256'] and len(raw)==source['bytes']
    repaired=Path(__file__).read_bytes();n=REPORT+'/delivery-script.py'
    save(W/'delivery-script-path-repair.py',repaired)
    entries[n]=(n,W/'delivery-script-path-repair.py',blob(repaired));expected[n]=blob(repaired)
    git('read-tree',BASE)
    finish(list(entries.values()),expected,len(splits),baseline)

def push():
    info=json.loads((W/'commit.json').read_bytes());commit=info['commit']
    remote=git('ls-remote','origin','refs/heads/main').decode().split()[0]
    assert remote in [BASE,commit], 'Remote main advanced; integrate before publishing.'
    if remote!=commit:print(git('push','origin',commit+':refs/heads/main').decode(),flush=True)
    remote=git('ls-remote','origin','refs/heads/main').decode().split()[0];assert remote==commit
    expected=json.loads((W/'expected-blobs.json').read_bytes());actual=tree(commit);baseline=tree(BASE)
    assert set(baseline)<=set(actual) and all(actual.get(n,{}).get('oid')==oid for n,oid in expected.items())
    receipt={'recordedAtUtc':now(),'sourceRoot':str(G),'isolatedGitDirectory':str(REPO),'baseCommit':BASE,'commit':commit,'remoteMain':remote,'url':REMOTE.removesuffix('.git')+'/commit/'+commit,'expectedBlobsVerified':len(expected),'priorTrackedEntriesPreserved':len(baseline),'totalCommitEntries':len(actual),'trackedEntriesDeleted':0,'sourceInformationDeleted':0,'sharedCheckoutModifiedByThisDelivery':False,'developmentPaused':True,'wholeGameComplete':False}
    save(W/'push-receipt.json',js(receipt));save(G/REPORT/'PUSH_RECEIPT.json',js(receipt))
    print(json.dumps(receipt),flush=True)

if __name__=='__main__':{'scan':scan,'assemble':assemble,'resume-assembly':resume_assembly,'push':push}[sys.argv[1]]()
