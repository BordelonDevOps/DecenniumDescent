"""Record observed Current06 submission without interpreting stale native data as failure."""
from copy import deepcopy
from datetime import datetime,timezone
from pathlib import Path
import ast,json,re,subprocess,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded
def read(p): return json.loads(p.read_bytes())
def main():
 now=datetime.now(timezone.utc).isoformat()
 previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_AC6_LOCAL_CURRENT_05_SUBMITTED.json'
 checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_AC6_SEMANTIC_CURRENT_06_SUBMITTED.json'
 delta=A/'AC6_SEMANTIC_CURRENT_06_NAVIGATION_DELTA.json'
 keep=A/'navigation-before-ac6-semantic-current-06'
 receipt=A/'AC6_SEMANTIC_CURRENT_06_SUBMISSION_RECEIPT.json'
 assert not any(p.exists() for p in [checkpoint,delta,keep,receipt])
 prep=read(A/'AC6_SEMANTIC_CURRENT_06_PREPARATION.json')
 for record in [prep['archive'],prep['request'],prep['independentCheck'],prep['semanticReview'],*prep['candidateFiles']]:
  assert info(G/record['path'])==record
 check=A/'AC6_SEMANTIC_CURRENT_06_CHECK.json'
 assert read(check)['checkCount']==851 and read(check)['failureCount']==0
 live=A/'AC6_SEMANTIC_CURRENT_06_SUBMITTED_BROWSER.txt'
 progress=A/'AC6_SEMANTIC_CURRENT_06_PROGRESS_BROWSER.txt'
 request=(A/'AC6_SEMANTIC_CURRENT_06_REQUEST.txt').read_text(encoding='utf8')
 dom=live.read_text(encoding='utf8')
 assert ' '.join(request.split()) in ' '.join(dom.split())
 assert 'DD_AC6_Semantic_Current_06.zip' in dom and 'button "Stop"' in dom
 assert 'button "Stop"' in progress.read_text(encoding='utf8')
 state=read(previous)
 receipt.write_bytes(encoded({'id':'AC6-SEMANTIC-CURRENT-06-ACTUAL-SUBMISSION','recordedAtUtc':now,'threadId':'6ad1acef-455c-83ea-bc33-56e4adaec9c8','title':'Review Continuation Part 4','browserTabId':'125746324','userTurnId':None,'archive':prep['archive'],'request':prep['request'],'browserEvidence':info(live),'progressEvidence':info(progress),'screenshot':info(A/'PART4_AC6_SEMANTIC_CURRENT_06_SUBMITTED.png'),'requestMatchesAfterBrowserWhitespaceNormalization':True,'nativeObservationLimit':info(A/'AC6_SEMANTIC_CURRENT_06_NATIVE_OBSERVATION_LIMIT.json'),'serverAttachmentByteComparison':'Not available at this observation; local package binding verified. Browser shows submitted attachment and active review.','status':'Sent once; actual browser confirms GPT responding. Native stale prior turn and timeout do not negate browser submission. Do not resend.','newSpellAdoptions':0}))
 start=G/'START_HERE.md';builder=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json'
 raw={};saved=[]
 for p in [start,builder,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
  b=p.read_bytes();q=keep/p.relative_to(G);q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b);raw[p]=b
  saved.append({**info(p),'preservedCopy':q.relative_to(G).as_posix()})
 (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
 text=raw[start].decode();assert text.count(previous.relative_to(G).as_posix())==1
 text=text.replace(previous.relative_to(G).as_posix(),checkpoint.relative_to(G).as_posix(),1)
 replacement='**Current GPT conference:** The [actual Current05 review](docs/audit/2026-10-08/full-game/DD_AC6_Local_Current_05_Review.zip) agreed with three changes and required choosing a readied spell area at release. Our [independent semantic review](docs/audit/2026-10-08/full-game/AC6_LOCAL_CURRENT_05_SEMANTIC_REVIEW_06.json) read all 14 procedures, both Nexus modes, 55 current cases and 51 original scenarios, finding additional critical-hit, dispel, barrier and omitted-example issues. The [complete Current06 candidate](docs/audit/2026-10-08/full-game/DD_AC6_Semantic_Current_06.zip) contains eight findings and 25 corrected cases, preserves prior versions, and passed [851 focused checks](docs/audit/2026-10-08/full-game/AC6_SEMANTIC_CURRENT_06_CHECK.json). It is [submitted to actual GPT in Review Continuation Part 4](docs/audit/2026-10-08/full-game/AC6_SEMANTIC_CURRENT_06_SUBMISSION_RECEIPT.json). GPT is reviewing it; exact acceptance and adoption remain open. No AC6 spell is adopted.\n\n'
 text,n=re.subn(r'\*\*Current GPT conference:\*\*.*?\n\n',lambda _:replacement,text,count=1,flags=re.S);assert n==1
 start.write_text(text,encoding='utf8',newline='\n')
 cov=json.loads(raw[ledger]);oldcov=deepcopy(cov)
 for ident in ['DD-11','DD-12']:
  row=next(x for x in cov['aspects'] if x['id']==ident);old=deepcopy(row)
  row['validationEvidence'].extend(p.relative_to(G).as_posix() for p in [A/'AC6_LOCAL_CURRENT_05_SEMANTIC_REVIEW_06.json',check,receipt])
  row.setdefault('currentEvidenceAddenda',[]).append({'id':'ac6-semantic-current-06-submitted','recordedAtUtc':now,'status':'Actual GPT Current05 review preserved; Current06 includes eight findings and 25 corrected cases, sent to GPT. No exact acceptance/adoption.','checks':851,'failures':0,'newRuleAdoptions':0})
  assert all(row[k]==old[k] for k in ['status','closure','humanEvidence','completionClass'])
 assert [x for x in cov['aspects'] if x['id'] not in ['DD-11','DD-12']]==[x for x in oldcov['aspects'] if x['id'] not in ['DD-11','DD-12']]
 ledger.write_bytes(encoded(cov))
 code=raw[builder].decode();tail=' + read(A / "AC6_LOCAL_CURRENT_05_NAVIGATION_DELTA.json")["changes"]\n';assert code.count(tail)==1
 code=code.replace(tail,tail.rstrip('\n')+' + read(A / "AC6_SEMANTIC_CURRENT_06_NAVIGATION_DELTA.json")["changes"]\n',1)
 rows=[('AC6 — actual Current05 review','DD_AC6_Local_Current_05_Review.zip'),('AC6 — eight semantic findings','AC6_LOCAL_CURRENT_05_SEMANTIC_REVIEW_06.json'),('AC6 — complete Current06 candidate','DD_AC6_Semantic_Current_06.zip'),('AC6 — 851 focused checks',check.name),('AC6 — actual Current06 GPT submission',receipt.name)]
 code=code.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(row)+',\n' for row in rows),1)
 scope='451 reviewed /397 pending ordinary spells;175 complete standalone procedures. AC5 accepted/applied. Actual GPT Current05 review preserved; AC6 Current06 addresses eight findings and25 corrected cases with851 checks passed, submitted to actual GPT Part4. Exact acceptance/adoption remain open. DE4 current03 remains unsent/unadopted with15 procedures30 examples75 sources and418 checks. All75 development areas and final whole-game flow remain in scope.'
 vals=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(vals)==1
 code=code.replace(ast.get_source_segment(code,vals[0]),repr(scope),1);compile(code,str(builder),'exec');builder.write_text(code,encoding='utf8',newline='\n')
 delta.write_bytes(encoded({'recordedAtUtc':now,'changes':[{'before':next(x for x in saved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,ledger,builder]],'newSpellAdoptions':0,'fullDomainClosureChanged':False,'sourceInformationDeleted':0}))
 run=subprocess.run([sys.executable,'-X','utf8',str(builder)],capture_output=True,text=True,encoding='utf8');assert run.returncode==0,(run.stdout[-1000:],run.stderr[-1000:])
 build=read(A/'REVIEW_MAP_BUILD.json');assert not build['missingLinks']
 prior=deepcopy(state['activeGptReview'])
 prior.update(status='Actual Current05 review returned: three agreements and Ready-at-release revision. Independent review found additional substantive issues addressed in Current06; not adopted.',returnReceived=True,generationConfirmedLiveAtObservation=False,returnedArchive=info(A/'DD_AC6_Local_Current_05_Review.zip'),completionNative=info(A/'AC6_LOCAL_CURRENT_05_COMPLETED_NATIVE.json'),semanticReview=prep['semanticReview'])
 state.setdefault('priorGptReviews',[]).append(prior)
 state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),newRuleAdoptions=0,newRuleAdoptionScope='Current06 submitted; no accepted spell, cosmology canon or domain closure changed.',navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':build['existingDistinctLinks'],'missingLinks':[]})
 state['activeGptReview']={**state['activeGptReview'],'reviewId':'AC6-SEMANTIC-CURRENT-06','submission':info(receipt),'userTurnId':None,'status':'Actual Current06 sent once; browser confirms active generation. Native prior-turn read was stale, then timed out. Continue same browser chat; do not resend.','generationConfirmedLiveAtObservation':True,'expectedReturn':'DD_AC6_Semantic_Current_06_Review.zip','returnReceived':False,'newRulesAdopted':False,'lastSuccessfulObservation':info(progress),'currentPackage':prep['archive'],'currentCandidateDirectory':(A/'ac6-semantic-current-06').relative_to(G).as_posix(),'independentCheck':info(check),'substantiveReviewComplete':False}
 state['safeNextActions']=[
  'Continue SAME Part4 Current06 review in tab125746324. Browser confirms submitted package and active assistant generation. Native observation returned prior05 then timed out; do not resend/restart.',
  'When DD_AC6_Semantic_Current_06_Review.zip arrives, preserve exact bytes. Independently verify all eight dispositions, eight current file hashes, archive binding, actual source evidence, declared scope and replacements. No adoption from focused851 checks alone.',
  'Current06 preserves fourteen identities/sixteen placements,103 frozen sources,22 original texts,55 ordered cases and prior versions. All14 procedures/both Nexus modes/55 cases/51 original scenarios were read during local semantic review; full semantic closure remains open.',
  'DE4 current03 and nine-file Fate guard remain unsent/unadopted; retain previous detailed preparation. Clarify FieldRepair touch/recharge fixture when reviewing. Refresh accepted AC6 dependencies before sending.',
  'Do not rerun one-shot scripts. Counts451 reviewed397 pending175 standalone unchanged. All75 areas and final GPT whole-game flow remain in scope; latest verified GitHub backup18c6e3a predates this work.'
 ]
 state['resumedBlockedAudit']={'classification':'progress','meaningfulProgress':'Prepared Current06 substantive corrections and submitted to actual GPT. Browser confirmation authoritative despite native observation lag. No adoption.','evidence':info(check),'activeReviewObservation':info(progress)}
 state.setdefault('preservationManifests',[]).append(info(keep/'PRESERVATION_MANIFEST.json'));checkpoint.write_bytes(encoded(state))
 print(json.dumps({'checkpoint':info(checkpoint),'submission':info(receipt),'links':build['existingDistinctLinks'],'missingLinks':0,'newSpellAdoptions':0,'currentOrdinarySpells':state['currentOrdinarySpellCounts']}))
if __name__=='__main__': main()
