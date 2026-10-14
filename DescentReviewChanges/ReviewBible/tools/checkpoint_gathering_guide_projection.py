"""Update current navigation after the GI verdict and guide/projection checks."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil
R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
files=[G/'START_HERE.md',A/'GPT_REVIEW_CONTINUATION_HANDOFF.md',A/'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json',A/'GATHERING_TOOL_PART2_DISPATCH.json',R/'data/playtest/game_development_coverage.json',R/'docs/director-only/GATHERING_TOOL_INTERNAL_DRAFT_INDEX.md',A/'GATHERING_TOOL_GUIDE_PROJECTION_VALIDATION.json',A/'GATHERING_TOOL_CANDIDATE_ARITHMETIC_CASES.json',A/'GATHERING_TOOL_INTERNAL_AUTHORING_STATUS.json']
archive=A/'navigation-before-gathering-guide-projection-checkpoint';assert not archive.exists();archive.mkdir()
manifest=[]
for p in files:
 dst=archive/p.name;shutil.copy2(p,dst);manifest.append({'original':p.relative_to(G).as_posix(),'savedAs':dst.name,'sha256':sha(dst)})
dump(archive/'MANIFEST.json',manifest)
current='''**Current gathering work:** GPT's joint GI-01–12 source reconciliation is complete. GI-11-C1 corrects surviving residue versus physical loss; GI-12-C1 corrects Skinning structural coverage. Both are applied separately, with original evidence preserved. All128 internal cards,82 public cards,17 internal/15 public body models,three auxiliary models and four operational guides are authored. All492 public-book paragraphs remain exact. The guide/projection validator passes824 checks, with1,536 explicit manufacturing rows,544 structural inputs and256 restoration quotations; these are authored-data/reference-arithmetic evidence, not runtime or balance tests. Complete finite physical/qualification sequences and all eight joint seams remain next, followed by separate exact GPT review. Zero gathering cards are approved. Reviewed recipes remain392/687, public251/433. Source preservation, final joint whole-game flow, authorized push, verified remote commit and then careful cosmology review remain the governing sequence.'''
for p in [G/'START_HERE.md',A/'GPT_REVIEW_CONTINUATION_HANDOFF.md']:
 s=p.read_text(encoding='utf-8');lines=s.splitlines()
 for i,line in enumerate(lines):
  if line.startswith('**Current joint work:**'):
   lines[i]=current;break
 else:lines.insert(2,current)
 s='\n'.join(lines)+'\n'
 # Preserve all historical checkpoints while clearly labeling their time scope.
 if p.name=='GPT_REVIEW_CONTINUATION_HANDOFF.md':
  s=s.replace('## Next prepared source evidence','## Historical source-preparation checkpoints\n\nThe current header and CURRENT_OBSERVATION record supersede earlier pending/active labels below. These dated stages remain as historical context.',1)
  s=s.replace('**Current gathering conference:**','**Historical gathering conference checkpoint:**')
  s=s.replace('## Live Part 2 checkpoint','## Earlier completed Part 2 reviews',1)
 p.write_text(s,encoding='utf-8')
idx=R/'docs/director-only/GATHERING_TOOL_INTERNAL_DRAFT_INDEX.md'
idx.write_text('''# Gathering tools — candidate index

**128 authored candidates; zero new approvals.** The reviewed recipe total remains392/687. Joint source reconciliation is complete; exact-card review remains pending. Original sources and earlier drafts are preserved.

| Trade | All internal cards | Public cards |
|---|---|---|
| Mining | [43 cards](MINING_INTERNAL_RECIPE_CARDS.md) | [29 cards](../mechanics/MINING_CANDIDATE_RECIPE_CARDS.md) |
| Skinning | [43 cards](SKINNING_INTERNAL_RECIPE_CARDS.md) | [28 cards](../mechanics/SKINNING_CANDIDATE_RECIPE_CARDS.md) |
| Salvaging | [42 cards](SALVAGING_INTERNAL_RECIPE_CARDS.md) | [25 cards](../mechanics/SALVAGING_CANDIDATE_RECIPE_CARDS.md) |

Use the [internal operational guide](GATHERING_TOOL_INTERNAL_OPERATIONAL_GUIDE.md), [player shared guide](../mechanics/GATHERING_TOOL_CANDIDATE_GUIDE.md), and [complete preserved source directions](GATHERING_TOOL_INTERNAL_SOURCE_DIRECTIONS.md). The [internal JSON](../../data/director/gathering_tool_recipe_candidate_internal.json) retains every original object, separate operational additions and17 output models. The [public JSON](../../data/crafting/gathering_tool_recipe_candidate_public.json) contains82 cards,15 models and all492 public-book paragraphs. Both include the same three auxiliary models.

The actual [GI-01–12 reply](../../../../docs/audit/2026-10-08/full-game/GPT_GATHERING_JOINT_SOURCE_RECONCILIATION.md) authorizes exact-card authorship, with corrected residue accounting and Skinning structural counts. It does not approve cards. The source tally erratum remains separately preserved.

[Guide/projection validation](../../../../docs/audit/2026-10-08/full-game/GATHERING_TOOL_GUIDE_PROJECTION_VALIDATION.json) passes824 checks. Independent authored-reference arithmetic covers1,536 explicit manufacturing rows,544 structural inputs including Broken,3,264 reference transitions and256 repair quotations. Source/register/manuscript checks are separate. Neither result proves physical histories, actual stock, runtime execution or campaign balance.

Supplemental material profiles require exact public authority:82 component occurrences have matching public profiles;203 retain their ingredient/consumption requirements while extra metadata is withheld and preserved internally. Full player envelopes remain subject to exact review.

Next: finish all finite physical/qualification sequences and the eight combined seams, then submit every complete card and guide for exact GPT review. All128 gathering cards remain unapproved. Cosmology remains after final joint whole-game flow, the authorized push and verified remote commit.
''',encoding='utf-8')
obsp=A/'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json';obs=read(obsp);cap=read(A/'GATHERING_JOINT_SOURCE_RECONCILIATION_REPLY_CAPTURE.json')
obs['observedAtUtc']=datetime.now(timezone.utc).isoformat();obs['currentRequest'].update(sourceVerdictPending=False,notebookStatusAsObserved='idle; completed joint source response captured',actualLastObservedTurn=cap['turnId'],actualReplyId=cap['replyId'],liveObservationFile='GATHERING_JOINT_SOURCE_RECONCILIATION_REPLY_CAPTURE.json',nextAction='Complete finite physical/qualification sequences, then separate exact-card dispatch; no new request pending')
obs['latestCompletedSourceConference']={'turnId':cap['turnId'],'replyId':cap['replyId'],'file':'GPT_GATHERING_JOINT_SOURCE_RECONCILIATION.md','captureEvidence':'GATHERING_JOINT_SOURCE_RECONCILIATION_REPLY_CAPTURE.json','scope':'GI-01–12 source reconciliation; GI-11-C1/GI-12-C1 applied; no exact approval'}
obs.setdefault('independentProgress',{}).update(gatheringInternalCardsAuthored=128,gatheringPublicCardsAuthored=82,gatheringInternalBodies=17,gatheringPublicBodies=15,gatheringAuxiliaryModels=3,gatheringGuideProjectionChecks=824,gatheringManufacturingRows=1536,gatheringStructuralPositiveInputs=442,gatheringStructuralInputsIncludingZero=544,gatheringStructuralReferenceTransitions=3264,gatheringRestorationQuotes=256,gatheringSourceJointReconciled=True,gatheringExactReviewSubmitted=False,gatheringApproved=0)
dump(obsp,obs)
dp=A/'GATHERING_TOOL_PART2_DISPATCH.json';dispatch=read(dp);dispatch['status']='All source directions and GI-01–12 reconciled; all128 internal and82 public candidates authored; physical sequences and exact review next';dispatch['jointSourceReconciliationCompleted']={'turnId':cap['turnId'],'replyId':cap['replyId'],'file':'GPT_GATHERING_JOINT_SOURCE_RECONCILIATION.md','correctionsApplied':['GI-11-C1','GI-12-C1'],'exactApproval':False};dispatch['nextAction']='Complete finite physical/qualification sequence evidence and submit all128 complete exact candidates';dump(dp,dispatch)
covp=R/'data/playtest/game_development_coverage.json';cov=read(covp);row=next(r for r in cov['aspects'] if r['id']=='DD-29')
for field,paths in {'reviewEvidence':['docs/audit/2026-10-08/full-game/GPT_GATHERING_JOINT_SOURCE_RECONCILIATION.md'],'draftEvidence':['DescentReviewChanges/ReviewBible/docs/director-only/GATHERING_TOOL_INTERNAL_OPERATIONAL_GUIDE.md','DescentReviewChanges/ReviewBible/data/crafting/gathering_tool_recipe_candidate_public.json'],'validationEvidence':['docs/audit/2026-10-08/full-game/GATHERING_TOOL_GUIDE_PROJECTION_VALIDATION.json']}.items():
 for path in paths:
  if path not in row[field]:row[field].append(path)
row['openIssues']=[x for x in row['openIssues'] if 'gathering' not in x.lower()]+['All128 gathering internal and82 public cards/guides authored; joint source directions reconciled. Complete finite physical/qualification sequences and separate exact GPT review. No gathering promotions;167 advanced recipes and system integration remain.']
dump(covp,cov)
sp=A/'GATHERING_TOOL_INTERNAL_AUTHORING_STATUS.json';status=read(sp);status['outputs'][idx.relative_to(G).as_posix()]=sha(idx);status['guideProjectionValidation']='GATHERING_TOOL_GUIDE_PROJECTION_VALIDATION.json';status['guideProjectionChecks']=824;status['openWork']=['Complete finite physical/qualification sequences and eight joint seams','Submit all128 complete cards, guides and public envelopes for separate exact GPT review'];dump(sp,status)
print(json.dumps({'checkpoint':'gathering guides/public projection authored and validated','sourceReply':cap['replyId'],'newApprovals':0,'next':'finite physical sequences and exact candidate review'}))
