"""Verify or restore exact historical transport ZIPs; never rebuild their bytes.

Default is verification only. To run historical packaging/return-verification scripts,
restore their named ZIP first with --write --output-root <repository root>.
Original history and LFS payload availability are required. No purge is authorized.
"""
import argparse, hashlib, json, os, subprocess, sys
from pathlib import Path

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',required=True,type=Path)
    parser.add_argument('--index',type=Path,default=Path(__file__).with_name('TRANSPORT_MEMBER_INDEX.json'))
    parser.add_argument('--archive',help='Exact basename from the index; omit to verify all archives')
    parser.add_argument('--write',action='store_true')
    parser.add_argument('--output-root',type=Path)
    args=parser.parse_args()
    if args.write and (not args.archive or not args.output_root):parser.error('--write requires --archive and --output-root')
    repo=args.repo.resolve(strict=True);manifest=json.loads(args.index.read_text(encoding='utf-8'))
    selected=[a for a in manifest['archives'] if args.archive is None or Path(a['archive']).name==args.archive]
    if not selected:parser.error('Archive is not in this reviewed index')
    for a in selected:
        pointer=subprocess.check_output(['git','show',manifest['baseCommit']+':'+a['archive']],cwd=repo)
        if ('oid sha256:'+a['sha256']).encode() not in pointer or ('size '+str(a['bytes'])).encode() not in pointer:raise RuntimeError('Historical LFS pointer mismatch')
        cache=repo/'.git/lfs/objects'/a['sha256'][:2]/a['sha256'][2:4]/a['sha256']
        if not cache.is_file():raise RuntimeError('Exact local LFS payload missing; obtain this specific historical object before restore. No automatic bulk download is attempted.')
        dest=None;handle=None
        if args.write:
            root=args.output_root.resolve(strict=True);dest=(root/a['archive']).resolve()
            if not dest.is_relative_to(root) or not (repo/a['archive']).resolve().is_relative_to(repo):raise RuntimeError('Unsafe destination')
            if dest.exists():raise RuntimeError('Refusing to overwrite existing destination: '+str(dest))
            dest.parent.mkdir(parents=True,exist_ok=True);handle=dest.open('xb')
        digest=hashlib.sha256();length=0
        try:
            with cache.open('rb') as f:
                while data:=f.read(1024*1024):
                    digest.update(data);length+=len(data)
                    if handle:handle.write(data)
        finally:
            if handle:handle.close()
        if length!=a['bytes'] or digest.hexdigest()!=a['sha256']:raise RuntimeError('Retained historical ZIP is corrupt; do not use restored output')
        print(json.dumps({'archive':a['archive'],'bytes':length,'sha256':digest.hexdigest(),'status':'RESTORED' if args.write else 'VERIFIED_EXACT_HISTORICAL_PAYLOAD','destination':str(dest) if dest else None}),flush=True)

if __name__=='__main__':main()
