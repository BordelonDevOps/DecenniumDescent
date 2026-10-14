"""Reconcile current navigation while archiving every previous status file."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil,re,subprocess,sys
R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(G).as_posix()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
CURRENT='**Current gathering work:** All128 Mining, Skinning and Salvaging cards have completed exact authored-operational review in Calibration Review Part2. GEX-01/GEX-02 are applied;1,668 existing checks and45 focused checks pass, with82 protected inputs unchanged. All originals and submitted revisions remain preserved. Recipe totals are520/687 reviewed,167 remaining; public333/433 reviewed,100 remaining. The accepted public package uses Director verification of exact ingredient stock. The next recipe cohort is Enchanting43, Rune Carving41, Scribing40 and Tinkering43. Runtime, human balance and final whole-game flow remain open. Final joint flow precedes the authorized push, remote verification and careful cosmology review.'
def main():
 receipt=read(A/'GATHERING_128_EXACT_PROMOTION_RECEIPT.json');assert receipt['recipesPromoted']==128
 files=[G/'START_HERE.md',A/'GPT_REVIEW_CONTINUATION_HANDOFF.md',A/'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json',R/'data/playtest/game_development_coverage.json',R/'docs/mechanics/GAME_DEVELOPMENT_COVERAGE.md',R/'tools/build_crafting_recipe_review_catalog.py',R/'tools/build_crafting_review_queue.py',R/'data/director/crafting_recipe_review_catalog.json',R/'data/playtest/crafting_recipe_review_catalog_public.json',R/'docs/mechanics/CRAFTING_RECIPE_REVIEW_INDEX.md',R/'docs/director-only/CRAFTING_REVIEW_QUEUE.md',A/'CRAFTING_RECIPE_REVIEW_CATALOG_VALIDATION.json',A/'CRAFTING_REVIEW_QUEUE_VALIDATION.json']
 archive=A/'navigation-before-gathering-promotion';assert not archive.exists();archive.mkdir();saved={}
 for p in files:
  assert p.is_file(),p
  q=archive/rel(p);q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);assert sha(q)==sha(p);saved[rel(p)]=sha(p)
 dump(archive/'MANIFEST.json',saved)
 builder=R/'tools/build_crafting_recipe_review_catalog.py';s=builder.read_text(encoding='utf-8')
 anchor='    ]\n    batch_records=[]'
 extra=''
 for tr in ['Mining','Skinning','Salvaging']:
  extra+=f"        ('{tr}','data/director/gathering_tool_recipe_candidate_internal.json','docs/mechanics/GATHERING_TOOL_REVIEW_STATUS.json','docs/mechanics/{tr.upper()}_CANDIDATE_RECIPE_CARDS.md','docs/director-only/{tr.upper()}_INTERNAL_RECIPE_CARDS.md'),\n"
 assert s.count(anchor)==1;s=s.replace(anchor,extra+anchor)
 old="        cards=read(dp)['cards'];reviewed=False"
 assert s.count(old)==1;s=s.replace(old,old+"\n        if name in ('Mining','Skinning','Salvaging'):cards=[c for c in cards if c['sourceRecipe']['skill']==name]")
 builder.write_text(s,encoding='utf-8')
 qp=R/'tools/build_crafting_review_queue.py';s=qp.read_text(encoding='utf-8')
 for a,b in [('len(checked_manifests)==9','len(checked_manifests)==10'),("sum(x['reviewed'] for x in rows)==392","sum(x['reviewed'] for x in rows)==520"),('prepared_only==295','prepared_only==167'),('**392 of 687 recipes reviewed; 295 remain.** All295','**520 of 687 recipes reviewed; 167 remain.** All167'),('reviews are251 of433','reviews are333 of433'),("'reviewed':392,'remaining':295","'reviewed':520,'remaining':167"),("'otherSourcePrepared':295","'otherSourcePrepared':167"),("'verifiedReviewedManifests':9","'verifiedReviewedManifests':10")]:assert a in s,a;s=s.replace(a,b)
 start=s.index('Rebase the unsent gathering-tool packet');end=s.index('No new decisions are inferred from preparation.',start)+len('No new decisions are inferred from preparation.')
 s=s[:start]+'Mining, Skinning and Salvaging exact review is complete: GEX-01/GEX-02 fulfilled,128 cards promoted,82 public;1,668 existing and45 focused checks pass,82 protected inputs unchanged. Refresh the prepared167 advanced-trade source handoff against these completed interfaces and include the actual Tinker/device and crafting-feat comparisons. Source preparation still grants no advanced recipe approval.'+s[end:]
 qp.write_text(s,encoding='utf-8')
 for name in ['build_crafting_recipe_review_catalog.py','build_crafting_review_queue.py']:
  run=subprocess.run([sys.executable,'-X','utf8',str(R/'tools'/name)],capture_output=True,text=True,encoding='utf-8');assert run.returncode==0,(name,run.stdout,run.stderr);print(run.stdout.strip())
 for p in [G/'START_HERE.md',A/'GPT_REVIEW_CONTINUATION_HANDOFF.md']:
  text=p.read_text(encoding='utf-8');text,n=re.subn(r'\*\*Current gathering work:\*\*[^\n]+',CURRENT,text,count=1);assert n==1
  if p.name=='START_HERE.md':
   text=text.replace('**392 of 687 reviewed; 295 remain.** Public: 251 of 433 reviewed','**520 of 687 reviewed; 167 remain.** Public: 333 of 433 reviewed').replace('128 gathering-tool and 167 advanced-trade sources; availability and integration remain separate','167 advanced-trade sources; availability and integration remain separate').replace('Jewelcrafting and Fishing. Individual review','Jewelcrafting, Fishing, Mining, Skinning and Salvaging. Individual review')
  else:text=text.replace('Current operational-pass recipe totals: **392 of687 reviewed;295 remain**. Public totals: **251 of433 reviewed;182 remain**.','Current operational-pass recipe totals: **520 of687 reviewed;167 remain**. Public totals: **333 of433 reviewed;100 remain**.')
  p.write_text(text,encoding='utf-8')
 p=R/'data/playtest/game_development_coverage.json';data=read(p);aspect=next(x for x in data['aspects'] if x['id']=='DD-29')
 for name in ['GPT_GATHERING_128_EXACT_OPERATIONAL_REVIEW.md','GATHERING_128_EXACT_PROMOTION_RECEIPT.json']:
  v=rel(A/name)
  if v not in aspect['reviewEvidence']:aspect['reviewEvidence'].append(v)
 for name in ['GATHERING_128_EXACT_COMPLETION_VALIDATION.json']:
  v=rel(A/name)
  if v not in aspect['validationEvidence']:aspect['validationEvidence'].append(v)
 old=aspect['gatheringToolCurrentCheckpoint'];aspect['resolvedIssueHistory'].append({'previousText':old,'resolution':'All128 exact-reviewed and promoted after GEX-01/GEX-02; see promotion receipt.'})
 aspect['gatheringToolCurrentCheckpoint']='REVIEWED128 gathering cards,82public,17/15models;GEX-01/GEX-02 fulfilled;1,668 existing plus45 focused checks;82 protected inputs unchanged. Current520/687 reviewed,167remain;public333/433.'
 aspect['advancedCraftCurrentCheckpoint']='167 complete advanced-trade sources,100public book bindings,50 source cases;complete-file archive prepared but unsent. Refresh completed gathering and Tinker/device/feat interfaces before dispatch. No advanced effect approval.'
 remaining=[]
 for issue in aspect['openIssues']:
  if issue.startswith('Current recipe pass392/') or issue.startswith('All128 gathering complete candidates'):
   aspect['resolvedIssueHistory'].append({'previousText':issue,'resolution':'Gathering exact gate fulfilled;520 recipes reviewed,167 advanced recipes remain.'})
  else:remaining.append(issue)
 remaining.append('Current recipe pass520/687 reviewed,167remaining,public333/433. Complete Enchanting43,RuneCarving41,Scribing40,Tinkering43 and broader whole-game interfaces; source preparation is not effect approval.')
 aspect['openIssues']=remaining;aspect['completedScopes'].append('All128 gathering-tool authored operational cards,82 public, reviewed and promoted with GEX-01/GEX-02 fulfilled; full source/visibility and original paragraphs preserved.')
 dump(p,data)
 p=A/'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json';obs=read(p)
 history={k:obs[k] for k in ['currentRequest','authoredProgress','nextAction','currentGoalTurnClassification','lastCompletedExactReview','gatheringSourceConference'] if k in obs}
 obs['historyBeforeGatheringPromotion']=history
 obs['currentRequest']={'scope':'Gathering completed; preparing advanced167 source conference','exactVerdictPending':False,'verdictFile':receipt['authority']['verdictFile'],'replyId':receipt['authority']['replyId'],'promotionReceipt':'GATHERING_128_EXACT_PROMOTION_RECEIPT.json','recipesApproved':128,'nextAction':'Refresh then submit complete advanced167 source bundle','advancedSubmitted':False}
 obs['authoredProgress']={'gatheringCardsReviewed':128,'gatheringPublicReviewed':82,'checks':1713,'protectedInputs':82,'currentReviewedRecipes':520,'remainingRecipes':167,'publicReviewed':333,'completionReceipt':'GATHERING_128_EXACT_PROMOTION_RECEIPT.json'}
 obs['latestCompletedExactReview']={**receipt['authority'],'file':receipt['authority']['verdictFile'],'completionReceipt':'GATHERING_128_EXACT_PROMOTION_RECEIPT.json'};obs['lastCompletedExactReview']=obs['latestCompletedExactReview']
 obs['gatheringSourceConference']={'status':'complete; source directions reconciled,exact review completed and all128 promoted','preservedHistory':'historyBeforeGatheringPromotion.gatheringSourceConference'}
 obs['nextAction']='Refresh advanced167 handoff, include actual Tinker/device and crafting-feat comparisons, then request finite authoring decisions in the same Part2 notebook.'
 obs['currentGoalTurnClassification']='progress: captured complete gathering exact verdict, applied both corrections, passed1713 checks and promoted128 cards';obs['consecutiveBlockedGoalTurns']=0;obs['observedAtUtc']=datetime.now(timezone.utc).isoformat()
 obs['independentProgress']['gatheringApproved']=128;obs['independentProgress']['gatheringExactReviewCompleted']=True
 obs['independentProgress']['gatheringInternalDraft'].update({'status':'Reviewed authored operational PLAYTEST','publicProjectionAuthored':True,'exactReviewSubmitted':True,'recipesApproved':128})
 dump(p,obs)
 run=subprocess.run([sys.executable,'-X','utf8',str(R/'tools/build_game_coverage.py')],capture_output=True,text=True,encoding='utf-8');assert run.returncode==0,(run.stdout,run.stderr);print(run.stdout.strip())
 print('Current navigation reconciled; previous statuses preserved in '+rel(archive))
if __name__=='__main__':main()
