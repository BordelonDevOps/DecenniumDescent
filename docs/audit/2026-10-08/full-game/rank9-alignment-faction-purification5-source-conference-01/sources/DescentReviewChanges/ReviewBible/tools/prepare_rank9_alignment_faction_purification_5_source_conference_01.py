"""Freeze five full sources, scoped comparisons and unselected questions without applying rules."""
from pathlib import Path
from datetime import datetime,timezone
from copy import deepcopy
import hashlib,json,zipfile
from rank9_alignment_faction_purification_5_questions_01 import IDS,TIERS,Q,FINDINGS,CASES
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_bytes())
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def at(d,ptr):
 for k in ptr.strip('/').split('/') if ptr else []:
  k=k.replace('~1','/').replace('~0','~');d=d[int(k)] if isinstance(d,list) else d[k]
 return d
def main():
 stem='RANK9_ALIGNMENT_FACTION_PURIFICATION_5_SOURCE_CONFERENCE_01';root=A/'rank9-alignment-faction-purification5-source-conference-01'
 out=R/'data/director/spell_review/rank9_alignment_faction_purification_5_source_conference_01.json'
 check,prep,request=[A/(stem+s) for s in ['_CHECK.json','_PREPARATION.json','_REQUEST.txt']]
 archive=A/'DD_Rank9_Alignment_Faction_Purification_5_Source_Conference_01.zip'
 assert not any(p.exists() for p in [root,out,check,prep,request,archive])
 sources={};checks=[]
 def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
 def bind(p):
  b=info(p);sources[b['path']]=b;return b
 cpfile=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_RESONANCE_FIELDS_76.json';cp=read(cpfile)
 catp=R/'data/public/spell_playtests/catalog.json';ip=catp.parent/'authored_review_index.json'
 qp=R/'data/director/spell_review/remaining_work_queue_63.json';regp=qp.parent/'accepted_interface_registry_06.json'
 cov=R/'data/playtest/game_development_coverage.json';ledger=A/'PERTINENT_GPT_DECISIONS_2026_10_20_02.json'
 catalog,index,queue,registry=map(read,[catp,ip,qp,regp]);protected={p:p.read_bytes() for p in [catp,ip,qp,regp,cpfile,cov,ledger]}
 for b in cp['canonicalHelperBaselinesUnchanged']:
  p=G/b['path'];ck('Current helper '+b['path'],info(p)==b);protected[p]=p.read_bytes();bind(p)
 ck('Exact checkpoint76',info(cpfile)['sha256']=='c226a0a550c84d9c5fc934121ad53648a93d59e5b7d4d25137685695d79b08d9')
 ck('Exact queue63',info(qp)==cp['currentWorkQueue'])
 ck('45accepted remain unapplied',cp['acceptedButUnapplied']==45 and queue['acceptedButUnappliedTotalCurrent']==45 and not cp['implementationApplied'])
 ck('Actual applied baseline',index['authoredCounts']=={'reviewed':525,'pending':323} and index['representationCounts']['completeReviewedStandaloneProcedures']==249 and len(registry['entries'])==173)
 for p in [catp,ip,qp,regp,cpfile,cov,ledger,Path(__file__),Path(__file__).with_name('rank9_alignment_faction_purification_5_questions_01.py'),G/'CANON_MANIFEST.md',G/'docs/canon/CANON_MANIFEST.json',G/'docs/canon/REPOSITORY_PROMOTION.md',A/'GPT_PART5_PERTINENT_OWNER_CHOICES_2026_10_20_NATIVE.json',A/'GPT_PART5_STATUS_SYNC_15_NATIVE.json',G/'docs/audit/2026-10-20/github-snapshot-material-forging72/PUSH_RECEIPT.json',R/'rulebook_output.txt',G/'docs/reference/Player_Rulebook_v6_source_text.txt',R/'books/player/Decennium_Descent_Player_Rulebook_v6.docx']:bind(p)
 lines=(R/'rulebook_output.txt').read_text('utf-16').splitlines();reference=(G/'docs/reference/Player_Rulebook_v6_source_text.txt').read_text('utf-8').splitlines();records=[]
 for sid in IDS:
  priorp=A/(('CONJURATION' if sid in ['alignment-ascension','faction-incarnate'] else 'ABJURATION')+'_RANK9_SOURCE_PREPARATION.json');bind(priorp);prior=read(priorp)
  n=next(i for i,x in enumerate(prior['selectedSpells']) if x['spellId']==sid);hist=prior['selectedSpells'][n]
  card=next(x for x in catalog['spells'] if x['id']==sid);row=next(x for x in queue['rows'] if x['id']==sid);entry=next(x for x in index['entries'] if x['id']==sid)
  ck('Full source/current/history equality '+sid,hist['fullSourceAndCurrentAccessRecord']==card==row['completeCurrentSourceAndAccess'])
  ck('Actual ungrouped pending identity '+sid,row['currentGroup'] is None and not row['previousAuthoringMapRowUnchanged']['completeEarlierProposalRecords'] and entry['authoredStatus']=='pending-authored-procedure')
  classes=['Druid','Mage','Wizard'] if sid=='faction-incarnate' else ['Cleric','Druid','Mage','Wizard']
  access={c:{'rank':9,'minimumClassLevel':17,'school':('Divination' if c=='Cleric' else 'Conjuration') if sid=='alignment-ascension' else ('Conjuration' if sid=='faction-incarnate' else 'Abjuration'),'baseRpCost':26} for c in classes}
  ck('Exact native access '+sid,card['classAccess']==access)
  placements=2 if sid=='alignment-ascension' else 1;duration={'faction-incarnate':'Concentration, up to 1 minute','corruption-purification':'Until dispelled'}.get(sid,'Instantaneous')
  ck('Exact Core casting/duration '+sid,len(card['source']['coreEntries'])==placements and all(e['original']['casting_time']=='1 action' and e['original']['range']=='120 feet' and e['original']['components']=='V, S, F' and e['original']['duration']==duration and e['original']['rp_cost']==26 for e in card['source']['coreEntries']))
  books=[deepcopy(b) for b in prior['currentBookBindings'] if b['spellId']==sid]
  ck('Every original book placement '+sid,len(books)==len(card['source']['original']['placements'])==placements)
  for b in books:
   k=b['currentBookRow']['line']-1;ck('Two actual manuscript rows '+sid+b['catalogPlacement']['school'],lines[k]==reference[k]==b['currentBookRow']['exactText'])
  for kind in ['catalog','core']:ck('Exact underlying '+kind+' '+sid,bind(R/card['source'][kind+'Path'])['sha256']==card['source'][kind+'Sha256'])
  records.append({'spellId':sid,'riskTier':TIERS[sid][0],'riskReason':TIERS[sid][1],'completeCurrentCatalogSourceAndAccess':deepcopy(card),'currentIndexEntry':deepcopy(entry),'originalQuestionSource':info(priorp),'originalQuestionPointer':'/selectedSpells/'+str(n),'completeOriginalSourceQuestionUnchanged':deepcopy(hist),'completeHistoricalCommonQuestionUnchanged':prior['commonOperationalQuestion'],'completeHistoricalScopeExceptionUnchanged':prior['commonQuestionException'],'completeCurrentBookBindings':books,'earlierCompleteProcedures':[],'earlierOperationalWorkedCases':[],'status':'Prepared source questions only; no selected procedure or executable vectors.'})
 mechanics=['VIDEO_GAME_ONLY_DIRECTIVE.md','CLASS_PLAYTEST_RULES.md','SPELL_INTEGRATION_RULES.md','COMBAT_ACTION_PLAYTEST.md','CORE_RESOLUTION_PLAYTEST.md','CONDITIONS_PLAYTEST.md','CONDITION_RECOVERY_PLAYTEST.md','CONTROL_STATES_PLAYTEST.md','BODY_EQUIPMENT_PLAYTEST.md','CREATURE_LIFECYCLE_PLAYTEST.md','HEALING_DEATH_PLAYTEST.md','TRANSFORMATION_SPELL_PLAYTEST.md','RESONANCE_CANON.md','COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md','CHARACTER_CREATION_PLAYTEST.md','CHARACTER_FOUNDATION_TABLES.md','XP_ADVANCEMENT_CANON.md','STRAIN_PLAYTEST.md','CUSTOM_CONDITION_BINDINGS.md','CONTROL_SOURCE_BINDINGS.md','EQUIPMENT_ITEM_PROCEDURES.md','EQUIPMENT_ACQUISITION_PLAYTEST.md','WORLD_DUNGEON_LOOP.md','EXPEDITION_STRUCTURE_CANON.md','REPUTATION.md','expedition/SOCIAL_SCENARIO_WALKTHROUGHS.md','expedition/SOCIAL_SCENARIO_RECORDS.md']
 for name in mechanics:bind(R/'docs/mechanics'/name)
 for name in ['data/playtest/control_state_bindings.json','data/playtest/condition_playtests.json','data/playtest/equipment_acquisition_candidate.json','data/playtest/equipment_source_catalog.json','src/data/resonance-economy.js','src/data/reputation.js','src/lib/character-storage.js','data/public/feat_candidates/exact_01/candidate.json','data/public/feat_candidates/exact_01/shared_rules.json','data/public/feat_candidates/exact_01/supplements.json']:bind(R/name)
 rep=R/'docs/mechanics/REPUTATION.md';oldrep=G/'docs/mechanics/REPUTATION.md';bind(oldrep)
 reptext=rep.read_text('utf-8');helper=(R/'src/data/reputation.js').read_text('utf-8')
 ck('Current scale+3', '**+3 (Honored)**' in reptext and 'Math.max(-3, Math.min(3, Math.round(Number(score) || 0)))' in helper)
 repContext={'currentGuidance':info(rep),'completeCurrentGuidance':reptext,'historicalConflictingGuidance':info(oldrep),'completeHistoricalConflictingGuidance':oldrep.read_text('utf-8'),'qualification':'Preserve both exact documents. Current ReviewBible guidance and existing scoped interfaces apply; root automatic reputation-to-RP/cost wording is conflicting history, not re-adopted. Current native maximum+3 is distinct from Honored tier threshold. Draft faction placeholders are not certified institutions.'}
 classSources=[]
 for name in ['wizard','mage','druid','cleric','paladin','oracle','mirrorsage']:
  p=R/('data/public/class_playtests/'+name+'.json');classSources.append({'source':bind(p),'qualification':'Complete existing class engine, all stages and selection/automatic acquisition. Paladin oaths and Oracle intrinsic Curse are comparisons, not new spell access or removable corruption by name.'})
 inherited=[];nums=list(range(12))+[13,14,20,21,23,24,25,26,28,29,30,31,36,39,40,49,50,51,52,53,69,76,77,97,98,99]
 ck('Unique interface pointers',len(nums)==len(set(nums)))
 for n in nums:
  e=registry['entries'][n];b=e['currentAuthoritativeSource'];actual=bind(G/b['path']);ck('Exact interface source '+str(n),all(actual[k]==b[k] for k in ['bytes','sha256']))
  inherited.append({'registryPointer':'/entries/'+str(n),'completeEntryUnchanged':deepcopy(e),'scopeLimit':'Preserve actual source scope. Alignment/faction/Corruption similarities do not create universal inheritance; all new cure/profile/benefit/information choices require explicit local authorship.'})
 counterparts=[]
 counterpartIds=['alignment-lock','alignment-anchor','alignment-purge','alignment-suggestion','alignment-nexus','alignment-revelation','alignment-forecast','corruption-cleanse','corruption-purge','corruption-ward','faction-seal','faction-ally','faction-champion','faction-army','faction-portal','faction-sanctuary','faction-insight','faction-divination','faction-secrets','faction-omniscience','alignment-portal']
 for sid in counterpartIds:
  e=next(x for x in index['entries'] if x['id']==sid);ck('Applied counterpart '+sid,e['authoredStatus']=='reviewed-authored-operational-playtest')
  p=(ip.parent/e['procedureFile']).resolve();d=read(p);ptr=e.get('wholeCardPointer') or e['procedurePointer'];b=bind(p)
  if e.get('completeEnvelopeBinding'):ck('Exact counterpart envelope '+sid,b==e['completeEnvelopeBinding'])
  if e.get('authoredAcceptanceReceipt'):ck('Exact acceptance '+sid,bind(G/e['authoredAcceptanceReceipt']['path'])==e['authoredAcceptanceReceipt'])
  card=deepcopy(at(d,ptr))
  for key in ['operational','operationalCandidate']:
   op=card.get(key)
   if isinstance(op,dict):
    for rel in op.get('sourceReview',[])+op.get('reviewEvidence',[]):bind(G/rel)
    if op.get('authoringFile'):bind(R/op['authoringFile'])
  for rel in e.get('caseSourceReferenceAliases',{}).values():bind(G/rel)
  profiles={k:deepcopy(v) for k,v in d.items() if 'profile' in k.lower()}
  counterparts.append({'spellId':sid,'source':b,'pointer':ptr,'completeCurrentCard':card,'completeSharedRules':deepcopy(at(d,e['sharedRulesPointer']) if e.get('sharedRulesPointer') else d.get('sharedRules',{})),'completeSupportingProfiles':profiles,'indexEntry':deepcopy(e),'qualification':'Applied authored comparison in its exact scope; no runtime claim and no automatic limitation of the rank9 native promise to a lower-rank version.'})
 pending=[]
 for sid in ['alignment-avatar','faction-paragon','corruption-immunity','alignment-immunity','faction-aegis','faction-citadel']:
  row=next(x for x in queue['rows'] if x['id']==sid);pending.append({'spellId':sid,'completeSourceAndCurrentQueueRow':deepcopy(row),'qualification':'Pending source/status comparison only, not an accepted operative procedure or positive-case authority.'})
 context={}
 for rel in ['rank7-identity-casting5-part5-correction-return-02/context/COMPANION05_MODEL.json','rank7-identity-casting5-part5-correction-return-02/context/COMPANION05_ACCEPTANCE.json','copy-ready-preparation-only-part5-successor-01/POLICY_SELECTION.json','COPY_READY_PREPARATION_ONLY_PART5_01_LOCAL_PREFLIGHT.json','copy-ready-preparation-only-part5-successor-01/successor/CONTROL15_READY_REFERENCE_SUCCESSOR14.json','CONTROL15_PART5_FULL_RETURN_02_LOCAL_RECEIPT.json','RANK8_DAMAGE6_PART5_EXACT_AUTHORING_ACCEPTANCE_75.json','RANK7_READY_DEADLINE_RETURN_03_AVAILABLE_75.json','GPT_PART5_RANK7_READY_DEADLINE_RETURN_03_NATIVE.json','GPT_PART5_RANK7_EXACT_RETURN_UNAVAILABLE_77_NATIVE.json','RANK7_EXACT_MODEL_RECOVERY_77.json','GPT_PART5_RANK7_EXACT_MODEL_RECOVERY_77_DISPATCH_NATIVE.json','UNITY_DEVELOPMENT_DIRECTIONS_INTAKE_75.json','unity-development-directions-75/Decennium_Descent_Unity_Codex_Directions.md']:context[rel]=bind(A/rel)
 context['qualification']='45accepted-unapplied; canonical implementation reserved. Rank7 original Return03 archive unavailable in GPT session; exact reported MODEL reconstructed locally and separately submitted for complete artifact recovery, not accepted or applied. Unity direction does not select new cadence or implement an engine.'
 for name in ['CURRENT_COSMOLOGY_READ_FIRST.md','EPILOGUE_RELIC_NULL_REVIEWED_01.md','SOULS_RESEARCH_REVIEWED_01.md']:bind(R/'docs/director-only/cosmology'/name)
 for name in ['epilogue_relic_null_reviewed_01.json','souls_research_reviewed_01.json']:bind(R/'data/director/cosmology'/name)
 questions=[{'id':i,'spellIds':ids,'exactSourceOrConflict':s,'options':opts,'recommendationAndConsequences':rec,'decisionSelected':False} for i,ids,s,opts,rec in Q]
 ck('28unique unselected questions',len(questions)==len({q['id'] for q in questions})==28 and not any(q['decisionSelected'] for q in questions))
 ck('Exactly five identities',set().union(*(set(q['spellIds']) for q in questions))==set(IDS) and len(records)==5)
 ck('Six complete native placements',sum(len(x['completeCurrentBookBindings']) for x in records)==6)
 ck('21 full applied counterparts',len(counterparts)==21)
 candidate={'id':'RANK9-ALIGNMENT-FACTION-PURIFICATION5-SOURCE-CONFERENCE01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'SOURCE_CONFERENCE_PREPARED_UNSENT','developmentDirection':'video-game-only','records':records,'historicalWorkflowQualification':'Original pre-push/post-push wording remains exact history. Verified backup through72 exists. Current protected cosmology sources remain provisional source boundaries; no new metaphysics is selected.','currentAcceptedInterfaceComparisons':inherited,'completeAppliedCounterparts':counterparts,'completeClassSources':classSources,'reputationSourceConflict':repContext,'pendingComparisonsNotAuthority':pending,'laterCompleteReviewContext':context,'questions':questions,'riskCounts':{'C':5},'sourceFindings':FINDINGS,'futureCaseRequirements':CASES,'semanticDelta':[{'spellId':sid,'riskTier':'C','riskReason':TIERS[sid][1],'startingPoint':'Complete native source and historical question, no authored procedure/cases.','genuineQuestionIds':[q['id'] for q in questions if sid in q['spellIds']]} for sid in IDS],'earlierOperationalWorkedCases':[],'currentVectors':[],'countsUnchanged':deepcopy(index['authoredCounts']),'sourceBindings':list(sources.values()),'newRuleAdoptions':0,'runtimeTestsExecuted':0,'humanPlaytests':0,'sourceInformationDeleted':0,'cosmologyDecisions':0,'wholeGameComplete':False}
 root.mkdir();frozen=[]
 for b in sources.values():
  p=G/b['path'];ck('Current complete source '+b['path'],info(p)==b);dst=root/'sources'/b['path'];target=Path('\\\\?\\'+str(dst.resolve()));target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(p.read_bytes());ck('Frozen complete source '+b['path'],target.read_bytes()==p.read_bytes());frozen.append({**b,'frozenCopy':dst.relative_to(G).as_posix()})
 for p,b in protected.items():ck('Protected authority unchanged '+p.name,p.read_bytes()==b)
 out.write_bytes(enc(candidate));check.write_bytes(enc({'candidate':info(out),'checks':checks,'checkCount':len(checks),'sourceCount':len(sources),'sourceIdentities':5,'placements':6,'questions':28,'riskCounts':{'C':5},'failures':0,'earlierCompleteProcedures':0,'newCurrentVectors':0,'validationScope':'Full source/access/history/context preservation and preparation; no selected semantics or runtime testing.'}))
 manifest=root/'MANIFEST.json';manifest.write_bytes(enc({'candidate':info(out),'check':info(check),'files':list(sources.values()),'frozenSources':frozen,'sourceCount':len(sources),'newRuleAdoptions':0}))
 readme='Five complete rank9 identities,six placements,28unselected questions,21complete applied counterparts,seven complete class sources,and scoped current alignment/faction/Corruption/KT/PT/Null context. Current45accepted-unapplied;applied525/323/249/173 unchanged. Exact original history retained. No selected procedure,runtime,balance,cosmology,implementation or release approval.\n'
 (root/'README.md').write_text(readme,encoding='utf-8',newline='\n')
 with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p,n in [(out,'CANDIDATE.json'),(check,'SOURCE_CHECK.json'),(manifest,'MANIFEST.json')]:z.write(p,n)
  z.writestr('README.md',readme)
  for b in sources.values():z.writestr('sources/'+b['path'],(G/b['path']).read_bytes())
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None and len(z.namelist())==len(set(z.namelist())) and z.read('CANDIDATE.json')==out.read_bytes()
  for b in sources.values():assert z.read('sources/'+b['path'])==(G/b['path']).read_bytes()
 ab=info(archive)
 request.write_text(f'Review {archive.name}, {ab["bytes"]}bytes SHA256{ab["sha256"]}. Read all five complete identities/sixplacements,28unselected questions,21full applied counterparts,seven full class sources,current scoped interfaces and protected cosmology records. Preserve BOTH Ascension energy-form AND divine-insight placements with actual class school; Alignment Perfection purification and alignment-dependent benefits; Incarnate living faction embodiment with printed concentration1minute; Faction Perfection real maximum reputation and significant benefits; Corruption Purification permanent all-corruption removal despite Until dispelled metadata. Separate reputation+3 fromHonored+2,membership,permission,alliedStatus and historical deeds. Current ReviewBible guidance forbids automatic reputation-to-RP/cost modifiers; preserve the older conflicting root text as history. Distinguish ordinaryCorrupted,activeCorruption,numerictracks,KT/PTstages/symptoms,knowledge,NullVeil and actual removal protections. No hidden new cosmology follows from purity/avatar/embodiment/divine wording. Resolve genuine forks explicitly as NEW scoped authorship; recommendations are not selections. Provide complete procedures,all28dispositions,full state positive encounters and meaningful independent branches,one combined interaction,exact reversible operations and complete current artifacts. Preserve full source/history and conditional holds. Current45accepted-unapplied,applied525/323/249/173; owner reserves canonical implementation. Rank7 recovery is separate. PreparedUNSENT until actually submitted; no runtime,balance,cosmology or release approval.\n',encoding='utf-8',newline='\n')
 prep.write_bytes(enc({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PREPARED_UNSENT','candidate':info(out),'archive':ab,'manifest':info(manifest),'check':info(check),'request':info(request),'sourceCount':len(sources),'identityCount':5,'placementCount':6,'questionCount':28,'riskCounts':{'C':5},'allArchiveMembersVerified':True,'newRuleAdoptions':0,'sourceInformationDeleted':0}))
 print(json.dumps({'preparation':info(prep),'candidate':info(out),'archive':ab,'sources':len(sources),'checks':len(checks),'questions':28,'failures':0}))
if __name__=='__main__':main()
