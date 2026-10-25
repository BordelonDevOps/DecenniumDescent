"""Fresh acceptance recording for four independently read Information8 identities; data only."""
from pathlib import Path
import json,hashlib,datetime,copy,sys
sys.stdout.reconfigure(encoding='utf-8')
D=Path(__file__).parent;G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';E=D/'information8_return01_received'
ids=['arcane-eye','faction-destiny','legend-lore','prophetic-frenzy'];excluded=['concordant-mindlink','faction-prophecy','find-the-path','resonance-prophecy']
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def sha(b):return hashlib.sha256(b).hexdigest()
def bind(p):return {'path':p.relative_to(G).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
def fresh(p,b):
 assert not p.exists(),str(p)
 p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
ip=R/'data/public/spell_playtests/authored_review_index.json';index=read(ip)
assert sha(ip.read_bytes())=='4f29c42cae7a3e1f8fee5de218cc7feb939370f69b7403eeeea83fd1a4192d2d'
assert index['authoredCounts']=={'reviewed':628,'pending':220}
assert read(E/'evidence/CURRENT_INDEX.json')==index
manifest=read(E/'MANIFEST.json');bindings=[]
for item in manifest['members']:
 p=E/item['path'];assert p.resolve().is_relative_to(E.resolve())
 assert p.stat().st_size==item['bytes'] and sha(p.read_bytes())==item['sha256'];bindings.append(bind(p))
bindings.append(bind(E/'MANIFEST.json'));assert len(bindings)==114
archive=D/'DD_Information8_Director_Return01_131.zip'
assert archive.stat().st_size==473006337 and sha(archive.read_bytes())=='25512356223bf074f1afc709e49bc7da33c921d09ba61ce71ff6a747f067b67e'
reports=[D/n for n in ['INFORMATION8_RETURN01_INDEPENDENT_DATA_AUDIT_129.json','INFORMATION8_RETURN01_ACTOR_CARD_AUDIT_129.json','INFORMATION8_RETURN01_BOOK_AUDIT_129.json']]
audits=[read(p) for p in reports];assert all(a['errors']==[] for a in audits)
assert [a['checks'] for a in audits]==[14255,384,663]
catalog={s['id']:s for s in read(R/'data/public/spell_playtests/catalog.json')['spells']}
procs=read(E/'PROCEDURES.json')['spells'];shared=read(E/'SHARED_RULES.json');assert len(procs)==8 and len(shared)==6
assert all(s['completeNativeSourceAndAccess']==catalog[s['id']] for s in procs)
source_same=[];historical_drift=[]
base=E/'evidence/original_sources'
for p in base.rglob('*'):
 if not p.is_file():continue
 rel=p.relative_to(base);q=G/rel
 if q.is_file():
  if p.read_bytes()==q.read_bytes():source_same.append(bind(q))
  else:historical_drift.append(rel.as_posix())
assert historical_drift==['DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'] and len(source_same)==27
allcases=[]
def walk(c):
 allcases.append(c)
 for b in c['branches']:walk(b)
main=read(E/'CASEBOOK.json')['mainCases']
for c in main:walk(c)
selected=[c for c in allcases if c['spellId'] in ids];caseids=[c['id'] for c in selected]
events=[e for c in selected for e in c['timeline']]
casts=[x for x in audits[0]['casts'] if x['event'] in {e['id'] for e in events}]
# Destiny explicitly imports the institution rule embedded in Prophecy. Preserve that exact clause,
# without selecting Prophecy's procedure or the four rejected case families.
institution=next(s for s in procs if s['id']=='faction-prophecy')['procedure'].split('\n\nINFO131-INSTITUTION: ',1)[1]
model={'id':'INFORMATION4-EXACT-REFERENCE-ENVELOPE-129','status':'EXACT_DIRECTOR_BYTES_ASSEMBLED_FOR_FOUR_IDENTITY_ACCEPTANCE','acceptedIds':ids,'excludedPendingIds':excluded,'completeProcedures':copy.deepcopy(procs),'sharedRules':copy.deepcopy(shared)+[{'id':'INFO131-INSTITUTION','rule':institution,'exactSource':{'file':'PROCEDURES.json','pointer':'/spells/2/procedure','prefix':'INFO131-INSTITUTION: '},'selectedScope':'Faction Destiny only; this does not select Faction Prophecy.'}],'assemblyOnly':'All eight complete procedure objects and six shared rule objects are exact delivered values. The separately embedded institution clause is reproduced verbatim for Destiny. Only the four explicitly named identities are selected; excluded procedures/cases remain evidence. Historical pending labels/counts remain historical.'}
mp=D/'INFORMATION4_EXACT_REFERENCE_MODEL_129.json';fresh(mp,enc(model))
findings=[
 {'id':'INFO129-F01','identities':['resonance-prophecy'],'cases':['DI6-06-A','DI6-06-B','DI6-06-B/actual-paid-Ready-distinct-from-flight'],'issue':'Actual NEAR wall blocks C body to initial field center; FAR wall does not fully hide R body. True visibility flags contradict physical extents.','evidence':'NEAR x5..15,y-10..0,z0..8 contains segment point14,-9,3. FAR y<=12 misses ray to R body corner57.5,22.5 at x48/y13.826.'},
 {'id':'INFO129-F02','identities':['resonance-prophecy'],'issue':'Ready permitted view exposes hidden R coordinates/internal phase; eligible committed Counterspell notice is omitted.','case':'DI6-06-B/actual-paid-Ready-distinct-from-flight:9'},
 {'id':'INFO129-F03','identities':['find-the-path'],'issue':'DI6-04-B finite map lacks corridor boundaries proving claimed120ft detour shortest; positive clear itinerary alone is insufficient. Corrected guard movement/bar placement is retained.'},
 {'id':'INFO129-F04','identities':['concordant-mindlink','resonance-prophecy'],'cases':['UN5-06-A/actual-suppressed-recipient-send','DI6-06-B'],'issue':'X/D classDispel at18.1 lacks source-proven perception of ongoing Lesser Antimagic. Suppressor-ending exception does not waive perception.'},
 {'id':'INFO129-F05','identities':['faction-prophecy'],'case':'DI5-06-B:30','issue':'At18.2, seven-day inquiry ends604818.2 yet output forecasts earliest replacement day8 from691200..777600. Destiny30-day forecasts retain their valid separate scope.'}
]
notes={
 'arcane-eye':'Full two mains and three branches read: native Universal sensor; full1inch sphere/sweep through actual aperture and closing barrier; behind-door clear sphere; actual2RP ArcaneSight gives independent aura perception before3RP classDispel; same-caster concentration conflict; no remote origin or creature target grant.',
 'faction-destiny':'Both mains and protected-leader branch read: full pre-established finite institution/private physical capacities;30day supported conditional alternatives and stable overlapping-window selection; actual paid Disintegrate destroys two empty carts; day1 elapsed out-of-initiative inquiry pays real Action/RP/D; protected individual intention stays Indeterminate while independent transport failure remains readable. Day8 is within this selected30day scope.',
 'legend-lore':'Both mains and equivalent retry branch read: actual pre-existing legendary history, authentic physical references; remote subject-only LoE exception; ambiguous reference gives nondiagnostic Indeterminate; actual courier continuous movement and separate reading Action precede new10RP inquiry; equivalent retry does not authenticate or rotate facts.',
 'prophetic-frenzy':'Both mains and five branches read: only printed NegateHit/AutomaticSave modes selected, no AutomaticTask. Actual old/new bank, countered cast, three-use depletion, real Focused stance, W3 death-save incapacity, full MarkOmen/FateCoin/FateReversal lineage and real hand/free-interaction sequence. Current ForceWard halves10force to5 only where actually acquired; no phantom Divination fire resistance. No invented interrupt provider or hidden outcome presentation.'}
scope='Only Arcane Eye, Faction Destiny, Legend Lore and Prophetic Frenzy, their selected cases and source-applicable shared requirements are accepted. The exact INFO131-INSTITUTION clause is selected solely as expressly imported by Faction Destiny. Concordant Mindlink, Faction Prophecy, Find the Path and Resonance Prophecy remain unaccepted candidate evidence pending the listed corrections. All prior accepted cohorts and content/runtime/human/balance/cosmology/temporal/release holds remain. No new global rule, class grant or runtime selector is introduced.'
review={'id':'INFORMATION8-RETURN01-INDEPENDENT-SEMANTIC-REVIEW-129','recordedAtUtc':now,'status':'FOUR_ACCEPTABLE_FOUR_REQUIRE_DIRECTOR_CORRECTION','reviewedAllEightProcedures':True,'originalQuestionsRead':25,'originalMainsRead':16,'branchesRead':16,'dataChecksPassed':sum(a['checks'] for a in audits),'sourceFilesExactCurrent':27,'historicalIndexPreserved':historical_drift,'bookCapacityCandidatesResolved':'Actual selected Floating Preparation at class6 grants one extra any-school matrix; W7 capacity12, W13 variants18; actual45minute prior-rest study retained.','timingCandidatesResolved':'Three actual long walks and real readied Dimension Door release; no off-turn new paid Action. Outside initiative paid casts have actual>=6seconds spacing. Raid uses actual actor phase/encounter, not nullable global descriptive label.','forceWardFindingResolved':True,'perIdentityReview':notes,'acceptedIds':ids,'excludedPendingIds':excluded,'findings':findings,'scope':scope,'runtimeExecuted':False,'suppliedProgramsExecuted':False}
rp=D/'INFORMATION8_RETURN01_SEMANTIC_REVIEW_129.json';fresh(rp,enc(review))
accept={'id':'INFORMATION4-EXACT-AUTHORED-ACCEPTANCE-129','recordedAtUtc':now,'status':'EXACT_FOUR_AUTHORED_PROCEDURES_ACCEPTED_WITH_RETAINED_HOLDS','approvedForCanonicalApplication':True,'acceptedIdentities':ids,'excludedPendingIdentities':excluded,'semanticFindings':[],'excludedFindings':findings,'authority':'Director selected complete Return01 followed by independent full source/card/book, state and semantic review under owner instruction to apply each accepted batch in Calibration review part6.','scope':scope,'acceptedProcedures':[{'id':s['id'],'modelPointer':'/completeProcedures/'+str(n),'procedureTextSha256':sha(s['procedure'].encode()),'nativeAccessRows':len(s['completeNativeSourceAndAccess']['classAccess'])} for n,s in enumerate(procs) if s['id'] in ids],'acceptedCaseIds':caseids,'counts':{'identities':4,'mains':8,'branches':len(selected)-8,'events':len(events),'newCastTransitions':len(casts),'allOriginalQuestionsPreserved':25},'verification':{'wholeArchiveDataChecks':14255,'wholeArchiveCardChecks':384,'wholeArchiveBookChecks':663,'selectedSemanticFindings':0,'allSelectedSubstantiveCaseEventsRead':True,'allSelectedForwardInverseEventsPass':True,'sourceFilesExactCurrent':27,'nativeAccessExactCurrent':True},'retainedHolds':read(E/'HOLDS.json'),'reviewNotes':notes,'archive':bind(archive),'acceptedFileBindings':bindings,'referenceModel':bind(mp),'canonicalBaseline':bind(ip),'evidenceReports':[bind(p) for p in reports]+[bind(rp)],'canonicalApplied':False,'runtimeExecuted':False,'humanPlaytests':False,'balanceApproval':False,'cosmologyApproval':False,'releaseApproval':False,'localRuleOrCaseChanges':0,'localPackagingOnly':True}
ap=D/'INFORMATION4_EXACT_ACCEPTANCE_129.json';fresh(ap,enc(accept))
print(json.dumps({'acceptance':bind(ap),'model':bind(mp),'counts':accept['counts'],'checks':review['dataChecksPassed'],'accepted':ids,'pendingCorrections':excluded},indent=2))
