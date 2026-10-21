"""Preserve complete miracle/reality sources and unselected review choices."""
from pathlib import Path
from datetime import datetime,timezone
from copy import deepcopy
import hashlib,json,zipfile
from prepare_rank9_alignment_faction_purification_5_source_conference_01 import G,R,A,read,enc,info,at
from rank9_miracle_reality_2_questions_01 import IDS,TIERS,Q,FINDINGS,CASES

def main():
 stem='RANK9_MIRACLE_REALITY_2_SOURCE_CONFERENCE_01';root=A/'rank9-miracle-reality2-source-conference-01';out=R/'data/director/spell_review/rank9_miracle_reality_2_source_conference_01.json'
 check,prep,request=[A/(stem+s) for s in ['_CHECK.json','_PREPARATION.json','_REQUEST.txt']];archive=A/'DD_Rank9_Miracle_Reality_2_Source_Conference_01.zip'
 assert not any(p.exists() for p in [root,out,check,prep,request,archive])
 sources={};checks=[]
 def ck(n,v):
  checks.append({'check':n,'passed':bool(v)})
  assert v,n
 def bind(p):
  p=p.resolve();b=info(p);sources[b['path']]=b;return b
 cpfile=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK7_RECOVERY_ACCEPTED_79.json';cp=read(cpfile)
 catp=R/'data/public/spell_playtests/catalog.json';ip=catp.parent/'authored_review_index.json';qp=R/'data/director/spell_review/remaining_work_queue_66.json';regp=qp.parent/'accepted_interface_registry_06.json'
 cov=R/'data/playtest/game_development_coverage.json';ledger=A/'PERTINENT_GPT_DECISIONS_2026_10_20_02.json'
 catalog,index,queue,registry=map(read,[catp,ip,qp,regp]);protected={p:p.read_bytes() for p in [catp,ip,qp,regp,cpfile,cov,ledger]}
 ck('Exact checkpoint79',info(cpfile)['sha256']=='ad8c04966e578038887c04633f669b6c31bec344451c47b180a5820b267c7451');ck('Exact queue66',info(qp)==cp['currentWorkQueue'])
 ck('50accepted remain unapplied',cp['acceptedButUnapplied']==50 and queue['acceptedButUnappliedTotalCurrent']==50 and not cp['implementationApplied'])
 ck('Current applied coverage',index['authoredCounts']=={'reviewed':525,'pending':323} and index['representationCounts']['completeReviewedStandaloneProcedures']==249 and len(registry['entries'])==173)
 for b in cp['canonicalHelperBaselinesUnchanged']:
  p=G/b['path'];ck('Current helper '+b['path'],info(p)==b);protected[p]=p.read_bytes();bind(p)
 for p in [catp,ip,qp,regp,cpfile,cov,ledger,Path(__file__),Path(__file__).with_name('rank9_miracle_reality_2_questions_01.py'),Path(__file__).with_name('prepare_rank9_alignment_faction_purification_5_source_conference_01.py'),Path(__file__).with_name('rank9_alignment_faction_purification_5_questions_01.py'),G/'CANON_MANIFEST.md',G/'docs/canon/CANON_MANIFEST.json',G/'docs/canon/REPOSITORY_PROMOTION.md',A/'GPT_PART5_PERTINENT_OWNER_CHOICES_2026_10_20_NATIVE.json',A/'GPT_PART5_STATUS_SYNC_16_COMPLETED_NATIVE.json',G/'docs/audit/2026-10-20/github-snapshot-material-forging72/PUSH_RECEIPT.json',R/'rulebook_output.txt',G/'docs/reference/Player_Rulebook_v6_source_text.txt',R/'books/player/Decennium_Descent_Player_Rulebook_v6.docx']:bind(p)
 lines=(R/'rulebook_output.txt').read_text('utf-16').splitlines();reference=(G/'docs/reference/Player_Rulebook_v6_source_text.txt').read_text('utf-8').splitlines();records=[]
 for sid,priorname in zip(IDS,['DIVINATION_RANK9_SOURCE_PREPARATION.json','TRANSMUTATION_UNIVERSAL_RANK9_SOURCE_PREPARATION.json']):
  priorp=A/priorname;bind(priorp);prior=read(priorp);n=next(i for i,x in enumerate(prior['selectedSpells']) if x['spellId']==sid);hist=prior['selectedSpells'][n];card=next(x for x in catalog['spells'] if x['id']==sid);row=next(x for x in queue['rows'] if x['id']==sid);entry=next(x for x in index['entries'] if x['id']==sid)
  ck('Exact full source/current/history '+sid,hist['fullSourceAndCurrentAccessRecord']==card==row['completeCurrentSourceAndAccess']);ck('Actually ungrouped pending '+sid,row['currentGroup'] is None and not row['previousAuthoringMapRowUnchanged']['completeEarlierProposalRecords'] and entry['authoredStatus']=='pending-authored-procedure')
  schools={'Cleric':'Divination','Wizard':'Divination'} if sid==IDS[0] else {'Cleric':'Universal','Druid':'Transmutation','Mage':'Transmutation','Wizard':'Transmutation'};access={c:{'rank':9,'minimumClassLevel':17,'school':sc,'baseRpCost':26} for c,sc in schools.items()};ck('Exact actual class schools '+sid,card['classAccess']==access)
  count=1 if sid==IDS[0] else 2;core=card['source']['coreEntries'];ck('Complete native Core metadata '+sid,len(core)==count and all(x['original']['casting_time']=='1 action' and x['original']['range']=='120 feet' and x['original']['duration']=='Instantaneous' and x['original']['components']=='V, S, F' and x['original']['rp_cost']==26 for x in core))
  books=[deepcopy(b) for b in prior['currentBookBindings'] if b['spellId']==sid];ck('Every native placement '+sid,len(books)==len(card['source']['original']['placements'])==count)
  for b in books:
   k=b['currentBookRow']['line']-1;ck('Both exact manuscripts '+sid+str(k),lines[k]==reference[k]==b['currentBookRow']['exactText'])
  for kind in ['catalog','core']:ck('Exact underlying source '+sid+kind,bind(R/card['source'][kind+'Path'])['sha256']==card['source'][kind+'Sha256'])
  records.append({'spellId':sid,'riskTier':TIERS[sid][0],'riskReason':TIERS[sid][1],'completeCurrentCatalogSourceAndAccess':deepcopy(card),'currentIndexEntry':deepcopy(entry),'originalQuestionSource':info(priorp),'originalQuestionPointer':'/selectedSpells/'+str(n),'completeOriginalSourceQuestionUnchanged':deepcopy(hist),'completeHistoricalCommonQuestionUnchanged':prior['commonOperationalQuestion'],'completeHistoricalScopeExceptionUnchanged':prior['commonQuestionException'],'completeCurrentBookBindings':books,'earlierCompleteProcedures':[],'earlierOperationalWorkedCases':[],'status':'Source conference prepared; no selected procedure or executable vectors.'})
 mechanics=['VIDEO_GAME_ONLY_DIRECTIVE.md','CLASS_PLAYTEST_RULES.md','SPELL_INTEGRATION_RULES.md','COMBAT_ACTION_PLAYTEST.md','CORE_RESOLUTION_PLAYTEST.md','CONDITIONS_PLAYTEST.md','CONDITION_RECOVERY_PLAYTEST.md','CONTROL_STATES_PLAYTEST.md','BODY_EQUIPMENT_PLAYTEST.md','CREATURE_LIFECYCLE_PLAYTEST.md','CREATURE_LIFECYCLE_SOURCE_BINDINGS.md','MAXIMUM_HP_PLAYTEST.md','HEALING_DEATH_PLAYTEST.md','TRANSFORMATION_SPELL_PLAYTEST.md','RESONANCE_CANON.md','COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md','CHARACTER_CREATION_PLAYTEST.md','CHARACTER_FOUNDATION_TABLES.md','XP_ADVANCEMENT_CANON.md','STRAIN_PLAYTEST.md','CUSTOM_CONDITION_BINDINGS.md','CONTROL_SOURCE_BINDINGS.md','EQUIPMENT_ITEM_PROCEDURES.md','EQUIPMENT_ACQUISITION_PLAYTEST.md','WORLD_DUNGEON_LOOP.md','EXPEDITION_STRUCTURE_CANON.md','COSMOLOGY_EPILOGUE_CHARACTER_PLAYTEST.md','OWNER_COSMOLOGY_LOCKS_2026-07-30.md','APPENDIX_B_FOLK_RELIGION.md']
 for name in mechanics:
  p=R/'docs/mechanics'/name
  if not p.exists():p=G/'docs/mechanics'/name
  bind(p)
 for name in ['data/playtest/creature_lifecycle_bindings.json','data/playtest/control_state_bindings.json','data/playtest/condition_playtests.json','data/playtest/equipment_acquisition_candidate.json','data/playtest/equipment_source_catalog.json','src/data/resonance-economy.js','data/public/feat_candidates/exact_01/candidate.json','data/public/feat_candidates/exact_01/shared_rules.json','data/public/feat_candidates/exact_01/supplements.json','docs/canon/PLAYER_DIRECTOR_BOUNDARY.md']:bind(R/name)
 classes=[{'source':bind(R/('data/public/class_playtests/'+n+'.json')),'qualification':'Complete source-qualified class access and all stages; no feature entitlement or body/plane rule by analogy.'} for n in ['cleric','druid','mage','wizard','mirrorsage','oracle','monk']]
 inherited=[];nums=list(range(12))+[13,14,21,22,23,24,26,36,39,40,48,49,50,51,80,81,82,83,84,85,86,87,88,89,90,91,92,93,130,141,143,149,150]
 ck('Unique interface pointers',len(nums)==len(set(nums)))
 for n in nums:
  e=registry['entries'][n];b=e['currentAuthoritativeSource'];actual=bind(G/b['path']);ck('Exact interface source '+str(n),all(actual[k]==b[k] for k in ['bytes','sha256']));inherited.append({'registryPointer':'/entries/'+str(n),'completeEntryUnchanged':deepcopy(e),'scopeLimit':'Current named source only. Information, body, price, source attribution, Null and recovery rules remain scoped; no universal miracle or Wish override is inferred.'})
 counterparts=[]
 for sid in ['divine-perception','eyes-of-the-divine','faction-divination','resonance-divination','remove-curse','bestow-curse','resurrection','true-resurrection','mass-resurrection-denial','antimagic-field-lesser','greater-dispel','dimensional-anchor','faction-portal','soul-mirror']:
  e=next(x for x in index['entries'] if x['id']==sid);ck('Applied counterpart '+sid,e['authoredStatus']=='reviewed-authored-operational-playtest');p=(ip.parent/e['procedureFile']).resolve();d=read(p);ptr=e.get('wholeCardPointer') or e['procedurePointer'];b=bind(p)
  if e.get('completeEnvelopeBinding'):ck('Exact counterpart envelope '+sid,b==e['completeEnvelopeBinding'])
  if e.get('authoredAcceptanceReceipt'):ck('Exact counterpart receipt '+sid,bind(G/e['authoredAcceptanceReceipt']['path'])==e['authoredAcceptanceReceipt'])
  card=deepcopy(at(d,ptr))
  for k in ['operational','operationalCandidate']:
   op=card.get(k)
   if isinstance(op,dict):
    for rel in op.get('sourceReview',[])+op.get('reviewEvidence',[]):bind(G/rel)
    if op.get('authoringFile'):bind(R/op['authoringFile'])
  for rel in e.get('caseSourceReferenceAliases',{}).values():bind(G/rel)
  counterparts.append({'spellId':sid,'source':b,'pointer':ptr,'completeCurrentCard':card,'completeSharedRules':deepcopy(at(d,e['sharedRulesPointer']) if e.get('sharedRulesPointer') else d.get('sharedRules',{})),'indexEntry':deepcopy(e),'qualification':'Applied authored comparison in its exact scope; old catalog or cosmology workflow labels do not undo its current authored acceptance.'})
 cosmo=[]
 for name in ['CURRENT_COSMOLOGY_READ_FIRST.md','GODS_PANTHEONS_REVIEWED_01.md','EPILOGUE_CHARACTER_REVIEWED_01.md','PLANES_REVIEWED_01.md','HEARTCELL_OWNER_UPDATE_02.md','Q6_LATER_LOCK_REVIEWED_01.md','SOULS_RESEARCH_REVIEWED_01.md','EPILOGUE_RELIC_NULL_REVIEWED_01.md']:
  cosmo.append(bind(R/'docs/director-only/cosmology'/name))
 for name in ['planes_reviewed_01.json','gods_pantheons_reviewed_01.json','epilogue_character_reviewed_01.json','epilogue_character_cases_01.json','heartcell_owner_update_02.json','q6_later_lock_reviewed_01.json','souls_research_reviewed_01.json','epilogue_relic_null_reviewed_01.json']:
  cosmo.append(bind(R/'data/director/cosmology'/name))
 for name in ['COSMOLOGY_PLANES_SOURCE_CONCORDANCE_01.json','COSMOLOGY_PLANES_01_APPLICATION_CHECK.json','COSMOLOGY_SOULS_RESEARCH_01_APPLICATION_CHECK.json','COSMOLOGY_PLANES_TRANSIT_DEPENDENCY_READING_01.json']:cosmo.append(bind(A/name))
 planes=read(R/'data/director/cosmology/planes_reviewed_01.json');pzip=A/'DD_Cosmology_Planes_01.zip';zipbinding=bind(pzip)
 with zipfile.ZipFile(pzip) as z:
  ck('Original planes archive CRC',z.testzip() is None)
  for b in planes['sourceBindings']:
   raw=z.read('sources/'+b['path']);ck('Every original plane source retained '+b['path'],len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256'])
 frozenCosmo={'completeOriginalArchive':zipbinding,'sourceBindings':deepcopy(planes['sourceBindings']),'sourceCount':len(planes['sourceBindings']),'qualification':'These64bindings refer to frozen original inputs, including DOCX, saved website and viewer. Current chapters and exact owner amendments qualify authority; historical pending-spell/status labels are not new current status. No realm equivalence is selected.'}
 godrecord=read(R/'data/director/cosmology/gods_pantheons_reviewed_01.json');godzip=A/'DD_Cosmology_Gods_Pantheons_01.zip';godzipbinding=bind(godzip)
 godmembers=[]
 with zipfile.ZipFile(godzip) as z:
  ck('Original gods archive CRC',z.testzip() is None)
  for path,expected in godrecord['sourceHashes'].items():
   member='sources/'+path;raw=z.read(member);ck('Every original god source retained '+path,hashlib.sha256(raw).hexdigest()==expected);godmembers.append({'path':path,'member':member,'bytes':len(raw),'sha256':expected})
 godfollow=[bind(A/n) for n in ['DD_Cosmology_Gods_Pantheons_Followup_01.zip','COSMOLOGY_GODS_PANTHEONS_FOLLOWUP_01_Addendum_and_Evidence.zip','cosmology-gods-pantheons-followup-01-received/COSMOLOGY_GODS_PANTHEONS_01_REGISTER_CORRECTED.json','cosmology-gods-pantheons-followup-01-received/FOLLOWUP_DISPOSITIONS.json','COSMOLOGY_GODS_PANTHEONS_FOLLOWUP_01_RECEIVED_DECISION.json']]
 for key in ['authority','receivedDecision']:ck('Exact corrected gods authority '+key,bind(G/godrecord[key]['path'])==godrecord[key])
 godContext={'originalArchive':godzipbinding,'completeOriginalSources':godmembers,'sourceCount':len(godmembers),'fullCorrectedFollowup':godfollow,'qualification':'Original71source bytes and corrected identity/revelation distinctions preserved. Current owner, Q6 and later souls/Null records retain their scopes; no new deity equivalence or miracle menu selected.'}
 clericfile=R/'data/public/class_playtests/cleric.json';cleric=read(clericfile);saint=deepcopy(cleric['cards'][34]);ck('Distinct actual Saint feature',saint['id']=='cleric.hero.saint.divine-intervention' and saint['activation']=='Reaction' and saint['cost']=='4 RP' and saint['frequency']=='1/long rest')
 distinctSaint={'source':info(clericfile),'pointer':'/cards/34','completeCurrentCard':saint,'completeClassSourceIncluded':True,'qualification':'Separate source-specific selected Saint Hero feature. Its4RP Reaction,60feet ally target and1longrest allowance do not replace or constrain the rank9spell, and Wizard does not gain Saint access.'}
 rank7=A/'rank7-identity-casting5-part5-ready-deadline-recovery-01';acceptp=A/'RANK7_IDENTITY_CASTING5_PART5_EXACT_AUTHORING_ACCEPTANCE_79.json';accept=read(acceptp);bind(acceptp);ck('Exact accepted Rank7 model',bind(rank7/'MODEL.json')==accept['selectedSuccessor'])
 acceptedArtifacts=[bind(rank7/n) for n in ['HOLD_REGISTER.json','SPELL_DISPOSITIONS.json','QUESTION_DISPOSITIONS.json','CASE_DISPOSITIONS.json','PLAYER_CHAPTER.md','DIRECTOR_REVIEW.md','evidence/shared_rules.json','evidence/procedures.json']]
 rank7model=read(rank7/'MODEL.json');acceptedComparisons=[]
 for sid in ['sequester','simulacrum','erase-from-reality']:
  n=next(i for i,x in enumerate(rank7model['records']) if x['spellId']==sid);acceptedComparisons.append({'spellId':sid,'source':info(rank7/'MODEL.json'),'pointer':'/records/'+str(n),'completeSelectedRecord':deepcopy(rank7model['records'][n]),'completeSharedRules':deepcopy(rank7model['selectedSharedRules']),'qualification':'Exactly accepted but unapplied source-specific authoring; no universal reality, soul, copy or inventory authority inferred.'})
 pending=[]
 for sid in ['commune','divine-intervention-lesser','divine-truth','foresight-perfect','creation','fabricate','legend-lore','clone']:
  row=next(x for x in queue['rows'] if x['id']==sid);pending.append({'spellId':sid,'completeSourceAndCurrentQueueRow':deepcopy(row),'qualification':'Pending full source/status only, not positive-case authority.'})
 for n in ['rank9_resonance_fields_3_source_conference_01.json','rank9_material_forging_2_source_conference_01.json','rank9_knowledge_revelation_5_source_conference_01.json']:bind(R/'data/director/spell_review'/n)
 for n in ['RANK7_READY_DEADLINE_RECOVERY_01_SEMANTIC_RECONCILIATION_79.json','RANK8_DAMAGE6_PART5_EXACT_AUTHORING_ACCEPTANCE_75.json','rank8-damage6-part5-cast-history-return-03/MODEL.json','rank8-damage6-part5-cast-history-return-03/HOLD_REGISTER.json','copy-ready-preparation-only-part5-successor-01/POLICY_SELECTION.json','COPY_READY_PREPARATION_ONLY_PART5_01_LOCAL_PREFLIGHT.json','copy-ready-preparation-only-part5-successor-01/successor/CONTROL15_READY_REFERENCE_SUCCESSOR14.json','CONTROL15_PART5_FULL_RETURN_02_LOCAL_RECEIPT.json','UNITY_DEVELOPMENT_DIRECTIONS_INTAKE_75.json']:bind(A/n)
 questions=[{'id':i,'spellIds':ids,'exactSourceOrConflict':s,'options':opts,'recommendationAndConsequences':rec,'decisionSelected':False} for i,ids,s,opts,rec in Q]
 ck('24unique unselected questions',len(questions)==len({q['id'] for q in questions})==24 and not any(q['decisionSelected'] for q in questions));ck('All three placements preserved',len(records)==2 and sum(len(x['completeCurrentBookBindings']) for x in records)==3)
 ck('Complete question identity scope',set().union(*(set(q['spellIds']) for q in questions))==set(IDS));ck('14applied comparisons and7classes',len(counterparts)==14 and len(classes)==7)
 candidate={'id':'RANK9-MIRACLE-REALITY2-SOURCE-CONFERENCE01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'SOURCE_CONFERENCE_PREPARED_UNSENT','developmentDirection':'video-game-only','records':records,'historicalWorkflowQualification':'Original post-push wording retained as historical source; latest verified GitHub backup through72 satisfies sequencing only. Checkpoint79 governs current50accepted-unapplied status. No cosmology-equivalence or implementation approval follows.','currentAcceptedInterfaceComparisons':inherited,'completeAppliedCounterparts':counterparts,'completeClassSources':classes,'currentCosmologyContext':cosmo,'frozenOriginalCosmologyHistory':frozenCosmo,'acceptedButUnappliedRank7Context':{'receipt':info(acceptp),'completeReceipt':accept,'fullCurrentArtifacts':acceptedArtifacts,'fullModel':info(rank7/'MODEL.json'),'completeRelevantComparisons':acceptedComparisons},'pendingComparisonsNotAuthority':pending,'questions':questions,'riskCounts':{'C':2},'sourceFindings':FINDINGS,'futureCaseRequirements':CASES,'semanticDelta':[{'spellId':sid,'riskTier':'C','riskReason':TIERS[sid][1],'startingPoint':'Complete native source and historical question; no authored procedure or cases.','genuineQuestionIds':[q['id'] for q in questions if sid in q['spellIds']]} for sid in IDS],'earlierOperationalWorkedCases':[],'currentVectors':[],'countsUnchanged':deepcopy(index['authoredCounts']),'sourceBindings':list(sources.values()),'newRuleAdoptions':0,'runtimeTestsExecuted':0,'humanPlaytests':0,'sourceInformationDeleted':0,'cosmologyDecisions':0,'wholeGameComplete':False}
 candidate['frozenOriginalGodsAndCorrectedFollowup']=godContext;candidate['distinctClassFeatureComparison']=distinctSaint
 ck('71original god sources and64plane sources',len(godmembers)==71 and frozenCosmo['sourceCount']==64)
 root.mkdir();frozen=[]
 for b in sources.values():
  p=G/b['path'];ck('Current complete source '+b['path'],info(p)==b);dst=root/'sources'/b['path'];target=Path('\\\\?\\'+str(dst.resolve()));target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(p.read_bytes());ck('Frozen complete source '+b['path'],target.read_bytes()==p.read_bytes());frozen.append({**b,'frozenCopy':dst.relative_to(G).as_posix()})
 for p,b in protected.items():ck('Protected authority unchanged '+p.name,p.read_bytes()==b)
 out.write_bytes(enc(candidate));check.write_bytes(enc({'candidate':info(out),'checks':checks,'checkCount':len(checks),'sourceCount':len(sources),'sourceIdentities':2,'placements':3,'questions':24,'originalFrozenCosmologySources':64,'riskCounts':{'C':2},'failures':0,'earlierCompleteProcedures':0,'newCurrentVectors':0,'validationScope':'Complete source/access/context preservation and preparation; not selected miracle/reality mechanics, runtime, balance or cosmology.'}))
 manifest=root/'MANIFEST.json';manifest.write_bytes(enc({'candidate':info(out),'check':info(check),'sources':list(sources.values()),'frozenCopies':frozen,'nestedOriginalCosmology':frozenCosmo}))
 readme='Complete two-spell source conference. Preserve Greater Divine Intervention question/task miracle and Wish reality reshaping, all three placements and actual class schools.24choices remain unselected. Full original gods/planes archives and current scoped records included. No Saint-feature substitution, imported Wish safe list, punitive wording, stress chance or cap.50accepted-unapplied; canonical implementation reserved.\n';(root/'README.md').write_text(readme,encoding='utf-8',newline='\n')
 with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p,n in [(out,'CANDIDATE.json'),(check,'SOURCE_CHECK.json'),(manifest,'MANIFEST.json')]:z.write(p,n)
  z.writestr('README.md',readme)
  for b in sources.values():z.writestr('sources/'+b['path'],(G/b['path']).read_bytes())
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None and len(z.namelist())==len(set(z.namelist())) and z.read('CANDIDATE.json')==out.read_bytes()
  for b in sources.values():assert z.read('sources/'+b['path'])==(G/b['path']).read_bytes()
 ab=info(archive)
 request.write_text(f'Review {archive.name}, {ab["bytes"]} bytes SHA256 {ab["sha256"]}. Read both complete identities, all three placements,24unselected questions,14applied counterparts,7full classes,current scoped interfaces,full accepted-unapplied Rank7 context,71frozen original god/pantheon sources with corrected follow-up and64original plane sources. Preserve Greater Divine Intervention ONEquestion ORtask with Director-determined miracle and Wish as the most powerful reality-reshaping spell. Both rank9/class17/base26RP/Action/120feet/V-S-F/CoreInstantaneous. Greater is Cleric/Wizard Divination; Wish is ClericUniversal and Druid/Mage/WizardTransmutation. The Saint Reaction4RP/1longrest feature is distinct. Define concrete useful request/outcome procedures,real target/source/state/clock/resource transactions,information boundaries,persistence and failure handling without an imported Wish copylist,rank8limit,stresschance,goldcap or monkey-paw penalty. Missing limits and powers are NEW scoped authorship. Functioning faith is not proof of cosmic genealogy. Keep actual Hunt/Null/death/owner/Q6 and conditional holds; pending other cohorts are not authority. Return full reasoning,24dispositions,complete procedures,at least2positive encounters per spell covering question/task and multiple substantive Wish changes,fullstate branches and one cross-source case,exact reversible operations and preserved complete history.50accepted-unapplied;applied525/323/249/173;owner reserves implementation. PreparedUNSENT; no runtime,balance,cosmology orreleaseapproval.\n',encoding='utf-8',newline='\n')
 prep.write_bytes(enc({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PREPARED_UNSENT','candidate':info(out),'archive':ab,'manifest':info(manifest),'check':info(check),'request':info(request),'sourceCount':len(sources),'frozenOriginalCosmologySourceCount':64,'identityCount':2,'placementCount':3,'questionCount':24,'interfaceCount':len(inherited),'riskCounts':{'C':2},'allArchiveMembersVerified':True,'newRuleAdoptions':0,'sourceInformationDeleted':0}))
 print(json.dumps({'preparation':info(prep),'candidate':info(out),'archive':ab,'sources':len(sources),'checks':len(checks),'questions':24,'interfaces':len(inherited),'failures':0}))
if __name__=='__main__':main()
