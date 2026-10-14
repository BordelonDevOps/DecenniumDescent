"""Advance current recipe navigation after the fulfilled AEX gate; archive history."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil,re,subprocess,sys
R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(G).as_posix()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def replace(s,a,b):assert s.count(a)==1,(a,s.count(a));return s.replace(a,b,1)
def main():
 receipt=read(A/'ADVANCED_167_EXACT_PROMOTION_RECEIPT.json');assert receipt['recipesPromoted']==167
 files=[G/'START_HERE.md',A/'GPT_REVIEW_CONTINUATION_HANDOFF.md',A/'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json',R/'data/playtest/game_development_coverage.json',R/'docs/mechanics/GAME_DEVELOPMENT_COVERAGE.md',R/'tools/build_crafting_recipe_review_catalog.py',R/'tools/build_crafting_review_queue.py',R/'data/director/crafting_recipe_review_catalog.json',R/'data/playtest/crafting_recipe_review_catalog_public.json',R/'docs/mechanics/CRAFTING_RECIPE_REVIEW_INDEX.md',R/'docs/director-only/CRAFTING_REVIEW_QUEUE.md',A/'CRAFTING_RECIPE_REVIEW_CATALOG_VALIDATION.json',A/'CRAFTING_REVIEW_QUEUE_VALIDATION.json']
 archive=A/'navigation-before-advanced-promotion';assert not archive.exists();archive.mkdir()
 for p in files:
  q=archive/rel(p);q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);assert sha(q)==sha(p)
 dump(archive/'MANIFEST.json',{rel(p):sha(p) for p in files})
 p=R/'tools/build_crafting_recipe_review_catalog.py';s=p.read_text(encoding='utf-8');extra=''
 for trade in ['Enchanting','Rune Carving','Scribing','Tinkering']:
  code=trade.upper().replace(' ','_')
  extra+=f"        ('{trade}','data/director/advanced_craft_recipe_candidate_internal.json','docs/mechanics/ADVANCED_CRAFT_REVIEW_STATUS.json','docs/mechanics/{code}_CANDIDATE_RECIPE_CARDS.md','docs/director-only/{code}_INTERNAL_RECIPE_CARDS.md'),\n"
 s=replace(s,'    ]\n    batch_records=[]',extra+'    ]\n    batch_records=[]')
 s=replace(s,"if name in ('Mining','Skinning','Salvaging'):","if name in ('Mining','Skinning','Salvaging','Enchanting','Rune Carving','Scribing','Tinkering'):")
 p.write_text(s,encoding='utf-8')
 p=R/'tools/build_crafting_review_queue.py';s=p.read_text(encoding='utf-8')
 for a,b in [('len(checked_manifests)==10','len(checked_manifests)==11'),("sum(x['reviewed'] for x in rows)==520","sum(x['reviewed'] for x in rows)==687"),('prepared_only==167','prepared_only==0'),("'reviewed':520,'remaining':167","'reviewed':687,'remaining':0"),("'otherSourcePrepared':167","'otherSourcePrepared':0"),("'verifiedReviewedManifests':10","'verifiedReviewedManifests':11")]:s=replace(s,a,b)
 s=replace(s,'**520 of 687 recipes reviewed; 167 remain.** All167 remaining formulas have complete trade-specific source evidence prepared. Public operational reviews are333 of433. Source preparation is not effect approval; each remaining trade needs joint decisions,complete operational cards and exact review.','**687 of 687 recipes reviewed; zero remain for this authored-operational pass.** All433 public formulas have completed the same pass. Availability, broader integration, human balance and runtime remain separate.')
 s=replace(s,'Refresh the prepared167 advanced-trade source handoff against these completed interfaces and include the actual Tinker/device and crafting-feat comparisons. Source preparation still grants no advanced recipe approval.','Advanced167 exact review is also complete: AEX-01–07 fulfilled,7,585 existing checks,1,006 additional static checks and33 focused authored adjudications;138 protected inputs unchanged at promotion. All167 advanced cards and100 public versions are reviewed. Original sources and submitted revisions remain preserved.')
 s=replace(s,'Enchanting,Rune Carving,Scribing andTinkering now have167 complete source records,100 book bindings and50 unresolved cases in five unsent parts. The source comparison preserves21 Rune tool-list andeight component-name differences against each of two older versions.22 Scribing use-count questions,18 incomplete automaton attack profiles andfive distinct custom effects remain undecided.','Enchanting43, Rune Carving41, Scribing40 and Tinkering43 have complete reviewed operational cards,22 body variants,50 host templates and37 authored sequence dispositions. The source verdict resolves Scribing counts,automaton profiles,custom schemas and the null-year overlay; historical fields and older name variants remain preserved. Read ADVANCED_CRAFT_REVIEW_STATUS.json for exact authority and artifact hashes.')
 s=replace(s,'preserves48 complete class cards,8 engine paragraphs and210 source lines against43 pending Tinkering recipes;18 interface cases remain for joint review.','preserves48 complete class cards,8 engine paragraphs and210 source lines. Its recipe interfaces are incorporated into the reviewed advanced guide; this does not approve pending class/feat revisions or certify runtime.')
 p.write_text(s,encoding='utf-8')
 for name in ['build_crafting_recipe_review_catalog.py','build_crafting_review_queue.py']:
  run=subprocess.run([sys.executable,'-X','utf8',str(R/'tools'/name)],capture_output=True,text=True,encoding='utf-8');assert run.returncode==0,(run.stdout,run.stderr);print(run.stdout.strip())
 current='**Advanced crafting review complete:** All167 internal cards and100 public versions have completed exact authored-operational review in Calibration Review Part2. AEX-01–07 are fulfilled:7,585 existing checks,1,006 additional static checks and33 focused authored adjudications pass. All138 protected inputs were unchanged at promotion, and originals/submitted revisions remain preserved. Recipe totals are **687/687 reviewed; public433/433**. These are authored playtest rules; runtime, human balance and whole-game flow remain open. Next: onboarding and design-charter review, then remaining systems. Final joint flow precedes GitHub push; remote verification precedes careful cosmology review.'
 gathering='**Completed gathering work:** All128 Mining, Skinning and Salvaging cards,including82 public,retain their completed GEX-01/GEX-02 review. Their original evidence and full player envelope remain preserved. The advanced cohort is also complete; use the current all-recipe totals above.'
 for p in [G/'START_HERE.md',A/'GPT_REVIEW_CONTINUATION_HANDOFF.md']:
  s=p.read_text(encoding='utf-8');s,n=re.subn(r'\*\*Advanced crafting exact review submitted:\*\*[^\n]+',current,s,count=1);assert n==1
  s,n=re.subn(r'\*\*Current gathering work:\*\*[^\n]+',gathering,s,count=1);assert n==1
  if p.name=='START_HERE.md':
   s=replace(s,'| Recipes | **520 of 687 reviewed; 167 remain.** Public: 333 of 433 reviewed | All167 advanced drafts and37 worked sequences submitted; exact semantic verdict pending. Availability and integration are separate |','| Recipes | **687 of 687 reviewed; zero remain.** Public:433 of433 reviewed | All16 trades complete for authored-operational playtest. Availability, whole-game integration, balance and runtime remain separate |')
   s=s.replace('| Remaining recipes | Advanced candidates:','| Advanced recipes | Reviewed playtest cards:').replace('; exact review pending. |','; [fulfilled exact-review receipt](docs/audit/2026-10-08/full-game/ADVANCED_167_EXACT_PROMOTION_RECEIPT.json). |')
  else:s=s.replace('Current operational-pass recipe totals: **520 of687 reviewed;167 remain**. Public totals: **333 of433 reviewed;100 remain**.','Current operational-pass recipe totals: **687 of687 reviewed;zero remain**. Public totals: **433 of433 reviewed;zero remain**.')
  p.write_text(s,encoding='utf-8')
 p=R/'data/playtest/game_development_coverage.json';data=read(p);aspect=next(x for x in data['aspects'] if x['id']=='DD-29')
 for field,names in [('reviewEvidence',['advanced167-exact-reviewer-files/AEX_167_Exact_Review_Verdict.md','ADVANCED_167_EXACT_PROMOTION_RECEIPT.json']),('validationEvidence',['ADVANCED_167_EXACT_COMPLETION_VALIDATION.json'])]:
  for name in names:
   value=rel(A/name)
   if value not in aspect[field]:aspect[field].append(value)
 for key in ['advancedCraftCurrentCheckpoint','gatheringToolCurrentCheckpoint','tailoringCurrentCheckpoint','craftingFeatInterfaceCheckpoint']:
  aspect['resolvedIssueHistory'].append({'previousText':aspect[key],'resolution':'Historical cohort checkpoint preserved; current recipe total687/687,public433/433. Feat approvals remain8/335.'})
 aspect['advancedCraftCurrentCheckpoint']='REVIEWED167 advanced recipes,100public;AEX-01–07 fulfilled.7,585 existing checks,1,006 static checks,33 authored adjudications;138 protected inputs unchanged at promotion. All687 recipes/public433 complete for this pass.'
 aspect['gatheringToolCurrentCheckpoint']='REVIEWED128 gathering cards,82public;GEX-01/GEX-02 fulfilled. Historical cohort evidence retained; current total687/687.'
 aspect['tailoringCurrentCheckpoint']='REVIEWED43 Tailoring cards,29public;four finite repairs fulfilled. Historical cohort evidence retained; current total687/687.'
 aspect['craftingFeatInterfaceCheckpoint']='24pending crafting/research/language feat interfaces are part of the full327 pending feat review.8/335feats reviewed; recipe count687/687 is separate.'
 remaining=[]
 for issue in aspect['openIssues']:
  if issue.startswith(('Final four trade sources','Tinker class/device interface preparation','Current recipe pass520/')):
   aspect['resolvedIssueHistory'].append({'previousText':issue,'resolution':'Advanced source decisions and exact recipe review complete under AEX-01–07. No class/feat/runtime promotion inferred.'})
  else:remaining.append(issue)
 remaining.append('All687 recipe cards/public433 have completed authored-operational review. Complete unresolved bestiary/material crosslinks, pending feat/spell interfaces and expedition/economy integration before final whole-game flow; human balance/runtime remain separate.')
 aspect['openIssues']=remaining;aspect['completedScopes'].append('All167 advanced cards/public100 completed exact authored-operational review after AEX-01–07; all16 recipe trades now complete,687/687 and433/433public.')
 dump(p,data)
 p=A/'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json';obs=read(p)
 obs['historyBeforeAdvancedPromotion']={k:obs[k] for k in ['currentRequest','authoredProgress','nextAction','advancedCandidateProgress','threadStatus','lastCompletedExactReview'] if k in obs}
 obs.update(observedAtUtc=datetime.now(timezone.utc).isoformat(),threadStatus='Completed advanced exact verdict captured; next review not yet sent',currentRequest={'scope':'Advanced167 exact gate complete; onboarding/design-charter preparation next','exactVerdictPending':False,'promotionReceipt':'ADVANCED_167_EXACT_PROMOTION_RECEIPT.json','replyId':receipt['authority']['replyId']},authoredProgress={'advancedRecipesReviewed':167,'advancedPublicReviewed':100,'currentReviewedRecipes':687,'remainingRecipes':0,'publicReviewed':433,'existingChecks':7585,'additionalStaticChecks':1006,'focusedAuthoredCases':33},nextAction='Refresh prepared onboarding bundle against completed recipe status, include source-grounded design charter and relevant sources, submit next bounded review in Part2.',currentGoalTurnClassification='progress: fulfilled seven corrections and all finite checks, recorded167 promotions and refreshed navigation',consecutiveBlockedGoalTurns=0)
 obs['latestCompletedExactReview']=receipt['authority'];obs['lastCompletedExactReview']=receipt['authority'];obs['advancedCandidateProgress']={'status':'reviewed-authored-operational-playtest','recipes':167,'public':100,'receipt':'ADVANCED_167_EXACT_PROMOTION_RECEIPT.json','runtimeImplemented':False}
 dump(p,obs)
 run=subprocess.run([sys.executable,'-X','utf8',str(R/'tools/build_game_coverage.py')],capture_output=True,text=True,encoding='utf-8');assert run.returncode==0,(run.stdout,run.stderr);print(run.stdout.strip())
 changed={n:{'oldSha256':h,'currentSha256':sha(G/n),'preservedAt':rel(archive/n)} for n,h in receipt['protectedInputHashes'].items() if sha(G/n)!=h}
 assert all((archive/n).is_file() and sha(archive/n)==x['oldSha256'] for n,x in changed.items())
 dump(A/'ADVANCED_PROMOTION_NAVIGATION_RECEIPT.json',{'status':'PASS','archive':rel(archive),'previousProtectedNavigationFilesUpdated':changed,'unchangedOtherProtectedInputs':138-len(changed),'reviewedRecipes':687,'publicReviewedRecipes':433,'sourceInformationDeleted':0,'wholeGameClosure':'open'})
 print('Current recipe navigation687/687; protected changes are archived navigation records only.')
if __name__=='__main__':main()
