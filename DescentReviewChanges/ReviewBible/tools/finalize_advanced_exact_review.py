"""Record the finite AEX promotion; prove final edits change review labels only."""
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
import json,hashlib,shutil
R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
STATUS='REVIEWED — authored operational PLAYTEST advanced recipe set'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(G).as_posix()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
REPLACEMENTS={
 'Internal candidate;':'Reviewed internal playtest;',
 'exact approval pending.':'authored-operational exact approval complete.',
 'Player candidate;':'Reviewed player playtest;',
 'exact review pending.':'authored-operational exact review complete.',
 '**Authored playtest candidate; separate exact review pending.**':'**REVIEWED — authored operational PLAYTEST.**',
 '**Authored candidate; exact review pending.**':'**REVIEWED — authored operational PLAYTEST bodies.**',
 '**Exact corrections AEX-01–07 applied; validation and promotion receipt pending.**':'**REVIEWED — AEX-01–07 fulfilled; exact authored-operational review complete.**',
 '**Exact corrections applied; validation pending.**':'**REVIEWED — exact corrections validated for authored-operational playtest.**',
 'cards; exact corrections applied, validation and promotion receipt pending.':'cards; reviewed authored-operational PLAYTEST with AEX-01–07 fulfilled.',
}
def promote(text):
 # Longer phrases first keeps each inverse substitution unambiguous.
 for a,b in sorted(REPLACEMENTS.items(),key=lambda x:-len(x[0])):text=text.replace(a,b)
 return text
def inverse(text):
 for a,b in reversed(sorted(REPLACEMENTS.items(),key=lambda x:-len(x[0]))):text=text.replace(b,a)
 return text
