"""Record verified Rank8 receipt and actual Rank7 dispatch, without rule adoption."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
from copy import deepcopy
import json, hashlib
G=Path(r'C:\Github\DecenniumDescent'); R=G/'DescentReviewChanges/ReviewBible'; A=G/'docs/audit/2026-10-08/full-game'
def read(p): return json.loads(p.read_bytes())
def enc(x): return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def bind(p):
 b=p.read_bytes(); return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
 old=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_ELEMENTAL_PETS_69.json'; out=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK8_RETURN_RANK7_DISPATCH_70.json'
 report=out.with_name(out.stem+'_CHECK.json'); qout=R/'data/director/spell_review/remaining_work_queue_57.json'
 navbackup=A/'navigation-before-rank8-return-rank7-dispatch-70'; savedscript=A/Path(__file__).name
 assert not any(p.exists() for p in [out,report,qout,navbackup,savedscript])
 cp=read(old); qpath=G/cp['currentWorkQueue']['path']; q0=read(qpath); q=deepcopy(q0); checks=[]
 def ck(name,ok): checks.append({'check':name,'passed':bool(ok)}); assert ok,name
 ck('Exact checkpoint69',bind(old)['sha256']=='fe359f0255f2428f22c35779e2caf2adf985058ba778409107bc05906252789b')
 protected=[old,R/'data/public/spell_playtests/catalog.json',R/'data/playtest/game_development_coverage.json']
 for key in ['currentWorkQueue','currentAuthoredIndex','currentAcceptedInterfaceRegistry','decisionLedger']:
  b=cp[key]; ck('Authority '+key,bind(G/b['path'])==b); protected.append(G/b['path'])
 for b in cp['canonicalHelperBaselinesUnchanged']:
  ck('Helper '+b['path'],bind(G/b['path'])==b); protected.append(G/b['path'])
 originals={p:p.read_bytes() for p in protected}
 pfpath=A/'RANK8_DAMAGE6_PART5_CORRECTION_RETURN_02_LOCAL_PREFLIGHT.json'; pf=read(pfpath)
 ck('1060 independent preservation checks',pf['checkCount']==1060 and pf['failures']==0 and all(c['passed'] for c in pf['checks']))
 for key in ['archive','model','nativeFinal']: ck('Returned '+key,bind(G/pf[key]['path'])==pf[key])
 nativepath=A/'GPT_PART5_RANK7_IDENTITY_CORRECTIONS_12_DISPATCH_NATIVE.json'; native=read(nativepath)
 textpath=A/'GPT_PART5_RANK7_IDENTITY_CORRECTIONS_12_DISPATCH_TEXT.txt'; user=native['turns'][0]['items'][0]
 ck('Actual submitted user message',user['id']=='da1a6a38-58f0-48f8-a594-1edade3d774f' and user['type']=='userMessage')
 ck('Exact submitted text',user['content'][0]['text'].split('\n\n[User attached')[0]==textpath.read_text(encoding='utf-8').rstrip('\n'))
 ck('Native GPT active after submission',native['thread']['status']['type']=='active')
 archive=A/'DD_Rank7_Identity_Casting5_Local_Corrections_01.zip'
 attachments=[b for b in native['attachments'] if b['name']==archive.name]
 ck('Actual attached bytes match prepared archive',len(attachments)==1 and Path(attachments[0]['path']).read_bytes()==archive.read_bytes())
 ck('Prepared Rank7 archive exact',bind(archive)['sha256']=='bbc7ed5790a0b287a43e324f545d473066dd0584328b3904b49db2563b7bd5f5' and archive.stat().st_size==14757388)
 received={'archive':pf['archive'],'model':pf['model'],'nativeFinal':pf['nativeFinal'],'localPreflight':bind(pfpath),'assistantTurn':'0d2643ff-e739-40e7-bbeb-7df819ee4a3c','status':'CORRECTED_FULL_RETURN_PRESERVED_PENDING_INDEPENDENT_SEMANTIC_REVIEW','preservationChecks':1060,'manifestFiles':98,'originalHistoryMembers':40,'mainCases':12,'independentBranches':42,'incrementalModelOperations':17,'alternativeOriginalModelOperations':54,'artifactReplacements':17,'newAcceptedIdentities':0,'implementationApplied':False}
 dispatch={'threadId':native['thread']['id'],'title':native['thread']['title'],'userTurn':user['id'],'request':bind(textpath),'fullPreparedRequest':bind(A/'GPT_PART5_RANK7_IDENTITY_CORRECTIONS_12_REQUEST.txt'),'archive':bind(archive),'nativeConfirmation':bind(nativepath),'sent':True,'completedResponseReceived':False,'attachmentBytesIndependentlyVerified':True,'scope':'Three bounded Rank7 findings: legal Adept acquisition, eight remaining Action ledgers, successful Erase history.','latestObservedStatus':'Actual user message and attached bytes verified; native GPT active after submission.'}
 for oldgroup,group in zip(q0['groups'],q['groups']):
  if group['group'] not in ('rank7-identity-casting5','rank8-damage6'): continue
  group['previousObservationBefore70']={k:deepcopy(group[k]) for k in ['phase','latestObservedStatus']}
  if group['group']=='rank8-damage6': group.update(phase='corrected-return-pending-independent-semantic-review',latestObservedStatus='Return02 completely preserved;1060 independent checks pass. Eight corrected findings and Pyre-only completion await independent semantic review.',completedCorrectionReturn=received)
  else: group.update(phase='bounded-correction-conference-actually-sent',latestObservedStatus='Three-finding correction12 actually submitted with full14,757,388-byte evidence archive; native GPT active.',actualCorrectionDispatch=dispatch)
  ck('Group identities/candidate preserved '+group['group'],group['identities']==oldgroup['identities'] and group['candidate']==oldgroup['candidate'])
 for oldrow,row in zip(q0['rows'],q['rows']):
  if row.get('currentGroup') not in ('rank7-identity-casting5','rank8-damage6'): continue
  row['previousObservationBefore70']={k:deepcopy(row[k]) for k in ['currentPhase','nextAction']}
  if row['currentGroup']=='rank8-damage6': row.update(currentPhase='corrected-return-pending-independent-semantic-review',nextAction='Independently reconcile all eight corrections and the new scoped Pyre completion against full returned cases and actual sources. No new acceptance yet.')
  else: row.update(currentPhase='bounded-correction-conference-actually-sent',nextAction='Receive completed correction12 and independently verify full acquisition, Action ledger and Erase history corrections. Do not interrupt the active response.')
  ck('Acceptance unchanged '+row['id'],row['semanticAcceptanceClaimed']==oldrow['semanticAcceptanceClaimed']==False)
 q['previousSummaryBefore70']={k:deepcopy(q[k]) for k in ['limitations','pendingDistribution']}
 q.update(id='REMAINING-WORK-QUEUE-57',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousQueue=bind(qpath),pendingDistribution=dict(Counter(r['currentPhase'] for r in q['rows'])),currentRank8CorrectionReturn=received,currentRank7ActualCorrectionDispatch=dispatch)
 q['latestActualReviewEvidence'].extend([bind(pfpath),bind(nativepath)])
 q['limitations']='Current70: Rank8 corrected Return02 preserved with1060 checks; independent correction semantics pending. Rank7 three-finding correction12 actually submitted; native GPT active.50 groups cover307 pending identities;16 remain ungrouped. Elemental-pets2 remains prepared unsent. Applied525/323/249/173 and39 accepted-but-unapplied unchanged. No engine/runtime,cosmology,balance or release acceptance. Implementation remains separately reserved. Verified GitHub backup through65.'
 ck('All full source/history rows retained',len(q['rows'])==len(q0['rows'])==323 and all(all(a[k]==b[k] for k in ['id','completeCurrentSourceAndAccess','currentIndexEntryUnchanged','previousAuthoringMapRowUnchanged']) for a,b in zip(q['rows'],q0['rows'])))
 ck('Unrelated groups exact',all(a==b for a,b in zip(q['groups'],q0['groups']) if a['group'] not in ('rank7-identity-casting5','rank8-damage6')))
 ck('Counts preserved',len(q['groups'])==50 and sum(r['currentGroup'] is not None for r in q['rows'])==307 and sum(r['currentGroup'] is None for r in q['rows'])==16 and q['ordinarySpellCounts']==q0['ordinarySpellCounts'] and q['sourceBindings']==q0['sourceBindings'])
 for b in cp['navigation']: ck('Previous navigation '+b['path'],bind(G/b['path'])==b)
 navpaths=[G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',G/'REVIEW_MAP.html']; nav={p:p.read_bytes() for p in navpaths}
 navbackup.mkdir()
 for p,b in nav.items(): (navbackup/p.name).write_bytes(b)
 qout.write_bytes(enc(q)); base='docs/audit/2026-10-08/full-game/'
 for p,prefix in [(navpaths[0],''),(navpaths[1],'../../../')]:
  raw=nav[p]; pos=raw.index(b'\n')+1
  notice=('\n**Current GPT exchange — 20 October 2026:** [Checkpoint70]('+prefix+base+out.name+') records the full Rank8 corrected return, preserved with1,060 independent checks and awaiting semantic review. The three-finding Rank7 correction packet is actually submitted and GPT is active. Queue57 retains307 grouped/16 ungrouped pending identities; applied525/323/249,173 interfaces and39 accepted-but-unapplied remain unchanged. Implementation remains reserved; GitHub backup is through65.\n').encode()
  p.write_bytes(raw[:pos]+notice+raw[pos:]); ck('Original navigation retained '+p.name,p.read_bytes().replace(notice,b'',1)==raw)
 p=navpaths[2]; raw=nav[p]; pos=raw.index(b'</h1>')+len(b'</h1>')
 notice=('<section class="sequence" aria-label="Current GPT correction exchange"><p><strong>Checkpoint70: Rank8 correction received; Rank7 corrections sent.</strong>1,060 preservation checks passed; independent Rank8 semantics pending. Queue57 preserves307 grouped/16 ungrouped pending identities. No rules applied. <a href="'+base+out.name+'">Current checkpoint</a></p></section>').encode()
 p.write_bytes(raw[:pos]+notice+raw[pos:]); ck('Original map retained',p.read_bytes().replace(notice,b'',1)==raw)
 cp['previousGptObservationBefore70']=deepcopy(cp['activeGptReviewAtLastVerifiedObservation'])
 cp.update(id='ACTIVE-AUTHORING-RANK8-RETURN-RANK7-DISPATCH-70',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousCheckpoint=bind(old),status='Complete Rank8 correction Return02 received and preserved; complete Rank7 correction12 actually submitted. No new acceptance or implementation.',currentWorkQueue=bind(qout),completedRank8Damage6CorrectionReturn02=received,activeGptReviewAtLastVerifiedObservation=dispatch,navigation=[bind(p) for p in navpaths],preservedNavigation=[bind(navbackup/p.name) for p in navpaths],lastUsageObservation={'usedPercent':26,'remainingPercent':74,'stopAtRemainingPercent':20},queueObservationSupersession='Queue57 updates only actual review observations for Rank8 six and Rank7 five; all50 groups and source histories preserved.',nextAction='Complete independent Rank8 correction semantic review while GPT handles Rank7 correction12; continue pending source conferences and16 ungrouped rank9 identities. Preserve separate owner implementation reservation.',laterLocalWork='Checkpoints66–70,Queue57,Rank8 correction return and Rank7 correction dispatch remain local after verified GitHub backup through65.',previousGoalTurnClassification='Progress: received and preserved full Rank8 correction return; sent prepared full Rank7 bounded correction conference.')
 ck('Applied and accepted counts unchanged',cp['authoredCounts']=={'reviewed':525,'pending':323,'standalone':249,'total':848} and cp['acceptedButUnapplied']==39 and not cp['implementationApplied'])
 out.write_bytes(enc(cp)); savedscript.write_bytes(Path(__file__).read_bytes())
 for p,b in originals.items(): ck('Protected unchanged '+p.relative_to(G).as_posix(),p.read_bytes()==b)
 report.write_bytes(enc({'checkpoint':bind(out),'queue':bind(qout),'checks':checks,'checkCount':len(checks),'failures':0,'sourceInformationDeleted':0,'implementationApplied':False,'scope':'Verified full receipt, actual dispatch, immutable source/history and navigation continuity only.'}))
 print(json.dumps({'checkpoint':bind(out),'queue':bind(qout),'report':bind(report),'checks':len(checks),'failures':0}))
if __name__=='__main__': main()
