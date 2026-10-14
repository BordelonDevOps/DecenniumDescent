#!/usr/bin/env python3
"""Create a separate, unlabelled EX58-X01 reference descendant. No source overwrite.

Usage: python apply_ex58_x01_reference.py ORIGINAL_ROOT NEW_ROOT REPORT.json
Requires this package's EX58_X01_CORRECTIONS.json alongside the script.
The original root, manifest, historical receipts and scripts are preserved.
"""
from pathlib import Path
import copy, hashlib, importlib.util, json, shutil, sys

B='DescentReviewChanges/ReviewBible'
PD=B+'/data/public/expedition_candidate/'
ID=B+'/data/director/expedition_candidate/'
MD=B+'/docs/mechanics/expedition/'
def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def info(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def pointer_parent(x,ptr):
    toks=[t.replace('~1','/').replace('~0','~') for t in ptr.strip('/').split('/')]
    for t in toks[:-1]: x=x[int(t)] if isinstance(x,list) else x[t]
    return x,int(toks[-1]) if isinstance(x,list) else toks[-1]
def change_case(c,ops):
    assert c['id']=='EX-W13'
    for op in ops:
        par,key=pointer_parent(c,op['relativePointer']);assert par[key]==op['old'],op['relativePointer'];par[key]=copy.deepcopy(op['replacement'])

def main():
    if len(sys.argv)!=4: raise SystemExit(__doc__)
    source,dest,report=map(Path,sys.argv[1:]);source=source.resolve();dest=dest.resolve();report=report.resolve()
    if dest.exists() or report.exists(): raise SystemExit('Destination/report must not exist; original is never edited.')
    if source==dest or source in dest.parents: raise SystemExit('Use a separate destination outside the original source tree.')
    corr=load(Path(__file__).with_name('EX58_X01_CORRECTIONS.json'))
    manifest=load(source/'EX58_EXACT_FILE_MANIFEST.json')
    for p,rec in manifest['files'].items(): assert info(source/p)==rec,p
    shutil.copytree(source,dest)
    pb=load(dest/(PD+'boundary_records.json')); ib=load(dest/(ID+'boundary_records.json'))
    pc=load(dest/(PD+'complete_candidate.json')); ic=load(dest/(ID+'complete_candidate.json'))
    oldcase=copy.deepcopy(pb['cases'][12]);newcase=copy.deepcopy(oldcase);change_case(newcase,corr['logicalReplacements'])
    for c in [pb['cases'][12],ib['publicEnvelope']['cases'][12],pc['components']['boundary_records']['cases'][12],pc['reading']['boundaryCases'][12],ic['completeComponents']['boundary_records']['publicEnvelope']['cases'][12]]:
        assert c==oldcase;change_case(c,corr['logicalReplacements']);assert c==newcase
    save(dest/(PD+'boundary_records.json'),pb);save(dest/(ID+'boundary_records.json'),ib);save(dest/(PD+'complete_candidate.json'),pc)
    for p in [PD+'boundary_records.json',ID+'boundary_records.json']:
        assert ic['componentBindings'][p]==manifest['files'][p]
        ic['componentBindings'][p]=info(dest/p)
    save(dest/(ID+'complete_candidate.json'),ic)
    # Standalone authored renderings: exact one-occurrence source replacements.
    p=dest/(MD+'EXPEDITION_BOUNDARY_WALKTHROUGHS.md');s=p.read_text();assert s.count(oldcase['actualSyntheticPremises'])==1
    p.write_text(s.replace(oldcase['actualSyntheticPremises'],newcase['actualSyntheticPremises']),encoding='utf-8',newline='\n')
    p=dest/(MD+'EXPEDITION_BOUNDARY_RECORDS.md');s=p.read_text();old=json.dumps(oldcase,ensure_ascii=False,indent=2);new=json.dumps(newcase,ensure_ascii=False,indent=2);assert s.count(old)==1
    p.write_text(s.replace(old,new),encoding='utf-8',newline='\n')
    spec=importlib.util.spec_from_file_location('ex58_render_only',dest/B/'tools/assemble_ex58_exact_candidate.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    (dest/(MD+'EXPEDITION_PLAYER_BOOK.md')).write_text(m.render_player(pc),encoding='utf-8',newline='\n')
    (dest/(MD+'EXPEDITION_DIRECTOR_BOOK.md')).write_text(m.render_director(ic),encoding='utf-8',newline='\n')
    changed=[]
    for p,rec in manifest['files'].items():
        if info(dest/p)!=rec: changed.append(p)
    assert set(changed)==set(corr['affectedCandidateFiles']),changed
    assert load(dest/(ID+'boundary_records.json'))['completeOriginalBoundaries']==load(source/(ID+'boundary_records.json'))['completeOriginalBoundaries']
    result={'reviewId':corr['reviewId'],'correctionId':'EX58-X01','inputArchiveSha256':corr['submissionSha256'],
            'referenceOnly':True,'labelsNormalized':False,'runtimeEnabled':False,'sourceRootUnchanged':all(info(source/p)==rec for p,rec in manifest['files'].items()),
            'onlyNamedCandidateFilesChanged':True,'unchangedOtherPayloads':len(manifest['files'])-len(changed),
            'changedFiles':{p:{'submitted':manifest['files'][p],'referenceDescendant':info(dest/p)} for p in changed},
            'history':'Original outer manifest, all 304 V3 payloads, all source deliveries, source registers/errata, source spell/class/body objects and old reports remain unchanged. Append a new fulfillment receipt; do not overwrite original hashes.'}
    save(report,result)
    print(json.dumps({'changedFiles':len(changed),'unchangedOtherPayloads':result['unchangedOtherPayloads'],'sourceRootUnchanged':result['sourceRootUnchanged']},indent=2))
if __name__=='__main__':main()
