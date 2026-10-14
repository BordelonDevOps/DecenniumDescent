"""Apply only LAX-01--03, preserve originals, then verify before scoped labels.

One-use repository fulfillment. External reviewer scripts were inspected before use.
No gameplay, source catalog, runtime, publishing or cosmology changes.
"""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
from copy import deepcopy
from zipfile import ZipFile
import hashlib, json, re, shutil, subprocess, sys

R=Path(__file__).resolve().parents[1]; G=R.parents[1]
A=G/'docs/audit/2026-10-08/full-game'; V=A/'language-exact-reviewer-files'
W=Path('C:/Users/cbord/Documents/ChatGPT/Decennium Descent/lax-exact-fulfillment')
B='DescentReviewChanges/ReviewBible'; AR='docs/audit/2026-10-08/full-game'
P=B+'/data/playtest/language_communication_candidate_public.json'
I=B+'/data/director/language_communication_candidate_internal.json'
GUIDE=B+'/docs/mechanics/LANGUAGE_COMMUNICATION_PLAYTEST.md'
IG=B+'/docs/director-only/LANGUAGE_COMMUNICATION_INTERNAL_CANDIDATE.md'
WG=B+'/docs/mechanics/LANGUAGE_COMMUNICATION_WORKED_SEQUENCES.md'
CASE=AR+'/LANGUAGE_CANDIDATE_WORKED_ADJUDICATIONS.json'
VALIDATOR=B+'/tools/validate_language_candidate.py'
REPORT=AR+'/LANGUAGE_CANDIDATE_VALIDATION.json'

def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def hashes(paths): return {p:sha(G/p) for p in paths}
def run(*args): subprocess.run([sys.executable,'-X','utf8',*map(str,args)],check=True)

def set_pointer(obj,pointer,value):
    parts=pointer.strip('/').split('/'); current=obj
    for n,part in enumerate(parts):
        match=re.fullmatch(r'([^\[]+)\[id=([^\]]+)\]',part)
        last=n==len(parts)-1
        if match:
            rows=current[match[1]]; found=[k for k,x in enumerate(rows) if x['id']==match[2]]
            assert len(found)==1
            if last: rows[found[0]]=deepcopy(value)
            else: current=rows[found[0]]
        elif last: current[part]=deepcopy(value)
        else: current=current[part]

