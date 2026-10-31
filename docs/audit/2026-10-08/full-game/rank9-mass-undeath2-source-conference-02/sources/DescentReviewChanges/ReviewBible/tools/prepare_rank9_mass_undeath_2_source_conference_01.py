"""Preserve two complete mass-undeath sources and source-linked unselected choices."""
from pathlib import Path
from datetime import datetime,timezone
from copy import deepcopy
import hashlib,json,zipfile
from prepare_rank9_alignment_faction_purification_5_source_conference_01 import G,R,A,read,enc,info,at
from rank9_mass_undeath_2_questions_01 import IDS,TIERS,Q,FINDINGS,CASES
def main():
 stem='RANK9_MASS_UNDEATH_2_SOURCE_CONFERENCE_01';root=A/'rank9-mass-undeath2-source-conference-01';out=R/'data/director/spell_review/rank9_mass_undeath_2_source_conference_01.json'
 check,prep,request=[A/(stem+s) for s in ['_CHECK.json','_PREPARATION.json','_REQUEST.txt']];archive=A/'DD_Rank9_Mass_Undeath_2_Source_Conference_01.zip'
 assert not any(p.exists() for p in [root,out,check,prep,request,archive])
 sources={};checks=[]
 def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
 def bind(p):b=info(p);sources[b['path']]=b;return b
 cpfile=A/'ACTIVE_AUTHORING_CHECKPOINT_ALIGNMENT_FACTION_RANK7_RECOVERY_77.json';cp=read(cpfile)
 catp=R/'data/public/spell_playtests/catalog.json';ip=catp.parent/'authored_review_index.json';qp=R/'data/director/spell_review/remaining_work_queue_64.json';regp=qp.parent/'accepted_interface_registry_06.json'
 cov=R/'data/playtest/game_development_coverage.json';ledger=A/'PERTINENT_GPT_DECISIONS_2026_10_20_02.json'
 catalog,index,queue,registry=map(read,[catp,ip,qp,regp]);protected={p:p.read_bytes() for p in [catp,ip,qp,regp,cpfile,cov,ledger]}
 for b in cp['canonicalHelperBaselinesUnchanged']:
  p=G/b['path'];ck('Current helper '+b['path'],info(p)==b);protected[p]=p.read_bytes();bind(p)
 ck('Exact checkpoint77',info(cpfile)['sha256']=='14801b3040adb0f60da1d599262747d62cc47106c5d5f8e56880589446ca6a32')
 ck('Exact queue64',info(qp)==cp['currentWorkQueue'])
 ck('45accepted remain unapplied',cp['acceptedButUnapplied']==45 and queue['acceptedButUnappliedTotalCurrent']==45 and not cp['implementationApplied'])
 ck('Current applied coverage',index['authoredCounts']=={'reviewed':525,'pending':323} and index['representationCounts']['completeReviewedStandaloneProcedures']==249 and len(registry['entries'])==173)
 for p in [catp,ip,qp,regp,cpfile,cov,ledger,Path(__file__),Path(__file__).with_name('rank9_mass_undeath_2_questions_01.py'),Path(__file__).with_name('prepare_rank9_alignment_faction_purification_5_source_conference_01.py'),Path(__file__).with_name('rank9_alignment_faction_purification_5_questions_01.py'),G/'CANON_MANIFEST.md',G/'docs/canon/CANON_MANIFEST.json',G/'docs/canon/REPOSITORY_PROMOTION.md',A/'GPT_PART5_PERTINENT_OWNER_CHOICES_2026_10_20_NATIVE.json',A/'GPT_PART5_STATUS_SYNC_15_NATIVE.json',G/'docs/audit/2026-10-20/github-snapshot-material-forging72/PUSH_RECEIPT.json',R/'rulebook_output.txt',G/'docs/reference/Player_Rulebook_v6_source_text.txt',R/'books/player/Decennium_Descent_Player_Rulebook_v6.docx']:bind(p)
 lines=(R/'rulebook_output.txt').read_text('utf-16').splitlines();reference=(G/'docs/reference/Player_Rulebook_v6_source_text.txt').read_text('utf-8').splitlines();records=[]
 priorp=A/'NECROMANCY_RANK9_SOURCE_PREPARATION.json';bind(priorp);prior=read(priorp)
 for sid in IDS:
  n=next(i for i,x in enumerate(prior['selectedSpells']) if x['spellId']==sid);hist=prior['selectedSpells'][n];card=next(x for x in catalog['spells'] if x['id']==sid);row=next(x for x in queue['rows'] if x['id']==sid);entry=next(x for x in index['entries'] if x['id']==sid)
  ck('Exact full source/current/history '+sid,hist['fullSourceAndCurrentAccessRecord']==card==row['completeCurrentSourceAndAccess'])
  ck('Actually ungrouped pending '+sid,row['currentGroup'] is None and not row['previousAuthoringMapRowUnchanged']['completeEarlierProposalRecords'] and entry['authoredStatus']=='pending-authored-procedure')
  ck('Exact actual access '+sid,card['classAccess']=={c:{'rank':9,'minimumClassLevel':17,'school':'Necromancy','baseRpCost':26} for c in ['Cleric','Druid','Wizard']})
  core=card['source']['coreEntries'];duration,components=('Until dispelled','V, S, F') if sid==IDS[0] else ('Concentration, up to 1 minute','V, S, M/F')
  ck('Exact individual Core metadata '+sid,len(core)==1 and core[0]['original']['casting_time']=='1 action' and core[0]['original']['range']=='120 feet' and core[0]['original']['duration']==duration and core[0]['original']['components']==components and core[0]['original']['rp_cost']==26)
  books=[deepcopy(b) for b in prior['currentBookBindings'] if b['spellId']==sid];ck('One complete native placement '+sid,len(books)==len(card['source']['original']['placements'])==1)
  for b in books:
   k=b['currentBookRow']['line']-1;ck('Both exact manuscripts '+sid,lines[k]==reference[k]==b['currentBookRow']['exactText'])
  for kind in ['catalog','core']:ck('Exact underlying source '+sid+kind,bind(R/card['source'][kind+'Path'])['sha256']==card['source'][kind+'Sha256'])
  records.append({'spellId':sid,'riskTier':TIERS[sid][0],'riskReason':TIERS[sid][1],'completeCurrentCatalogSourceAndAccess':deepcopy(card),'currentIndexEntry':deepcopy(entry),'originalQuestionSource':info(priorp),'originalQuestionPointer':'/selectedSpells/'+str(n),'completeOriginalSourceQuestionUnchanged':deepcopy(hist),'completeHistoricalCommonQuestionUnchanged':prior['commonOperationalQuestion'],'completeHistoricalScopeExceptionUnchanged':prior['commonQuestionException'],'completeCurrentBookBindings':books,'earlierCompleteProcedures':[],'earlierOperationalWorkedCases':[],'status':'Source conference prepared; no selected procedure or executable vectors.'})
 mechanics=['VIDEO_GAME_ONLY_DIRECTIVE.md','CLASS_PLAYTEST_RULES.md','SPELL_INTEGRATION_RULES.md','COMBAT_ACTION_PLAYTEST.md','CORE_RESOLUTION_PLAYTEST.md','CONDITIONS_PLAYTEST.md','CONDITION_RECOVERY_PLAYTEST.md','CONTROL_STATES_PLAYTEST.md','BODY_EQUIPMENT_PLAYTEST.md','CREATURE_LIFECYCLE_PLAYTEST.md','CREATURE_LIFECYCLE_SOURCE_BINDINGS.md','MAXIMUM_HP_PLAYTEST.md','HEALING_DEATH_PLAYTEST.md','TRANSFORMATION_SPELL_PLAYTEST.md','RESONANCE_CANON.md','COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md','CHARACTER_CREATION_PLAYTEST.md','CHARACTER_FOUNDATION_TABLES.md','XP_ADVANCEMENT_CANON.md','STRAIN_PLAYTEST.md','CUSTOM_CONDITION_BINDINGS.md','CONTROL_SOURCE_BINDINGS.md','EQUIPMENT_ITEM_PROCEDURES.md','EQUIPMENT_ACQUISITION_PLAYTEST.md','WORLD_DUNGEON_LOOP.md','EXPEDITION_STRUCTURE_CANON.md']
 for name in mechanics:bind(R/'docs/mechanics'/name)
 for name in ['data/playtest/creature_lifecycle_bindings.json','data/playtest/control_state_bindings.json','data/playtest/condition_playtests.json','data/playtest/equipment_acquisition_candidate.json','data/playtest/equipment_source_catalog.json','src/data/resonance-economy.js','data/director/bestiary_source_candidate_internal.json','data/playtest/bestiary_public_source_candidate.json','data/public/feat_candidates/exact_01/candidate.json','data/public/feat_candidates/exact_01/shared_rules.json','data/public/feat_candidates/exact_01/supplements.json']:bind(R/name)
 classSources=[{'source':bind(R/('data/public/class_playtests/'+n+'.json')),'qualification':'Complete class engine,all stages,actual acquisition and source-qualified native profiles; no imported access,cap,scaling or feature merely from a shared name.'} for n in ['cleric','druid','wizard','mage','paladin','ranger','mirrorsage','oracle']]
 inherited=[];nums=list(range(12))+[13,14,21,23,24,25,26,31,36,39,40,48,49,50,51,52,53,83,85,130,141]
 ck('Unique interface pointers',len(nums)==len(set(nums)))
 for n in nums:
  e=registry['entries'][n];b=e['currentAuthoritativeSource'];actual=bind(G/b['path']);ck('Exact interface source '+str(n),all(actual[k]==b[k] for k in ['bytes','sha256']))
  inherited.append({'registryPointer':'/entries/'+str(n),'completeEntryUnchanged':deepcopy(e),'scopeLimit':'Retain actual source scope. New mass-body creation/control/lifecycle rules need named extension; finite-summon disappearance is not automatically permanent-animation law.'})
 counterparts=[]
 for sid in ['animate-dead','corpse-puppet','corpse-light','speak-with-dead','resurrection','true-resurrection','mass-resurrection-denial','antimagic-field-lesser','greater-dispel','death-ward','death-tide']:
  e=next(x for x in index['entries'] if x['id']==sid);ck('Applied counterpart '+sid,e['authoredStatus']=='reviewed-authored-operational-playtest');p=(ip.parent/e['procedureFile']).resolve();d=read(p);ptr=e.get('wholeCardPointer') or e['procedurePointer'];b=bind(p)
  if e.get('completeEnvelopeBinding'):ck('Exact counterpart envelope '+sid,b==e['completeEnvelopeBinding'])
  if e.get('authoredAcceptanceReceipt'):ck('Exact acceptance '+sid,bind(G/e['authoredAcceptanceReceipt']['path'])==e['authoredAcceptanceReceipt'])
  card=deepcopy(at(d,ptr))
  for k in ['operational','operationalCandidate']:
   op=card.get(k)
   if isinstance(op,dict):
    for rel in op.get('sourceReview',[])+op.get('reviewEvidence',[]):bind(G/rel)
    if op.get('authoringFile'):bind(R/op['authoringFile'])
  for rel in e.get('caseSourceReferenceAliases',{}).values():bind(G/rel)
  counterparts.append({'spellId':sid,'source':b,'pointer':ptr,'completeCurrentCard':card,'completeSharedRules':deepcopy(at(d,e['sharedRulesPointer']) if e.get('sharedRulesPointer') else d.get('sharedRules',{})),'indexEntry':deepcopy(e),'qualification':'Applied authored comparison in its exact scope; no automatic new mass-animation quantities or runtime proof.'})
 addp=A/'RANK6_UNDEAD_PROFILE_SOURCE_ADDENDUM.json';add=read(addp);bind(addp);bind(A/'RANK6_UNDEAD_PROFILE_SOURCE_ADDENDUM.md');bind(A/add['basePreparation'])
 for rel in add['protectedFiles']:bind(G/rel)
 bestp=G/'src/bestiary_data_full.json';best=read(bestp);monsters=[]
 for old in add['completeMatches']:ck('Original addendum record retained '+old['searchedName'],read(G/old['file'])[old['index']]==old['fullOriginalRecord'])
 for name,expected in [('Skeleton',('Huge','15',494)),('Zombie',('Gargantuan','26',1030))]:
  matches=[(i,x) for i,x in enumerate(best) if x['name']==name];ck('One actual historical '+name,len(matches)==1);i,x=matches[0];ck('Exact extreme profile '+name,(x['size'],x['challengeRating'],x['hitPoints'])==expected);monsters.append({'source':info(bestp),'pointer':'/'+str(i),'completeOriginalRecord':deepcopy(x),'qualification':'Unreviewed historical monster comparison only; name is not approval for minion creation,CR,loot or automatic profile adoption.'})
 acceptedRoot=A/'companion-life10-exact05-part5-return-01';acceptp=acceptedRoot/'ACCEPTANCE.json';accept=read(acceptp);bind(acceptp);acceptedArtifacts=[]
 for b in accept['exactAcceptedArtifacts']:
  p=acceptedRoot/'accepted'/b['archivePath'];v=bind(p);ck('Exact accepted Companion artifact '+b['filename'],v['bytes']==b['bytes'] and v['sha256']==b['sha256']);acceptedArtifacts.append(v)
 acceptedInputs=[]
 for b in accept['inputArchives']:
  p=A/b['filename'];v=bind(p);ck('Exact full Companion input '+b['filename'],v['bytes']==b['bytes'] and v['sha256']==b['sha256']);acceptedInputs.append(v)
 cpmodel=acceptedRoot/'accepted/current/SPELLS_MODEL.json';comp=read(cpmodel);companionComparisons=[]
 for sid in ['danse-macabre','create-undead','command-undeath','negative-energy-flood','summon-corpse-golem','summon-death-knight','summon-soul-wraith']:
  i=next(i for i,s in enumerate(comp['spells']) if s['id']==sid);companionComparisons.append({'spellId':sid,'source':info(cpmodel),'pointer':'/spells/'+str(i),'completeCurrentCard':deepcopy(comp['spells'][i]),'completeSharedRules':deepcopy(comp['sharedRules']),'qualification':'Exactly accepted authored Companion05,not applied. Its source-local profiles and orders are comparisons;all exactCR2 holds remain.'})
 acceptedContext={'receipt':info(acceptp),'completeReceipt':accept,'fullEightAcceptedArtifacts':acceptedArtifacts,'completeOriginalInputArchives':acceptedInputs,'completeRelevantCompanionComparisons':companionComparisons,'noNewAcceptanceClaimed':True}
 pending=[{'spellId':sid,'completeSourceAndCurrentQueueRow':deepcopy(next(x for x in queue['rows'] if x['id']==sid)),'qualification':'Pending source/status comparison only;not accepted positive-case authority.'} for sid in ['finger-of-death','clone']]
 context={}
 for rel in ['RANK8_DAMAGE6_PART5_EXACT_AUTHORING_ACCEPTANCE_75.json','rank8-damage6-part5-cast-history-return-03/MODEL.json','rank8-damage6-part5-cast-history-return-03/HOLD_REGISTER.json','copy-ready-preparation-only-part5-successor-01/POLICY_SELECTION.json','COPY_READY_PREPARATION_ONLY_PART5_01_LOCAL_PREFLIGHT.json','copy-ready-preparation-only-part5-successor-01/successor/CONTROL15_READY_REFERENCE_SUCCESSOR14.json','CONTROL15_PART5_FULL_RETURN_02_LOCAL_RECEIPT.json','RANK7_EXACT_MODEL_RECOVERY_77.json','GPT_PART5_RANK7_EXACT_MODEL_RECOVERY_77_DISPATCH_NATIVE.json','UNITY_DEVELOPMENT_DIRECTIONS_INTAKE_75.json']:context[rel]=bind(A/rel)
 context['qualification']='Current45accepted-unapplied. Soul Pyre belongs to exact accepted-unapplied Rank8six;its corpse-use predicate remains source-specific. Rank7 exact recovered MODEL is pending full artifact recovery and independent acceptance. No canonical implementation or Unity engine/cadence selected.'
 for name in ['CURRENT_COSMOLOGY_READ_FIRST.md','EPILOGUE_RELIC_NULL_REVIEWED_01.md','SOULS_RESEARCH_REVIEWED_01.md']:bind(R/'docs/director-only/cosmology'/name)
 for name in ['epilogue_relic_null_reviewed_01.json','souls_research_reviewed_01.json']:bind(R/'data/director/cosmology'/name)
 questions=[{'id':i,'spellIds':ids,'exactSourceOrConflict':s,'options':opts,'recommendationAndConsequences':rec,'decisionSelected':False} for i,ids,s,opts,rec in Q]
 ck('24unique unselected questions',len(questions)==len({q['id'] for q in questions})==24 and not any(q['decisionSelected'] for q in questions))
 ck('Exactly2identities and placements',set().union(*(set(q['spellIds']) for q in questions))==set(IDS) and len(records)==2 and sum(len(x['completeCurrentBookBindings']) for x in records)==2)
 ck('Complete comparisons',len(counterparts)==11 and len(companionComparisons)==7 and len(acceptedArtifacts)==8 and len(acceptedInputs)==2)
 candidate={'id':'RANK9-MASS-UNDEATH2-SOURCE-CONFERENCE01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'SOURCE_CONFERENCE_PREPARED_UNSENT','developmentDirection':'video-game-only','records':records,'historicalWorkflowQualification':'Old pre-push source wording and labels retained as history;current checkpoint77 and latest exact acceptances govern status. No new cosmology selected.','currentAcceptedInterfaceComparisons':inherited,'completeAppliedCounterparts':counterparts,'completeClassSources':classSources,'historicalUndeadProfileAddendum':{'source':info(addp),'completeOriginalAddendum':add,'currentExactSkeletonZombieComparisons':monsters},'acceptedButUnappliedCompanionContext':acceptedContext,'pendingComparisonsNotAuthority':pending,'laterCompleteReviewContext':context,'questions':questions,'riskCounts':{'C':2},'sourceFindings':FINDINGS,'futureCaseRequirements':CASES,'semanticDelta':[{'spellId':sid,'riskTier':'C','riskReason':TIERS[sid][1],'startingPoint':'Complete native source and historical question;no authored procedure or cases.','genuineQuestionIds':[q['id'] for q in questions if sid in q['spellIds']]} for sid in IDS],'earlierOperationalWorkedCases':[],'currentVectors':[],'countsUnchanged':deepcopy(index['authoredCounts']),'sourceBindings':list(sources.values()),'newRuleAdoptions':0,'runtimeTestsExecuted':0,'humanPlaytests':0,'sourceInformationDeleted':0,'cosmologyDecisions':0,'wholeGameComplete':False}
 root.mkdir();frozen=[]
 for b in sources.values():
  p=G/b['path'];ck('Current complete source '+b['path'],info(p)==b);dst=root/'sources'/b['path'];target=Path('\\\\?\\'+str(dst.resolve()));target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(p.read_bytes());ck('Frozen complete source '+b['path'],target.read_bytes()==p.read_bytes());frozen.append({**b,'frozenCopy':dst.relative_to(G).as_posix()})
 for p,b in protected.items():ck('Protected authority unchanged '+p.name,p.read_bytes()==b)
 out.write_bytes(enc(candidate));check.write_bytes(enc({'candidate':info(out),'checks':checks,'checkCount':len(checks),'sourceCount':len(sources),'sourceIdentities':2,'placements':2,'questions':24,'riskCounts':{'C':2},'failures':0,'earlierCompleteProcedures':0,'newCurrentVectors':0,'validationScope':'Complete source/access/context preservation and preparation;not selected semantics,runtime or mass-animation balance.'}))
 manifest=root/'MANIFEST.json';manifest.write_bytes(enc({'candidate':info(out),'check':info(check),'files':list(sources.values()),'frozenSources':frozen,'sourceCount':len(sources),'newRuleAdoptions':0}))
 readme='Two complete rank9 mass-undeath identities/placements;24unselected questions;11applied comparisons;7complete accepted-unapplied Companion comparisons with8exact artifacts and2full original input archives;8complete class sources. Preserve8permanent controlled skeletons/zombies andALLcorpses in1mile. Historical extreme Skeleton/Zombie are unreviewed comparisons. No selected procedure,runtime,balance,cosmology,implementation or release approval.\n';(root/'README.md').write_text(readme,encoding='utf-8',newline='\n')
 with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p,n in [(out,'CANDIDATE.json'),(check,'SOURCE_CHECK.json'),(manifest,'MANIFEST.json')]:z.write(p,n)
  z.writestr('README.md',readme)
  for b in sources.values():z.writestr('sources/'+b['path'],(G/b['path']).read_bytes())
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None and len(z.namelist())==len(set(z.namelist())) and z.read('CANDIDATE.json')==out.read_bytes()
  for b in sources.values():assert z.read('sources/'+b['path'])==(G/b['path']).read_bytes()
 ab=info(archive)
 request.write_text(f'Review {archive.name},{ab["bytes"]}bytes SHA256{ab["sha256"]}. Read both complete identities/placements,24unselected questions,11applied comparisons,all8exact Companion05artifacts and2full original input archives,seven relevant complete Companion procedures,eight class sources,exact historical monster/addendum evidence and current scoped contracts. Preserve Field8skeletons/zombies under permanent control andUntilDispelled; preserve Plague ALLcorpses in1mile,range120ft,concentration1minute,M-or-F. Both Cleric/Druid/Wizard Necromancy rank9,class17,base26RP. Historical SkeletonHugeCR15/494HP andZombieGargantuanCR26/1030HP are not ordinary minion authority. Explicitly select complete useful profiles,real corpse/anatomy/provenance,geometry,target admission,mass commands/scheduling,animation-versus-control duration,capacity/recasting,Null/healing/suppression and permanent outcomes. No arbitrary count cap or tabletop convenience restriction; no new soul/afterlife doctrine,CRcertification,donor-resource inheritance,loot duplication or silent class-profile borrowing. Keep existing exactCR2andotherwhole-case holds separate from these two positive procedures. Supply full reasoning,24dispositions,complete procedures,at least2positive encounters each including8distinct Field bodies andmorethan8Plague corpses,full individual states/branches andonecross-sourcecase,exact reversible operations andcomplete current artifacts. Recommendations remain unselected. Applied525/323/249/173;45accepted-unapplied;owner reserves implementation. Rank7recovery is separate. PreparedUNSENT until actually submitted; no runtime,balance,cosmology orreleaseapproval.\n',encoding='utf-8',newline='\n')
 prep.write_bytes(enc({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PREPARED_UNSENT','candidate':info(out),'archive':ab,'manifest':info(manifest),'check':info(check),'request':info(request),'sourceCount':len(sources),'identityCount':2,'placementCount':2,'questionCount':24,'riskCounts':{'C':2},'allArchiveMembersVerified':True,'newRuleAdoptions':0,'sourceInformationDeleted':0}))
 print(json.dumps({'preparation':info(prep),'candidate':info(out),'archive':ab,'sources':len(sources),'checks':len(checks),'questions':24,'interfaces':len(inherited),'failures':0}))
if __name__=='__main__':main()
