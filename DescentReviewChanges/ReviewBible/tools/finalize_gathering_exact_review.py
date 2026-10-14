"""Record authorized gathering promotion after the current GEX gate passes.

Only review metadata and scope wording change here. The exact prepromotion
revision remains recoverable, and inverse normalization proves rule preservation.
"""
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
import hashlib,json,shutil
R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
STATUS='REVIEWED — authored operational PLAYTEST gathering recipe set'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(G).as_posix()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
REPLACEMENTS={
 '**Authored playtest candidate; exact review pending.**':'**REVIEWED — authored operational PLAYTEST.**',
 '**Authored candidate; exact review pending.**':'**REVIEWED — authored operational PLAYTEST body profiles.**',
 'authored candidates; exact review pending.':'reviewed authored-operational PLAYTEST cards.',
 '**All 128 authored candidates; exact review pending.**':'**All 128 reviewed authored-operational PLAYTEST cards.**',
 'These tools are not yet approved for normal campaign selection.':'These tools have completed authored-operational review for playtest selection, subject to their actual access and material requirements.',
 '**Internal draft •':'**Reviewed internal playtest •',
 '**Player candidate •':'**Reviewed player playtest •',
 'This draft has no operational approval.':'GEX-01/GEX-02 are fulfilled; this card has reviewed authored-operational playtest status.',
 'This authored card awaits exact review.':'This card has completed exact authored-operational review with GEX-01/GEX-02 fulfilled.',
 '**Exact-review candidate; synthetic premises, not campaign facts or runtime certification.**':'**Reviewed authored casebook; synthetic premises, not campaign facts or runtime certification.**',
 'The qualitative dispositions below require the exact reviewer to assess their agreement with the rules; they are not presented as automated runtime passes.':'The exact reviewer assessed the qualitative dispositions below as consistent conditional authored examples; they are not presented as automated runtime passes.',
 '**128 authored candidates; zero new approvals.** The reviewed recipe total remains392/687. Joint source reconciliation is complete; exact-card review remains pending.':'**All128 gathering cards have completed authored-operational review.** With GEX-01/GEX-02 fulfilled, the reviewed recipe total is520/687, with167 remaining; public333/433.',
 'Full player envelopes remain subject to exact review.':'The full Director-mediated player envelope was accepted by the exact review, with GEX-02 now carried into its operating instructions.',
 'Its qualitative outcomes are authored expectations awaiting reviewer assessment.':'Its qualitative outcomes have been assessed by the exact reviewer as conditional authored examples.',
 'Next: submit every complete card, guide, source and accurately scoped evidence for exact GPT review. All128 gathering cards remain unapproved.':'All128 cards are promoted under the completed exact verdict and current-bound GEX completion receipt. The remaining167 advanced-trade formulas are the next recipe cohort.',
}
def promote_text(text):
 for a,b in REPLACEMENTS.items():text=text.replace(a,b)
 return text
