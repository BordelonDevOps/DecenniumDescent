"""Install byte-identical accepted damage25 artifacts; separately index actual receipt."""
from copy import deepcopy
from datetime import datetime,timezone
import hashlib,json,zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded
from prepare_ac5_current_interfaces_01 import at

def read(p):return json.loads(p.read_bytes())
def exact(raw,b):return len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256']

def main():
 now=datetime.now(timezone.utc).isoformat();root=A/'damage-control25-exact-rebound-10';authority=A/'damage-control25-exact10-review/REVIEW.json';auth=read(authority)
 receipt=A/'DAMAGE_CONTROL_25_EXACT10_APPLICATION_RECEIPT.json';report=A/'DAMAGE_CONTROL_25_EXACT10_APPLICATION_CHECK.json';operations=A/'DAMAGE_CONTROL_25_EXACT10_APPLICATION_OPERATIONS.json';keep=A/'source-before-damage25-exact10-application';status=R/'docs/mechanics/DAMAGE_CONTROL_25_REVIEW_STATUS.json'
 copies={name:G/path for name,path in auth['applicationBoundary']['acceptedCanonicalByteCopyPlan'].items()}
 assert not any(p.exists() for p in [receipt,report,operations,keep,status,*copies.values()])
 checks=[]
 def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
 nativep=A/'DAMAGE_CONTROL_25_EXACT_REBOUND_10_ACTUAL_GPT_FINAL.json';turn=read(nativep)['turns'][0];reply=next(x for x in turn['items'] if x['type']=='agentMessage')
 ck('Actual accepted notebook turn',turn['id']=='3e0faf42-f4a2-431f-9456-24c212a66cab' and reply['id']=='81bee90e-0066-41fc-a719-4d47ec46af01' and auth['verdict'] in reply['text'])
 reviewzip=A/'DD_Damage_Control_25_Exact_Rebound_10_Review.zip';ck('Actual downloaded final hash',exact(reviewzip.read_bytes(),{'bytes':42399,'sha256':'17833f27e7b5b2f189045266a460236dc5bdf90466b615eeab5678990e5ccc8e'}) and info(reviewzip)['sha256'] in reply['text'])
 with zipfile.ZipFile(reviewzip) as z:
  for name in ['REVIEW.json','VERDICT.md','SOURCE_VERIFICATION.json','EVIDENCE_MANIFEST.json']:ck('Review preserved '+name,z.read(name)==(authority.parent/name).read_bytes())
 ck('Bounded affirmative final',auth['verdict']=='ACCEPT_BYTE_IDENTICAL_FOR_PROVISIONAL_AUTHORED_DAMAGE_CONTROL25_VIDEO_GAME_CANDIDATE' and auth['candidateCanRemainByteIdentical'] and not auth['candidateReserializedOrModified'] and auth['remainingBlockingFindingCount']==0 and not auth['proposedReplacements'])
 submitted=A/auth['reviewedArchive']['name'];ck('Actual input exact',exact(submitted.read_bytes(),auth['reviewedArchive']))
 sources=read(root/'SOURCE_HASHES.json')['bindings'];drift=[]
 with zipfile.ZipFile(submitted) as z:
  ck('Eight unique accepted artifacts',len(auth['acceptedArtifactBindings'])==len({b['name'] for b in auth['acceptedArtifactBindings']})==8)
  for b in auth['acceptedArtifactBindings']:ck('Accepted raw artifact '+b['name'],z.read(b['archivePath'])==(root/b['name']).read_bytes() and exact((root/b['name']).read_bytes(),b))
  ck('77 complete frozen sources',len(sources)==77)
  for b in sources:
   ck('Submitted full source '+b['path'],exact(z.read('sources/'+b['path']),b))
   if not exact((G/b['path']).read_bytes(),b):drift.append({'reviewedFrozenSource':b,'currentLiveBinding':info(G/b['path']),'preservedInArchive':'sources/'+b['path']})
 model=read(root/'SPELLS_MODEL.json');cases=read(root/'CASEBOOK.json');register=read(root/'REGISTER.json');original=read(G/register['currentCandidate']['path']);ids=[s['id'] for s in model['spells']]
 ck('Exact Current09 unchanged',info(G/register['currentCandidate']['path'])==register['currentCandidate'])
 ck('25 actual accepted identities',ids==auth['acceptedScope']['spellIds'] and len(set(ids))==25)
 ck('26 printed placements',sum(len(s['completeSourceAndAccess']['source']['original']['placements']) for s in model['spells'])==26)
 ck('Shared rules retained',model['sharedRules']==original['sharedRules'])
 ck('36 complete original scenario texts retained',len(cases['historicalOriginalTexts'])==36 and cases['historicalOriginalTexts']==model['originalScenarioTextsUnchanged'])
 ck('70 current scenarios retained in order',[c['id'] for c in cases['cases']]==auth['acceptedScope']['currentCaseIds'] and len(cases['cases'])==70)
 originals=[]
 for group in register['caseCategories']: originals.extend(original[group['sourceArray']])
 ck('70 complete current case objects exact',cases['cases']==originals)
 catalogp=R/'data/public/spell_playtests/catalog.json';catbinding=info(catalogp);catalog=read(catalogp);byid={s['id']:s for s in catalog['spells']}
 for s,o in zip(model['spells'],original['spells']):
  ck('Whole source/access and procedure '+s['id'],s['completeSourceAndAccess']==byid[s['id']] and s['procedure']==o['procedure'] and s['completeSourceAndAccess']==o['completeSourceAndAccess'])
 ck('All 25 source dispositions agree',len(auth['currentProcedureDispositions'])==25 and all(s['exactCurrentProcedureAccepted'] for s in auth['currentProcedureDispositions']))
 ck('All eleven local repairs agree',len(auth['localRepairDispositions'])==11 and all(x['disposition']=='AGREE' for x in auth['localRepairDispositions']))
 indexp=R/'data/public/spell_playtests/authored_review_index.json';before_raw=indexp.read_bytes();old=json.loads(before_raw);index=deepcopy(old)
 ck('480/368 baseline and204 standalone',index['authoredCounts']=={'reviewed':480,'pending':368} and index['representationCounts']['completeReviewedStandaloneProcedures']==204)
 ck('Source catalog hash current',index['sourceCatalogSha256']==catbinding['sha256'])
 public=copies['SPELLS_MODEL.json'];publicbinding=info(public,(root/'SPELLS_MODEL.json').read_bytes());aliases={'SPELLS_MODEL.json':public.relative_to(G).as_posix(),'CASEBOOK.json':copies['CASEBOOK.json'].relative_to(G).as_posix(),'REGISTER.json':(root/'REGISTER.json').relative_to(G).as_posix()}
 rec={'recordedAtUtc':now,'reviewId':auth['id'],'status':'exact-authored-acceptance-applied','developmentDirection':'video-game-only','acceptanceAuthority':info(authority),'acceptanceArchive':info(reviewzip),'reviewedArchive':info(submitted),'actualNativeFinal':info(nativep),'actualReturnReceipt':info(A/'DAMAGE_CONTROL_25_EXACT10_RETURN_RECEIPT.json'),'acceptedArtifactBindings':auth['acceptedArtifactBindings'],'acceptedSpellIds':ids,'completeEnvelope':publicbinding,'canonicalCopies':[{'source':info(root/n),'destination':info(dst,(root/n).read_bytes()),'byteIdentical':True} for n,dst in copies.items()],'caseSourceReferenceAliases':aliases,'sourceFiles':77,'placements':26,'currentCases':70,'preservedHistoricalScenarios':36,'sourceSnapshotDriftSincePreparation':drift,'driftPolicy':'Original supplied source bytes remain in the accepted input ZIP. Current receipt records live discovery independently; no old snapshot is silently treated as current.','authoredCountsBefore':{'reviewed':480,'pending':368},'authoredCountsAfter':{'reviewed':505,'pending':343},'standaloneAfter':229,'indexUpdateIsSeparatelyVerifiedLocalApplication':True,'normalization':'None; exact payloads preserve historical pending labels. This actual final and application receipt establish bounded authored acceptance.','catalogBindingUnchanged':catbinding,'runtimeSelectionEnabled':False,'runtimeImplemented':False,'runtimeTestsExecuted':0,'humanPlaytested':False,'numericalBalanceApproved':False,'cosmologyCanonModified':False,'domainGatesChanged':False,'sourceInformationDeleted':0,'pushed':False}
 receipt_raw=encoded(rec);receiptbinding=info(receipt,receipt_raw);changes=[]
 for n,ident in enumerate(ids):
  e=next(e for e in index['entries'] if e['id']==ident);before=deepcopy(e);ck('Pending membership '+ident,e['authoredStatus']=='pending-authored-procedure')
  e['sourceCatalogWholeCardPointer']=e['wholeCardPointer'];e.update(authoredStatus='reviewed-authored-operational-playtest',procedureFile='../spell_candidates/damage_control_25_reviewed_10.json',procedurePointer=f'/spells/{n}',wholeCardPointer=f'/spells/{n}',wholeCardIdField='id',procedureTextPointer=f'/spells/{n}/procedure',sharedRulesPointer='/sharedRules',manuscript='../../../docs/spells/candidates/DAMAGE_CONTROL_25_REVIEWED_10.md',reviewId=auth['id'],runtimeSelectionEnabled=False,completeEnvelopeBinding=publicbinding,authoredAcceptanceReceipt=receiptbinding,historicalCandidateLabelsPreserved=True,caseSourceReferenceAliases=aliases)
  changes.append({'id':ident,'before':before,'after':deepcopy(e)});ck('New discovery resolves '+ident,at(model,e['wholeCardPointer'])['id']==ident and at(model,e['procedureTextPointer'])==model['spells'][n]['procedure'])
 index['authoredCounts']={'reviewed':505,'pending':343};index['representationCounts']['completeReviewedStandaloneProcedures']=229
 index.setdefault('additionalStandaloneEnvelopes',[]).append({'file':'../spell_candidates/damage_control_25_reviewed_10.json','binding':publicbinding,'reviewId':auth['id'],'acceptedIds':ids,'authority':info(authority),'receipt':receiptbinding})
 for before,after in zip(old['entries'],index['entries']):
  if before['id'] not in ids:ck('Unrelated index entry unchanged '+before['id'],before==after)
 ck('848 identities/order unchanged',[e['id'] for e in old['entries']]==[e['id'] for e in index['entries']] and len(index['entries'])==848)
 ck('Actual membership505 and343',sum(e['authoredStatus']=='reviewed-authored-operational-playtest' for e in index['entries'])==505 and sum(e['authoredStatus']!='reviewed-authored-operational-playtest' for e in index['entries'])==343)
 ck('No runtime switch introduced',not any(index['entries'][n].get('runtimeSelectionEnabled') for n in range(len(index['entries'])) if index['entries'][n]['id'] in ids))
 coveragep=R/'data/playtest/game_development_coverage.json';coverage_before=info(coveragep)
 # Validate all preconditions before changing live membership. Preserve its complete original.
 keep.mkdir();backup=keep/'authored_review_index.json';backup.write_bytes(before_raw);ck('Original index preserved byte-identically',backup.read_bytes()==before_raw)
 for name,dst in copies.items():dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes((root/name).read_bytes());ck('Installed byte-identical '+name,dst.read_bytes()==(root/name).read_bytes())
 receipt.write_bytes(receipt_raw);assert indexp.read_bytes()==before_raw;indexp.write_bytes(encoded(index))
 ck('Source catalog untouched',info(catalogp)==catbinding);ck('All domain gates untouched',info(coveragep)==coverage_before)
 for e in read(indexp)['entries']:
  if e['id'] in ids:ck('Installed discovery/receipt '+e['id'],info(public)==e['completeEnvelopeBinding'] and info(receipt)==e['authoredAcceptanceReceipt'] and at(read(public),e['wholeCardPointer'])['id']==e['id'])
 status.write_bytes(encoded({'status':'Reviewed authored video-game candidate; runtime, human playtesting and balance pending','reviewId':auth['id'],'receipt':info(receipt),'model':info(public),'cases':info(copies['CASEBOOK.json']),'playerChapter':info(copies['PLAYER_CHAPTER.md']),'directorChapter':info(copies['DIRECTOR_REVIEW.md']),'acceptedSpellIds':ids,'caseSourceReferenceAliases':aliases,'historicalPendingLabelsPreserved':True,'runtimeSelectionEnabled':False,'sourceInformationDeleted':0}))
 operations.write_bytes(encoded({'recordedAtUtc':now,'authority':info(authority),'receipt':info(receipt),'indexBefore':info(backup),'indexAfter':info(indexp),'membershipChanges':changes,'metadataBefore':{k:v for k,v in old.items() if k!='entries'},'metadataAfter':{k:v for k,v in index.items() if k!='entries'},'copies':rec['canonicalCopies'],'sourceInformationDeleted':0}))
 report.write_bytes(encoded({'recordedAtUtc':now,'scope':'Actual final verification, byte-identical installation and separate authored membership integration; no engine execution.','receipt':info(receipt),'operations':info(operations),'checks':checks,'checkCount':len(checks),'failureCount':0,'authoredCounts':index['authoredCounts'],'standaloneProcedures':229,'sourceCatalogUnchanged':True,'domainGatesUnchanged':True,'runtimeTestsExecuted':0,'humanPlaytested':False,'sourceInformationDeleted':0}));print(json.dumps({'receipt':info(receipt),'applicationCheck':info(report),'checks':len(checks),'counts':index['authoredCounts'],'sourceSnapshotDrifts':len(drift)}))

if __name__=='__main__':main()
