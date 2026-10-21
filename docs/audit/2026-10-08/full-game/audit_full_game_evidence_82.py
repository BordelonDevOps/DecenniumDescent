"""Current read-only evidence frontier; no gameplay or historical ledger edits."""
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib,json
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
LEDGER=R/'data/playtest/game_development_coverage.json'
OUT=A/'FULL_GAME_CURRENT_EVIDENCE_FRONTIER_82.json'
MAP=A/'FULL_GAME_CURRENT_REVIEW_MAP_82.md'
CHECK=A/'FULL_GAME_CURRENT_EVIDENCE_FRONTIER_82_CHECK.json'
SAVED=A/Path(__file__).name
for p in [OUT,MAP,CHECK,SAVED]:assert not p.exists(),str(p)
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(d):return (json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def info(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return {'path':p.relative_to(G).as_posix(),'bytes':p.stat().st_size,'sha256':h.hexdigest()}
checks=[]
def ck(name,ok):
 checks.append({'check':name,'pass':bool(ok)})
 if not ok:raise AssertionError(name)
base=LEDGER.read_bytes();ledger=j(LEDGER);rows=ledger['aspects']
ck('All75 original distinct domain IDs present',len(rows)==75 and {x['id'] for x in rows}=={f'DD-{i:02d}' for i in range(75)})
for x in rows:ck('Full explicit requirement and acceptance gate '+x['id'],bool(x['requiredCoverage']) and bool(x['acceptanceGate']))
refs=defaultdict(list);fields=['sourceEvidence','reviewEvidence','draftEvidence','validationEvidence','humanEvidence']
for row in rows:
 for field in fields:
  for value in row.get(field,[]):
   ck('Evidence path has explicit string form '+row['id']+'/'+field,isinstance(value,str))
   refs[value].append({'domain':row['id'],'evidenceRole':field})
evidence=[];bydomain=defaultdict(list)
for path,uses in sorted(refs.items()):
 p=G/path;ck('Referenced local evidence exists '+path,p.exists())
 if p.is_file():record={'kind':'file',**info(p),'references':uses}
 else:
  members=[info(f) for f in sorted(p.rglob('*')) if f.is_file()]
  record={'kind':'directory','path':path,'fileCount':len(members),'members':members,'references':uses}
 evidence.append(record)
 for use in uses:bydomain[use['domain']].append({'path':path,'kind':record['kind'],'evidenceRole':use['evidenceRole']})
ck('Bounded evidence reference census',len(refs)==1135 and sum(map(len,refs.values()))==4088)
ck('Existing closure declarations are preserved',Counter(x['closure'] for x in rows)==Counter({'open':74,'closed':1}) and next(x for x in rows if x['closure']=='closed')['id']=='DD-23')

bound_sources={}
def bind(p):
 f=info(p);bound_sources[f['path']]=f;return f
current=[]
def fact(id,domains,text,paths,status='CURRENT_EVIDENCE_OBSERVATION',qualification=None):
 current.append({'id':id,'domains':domains,'status':status,'statement':text,'sources':[bind(p) for p in paths],'qualification':qualification})
cpfile=A/'ACTIVE_AUTHORING_CHECKPOINT_BESTIARY_REFRESH_81.json';cp=j(cpfile)
qfile=G/cp['currentWorkQueue']['path'];queue=j(qfile)
idxfile=R/'data/public/spell_playtests/authored_review_index.json';idx=j(idxfile)
regfile=R/'data/director/spell_review/accepted_interface_registry_06.json';registry=j(regfile)
ck('Exact source checkpoint81',info(cpfile)['sha256']=='a2284feab326a9cbeffd366d6b959135bf54a05d5c8e713c993951225c376946')
ck('Exact current queue67',info(qfile)==cp['currentWorkQueue'])
ck('525/323 applied counts and249 standalone',idx['authoredCounts']=={'reviewed':525,'pending':323} and idx['representationCounts']['completeReviewedStandaloneProcedures']==249)
ck('173 registered scoped interfaces',len(registry['entries'])==173)
ck('56groups cover all323unique pending identities',len(queue['groups'])==56 and len(queue['rows'])==323 and len(set(r['id'] for r in queue['rows']))==323 and all(r['currentGroup'] for r in queue['rows']))
accepted=[r for r in queue['rows'] if r['currentPhase'] in ['actual-exact-accepted-integration-staged-not-applied','actual-full-conference-accepted-successor-not-applied']]
ck('50 accepted successors remain unapplied',len(accepted)==cp['acceptedButUnapplied']==queue['acceptedButUnappliedTotalCurrent']==50 and not cp['implementationApplied'])
fact('CURRENT-SPELL-QUEUE',['DD-11','DD-12','DD-13','DD-18','DD-24','DD-35'],
 'The applied ordinary-spell index records525 reviewed and323 pending out of848;249 complete standalone procedures and173 scoped interfaces. All323pending identities have56 source/review groups. Of these pending applied-index entries,50 have accepted-but-unapplied successors;273 do not yet have that acceptance status. Preserve all conditional and whole-case holds.',
 [cpfile,qfile,idxfile,regfile],qualification='Source grouping is not authored acceptance. Accepted but unapplied entries remain pending in the applied index; no count is a percentage of whole-game completion.')

exstatus=R/'docs/mechanics/expedition/EXPEDITION_REVIEW_STATUS.json';ex=j(exstatus)
exlabels=A/'EX58_REVIEW_LABEL_NORMALIZATION.json';exlabel=j(exlabels)
exful=A/'EX58_X01_FULFILLMENT.json';exf=j(exful)
excov=A/'EX58_COVERAGE_ADDENDUM.json';exc=j(excov)
exbindings=[]
for path,bound in exlabel['currentEightCandidateFiles'].items():
 actual=info(G/path);match=actual['bytes']==bound['bytes'] and actual['sha256']==bound['sha256'];exbindings.append({'path':path,'recorded':bound,'current':actual,'matches':match});ck('Exact reviewed EX58 current artifact '+path,match)
ck('EX58 scoped authored approval and unclosed testing gates',ex['exactCandidateAuthoredApproval'] and exf['exactCandidateAuthoredApproval'] and not ex['runtimeImplemented'] and not ex['humanPlaytestConfirmed'] and not ex['wholeGameFlowConfirmed'])
fact('EX58-CURRENT-ACCEPTED-SCOPE',list(exc['scopes']),
 'The completed EX58 exact review and fulfilled X01 correction govern the expedition, transport, social and reputation candidate. All eight current artifacts still match the recorded final bytes. The58source directions,190chapter examples,29transport profiles,four auxiliaries,21integrated events,15contract families,28boundary cases and24social scenarios are authored evidence. Earlier expedition26 prepared/unsent labels are historical.',
 [exstatus,exful,exlabels,excov],status='EXACT_AUTHORED_SCOPE_ACCEPTED_CURRENT_BYTES_VERIFIED',qualification='Broader domain closure, runtime, selection enablement, human testing, balance and whole-game flow remain unproved. Do not dispatch a duplicate preliminary expedition26 conference.')
for d,text in exc['scopes'].items():
 fact('EX58-SCOPE-'+d,[d],text,[excov,exstatus],status='EXISTING_REVIEWED_SCOPE_RESTATEMENT',qualification='This is the verbatim scoped addendum; it expressly closes no full domain.')

laxstatus=R/'docs/mechanics/LANGUAGE_REVIEW_STATUS.json';lax=j(laxstatus)
laxreceipt=A/'LANGUAGE_EXACT_FULFILLMENT.json';lx=j(laxreceipt)
for path,hash in lx['finalHashes'].items():ck('Current exact language file '+path,info(G/path)['sha256']==hash)
ck('LAX exact authored approval',lax['exactLanguageApproval'] and lx['exactLanguageApproval'])
fact('LANGUAGE-CURRENT-EXACT-SCOPE',['DD-04','DD-15','DD-45','DD-46','DD-54','DD-60','DD-61'],
 'The LAX-EXACT-2026-10-11 language/communication scope is accepted; all seven current final files match the receipt. Historical language-conference-pending text is superseded within that exact scope. Broader integration remains open.',
 [laxstatus,laxreceipt],status='EXACT_AUTHORED_SCOPE_ACCEPTED_CURRENT_BYTES_VERIFIED')

bestiaryprep=A/'BESTIARY_COMPLETE_FILE_HANDOFF_V3_PREPARATION_81.json';bp=j(bestiaryprep)
ck('Bestiary current packet exact',info(G/bp['archive']['path'])==bp['archive'] and not bp['sent'])
fact('BESTIARY-CURRENT-PREPARATION',['DD-28','DD-29','DD-33','DD-34','DD-35','DD-38','DD-54','DD-65'],
 'Complete bestiary V3 is prepared and unsent:67dossiers,66stat blocks,26public routes,162listed actions,79trait occurrences,178harvest entries and27unselected source questions. It preserves the entire V2 archive, all370previous current dependencies and full before/current pairs for seven changes.396modifier and119printed damage-mean diagnostics plus preservation checks total1525passing checks.',
 [bestiaryprep,A/'BESTIARY_CURRENT_SOURCE_INTERFACES_81.json'],status='SOURCE_PREPARATION_UNSENT',qualification='No creature behavior or numerical balance is newly approved. ExactCR2 Undead absence is bounded to the66known stat blocks; positive Command Undeath case holds remain.')

feat=A/'FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_AFTER_FLORA_FULFILLMENT.json';ft=j(feat)
ck('Feat parent exact review still explicitly open',not ft['fullFeatCandidateApproved'] and not ft['all335FullAcquisitionsExecuted'])
fact('FEAT335-PARENT-GATE',['DD-04','DD-06','DD-07','DD-08','DD-14','DD-15','DD-17','DD-69'],
 'The current acquisition follow-through records fulfilled finite findings and assembled335-feat acquisition/initial-state evidence, while explicitly leaving full assembled335-feat exact review and execution of all335acquisitions open. Later scoped copied-feature choices are preserved in the pertinent-decisions ledger and accepted spell contexts; none proves the parent feat gate closed.',
 [feat,A/'FEAT335_FULL_EXACT_REVIEW_PREFLIGHT.json',A/'PERTINENT_GPT_DECISIONS_2026_10_20_02.json'],status='BOUNDED_FULFILLMENT_PARENT_REVIEW_OPEN')

for fname,domains in [
 ('CHARACTER_FOUNDATION_REVIEW_STATUS.json',['DD-04','DD-06','DD-07']),
 ('ANCESTRY_BACKGROUND_REVIEW_STATUS.json',['DD-04','DD-05']),
 ('EQUIPMENT_REVIEW_STATUS.json',['DD-25','DD-26','DD-27','DD-28']),
 ('ADVANCED_CRAFT_REVIEW_STATUS.json',['DD-28','DD-29','DD-30','DD-31']),
]:
 p=R/'docs/mechanics'/fname;d=j(p)
 extra=[p]
 if fname=='ADVANCED_CRAFT_REVIEW_STATUS.json':extra += [A/'TEACHING_TEX_EXACT_FULFILLMENT.json',A/'TC_RECYCLING_01_CONTROLLING_ERRATUM.md',A/'TEACHING_TEX_ADDENDUM_FULFILLMENT.json',A/'TEX_CONTROLLING_ADDENDUM_2026_10_11.md']
 fact('REPORTED-'+fname.removesuffix('.json'),domains,str(d['status']),extra,status='CURRENT_STATUS_RECORD_BOUND_NOT_REAUDITED',qualification='Status and referenced source files are preserved as existing evidence. This frontier audit does not rerun the original semantic review, certify every dependent content item or close a whole domain.')

cosmo_paths=[R/'data/director/cosmology'/n for n in ['chronology_source_reviewed_01.json','chronology_research_route_reviewed_01.json','creation_origins_reviewed_01.json','owner_reconciliation_reviewed_01.json','planes_reviewed_01.json','gods_pantheons_reviewed_01.json','souls_research_reviewed_01.json','epilogue_campaign_arcs_reviewed_01.json','epilogue_character_reviewed_01.json','epilogue_relic_null_reviewed_01.json','q6_later_lock_reviewed_01.json']]
push=G/cp['latestPreviouslyVerifiedGitHubBackup']['receipt']['path']
ck('Previously verified push receipt remains exact',info(push)==cp['latestPreviouslyVerifiedGitHubBackup']['receipt'])
fact('POST-PUSH-SCOPED-COSMOLOGY',['DD-47','DD-48','DD-49','DD-50','DD-51','DD-52','DD-54','DD-65','DD-74'],
 'The required GitHub-before-cosmology sequence has already progressed to documented scoped cosmology successors. Current chronology, origins/owner reconciliation, planes, pantheons, souls/research, epilogue and Null/Q6 records exist and are bound here. Earlier blanket post-push deferral or Part2 conversation-limit labels are history. The latest previously verified backup remains commit9367b319e460134a3fc35b530da29ecbe6224b6a through checkpoint72; later work is local.',
 [push,*cosmo_paths],status='CURRENT_SCOPED_RECORDS_BOUND',qualification='No cosmology is reinterpreted and no new canon decision is made by this audit. File presence and hashes are not a claim that every setting domain is finished.')
unity=A/'UNITY_DEVELOPMENT_DIRECTIONS_INTAKE_75.json';brief=A/'unity-development-directions-75/Decennium_Descent_Unity_Codex_Directions.md'
ck('Unity brief complete preserved identity',info(brief)['sha256']=='cfca586c7351f7ac913523a3b9cde076bc3e92f4301404f1f78b608db6145369')
fact('UNITY-DIRECTION-PRESERVED',['DD-01','DD-05','DD-53','DD-58','DD-59','DD-60','DD-62','DD-63','DD-64','DD-65','DD-67','DD-69','DD-70','DD-71','DD-72','DD-73'],
 'The full18-section Unity brief is preserved: SNES-style direct exploration, tactical combat, companion resource management, shared simulation and continuing AI engineering oversight. Its prepared starter prompt is not a new owner command to implement rules. The intake distinguishes directions from an implemented/tested Unity game.',
 [unity,brief,A/'UNITY_DIRECTIONS_PERTINENT_RECHECK_81_NATIVE.json'],status='DIRECTION_PRESERVED_IMPLEMENTATION_NOT_PROVED',qualification='No new combat cadence, engine implementation, scene execution or playability is inferred.')

domains=[]
for original in rows:
 matches=[f for f in current if original['id'] in f['domains']]
 domains.append({'id':original['id'],'domain':original['domain'],'requiredCoverage':original['requiredCoverage'],'acceptanceGate':original['acceptanceGate'],'originalClosureDeclaration':original['closure'],'originalStatusLabel':original['status'],'completionClass':original.get('completionClass'),'originalFullLedgerRow':original,'existingEvidenceReferences':bydomain[original['id']],'currentEvidenceFactIds':[f['id'] for f in matches],'newClosureClaimed':False,'completionInterpretation':'Original closed declaration is retained only in its stated scope; no global engine, balance or release completion inferred.' if original['closure']=='closed' else 'Whole-domain gate remains open. Reuse exact accepted subscopes and continue the remaining explicit requirements; current evidence facts qualify historical status notes without deleting them.'})
ck('Every original domain row retained completely',all(a['originalFullLedgerRow']==b for a,b in zip(domains,rows)))
report={'id':'FULL-GAME-CURRENT-EVIDENCE-FRONTIER-82','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'CURRENT_EVIDENCE_NAVIGATION_AUDIT_NO_RULE_OR_GATE_PROMOTION','baseLedger':info(LEDGER),'currentAuthoringCheckpoint':bind(cpfile),'currentQueue':bind(qfile),'scope':'All75explicit domain requirements and their five evidence-role lists. Complete original rows retained; bounded current authoritative receipts clarify stale labels. No completion percentage is inferred.',
 'counts':{'domains':75,'originalOpenDeclarations':74,'originalClosedDeclarations':1,'uniqueEvidencePaths':len(refs),'evidenceRoleUses':sum(map(len,refs.values())),'fileReferences':sum(x['kind']=='file' for x in evidence),'directoryReferences':sum(x['kind']=='directory' for x in evidence),'missingReferences':0,'currentEvidenceFacts':len(current),'newDomainClosures':0},
 'currentOrdinarySpellCounts':{'total':848,'appliedReviewed':525,'appliedPending':323,'standalone':249,'interfaces':173,'acceptedButUnapplied':50,'otherPending':273,'preparedGroups':56,'ungroupedPending':0},
 'acceptedButUnappliedIdentities':[{'id':x['id'],'group':x['currentGroup'],'phase':x['currentPhase']} for x in accepted],
 'currentFacts':current,'exactEX58CurrentArtifactChecks':exbindings,'allReferencedEvidence':evidence,'additionalBoundSources':list(bound_sources.values()),'domains':domains,
 'nextWorkOrder':['Receive and independently review the same active Resonance Fields3 return; no restarting a live request.','Confer on the prepared complete bestiary V3 packet, retaining exact current language/crafting/companion/spell contracts.','Continue all remaining prepared spell groups and full assembled feat exact review; do not reopen fulfilled EX58 preliminaries.','Resolve remaining whole-domain integration requirements and perform the final joint authored flow review.','Keep owner-reserved application, engine/runtime work, human testing, numerical balance and publication/release as separate evidence gates.'],
 'sourceInformationDeleted':0,'canonicalChanges':False,'runtimeTestsExecuted':0,'wholeGameComplete':False,'limitations':['Reference existence and hashes do not establish that cited evidence proves a gate.','The1135-path census covers the explicit five evidence lists; prose-only mentions and all possible project files are not claimed audited by it.','Current status records labeled not reaudited are reported as existing evidence, not newly accepted here.','The original74open/1closed declarations are not a percentage-complete measure.','The full repository is not duplicated in this frontier; source identities and complete original ledger rows are retained and paths are verified.']}
lines=['# Current whole-game review map','', 'This map preserves all75 domain requirements and points to current evidence without changing game rules or closing gates. It distinguishes older status notes from later exact reviews.','',
 '**Current spell status:**525 applied reviewed /323 pending;50 of the pending entries have accepted but unapplied successors. All323 have source/review groups. This is not a whole-game completion percentage.','',
 '**Settled preliminary work to reuse:** EX58 expedition/transport/social/reputation and LAX language exact scopes remain accepted; all eight EX58 and seven LAX current final artifacts match their receipts. Earlier preliminary “unsent” labels do not require repeating those conferences.','',
 '**Next content discussion:** the complete bestiary V3 is prepared and unsent. Its27 source questions cover actual creature procedures and harvest/crafting interfaces; it does not yet approve those creatures.','',
 '**Whole-game gates:** the retained ledger declares74 domains open and DD-23 closed in its stated health/death scope. This audit makes no new closure claim. Runtime, human gameplay, balance and release remain separate.','',
 '[Full source-bound evidence and original domain rows](FULL_GAME_CURRENT_EVIDENCE_FRONTIER_82.json) · [Current checkpoint](ACTIVE_AUTHORING_CHECKPOINT_BESTIARY_REFRESH_81.json) · [Bestiary packet preparation](BESTIARY_COMPLETE_FILE_HANDOFF_V3_PREPARATION_81.json)','',
 '## Current evidence qualifications','']
for f in current:
 if f['id'].startswith('EX58-SCOPE-'):continue
 links='; '.join('['+Path(s['path']).name+']('+str(Path(s['path']).relative_to('docs/audit/2026-10-08/full-game')).replace('\\','/')+')' if s['path'].startswith('docs/audit/2026-10-08/full-game/') else '['+Path(s['path']).name+'](../../../../'+s['path']+')' for s in f['sources'][:4])
 lines.extend(['- **'+f['id']+'** — '+f['statement']+' '+links, ''])
lines.extend(['## Every required domain','', '| ID | Domain | Required coverage | Acceptance gate | Recorded declaration | Current evidence |','|---|---|---|---|---|---|'])
def cell(s):return str(s).replace('|','\\|').replace('\n',' ')
for d in domains:lines.append('| '+' | '.join(cell(x) for x in [d['id'],d['domain'],d['requiredCoverage'],d['acceptanceGate'],d['originalClosureDeclaration'],'; '.join(d['currentEvidenceFactIds']) or 'Full original evidence retained; remaining gate not re-adjudicated.'])+' |')
lines+=['','## Scope of these checks','','All1135 explicitly listed evidence paths resolve:1132files and3directories, used4088times across source/review/draft/validation/human evidence roles. Directory members are inventoried. Hashes bind current bytes; they do not establish substantive approval. Every original domain row, issue, review scope and evidence reference remains intact in the JSON. No rules, old files, closure declarations or runtime were changed.','']
ck('Original whole-game ledger byte-identical at end',LEDGER.read_bytes()==base)
ck('Current queue unchanged at end',info(qfile)==cp['currentWorkQueue'])
for v in cp['canonicalHelperBaselinesUnchanged']:ck('Reserved helper unchanged '+v['path'],info(G/v['path'])==v)
OUT.write_bytes(enc(report));MAP.write_text('\n'.join(lines),encoding='utf-8');SAVED.write_bytes(Path(__file__).read_bytes())
CHECK.write_bytes(enc({'frontier':info(OUT),'reader':info(MAP),'checks':checks,'checkCount':len(checks),'failures':0,'newDomainClosures':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0,'scope':report['scope']}))
print(json.dumps({'frontier':info(OUT),'reader':info(MAP),'checkReport':info(CHECK),'counts':report['counts'],'checks':len(checks),'failures':0}))
