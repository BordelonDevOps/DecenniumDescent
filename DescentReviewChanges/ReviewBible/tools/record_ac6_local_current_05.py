"""Record actual GPT submission and update navigation without changing rule adoption."""
from copy import deepcopy
from datetime import datetime,timezone
from pathlib import Path
import ast,json,re,subprocess,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded
def read(p):return json.loads(p.read_bytes())
def main():
 now=datetime.now(timezone.utc).isoformat()
 previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_AC6_REPAIR_04_SUBMITTED.json'
 checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_AC6_LOCAL_CURRENT_05_SUBMITTED.json'
 delta=A/'AC6_LOCAL_CURRENT_05_NAVIGATION_DELTA.json';keep=A/'navigation-before-ac6-local-current-05'
 receipt=A/'AC6_LOCAL_CURRENT_05_SUBMISSION_RECEIPT.json'
 assert not any(p.exists() for p in [checkpoint,delta,keep,receipt])
 native=A/'AC6_LOCAL_CURRENT_05_SUBMITTED_NATIVE.json';d=read(native);turn=d['turns'][0]
 assert turn['id']=='7bbead9b-1de9-4dd6-b69c-765c77d1ccbc'
 user=next(x for x in turn['items'] if x['type']=='userMessage')
 submitted='\n'.join(x['text'] for x in user['content'] if x['type']=='text').split('\n\n[User attached')[0]
 request=(A/'AC6_LOCAL_CURRENT_05_REQUEST.txt').read_text(encoding='utf8')
 assert submitted.rstrip('\n')==request.rstrip('\n')
 attachment=next(x for x in d['attachments'] if x['name']=='DD_AC6_Local_Current_05.zip')
 archive=A/'DD_AC6_Local_Current_05.zip';assert Path(attachment['path']).read_bytes()==archive.read_bytes()
 live=A/'AC6_LOCAL_CURRENT_05_SUBMITTED_BROWSER.txt';assert 'button "Stop"' in live.read_text(encoding='utf8')
 check=A/'AC6_LOCAL_CURRENT_05_CHECK.json';assert read(check)['failureCount']==0 and read(check)['checkCount']==939
 decheck=A/'DE4_CURRENT_PROCEDURES_CHECK_03.json';assert read(decheck)['failureCount']==0
 de=R/'data/director/spell_proposals/divination_enchantment_rank4_current_03.json'
 receipt.write_bytes(encoded({'id':'AC6-LOCAL-CURRENT-05-ACTUAL-SUBMISSION','recordedAtUtc':now,'threadId':d['thread']['id'],'title':d['thread']['title'],'userTurnId':turn['id'],'archive':info(archive),'request':info(A/'AC6_LOCAL_CURRENT_05_REQUEST.txt'),'nativeEvidence':info(native),'browserEvidence':info(live),'screenshot':info(A/'PART4_AC6_LOCAL_CURRENT_05_SUBMITTED.png'),'uploadedArchiveBytesMatch':True,'exactRequestMatches':submitted==request,'requestMatchesAfterTerminalNewlineNormalization':True,'status':'Submitted once; browser shows active generation. Native user-only completed/idle record is not assistant completion.','newSpellAdoptions':0}))
 start=G/'START_HERE.md';builder=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json'
 raw={};saved=[]
 for p in [start,builder,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
  b=p.read_bytes();q=keep/p.relative_to(G);q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b);raw[p]=b
  saved.append({**info(p),'preservedCopy':q.relative_to(G).as_posix()})
 (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
 text=raw[start].decode();assert text.count(previous.relative_to(G).as_posix())==1
 text=text.replace(previous.relative_to(G).as_posix(),checkpoint.relative_to(G).as_posix(),1)
 replacement='**Current GPT conference:** The [actual AC6 Repair04 return](docs/audit/2026-10-08/full-game/DD_AC6_Repair_04_Return.zip) is preserved. Its [independent structural review](docs/audit/2026-10-08/full-game/AC6_REPAIR_04_INDEPENDENT_STRUCTURAL_CHECK.json) found one missing history copy plus remaining Chain Arc geometry and Air Pet Falling fixture issues. The [complete Local Current05 candidate](docs/audit/2026-10-08/full-game/DD_AC6_Local_Current_05.zip) repairs those issues and explicitly proposes consistent body-volume range and scoped summon-intersection suppression. [939 independent checks](docs/audit/2026-10-08/full-game/AC6_LOCAL_CURRENT_05_CHECK.json) passed, including preserved history, 189 current pointers and concrete geometry/timing. It is [submitted to actual GPT in Review Continuation Part 4](docs/audit/2026-10-08/full-game/AC6_LOCAL_CURRENT_05_SUBMISSION_RECEIPT.json). GPT is reviewing four bounded changes and remaining substantive issues. Full 55-case semantic closure and exact acceptance remain open; no AC6 spell is adopted.\n\n'
 text,n=re.subn(r'\*\*Current GPT conference:\*\*.*?\n\n',lambda _:replacement,text,count=1,flags=re.S);assert n==1
 replacement='**Next fifteen-spell group:** The [Divination/Enchantment rank-four current draft03](DescentReviewChanges/ReviewBible/data/director/spell_proposals/divination_enchantment_rank4_current_03.json) contains 15 procedures and 30 current examples, retaining 30 original texts and 75 source bindings. [418 checks](docs/audit/2026-10-08/full-game/DE4_CURRENT_PROCEDURES_CHECK_03.json) passed after correcting Portal formation compatibility, separate-controller versus self-recast Dominate Person, actual Dispel costs/resource pools, Druid ability bounds, and proposed finite Compulsion expiry when a phase is missing. The [nine-file Fate Reversal guard amendment](docs/audit/2026-10-08/full-game/DE4_FATE_GUARD_AMENDMENT_DRAFT_02.json) remains an explicit proposal. This group and its guard amendment remain unsent/unadopted; refresh any accepted AC6 dependencies before joint review.\n\n'
 text,n=re.subn(r'\*\*Next fifteen-spell group:\*\*.*?\n\n',lambda _:replacement,text,count=1,flags=re.S);assert n==1
 start.write_text(text,encoding='utf8',newline='\n')
 cov=json.loads(raw[ledger]);oldcov=deepcopy(cov)
 evidence=[A/'AC6_REPAIR_04_INDEPENDENT_STRUCTURAL_CHECK.json',check,receipt,decheck]
 for ident in ['DD-11','DD-12']:
  row=next(x for x in cov['aspects'] if x['id']==ident);old=deepcopy(row)
  row['validationEvidence'].extend(p.relative_to(G).as_posix() for p in evidence)
  row.setdefault('currentEvidenceAddenda',[]).append({'id':'ac6-local-current-05-submitted','recordedAtUtc':now,'status':'Actual Repair04 preserved; local history/body geometry/Falling corrections prepared and sent to actual GPT. DE4 current03 corrections complete locally, unsent. No semantic closure/adoption.','checks':939,'failures':0,'de4Checks':418,'de4Failures':0,'newRuleAdoptions':0})
  assert all(row[k]==old[k] for k in ['status','closure','humanEvidence','completionClass'])
 assert [x for x in cov['aspects'] if x['id'] not in ['DD-11','DD-12']]==[x for x in oldcov['aspects'] if x['id'] not in ['DD-11','DD-12']]
 ledger.write_bytes(encoded(cov))
 code=raw[builder].decode();tail=' + read(A / "AC6_REPAIR_04_NAVIGATION_DELTA.json")["changes"]\n';assert code.count(tail)==1
 code=code.replace(tail,tail.rstrip('\n')+' + read(A / "AC6_LOCAL_CURRENT_05_NAVIGATION_DELTA.json")["changes"]\n',1)
 rows=[('AC6 — actual Repair04 independent review','AC6_REPAIR_04_INDEPENDENT_STRUCTURAL_CHECK.json'),('AC6 — complete Local Current05 package','DD_AC6_Local_Current_05.zip'),('AC6 —939 preservation and repaired-scenario checks','AC6_LOCAL_CURRENT_05_CHECK.json'),('AC6 — actual Local Current05 GPT submission',receipt.name),('DE4 — current03 checks and corrected scenarios',decheck.name)]
 code=code.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(row)+',\n' for row in rows),1)
 scope='451 reviewed /397 pending ordinary spells;175 complete standalone procedures. AC5 accepted/applied. AC6 actual Repair04 preserved; Local Current05 fixes history/geometry/Falling with939 checks passed and is sent to actual GPT Part4; full semantic closure and adoption remain open. DE4 current03 has15 procedures30 examples75 sources and418 checks passed, unsent/unadopted. All75 development areas and final whole-game flow remain in scope.'
 vals=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(vals)==1
 code=code.replace(ast.get_source_segment(code,vals[0]),repr(scope),1);compile(code,str(builder),'exec');builder.write_text(code,encoding='utf8',newline='\n')
 delta.write_bytes(encoded({'recordedAtUtc':now,'changes':[{'before':next(x for x in saved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,ledger,builder]],'newSpellAdoptions':0,'fullDomainClosureChanged':False,'sourceInformationDeleted':0}))
 run=subprocess.run([sys.executable,'-X','utf8',str(builder)],capture_output=True,text=True,encoding='utf8');assert run.returncode==0,(run.stdout[-1000:],run.stderr[-1000:])
 build=read(A/'REVIEW_MAP_BUILD.json');assert not build['missingLinks']
 state=read(previous);priorreview=deepcopy(state['activeGptReview'])
 priorreview.update(status='Actual Repair04 downloaded and preserved. Independent746 structural checks had one missing NX-D02 prior-case copy; geometry/Falling defects also found. Corrected locally in Current05; not adopted.',returnReceived=True,generationConfirmedLiveAtObservation=False,returnedArchive=info(A/'DD_AC6_Repair_04_Return.zip'),structuralCheck=info(A/'AC6_REPAIR_04_INDEPENDENT_STRUCTURAL_CHECK.json'),completionNative=info(A/'AC6_REPAIR_04_COMPLETED_NATIVE.json'))
 state.setdefault('priorGptReviews',[]).append(priorreview)
 state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='progress: actual AC6 Repair04 independently checked and DE4 current03 locally corrected',coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),newRuleAdoptions=0,newRuleAdoptionScope='Complete local AC6 Current05 correction submitted. No accepted ordinary spell or domain closure changed.',navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':build['existingDistinctLinks'],'missingLinks':[]})
 state['activeGptReview']={**state['activeGptReview'],'reviewId':'AC6-LOCAL-CURRENT-05','submission':info(receipt),'userTurnId':turn['id'],'status':'Actual Current05 sent once; browser confirms active assistant generation. Wait on this same submission, do not resend/restart due timeout.','generationConfirmedLiveAtObservation':True,'expectedReturn':'DD_AC6_Local_Current_05_Review.zip','returnReceived':False,'newRulesAdopted':False,'lastSuccessfulObservation':info(live),'currentPackage':info(archive),'currentCandidateDirectory':(A/'ac6-local-current-05').relative_to(G).as_posix(),'independentCheck':info(check),'substantiveReviewComplete':False}
 dep=state['de4CurrentPreparation']
 dep.update(currentDraft=info(de),currentDraftCheck=info(decheck),currentProcedureCount=15,newWorkedExamples=30,currentDraftSourceCount=75,status='Current03 contains local corrections to Portal, control replacement, Dispel resources, Druid ability score and proposed finite Compulsion expiry;418 checks pass. Unsent/unadopted. Refresh accepted AC6 dependencies and submit full group plus nine-file Fate guard for joint review.')
 if 'remainingLocalSemanticCorrections' in dep:dep['priorLocalSemanticCorrectionRecord']=dep.pop('remainingLocalSemanticCorrections')
 dep['remainingJointChoices']=['Source-scoped Seal loci and Divination suppression','Fate Reversal shared guard across three spells and exact nine-file amendment','Dominate Person same-plane order delivery','Finite Compulsion expiry after one original eligible opportunity, including missing-phase bookkeeping','Separate Phantasmal Killer root provenance']
 state['safeNextActions']=[
  'Continue SAME Part4 Current05 review user turn7bbead9b-1de9-4dd6-b69c-765c77d1ccbc using tab125746324. Native user-only idle/completed is not terminal assistant evidence. Do not resend or restart.',
  'When DD_AC6_Local_Current_05_Review.zip arrives, preserve exact bytes and independently verify the four dispositions, all bound input hashes, actual source evidence, declared semantic review scope and any proposed changes. Local939 checks passed but full55-case semantic closure remains open. Do not adopt from narrow checks.',
  'AC6 Current05 is complete unadopted candidate under ac6-local-current-05. It retains all14/16 source/access,103 sources,22 texts,55 cases. Return04/03 archives and changed current records are preserved. Interrupted first chapter build is retained under ac6-local-current-05-interrupted-chapter-build; do not use it as current.',
  'DE4 current03 has15 procedures30 examples75 sources,418 checks passed; old30 texts and corrected prior cases retained. It and nine-file Fate guard remain unsent/unadopted. Finite Compulsion opportunity/expiry is explicit new authorship, not accepted existing rule. FieldRepair example may benefit from explicit touch/recharge availability when next reviewed.',
  'All16 AC5 procedures remain applied. Do not rerun one-shot preparation/application scripts. Counts451 reviewed397 pending,175 standalone procedures are unchanged.',
  'Continue all75 development areas including remaining spells/environment/consumables/disease/feats/bestiary/Director/packaging/companion interfaces and final actual GPT whole-game flow. Latest verified GitHub backup18c6e3a predates this local work.'
 ]
 state['resumedBlockedAudit']={'classification':'progress','meaningfulProgress':'Prepared and independently verified complete AC6 Current05 corrections, submitted to actual GPT, and recorded DE4 current03 completion. No adoption or closure claim.','evidence':info(check),'activeReviewObservation':info(live)}
 state.setdefault('preservationManifests',[]).append(info(keep/'PRESERVATION_MANIFEST.json'));checkpoint.write_bytes(encoded(state))
 print(json.dumps({'checkpoint':info(checkpoint),'submission':info(receipt),'links':build['existingDistinctLinks'],'missingLinks':0,'newSpellAdoptions':0,'currentOrdinarySpells':state['currentOrdinarySpellCounts'],'activeReviewUserTurn':turn['id']}))
if __name__=='__main__':main()
