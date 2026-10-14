"""Record LRX finite fulfillment and reversible authored-review labels.

The complete standalone representation is retained; this does not convert it to
the older scalar catalog schema, implement a runtime, or alter protected sources.
Run once after the strict pre-label and focused reports have passed locally.
"""
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
from manifest_loader import load_protected_manifest

R=Path(__file__).resolve().parents[1]
G=R.parents[1]
A=G/'docs/audit/2026-10-08/full-game'
P=A/'low-rank136-exact-reviewer-files'
B='DescentReviewChanges/ReviewBible/'
FINAL_REPLY='5ece3872-cb87-4e1c-b14b-915859f41fef'
REVIEW='LRX-EXACT-2026-10-11'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def digest(p): return sha256(p.read_bytes()).hexdigest()
def write(p,x):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(x if isinstance(x,str) else json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def record(p): return {'bytes':p.stat().st_size,'sha256':digest(p)}
def diff(a,b,path=()):
    if type(a) is type(b) and isinstance(a,dict) and a.keys()==b.keys():
        return [d for k in a for d in diff(a[k],b[k],path+(k,))]
    if type(a) is type(b) and isinstance(a,list) and len(a)==len(b):
        return [d for i in range(len(a)) for d in diff(a[i],b[i],path+(i,))]
    return [] if a==b else [{'path':list(path),'before':deepcopy(a),'after':deepcopy(b)}]
def reversed_json(value,changes):
    out=deepcopy(value)
    for c in changes:
        node=out
        for key in c['path'][:-1]: node=node[key]
        assert node[c['path'][-1]]==c['after']
        node[c['path'][-1]]=deepcopy(c['before'])
    return out

def main():
    receipt_path=A/'LOW_RANK_136_EXACT_FULFILLMENT.json'
    assert not receipt_path.exists(), 'Do not overwrite completed fulfillment'
    strict=read(A/'LOW_RANK_136_LOCAL_STRICT_PRELABEL_PROOF.json')
    focused=read(A/'LOW_RANK_136_LOCAL_FOCUSED_REFERENCES.json')
    baseline=read(A/'LOW_RANK_136_LOCAL_EXACT_BASELINE_AUDIT.json')
    original49=read(A/'LOW_RANK_136_LOCAL_LRX01_BASELINE_VALIDATION.json')
    assert strict['checkCount']==1093 and not strict['failedChecks']
    assert focused['checkCount']==42 and not focused['failedChecks']
    assert baseline['checkCount']==5439 and not baseline['failedChecks']
    assert len(original49['checks'])==49 and all(c['pass'] for c in original49['checks'])
    assert original49['accessBoundaryTrials']==18840 and original49['ordinaryPriceTrials']==2808
    protected=load_protected_manifest(G)
    for rel,h in strict['amendedArtifactHashes'].items(): assert digest(G/rel)==h,rel
    reviewer_manifest=read(P/'FILE_MANIFEST.json')
    assert len(reviewer_manifest)==22
    for rel,e in reviewer_manifest.items(): assert record(P/rel)==e,rel
    authority=read(P/'LRX_FINAL_REVIEW_RECEIPT.json')
    assert authority['jsonFieldReplacementOperations']==16
    backup=A/'low-rank136-exact-prelabel'
    assert not backup.exists()
    prelabel={}
    for rel,h in strict['amendedArtifactHashes'].items():
        target=backup/rel
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes((G/rel).read_bytes())
        prelabel[rel]=record(target)
    write(backup/'FILE_MANIFEST.json',prelabel)
    disposition_files=['LRX_137_CARD_DISPOSITIONS.json','LRX_187_BOUNDARY_DISPOSITIONS.json','LRX_LRE_01_13_DISPOSITIONS.json']
    evidence_files=['LOW_RANK_136_LOCAL_STRICT_PRELABEL_PROOF.json','LOW_RANK_136_LOCAL_NAMED_AMENDMENTS_APPLIED.json','LOW_RANK_136_LOCAL_FOCUSED_REFERENCES.json','LOW_RANK_136_LOCAL_EXACT_BASELINE_AUDIT.json','LOW_RANK_136_LOCAL_LRX01_BASELINE_VALIDATION.json','LOW_RANK_136_LRX01_LOCAL_PREPARATION.json']
    pre_receipt={'reviewId':REVIEW,'finalReplyId':FINAL_REPLY,'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'finite-amendments-fulfilled-before-label-promotion','prelabelArtifacts':prelabel,'protectedOriginals':protected,'protectedSourceCount':342,'exactSubmission':record(A/'DD_Low_Rank_136_Exact_Review_v1.zip'),'reviewerArchive':record(A/'DD_Low_Rank_136_Exact_Verdict_and_Evidence.zip'),'dispositions':{n:record(P/n) for n in disposition_files},'localEvidence':{n:record(A/n) for n in evidence_files},'semanticOperations':16,'symmetricJsonOperations':32,'regeneratedArtifacts':8,'runtimeVerified':False,'humanPlaytested':False}
    write(A/'LOW_RANK_136_EXACT_PRELABEL_FULFILLMENT.json',pre_receipt)
    public_rel=B+'data/public/spell_playtests/candidate_low_rank_136.json'
    internal_rel=B+'data/playtest/spell_drafts/candidate_low_rank_136.json'
    changes={}
    for rel in [public_rel,internal_rel]:
        before=read(G/rel); after=deepcopy(before)
        after['version']='LR-REVIEWED-1.1'
        after['status']='REVIEWED-AUTHORED-OPERATIONAL-PLAYTEST-RUNTIME-UNIMPLEMENTED'
        after['scope']='136 reviewed complete authored ordinary-spell procedures plus the unchanged Blink receipt. LRX-01–05 fulfilled; full source/mode/access records retained. Runtime selection remains disabled because no complete adapter is implemented. Human balance and whole-game flow remain open.'
        for c in after['spells']:
            if c['operationalCandidate'] is None:
                assert c['id']=='blink'
                continue
            c['status']='reviewed-authored-operational-playtest'
            c['reviewEvidence'].update(exactCandidateApproval=True,catalogPromotionAuthorized=True,
                exactReviewId=REVIEW,finalReplyId=FINAL_REPLY,finiteCorrectionsFulfilled=['LRX-01','LRX-02','LRX-03','LRX-04','LRX-05'],
                fulfillmentReceipt='docs/audit/2026-10-08/full-game/LOW_RANK_136_EXACT_FULFILLMENT.json',
                approvalScope='Complete authored tabletop procedure; no complete runtime adapter or human balance claim.')
        edits=diff(before,after)
        assert all(e['path'][0] in ['version','status','scope'] or (e['path'][0]=='spells' and e['path'][2] in ['status','reviewEvidence']) for e in edits)
        assert reversed_json(after,edits)==before
        changes[rel]={'kind':'json','operations':edits,'reversedEqualsPrelabel':True}
        write(G/rel,after)
    for rel in [B+'data/playtest/spell_drafts/low_rank_137_authored_boundaries.json',B+'data/public/spell_playtests/low_rank_137_authored_boundaries.json']:
        before=read(G/rel);after=deepcopy(before)
        after['status']='reviewed-authored-expectations-LRX-EXACT-2026-10-11-not-runtime-results'
        edits=diff(before,after)
        assert len(edits)==1 and edits[0]['path']==['status']
        assert reversed_json(after,edits)==before
        changes[rel]={'kind':'json','operations':edits,'reversedEqualsPrelabel':True}
        write(G/rel,after)
    replacements=[
        ('# Low-rank spell candidates — complete review manuscript','# Low-rank spells — reviewed authored playtest manuscript'),
        ('**Status: 136 authored candidates awaiting exact joint review; Blink is a preserved receipt.**','**Status: 136 complete authored procedures reviewed; LRX-01–05 fulfilled. Blink remains a nonoperative receipt.**'),
        ('These separate draft cards are unavailable in the operational catalog. Their full original source records, class access and all 141 book bindings are in the companion JSON.','These complete authored procedures are approved for tabletop playtest under LRX-EXACT-2026-10-11. Their full original source records, class access and all 141 book bindings are in the companion JSON. The authored review index connects these 136 procedures with the 276 earlier reviewed entries. The older catalog and runtime selection remain unchanged; a complete adapter is not implemented.'),
        ('No source has been deleted or promoted by creating this manuscript.','All original source bytes are preserved. Only the 136 authorized authored-review labels and provenance have been promoted after the finite corrections.'),
        ('Status: **candidate-exact-review-pending**.','Status: **reviewed-authored-operational-playtest**.')]
    for rel in [B+'docs/playtest/LOW_RANK_136_CANDIDATE.md',B+'data/public/spell_playtests/candidate_low_rank_136.md']:
        text=(G/rel).read_text(encoding='utf-8');before=text
        ops=[]
        for old,new in replacements:
            count=text.count(old)
            assert count==(136 if old.startswith('Status: **candidate') else 1),(rel,old,count)
            text=text.replace(old,new);ops.append({'before':old,'after':new,'occurrences':count})
        reversed_text=text
        for op in reversed(ops):
            assert reversed_text.count(op['after'])==op['occurrences']
            reversed_text=reversed_text.replace(op['after'],op['before'])
        assert reversed_text==before
        changes[rel]={'kind':'text','operations':ops,'reversedEqualsPrelabel':True}
        write(G/rel,text)
    public=read(G/public_rel);internal=read(G/internal_rel)
    assert {k:v for k,v in public.items() if k!='spells'}=={k:v for k,v in internal.items() if k!='spells'}
    assert all(p=={k:v for k,v in i.items() if k!='internalSourceAuthoringRecord'} for p,i in zip(public['spells'],internal['spells']))
    assert sum(c['reviewEvidence']['exactCandidateApproval'] for c in public['spells'])==136
    assert all(c['selectionEnabled'] is False for c in public['spells'])
    assert load_protected_manifest(G)==protected
    catalog=read(R/'data/public/spell_playtests/catalog.json')
    by={c['id']:(i,c) for i,c in enumerate(public['spells']) if c['operationalCandidate'] is not None}
    entries=[]
    for i,s in enumerate(catalog['spells']):
        old=s['operational'] is not None
        assert not (old and s['id'] in by)
        if s['id'] in by:
            n,c=by[s['id']]
            assert c['sourceReceipt']==s
            entry={'id':s['id'],'name':s['name'],'authoredStatus':'reviewed-authored-operational-playtest','procedureFile':'candidate_low_rank_136.json','procedurePointer':f'/spells/{n}/operationalCandidate','wholeCardPointer':f'/spells/{n}','sharedRulesPointer':'/sharedRules','manuscript':'candidate_low_rank_136.md','reviewId':REVIEW,'runtimeSelectionEnabled':False}
        else:
            entry={'id':s['id'],'name':s['name'],'authoredStatus':'reviewed-authored-operational-playtest' if old else 'pending-authored-procedure','procedureFile':'catalog.json','procedurePointer':f'/spells/{i}/operational' if old else None,'wholeCardPointer':f'/spells/{i}','sourceStatus':s['status'],'priorCatalogSelectionStatusUnchanged':True}
            if s['id']=='blink': entry['authoredStatus']='receipt-only-post-push-cosmology'
        entries.append(entry)
    reviewed=sum(x['authoredStatus']=='reviewed-authored-operational-playtest' for x in entries)
    assert len(entries)==848 and len({x['id'] for x in entries})==848 and reviewed==412
    index={'schemaVersion':'1.0','status':'PARTIAL-AUTHORED-REVIEW-CATALOG','scope':'Discovery index for the complete authored procedures; read the whole referenced card and shared rules. This index never grants acquisition or runtime implementation. Preserved source catalog labels describe that older representation; this index records current authored review coverage.','authoredCounts':{'reviewed':412,'pending':436},'representationCounts':{'preservedLegacyOperationalRecords':276,'completeReviewedStandaloneProcedures':136},'sourceCatalogSha256':digest(R/'data/public/spell_playtests/catalog.json'),'standaloneEnvelopeSha256':digest(G/public_rel),'entries':entries}
    index_path=R/'data/public/spell_playtests/authored_review_index.json'
    assert not index_path.exists()
    write(index_path,index)
    proof={'reviewId':REVIEW,'scope':'Reversible review-label/provenance changes only, after the strictly verified named semantic amendments. The source catalog remains byte-identical.','prelabelArtifacts':prelabel,'changes':changes,'allReversalsEqualPrelabel':True,'finalArtifacts':{rel:record(G/rel) for rel in prelabel},'sourceCatalogUnchanged':True,'originalProtectedCount':342}
    proof_path=A/'LOW_RANK_136_EXACT_LABEL_ONLY_PROOF.json';write(proof_path,proof)
    status={'reviewId':REVIEW,'finalReplyId':FINAL_REPLY,'status':'FULFILLED-REVIEWED-AUTHORED-OPERATIONAL','mechanicalProcedures':136,'receiptOnly':['blink'],'authoredOrdinaryCounts':{'reviewed':412,'pending':436},'preservedLegacyCatalogCounts':{'operational':276,'pending':572},'authoredIndex':'data/public/spell_playtests/authored_review_index.json','completePublicEnvelope':'data/public/spell_playtests/candidate_low_rank_136.json','reviewScope':'Complete authored tabletop procedures, not an implemented full spell runtime or human balance approval.','sourceBytesModified':0,'runtimeSelectionEnabled':False,'runtimeVerified':False,'humanPlaytested':False,'wholeGameFlowApproved':False,'githubPushPerformed':False,'cosmologyReviewed':False,'fulfillmentReceipt':receipt_path.relative_to(G).as_posix(),'labelOnlyProof':proof_path.relative_to(G).as_posix(),'finalArtifacts':proof['finalArtifacts'],'authoredIndexHash':record(index_path)}
    status_path=R/'docs/mechanics/LOW_RANK_SPELL_REVIEW_STATUS.json';write(status_path,status)
    receipt={**pre_receipt,'status':'fulfilled-and-136-authored-procedures-promoted','prelabelReceipt':record(A/'LOW_RANK_136_EXACT_PRELABEL_FULFILLMENT.json'),'labelOnlyProof':record(proof_path),'finalArtifacts':proof['finalArtifacts'],'authoredReviewIndex':{'path':index_path.relative_to(G).as_posix(),**record(index_path)},'reviewStatus':{'path':status_path.relative_to(G).as_posix(),**record(status_path)},'authoredCounts':{'reviewed':412,'pending':436},'legacyCatalogUnchanged':True,'protectedOriginalsUnchanged':342,'promotedAuthoredProcedures':136,'newRuntimeImplementations':0,'blinkPromoted':False,'comparisonRecordsPromoted':0,'wholeGameFlowApproved':False,'pushPerformed':False,'cosmologyReviewed':False}
    write(receipt_path,receipt)
    print(json.dumps({k:receipt[k] for k in ['status','authoredCounts','protectedOriginalsUnchanged','promotedAuthoredProcedures','newRuntimeImplementations']}))

if __name__=='__main__': main()
