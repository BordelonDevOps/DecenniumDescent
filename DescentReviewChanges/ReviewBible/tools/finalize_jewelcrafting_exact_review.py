"""Apply the finite JC-ER01..03 promotion authorized by the saved exact verdict."""
from pathlib import Path
from copy import deepcopy
import json,hashlib,subprocess,sys,zipfile

ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1];AUDIT=GAME/'docs/audit/2026-10-08/full-game'
ARCHIVE=AUDIT/'jewelcrafting-before-exact-review-repairs'
THREAD='6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b';TURN='3074a6c4-b718-4241-ae05-f6b3ed1238b0';REPLY='872837f3-e844-4e3f-9a79-068060b62213'
STATUS='REVIEWED — authored operational PLAYTEST Jewelcrafting recipe set'
CARD_STATUS='reviewed-authored-operational-playtest'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,t):p.write_text(t,encoding='utf-8',newline='\n')
def dump(p,d):write(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')

def main():
    manifest=ROOT/'docs/mechanics/JEWELCRAFTING_REVIEW_STATUS.json';assert not manifest.exists()
    capture=read(AUDIT/'JEWELCRAFTING_EXACT_REVIEW_CAPTURE.json')
    assert capture['turnId']==TURN and capture['replyId']==REPLY and capture['downloadBodyContainedInMCP']
    verdict=AUDIT/'GPT_JEWELCRAFTING_EXACT_REVIEW.md';v=verdict.read_text(encoding='utf-8')
    assert 'this verdict authorizes promotion of all 43 Jewelcrafting cards' in v
    assert all(x in v for x in ('JC-ER01','JC-ER02','JC-ER03','without another generic conference or unchanged-card resubmission'))
    for p,h in read(ARCHIVE/'MANIFEST.json').items():assert sha(ARCHIVE/p)==h
    report=read(AUDIT/'JEWELCRAFTING_CANDIDATE_VALIDATION.json')
    assert report['status']=='PASS' and report['checkCount']==131 and report['recipesApproved']==0
    assert report['protectedFilesUnchanged']==54 and report['structuralStates']==486 and len(report['valueCombinations'])==86
    assert all(c['pass'] for c in report['checks'])
    assert all(sha(ROOT/p)==h for p,h in report['artifactHashes'].items())
    archive=AUDIT/'jewelcrafting_exact_review_evidence.zip'
    with zipfile.ZipFile(archive) as z:
        hashes=json.loads(z.read('jewelcrafting_exact_review_evidence/SHA256SUMS.json'))
        assert all(hashlib.sha256(z.read('jewelcrafting_exact_review_evidence/'+n)).hexdigest()==h for n,h in hashes.items())
        for name,rel in [('submitted_internal_cards_reconstructed.md','docs/director-only/JEWELCRAFTING_INTERNAL_RECIPE_CARDS.md'),('submitted_public_cards_reconstructed.md','docs/mechanics/JEWELCRAFTING_PUBLIC_RECIPE_CARDS.md')]:
            assert z.read('jewelcrafting_exact_review_evidence/'+name)==(ARCHIVE/(ROOT/rel).relative_to(GAME)).read_bytes()
    # Ensure repairs only add the two authorized shared contracts. Every source,
    # body, individual card, value and source-authority record is unchanged.
    additions={}
    for rel in report['artifactHashes']:
        p=ROOT/rel;old=ARCHIVE/p.relative_to(GAME)
        if p.suffix=='.json':
            original=read(old);repaired=read(p);restored=deepcopy(repaired)
            contract=restored['sharedOperationalProfile'];contract.pop('crossTradeRollIdentity')
            for k in ('orderedCampaignEventCheckpointRequired','allPrecedingDawnsBeforeSpend','rejectEarlierTransitions','oneAuthoritativeLedger'):assert contract['chargeLedger'].pop(k) is True
            assert restored==original,'Unrelated JSON alteration: '+rel
        elif 'RECIPE_CARDS' in rel:
            assert p.read_bytes()==old.read_bytes(),'Unrelated card prose alteration: '+rel
        else:
            a=old.read_text(encoding='utf-8').split('\n\n');b=p.read_text(encoding='utf-8').split('\n\n')
            added=[s for s in b if s not in a]
            assert len(added)==2 and any(s.startswith("Every participating item's evidence") for s in added) and any(s.startswith('Resolve creation, dawns and expenditures') for s in added)
            assert [s for s in b if s not in added]==a,'Unrelated guide alteration: '+rel
            additions[rel]=added
    dump(AUDIT/'JEWELCRAFTING_REPAIRED_PREPROMOTION_VALIDATION.json',report)
    repaired_hashes=report['artifactHashes']
    for rel in repaired_hashes:
        p=ROOT/rel
        if p.suffix=='.json':
            before=read(p);d=deepcopy(before)
            d.update(status=STATUS,exactRecipeApproval=True,exactReviewThreadId=THREAD,exactReviewTurnId=TURN,exactReplyId=REPLY,exactReviewConditions=['JC-ER01','JC-ER02','JC-ER03'])
            d['sharedOperationalProfile']['status']=CARD_STATUS
            for c in d['cards']:assert c['status']=='authored-draft-awaiting-exact-review';c['status']=CARD_STATUS
            restored=deepcopy(d)
            for key in ('exactReviewThreadId','exactReviewTurnId','exactReplyId','exactReviewConditions'):restored.pop(key)
            restored['status']=before['status'];restored['exactRecipeApproval']=False;restored['sharedOperationalProfile'].pop('status')
            for c,b in zip(restored['cards'],before['cards']):c['status']=b['status']
            assert restored==before
            dump(p,d)
        else:
            s=p.read_text(encoding='utf-8')
            for label in ('**DRAFT — exact review pending.**','**DRAFT; exact review pending.**','**Authored draft; exact-card review pending.**'):
                s=s.replace(label,'**REVIEWED — authored operational PLAYTEST.**')
            write(p,s)
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/validate_jewelcrafting_recipe_candidate.py')],check=True)
    final=read(AUDIT/'JEWELCRAFTING_CANDIDATE_VALIDATION.json');assert final['recipesApproved']==43 and final['status']=='PASS'
    projection=read(AUDIT/'JEWELCRAFTING_PUBLIC_PARAGRAPH_PROJECTION.json')
    assert projection['wholePublicCardsEqual'] and projection['wholePublicGuideEqual'] and projection['wholePublicEnvelopeEqual']
    receipt=AUDIT/'JEWELCRAFTING_EXACT_REPAIRS_APPLIED.json'
    repairs={
      'JC-ER01':{'result':'PASS','change':'Authoritative campaign/epoch/time/order/preceding-dawn checkpoints retained for each item. Reject unresolved preceding dawns and earlier or replayed transitions; one authoritative caller ledger. Creation checkpoints and actual historical dawn-state requirements retained.','checks':[c for c in final['checks'] if c['name'].startswith('JC-ER01')]},
      'JC-ER02':{'result':'PASS','change':'Canonical event ID and consistent kind/actor/ability/proficiency/actual-roll/automatic-result descriptors required before either trade calculation. Item premises remain current-event specific, with independent vocabulary and designation validation first. Protected older trade artifacts unchanged.','checks':[c for c in final['checks'] if c['name'].startswith('JC-ER02')]},
      'JC-ER03':{'result':'PASS','change':'Recipe268 fixtures derive DC19,2gp body and4509gp finished reference from actual source/card/model. Positive Broken HP5 quote is8h,1127.25gp/112725cp. Missing crystal/mount negatives isolate original-assembly gates with that same profile. Card/source values unchanged.','checks':[c for c in final['checks'] if 'recipe268' in c['name'] or 'Gem missing' in c['name']]}}
    dump(receipt,{'status':'PASS — exact-review conditions fulfilled','threadId':THREAD,'turnId':TURN,'replyId':REPLY,'preservedSubmittedRevision':ARCHIVE.relative_to(GAME).as_posix(),'repairs':repairs,'authorizedGuideAdditions':additions,'repairedPrepromotionHashes':repaired_hashes,'finalArtifactHashes':final['artifactHashes'],'checks':final['checkCount'],'predicateCases':len(final['predicateCases']),'structuralStates':486,'valueCombinations':86,'protectedFilesUnchanged':54,'completePublicCardsGuideAndJsonProjection':True,'referenceSha256':sha(ROOT/'tools/jewelcrafting_reference.py'),'validatorSha256':sha(ROOT/'tools/validate_jewelcrafting_recipe_candidate.py'),'verdictSha256':sha(verdict),'reviewerArchiveSha256':sha(archive),'verifiedReviewerArchiveHashes':len(hashes),'sourceInformationDeleted':0,'runtimeImplemented':False,'balanceApproved':False})
    m={'status':STATUS,'exactReviewThreadId':THREAD,'exactReviewTurnId':TURN,'exactReplyId':REPLY,'sourceConferenceTurnId':'96dbc19c-068f-4f2c-a81f-c2ea87d75f25','sourceConferenceReplyId':'c510dda9-431e-478b-92ee-5ea6d42407e8','repairsApplied':list(repairs),'coverage':{'recipes':43,'public':26,'restricted':1,'directorOnly':16,'baseModels':10,'publicBaseModels':9,'tags':14,'publicTags':12},'validationChecks':final['checkCount'],'protectedSourceAndPriorRuleArtifactsUnchanged':54,'artifactHashes':{(ROOT/p).relative_to(GAME).as_posix():h for p,h in final['artifactHashes'].items()},'replyHashes':{verdict.name:sha(verdict)},'validationEvidence':(AUDIT/'JEWELCRAFTING_CANDIDATE_VALIDATION.json').relative_to(GAME).as_posix(),'validationSha256':sha(AUDIT/'JEWELCRAFTING_CANDIDATE_VALIDATION.json'),'repairEvidence':receipt.relative_to(GAME).as_posix(),'repairEvidenceSha256':sha(receipt),'sourceInformationDeleted':0,'runtimeImplemented':False,'balanceApproved':False,'githubPushed':False,'aggregateReviewedRecipes':348,'remainingRecipeEffects':339,'publicReviewedRecipes':223,'cosmology':'Deferred until successful authorized GitHub push and verified remote commit.'}
    dump(manifest,m)
    p=AUDIT/'JEWELCRAFTING_EXACT_PART2_SUBMISSION.json';sub=read(p);sub.update(status='Completed exact verdict; JC-ER01..03 fulfilled and43 operational cards promoted',submittedCountsAndHashesAreHistorical=True,finalReviewManifest=manifest.relative_to(GAME).as_posix())
    sub['parts']['B_EXACT_CARDS'].update(actualAgentVerdictPending=False,replyId=REPLY,status='conditional verdict completed; fulfilled conditions recorded separately',lastObservedItemTypes=['userMessage','agentMessage']);dump(p,sub)
    p=AUDIT/'JEWELCRAFTING_AUTHORING_STATUS.json';d=read(p);d.update(status=STATUS,recipesApproved=43,currentReviewedRecipes=348,remainingRecipes=339,exactReviewTurnId=TURN,exactReplyId=REPLY,reviewManifest=manifest.relative_to(GAME).as_posix(),next='Fishing source conference, then remaining recipes and broader systems');dump(p,d)
    print(json.dumps({'status':STATUS,'checks':131,'protectedFilesUnchanged':54,'reviewedTotal':348,'publicReviewed':223,'remaining':339}))

if __name__=='__main__':main()
