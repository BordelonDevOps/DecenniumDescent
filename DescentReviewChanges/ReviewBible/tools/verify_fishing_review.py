"""Read-only verification of the final Fishing revision and preserved test evidence.

Use after promotion. The prepromotion generators/reports are historical evidence;
do not regenerate them over the reviewed candidate merely to check its status.
"""
from copy import deepcopy
import json
from build_fishing_recipe_candidate import ROOT,GAME,AUDIT,read,sha,dump,EXACT_AUTH
from finalize_fishing_exact_review import disk_path,REPLACEMENTS,STATUS,CARD_STATUS
from validate_fishing_repaired_candidate import independent_projection


def main():
    review=read(ROOT/'docs/mechanics/FISHING_REVIEW_STATUS.json')
    receipt=read(GAME/review['repairEvidence']);report=read(GAME/review['validationEvidence'])
    assert sha(GAME/review['repairEvidence'])==review['repairEvidenceSha256']
    assert sha(GAME/review['validationEvidence'])==review['validationSha256']==receipt['prepromotionValidationSha256']
    assert review['status']==STATUS and review['validationChecks']==717
    assert report['completionGateSatisfied'] and receipt['recipesPromoted']==44
    assert all(c['pass'] for c in report['checks'])
    assert sha(AUDIT/'GPT_FISHING_EXACT_OPERATIONAL_REVIEW.md')==EXACT_AUTH['sha256']
    archive=GAME/receipt['preservedRepairedRevision'];archived=read(archive/'MANIFEST.json')
    assert all(sha(disk_path(archive/p))==h for p,h in archived.items())
    for p,h in {**report['inputHashes'],**report['regressionInputHashes']}.items():assert archived[p]==h
    for rel,h in report['regressionInputHashes'].items():
        # The six artifacts intentionally changed only during recorded promotion.
        if rel not in review['artifactHashes']:assert sha(GAME/rel)==h,rel
    for rel,h in review['artifactHashes'].items():
        p=GAME/rel;assert sha(p)==h
        before=disk_path(archive/rel)
        if p.suffix=='.json':
            old=read(before);final=read(p);normalized=deepcopy(final)
            assert final['status']==STATUS and final['exactRecipeApproval'] and final['exactOperationalReviewAuthority']['completionGateSatisfied']
            assert all(c['status']==CARD_STATUS for c in final['cards'])
            for key in ('exactReviewThreadId','exactReviewTurnId','exactReplyId','exactReviewConditions'):normalized.pop(key)
            normalized['status']=old['status'];normalized['exactRecipeApproval']=False
            normalized['exactOperationalReviewAuthority']['completionGateSatisfied']=False
            for c,b in zip(normalized['cards'],old['cards']):c['status']=b['status']
            assert normalized==old
        else:
            expected=before.read_text(encoding='utf-8')
            for old,new in REPLACEMENTS.items():expected=expected.replace(old,new)
            assert p.read_text(encoding='utf-8')==expected
    internal=read(ROOT/'data/director/fishing_recipe_candidate_internal.json')
    public=read(ROOT/'data/playtest/fishing_recipe_candidate.json')
    expected=deepcopy(internal);expected['visibility']='public';expected=independent_projection(expected)
    expected['sharedOperationalProfile']['affinityRegistry'].pop('Cold');expected['sharedGuide']='docs/mechanics/FISHING_RECIPE_PLAYTEST.md'
    assert public==expected
    protected=read(AUDIT/'FISHING_PART2_SUBMISSION.json')['protectedFiles']
    assert len(protected)==63 and all(sha(GAME/p)==h for p,h in protected.items())
    acknowledgement=read(AUDIT/'FISHING_COMPLETION_NOTICE_DISPATCH.json')
    assert sha(AUDIT/acknowledgement['captureFile'])==acknowledgement['captureSha256']
    catalog=read(AUDIT/'CRAFTING_RECIPE_REVIEW_CATALOG_VALIDATION.json')
    assert catalog['totals']['reviewed']==392 and catalog['totals']['publicReviewed']==251 and catalog['totals']['unreviewed']==295
    result={'status':'PASS — final reviewed revision matches verified prepromotion content plus authorized status changes',
        'cards':44,'publicCards':28,'verifiedChecks':717,'protectedInputsUnchanged':63,
        'reviewedTotal':392,'publicReviewed':251,'remaining':295,
        'actualGptAcknowledgementReplyId':acknowledgement['replyId'],
        'runtimeImplemented':False,'balanceApproved':False,'wholeGameComplete':False,'githubPushed':False,'cosmology':'post-push only'}
    dump(AUDIT/'FISHING_FINAL_REVIEW_VERIFICATION.json',result);print(json.dumps(result))


if __name__=='__main__':main()
