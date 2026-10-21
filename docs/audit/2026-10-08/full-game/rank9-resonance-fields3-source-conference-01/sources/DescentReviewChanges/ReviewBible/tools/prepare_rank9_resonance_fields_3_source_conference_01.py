"""Freeze full source, accepted interfaces and unselected questions; apply no rules."""
from pathlib import Path
from datetime import datetime,timezone
from copy import deepcopy
import hashlib,json,zipfile
from rank9_resonance_fields_3_questions_01 import IDS,TIERS,Q,FINDINGS,CASES
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
 stem='RANK9_RESONANCE_FIELDS_3_SOURCE_CONFERENCE_01'
 root=A/'rank9-resonance-fields3-source-conference-01'
 out=R/'data/director/spell_review/rank9_resonance_fields_3_source_conference_01.json'
 check,prep,request=[A/(stem+s) for s in ['_CHECK.json','_PREPARATION.json','_REQUEST.txt']]
 archive=A/'DD_Rank9_Resonance_Fields_3_Source_Conference_01.zip'
 assert not any(p.exists() for p in [root,out,check,prep,request,archive])
 sources={};checks=[]
 def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
 def bind(p):
  b=info(p);sources[b['path']]=b;return b
 cpfile=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK8_ACCEPTANCE_UNITY_INTAKE_75.json';cp=read(cpfile)
 catp=R/'data/public/spell_playtests/catalog.json';ip=catp.parent/'authored_review_index.json'
 qp=R/'data/director/spell_review/remaining_work_queue_62.json';regp=qp.parent/'accepted_interface_registry_06.json'
 cov=R/'data/playtest/game_development_coverage.json';ledger=A/'PERTINENT_GPT_DECISIONS_2026_10_20_02.json'
 catalog,index,queue,registry=map(read,[catp,ip,qp,regp])
 protected={p:p.read_bytes() for p in [catp,ip,qp,regp,cpfile,cov,ledger]}
 for b in cp['canonicalHelperBaselinesUnchanged']:
  p=G/b['path'];ck('Current helper '+b['path'],info(p)==b);protected[p]=p.read_bytes();bind(p)
 ck('Exact checkpoint75',info(cpfile)['sha256']=='43ee2e1598d044009fea96e6a337f1d43ac4b1487f6b1b3d0329d37a92785cf9')
 ck('Exact queue62',info(qp)==cp['currentWorkQueue'])
 ck('Current45 accepted unapplied',cp['acceptedButUnapplied']==45 and queue['acceptedButUnappliedTotalCurrent']==45 and not cp['implementationApplied'])
 ck('Applied coverage unchanged',index['authoredCounts']=={'reviewed':525,'pending':323} and index['representationCounts']['completeReviewedStandaloneProcedures']==249 and len(registry['entries'])==173)
 for p in [catp,ip,qp,regp,cpfile,cov,ledger,Path(__file__),Path(__file__).with_name('rank9_resonance_fields_3_questions_01.py'),
  G/'CANON_MANIFEST.md',G/'docs/canon/CANON_MANIFEST.json',G/'docs/canon/REPOSITORY_PROMOTION.md',
  A/'GPT_PART5_PERTINENT_OWNER_CHOICES_2026_10_20_NATIVE.json',A/'GPT_PART5_STATUS_SYNC_15_NATIVE.json',
  G/'docs/audit/2026-10-20/github-snapshot-material-forging72/PUSH_RECEIPT.json',
  R/'rulebook_output.txt',G/'docs/reference/Player_Rulebook_v6_source_text.txt',R/'books/player/Decennium_Descent_Player_Rulebook_v6.docx']:bind(p)
 lines=(R/'rulebook_output.txt').read_text('utf-16').splitlines();reference=(G/'docs/reference/Player_Rulebook_v6_source_text.txt').read_text('utf-8').splitlines()
 records=[]
 for sid in IDS:
  priorp=A/('EVOCATION_RANK9_SOURCE_PREPARATION.json' if sid=='arc-furnace' else 'CONJURATION_RANK9_SOURCE_PREPARATION.json')
  bind(priorp);prior=read(priorp);n=next(i for i,x in enumerate(prior['selectedSpells']) if x['spellId']==sid);hist=prior['selectedSpells'][n]
  card=next(x for x in catalog['spells'] if x['id']==sid);row=next(x for x in queue['rows'] if x['id']==sid);entry=next(x for x in index['entries'] if x['id']==sid)
  ck('Full native/current/history identity '+sid,hist['fullSourceAndCurrentAccessRecord']==card==row['completeCurrentSourceAndAccess'])
  ck('Actually ungrouped pending '+sid,row['currentGroup'] is None and not row['previousAuthoringMapRowUnchanged']['completeEarlierProposalRecords'] and entry['authoredStatus']=='pending-authored-procedure')
  school='Evocation' if sid=='arc-furnace' else 'Conjuration';classes=['Mage','Wizard'] if sid=='arc-furnace' else ['Druid','Mage','Wizard']
  ck('Exact class access '+sid,card['classAccess']=={c:{'rank':9,'minimumClassLevel':17,'school':school,'baseRpCost':26} for c in classes})
  ck('Exact Core metadata '+sid,len(card['source']['coreEntries'])==1 and all(e['original']['casting_time']=='1 action' and e['original']['range']=='120 feet' and e['original']['components']=='V, S, F' and e['original']['duration']=='Instantaneous' and e['original']['rp_cost']==26 for e in card['source']['coreEntries']))
  books=[deepcopy(b) for b in prior['currentBookBindings'] if b['spellId']==sid]
  ck('One complete original placement '+sid,len(books)==len(card['source']['original']['placements'])==1)
  for b in books:
   k=b['currentBookRow']['line']-1;ck('Two exact manuscript rows '+sid,lines[k]==reference[k]==b['currentBookRow']['exactText'])
  for kind in ['catalog','core']:ck('Full underlying source '+sid+kind,bind(R/card['source'][kind+'Path'])['sha256']==card['source'][kind+'Sha256'])
  records.append({'spellId':sid,'riskTier':TIERS[sid][0],'riskReason':TIERS[sid][1],'completeCurrentCatalogSourceAndAccess':deepcopy(card),'currentIndexEntry':deepcopy(entry),'originalQuestionSource':info(priorp),'originalQuestionPointer':'/selectedSpells/'+str(n),'completeOriginalSourceQuestionUnchanged':deepcopy(hist),'completeHistoricalCommonQuestionUnchanged':prior['commonOperationalQuestion'],'completeHistoricalScopeExceptionUnchanged':prior['commonQuestionException'],'completeCurrentBookBindings':books,'earlierCompleteProcedures':[],'earlierOperationalWorkedCases':[],'status':'Source conference prepared; no selected procedure or executable vectors.'})
 mechanics=['VIDEO_GAME_ONLY_DIRECTIVE.md','CLASS_PLAYTEST_RULES.md','SPELL_INTEGRATION_RULES.md','COMBAT_ACTION_PLAYTEST.md','CORE_RESOLUTION_PLAYTEST.md','CONDITIONS_PLAYTEST.md','CONTROL_STATES_PLAYTEST.md','BODY_EQUIPMENT_PLAYTEST.md','CREATURE_LIFECYCLE_PLAYTEST.md','HEALING_DEATH_PLAYTEST.md','TRANSFORMATION_SPELL_PLAYTEST.md','RESONANCE_CANON.md','COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md','CHARACTER_CREATION_PLAYTEST.md','CHARACTER_FOUNDATION_TABLES.md','XP_ADVANCEMENT_CANON.md','STRAIN_PLAYTEST.md','CUSTOM_CONDITION_BINDINGS.md','CONTROL_SOURCE_BINDINGS.md','EQUIPMENT_ITEM_PROCEDURES.md','EQUIPMENT_ACQUISITION_PLAYTEST.md','WORLD_DUNGEON_LOOP.md','EXPEDITION_STRUCTURE_CANON.md']
 for name in mechanics:bind(R/'docs/mechanics'/name)
 for name in ['data/playtest/control_state_bindings.json','data/playtest/equipment_acquisition_candidate.json','data/playtest/equipment_source_catalog.json','src/data/resonance-economy.js','data/public/feat_candidates/exact_01/candidate.json','data/public/feat_candidates/exact_01/shared_rules.json','data/public/feat_candidates/exact_01/supplements.json']:bind(R/name)
 classcomparisons=[]
 for name in ['wizard','mage','druid','mirrorsage','manifest']:
  p=R/('data/public/class_playtests/'+name+'.json');b=bind(p);d=read(p)
  for i,c in enumerate(d['cards'] if name in ['wizard','mage'] else []):
   if any(x in (c['id']+' '+c.get('name','')).lower() for x in ['absorption','efficient-casting','grand-reservoir','resonance-transfusion','elemental-fusion','resonance-apex','nuke-chain']):
    classcomparisons.append({'source':b,'pointer':'/cards/'+str(i),'completeCard':deepcopy(c),'qualification':'Actual acquisition and exact feature only; no automatic access to every Arch/Hero selection. Absorption, damage riders, temporaryHP, refunds and transfers are distinct source-specific operations.'})
 inherited=[]
 nums=list(range(12))+[13,14,23,24,26,35,36,39,40,41,49,50,112,113,148,150]
 ck('Unique interface pointers',len(nums)==len(set(nums)))
 for n in nums:
  e=registry['entries'][n];b=e['currentAuthoritativeSource'];actual=bind(G/b['path']);ck('Exact interface source '+str(n),all(actual[k]==b[k] for k in ['bytes','sha256']))
  inherited.append({'registryPointer':'/entries/'+str(n),'completeEntryUnchanged':deepcopy(e),'scopeLimit':'Preserve exact accepted scope. New all-magic conversion/enhancement, percentage damage and half-cost placement require named spell-local authorship; no global inheritance merely from a similar name.'})
 counterparts=[]
 for sid in ['resonance-nexus','resonance-well','resonance-conduit','absorb-elements','resonance-barrier','resonance-forge','resonance-dampening-field','greater-dispel','antimagic-field-lesser']:
  e=next(x for x in index['entries'] if x['id']==sid);ck('Applied counterpart '+sid,e['authoredStatus']=='reviewed-authored-operational-playtest')
  p=(ip.parent/e['procedureFile']).resolve();d=read(p);ptr=e.get('wholeCardPointer') or e['procedurePointer'];b=bind(p)
  if e.get('completeEnvelopeBinding'):ck('Exact counterpart envelope '+sid,b==e['completeEnvelopeBinding'])
  if e.get('authoredAcceptanceReceipt'):ck('Exact counterpart acceptance '+sid,bind(G/e['authoredAcceptanceReceipt']['path'])==e['authoredAcceptanceReceipt'])
  card=deepcopy(at(d,ptr))
  for key in ['operational','operationalCandidate']:
   op=card.get(key)
   if isinstance(op,dict):
    for rel in op.get('sourceReview',[])+op.get('reviewEvidence',[]):bind(G/rel)
    if op.get('authoringFile'):bind(R/op['authoringFile'])
  for rel in e.get('caseSourceReferenceAliases',{}).values():bind(G/rel)
  counterparts.append({'spellId':sid,'source':b,'pointer':ptr,'completeCurrentCard':card,'completeSharedRules':deepcopy(at(d,e['sharedRulesPointer']) if e.get('sharedRulesPointer') else d.get('sharedRules',{})),'indexEntry':deepcopy(e),'qualification':'Applied authored comparison in its exact scope, not runtime proof or permission to replace rank9 printed benefits by lower-rank behavior.'})
 pending=[]
 for name in ['rank9-casting-cost5']:
  g=next(g for g in queue['groups'] if g['group']==name);b=bind(G/g['candidate']['path']);ab=bind(G/g['archive']['path']);ck('Exact pending candidate '+name,b==g['candidate']);ck('Exact pending archive '+name,ab==g['archive'])
  pending.append({'group':name,'candidate':b,'archive':ab,'identities':deepcopy(g['identities']),'qualification':'Complete prepared source conference, not selected authority or an executable positive-case premise. The later owner Soulburn Reservoir clarification is retained separately in the current decision ledger.'})
 context={}
 for rel in ['copy-ready-preparation-only-part5-successor-01/POLICY_SELECTION.json','COPY_READY_PREPARATION_ONLY_PART5_01_LOCAL_PREFLIGHT.json','copy-ready-preparation-only-part5-successor-01/successor/CONTROL15_READY_REFERENCE_SUCCESSOR14.json','CONTROL15_PART5_FULL_RETURN_02_LOCAL_RECEIPT.json','RANK8_DAMAGE6_PART5_EXACT_AUTHORING_ACCEPTANCE_75.json','rank8-damage6-part5-cast-history-return-03/MODEL.json','rank8-damage6-part5-cast-history-return-03/HOLD_REGISTER.json','RANK7_READY_DEADLINE_RETURN_03_AVAILABLE_75.json','GPT_PART5_RANK7_READY_DEADLINE_RETURN_03_NATIVE.json','UNITY_DEVELOPMENT_DIRECTIONS_INTAKE_75.json','unity-development-directions-75/Decennium_Descent_Unity_Codex_Directions.md','unity-development-directions-75/Decennium_Descent_Codex_Start_Prompt.txt']:
  context[rel]=bind(A/rel)
 context['qualification']='Rank8 six accepted but unapplied, total45. Rank7 Ready Return03 reply received; archive download and independent validation pending. GPT actual status-sync15 confirms both. Owner reserves canonical implementation. Unity brief is preserved product/engineering direction, not an applied engine or cadence change.'
 for name in ['CURRENT_COSMOLOGY_READ_FIRST.md','EPILOGUE_RELIC_NULL_REVIEWED_01.md','SOULS_RESEARCH_REVIEWED_01.md']:bind(R/'docs/director-only/cosmology'/name)
 for name in ['epilogue_relic_null_reviewed_01.json','souls_research_reviewed_01.json']:bind(R/'data/director/cosmology'/name)
 questions=[{'id':i,'spellIds':ids,'exactSourceOrConflict':s,'options':options,'recommendationAndConsequences':rec,'decisionSelected':False} for i,ids,s,options,rec in Q]
 ck('24 unique unselected questions',len(questions)==len({q['id'] for q in questions})==24 and not any(q['decisionSelected'] for q in questions))
 ck('Exactly three spell identities',set().union(*(set(q['spellIds']) for q in questions))==set(IDS))
 ck('Nine applied comparisons and three source records',len(counterparts)==9 and len(records)==3)
 candidate={'id':'RANK9-RESONANCE-FIELDS3-SOURCE-CONFERENCE01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'SOURCE_CONFERENCE_PREPARED_UNSENT','developmentDirection':'video-game-only','records':records,
  'historicalWorkflowQualification':'Pre-push source-question wording and old39-count notebook replies remain exact history. Verified GitHub backup through72 and current local checkpoint75/acceptance75 govern current status; no new cosmology or implementation selected.',
  'currentAcceptedInterfaceComparisons':inherited,'completeAppliedCounterparts':counterparts,'completeClassFeatureComparisons':classcomparisons,'pendingComparisonsNotAuthority':pending,'laterCompleteReviewContext':context,'questions':questions,'riskCounts':{'C':3},'sourceFindings':FINDINGS,'futureCaseRequirements':CASES,
  'semanticDelta':[{'spellId':sid,'riskTier':'C','riskReason':TIERS[sid][1],'startingPoint':'Complete native source and historical question; no authored procedure or cases.','genuineQuestionIds':[q['id'] for q in questions if sid in q['spellIds']]} for sid in IDS],
  'earlierOperationalWorkedCases':[],'currentVectors':[],'countsUnchanged':deepcopy(index['authoredCounts']),'sourceBindings':list(sources.values()),'newRuleAdoptions':0,'runtimeTestsExecuted':0,'humanPlaytests':0,'sourceInformationDeleted':0,'cosmologyDecisions':0,'wholeGameComplete':False}
 root.mkdir();frozen=[]
 for b in sources.values():
  p=G/b['path'];ck('Current complete source '+b['path'],info(p)==b)
  dst=root/'sources'/b['path'];target=Path('\\\\?\\'+str(dst.resolve()));target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(p.read_bytes());ck('Frozen complete source '+b['path'],target.read_bytes()==p.read_bytes());frozen.append({**b,'frozenCopy':dst.relative_to(G).as_posix()})
 for p,b in protected.items():ck('Protected authority unchanged '+p.name,p.read_bytes()==b)
 out.write_bytes(enc(candidate));check.write_bytes(enc({'candidate':info(out),'checks':checks,'checkCount':len(checks),'sourceCount':len(sources),'sourceIdentities':3,'placements':3,'questions':24,'riskCounts':{'C':3},'failures':0,'earlierCompleteProcedures':0,'newCurrentVectors':0,'validationScope':'Complete source/access/context preservation and preparation, not selected semantics or runtime testing.'}))
 manifest=root/'MANIFEST.json';manifest.write_bytes(enc({'candidate':info(out),'check':info(check),'files':list(sources.values()),'frozenSources':frozen,'sourceCount':len(sources),'newRuleAdoptions':0}))
 readme='Three complete rank9 identities and original placements;24 unselected questions;9 full applied spell comparisons;full actual class features;one complete pending casting-cost source archive. Preserve+50percent allied spell damage,all-magic absorption/conversion,and all-magic enhancement with half Resonance costs. All tierC. Current accepted-unapplied45; applied525/323/249/173 unchanged. No selected procedure,runtime,balance,cosmology,implementation or release approval.\n'
 (root/'README.md').write_text(readme,encoding='utf-8',newline='\n')
 with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p,name in [(out,'CANDIDATE.json'),(check,'SOURCE_CHECK.json'),(manifest,'MANIFEST.json')]:z.write(p,name)
  z.writestr('README.md',readme)
  for b in sources.values():z.writestr('sources/'+b['path'],(G/b['path']).read_bytes())
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None and len(z.namelist())==len(set(z.namelist())) and z.read('CANDIDATE.json')==out.read_bytes()
  for b in sources.values():assert z.read('sources/'+b['path'])==(G/b['path']).read_bytes()
 ab=info(archive)
 request.write_text(f'Review {archive.name}, {ab["bytes"]} bytes SHA256 {ab["sha256"]}. Read all three complete identities/placements,24 unselected questions,9 full applied spell counterparts,actual class feature comparisons,current interface sources and complete pending casting-cost archive as nonauthority. Preserve Arc Furnace allies spell damage+50percent in a zone; Resonance Singularity a point absorbing all magic and converting it to Resonance; Supreme Nexus both all-magic enhancement and halved Resonance costs. All rank9,class17,base26RP,Action,120feet,V/S/F,CoreInstantaneous conflict. Mage/Wizard Evocation access for Furnace; Druid/Mage/Wizard Conjuration for the other two. Do not replace these benefits by easier lower-rank versions or invent crafting from Furnace. Select explicit spell-local geometry,duration,qualification,damage/provenance,all-magic scope,absorption/lifecycle,conversion recipient/rate/ledger,half-price stage,protected principal,actual-paid-base attribution,enhancement,stacking and finite cross-field order. Every missing limit/formula/category exception is NEW scoped authorship. Preserve accepted price and Null contracts,actual source acquisition,paid casting history and real Action/Reaction/turn markers. Return full reasoning,complete selected procedures and artifact bytes,exact reversible operations,at least two useful positive encounters per spell plus meaningful full-state branches and one combined-field case. No held external positive premise or pending cohort may be silently treated as executable law. Rank8 six accepted-unapplied,total45;Rank7 exact return pending independent local validation;owner reserves canonical implementation. Separate source,semantic,numerical,specification,runtime,human,balance,cosmology and release gates. Prepared UNSENT until separately submitted.\n',encoding='utf-8',newline='\n')
 prep.write_bytes(enc({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PREPARED_UNSENT','candidate':info(out),'archive':ab,'manifest':info(manifest),'check':info(check),'request':info(request),'sourceCount':len(sources),'identityCount':3,'placementCount':3,'questionCount':24,'riskCounts':{'C':3},'allArchiveMembersVerified':True,'newRuleAdoptions':0,'sourceInformationDeleted':0}))
 print(json.dumps({'preparation':info(prep),'candidate':info(out),'archive':ab,'sources':len(sources),'checks':len(checks),'questions':24,'failures':0}))
if __name__=='__main__':main()
