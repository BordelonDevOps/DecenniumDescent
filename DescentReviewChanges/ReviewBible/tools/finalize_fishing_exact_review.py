"""Promote only the repaired revision authorized by the actual FI-E01..11 verdict."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
import json,shutil,os
from build_fishing_recipe_candidate import ROOT,GAME,AUDIT,read,sha,dump,write,EXACT_AUTH

STATUS='REVIEWED — authored operational PLAYTEST Fishing recipe set'
CARD_STATUS='reviewed-authored-operational-playtest'
REPLACEMENTS={
    '**DRAFT; required exact-review corrections in progress.**':'**REVIEWED — authored operational PLAYTEST.**',
    'The Fishing source conference authorizes these NEW completions alongside the preserved recipe fields. It does not approve the finished cards.':
        'The source conference and completed FI-E01–11 exact-review corrections authorize this operational PLAYTEST candidate alongside the preserved recipe fields.',
    'The exact review has returned eleven required corrections (FI-E01–11). Its conditional authorization permits promotion only after every correction, specified regression and complete artifact-agreement check passes. This draft remains unpromoted while those repairs are in progress. Preserve the originally submitted artifacts and their hashes separately from this revision.':
        'All eleven required exact-review corrections (FI-E01–11) are fulfilled. The version-bound completion receipt records the repaired rules, original valid sequence coverage, finite regressions, exact effect paragraphs, complete audience projections and protected sources. The actual verdict authorizes this operational PLAYTEST promotion. Original submissions and historical hashes remain preserved separately.',
    'The repair completion gate must compare all cards,guides,JSON,worked cases and complete audience projections against the actual exact verdict.':
        'The completed repair gate compared all cards, guides, JSON, worked cases and complete audience projections against the actual exact verdict.'}


def disk_path(path):
    # Preserve logical GAME-relative locators while allowing the existing long
    # source-pack names inside the audit archive on Windows.
    return Path('\\\\?\\'+str(path.resolve())) if os.name=='nt' else path


def main():
    review_path=ROOT/'docs/mechanics/FISHING_REVIEW_STATUS.json';assert not review_path.exists()
    report_path=AUDIT/'FISHING_REPAIRED_COMPLETION_VALIDATION.json';report=read(report_path)
    assert report['completionGateSatisfied'] and report['recipesPromoted']==0
    assert report['conditionsSatisfied']==[f'FI-E{i:02}' for i in range(1,12)]
    assert all(c['pass'] for c in report['checks'])
    for p,h in {**report['inputHashes'],**report['regressionInputHashes']}.items():assert sha(GAME/p)==h,p
    protected=read(AUDIT/'FISHING_PART2_SUBMISSION.json')['protectedFiles']
    assert len(protected)==63 and all(sha(GAME/p)==h for p,h in protected.items())
    assert sha(AUDIT/'GPT_FISHING_EXACT_OPERATIONAL_REVIEW.md')==EXACT_AUTH['sha256']
    verdict=(AUDIT/'GPT_FISHING_EXACT_OPERATIONAL_REVIEW.md').read_text(encoding='utf-8')
    assert 'completion of these eleven repairs and their specified checks authorizes promotion without another generic conference' in verdict
    archive=AUDIT/'fishing-repaired-before-promotion'
    saved={**report['inputHashes'],**report['regressionInputHashes'],report_path.relative_to(GAME).as_posix():sha(report_path)}
    for name in ('FISHING_AUTHORING_STATUS.json','FISHING_EXACT_REPAIR_PROGRESS.json'):
        p=AUDIT/name;saved[p.relative_to(GAME).as_posix()]=sha(p)
    if archive.exists():
        assert not (archive/'MANIFEST.json').exists(),'Completed archive is immutable'
        for p in disk_path(archive).rglob('*'):
            if p.is_file():
                rel=p.relative_to(disk_path(archive)).as_posix()
                assert rel in saved and sha(p)==saved[rel],'Partial archive differs from the verified revision'
    for rel,h in saved.items():
        p=disk_path(archive/rel);p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(GAME/rel,p);assert sha(p)==h
    dump(archive/'MANIFEST.json',saved)
    normalized=[]
    for rel in report['artifactHashes']:
        p=ROOT/rel
        if p.suffix=='.json':
            before=read(p);after=deepcopy(before)
            after.update({'status':STATUS,'exactRecipeApproval':True,'exactReviewThreadId':EXACT_AUTH['threadId'],
                'exactReviewTurnId':EXACT_AUTH['turnId'],'exactReplyId':EXACT_AUTH['replyId'],
                'exactReviewConditions':report['conditionsSatisfied']})
            after['exactOperationalReviewAuthority']['completionGateSatisfied']=True
            for c in after['cards']:c['status']=CARD_STATUS
            check=deepcopy(after)
            for key in ('exactReviewThreadId','exactReviewTurnId','exactReplyId','exactReviewConditions'):check.pop(key)
            check['status']=before['status'];check['exactRecipeApproval']=False
            check['exactOperationalReviewAuthority']['completionGateSatisfied']=False
            for c,b in zip(check['cards'],before['cards']):c['status']=b['status']
            assert check==before,'Promotion changed operational content: '+rel
            dump(p,after)
        else:
            before=p.read_text(encoding='utf-8');after=before
            for old,new in REPLACEMENTS.items():after=after.replace(old,new)
            check=after
            for old,new in REPLACEMENTS.items():check=check.replace(new,old)
            assert check==before and after!=before,'Unbound manuscript promotion: '+rel
            write(p,after)
        normalized.append({'file':rel,'onlyApprovalMetadataOrScopeWordingChanged':True})
    final_hashes={p:sha(ROOT/p) for p in report['artifactHashes']}
    # Every operational byte/field has just been normalized to the fully checked
    # prepromotion revision. No numerical or behavioral change accompanies approval.
    assert all(sha(disk_path(archive/p))==h for p,h in saved.items())
    assert all(sha(GAME/p)==h for p,h in protected.items())
    receipt_path=AUDIT/'FISHING_EXACT_REPAIRS_APPLIED.json'
    receipt={'status':'PASS — FI-E01..11 fulfilled and authorized operational promotion applied',
        'operationalAuthority':{**EXACT_AUTH,'completionGateSatisfied':True},
        'conditionsSatisfied':report['conditionsSatisfied'],'prepromotionValidation':report_path.relative_to(GAME).as_posix(),
        'prepromotionValidationSha256':sha(report_path),'preservedRepairedRevision':archive.relative_to(GAME).as_posix(),
        'repairedPrepromotionHashes':report['artifactHashes'],'finalArtifactHashes':final_hashes,
        'promotionNormalizationChecks':normalized,'sourceChecks':report['sourceChecks'],
        'sequenceChecks':report['sequenceChecks'],'focusedChecks':report['focusedChecks'],
        'projectionAndIntegrationChecks':report['projectionAndIntegrationChecks'],
        'protectedInputsUnchanged':63,'recipesPromoted':44,'publicRecipesPromoted':28,
        'referenceSha256':sha(ROOT/'tools/fishing_reference.py'),'finalizerSha256':sha(Path(__file__)),
        'sourceInformationDeleted':False,'runtimeImplemented':False,'balanceApproved':False,
        'publicationApproved':False,'wholeGameFlowApproved':False,'githubPushed':False,'cosmology':'post-push only'}
    dump(receipt_path,receipt)
    manifest={'status':STATUS,'exactReviewThreadId':EXACT_AUTH['threadId'],'exactReviewTurnId':EXACT_AUTH['turnId'],
        'exactReplyId':EXACT_AUTH['replyId'],'repairsApplied':report['conditionsSatisfied'],
        'coverage':{'recipes':44,'public':28,'restricted':3,'directorOnly':13,'baseModels':9,'publicBaseModels':9,'affinities':14,'publicAffinities':13},
        'validationChecks':report['sourceChecks']+report['sequenceChecks']+report['focusedChecks']+report['projectionAndIntegrationChecks'],
        'protectedSourceAndPriorRuleArtifactsUnchanged':63,
        'artifactHashes':{(ROOT/p).relative_to(GAME).as_posix():h for p,h in final_hashes.items()},
        'validationEvidence':report_path.relative_to(GAME).as_posix(),'validationSha256':sha(report_path),
        'repairEvidence':receipt_path.relative_to(GAME).as_posix(),'repairEvidenceSha256':sha(receipt_path),
        'replyHashes':{'GPT_FISHING_EXACT_OPERATIONAL_REVIEW.md':EXACT_AUTH['sha256']},
        'aggregateReviewedRecipes':392,'remainingRecipeEffects':295,'publicReviewedRecipes':251,
        'sourceInformationDeleted':0,'runtimeImplemented':False,'balanceApproved':False,'githubPushed':False,
        'cosmology':'Deferred until successful authorized GitHub push and verified remote commit.'}
    dump(review_path,manifest)
    status=read(AUDIT/'FISHING_AUTHORING_STATUS.json')
    status.update({'status':STATUS,'recipesApproved':44,'currentReviewedRecipes':392,'remainingRecipes':295,
        'outputs':final_hashes,'reviewManifest':review_path.relative_to(GAME).as_posix(),
        'exactOperationalReviewAuthority':receipt['operationalAuthority'],
        'next':'Continue the remaining 295 recipe effects and broader game review; no push before final joint flow review'})
    dump(AUDIT/'FISHING_AUTHORING_STATUS.json',status)
    progress=read(AUDIT/'FISHING_EXACT_REPAIR_PROGRESS.json')
    progress.update({'status':'PASS — FI-E01..11 fulfilled; 44 cards promoted under actual conditional verdict',
        'implementedAreas':report['conditionsSatisfied'],'focusedChecksPassed':report['focusedChecks'],
        'sourceProjectionArithmeticChecksPassed':report['sourceChecks'],'originalSequenceChecksPassed':report['sequenceChecks'],
        'projectionAndIntegrationChecksPassed':report['projectionAndIntegrationChecks'],'currentArtifactHashes':final_hashes,
        'recipesPromoted':44,'fullCompletionGateSatisfied':True,'completionReceipt':receipt_path.name})
    counts=Counter(c['issue'] for c in read(AUDIT/'FISHING_EXACT_REPAIR_VALIDATION.json')['checks'])
    for repair in progress['repairs']:
        repair.update({'status':'PASS — fulfilled and promoted','checksPassed':counts.get(repair['id'],report['projectionAndIntegrationChecks']),
            'completionEvidence':receipt_path.name})
    dump(AUDIT/'FISHING_EXACT_REPAIR_PROGRESS.json',progress)
    submission=read(AUDIT/'FISHING_EXACT_PART2_SUBMISSION.json')
    submission.update({'status':'Completed actual exact verdict; FI-E01..11 fulfilled; 44 operational cards promoted',
        'submittedCountsAndHashesAreHistorical':True,'finalReviewManifest':review_path.relative_to(GAME).as_posix()})
    dump(AUDIT/'FISHING_EXACT_PART2_SUBMISSION.json',submission)
    print(json.dumps({'status':STATUS,'recipesPromoted':44,'checks':manifest['validationChecks'],
        'protectedInputsUnchanged':63,'reviewedTotal':392,'publicReviewed':251,'remaining':295}))


if __name__=='__main__':main()
