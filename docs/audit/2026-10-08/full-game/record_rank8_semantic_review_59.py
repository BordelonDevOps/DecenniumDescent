"""Preserve bounded correction handoff and advance review navigation only."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import copy,hashlib,json,zipfile
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_bytes())
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
 now=datetime.now(timezone.utc).isoformat();checks=[]
 def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
 old=A/'ACTIVE_AUTHORING_CHECKPOINT_GITHUB_RANK8_RETURN_58.json';cp=read(old)
 oldq=G/cp['currentWorkQueue']['path'];q=read(oldq);originalq=copy.deepcopy(q)
 out=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK8_SEMANTIC_REVIEW_59.json';report=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK8_SEMANTIC_REVIEW_59_CHECK.json'
 newq=R/'data/director/spell_review/remaining_work_queue_48.json';keep=A/'navigation-before-rank8-semantic-review-59'
 packet=A/'DD_Rank8_Damage6_Local_Corrections_01.zip';prep=A/'RANK8_DAMAGE6_LOCAL_CORRECTIONS_01_PREPARATION.json';request=A/'GPT_PART5_RANK8_DAMAGE_CORRECTIONS_11_REQUEST.txt'
 ck('Fresh outputs',not any(p.exists() for p in [out,report,newq,keep,packet,prep,request]))
 ck('Exact checkpoint58',info(old)['sha256']=='ca821d87d6af12aad7a5efb4a701d24440d25c951ad078db8e8432e2902f67de')
 ck('Exact queue47',info(oldq)==cp['currentWorkQueue'])
 reviewpath=A/'RANK8_DAMAGE6_PART5_RETURN_01_SEMANTIC_REVIEW_59.json';review=read(reviewpath)
 ck('Bound semantic review',info(reviewpath)['sha256']=='3b366004312585825975317019bf1cd5d9db2419e406734a3aef74298c7e0b78' and review['findingsCount']==8 and review['diagnosticCheckCount']==96 and review['diagnosticFailures']==4 and review['newAcceptedIdentities']==0)
 nativepath=A/'GPT_PART5_RANK7_LIVE_AT_RANK8_REVIEW_59_NATIVE.json';native=read(nativepath)
 ck('Specific current Rank7 review live',native['thread']['status']['type']=='active' and native['turns'][0]['id']=='300380f5-c52b-471a-9eb5-f8251396eac2' and not any(i['type']=='agentMessage' for i in native['turns'][0]['items']))
 protected=[old,oldq,R/'data/public/spell_playtests/catalog.json',R/'data/playtest/game_development_coverage.json']
 for k in ['currentAuthoredIndex','currentAcceptedInterfaceRegistry','decisionLedger']:
  b=cp[k];ck('Protected binding '+k,info(G/b['path'])==b);protected.append(G/b['path'])
 for b in cp['canonicalHelperBaselinesUnchanged']:
  ck('Helper baseline '+b['path'],info(G/b['path'])==b);protected.append(G/b['path'])
 preserved={p:p.read_bytes() for p in protected}
 prompt=('Please perform a bounded correction conference on the exact Rank8Damage6 return after finishing the separate Rank7IdentityCasting5 request. This request is prepared locally and is not evidence of dispatch until an actual chat acknowledgment is preserved. The owner implementation reservation remains in force.\n\n'
 'Original complete return: DD_Rank8_Damage_6_Part5_Conference_Return_01.zip,4912092bytes,SHA256119bfa063012d4c8c870ad6385c680a7c00c153d778c83bad08ae9895ff935d0. Original MODEL1673824bytes,SHA256df8dd333da82c14178d21657e0702671506e1c30d3ed87d5204993ef8061bc90. Preserve all original input/return bytes.\n\n'
 'Independent local review read all6 procedures,6 shared clauses,20 question dispositions and12 main/41 branch cases.559 earlier checks establish source/manifest/forward/reverse preservation.96 subsequent diagnostics include92 passes and4 concrete failures; they are not runtime tests. The following8 findings include confirmed defects and explicitly marked questions. Review each against the exact bound source, correct what the source requires and explain any disagreement with complete evidence. Do not treat a request for clarification as an already-selected new mechanic.\n\n')
 prompt += json.dumps(review['findings'],ensure_ascii=False,indent=2)
 prompt += ('\n\nReturn full corrected procedure/case mirrors and chapters, actual source-qualified initial actors, complete timelines/RNG/state outcomes, a disposition for each finding, and exact full before/after operations from this returned MODEL and its dependent artifacts. Show any new bridge as narrowly scoped authorship, especially the failed-concentration case of an already-committed instantaneous Pyre blast. Do not change generic Ready, discard the caster self-hit, selectively exclude a co-located Greater Dispel target, or override geometry with a true flag. Add meaningful diagnostic examples for the repaired cases; distinguish numerical checks, authored semantics and production runtime.\n\n'
 'Retain all six identities/ranks/access/printed damage, the original source-only candidate,37 original source-to-successor operations and every previous report. A new composed path must bind its actual starting bytes; do not apply both original and incremental paths twice. Reconcile MODEL/currentVectors, CASE_DISPOSITIONS, DIRECTOR_REVIEW, spell dispositions, specification fixtures/reports and exact-operation mirrors wherever affected. Identify which unchanged artifacts stay exact. Preserve 525 reviewed/323 pending/249 standalone/173 interfaces and39 accepted-but-unapplied; these six remain unaccepted locally until the bounded corrections and evidence reconcile. No canonical rule, index, registry, runtime, cosmology or release application is authorized.\n')
 request.write_text(prompt,encoding='utf-8',newline='\n')
 members={'input/'+Path(review['package']['path']).name:(G/review['package']['path']).read_bytes(),'LOCAL_SEMANTIC_REVIEW.json':reviewpath.read_bytes(),'LOCAL_DIAGNOSTICS.py':(A/'audit_rank8_damage_part5_semantics_01.py').read_bytes(),'REQUEST.txt':request.read_bytes()}
 for b in review['sourceBindings']:
  ck('Exact correction source '+b['path'],info(G/b['path'])==b);members['sources/'+b['path']]=(G/b['path']).read_bytes()
 manifest={'id':'RANK8-DAMAGE6-LOCAL-CORRECTIONS-01','recordedAtUtc':now,'status':'PREPARED_UNSENT','files':[{'path':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for n,b in members.items()],'scope':'Eight local source-linked findings; complete original GPT return preserved. No proposed successor or canonical edits yet.'}
 with zipfile.ZipFile(packet,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for n,b in members.items():z.writestr(n,b)
  z.writestr('MANIFEST.json',enc(manifest))
 with zipfile.ZipFile(packet) as z:
  ck('Correction packet CRC',z.testzip() is None)
  for n,b in members.items():ck('Correction packet exact member '+n,z.read(n)==b)
 prep.write_bytes(enc({'recordedAtUtc':now,'status':'PREPARED_UNSENT','archive':info(packet),'request':info(request),'review':info(reviewpath),'boundFiles':len(members),'archiveMembers':len(members)+1,'findings':8,'implementationApplied':False}))
 phases={'rank8-damage6':'returned-proposed-conference-needs-bounded-corrections','rank7-identity-casting5':'actual-source-conference-review-in-progress'}
 for g in q['groups']:
  if g['group'] not in phases:continue
  g['priorObservationBefore59']={k:copy.deepcopy(g[k]) for k in ['phase','latestObservedStatus'] if k in g}
  g['phase']=phases[g['group']]
  if g['group']=='rank8-damage6':
   g.update(returnArchive=review['package'],proposedModel=review['model'],localSemanticReview=info(reviewpath),boundedCorrectionPreparation=info(prep),newAcceptedIdentities=0,returnedProposedMainCases=12,returnedProposedBranches=41,latestObservedStatus='Full proposed return received; independent semantic review identifies8 bounded findings. Correction handoff prepared UNSENT while separate Rank7 conference responds.')
  else:g.update(actualReviewRequest=info(A/'GPT_PART5_RANK7_IDENTITY_CONFERENCE_10_REQUEST.txt'),actualNativeConfirmation=info(nativepath),actualUserTurn='300380f5-c52b-471a-9eb5-f8251396eac2',latestObservedStatus='Actual separate five-spell conference is responding; no completed response or semantic acceptance yet.')
 for row in q['rows']:
  if row.get('currentGroup') in phases:
   row['previousPhaseBefore59']=row['currentPhase'];row['currentPhase']=phases[row['currentGroup']]
   row['nextAction']='Confer on the prepared8 local findings after Rank7 reply; independently verify corrected full successor. No canonical application.' if row['currentGroup']=='rank8-damage6' else 'Retrieve and independently review the active full Rank7 conference response when complete.'
 q.update(id='REMAINING-WORK-QUEUE-48',recordedAtUtc=now,previousQueue=info(oldq),pendingDistribution=dict(Counter(r['currentPhase'] for r in q['rows'])))
 q['previousSummaryBefore59']={k:copy.deepcopy(q[k]) for k in ['limitations','deliveredContextNotYetConferenced']}
 q['limitations']='Current through checkpoint59: applied525/323/249 and173 interfaces unchanged;39 accepted-but-unapplied (24 exact accepted/staged plus15 full Control successor). Rank8Damage6 return has8 local findings and is not accepted. Rank7IdentityCasting5 is actively responding. Preparation-only Ready successor is verified but unapplied.44 groups cover281 pending identities;42 rank9 identities remain ungrouped. Older summaries remain explicit history, not current live status. No runtime/human/balance/cosmology/domain/release closure.'
 q['deliveredContextNotYetConferenced']='Rank7IdentityCasting5 is the current live conference; Rank8Damage6 has returned and awaits the prepared bounded correction conference. Other unsent source packets retain their distinct queue phases.'
 q['currentRank8SemanticReview']=info(reviewpath);q['currentRank8CorrectionHandoff']=info(prep);q['acceptedButUnappliedTotalAt59']=39
 for p in [reviewpath,prep,packet,request,nativepath]:q['sourceBindings'].append(info(p))
 ck('Membership and source rows unchanged',len(q['rows'])==323 and all(a['id']==b['id'] and a['currentIndexEntryUnchanged']==b['currentIndexEntryUnchanged'] and a['completeCurrentSourceAndAccess']==b['completeCurrentSourceAndAccess'] for a,b in zip(q['rows'],originalq['rows'])))
 ck('Groups unchanged',len(q['groups'])==44 and all(a['identities']==b['identities'] and a['candidate']==b['candidate'] and a['archive']==b['archive'] for a,b in zip(q['groups'],originalq['groups'])))
 ck('Count totals',sum(q['pendingDistribution'].values())==323 and q['preparedOrActualReviewIdentityCount']==281 and q['originalSourceOrReceiptWorkCount']==42)
 newq.write_bytes(enc(q))
 navpaths=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html'];nav={p:p.read_bytes() for p in navpaths}
 for b in cp['navigation']:ck('Prior navigation exact '+b['path'],info(G/b['path'])==b)
 keep.mkdir()
 for p,b in nav.items():(keep/p.name).write_bytes(b)
 base='docs/audit/2026-10-08/full-game/'
 for p,prefix in [(navpaths[0],''),(navpaths[1],'../../../')]:
  b=nav[p];pos=b.index(b'\n')+1
  notice=('\n**Current semantic review — 20 October 2026:** [Checkpoint59]('+prefix+base+out.name+') records full local reading of Rank8Damage6 procedures and12 main/41 branch cases. [Eight bounded findings]('+prefix+base+reviewpath.name+') need reconciliation: Ready self-damage concentration, actual cover geometry, complete dispel capture and fixture/timing corrections.92 numerical checks passed;4 diagnostic failures expose concrete gaps. Correction packet prepared UNSENT; GPT continues Rank7IdentityCasting5. Queue48 retains525 reviewed/323 pending/249 standalone,173 interfaces,39 accepted-unapplied,281 grouped/42 ungrouped pending. GitHub backup remains through57; no gameplay application.\n').encode()
  p.write_bytes(b[:pos]+notice+b[pos:]);ck('Prior bytes retained '+p.name,p.read_bytes().replace(notice,b'',1)==b)
 p=navpaths[2];b=nav[p];pos=b.index(b'</h1>')+len(b'</h1>')
 notice=('<section class="sequence" aria-label="Current semantic review"><p><strong>Checkpoint59: Rank8 return needs8 bounded corrections.</strong>Full12 main/41 branch review completed;92 numerical checks passed and4 diagnostics expose missing/inconsistent inputs. GPT continues Rank7IdentityCasting5; correction packet prepared UNSENT. <a href="'+base+out.name+'">Current checkpoint</a> · <a href="'+base+reviewpath.name+'">Findings</a></p></section>').encode()
 p.write_bytes(b[:pos]+notice+b[pos:]);ck('Prior map preserved',p.read_bytes().replace(notice,b'',1)==b)
 cp.update(id='ACTIVE-AUTHORING-RANK8-SEMANTIC-REVIEW-59',recordedAtUtc=now,previousCheckpoint=info(old),status='Full local Rank8 semantic assessment identifies8 bounded findings; correction packet prepared UNSENT. Separate Rank7IdentityCasting5 review remains active.',currentWorkQueue=info(newq),navigation=[info(p) for p in navpaths],preservedNavigation=[info(keep/p.name) for p in navpaths],lastUsageObservation={'usedPercent':13,'remainingPercent':87,'stopAtRemainingPercent':20},previousGoalTurnClassification='progress: independently reviewed all six procedures,20 decisions,12 main/41 branch cases; produced8 source-linked findings and96 diagnostics; prepared complete correction handoff and reconciled current queue status.',laterLocalWork='Checkpoint58 Rank8 inbound preservation and this semantic review/correction packet,Queue48,checkpoint59 and navigation follow verified GitHub backup through57.',nextAction='Do not interrupt active Rank7IdentityCasting5. On its completed response receive/preserve/verify it,then deliver prepared Rank8 bounded corrections and require a full exact successor. Continue42 ungrouped rank9 source identities meanwhile. Preserve canonical implementation reservation; stop at20 percent remaining.')
 cp['completedRank8Damage6Return'].update(localSemanticReview=info(reviewpath),status='BOUNDED_CORRECTIONS_REQUIRED_NOT_ACCEPTED',correctionHandoff=info(prep),acceptedAggregateIncrement=0)
 cp['activeGptReviewAtLastVerifiedObservation'].update(userTurn='300380f5-c52b-471a-9eb5-f8251396eac2',nativeConfirmation=info(nativepath),note='Fresh native evidence now identifies the actual Rank7 request UUID and active status; no completed assistant response observed.')
 cp['queueObservationSupersession']='Queue48 now records the actual received Rank8 corrections state and active Rank7 review, preserving the complete Queue47 and its old summary text as history.'
 out.write_bytes(enc(cp))
 for p,b in preserved.items():ck('Protected authority unchanged '+p.relative_to(G).as_posix(),p.read_bytes()==b)
 ck('Applied counts and acceptance unchanged',cp['authoredCounts']=={'reviewed':525,'pending':323,'standalone':249,'total':848} and cp['acceptedButUnapplied']==39 and not cp['implementationApplied'])
 report.write_bytes(enc({'recordedAtUtc':now,'checkpoint':info(out),'checks':checks,'checkCount':len(checks),'failures':0,'sourceInformationDeleted':0,'canonicalImplementationApplied':False,'scope':'Correction packet/source preservation, current queue bookkeeping and navigation only; does not erase the4 diagnostic failures or confer semantic acceptance.'}))
 print(json.dumps({'checkpoint':info(out),'queue':info(newq),'correctionPacket':info(packet),'preparation':info(prep),'check':info(report),'checks':len(checks),'failures':0}))

if __name__=='__main__':main()
