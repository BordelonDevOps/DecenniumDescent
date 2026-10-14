"""Current reading-file/casebook and explicit public-allowlist preflight.

This compares the current corrected envelopes, not the historical initial
builder's hashes, and never relabels authored examples as executed scenarios.
"""
from datetime import datetime,timezone
from pathlib import Path
import json
import re
from validate_feat_exact_01_composite_casting import read,info
from validate_feat_exact_candidate_01_structure import expected_supplement, at

R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
I=R/'data/director/feat_candidates/exact_01';U=R/'data/public/feat_candidates/exact_01';D=R/'docs/feats/exact-candidate-01'
V=A/'feat327-source-verdict'

def main():
    out=A/'FEAT335_CURRENT_READING_FILES_CHECK.json';assert not out.exists()
    checks=[];paths={Path(__file__),R/'tools/validate_feat_exact_candidate_01_structure.py'}
    def get(p):paths.add(p);return read(p)
    def txt(p):paths.add(p);return p.read_text(encoding='utf-8')
    def check(label,truth):checks.append({'id':label,'passed':bool(truth)})
    internal=get(I/'candidate.json');public=get(U/'candidate.json')
    records={x['id']:x for x in internal['records']};p={x['id']:x for x in public['feats']}
    orig=json.JSONDecoder().raw_decode(txt(R/'src/data/feats.js').split('export const feats = ',1)[1])[0]
    old={x['id']:x for x in get(R/'data/public/feat_playtests/catalog.json')['feats'] if x['operationalStatus']=='operational-playtest'}
    check('335-immutable-registry-identities',internal['original335Registry']==orig and list(p)==[x['id'] for x in orig])
    check('327-questions-and-eight-reviewed',len(records)==327 and len(old)==8 and len({r['questionId'] for r in records.values()})==327)
    common={'schemaVersion','status','sourceVerdictId','createdAtUtc','selectionEnabled','runtimeImplemented','humanBalanceApproved','wholeGameFlowApproved','sourceInformationDeleted','cosmologyReviewed'}
    check('public-top-level-allowlist',set(public)==common|{'feats','originalFeats','unchangedReviewedFeats','sourceAuthoredCandidates','deferredNullWrappers','newSupplementsAreOutsideOriginalCounts'})
    source_cache={};chapter_cache={};cases=get(I/'example_dispositions.json')['cases'];additional=get(I/'additional_boundary_expectations.json')['cases']
    check('660-original-case-dispositions-unchanged',cases==get(V/'FEAT_660_EXAMPLE_DISPOSITIONS.json')['cases'] and len(cases)==660)
    check('28-additional-case-dispositions-unchanged',additional==get(V/'FEAT_ADDITIONAL_BOUNDARY_EXPECTATIONS.json')['cases'] and len(additional)==28)
    for raw in orig:
        sid=raw['id'];row=p[sid];check(sid+'/source-including-raw-fields',row['sourceObject']==raw)
        if sid in old:
            check(sid+'/entire-reviewed-record-retained',row['unchangedReviewedRecord']==old[sid])
            check(sid+'/reviewed-allowlist',set(row)=={'id','name','reviewStatus','sourceObject','unchangedReviewedRecord'})
            continue
        i=records[sid];direction=i['sourceDirection'];sp=G/direction['sourcePath']
        if sp not in source_cache:source_cache[sp]=get(sp)
        original=at(source_cache[sp],direction['sourcePointer'])
        original_question=original['originalQuestion'] if 'originalQuestion' in original else original['originalIssue']
        original_id=original['questionId'] if 'questionId' in original else original['proposalId']
        check(sid+'/original-question',i['originalQuestion']==direction['originalQuestion']==original_question)
        check(sid+'/question-identity',i['questionId']==direction['questionId']==original_id)
        check(sid+'/original-proposal-cases-retained',direction['submittedWorkedCases']==original['workedCases'])
        check(sid+'/explicit-public-allowlist',set(row)=={'id','name','cohort','sourceObject','reviewStatus','operationalRules','workedCases','payloadOperational','selectionEnabled','exactApproved','runtimeApproved','sharedRulesRef','supplementsRef'})
        check(sid+'/complete-current-reader-fields',all(row[k]==i[k] for k in ['operationalRules','workedCases','payloadOperational','sharedRulesRef','supplementsRef']))
        check(sid+'/selection-disabled',all(row[k] is False for k in ['selectionEnabled','exactApproved','runtimeApproved']))
        check(sid+'/exact-null-boundary',row['payloadOperational']==(None if sid in {'astral_projection','planar_binding'} else row['operationalRules']))
        cohort=row['cohort']
        if cohort not in chapter_cache:chapter_cache[cohort]=txt(D/(cohort.upper()+'.md'))
        text=chapter_cache[cohort]
        check(sid+'/complete-current-procedure-in-reader',row['operationalRules'] in text)
        check(sid+'/complete-current-examples-in-reader',all(x in text for x in row['workedCases']))
    casebook=txt(D/'source-audit/CASEBOOK.md')
    for e in cases:
        path=G/e['sourcePath']
        if path not in source_cache:source_cache[path]=get(path)
        check(e['id']+'/original-position-retained',at(source_cache[path],e['sourcePointer'])==e['original'])
        position=int(e['sourcePointer'].rsplit('/',1)[1])
        check(e['id']+'/current-final-outcome',records[e['featId']]['workedCases'][position]==e['completeExpectedOutcome'])
        check(e['id']+'/whole-casebook-disposition',json.dumps(e,ensure_ascii=False,indent=2) in casebook)
    for e in additional:check(e['id']+'/whole-additional-case',json.dumps(e,ensure_ascii=False,indent=2) in casebook)
    groups=get(I/'supplements.json')['groups'];pub_groups=get(U/'supplements.json')['groups'];sup_text=txt(D/'SUPPLEMENTS.md')
    check('nine-supplement-identities',len(groups)==len(pub_groups)==9 and [g['id'] for g in groups]==[g['id'] for g in pub_groups])
    for g,pub in zip(groups,pub_groups):
        check(g['id']+'/independent-public-reconstruction',pub['value']==expected_supplement(g) and set(pub)=={'id','cohort','status','selectionEnabled','value'} and pub['selectionEnabled'] is False)
        check(g['id']+'/full-supplement-reader',json.dumps(pub['value'],ensure_ascii=False,indent=2) in sup_text)
    check('no-private-comparison-card-in-public','completeCurrentSourceCard' not in json.dumps(pub_groups))
    check('shared-rules-full-parity',get(I/'shared_rules.json')==get(U/'shared_rules.json'))
    for f in D.rglob('*.md'):
        text=re.sub(r'```.*?```','',txt(f),flags=re.S)
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):
            if not re.match(r'^[a-zA-Z]+:|^#',target):check(str(f.relative_to(D))+'/link/'+target,(f.parent/target.split('#')[0]).resolve().is_file())
    failures=[c for c in checks if not c['passed']]
    result={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'fail' if failures else 'pass',
        'checks':len(checks),'failures':failures,'sourceBindings':[info(p) for p in sorted(paths)],'results':checks,
        'scope':'Current corrected reader/public/internal envelope parity, complete327 questions,660 original/final example positions plus28 additional cases, raw fields/eight reviewed preservation, nine complete public supplement allowlists and reader links. No claim that authored examples were executed or current full-source decisions independently reapproved.',
        'counts':{'originals':335,'questions':327,'reviewedUnchanged':8,'originalCasePositions':660,'additionalCases':28,'chapters':len(chapter_cache),'supplementGroups':9},
        'authoredCasesExecuted':0,'fullFXC10Closed':False,'fullCandidateReadyForSubmission':False,
        'cadenceInterpretationPendingGPT':'FEAT335-CADENCE-CHECK-01','newGameRules':0,'sourceInformationDeleted':0}
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'report':info(out),'checks':len(checks),'failures':failures}))

if __name__=='__main__':main()
