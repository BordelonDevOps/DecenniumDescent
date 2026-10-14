"""Preserve then propagate the actual GPT Nature source completion once."""
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json, shutil
from feat_exact_01_casting_credential_model import at
from validate_feat_exact_01_composite_casting import read, info
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
V=A/'feat335-nature-source-check-01-verdict'


def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')


def put(d,pointer,value):
    parent,key=pointer.rsplit('/',1);o=at(d,parent) if parent else d
    o[int(key) if isinstance(o,list) else key]=value


def main():
    report_path=A/'FEAT335_NATURE_SOURCE_PROPAGATION_CHECK.json';delta=A/'FEAT335_NATURE_DERIVED_OPERATIONS.json'
    record_path=A/'FEAT335_NATURE_SOURCE_CHECK_01_CONTROLLING_RECORD.json';preservation=A/'source-before-feat335-nature-completion'
    assert all(not p.exists() for p in [report_path,delta,record_path,preservation])
    receipt=read(A/'FEAT335_NATURE_SOURCE_CHECK_01_REPRODUCED.json');assert receipt['checks']==124 and receipt['jsonReportEqual']
    corrections=read(V/'EXACT_NATURE_CORRECTIONS.json');operations=corrections['operations'];checks=[];changes=[];prepared={};befores={}
    def check(label,condition):
        checks.append({'id':label,'passed':bool(condition)});assert condition,label
    for op in operations:
        p=G/op['path'];before=p.read_bytes();befores[p]=before
        check(op['id']+'/exact-full-file',len(before)==op['expectedFileBytes'] and sha256(before).hexdigest()==op['expectedFileSha256'])
        is_json=op['op']=='replace_json_string'
        old=json.dumps(op['old'],ensure_ascii=False).encode() if is_json else op['old'].encode()
        new=json.dumps(op['replacement'],ensure_ascii=False).encode() if is_json else op['replacement'].encode()
        check(op['id']+'/one-old-token',before.count(old)==op['expectedOccurrences']==1)
        after=before.replace(old,new,1);check(op['id']+'/exact-byte-inverse',after.count(new)==1 and after.replace(new,old,1)==before)
        if is_json:
            original=json.loads(before);updated=json.loads(after)
            check(op['id']+'/pointer-value',at(original,op['pointer'])==op['old'] and at(updated,op['pointer'])==op['replacement'])
            for guard in op.get('recordGuards',[])+([op['recordGuard']] if 'recordGuard' in op else []):
                check(op['id']+'/identity/'+guard['pointer'],at(original,guard['pointer'])==guard['equals'])
            restored=deepcopy(updated);put(restored,op['pointer'],op['old']);check(op['id']+'/all-other-fields',restored==original)
        check(op['id']+'/reviewer-descendant-equal',after==(V/'reference_descendants'/op['path']).read_bytes())
        prepared[p]=after
    borrowed=operations[2];old=json.dumps(borrowed['old'],ensure_ascii=False).encode();new=json.dumps(borrowed['replacement'],ensure_ascii=False).encode()
    mirrors=[(R/'data/director/feat_candidates/exact_01/supplements.json','/groups/8/completeAuthoringValue/5/proposedBorrowedProcedure',2),
        (R/'data/director/feat_candidates/exact_01/cohorts/heritage_mutation.json','/newFiniteBorrowingMenu/5/proposedBorrowedProcedure',1),
        (R/'docs/feats/exact-candidate-01/SUPPLEMENTS.md',None,1)]
    for p,pointer,count in mirrors:
        before=p.read_bytes();befores[p]=before
        check(p.name+'/mirror-old-count',before.count(old)==count)
        # In the internal SUP envelope the first occurrence is historical
        # /original; the second is the operative completeAuthoringValue.
        prefix,sep,suffix=before.rpartition(old);assert sep
        after=prefix+new+suffix
        check(p.name+'/mirror-byte-inverse',after.count(new)==1 and after.replace(new,old,1)==before)
        if pointer:
            original=json.loads(before);updated=json.loads(after)
            check(p.name+'/current-pointer',at(original,pointer)==borrowed['old'] and at(updated,pointer)==borrowed['replacement'])
            restored=deepcopy(updated);put(restored,pointer,borrowed['old']);check(p.name+'/other-fields-preserved',restored==original)
        prepared[p]=after
    public=R/'data/public/feat_candidates/exact_01/supplements.json';native=R/'data/public/class_playtests/ranger.json'
    old_s=read(public);new_s=json.loads(prepared[public]);old_r=read(native);new_r=json.loads(prepared[native])
    internal=R/'data/director/feat_candidates/exact_01/supplements.json';cohort=R/'data/director/feat_candidates/exact_01/cohorts/heritage_mutation.json'
    internal_rows=json.loads(prepared[internal])['groups'][8]['completeAuthoringValue']
    check('public-internal-current-SUP09-parity',len(internal_rows)==len(new_s['groups'][8]['value']) and all(
        public_row=={k:internal_row[k] for k in public_row}
        for public_row,internal_row in zip(new_s['groups'][8]['value'],internal_rows)))
    check('historical-SUP09-original-unchanged',read(internal)['groups'][8]['original']==json.loads(prepared[internal])['groups'][8]['original'])
    check('cohort-current-borrowed-procedure-parity',json.loads(prepared[cohort])['newFiniteBorrowingMenu'][5]['proposedBorrowedProcedure']==new_s['groups'][8]['value'][5]['proposedBorrowedProcedure'])
    check('cohort-bound-source-snapshots-preserved',read(cohort)['completeBorrowingClassSourceComparisons']==json.loads(prepared[cohort])['completeBorrowingClassSourceComparisons'])
    check('cohort-native-source-snapshot-preserved',read(cohort)['newFiniteBorrowingMenu'][5]['completeCurrentSourceCard']==json.loads(prepared[cohort])['newFiniteBorrowingMenu'][5]['completeCurrentSourceCard'])
    check('native-complete-rule-in-borrowed-wrapper',new_s['groups'][8]['value'][5]['proposedBorrowedProcedure'].endswith(new_r['cards'][7]['effect']))
    for i,row in enumerate(old_s['groups'][8]['value']):
        if i!=5:check('other-SUP09-row/'+row['sourceId'],row==new_s['groups'][8]['value'][i])
    for i,group in enumerate(old_s['groups']):
        if i!=8:check('other-supplement/'+group['id'],group==new_s['groups'][i])
    for i,card in enumerate(old_r['cards']):
        if i!=7:check('other-Ranger-card/'+card['id'],card==new_r['cards'][i])
    for key in old_r['cards'][7]:
        if key!='effect':check('Nature-field-preserved/'+key,old_r['cards'][7][key]==new_r['cards'][7][key])
    immutable=[R/'data/public/feat_candidates/exact_01/candidate.json',A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',
        R/'data/public/feat_candidates/exact_01/shared_rules.json',R/'data/director/heritage_mutation_feat_operating_proposal_internal.json',
        A/'FEAT335_BORROWED_SKILL_TRANSACTIONS_CHECK.json',R/'tools/feat335_borrowed_stunts.py',
        R/'tools/feat335_borrowed_transactions.py',R/'tools/feat335_borrowed_skill_transactions.py']
    fixed=[info(p) for p in immutable];now=datetime.now(timezone.utc).isoformat();preserved=[]
    for p,after in prepared.items():
        check(p.name+'/no-concurrent-source-change',p.read_bytes()==befores[p])
        dest=preservation/p.relative_to(G);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
        check(p.name+'/exact-preserved-bytes',dest.read_bytes()==befores[p])
        before={**info(p),'preservedCopy':dest.relative_to(G).as_posix()};preserved.append(before)
    save(preservation/'PRESERVATION_MANIFEST.json',preserved)
    for p,after in prepared.items():
        p.write_bytes(after);check(p.name+'/written-exact-descendant',p.read_bytes()==after)
        changes.append({'before':next(x for x in preserved if x['path']==p.relative_to(G).as_posix()),'after':info(p)})
    check('immutable-feats-contracts-original-proposals-and-old-models',fixed==[info(p) for p in immutable])
    save(delta,{'reviewId':'FEAT335-NATURE-SOURCE-CHECK-01','recordedAtUtc':now,'changes':changes,'directOperations':3,'derivedMirrors':3,'sourceInformationDeleted':0})
    record=read(V/'NATURE_CONTROLLING_RECORD.json');record.update(recordedAtUtc=now,
        localMeasuredDescendants=[x['after'] for x in changes],preservationManifest=info(preservation/'PRESERVATION_MANIFEST.json'),
        reproducedEvidence=info(A/'FEAT335_NATURE_SOURCE_CHECK_01_REPRODUCED.json'),derivedOperations=info(delta),
        finiteFollowthroughStatus='Not yet executed; all16 NWT groups remain required.',
        historicalSnapshotQualification='Embedded original/completeCurrentSourceCard/completeBorrowingClassSourceComparisons fields remain exact earlier source snapshots. Current Nature effect and borrowed procedure are resolved through this appended controlling record and its measured descendants.')
    save(record_path,record)
    save(report_path,{'recordedAtUtc':now,'status':'pass','checks':len(checks),'failures':[],'results':checks,
        'controllingRecord':info(record_path),'currentDescendants':[x['after'] for x in changes],
        'unchangedEvidence':fixed,'scope':'Three exact GPT amendments and three current mirrors with byte inverse and field/card preservation. Original source and previously executed reports/models remain unchanged.',
        'finiteNatureUseExecuted':False,'fullFeatExactApproved':False,'runtimeApproved':False,'cosmologyReviewed':False,'sourceInformationDeleted':0})
    print(json.dumps({'checks':len(checks),'files':len(changes),'report':info(report_path)}))


if __name__=='__main__':main()
