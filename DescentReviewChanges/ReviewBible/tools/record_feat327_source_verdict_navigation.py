"""Preserve TU6 navigation, then record the actual terminal feat source verdict."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json
import shutil

G = Path(r'C:\Github\DecenniumDescent')
R = G / 'DescentReviewChanges/ReviewBible'
A = G / 'docs/audit/2026-10-08/full-game'
def read(p): return json.loads(p.read_text('utf-8'))
def info(p):
    b=p.read_bytes()
    return {'bytes':len(b),'sha256':sha256(b).hexdigest()}
def once(text,before,after):
    assert text.count(before)==1,before
    return text.replace(before,after)

download=read(A/'FEAT327_SOURCE_VERDICT_DOWNLOAD_CHECK.json')
repro=read(A/'FEAT327_SOURCE_VERDICT_LOCAL_REPRODUCTION.json')
response=read(A/'FEAT327_SOURCE_VERDICT_RESPONSE.json')
assert download['payloadsVerified']==28 and download['archiveSha256']=='9d568cfb64c37297abef37eb5ca3805c71c2f3f708ae9a58a1ba896b73139239'
assert repro['checks']==repro['passed']==3884 and repro['failed']==0
assert response['replyId']=='b50ec7da-7a7c-4975-82bb-b99d10a24134'
nav=R/'tools/build_review_map.py'
s=nav.read_text('utf-8')
s=once(s,'    featured = [\n','    featured = [\n        ("GPT feat source verdict — exact candidate pending", "docs/audit/2026-10-08/full-game/feat327-source-verdict/FEAT327_FINAL_SOURCE_VERDICT.md"),\n')
s=once(s,'    pending = [\n','    pending = [\n        ("Feat source verdict — local archive verification", "FEAT327_SOURCE_VERDICT_DOWNLOAD_CHECK.json"),\n        ("Feat source verdict — independently rerun source checks", "FEAT327_SOURCE_VERDICT_LOCAL_REPRODUCTION.json"),\n')
old='The original feat request ended in access-limitation reply6cea42e9-4628-41a0-8619-6257ec16f577, not a final verdict. GPT reported its earlier707-payload verification but unavailable readable file-tool results. The exact report is preserved and continuation of the same packet/retained findings has been requested; no feat promotion.'
new='The original access-limitation report6cea42e9-4628-41a0-8619-6257ec16f577 is preserved. Continuation a64ef367-c9d6-400f-8ba6-4a76dd7f8080 subsequently completed with actual source verdict b50ec7da-7a7c-4975-82bb-b99d10a24134. Its969891-byte archive matches the declared SHA; all28 payloads and all3884 read-only source/manuscript/reference checks were independently verified locally. GPT supplies275 retained procedures,50 exact replacements,2 null deferred wrappers,67 field operations,26 corrected examples among660 positions,28 extra authored cases,16 shared rules and15 FEX resolutions. This completes source-authoring directions only. The complete assembled exact feat candidate still requires actual review; no feat or comparison promotion occurs.'
s=once(s,old,new)
compile(s,str(nav),'exec')
folder=A/'navigation-before-feat327-source-verdict'
assert not folder.exists()
manifest={}
for p in [nav,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
    rel=p.relative_to(G).as_posix();q=folder/rel;q.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(p,q);assert info(p)==info(q)
    manifest[rel]={**info(p),'preservedCopy':q.relative_to(G).as_posix()}
(folder/'PRESERVATION_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
nav.write_text(s,encoding='utf-8',newline='\n')
print(json.dumps({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'preservedNavigationFiles':len(manifest),'sourceVerdict':response['replyId'],'exactCandidateApproved':False}))
