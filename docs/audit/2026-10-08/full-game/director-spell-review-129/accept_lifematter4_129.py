"""Fresh exact acceptance of four independently reviewed identities; excludes Disintegrate."""
from pathlib import Path
import json,hashlib,datetime
G=Path(r'C:\Github\DecenniumDescent');D=Path(__file__).parent;E=D/'lifematter5_return01_received';R=G/'DescentReviewChanges/ReviewBible'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def bind(p):return {'path':p.relative_to(G).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
ids=['awaken','bone-cage','contagion','telekinesis'];out=D/'LIFEMATTER4_EXACT_ACCEPTANCE_129.json';assert not out.exists()
index=R/'data/public/spell_playtests/authored_review_index.json';assert bind(index)['sha256']=='6fb979c4a59fcf4cf1f4a8fb93390ee195c914e1a0755b3cfee747a79df34b91'
data=read(D/'LIFEMATTER5_RETURN01_INDEPENDENT_DATA_AUDIT_V2_129.json');assert not data['errors']
for f in ['LIFEMATTER5_ACTOR_CARD_AUDIT_129.json','LIFEMATTER5_BOOK_AUDIT_129.json']:
 audit=read(D/f);assert not audit.get('errors'),(f,audit)
castAudit=read(D/'LIFEMATTER5_RETURN01_CAST_SOURCE_AUDIT_129.json');assert castAudit['errors']==['EV6-06-A/actual-Null-positive-zero/already-Dying:8:Prone-Unconscious-cancellation']
m=read(E/'MANIFEST.json');bindings=m['payload']+[m['bindingFile']]
for b in bindings:
 p=E/b['path'];actual=bind(p);assert actual['bytes']==b['bytes'] and actual['sha256']==b['sha256']
procedures=read(E/'PROCEDURES.json')['spells'];model=read(E/'MODEL.json');env=read(E/'PROPOSED_STANDALONE_ENVELOPE.json');assert procedures==model['completeProcedures']==env['spells']
selected=[p for p in procedures if p['id'] in ids];assert [p['id'] for p in selected]==ids
q=read(E/'history/ORIGINAL_CANDIDATE.json')['questions']+read(E/'history/ORIGINAL_FOLLOWUPS.json')['reviewRequirements'];answers=read(E/'QUESTION_DISPOSITIONS.json')['dispositions'];assert len(q)==len(answers)==20
assert {r['id'] for r in q}=={r['id'] for r in answers}
assert all(next(x for x in q if x['id']==r['id'])==r['originalQuestionCompleteUnchanged'] for r in answers)
def walk(c):
 yield c
 for b in c['branches']:yield from walk(b)
main=[c for c in read(E/'CASEBOOK.json')['mainCases'] if c['spellId'] in ids];cases=[c for c in main for c in walk(c)]
assert len(main)==8 and len(cases)==26 and sum(len(c['timeline']) for c in cases)==253
review=read(D/'LIFEMATTER5_RETURN01_SEMANTIC_REVIEW_129.json');assert all(f['id'] in ['LM129-F01','LM129-F02','LM129-F03'] for f in review['findings'])
receipt={'id':'LIFEMATTER4-EXACT-AUTHORED-ACCEPTANCE-129','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'EXACT_FOUR_AUTHORED_PROCEDURES_ACCEPTED_WITH_RETAINED_HOLDS','approvedForCanonicalApplication':True,'acceptedIdentities':ids,'excludedIdentity':'disintegrate','semanticFindings':[],'unacceptedDisintegrateFindings':review['findings'],'authority':'Director selected full Return01 procedures followed by independent data, complete source/card/book, semantic and actual cast review under owner instruction to apply each accepted batch.','scope':'Only the four named procedure identities and shared requirements applicable to them are accepted. Disintegrate procedure, cases and Disintegrate-specific dust clauses remain unaccepted evidence, including the local dust clause within LM130-LIFE. This receipt adopts no new global damage or temporal rule. Other five-spell/pending labels in preserved return are historical context, not authority to select Disintegrate.','acceptedProcedures':[{'id':s['id'],'modelPointer':'/completeProcedures/'+str(procedures.index(s)),'procedureTextSha256':hashlib.sha256(s['procedure'].encode('utf-8')).hexdigest(),'nativeAccessRows':len(s['completeSourceAndAccess']['classAccess'])} for s in selected],'acceptedCaseIds':[c['id'] for c in cases],'counts':{'identities':4,'originalMains':8,'branches':18,'events':253,'actualCasts':23,'allOriginalQuestionsPreserved':20,'nativeAccessRows':sum(len(s['completeSourceAndAccess']['classAccess']) for s in selected)},'verification':{'wholeArchiveDataChecksPassed':5609,'wholeArchiveClassCardChecksPassed':712,'wholeArchiveWizardBookChecksPassed':839,'wholeArchiveCastSourceChecksPassed':1159,'wholeArchiveCastSourceFindings':1,'selectedCaseCastSourceFindings':0,'allSelectedForwardInverseEventsPass':True,'allSelectedSubstantiveCaseEventsRead':True,'offTurnPaidNormalActions':0,'initialActorBodyOverlaps':0,'noCanonicalSourceDrift':True},'nativeAndOriginalDataPreserved':True,'retainedHolds':read(E/'HOLD_REGISTER.json'),'reviewNotes':{k:v for k,v in review['caseReviewNotes'].items() if k!='Disintegrate'},'archive':bind(D/'DD_LifeMatter5_Director_Return01_130.zip'),'acceptedFileBindings':[bind(p) for p in sorted(E.rglob('*')) if p.is_file()],'canonicalBaseline':bind(index),'evidenceReports':[bind(D/f) for f in ['LIFEMATTER5_RETURN01_INDEPENDENT_DATA_AUDIT_V2_129.json','LIFEMATTER5_ACTOR_CARD_AUDIT_129.json','LIFEMATTER5_BOOK_AUDIT_129.json','LIFEMATTER5_RETURN01_CAST_SOURCE_AUDIT_129.json','LIFEMATTER5_RETURN01_SEMANTIC_REVIEW_129.json']],'canonicalApplied':False,'runtimeExecuted':False,'humanPlaytests':False,'balanceApproval':False,'cosmologyApproval':False,'releaseApproval':False,'localRuleOrCaseChanges':0}
out.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');print(json.dumps({'receipt':bind(out),'acceptedIdentities':ids,'counts':receipt['counts'],'disintegrate':'pending focused correction'}))
