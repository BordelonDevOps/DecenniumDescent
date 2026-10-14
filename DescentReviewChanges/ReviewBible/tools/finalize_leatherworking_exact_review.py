"""Apply only authorized review-status changes after the two finite evidence repairs."""
from pathlib import Path
from copy import deepcopy
import json,hashlib,subprocess,sys

ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1];AUDIT=GAME/'docs/audit/2026-10-08/full-game'
ARCHIVE=AUDIT/'leatherworking-before-part2-repairs'
TURN='2a3db078-0ab3-411a-a9d2-aeb19da8765e';REPLY='1f8a8f86-3d64-4665-8d7f-cd315727a240';THREAD='6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b'
STATUS='REVIEWED — authored operational PLAYTEST Leatherworking recipe set'
CARD_STATUS='reviewed-authored-operational-playtest'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,s):p.write_text(s,encoding='utf-8',newline='\n')
def dump(p,d):write(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')

def main():
    manifest=ROOT/'docs/mechanics/LEATHERWORKING_REVIEW_STATUS.json';assert not manifest.exists()
    report=read(AUDIT/'LEATHERWORKING_CANDIDATE_VALIDATION.json')
    assert report['status']=='PASS' and len(report['checks'])==91 and len(report['behaviorCases'])==52
    verdict=AUDIT/'GPT_LEATHERWORKING_EXACT_VERDICT.md';v=verdict.read_text(encoding='utf-8')
    assert TURN in v and REPLY in v and 'Promotion of all 44 cards is then authorized' in v
    for p,h in read(ARCHIVE/'PRESERVATION_MANIFEST.json')['files'].items():assert sha(ARCHIVE/p)==h
    assert all(sha(ROOT/p)==h for p,h in report['artifactHashes'].items())
    write(AUDIT/'LEATHERWORKING_REPAIRED_PREPROMOTION_VALIDATION.json',(AUDIT/'LEATHERWORKING_CANDIDATE_VALIDATION.json').read_text(encoding='utf-8'))
    changes={}
    for rel in ['data/director/leatherworking_recipe_candidate_internal.json','data/playtest/leatherworking_recipe_candidate.json']:
        p=ROOT/rel;before=read(p);d=deepcopy(before)
        assert d['status']=='authored-draft-awaiting-exact-review'
        d['status']=STATUS;d['exactRecipeApproval']=True;d['sharedOperationalProfile']['status']=CARD_STATUS
        d.update(exactReviewThreadId=THREAD,exactReviewTurnId=TURN,exactReplyId=REPLY)
        for c in d['cards']:assert c['status']=='authored-draft-awaiting-exact-review';c['status']=CARD_STATUS
        restored=deepcopy(d);restored['status']=before['status'];restored['exactRecipeApproval']=False;restored['sharedOperationalProfile']['status']=before['sharedOperationalProfile']['status']
        for k in ['exactReviewThreadId','exactReviewTurnId','exactReplyId']:restored.pop(k)
        for c,b in zip(restored['cards'],before['cards']):c['status']=b['status']
        assert restored==before,'Non-status JSON mutation'
        dump(p,d);changes[rel]='Only operational review status, approval flag and exact-review provenance; originals, models and operational rules byte-equivalent as JSON values.'
    for rel in report['artifactHashes']:
        if not rel.endswith('.md'):continue
        p=ROOT/rel;s=p.read_text(encoding='utf-8');before=s
        s=s.replace('**DRAFT — exact review pending.**','**REVIEWED — authored operational PLAYTEST.**')
        s=s.replace('**DRAFT — exact card review pending.**','**REVIEWED — authored operational PLAYTEST.**')
        s=s.replace('**DRAFT; exact review pending.**','**REVIEWED — authored operational PLAYTEST.**')
        old='That conference authorizes authoring, not approval of these cards. Current reviewed recipe totals remain 218/687; 469 remain.'
        new='That source conference remains historical authoring direction. The subsequent exact review (turn `'+TURN+'`, reply `'+REPLY+'`) conditionally approved these cards; LW-ER01 and LW-ER02 have been corrected and validated. Reviewed operational totals are now 262/687; 425 remain.'
        s=s.replace(old,new)
        assert s!=before and s.count('\n\n')==before.count('\n\n')
        write(p,s);changes[rel]='Review status labels and guide provenance paragraph only; all rule and card-effect paragraphs unchanged.'
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/validate_leatherworking_recipe_candidate.py')],check=True)
    final=read(AUDIT/'LEATHERWORKING_CANDIDATE_VALIDATION.json');assert final['status']=='PASS' and final['recipesApproved']==44
    # Regenerate exact public/internal paragraph references affected by status text.
    internal=(ROOT/'docs/director-only/LEATHERWORKING_INTERNAL_RECIPE_CARDS.md').read_text(encoding='utf-8')
    public=(ROOT/'docs/mechanics/LEATHERWORKING_PUBLIC_RECIPE_CARDS.md').read_text(encoding='utf-8')
    ip=internal.split('\n\n');pp=public.split('\n\n')
    refs=[{'internalParagraph':ip.index(p)} if p in ip else {'literal':p} for p in pp]
    assert '\n\n'.join(ip[r['internalParagraph']] if 'internalParagraph' in r else r['literal'] for r in refs)==public
    projection={'status':'PASS','internalParagraphs':ip,'publicParagraphProjection':refs,'internalParagraphCount':len(ip),'publicParagraphCount':len(pp),'publicReferences':sum('internalParagraph' in r for r in refs),'internalSha256':sha(ROOT/'docs/director-only/LEATHERWORKING_INTERNAL_RECIPE_CARDS.md'),'publicSha256':sha(ROOT/'docs/mechanics/LEATHERWORKING_PUBLIC_RECIPE_CARDS.md'),'scope':'Internal audit evidence only; full internal paragraphs include hidden recipes.'}
    projection_path=AUDIT/'LEATHERWORKING_FINAL_PARAGRAPH_PROJECTION.json';dump(projection_path,projection)
    repairs={'status':'PASS — exact-review conditions fulfilled','threadId':THREAD,'turnId':TURN,'replyId':REPLY,'preservedSubmittedRevision':ARCHIVE.relative_to(GAME).as_posix(),'repairs':{'LW-ER01':'Documented already-eligible suit-grade input; unselected suit uses None and retains cold resistance under an explicit independently legal alternative-formula premise. Separate selected Crude, zero-recipe and positive-recipe assertions pass.','LW-ER02':'Explicit Tiny transformed body retains140lb and uses existing1.5 casualty Load; melded equipment15lb/1.5Load, no other equipment and inactive relief produce155lb/3Load. Actual handling/anatomy limits remain necessary.'},'correctedBehaviorCases':[c for c in final['behaviorCases'] if any(s in c['name'] for s in ['LW-01','LW-ER01','LW-ER02'])],'statusOnlyArtifactChanges':changes,'checks':len(final['checks']),'behaviorCases':len(final['behaviorCases']),'protectedFilesUnchanged':42,'paragraphProjectionSha256':sha(projection_path),'referenceSha256':sha(ROOT/'tools/leatherworking_reference.py'),'validatorSha256':sha(ROOT/'tools/validate_leatherworking_recipe_candidate.py'),'verdictSha256':sha(verdict),'sourceInformationDeleted':0}
    receipt=AUDIT/'LEATHERWORKING_EXACT_REPAIRS_APPLIED.json';dump(receipt,repairs)
    m={'status':STATUS,'exactReviewThreadId':THREAD,'exactReviewTurnId':TURN,'exactReplyId':REPLY,'sourceConferenceTurnId':'86413ad7-8096-4e6f-baca-3cab34aa66a3','sourceConferenceReplyId':'4f808c26-f93b-4b50-ac05-a917b7ca2b7e','repairsApplied':['LW-ER01','LW-ER02'],'coverage':{'recipes':44,'public':30,'restricted':1,'directorOnly':13,'baseModels':19,'publicBaseModels':14},'validationChecks':len(final['checks']),'localBehaviorCases':len(final['behaviorCases']),'localDurabilityStates':final['durabilityStates'],'localBurdenStates':final['burdenStates'],'protectedSourceAndPriorRuleArtifactsUnchanged':42,'artifactHashes':{(ROOT/p).relative_to(GAME).as_posix():h for p,h in final['artifactHashes'].items()},'replyHashes':{verdict.name:sha(verdict)},'validationEvidence':(AUDIT/'LEATHERWORKING_CANDIDATE_VALIDATION.json').relative_to(GAME).as_posix(),'validationSha256':sha(AUDIT/'LEATHERWORKING_CANDIDATE_VALIDATION.json'),'repairEvidence':receipt.relative_to(GAME).as_posix(),'repairEvidenceSha256':sha(receipt),'sourceInformationDeleted':0,'runtimeImplemented':False,'balanceApproved':False,'githubPushed':False,'aggregateReviewedRecipes':262,'remainingRecipeEffects':425,'cosmology':'Deferred until successful authorized GitHub push and verified remote commit.'}
    dump(manifest,m)
    sub=read(AUDIT/'LEATHERWORKING_EXACT_PART2_SUBMISSION.json');sub['status']='Completed exact verdict; both finite repairs validated;44 operational cards promoted';sub['parts']['B_EXACT_CARDS'].update(status='Completed conditional verdict; fulfilled conditions recorded separately',replyId=REPLY);sub['finalReviewManifest']=manifest.relative_to(GAME).as_posix();sub['submittedCountsAreHistorical']=True;dump(AUDIT/'LEATHERWORKING_EXACT_PART2_SUBMISSION.json',sub)
    author=read(AUDIT/'LEATHERWORKING_AUTHORING_STATUS.json');author.update(status=STATUS,recipesApproved=44,currentReviewedRecipes=262,remainingRecipes=425,exactReviewTurnId=TURN,exactReplyId=REPLY,reviewManifest=manifest.relative_to(GAME).as_posix());dump(AUDIT/'LEATHERWORKING_AUTHORING_STATUS.json',author)
    print(json.dumps({'status':m['status'],'checks':m['validationChecks'],'cases':m['localBehaviorCases'],'publicParagraphReferences':projection['publicReferences'],'reviewedTotal':262,'remaining':425}))
if __name__=='__main__':main()
