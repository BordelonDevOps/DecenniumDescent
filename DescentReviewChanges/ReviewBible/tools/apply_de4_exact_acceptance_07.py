"""Apply real exact DE4 acceptance; preserve every replaced file and staged index."""
from copy import deepcopy
from datetime import datetime,timezone
import json,zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded
from prepare_ac5_current_interfaces_01 import at
from prepare_de4_fate_guard_amendment_01 import parent

def read(p):return json.loads(p.read_bytes())
def same(p,b):return all(info(p)[k]==b[k] for k in ['bytes','sha256'])

def main():
 now=datetime.now(timezone.utc).isoformat();candidate=A/'de4-exact-rebound-07';authority=A/'de4-exact-acceptance-07/REVIEW.json';archive=A/'DD_DE4_Exact_Rebound_07_Review.zip';submitted=A/'DD_DE4_Exact_Rebound_07.zip';native=A/'DE4_EXACT_ACCEPTANCE_07_ACTUAL_NATIVE.json'
 receipt=A/'DE4_EXACT_ACCEPTANCE_07_RECEIPT.json';report=A/'DE4_EXACT_ACCEPTANCE_07_APPLICATION_CHECK.json';operations=A/'DE4_EXACT_ACCEPTANCE_07_OPERATIONS.json';keep=A/'source-before-de4-exact-acceptance-07';status=R/'docs/mechanics/DIVINATION_ENCHANTMENT_RANK4_REVIEW_STATUS.json'
 public=R/'data/public/spell_candidates/divination_enchantment_rank4_reviewed_07.json';cases=R/'data/playtest/spell_candidates/divination_enchantment_rank4_cases_07.json';player=R/'docs/spells/candidates/DIVINATION_ENCHANTMENT_RANK4_REVIEWED_07.md';director=R/'docs/director-only/spells/DIVINATION_ENCHANTMENT_RANK4_REVIEWED_07.md'
 assert not any(p.exists() for p in [receipt,report,operations,keep,status,public,cases,player,director])
 checks=[]
 def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
 auth=read(authority);plan=read(candidate/'INTEGRATION_PLAN.json');sources=read(candidate/'SOURCE_HASHES.json')['bindings'];model=read(candidate/'SPELLS_MODEL.json');cb=read(candidate/'CASEBOOK.json');original=read(G/plan['currentCandidate']['path'])
 ck('Exact downloaded review',same(archive,{'bytes':24015,'sha256':'261b5138a639404ea5bdb07b1525f9556eac17dfd3611c6ebf4f8ccead701f0e'}))
 with zipfile.ZipFile(archive) as z:
  ck('Safe review members',sorted(z.namelist())==['REVIEW.json','VERDICT.md'])
  for n in z.namelist():ck('Exact recovered review '+n,z.read(n)==(authority.parent/n).read_bytes())
 turn=read(native)['turns'][0];reply=next(x for x in turn['items'] if x['type']=='agentMessage')
 ck('Actual notebook acceptance',turn['id']=='e4660f30-67f8-4c14-a92f-7cd2a49d6474' and reply['id']=='08263e22-ae30-4a00-83a9-458866080ae5' and auth['verdict'] in reply['text'] and info(archive)['sha256'] in reply['text'])
 ck('Affirmative bounded verdict',auth['verdict']=='ACCEPT_BYTE_IDENTICAL_FOR_PROVISIONAL_AUTHORED_DE4_VIDEO_GAME_CANDIDATE' and auth['blockingFindingsRemaining']==0 and auth['candidateFilesMayRemainByteIdentical'] and not auth['candidateFilesReserializedOrChanged'])
 ck('Submitted archive exact',same(submitted,auth['reviewedArchive']))
 expected={'INTEGRATION_PLAN.json','SPELLS_MODEL.json','CASEBOOK.json','PLAYER_CHAPTER.md','DIRECTOR_REVIEW.md','SOURCE_HASHES.json','REGISTER.json','EVIDENCE_MANIFEST.json'}
 ck('18 exact unique accepted files',len(auth['acceptedArtifactBindings'])==18 and len({b['path'] for b in auth['acceptedArtifactBindings']})==18 and {b['name'] for b in auth['acceptedArtifactBindings'] if b['role']=='root candidate'}==expected)
 with zipfile.ZipFile(submitted) as z:
  for b in auth['acceptedArtifactBindings']:
   p=candidate/b['path'].removeprefix('current/');ck('Accepted exact bytes '+b['path'],same(p,b) and z.read(b['path'])==p.read_bytes())
  ck('95 frozen sources',len(sources)==95)
  for b in sources:ck('Frozen source '+b['path'],info(G/b['path'])==b and z.read('sources/'+b['path'])==(G/b['path']).read_bytes())
 for b in read(candidate/'EVIDENCE_MANIFEST.json')['files']:ck('Manifest exact '+b['name'],same(candidate/b['name'],b))
 ck('Four agreed dispositions',len(auth['dispositions'])==4 and all(x['disposition']=='AGREE' for x in auth['dispositions']))
 ck('Actual application remains separate',not auth['applicationBoundary']['liveApplicationPerformedByThisReview'])
 before_raw={};staged_raw={};opcount=0
 for ch,pre in zip(plan['changes'],auth['applicationBoundary']['beforePreconditions']):
  target=G/ch['target'];before_raw[ch['target']]=target.read_bytes();staged_raw[ch['target']]=(candidate/ch['proposedFile']).read_bytes()
  ck('Live target before exact '+ch['target'],info(target)==ch['before']==pre['expectedBefore'] and before_raw[ch['target']]==(candidate/ch['preservedBefore']).read_bytes())
  ck('Exact accepted target after '+ch['target'],info(target,staged_raw[ch['target']])==ch['after']==pre['acceptedAfter'])
  if target.suffix=='.json':
   obj=json.loads(before_raw[ch['target']])
   for op in ch['operations']:
    par,key=parent(obj,op['pointer'])
    if op['operation']=='replace':ck('Operation before '+ch['target']+op['pointer'],par[key]==op['before'])
    else:ck('New field absent '+ch['target']+op['pointer'],op['operation']=='add' and key not in par)
    par[key]=deepcopy(op['after']);opcount+=1
   ck('Replayed whole JSON '+ch['target'],obj==json.loads(staged_raw[ch['target']]))
 ck('707 exact JSON operations',opcount==707 and len(plan['changes'])==10)
 ids=[s['id'] for s in model['spells']];ck('15 accepted identities',ids==auth['acceptedScope']['spellIds'] and len(set(ids))==15)
 ck('37 exact cases',cb['cases']==model['currentExamples']==original['currentExamples'] and [c['id'] for c in cb['cases']]==auth['acceptedScope']['caseIds'])
 ck('30 original texts preserved',cb['historicalOriginalTexts']==original['originalExamplesUnchanged'] and len(cb['historicalOriginalTexts'])==30)
 ck('Procedures/shared rules unchanged',model['sharedRules']==original['sharedRules'] and all(s['procedure']==o['procedure'] and s['completeSourceAndAccess']==o['completeSourceAndAccess'] for s,o in zip(model['spells'],original['spells'])))
 catpath=R/'data/public/spell_playtests/catalog.json';catalog=json.loads(staged_raw[catpath.relative_to(G).as_posix()]);byid={s['id']:s for s in catalog['spells']}
 for s in model['spells']:ck('Full source/access retained '+s['id'],s['completeSourceAndAccess']==byid[s['id']])
 ck('17 printed placements',sum(len(s['completeSourceAndAccess']['source']['original']['placements']) for s in model['spells'])==17)
 copies=[(public,candidate/'SPELLS_MODEL.json'),(cases,candidate/'CASEBOOK.json'),(player,candidate/'PLAYER_CHAPTER.md'),(director,candidate/'DIRECTOR_REVIEW.md')]
 public_binding=info(public,(candidate/'SPELLS_MODEL.json').read_bytes());aliases={'SPELLS_MODEL.json':public.relative_to(G).as_posix(),'CASEBOOK.json':cases.relative_to(G).as_posix(),'REGISTER.json':(candidate/'REGISTER.json').relative_to(G).as_posix()}
 rec={'reviewId':auth['id'],'recordedAtUtc':now,'status':'exact-authored-acceptance-applied','developmentDirection':'video-game-only','acceptanceAuthority':info(authority),'acceptanceArchive':info(archive),'reviewedArchive':info(submitted),'actualGptReply':info(native),'acceptedArtifactBindings':auth['acceptedArtifactBindings'],'acceptedSpellIds':ids,'sourceFiles':95,'placements':17,'authoredCases':37,'preservedHistoricalScenarioTexts':30,'canonicalCopies':[{'source':info(src),'destination':info(dst,src.read_bytes()),'byteIdentical':True} for dst,src in copies],'completeEnvelope':public_binding,'exactStagedIntegrationCopies':[{'target':c['target'],'before':c['before'],'acceptedAfter':c['after']} for c in plan['changes']],'indexMembershipUpdateIsSeparateFromAcceptedStagedBytes':True,'normalization':'None in sealed accepted payloads. Historical pending labels remain preparation history; this actual receipt establishes authored acceptance. The live index receives the separate expressly deferred membership update.','caseSourceReferenceAliases':aliases,'authoredCountsBefore':{'reviewed':465,'pending':383},'authoredCountsAfter':{'reviewed':480,'pending':368},'sourceAndAccessUnchanged':True,'sealedAC6Changed':False,'runtimeSelectionEnabled':False,'runtimeImplemented':False,'runtimeTestsExecuted':0,'humanBalanceApproved':False,'wholeGameFlowConfirmed':False,'sourceInformationDeleted':0,'pushed':False}
 receipt_raw=encoded(rec);receipt_binding=info(receipt,receipt_raw)
 indexp=R/'data/public/spell_playtests/authored_review_index.json';indexrel=indexp.relative_to(G).as_posix();staged_index=json.loads(staged_raw[indexrel]);index=deepcopy(staged_index)
 ck('465/383 baseline',index['authoredCounts']=={'reviewed':465,'pending':383} and index['representationCounts']['completeReviewedStandaloneProcedures']==189)
 ck('Current staged catalog binding',index['sourceCatalogSha256']==info(catpath,staged_raw[catpath.relative_to(G).as_posix()])['sha256'])
 for n,ident in enumerate(ids):
  e=next(e for e in index['entries'] if e['id']==ident);ck('Pending prior membership '+ident,e['authoredStatus']=='pending-authored-procedure');e['sourceCatalogWholeCardPointer']=e['wholeCardPointer']
  e.update(authoredStatus='reviewed-authored-operational-playtest',procedureFile='../spell_candidates/divination_enchantment_rank4_reviewed_07.json',procedurePointer=f'/spells/{n}',wholeCardPointer=f'/spells/{n}',wholeCardIdField='id',procedureTextPointer=f'/spells/{n}/procedure',sharedRulesPointer='/sharedRules',manuscript='../../../docs/spells/candidates/DIVINATION_ENCHANTMENT_RANK4_REVIEWED_07.md',reviewId=auth['id'],runtimeSelectionEnabled=False,completeEnvelopeBinding=public_binding,authoredAcceptanceReceipt=receipt_binding,historicalCandidateLabelsPreserved=True,caseSourceReferenceAliases=aliases)
  ck('Discovery resolves '+ident,at(model,e['wholeCardPointer'])['id']==ident and at(model,e['procedureTextPointer'])==model['spells'][n]['procedure'])
 index['authoredCounts']={'reviewed':480,'pending':368};index['representationCounts']['completeReviewedStandaloneProcedures']=204
 index.setdefault('additionalStandaloneEnvelopes',[]).append({'file':'../spell_candidates/divination_enchantment_rank4_reviewed_07.json','binding':public_binding,'reviewId':auth['id'],'acceptedIds':ids,'authority':info(authority),'receipt':receipt_binding})
 for old,new in zip(staged_index['entries'],index['entries']):
  if old['id'] not in ids:ck('Unrelated membership unchanged '+old['id'],old==new)
 ck('848 original identities and order',len(index['entries'])==848 and [e['id'] for e in index['entries']]==[e['id'] for e in staged_index['entries']])
 ck('Actual membership counts',sum(e['authoredStatus']=='reviewed-authored-operational-playtest' for e in index['entries'])==480 and sum(e['authoredStatus']=='pending-authored-procedure' for e in index['entries'])==367 and sum(e['authoredStatus']=='receipt-only-post-push-cosmology' for e in index['entries'])==1)
 # All fallible source/precondition checks precede mutation. Preserve complete live originals first.
 preserved=[]
 for rel,raw in before_raw.items():
  p=keep/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw);ck('Original backup exact '+rel,p.read_bytes()==raw);preserved.append({'original':info(G/rel,raw),'preservedCopy':info(p)})
 staged_index_keep=keep/'accepted-staged-index-before-membership.json';staged_index_keep.write_bytes(staged_raw[indexrel])
 (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded({'files':preserved,'acceptedStagedIndex':info(staged_index_keep),'purpose':'Preserve both pre-integration originals and exact accepted binding-only index before separate membership update.'}))
 for ch in plan['changes']:
  target=G/ch['target'];assert target.read_bytes()==before_raw[ch['target']];target.write_bytes(staged_raw[ch['target']]);ck('Exact target installed '+ch['target'],info(target)==ch['after'])
 for dst,src in copies:dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(src.read_bytes());ck('Byte-identical canonical copy '+dst.name,dst.read_bytes()==src.read_bytes())
 receipt.write_bytes(receipt_raw);assert indexp.read_bytes()==staged_raw[indexrel];indexp.write_bytes(encoded(index))
 ck('Registered receipt matches',all(e.get('authoredAcceptanceReceipt')==info(receipt) for e in index['entries'] if e['id'] in ids))
 for b in sources:
  p=keep/b['path'] if b['path'] in before_raw else G/b['path'];ck('Reviewed source retained after integration '+b['path'],same(p,b))
 status.write_bytes(encoded({'reviewId':auth['id'],'status':'Reviewed authored video-game candidate; runtime, gameplay and balance pending','receipt':info(receipt),'completeExactModel':info(public),'playerChapter':info(player),'directorChapter':info(director),'authoredCases':info(cases),'caseSourceReferenceAliases':aliases,'acceptedSpellIds':ids,'caseCount':37,'historicalPayloadLabelsPreserved':True,'sourceInformationDeleted':0,'runtimeSelectionEnabled':False}))
 operations.write_bytes(encoded({'recordedAtUtc':now,'authority':info(authority),'receipt':info(receipt),'preservationManifest':info(keep/'PRESERVATION_MANIFEST.json'),'exactTargetChanges':rec['exactStagedIntegrationCopies'],'separateMembershipUpdate':{'before':info(staged_index_keep),'after':info(indexp),'identities':ids},'canonicalCopies':[info(p) for p,_ in copies],'sourceInformationDeleted':0}))
 report.write_bytes(encoded({'recordedAtUtc':now,'scope':'Actual exact acceptance,707 operation replay,source/scenario preservation and authored application; no engine execution','receipt':info(receipt),'operations':info(operations),'checks':checks,'checkCount':len(checks),'failureCount':0,'authoredCounts':index['authoredCounts'],'runtimeTestsExecuted':0,'humanPlaytested':False,'sourceInformationDeleted':0}))
 print(json.dumps({'receipt':info(receipt),'applicationCheck':info(report),'checks':len(checks),'failures':0,'authoredCounts':index['authoredCounts']}))

if __name__=='__main__':main()
