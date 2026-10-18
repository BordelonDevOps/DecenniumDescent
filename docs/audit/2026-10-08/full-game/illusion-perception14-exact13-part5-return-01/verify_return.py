#!/usr/bin/env python3
"""Verify this return manifest and optional exact original current-artifact bytes."""
from __future__ import annotations
import argparse,hashlib,json,stat,sys,zipfile
from pathlib import Path,PurePosixPath

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('archive',type=Path)
    p.add_argument('--input',type=Path)
    a=p.parse_args()
    try:
        with zipfile.ZipFile(a.archive) as z:
            ns=z.namelist()
            assert len(ns)==len(set(ns)), 'duplicate return member'
            for i in z.infolist():
                n=i.filename;q=PurePosixPath(n)
                assert not q.is_absolute() and '..' not in q.parts and '\\' not in n and ':' not in n, 'unsafe return member'
                assert not stat.S_ISLNK(i.external_attr>>16), 'symbolic link'
            assert z.testzip() is None, 'return CRC failure'
            manifest=json.loads(z.read('MANIFEST.json'))
            assert manifest['fileCount']==len(manifest['files']), 'manifest count'
            assert set(ns)=={'MANIFEST.json'}|{x['path'] for x in manifest['files']}, 'manifest membership'
            for e in manifest['files']:
                b=z.read(e['path'])
                assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'], e['path']
            acc=json.loads(z.read('ACCEPTANCE.json'))
            assert acc['requiredPointerOperations']==0 and acc['artifactMutationCount']==0
            assert len(acc['exactAcceptedArtifacts'])==8
            for e in acc['exactAcceptedArtifacts']:
                b=z.read(e['acceptedReturnPath'])
                assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'], e['name']
            original_checked=False
            if a.input:
                raw=a.input.read_bytes();ib=acc['inputArchive']
                assert len(raw)==ib['bytes'] and hashlib.sha256(raw).hexdigest()==ib['sha256'], 'original archive binding'
                with zipfile.ZipFile(a.input) as source:
                    for e in acc['exactAcceptedArtifacts']:
                        assert z.read(e['acceptedReturnPath'])==source.read(e['inputArchivePath']), e['name']
                original_checked=True
            result={'manifestFiles':manifest['fileCount'],'totalZipMembers':len(ns),'failures':0,'originalEightArtifactsCompared':original_checked}
        print(json.dumps(result,indent=2));return 0
    except (OSError,AssertionError,KeyError,ValueError,zipfile.BadZipFile) as exc:
        print(f'Return verification failed: {exc}',file=sys.stderr);return 1

if __name__=='__main__':raise SystemExit(main())