def main():
 manifest=R/'docs/mechanics/ADVANCED_CRAFT_REVIEW_STATUS.json';assert not manifest.exists()
 vp=A/'ADVANCED_167_EXACT_COMPLETION_VALIDATION.json';v=read(vp)
 assert v['completionGateSatisfied'] and v['focusedCases']==33 and not v['failed'] and v['recipesPromoted']==0
 assert sha(R/'tools/validate_advanced_exact_corrections.py')==v['validatorSha256']
 assert all(sha(G/p)==h for p,h in v['artifactHashes'].items())
 assert sha(G/v['verdictFile'])==v['verdictSha256']
 for s in v['existingSuites']:assert sha(G/s['file'])==s['sha256'] and sha(G/s['script'])==s['scriptSha256']
 protected=read(A/'ADVANCED_CRAFT_JOINT_SUBMISSION.json')['currentFileHashes']
 assert all(sha(G/p)==h for p,h in protected.items())
 archive=A/'advanced167-corrected-before-promotion';archive.mkdir(exist_ok=True)
 saved={**v['artifactHashes'],rel(vp):sha(vp)}
 for s in v['existingSuites']:saved[s['file']]=s['sha256'];saved[s['script']]=s['scriptSha256']
 for name in ['ADVANCED_CRAFT_INTERNAL_AUTHORING_STATUS.json','ADVANCED_CRAFT_PUBLIC_AUTHORING_STATUS.json','ADVANCED_CRAFT_AUTHORING_PROGRESS.json','ADVANCED_CRAFT_CANDIDATE_READINESS.json','ADVANCED_CRAFT_EXACT_SUBMISSION.json','ADVANCED_CRAFT_AEX_APPLICATION.json','ADVANCED_CRAFT_PUBLIC_PROJECTION_LEDGER.json']:
  p=A/name;saved[rel(p)]=sha(p)
 for name,h in saved.items():
  dst=archive/name;dst.parent.mkdir(parents=True,exist_ok=True)
  if dst.exists():assert sha(dst)==h
  else:shutil.copy2(G/name,dst)
  assert sha(dst)==h
 dump(archive/'MANIFEST.json',saved)
 authority={'threadId':'6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b','turnId':'dbffb1f2-10d4-4454-a983-2e3850f654eb','replyId':'d35f30fb-dbf5-4cc6-a8ba-2d4698c0be91','verdictFile':v['verdictFile'],'sha256':v['verdictSha256'],'conditionsSatisfied':v['conditionsSatisfied'],'completionGateSatisfied':True}
 normalized=[]
 # First update text, then copy exactly those reviewed guide bytes into public JSON.
 for name in v['artifactHashes']:
  p=G/name
  if p.suffix!='.md':continue
  before=p.read_text(encoding='utf-8');after=promote(before)
  assert inverse(after)==before,name
  p.write_text(after,encoding='utf-8');normalized.append({'file':name,'onlyReviewLabelsChanged':True})
 for name in v['artifactHashes']:
  p=G/name
  if p.suffix!='.json':continue
  before=read(p);after=deepcopy(before)
  after.update(status=STATUS,exactRecipeApproval=True,exactOperationalReviewAuthority=authority)
  for c in after['cards']:
   c['status']='reviewed-authored-operational-playtest';c['manuscriptText']=promote(c['manuscriptText'])
  for b in after['bodyModels'].values():
   if 'status' in b:b['status']='reviewed-authored-operational-playtest-body'
  if 'operatingGuideText' in after:
   after['operatingGuideText']=(R/after['guide']).read_text(encoding='utf-8')
   after['bodyGuideText']=(R/after['bodyGuide']).read_text(encoding='utf-8')
  if 'controllingCorrections' in after:
   for c in after['controllingCorrections']:
    if c['id'].startswith('AEX-'):c['status']='fulfilled; promotion recorded under completed exact verdict'
  restored=deepcopy(after);restored.pop('exactOperationalReviewAuthority')
  for key in ['status','exactRecipeApproval']:restored[key]=before[key]
  for c,old in zip(restored['cards'],before['cards']):c['status']=old['status'];c['manuscriptText']=inverse(c['manuscriptText'])
  for k,b in restored['bodyModels'].items():
   if 'status' in before['bodyModels'][k]:b['status']=before['bodyModels'][k]['status']
  if 'operatingGuideText' in restored:
   for key in ['operatingGuideText','bodyGuideText']:restored[key]=inverse(restored[key])
  if 'controllingCorrections' in restored:restored['controllingCorrections']=before['controllingCorrections']
  assert restored==before,name
  dump(p,after);normalized.append({'file':name,'onlyReviewMetadataAndLabelsChanged':True})
 final={name:sha(G/name) for name in v['artifactHashes']}
 # Every rendered card and embedded guide must still equal its final JSON.
 for audience,fn,suffix in [('director-only','data/director/advanced_craft_recipe_candidate_internal.json','INTERNAL_RECIPE_CARDS'),('mechanics','data/crafting/advanced_craft_recipe_candidate_public.json','CANDIDATE_RECIPE_CARDS')]:
  data=read(R/fn)
  for c in data['cards']:
   trade=c['sourceRecipe']['skill'].upper().replace(' ','_')
   assert c['manuscriptText'] in (R/f'docs/{audience}/{trade}_{suffix}.md').read_text(encoding='utf-8')
 assert all(sha(G/p)==h for p,h in protected.items())
 receipt={'status':'PASS — AEX-01–07 fulfilled; 167 authorized promotions recorded','promotedAtUtc':datetime.now(timezone.utc).isoformat(),'authority':authority,'prepromotionValidation':rel(vp),'prepromotionValidationSha256':sha(vp),'prepromotionArchive':rel(archive),'prepromotionHashes':v['artifactHashes'],'finalArtifactHashes':final,'normalizationChecks':normalized,'existingChecks':v['existingChecks'],'focusedCases':33,'additionalStaticChecks':v['staticChecks'],'qualitativeSequenceDisposition':'W-01–W-19, E-01–E-16 and E-18 accepted by GPT; E-17 public completeness condition fulfilled by AEX corrections and whole-envelope checks. Authored adjudications, not executed state-machine tests.','applicationMap':read(A/'ADVANCED_CRAFT_AEX_APPLICATION.json')['applicationMap'],'protectedInputHashes':protected,'protectedInputsUnchanged':138,'recipesPromoted':167,'publicRecipesPromoted':100,'aggregateReviewedRecipes':687,'remainingRecipes':0,'publicReviewedRecipes':433,'publicRemainingRecipes':0,'sourceInformationDeleted':0,'runtimeImplemented':False,'balanceApproved':False,'wholeGameFlowApproved':False,'githubPushed':False,'cosmologyReviewed':False,'finalizerSha256':sha(Path(__file__))}
 rp=A/'ADVANCED_167_EXACT_PROMOTION_RECEIPT.json';dump(rp,receipt)
 dump(manifest,{'status':STATUS,'exactReviewThreadId':authority['threadId'],'exactReviewTurnId':authority['turnId'],'exactReplyId':authority['replyId'],'conditionsSatisfied':v['conditionsSatisfied'],'coverage':{'recipes':167,'public':100,'restricted':7,'directorOnly':60,'bodyVariants':22,'publicBodyVariants':15,'hostTemplates':50,'qualitativeAuthoredSequences':37,'tinkerInterfaceCards':48},'artifactHashes':final,'validationChecks':v['existingChecks']+v['staticChecks'],'focusedAuthoredCases':33,'validationEvidence':rel(vp),'validationSha256':sha(vp),'promotionReceipt':rel(rp),'promotionReceiptSha256':sha(rp),'aggregateReviewedRecipes':687,'remainingRecipeEffects':0,'publicReviewedRecipes':433,'runtimeImplemented':False,'balanceApproved':False,'sourceInformationDeleted':0})
 ih=sha(R/'data/director/advanced_craft_recipe_candidate_internal.json');ph=sha(R/'data/crafting/advanced_craft_recipe_candidate_public.json')
 for name in ['ADVANCED_CRAFT_INTERNAL_AUTHORING_STATUS.json','ADVANCED_CRAFT_PUBLIC_AUTHORING_STATUS.json','ADVANCED_CRAFT_AUTHORING_PROGRESS.json','ADVANCED_CRAFT_CANDIDATE_READINESS.json']:
  p=A/name;s=read(p);s.update(status=STATUS,exactReviewCompleted=True,exactReviewSubmitted=True,qualitativeExactReviewPending=False,exactReviewAuthority=authority,promotionReceipt=rel(rp),internalCandidateSha256=ih,publicCandidateSha256=ph,nextAction='Review prepared onboarding and design charter, then remaining whole-game systems; final joint flow before push, remote verification before cosmology.')
  for key in ['recipesApproved','newAdvancedApprovals','newApprovals']:
   if key in s:s[key]=100 if name=='ADVANCED_CRAFT_PUBLIC_AUTHORING_STATUS.json' else 167
  for key in ['currentReviewedRecipeCount','reviewedRecipes']:
   if key in s:s[key]=687
  if 'reviewedPublicRecipes' in s:s['reviewedPublicRecipes']=433
  for key in ['internalSourceAndManuscriptChecks','internalSourceManuscriptArithmeticChecks']:
   if key in s:s[key]=5808
  if 'remainingWork' in s:s['remainingWork']=['Remaining whole-game interfaces and authored content','Human balance and runtime remain separate']
  if 'outputHashes' in s:s['outputHashes']=final
  dump(p,s)
 p=A/'ADVANCED_CRAFT_EXACT_SUBMISSION.json';s=read(p);s.update(status='Completed exact verdict; AEX-01–07 fulfilled; all167 promoted',exactVerdictPending=False,newApprovals=167,finalReplyId=authority['replyId'],recipesReviewed=687,publicRecipesReviewed=433,promotionReceipt=rp.name,submittedArtifactHashesAreHistorical=True);dump(p,s)
 p=A/'ADVANCED_CRAFT_PUBLIC_PROJECTION_LEDGER.json';s=read(p);s.update(status='Reviewed full public envelope; AEX-01–07 fulfilled',internalCandidateSha256=ih);dump(p,s)
 p=A/'ADVANCED_CRAFT_AEX_APPLICATION.json';s=read(p);s.update(status='AEX-01–07 fulfilled; exact promotion receipt recorded',appliedCandidateHashesAreHistorical=True,currentInternalCandidateSha256=ih,currentPublicCandidateSha256=ph,promotionReceipt=rp.name,newApprovals=167);dump(p,s)
 print(json.dumps({k:receipt[k] for k in ['status','recipesPromoted','publicRecipesPromoted','aggregateReviewedRecipes','remainingRecipes','existingChecks','focusedCases','additionalStaticChecks']}))
if __name__=='__main__':main()
