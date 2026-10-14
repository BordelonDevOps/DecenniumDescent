"""Apply the independently reproduced EX58-X01 descendant, preserving originals."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import copy
import importlib.util
import json

G=Path(r'C:\Github\DecenniumDescent')
R=G/'DescentReviewChanges/ReviewBible'
A=G/'docs/audit/2026-10-08/full-game'
P=A/'ex58-exact-gpt-verdict'
W=Path('\\\\?\\'+str(A/'ex58-exact-local-reproduction'))

def read(p): return json.loads(p.read_text('utf-8-sig'))
def info(p):
    b=p.read_bytes(); return {'bytes':len(b),'sha256':sha256(b).hexdigest()}
def save(p,d):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def parent(d,ptr):
    keys=[k.replace('~1','/').replace('~0','~') for k in ptr.lstrip('/').split('/')]
    for k in keys[:-1]: d=d[int(k)] if isinstance(d,list) else d[k]
    return d,int(keys[-1]) if isinstance(d,list) else keys[-1]

def main():
    receipt=A/'EX58_X01_FULFILLMENT.json'
    backup=A/'ex58-before-x01'
    assert not receipt.exists() and not backup.exists(), 'One-use fulfillment; preserve all prior outputs'
    corr=read(P/'EX58_X01_CORRECTIONS.json')
    ref=read(P/'EX58_REFERENCE_AMENDMENT_HASHES.json')
    baseline=read(W/'BASELINE_CHECK.json')
    corrected=read(W/'CORRECTED_REVIEW_CHECK.json')
    strict=read(W/'STRICT_CHECK.json')
    assert baseline['checks']==1584 and baseline['failed']==2
    assert all('EX58-X01' in x['name'] for x in baseline['failureDetails'])
    assert corrected['checks']==1584 and corrected['failed']==0
    assert strict['checks']==435 and strict['failed']==0
    manifest=read(W/'original/EX58_EXACT_FILE_MANIFEST.json')['files']
    assert len(manifest)==419
    current,archive_only={},[]
    for rel,expected in manifest.items():
        p=G/rel
        assert info(W/'original'/rel)==expected
        if p.is_file():
            assert info(p)==expected, 'Unexpected live change: '+rel
            current[rel]=expected
        else: archive_only.append(rel)
    assert len(current)==416 and len(archive_only)==3
    changed=set(corr['affectedCandidateFiles'])
    assert len(changed)==8 and changed==set(ref['changedFiles'])
    for rel in changed:
        assert info(W/'corrected'/rel)==ref['changedFiles'][rel]['referenceDescendant']
    # Independently rebuild all JSON amendments from the delivered exact operations.
    objects={rel:read(G/rel) for rel in changed if rel.endswith('.json')}
    assert len(corr['concreteJSONOperations'])==25
    for op in corr['concreteJSONOperations']:
        assert op['op']=='replace_json_value' and op['guardCaseId']=='EX-W13'
        container,key=parent(objects[op['path']],op['pointer'])
        assert container[key]==op['old']; container[key]=copy.deepcopy(op['replacement'])
    bindings=corr['derivedBindings']
    for rel in bindings['keysToRefresh']:
        objects[bindings['path']]['componentBindings'][rel]=info(W/'corrected'/rel)
    for rel,obj in objects.items(): assert obj==read(W/'corrected'/rel), 'Unexpected JSON difference: '+rel
    # Independently reconstruct the entire allowed public object from the internal object.
    spec=importlib.util.spec_from_file_location('x01_public_projection',R/'tools/validate_ex58_exact_candidate.py')
    validator=importlib.util.module_from_spec(spec); spec.loader.exec_module(validator)
    pubrel='DescentReviewChanges/ReviewBible/data/public/expedition_candidate/complete_candidate.json'
    intrel='DescentReviewChanges/ReviewBible/data/director/expedition_candidate/complete_candidate.json'
    assert validator.project(objects[intrel])==objects[pubrel]
    # Preserve all eight live originals before any live candidate is changed.
    preserved={}
    for rel in sorted(changed):
        target=backup/rel;target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes((G/rel).read_bytes())
        assert info(target)==manifest[rel]
        preserved[rel]={**info(target),'preservedAs':target.relative_to(G).as_posix()}
    save(backup/'PRESERVATION_MANIFEST.json',preserved)
    for rel in sorted(changed): (G/rel).write_bytes((W/'corrected'/rel).read_bytes())
    # Exact live bytes must equal the independently checked corrected tree.
    for rel,old in current.items():
        expected=ref['changedFiles'][rel]['referenceDescendant'] if rel in changed else old
        assert info(G/rel)==expected, 'Post-apply bytes: '+rel
    assert validator.project(read(G/intrel))==read(G/pubrel)
    for rel in changed: assert (backup/rel).read_bytes()==(W/'original'/rel).read_bytes()
    register=read(P/'EX58_EXACT_DISPOSITION_REGISTER.json')
    result={
        'recordedAtUtc':datetime.now(timezone.utc).isoformat(),
        'reviewId':'EX58-EXACT-2026-10-11','correctionId':'EX58-X01',
        'status':'FULFILLED — corrected EX58 authored expedition, transport, social and reputation candidate accepted within the exact verdict scope. Pre-label bytes verified.',
        'replyId':'e1b66405-efca-40d8-9986-31fe30323dff',
        'sourceVerdict':{'path':(P/'EX58_EXACT_VERDICT.md').relative_to(G).as_posix(),**info(P/'EX58_EXACT_VERDICT.md')},
        'submissionSha256':corr['submissionSha256'],
        'concreteJSONReplacements':25,'jsonViews':5,'markdownMirrors':4,'currentBindingsRefreshed':2,
        'changedCandidateFiles':{rel:{'before':manifest[rel],'preLabelCurrent':info(G/rel),'originalPreservedAs':preserved[rel]['preservedAs']} for rel in sorted(changed)},
        'reviewerChecks':{'baseline':{'checks':1584,'passed':1582,'failed':2},'corrected':{'checks':1584,'passed':1584,'failed':0},'strictReference':{'checks':435,'passed':435,'failed':0,'deliberateInvalidFixturesRejected':8}},
        'fullIndependentPublicProjectionEquality':True,'liveCorrectedMatchesVerifiedReference':True,
        'originalPayloadsPreserved':419,'originalV3PayloadsPreserved':304,
        'otherPayloadsUnchanged':411,'otherLivePayloadsUnchanged':408,'archiveOnlyPayloads':archive_only,
        'sourceDirectionsRetained':len(register['sourceDirections']),'chapterExamples':len(register['chapterExamples']),
        'transportProfiles':len(register['transportProfiles']),'auxiliaries':len(register['auxiliaryProfiles']),
        'integratedEvents':len(register['integratedEvents']),'contractFamilies':len(register['contracts']),
        'boundaryCases':len(register['boundaryCases']),'socialScenarios':len(register['socialScenarios']),
        'exactCandidateAuthoredApproval':True,'labelsNormalized':False,'sourceRulesChanged':0,
        'checksAre':'Source and byte preservation, complete projection/rendering, reference arithmetic and finite invalid-fixture rejection. Not a general gameplay runtime or human balance result.',
        'runtimeImplemented':False,'selectionEnabled':False,'humanPlaytestConfirmed':False,
        'wholeGameFlowConfirmed':False,'newPromotions':0,'sourceInformationDeleted':0,'pushPerformed':False,'cosmologyReviewed':False,
        'evidence':{str(p.relative_to(W)):info(p) for p in [W/'BASELINE_CHECK.json',W/'AMENDMENT_REPORT.json',W/'CORRECTED_REVIEW_CHECK.json',W/'STRICT_CHECK.json']},
        'next':'Separately reversible top-level review-label update; preserved old generators must not overwrite the corrected current outputs.'
    }
    save(receipt,result)
    print(json.dumps({k:result[k] for k in ['status','concreteJSONReplacements','otherPayloadsUnchanged','fullIndependentPublicProjectionEquality','exactCandidateAuthoredApproval']},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