def main():
    assert not W.exists(), 'One-use fulfillment already started; inspect state before resuming.'
    W.mkdir(); frozen=W/'frozen'; frozen.mkdir()
    archive=A/'DD_Language_Communication_Exact_Review_v1.zip'
    assert sha(archive)=='788e1210d28120b5e94a6ddc4d1dcc69e48a2aeb7cfd60f434c9680b30fa2ec1'
    with ZipFile(archive) as z:
        manifest=json.loads(z.read('FILE_MANIFEST.json'))
        assert len(manifest)==184 and len(z.namelist())==185
        for name in z.namelist():
            path=PurePosixPath(name)
            assert not path.is_absolute() and '..' not in path.parts and ':' not in name and '\\' not in name
            target=frozen/name; target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes(z.read(name))
        for p,e in manifest.items(): assert sha(frozen/p)==e['sha256']
    originals=read(frozen/'ORIGINAL_SOURCE_V2_FILE_MANIFEST.json')
    assert len(originals)==152
    for p,e in originals.items(): assert sha(G/p)==e['sha256']
    spec=read(V/'LAX_CORRECTIONS.json')
    targets=sorted({x['file'] for c in spec['corrections'] for x in c['affected']})
    assert set(targets)=={P,I,GUIDE,IG,WG,CASE,VALIDATOR}
    backup=A/'language-before-lax-fulfillment'; assert not backup.exists(); backup.mkdir()
    before=hashes(targets+[REPORT])
    for p in targets+[REPORT]:
        assert sha(G/p)==sha(frozen/p),p
        dest=backup/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(G/p,dest)
    write(backup/'FILE_MANIFEST.json',{p:{'sha256':h,'bytes':(G/p).stat().st_size} for p,h in before.items()})
    documents={p:(read(G/p) if p.endswith('.json') else (G/p).read_text(encoding='utf-8-sig')) for p in targets}
    applications=[]
    for c in spec['corrections']:
        for edit in c['affected']:
            p=edit['file']; locator=edit.get('pointer',edit.get('section'))
            if 'old' in edit:
                assert documents[p].count(edit['old'])==1,(c['id'],p)
                documents[p]=documents[p].replace(edit['old'],edit['replacement'])
            elif 'insert' in edit:
                following='LA-16' if c['id']=='LAX-02' else 'LA-15'
                anchor='### '+following+' — '
                assert documents[p].count(anchor)==1
                documents[p]=documents[p].replace(anchor,edit['insert']+'\n\n'+anchor)
            elif 'replacement' in edit:
                set_pointer(documents[p],edit['pointer'],edit['replacement'])
            else:
                assert 'replacementRule' in edit
            applications.append({'correction':c['id'],'file':p,'location':locator,'operation': 'exact replacement' if 'replacement' in edit else 'exact insertion' if 'insert' in edit else 'derived full rendering'})
    documents[P]['guideText']=documents[GUIDE]
    t30=next(x for x in documents[CASE]['cases'] if x['id']=='LA-T30')
    heading='## LA-T30 — '+t30['title']+'\n\n'
    previous=documents[WG].split(heading,1)[1].split('\n## ',1)[0]
    replacement=t30['setup']+'\n\n'+'\n'.join(f"{s['step']}. {s['event']}" for s in t30['chronology'])+'\n\n**Outcome:** '+t30['adjudicatedOutcome']+'\n'
    documents[WG]=documents[WG].replace(heading+previous,heading+replacement)
    for p,d in documents.items():
        if isinstance(d,dict): write(G/p,d)
        else: (G/p).write_text(d,encoding='utf-8')
    prelabel=hashes(targets)
    for p,e in originals.items(): assert sha(G/p)==e['sha256']
    write(A/'LANGUAGE_EXACT_CORRECTION_APPLICATIONS.json',{'reviewId':'LAX-EXACT-2026-10-11','beforeHashes':before,'correctedPreLabelHashes':prelabel,'applications':applications,'approvalGranted':False})

    # Immutable submission reproduction retains its six expected findings.
    run(V/'verify_language_exact_review.py',frozen,'--archive',archive,'--output',W/'frozen-audit.json')
    baseline=read(W/'frozen-audit.json'); assert baseline['count']==711 and baseline['passed']==705 and len(baseline['failed'])==6
    shutil.copy2(W/'frozen-audit.json',A/'LANGUAGE_EXACT_FROZEN_REPRODUCTION.json')
    run(A/'language-source-reviewer-files/verify_language_source_packet.py',A/'DD_Language_Communication_Source_Prepared_v2.zip','--output',A/'LANGUAGE_EXACT_FULFILLMENT_SOURCE_460.json')
    source=read(A/'LANGUAGE_EXACT_FULFILLMENT_SOURCE_460.json'); assert source['count']==460 and not source['failed']
    run(G/VALIDATOR)
    candidate=read(G/REPORT); assert candidate['candidateChecks']==496 and not candidate['failed']
    assert candidate['groups']['executed-reference-arithmetic']==20 and candidate['groups']['executed-reference-boundaries']==18
    shutil.copy2(G/REPORT,A/'LANGUAGE_EXACT_FULFILLMENT_CANDIDATE_496.json')
    run(V/'verify_lax_named_corrections.py',frozen,G,'--output',W/'focused-owner.json')
    focused=read(W/'focused-owner.json'); assert focused['count']==focused['passed']==44 and not focused['failed']
    shutil.copy2(W/'focused-owner.json',A/'LANGUAGE_EXACT_FULFILLMENT_FOCUSED_44.json')

    # Prove the corrected reading path using only the original archive membership.
    portable=W/'portable-corrected';shutil.copytree(frozen,portable)
    for p in targets:
        shutil.copy2(G/p,portable/p)
    run(portable/VALIDATOR)
    portable_result=read(portable/REPORT);assert portable_result['candidateChecks']==496 and not portable_result['failed']
    shutil.copy2(portable/REPORT,A/'LANGUAGE_EXACT_FULFILLMENT_PORTABLE_496.json')
    assert hashes(targets)==prelabel
    stage=A/'language-lax-pre-label';stage.mkdir()
    for p in targets:
        dest=stage/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(G/p,dest)
    receipt={'reviewId':'LAX-EXACT-2026-10-11','requestId':'b152ba58-ee3a-4a1b-bcbe-4d7cc27e55cb','replyId':'12106bf1-18cf-41ee-b0df-8e5a8714d143',
             'atUtc':datetime.now(timezone.utc).isoformat(),'status':'All three exact corrections fulfilled against actual repository files; label normalization permitted',
             'authorityFile':str((V/'LAX_Language_Communication_Exact_Verdict.md').relative_to(G).as_posix()),'authoritySha256':sha(V/'LAX_Language_Communication_Exact_Verdict.md'),
             'beforeHashes':before,'correctedPreLabelHashes':prelabel,'applications':applications,
             'actualChecks':{'source':460,'candidate':496,'candidateReferenceArithmeticAndBoundaries':38,'focused':44,'focusedReferenceFixtures':14,'focusedStaticSourceComparisons':30,'standaloneCandidate':496},
             'checkScope':'Counts overlap. Static/source comparisons and finite reference fixtures; 32 semantic authored case dispositions, zero game-runtime or human tests.',
             'original152PayloadsUnchanged':True,'frozenSubmissionPreserved':True,'classSpellFeatPromotion':False,'runtimeImplemented':False,'humanBalanceApproved':False,'wholeGameFlowApproved':False,'cosmologyReviewed':False,
             'preparedReferenceAddendumDisposition':'Preserved but unnecessary and not submitted; final LAX-01 instead names exact replacement links to already-supplied complete public collections.'}
    write(A/'LANGUAGE_EXACT_FULFILLMENT_PRE_LABEL.json',receipt)

    label_edits={GUIDE:[('**Authored candidate v1 — exact joint review pending.**','**Reviewed authored language/communication playtest v1.1.**'),
                       ('exact joint review and broader integration remain open.','the authored language review is complete; broader game integration and human playtesting remain open.')],
                 WG:[('**Candidate v1; exact review pending.**','**Reviewed authored language/communication playtest v1.1.**')],
                 IG:[('**LA-CANDIDATE-v1; authored candidate, exact joint review pending. Director-only.**','**LA-CANDIDATE-v1.1; reviewed authored language/communication playtest. Director-only.**'),
                     ('Candidate implementation; exact review pending.','Reviewed language application; source-card statuses unchanged.')]}
    normalized={p:deepcopy(d) for p,d in documents.items()}
    label_proof=[]
    for p,edits in label_edits.items():
        for old,new in edits:
            n=normalized[p].count(old);assert n==(16 if old.startswith('Candidate implementation;') else 1),(p,old,n)
            normalized[p]=normalized[p].replace(old,new)
            label_proof.append({'file':p,'old':old,'replacement':new,'occurrences':n})
    for p in [P,I]:
        normalized[p]['candidateVersion']='LA-CANDIDATE-v1.1'
        normalized[p]['status']='reviewed-authored-language-communication-playtest'
        normalized[p]['exactLanguageApproval']=True
        label_proof.append({'file':p,'changedTopLevelFields':['candidateVersion','status','exactLanguageApproval']})
    normalized[P]['guideText']=normalized[GUIDE]
    for row in normalized[I]['decisionApplicationRegister']:
        assert row['applicationStatus']=='Applied to authored candidate; awaiting exact review'
        row['applicationStatus']='Receipt preservation reviewed; no cosmology interpretation' if row['id']=='LA-16' else 'Reviewed authored language application under LAX-EXACT-2026-10-11'
    label_proof.append({'file':I,'changedApplicationStatusIds':[r['id'] for r in normalized[I]['decisionApplicationRegister']],'originalExactApprovalGrantedValuesPreserved':True})
    # Complete deep-object reversal proves the normalization contains only its stated labels.
    for p in [P,I]:
        restored=deepcopy(normalized[p])
        for k in ['candidateVersion','status','exactLanguageApproval']:restored[k]=documents[p][k]
        if p==P:restored['guideText']=documents[p]['guideText']
        else:
            for old,new in zip(documents[p]['decisionApplicationRegister'],restored['decisionApplicationRegister']):new['applicationStatus']=old['applicationStatus']
        assert restored==documents[p]
    for p,d in normalized.items():
        if p not in [P,I,GUIDE,IG,WG]:assert d==documents[p];continue
        if isinstance(d,dict):write(G/p,d)
        else:(G/p).write_text(d,encoding='utf-8')
    for p,e in originals.items(): assert sha(G/p)==e['sha256']
    assert normalized[P]['guideText']==(G/GUIDE).read_text(encoding='utf-8')
    final=hashes(targets)
    reports=['LANGUAGE_EXACT_FULFILLMENT_SOURCE_460.json','LANGUAGE_EXACT_FULFILLMENT_CANDIDATE_496.json','LANGUAGE_EXACT_FULFILLMENT_FOCUSED_44.json','LANGUAGE_EXACT_FULFILLMENT_PORTABLE_496.json','LANGUAGE_EXACT_CORRECTION_APPLICATIONS.json','LANGUAGE_EXACT_FULFILLMENT_PRE_LABEL.json']
    receipt.update({'status':'PASS — reviewed authored language/communication playtest; LAX-01–03 fulfilled', 'completedAtUtc':datetime.now(timezone.utc).isoformat(),'exactLanguageApproval':True,'finalHashes':final,'labelOnlyProof':label_proof,
                    'reportHashes':{p:sha(A/p) for p in reports},'allChangesWithinExactCorrectionsAndPermittedLabels':True,'sourceInformationDeleted':0,'pushPerformed':False})
    write(A/'LANGUAGE_EXACT_FULFILLMENT.json',receipt)
    write(R/'docs/mechanics/LANGUAGE_REVIEW_STATUS.json',{'reviewId':receipt['reviewId'],'candidateVersion':'LA-CANDIDATE-v1.1','status':receipt['status'],'fulfillmentReceipt':str((A/'LANGUAGE_EXACT_FULFILLMENT.json').relative_to(G).as_posix()),'fulfillmentSha256':sha(A/'LANGUAGE_EXACT_FULFILLMENT.json'),'finalHashes':final,'exactLanguageApproval':True,'classSpellFeatPromotion':False,'runtimeImplemented':False,'humanBalanceApproved':False,'wholeGameFlowApproved':False})
    print(json.dumps({'status':receipt['status'],'files':len(targets),'source':460,'candidate':496,'focused':44,'portable':496,'finalHashes':final},indent=2))

if __name__=='__main__':main()
