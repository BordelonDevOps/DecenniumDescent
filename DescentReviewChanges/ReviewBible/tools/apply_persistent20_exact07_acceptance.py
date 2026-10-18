"""Byte-identical persistent20 installation plus separately verified live membership."""
from copy import deepcopy
from datetime import datetime,timezone
import hashlib,json,zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded
from prepare_ac5_current_interfaces_01 import at

def read(p):return json.loads(p.read_bytes())
def exact(raw,b):return len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256']
def canonical_sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def main():
 now=datetime.now(timezone.utc).isoformat();root=A/'persistent-damage20-exact-rebound-07';authority=A/'persistent-damage20-exact07-review/REVIEW.json';auth=read(authority);register=read(root/'REGISTER.json')
 receipt=A/'PERSISTENT_DAMAGE_20_EXACT07_APPLICATION_RECEIPT.json';report=A/'PERSISTENT_DAMAGE_20_EXACT07_APPLICATION_CHECK.json';operations=A/'PERSISTENT_DAMAGE_20_EXACT07_APPLICATION_OPERATIONS.json';keep=A/'source-before-persistent20-exact07-application';status=R/'docs/mechanics/PERSISTENT_DAMAGE_20_REVIEW_STATUS.json'
 copies={n:G/p for n,p in register['applicationPlan']['canonicalByteCopies'].items()};assert not any(p.exists() for p in [receipt,report,operations,keep,status,*copies.values()]);checks=[]
 def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
 nativep=A/'PERSISTENT_DAMAGE_20_EXACT_REBOUND_07_ACTUAL_GPT_FINAL.json';turn=read(nativep)['turns'][0];reply=next(i for i in turn['items'] if i['type']=='agentMessage')
 ck('Actual notebook final',turn['id']=='82f23f2f-dc41-4814-9d0f-ec6c331ee127' and reply['id']=='83efadaa-6cfb-4a89-b9c9-1fc6b354392a' and auth['verdict'] in reply['text'])
 rz=A/'DD_Persistent_Damage_20_Exact_Rebound_07_Review.zip';ck('Actual review archive hash',exact(rz.read_bytes(),{'bytes':47448,'sha256':'25b2b40fab9677f69c8231681a2ced54b69fa34560520e72d3821fd99deda63e'}) and info(rz)['sha256'] in reply['text'])
 with zipfile.ZipFile(rz) as z:
  for n in ['REVIEW.json','VERDICT.md','SOURCE_VERIFICATION.json','EVIDENCE_MANIFEST.json']:ck('Raw review preserved '+n,z.read(n)==(authority.parent/n).read_bytes())
 ck('Bounded exact affirmative verdict',auth['verdict']=='ACCEPT_BYTE_IDENTICAL_FOR_PROVISIONAL_AUTHORED_PERSISTENT_DAMAGE20_VIDEO_GAME_CANDIDATE' and auth['candidateCanRemainByteIdentical'] and not auth['requiredCorrections'] and not auth['remainingBlockingFindings'] and auth['authoredCoherenceVerdict']['blockingFindingCount']==0)
 submitted=A/auth['reviewedInputArchive']['name'];ck('Exact submitted input',exact(submitted.read_bytes(),auth['reviewedInputArchive']));sources=read(root/'SOURCE_HASHES.json')['bindings'];drift=[]
 with zipfile.ZipFile(submitted) as z:
  ck('Eight unique exact current artifacts',len(auth['acceptedArtifactBindings'])==len({b['name'] for b in auth['acceptedArtifactBindings']})==8)
  for b in auth['acceptedArtifactBindings']:ck('Accepted payload '+b['name'],z.read(b['archivePath'])==(root/b['name']).read_bytes() and exact((root/b['name']).read_bytes(),b))
  ck('84 complete frozen sources',len(sources)==84)
  for b in sources:
   ck('Full input source '+b['path'],exact(z.read('sources/'+b['path']),b))
   if not exact((G/b['path']).read_bytes(),b):drift.append({'reviewedFrozenSource':b,'currentLiveBinding':info(G/b['path']),'preservedInArchive':'sources/'+b['path']})
 indexp=R/'data/public/spell_playtests/authored_review_index.json';ck('Only prior membership changed since freeze',[x['reviewedFrozenSource']['path'] for x in drift]==[indexp.relative_to(G).as_posix()])
 ck('Current index is verified damage25 result',read(A/'DAMAGE_CONTROL_25_EXACT10_APPLICATION_OPERATIONS.json')['indexAfter']==info(indexp))
 model=read(root/'SPELLS_MODEL.json');cases=read(root/'CASEBOOK.json');originalp=G/register['candidate']['path'];original=read(originalp);ids=[s['id'] for s in model['spells']]
 ck('Exact Current07 still preserved',info(originalp)==register['candidate']);ck('20 accepted identities/order',ids==auth['acceptedModule']['acceptedSpellIds'] and ids==register['spellIds'] and len(set(ids))==20)
 ck('21 printed placements',sum(len(s['completeSourceAndAccess']['source']['original']['placements']) for s in model['spells'])==21)
 ck('Nine full shared rules exact',model['sharedRules']==original['sharedRules'] and len(model['sharedRules'])==9)
 ck('40 original scenarios exact',len(cases['originalExamplesUnchanged'])==40 and cases['originalExamplesUnchanged']==original['originalExamplesUnchanged'])
 ordered=[]
 for group in cases['categories']:ordered.extend(original[group['sourceArray']])
 ck('57 complete current cases/order retained',cases['cases']==ordered and len(ordered)==57 and [c['id'] for c in ordered]==auth['acceptedModule']['currentCaseIds'])
 catalogp=R/'data/public/spell_playtests/catalog.json';catbinding=info(catalogp);byid={s['id']:s for s in read(catalogp)['spells']}
 for n,(s,o) in enumerate(zip(model['spells'],original['spells'])):
  ck('Whole spell/source/root unchanged '+s['id'],s==o and s['completeSourceAndAccess']==byid[s['id']])
  ar=auth['procedureReview'][n];ck('Actual procedure disposition '+s['id'],ar['spellId']==s['id'] and ar['verdict']=='AGREE_FOR_EXACT_AUTHORED_CANDIDATE' and ar['currentProcedureAndRootMapRead'] and ar['sourceAccessCanonicalObjectSha256']==canonical_sha(s['completeSourceAndAccess']))
 for c,ar in zip(ordered,auth['caseReview']):ck('Exact reviewed case '+c['id'],c['id']==ar['id'] and ar['currentAdjudicationReadInFull'] and canonical_sha(c)==ar['boundCaseCanonicalObjectSha256'])
 ck('Three local repairs concur',len(auth['localRepairDispositions'])==3 and all(x['verdict']=='AGREE' for x in auth['localRepairDispositions']))
 ck('All24 questions resolved',len(auth['conferenceQuestionResolution'])==24 and all(x['currentDisposition']=='RESOLVED_IN_EXACT07_WITH_RETAINED_SCOPED_BOUNDARIES' for x in auth['conferenceQuestionResolution']))
 before_raw=indexp.read_bytes();old=json.loads(before_raw);index=deepcopy(old);oldcounts=deepcopy(index['authoredCounts']);oldstandalone=index['representationCounts']['completeReviewedStandaloneProcedures']
 ck('Actual current membership counts',oldcounts=={'reviewed':505,'pending':343} and oldstandalone==229 and len(index['entries'])==848)
 ck('Catalog hash still current',index['sourceCatalogSha256']==catbinding['sha256'])
 newcounts={'reviewed':oldcounts['reviewed']+len(ids),'pending':oldcounts['pending']-len(ids)};newstandalone=oldstandalone+len(ids)
 public=copies['SPELLS_MODEL.json'];publicbinding=info(public,(root/'SPELLS_MODEL.json').read_bytes());aliases={'SPELLS_MODEL.json':public.relative_to(G).as_posix(),'CASEBOOK.json':copies['CASEBOOK.json'].relative_to(G).as_posix(),'REGISTER.json':(root/'REGISTER.json').relative_to(G).as_posix()}
 rec={'recordedAtUtc':now,'reviewId':auth['id'],'status':'exact-authored-acceptance-applied','developmentDirection':'video-game-only','acceptanceAuthority':info(authority),'acceptanceArchive':info(rz),'reviewedArchive':info(submitted),'actualNativeFinal':info(nativep),'actualReturnReceipt':info(A/'PERSISTENT_DAMAGE_20_EXACT07_RETURN_RECEIPT.json'),'acceptedArtifactBindings':auth['acceptedArtifactBindings'],'acceptedSpellIds':ids,'completeEnvelope':publicbinding,'canonicalCopies':[{'source':info(root/n),'destination':info(p,(root/n).read_bytes()),'byteIdentical':True} for n,p in copies.items()],'caseSourceReferenceAliases':aliases,'sourceFiles':84,'placements':21,'currentCases':57,'preservedHistoricalScenarios':40,'sourceSnapshotDriftSincePreparation':drift,'driftPolicy':'Only live membership changed through independently verified damage25 application. All84 frozen sources remain exact in the accepted archive; other83 still match live. Do not replace505/343 live baseline with480/368 historical snapshot.','authoredCountsBefore':oldcounts,'authoredCountsAfter':newcounts,'standaloneBefore':oldstandalone,'standaloneAfter':newstandalone,'indexUpdateIsSeparatelyVerifiedLocalApplication':True,'normalization':'None; exact payloads retain historical pending labels, with actual exact acceptance and application in separate receipts.','catalogBindingUnchanged':catbinding,'runtimeSelectionEnabled':False,'runtimeImplemented':False,'runtimeTestsExecuted':0,'humanPlaytested':False,'numericalBalanceApproved':False,'cosmologyCanonModified':False,'domainGatesChanged':False,'sourceInformationDeleted':0,'pushed':False}
 receipt_raw=encoded(rec);receiptbinding=info(receipt,receipt_raw);changes=[]
 for n,ident in enumerate(ids):
  e=next(e for e in index['entries'] if e['id']==ident);before=deepcopy(e);ck('Pending exact identity '+ident,e['authoredStatus']=='pending-authored-procedure');e['sourceCatalogWholeCardPointer']=e['wholeCardPointer']
  e.update(authoredStatus='reviewed-authored-operational-playtest',procedureFile='../spell_candidates/persistent_damage_20_reviewed_07.json',procedurePointer=f'/spells/{n}',wholeCardPointer=f'/spells/{n}',wholeCardIdField='id',procedureTextPointer=f'/spells/{n}/procedure',sharedRulesPointer='/sharedRules',manuscript='../../../docs/spells/candidates/PERSISTENT_DAMAGE_20_REVIEWED_07.md',reviewId=auth['id'],runtimeSelectionEnabled=False,completeEnvelopeBinding=publicbinding,authoredAcceptanceReceipt=receiptbinding,historicalCandidateLabelsPreserved=True,caseSourceReferenceAliases=aliases)
  changes.append({'id':ident,'before':before,'after':deepcopy(e)});ck('Current discovery resolves '+ident,at(model,e['wholeCardPointer'])['id']==ident and at(model,e['procedureTextPointer'])==model['spells'][n]['procedure'])
 index['authoredCounts']=newcounts;index['representationCounts']['completeReviewedStandaloneProcedures']=newstandalone;index.setdefault('additionalStandaloneEnvelopes',[]).append({'file':'../spell_candidates/persistent_damage_20_reviewed_07.json','binding':publicbinding,'reviewId':auth['id'],'acceptedIds':ids,'authority':info(authority),'receipt':receiptbinding})
 for before,after in zip(old['entries'],index['entries']):
  if before['id'] not in ids:ck('Unrelated membership unchanged '+before['id'],before==after)
 ck('848 identities/order retained',[e['id'] for e in index['entries']]==[e['id'] for e in old['entries']] and len(index['entries'])==848)
 ck('Actual computed525/323 counts',newcounts=={'reviewed':525,'pending':323} and sum(e['authoredStatus']=='reviewed-authored-operational-playtest' for e in index['entries'])==525 and sum(e['authoredStatus']!='reviewed-authored-operational-playtest' for e in index['entries'])==323 and newstandalone==249)
 cov=R/'data/playtest/game_development_coverage.json';cov_before=info(cov)
 # All semantic and live-index preconditions pass before installing or writing membership.
 keep.mkdir();backup=keep/'authored_review_index.json';backup.write_bytes(before_raw);ck('Original index preserved',backup.read_bytes()==before_raw)
 for n,p in copies.items():p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((root/n).read_bytes());ck('Exact canonical raw copy '+n,p.read_bytes()==(root/n).read_bytes())
 receipt.write_bytes(receipt_raw);assert indexp.read_bytes()==before_raw;indexp.write_bytes(encoded(index));ck('Source catalog untouched',info(catalogp)==catbinding);ck('All75 domain gates untouched',info(cov)==cov_before)
 for e in read(indexp)['entries']:
  if e['id'] in ids:ck('Installed entry/receipt resolves '+e['id'],info(public)==e['completeEnvelopeBinding'] and info(receipt)==e['authoredAcceptanceReceipt'] and at(read(public),e['wholeCardPointer'])['id']==e['id'] and e['runtimeSelectionEnabled'] is False)
 status.write_bytes(encoded({'status':'Reviewed authored video-game candidate; runtime, human gameplay and balance pending','reviewId':auth['id'],'receipt':info(receipt),'model':info(public),'cases':info(copies['CASEBOOK.json']),'playerChapter':info(copies['PLAYER_CHAPTER.md']),'directorChapter':info(copies['DIRECTOR_REVIEW.md']),'acceptedSpellIds':ids,'caseSourceReferenceAliases':aliases,'historicalPendingLabelsPreserved':True,'runtimeSelectionEnabled':False,'sourceInformationDeleted':0}))
 operations.write_bytes(encoded({'recordedAtUtc':now,'authority':info(authority),'receipt':info(receipt),'indexBefore':info(backup),'indexAfter':info(indexp),'membershipChanges':changes,'metadataBefore':{k:v for k,v in old.items() if k!='entries'},'metadataAfter':{k:v for k,v in index.items() if k!='entries'},'copies':rec['canonicalCopies'],'sourceInformationDeleted':0}))
 report.write_bytes(encoded({'recordedAtUtc':now,'scope':'Actual exact final, unchanged artifact installation and separately verified authored membership. No runtime game execution.','receipt':info(receipt),'operations':info(operations),'checks':checks,'checkCount':len(checks),'failureCount':0,'authoredCounts':newcounts,'standaloneProcedures':newstandalone,'sourceCatalogUnchanged':True,'domainGatesUnchanged':True,'runtimeTestsExecuted':0,'humanPlaytested':False,'sourceInformationDeleted':0}));print(json.dumps({'receipt':info(receipt),'applicationCheck':info(report),'checks':len(checks),'counts':newcounts,'standalone':newstandalone,'sourceSnapshotDrifts':len(drift)}))

if __name__=='__main__':main()
