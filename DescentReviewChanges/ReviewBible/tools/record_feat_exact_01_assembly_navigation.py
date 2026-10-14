"""Preserve navigation and link the complete source-directed feat assembly."""
from pathlib import Path
from hashlib import sha256
import json
import shutil
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
def info(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':sha256(b).hexdigest()}
def read(p):return json.loads(p.read_text('utf-8'))
def once(s,b,a):
    assert s.count(b)==1,b
    return s.replace(b,a)
build=read(A/'FEAT_EXACT_CANDIDATE_01_BUILD.json');validation=read(A/'FEAT_EXACT_CANDIDATE_01_STRUCTURE_CHECK.json')
assert build['failures']==validation['failures']==0 and not build['readyForSubmission']
nav=R/'tools/build_review_map.py';s=nav.read_text('utf-8')
s=once(s,'    featured = [\n','    featured = [\n        ("Complete feat candidate — 325 procedures plus two deferred wrappers", "DescentReviewChanges/ReviewBible/docs/feats/exact-candidate-01/README.md"),\n')
s=once(s,'    pending = [\n','    pending = [\n        ("Feat candidate assembly — originals and full text", "FEAT_EXACT_CANDIDATE_01_BUILD.json"),\n        ("Feat candidate — independent public and source checks", "FEAT_EXACT_CANDIDATE_01_STRUCTURE_CHECK.json"),\n')
s=once(s,'This completes source-authoring directions only. The complete assembled exact feat candidate still requires actual review; no feat or comparison promotion occurs.',
    'This completes source-authoring directions only. The complete exact feat text is now assembled in separate internal/public envelopes and nine reader plus nine source-audit chapters:325 full procedures,two null wrappers,all335 originals/eight reviewed unchanged,660 original cases and28 extra authored cases,16 shared rules,91 convention dispositions,15 FEX resolutions and all finite supplements. All1838 curriculum placements and7 ritual placements bind their exact reviewed payloads;282 reviewed spell references and2 literal deferred receipts are preserved. Assembly9061 and independent projection/source6826 checks pass. The finite FXC state-boundary cases, full evidence package and actual exact review remain outstanding. No feat or comparison promotion occurs.')
compile(s,str(nav),'exec')
folder=A/'navigation-before-feat-exact-01-assembly';assert not folder.exists()
manifest={}
for p in [nav,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json',A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_TU6.json']:
    rel=p.relative_to(G).as_posix();q=folder/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);assert info(p)==info(q)
    manifest[rel]={**info(p),'preservedCopy':q.relative_to(G).as_posix()}
(folder/'PRESERVATION_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
nav.write_text(s,encoding='utf-8',newline='\n');print('Preserved four navigation/checkpoint originals; linked complete feat candidate assembly.')
