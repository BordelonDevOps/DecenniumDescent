"""Fresh exact one-ID authored acceptance and reversible canonical selection. No supplied code executes."""
from pathlib import Path
import json,hashlib,datetime,copy,shutil
G=Path(r'C:\Github\DecenniumDescent');D=Path(__file__).parent;R=G/'DescentReviewChanges/ReviewBible';S=D/'lifematter5_return02_received';E=R/'data/public/spell_candidates/disintegrate_reviewed_129'
rd=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
enc=lambda x:(json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode('utf-8')
sha=lambda b:hashlib.sha256(b).hexdigest()
def bind(p):return {'path':p.relative_to(G).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
def fresh(p,b):
 assert not p.exists(),str(p)
 p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
def ptr(x,p):
 for k in p.strip('/').split('/'):x=x[int(k)] if isinstance(x,list) else x[k.replace('~1','/').replace('~0','~')]
 return x
ip=R/'data/public/spell_playtests/authored_review_index.json';raw=ip.read_bytes();old=rd(ip)
assert sha(raw)=='ecec00171e60785d28d418cf3ec940d14261fbe9edcf68566e05406e2236b02d' and old['authoredCounts']=={'reviewed':627,'pending':221}
reports=['LIFEMATTER5_RETURN02_INDEPENDENT_DATA_AUDIT_129.json','LIFEMATTER5_RETURN02_ACTOR_CARD_AUDIT_129.json','LIFEMATTER5_RETURN02_BOOK_AUDIT_129.json','LIFEMATTER5_RETURN02_CAST_SOURCE_AUDIT_129.json','DISINTEGRATE_RETURN02_FINAL_INDEPENDENT_REVIEW_129.json']
for name in reports:assert rd(D/name)['errors']==[],name
final=rd(D/reports[-1]);assert final['passed'] and final['semanticFindings']==[] and final['appliedFourUnchanged']
manifest=rd(S/'MANIFEST.json');files=sorted(p for p in S.rglob('*') if p.is_file());assert len(files)==148
for b in manifest['payload']+[manifest['bindingFile']]:
 actual=bind(S/b['path']);assert actual['bytes']==b['bytes'] and actual['sha256']==b['sha256']
model=rd(S/'MODEL.json');procs=model['completeProcedures'];procedure=procs[3];assert procedure['id']=='disintegrate'
assert procs==rd(S/'PROCEDURES.json')['spells']==rd(S/'PROPOSED_STANDALONE_ENVELOPE.json')['spells']
scope='Only Disintegrate and the original shared requirements applicable to it, including its original LM130-LIFE dust clause as completed by LM130-DISINTEGRATE-R02-SCOPE, are newly accepted. Earlier Core death/replacement priority and independent temporal-provider contracts retain their actual scope; no global damage/temporal rule is introduced. Four previously applied LifeMatter procedure objects/index selections remain unchanged. All explicit content/fixture/runtime/human/balance/cosmology/release holds remain.'
ap=D/'DISINTEGRATE_EXACT_ACCEPTANCE_129.json'
accept={'id':'DISINTEGRATE-EXACT-AUTHORED-ACCEPTANCE-129','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'EXACT_DISINTEGRATE_AUTHORED_PROCEDURE_ACCEPTED_WITH_RETAINED_HOLDS','approvedForCanonicalApplication':True,'acceptedIdentities':['disintegrate'],'contextOnlyAlreadyAppliedIds':['awaken','bone-cage','contagion','telekinesis'],'authority':'Director selected complete corrected Return02; independent complete-source, actual cast, reversible-data and semantic review resolved all three original findings under owner instruction to apply each accepted batch.','scope':scope,'semanticFindings':[],'resolvedFindings':final['resolvedFindings'],'acceptedProcedures':[{'id':'disintegrate','modelPointer':'/completeProcedures/3','procedureTextSha256':sha(procedure['procedure'].encode('utf-8')),'nativeAccessRows':len(procedure['completeSourceAndAccess']['classAccess'])}],'acceptedCaseIds':final['selectedCases'],'counts':{'identities':1,'originalMains':2,'branches':9,'events':266,'actualCasts':44,'allOriginalQuestionsPreserved':20},'verification':{'wholeArchiveDataChecks':5965,'wholeArchiveClassCardChecks':712,'wholeArchiveWizardBookChecks':839,'wholeArchiveCastSourceChecks':1222,'finalIndependentChecks':293,'allChecksPassed':True,'original121MemberHistoryExact':True,'allSelectedSubstantiveCaseEventsRead':True,'offTurnPaidNormalActions':0,'appliedFourExact':True},'archive':bind(D/'DD_LifeMatter5_Director_Return02_130.zip'),'acceptedFileBindings':[bind(p) for p in files],'canonicalBaseline':bind(ip),'evidenceReports':[bind(D/n) for n in reports],'retainedHolds':rd(S/'HOLD_REGISTER.json'),'canonicalApplied':False,'localRuleOrCaseChanges':0,'runtimeExecuted':False,'humanPlaytests':False,'balanceApproval':False,'cosmologyApproval':False,'releaseApproval':False}
fresh(ap,enc(accept))
assert rd(ap)['approvedForCanonicalApplication'] and ip.read_bytes()==raw
fresh(D/'authored_review_index.before_disintegrate_129.json',raw)
assert not E.exists();shutil.copytree(S,E)
for p in files:assert p.read_bytes()==(E/p.relative_to(S)).read_bytes()
chapter=R/'docs/spells/candidates/DISINTEGRATE_REVIEWED_129.md'
text='# Disintegrate - applied authored review129\n\nExact corrected Return02 is independently accepted by DISINTEGRATE_EXACT_ACCEPTANCE_129.json and selected by DISINTEGRATE_APPLICATION_129.json. The entire148-file source package is preserved byte for byte in data/public/spell_candidates/disintegrate_reviewed_129.\n\n'+scope+'\n\nHistorical proposed/pending labels and count snapshots in preserved sources remain evidence; the exact acceptance/application receipts control this one identity.\n\n## Disintegrate\n\n'+procedure['procedure']+'\n\n## Shared requirements within this identity scope\n\n'
for rule in model['sharedRules']:text+='### '+rule['id']+'\n\n'+rule['rule']+'\n\n'
fresh(chapter,text.encode('utf-8'))
rp=D/'DISINTEGRATE_APPLICATION_129.json'
receipt={'id':'DISINTEGRATE-APPLICATION-129','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'APPLIED_DISINTEGRATE_AUTHORED_IDENTITY_WITH_RETAINED_HOLDS','ownerInstruction':'Continue pending ordinary spells with GPT as director in Calibration review part6; apply each batch upon exact acceptance; complete all232 pending.','acceptedIds':['disintegrate'],'authority':bind(ap),'acceptedModelSource':bind(S/'MODEL.json'),'canonicalModel':bind(E/'MODEL.json'),'exactEvidenceRoot':E.relative_to(G).as_posix(),'evidenceManifest':bind(E/'MANIFEST.json'),'casebook':bind(E/'CASEBOOK.json'),'holds':bind(E/'HOLD_REGISTER.json'),'chapter':bind(chapter),'runtimeSelectionEnabled':False,'runtimeImplemented':False,'historicalPendingLabelsPreserved':True,'localRuleOrCaseChanges':0,'scope':scope}
fresh(rp,enc(receipt));idx=copy.deepcopy(old);ops=[]
for i,e in enumerate(idx['entries']):
 if e['id']!='disintegrate':continue
 assert e['authoredStatus']=='pending-authored-procedure';before=copy.deepcopy(e);p='/completeProcedures/3'
 e.update(authoredStatus='reviewed-authored-operational-playtest',procedureFile='../spell_candidates/disintegrate_reviewed_129/MODEL.json',sourceCatalogWholeCardPointer=before['wholeCardPointer'],wholeCardPointer=p,wholeCardIdField='id',procedurePointer=p,procedureTextPointer=p+'/procedure',sharedRulesPointer='/sharedRules',manuscript='../../../docs/spells/candidates/'+chapter.name,reviewId=receipt['id'],runtimeSelectionEnabled=False,completeEnvelopeBinding=bind(E/'MODEL.json'),authoredAcceptanceReceipt=bind(ap),authoredApplicationReceipt=bind(rp),historicalCandidateLabelsPreserved=True,casebookBinding=bind(E/'CASEBOOK.json'),retainedHoldsBinding=bind(E/'HOLD_REGISTER.json'),completeEvidenceRoot=E.relative_to(G).as_posix(),acceptedSharedRuleScope=scope)
 ops.append({'pointer':'/entries/'+str(i),'before':before,'after':copy.deepcopy(e)})
assert len(ops)==1
idx['authoredCounts']={'reviewed':628,'pending':220};idx['representationCounts']['completeReviewedStandaloneProcedures']=352
idx['additionalStandaloneEnvelopes'].append({'file':'../spell_candidates/disintegrate_reviewed_129/MODEL.json','binding':bind(E/'MODEL.json'),'reviewId':receipt['id'],'acceptedIds':['disintegrate'],'authority':bind(ap),'receipt':bind(rp)})
for k in ['authoredCounts','representationCounts','additionalStandaloneEnvelopes']:ops.append({'pointer':'/'+k,'before':old[k],'after':copy.deepcopy(idx[k])})
assert sum(e['authoredStatus']=='reviewed-authored-operational-playtest' for e in idx['entries'])==628
unchanged=sum(x['id']!='disintegrate' and x==y for x,y in zip(old['entries'],idx['entries']));assert unchanged==847
reverse=copy.deepcopy(idx)
for o in reversed(ops):
 ks=o['pointer'].strip('/').split('/');v=reverse
 for k in ks[:-1]:v=v[int(k)] if isinstance(v,list) else v[k]
 k=int(ks[-1]) if isinstance(v,list) else ks[-1];assert v[k]==o['after'];v[k]=copy.deepcopy(o['before'])
assert reverse==old
e=next(e for e in idx['entries'] if e['id']=='disintegrate');m=rd((ip.parent/e['procedureFile']).resolve())
assert ptr(m,e['wholeCardPointer'])['id']=='disintegrate' and ptr(m,e['procedureTextPointer'])==procedure['procedure'] and len(ptr(m,e['sharedRulesPointer']))==7
out=enc(idx);fresh(D/'DISINTEGRATE_INDEX_OPERATIONS_129.json',enc({'id':'DISINTEGRATE-INDEX-OPERATIONS-129','before':{'bytes':len(raw),'sha256':sha(raw),'backup':'authored_review_index.before_disintegrate_129.json'},'after':{'bytes':len(out),'sha256':sha(out)},'operations':ops,'reverseSemanticExact':True,'reverseByteExactBackup':True}))
assert ip.read_bytes()==raw;ip.write_bytes(out);assert rd(ip)==idx
result={'id':'DISINTEGRATE-APPLICATION-VALIDATION-129','passed':True,'acceptedIdentitiesApplied':1,'unrelatedIndexEntriesUnchanged':847,'priorLifeMatter4EntriesUnchanged':True,'completeEvidenceFilesPreserved':len(files),'exactEvidencePreserved':True,'forwardReverseIndexOperations':len(ops),'counts':idx['authoredCounts'],'representationCounts':idx['representationCounts'],'index':bind(ip),'applicationReceipt':bind(rp),'acceptanceReceipt':bind(ap),'runtimeSelectionEnabled':False}
fresh(D/'DISINTEGRATE_APPLICATION_VALIDATION_129.json',enc(result));print(json.dumps(result,indent=2))
