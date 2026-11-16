"""Verify each retained historical member against its immutable SHA-256."""
import argparse,hashlib,json,subprocess,zipfile
from pathlib import Path

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--repo',required=True,type=Path)
    parser.add_argument('--index',type=Path,default=Path(__file__).with_name('TRANSPORT_MEMBER_INDEX.json'));args=parser.parse_args()
    repo=args.repo.resolve();index=json.loads(args.index.read_text(encoding='utf-8'));bundle=args.index.parent/index['bundle']['path']
    assert bundle.stat().st_size==index['bundle']['bytes']
    with bundle.open('rb') as f:assert hashlib.file_digest(f,'sha256').hexdigest()==index['bundle']['sha256']
    cachepath=Path(subprocess.check_output(['git','rev-parse','--git-path','lfs/objects'],cwd=repo,text=True).strip())
    if not cachepath.is_absolute():cachepath=repo/cachepath
    git=subprocess.Popen(['git','cat-file','--batch'],cwd=repo,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    verified={};members=0;targets={a['archive'] for a in index['archives']}
    try:
        with zipfile.ZipFile(bundle) as z:
            for archive in index['archives']:
                for member in archive['members']:
                    keep=member['retained'];kind=keep['kind'];key=(kind,member['sha256'])
                    if 'path' in keep:assert keep['path'] not in targets and (repo/keep['path']).is_file()
                    if key not in verified:
                        h=hashlib.sha256();size=0
                        if kind=='PRESERVED_UNIQUE_MEMBER':
                            with z.open(keep['member']) as f:
                                while data:=f.read(1024*1024):h.update(data);size+=len(data)
                        elif kind=='HEAD_LFS_SHA256_VERIFIED':
                            oid=member['sha256'];p=cachepath/oid[:2]/oid[2:4]/oid
                            with p.open('rb') as f:
                                while data:=f.read(1024*1024):h.update(data);size+=len(data)
                        elif kind=='HEAD_GIT_BLOB_SHA256_VERIFIED':
                            git.stdin.write((keep['gitBlob']+'\n').encode());git.stdin.flush();head=git.stdout.readline().decode().split()
                            assert len(head)==3 and head[1]=='blob';left=int(head[2])
                            while left:
                                data=git.stdout.read(min(1024*1024,left));assert data;h.update(data);size+=len(data);left-=len(data)
                            assert git.stdout.read(1)==b'\n'
                        else:raise RuntimeError('Unknown preservation kind '+kind)
                        assert size==member['bytes'] and h.hexdigest()==member['sha256'];verified[key]=size
                    assert verified[key]==member['bytes'];members+=1
    finally:
        git.stdin.close();git.stdout.close();git.wait()
    print(json.dumps({'status':'PASS','archives':len(index['archives']),'members':members,'distinctVerifiedObjects':len(verified),'unpreservedMembers':0,'preservationBundleSha256':index['bundle']['sha256']}))

if __name__=='__main__':main()