def main():
 manifest_path=R/'docs/mechanics/GATHERING_TOOL_REVIEW_STATUS.json';assert not manifest_path.exists()
 rp=A/'GATHERING_128_EXACT_COMPLETION_VALIDATION.json';report=read(rp)
 assert report['completionGateSatisfied'] and report['conditionsSatisfied']==['GEX-01','GEX-02'] and not report['recipesPromoted']
 assert all(c['pass'] for c in report['checks'])
 assert all(sha(G/p)==h for p,h in {**report['artifactHashes'],**report['generationHashes']}.items())
 for suite in report['existingSuites']:assert sha(G/suite['file'])==suite['sha256'] and sha(G/suite['script'])==suite['scriptSha256']
 assert sha(R/'tools/validate_gathering_exact_corrections.py')==report['validatorSha256']
 cap=read(A/'GATHERING_128_EXACT_VERDICT_CAPTURE.json');assert sha(A/cap['verdictFile'])==cap['verdictSha256']
 protected=read(A/'GATHERING_128_EXACT_BUNDLE_SUBMISSION.json')['protectedFiles']
 assert all(sha(G/p)==h for p,h in protected.items())
 archive=A/'gathering-corrected-before-promotion';assert not archive.exists();archive.mkdir()
 saved={**report['artifactHashes'],**report['generationHashes'],rel(rp):sha(rp)}
 for n in ['GATHERING_TOOL_INTERNAL_AUTHORING_STATUS.json','GATHERING_TOOL_INTERNAL_DRAFT_VALIDATION.json','GATHERING_TOOL_GUIDE_PROJECTION_VALIDATION.json','GATHERING_TOOL_WORKED_CASE_VALIDATION.json','GATHERING_TOOL_CANDIDATE_ARITHMETIC_CASES.json']:
  saved[rel(A/n)]=sha(A/n)
 for p,h in saved.items():
  dst=archive/p;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(G/p,dst);assert sha(dst)==h
 dump(archive/'MANIFEST.json',saved)
 authority={'threadId':cap['threadId'],'turnId':cap['turnId'],'replyId':cap['replyId'],'verdictFile':cap['verdictFile'],'sha256':cap['verdictSha256'],'conditionsSatisfied':['GEX-01','GEX-02'],'completionGateSatisfied':True}
 normalized=[]
 for name in report['artifactHashes']:
  p=G/name
  if p.suffix=='.json':
   before=read(p);after=deepcopy(before)
   assert 'cards' in before
   after.update({'status':STATUS,'exactRecipeApproval':True,'exactOperationalReviewAuthority':authority})
   for c in after['cards']:c['status']='reviewed-authored-operational-playtest'
   inverse=deepcopy(after);inverse.pop('exactOperationalReviewAuthority');inverse['status']=before['status'];inverse['exactRecipeApproval']=before['exactRecipeApproval']
   for c,old in zip(inverse['cards'],before['cards']):c['status']=old['status']
   assert inverse==before
   dump(p,after);normalized.append({'file':name,'onlyReviewMetadataChanged':True})
  elif not name.endswith('GATHERING_TOOL_INTERNAL_SOURCE_DIRECTIONS.md'):
   before=p.read_bytes().decode('utf-8');after=promote_text(before);inverse=after
   for old,new in reversed(list(REPLACEMENTS.items())):inverse=inverse.replace(new,old)
   assert inverse==before,name
   if after!=before:p.write_bytes(after.encode('utf-8'))
   normalized.append({'file':name,'onlyReviewScopeWordingChanged':True,'changed':after!=before})
  else:normalized.append({'file':name,'historicalSourceDirectionsPreservedUnchanged':sha(p)==report['artifactHashes'][name]})
 final={p:sha(G/p) for p in report['artifactHashes']}
 assert all(sha(G/p)==h for p,h in protected.items())
 receipt={'status':'PASS — GEX-01/GEX-02 fulfilled; all128 authorized promotions recorded','promotedAtUtc':datetime.now(timezone.utc).isoformat(),'authority':authority,'prepromotionValidation':rel(rp),'prepromotionValidationSha256':sha(rp),'prepromotionArchive':rel(archive),'prepromotionHashes':report['artifactHashes'],'finalArtifactHashes':final,'normalizationChecks':normalized,'existingChecks':report['existingChecks'],'focusedChecks':report['focusedChecks'],'protectedInputsUnchanged':len(protected),'recipesPromoted':128,'publicRecipesPromoted':82,'aggregateReviewedRecipes':520,'remainingRecipes':167,'publicReviewedRecipes':333,'publicRemainingRecipes':100,'sourceInformationDeleted':0,'runtimeImplemented':False,'balanceApproved':False,'wholeGameFlowApproved':False,'githubPushed':False,'cosmologyReviewed':False,'finalizerSha256':sha(Path(__file__))}
 receipt_path=A/'GATHERING_128_EXACT_PROMOTION_RECEIPT.json';dump(receipt_path,receipt)
 manifest={'status':STATUS,'exactReviewThreadId':cap['threadId'],'exactReviewTurnId':cap['turnId'],'exactReplyId':cap['replyId'],'conditionsSatisfied':['GEX-01','GEX-02'],'coverage':{'recipes':128,'public':82,'restricted':6,'directorOnly':40,'baseModels':17,'publicBaseModels':15,'auxiliaryModels':3},'artifactHashes':final,'validationChecks':report['existingChecks']+report['focusedChecks'],'validationEvidence':rel(rp),'validationSha256':sha(rp),'promotionReceipt':rel(receipt_path),'promotionReceiptSha256':sha(receipt_path),'aggregateReviewedRecipes':520,'remainingRecipeEffects':167,'publicReviewedRecipes':333,'runtimeImplemented':False,'balanceApproved':False,'sourceInformationDeleted':0}
 dump(manifest_path,manifest)
 status=read(A/'GATHERING_TOOL_INTERNAL_AUTHORING_STATUS.json')
 status.update({'status':STATUS,'outputs':final,'recipesApproved':128,'currentReviewedRecipes':520,'remainingRecipes':167,'publicReviewedRecipes':333,'exactReviewCompleted':True,'exactReviewAuthority':authority,'reviewManifest':rel(manifest_path),'promotionReceipt':rel(receipt_path),'openWork':['167 advanced-trade recipes','Remaining whole-game interfaces and authored content','Human balance and full runtime remain separate'],'next':'Refresh and submit the prepared167 advanced-trade source cohort; preserve cosmology until after final joint flow, push and remote verification'})
 dump(A/'GATHERING_TOOL_INTERNAL_AUTHORING_STATUS.json',status)
 sub=read(A/'GATHERING_128_EXACT_BUNDLE_SUBMISSION.json');sub.update({'status':'Completed exact verdict; GEX corrections fulfilled;128 cards promoted','verdictPending':False,'sameSubmissionStillUnderReview':False,'notebookStatusAsObserved':'completed final reply captured','finalReplyId':cap['replyId'],'promotionReceipt':receipt_path.name,'submittedArtifactHashesAreHistorical':True})
 dump(A/'GATHERING_128_EXACT_BUNDLE_SUBMISSION.json',sub)
 print(json.dumps({k:receipt[k] for k in ['status','recipesPromoted','publicRecipesPromoted','existingChecks','focusedChecks','aggregateReviewedRecipes','remainingRecipes']}))
if __name__=='__main__':main()
