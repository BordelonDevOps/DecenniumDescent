"""Freeze exact material/item sources and unselected questions; apply no rules."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
from copy import deepcopy
import hashlib, json, zipfile
from rank9_material_forging_2_questions_01 import IDS, TIERS, Q, FINDINGS, CASES

G=Path(r'C:\Github\DecenniumDescent-review-push-134'); R=G/'DescentReviewChanges/ReviewBible'; A=G/'docs/audit/2026-10-08/full-game'
def read(p): return json.loads(p.read_bytes())
def enc(x): return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def info(p):
 b=p.read_bytes(); return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def at(d,ptr):
 for key in ptr.strip('/').split('/') if ptr else []:
  key=key.replace('~1','/').replace('~0','~'); d=d[int(key)] if isinstance(d,list) else d[key]
 return d
def main():
 stem='RANK9_MATERIAL_FORGING_2_SOURCE_CONFERENCE_02'
 root=A/'rank9-material-forging2-source-conference-02'
 out=R/'data/director/spell_review/rank9_material_forging_2_source_conference_02.json'
 check,prep,request=[A/(stem+s) for s in ['_CHECK.json','_PREPARATION.json','_REQUEST.txt']]
 archive=A/'DD_Rank9_Material_Forging_2_Source_Conference_02.zip'
 assert not any(p.exists() for p in [root,out,check,prep,request,archive])
 sources={}; checks=[]
 def ck(name,ok): checks.append({'check':name,'passed':bool(ok)}); assert ok,name
 def bind(p):
  b=info(p); sources[b['path']]=b; return b
 authority_dir=A/'director-spell-review-129'
 evidence_paths={
  'currentQueue':authority_dir/'CURRENT_SPELL_QUEUE_209.json',
  'currentHandoff':authority_dir/'CURRENT_HANDOFF_209.json',
  'currentPendingAudit':authority_dir/'CURRENT44_PENDING_IDENTITY_AUDIT_209.json',
  'application':authority_dir/'RANK9ELEMENTALPETS2_APPLICATION_209.json',
  'acceptance':authority_dir/'RANK9ELEMENTALPETS2_EXACT_ACCEPTANCE_209.json',
  'independentAudit':authority_dir/'RANK9ELEMENTALPETS2_INDEPENDENT_AUDIT_209.json',
  'applicationValidation':authority_dir/'RANK9ELEMENTALPETS2_APPLICATION_VALIDATION_209.json',
  'deliveryManifest':authority_dir/'rank9_elementalpets2_return209_received/DD_Rank9_ElementalPets2_Director_Return209_Repack01_DELIVERY.json'}
 evidence={k:read(p) for k,p in evidence_paths.items()}
 for p in evidence_paths.values(): bind(p)
 ck('Current authority chain',evidence['currentHandoff']['currentAuthority']=={'reviewedApplied':804,'pending':44,'acceptedUnapplied':0,'completeStandaloneProcedures':528,'scopedInterfaces':173} and evidence['currentQueue']['currentAuthority']==evidence['currentHandoff']['currentAuthority'] and evidence['currentPendingAudit']['pendingCount']==44 and evidence['application']['acceptedIds']==['elemental-convergence','elemental-fusion'] and evidence['application']['countsAfter']=={'reviewed':804,'pending':44} and evidence['deliveryManifest']['acceptedIds']==['elemental-convergence','elemental-fusion'])
 authority_evidence={'currentAuthority':evidence['currentHandoff']['currentAuthority'],'currentQueueBinding':info(evidence_paths['currentQueue']),'currentHandoffBinding':info(evidence_paths['currentHandoff']),'pendingIdentityAuditBinding':info(evidence_paths['currentPendingAudit']),'applicationReceiptBinding':info(evidence_paths['application']),'acceptanceReceiptBinding':info(evidence_paths['acceptance']),'independentAuditBinding':info(evidence_paths['independentAudit']),'applicationValidationBinding':info(evidence_paths['applicationValidation']),'returnDeliveryManifestBinding':info(evidence_paths['deliveryManifest']),'priorReturnReportedAuthority':evidence['deliveryManifest']['sourceAuthority'],'priorReturnWasApplied':evidence['deliveryManifest']['applied']}
 catp=R/'data/public/spell_playtests/catalog.json'; ip=catp.parent/'authored_review_index.json'
 qp=R/'data/director/spell_review/remaining_work_queue_67.json'; regp=qp.parent/'accepted_interface_registry_06.json'
 cp=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK8_CORRECTION_SEMANTICS_71.json'
 cov=R/'data/playtest/game_development_coverage.json'; ledger=A/'PERTINENT_GPT_DECISIONS_2026_10_20_02.json'
 catalog,index,queue,registry=map(read,[catp,ip,qp,regp])
 native_source_path=R/'src/data/spells.js'; native_source_text=native_source_path.read_text('utf-8')
 native_start=native_source_text.index('export const SPELLS = ')+len('export const SPELLS = ')
 native_end=native_source_text.index('\n};',native_start)+2
 native_spells=json.loads(native_source_text[native_start:native_end])
 core_path=R/'data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json'; current_core=read(core_path)
 protected={p:p.read_bytes() for p in [catp,ip,qp,regp,cp,cov,ledger]}
 ck('Current applied counts',index['authoredCounts']=={'reviewed':804,'pending':44} and index['representationCounts']['completeReviewedStandaloneProcedures']==528 and len(registry['entries'])==173)
 for p in [catp,ip,qp,regp,cp,cov,ledger,Path(__file__),Path(__file__).with_name('rank9_material_forging_2_questions_01.py'),
   A/'GPT_PART5_PERTINENT_OWNER_CHOICES_2026_10_20_NATIVE.json',A/'GPT_UNITY_DEVELOPMENT_SETUP_2026_10_20_NATIVE.json',
   G/'docs/audit/2026-10-20/github-snapshot-illusion-reality65/PUSH_RECEIPT.json',
   R/'rulebook_output.txt',G/'docs/reference/Player_Rulebook_v6_source_text.txt',R/'books/player/Decennium_Descent_Player_Rulebook_v6.docx']:
  bind(p)
 lines=(R/'rulebook_output.txt').read_text('utf-16').splitlines()
 reference=(G/'docs/reference/Player_Rulebook_v6_source_text.txt').read_text('utf-8').splitlines()
 records=[]
 for sid in IDS:
  old=A/('CONJURATION_RANK9_SOURCE_PREPARATION.json' if sid=='eternal-forge' else 'TRANSMUTATION_UNIVERSAL_RANK9_SOURCE_PREPARATION.json')
  bind(old); prior=read(old); n=next(i for i,s in enumerate(prior['selectedSpells']) if s['spellId']==sid); hist=prior['selectedSpells'][n]
  card=next(c for c in catalog['spells'] if c['id']==sid); row=next(x for x in queue['rows'] if x['id']==sid); entry=next(x for x in index['entries'] if x['id']==sid)
  ck('Historical identity and current source/access '+sid,hist['fullSourceAndCurrentAccessRecord']['id']==sid and card==row['completeCurrentSourceAndAccess'])
  ck('Actually pending in material group '+sid,row['currentGroup']=='rank9-material-forging2' and not row['previousAuthoringMapRowUnchanged']['completeEarlierProposalRecords'] and entry['authoredStatus']=='pending-authored-procedure')
  school='Conjuration' if sid=='eternal-forge' else 'Transmutation'
  ck('Complete exact access '+sid,card['classAccess']=={c:{'rank':9,'minimumClassLevel':17,'school':school,'baseRpCost':26} for c in ['Druid','Mage','Wizard']})
  components='V, S, F' if sid=='eternal-forge' else 'V, S, M/F'; duration='Until dispelled' if sid=='eternal-forge' else 'Instantaneous'
  ck('Exact Core metadata '+sid,all(e['original']['casting_time']=='1 action' and e['original']['range']=='120 feet' and e['original']['components']==components and e['original']['duration']==duration for e in card['source']['coreEntries']))
  books=[deepcopy(x) for x in prior['currentBookBindings'] if x['spellId']==sid]
  ck('One full original placement '+sid,len(books)==len(card['source']['original']['placements'])==1)
  for b in books:
   j=b['currentBookRow']['line']-1; ck('Both original manuscript rows '+sid,lines[j]==reference[j]==b['currentBookRow']['exactText'])
  native_binding=bind(R/card['source']['catalogPath']); core_binding=bind(core_path)
  current_native=native_spells[card['source']['catalogKey']]
  core_idx=card['source']['coreEntries'][0]['index']; current_core_entry=current_core['spells'][core_idx]
  ck('Current native spell source row '+sid,all(current_native.get(k)==v for k,v in card['source']['original'].items() if k in current_native))
  ck('Current Core spell source row '+sid,current_core_entry==card['source']['coreEntries'][0]['original'])
  records.append({'spellId':sid,'riskTier':TIERS[sid][0],'riskReason':TIERS[sid][1],
   'completeCurrentCatalogSourceAndAccess':deepcopy(card),'currentIndexEntry':deepcopy(entry),'originalQuestionSource':info(old),'originalQuestionPointer':'/selectedSpells/'+str(n),
   'completeOriginalSourceQuestionUnchanged':deepcopy(hist),'completeHistoricalCommonQuestionUnchanged':prior['commonOperationalQuestion'],
   'completeHistoricalScopeExceptionUnchanged':prior['commonQuestionException'],'completeCurrentBookBindings':books,
   'currentNativeSourceBinding':native_binding,'historicalCatalogFileSha256':card['source']['catalogSha256'],'currentCoreSourceBinding':core_binding,
   'currentNativeSourceRow':deepcopy(current_native),'currentCoreSourceRow':deepcopy(current_core_entry),
   'earlierCompleteProcedures':[],'earlierOperationalWorkedCases':[],'status':'Source conference prepared; no selected procedure or executable vectors.'})
 mechanics=['VIDEO_GAME_ONLY_DIRECTIVE.md','CLASS_PLAYTEST_RULES.md','SPELL_INTEGRATION_RULES.md','COMBAT_ACTION_PLAYTEST.md',
  'CORE_RESOLUTION_PLAYTEST.md','CONDITIONS_PLAYTEST.md','CONTROL_STATES_PLAYTEST.md','BODY_EQUIPMENT_PLAYTEST.md',
  'CREATURE_LIFECYCLE_PLAYTEST.md','HEALING_DEATH_PLAYTEST.md','TRANSFORMATION_SPELL_PLAYTEST.md','RESONANCE_CANON.md',
  'COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md','CHARACTER_CREATION_PLAYTEST.md','CHARACTER_FOUNDATION_TABLES.md',
  'XP_ADVANCEMENT_CANON.md','STRAIN_PLAYTEST.md','CUSTOM_CONDITION_BINDINGS.md','CONTROL_SOURCE_BINDINGS.md',
  'EQUIPMENT_ITEM_PROCEDURES.md','EQUIPMENT_ACQUISITION_PLAYTEST.md','EQUIPMENT_SOURCE_BINDINGS.md','EQUIPMENT_REVIEW_STATUS.json',
  'CRAFTING_HARVEST_PLAYTEST.md','CRAFTING_TRADE_REFERENCE.md','CRAFTING_ENGINE_REVIEW_STATUS.json','CRAFTING_RECIPE_REVIEW_INDEX.md',
  'BLACKSMITHING_RECIPE_PLAYTEST.md','BLACKSMITHING_REVIEW_STATUS.json','JEWELCRAFTING_RECIPE_PLAYTEST.md','JEWELCRAFTING_REVIEW_STATUS.json',
  'ADVANCED_CRAFT_CANDIDATE_GUIDE.md','ADVANCED_CRAFT_CANDIDATE_BODY_CATALOGUE.md','ADVANCED_CRAFT_REVIEW_STATUS.json',
  'GATHERING_TOOL_CANDIDATE_GUIDE.md','GATHERING_TOOL_CANDIDATE_BODY_CATALOGUE.md','GATHERING_TOOL_REVIEW_STATUS.json',
  'T1_5_CRAFTING_COMPONENTS_2026-07-31.md','WORLD_DUNGEON_LOOP.md','EXPEDITION_STRUCTURE_CANON.md']
 for name in mechanics: bind(R/'docs/mechanics'/name)
 for name in ['data/playtest/control_state_bindings.json','data/playtest/equipment_acquisition_candidate.json','data/playtest/equipment_source_catalog.json',
   'data/playtest/crafting_engine_candidate.json','data/director/crafting_engine_recipe_index.json','src/data/crafting-recipes.json',
   'data/director/blacksmithing_recipe_candidate_internal.json','data/director/jewelcrafting_recipe_candidate_internal.json',
   'data/crafting/advanced_craft_recipe_candidate_public.json','data/director/advanced_craft_recipe_candidate_internal.json',
   'data/crafting/gathering_tool_recipe_candidate_public.json','data/director/gathering_tool_recipe_candidate_internal.json',
   'scripts/fill-crafting-components.mjs','data/director/feat_candidates/exact_01/cohorts/crafting.json']:
  bind(R/name)
 biblep=R/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json'; bible=read(biblep); bind(biblep)
 recipep=R/'data/director/crafting_recipe_review_catalog.json'; recipes=read(recipep); bind(recipep)
 current_recipe_by_id={r['id']:r for r in bible['recipes']}
 ck('Reviewed recipe metadata maps to current source',all(r['recipeId'] in current_recipe_by_id and r['name']==current_recipe_by_id[r['recipeId']]['name'] and r['visibility']==current_recipe_by_id[r['recipeId']]['visibility'] and r['sourceStatus']==current_recipe_by_id[r['recipeId']]['status'] for r in recipes['recipes']))
 ck('All687 recipes actually reviewed',recipes['totals']=={'sourceRecipes':687,'reviewed':687,'unreviewed':0,'authoredDrafts':0,'publicRecipes':433,'publicReviewed':433} and len(recipes['recipes'])==687 and all(r['status']=='reviewed-authored-playtest' for r in recipes['recipes']))
 ck('Recipe identities match original full Bible',set(r['recipeId'] for r in recipes['recipes'])==set(r['id'] for r in bible['recipes']))
 for row in recipes['recipes']:
  bind(R/row['cardFile']); bind(R/row['reviewManifest'])
 recipecomparisons=[]
 for name,rid in [('blacksmithing','recipe-42'),('jewelcrafting','recipe-241')]:
  p=R/('data/playtest/'+name+'_recipe_candidate.json'); d=read(p); b=bind(p); n=next(i for i,c in enumerate(d['cards']) if c['recipeId']==rid); card=d['cards'][n]
  ck('Complete genuine reviewed product '+rid,card['status']=='reviewed-authored-operational-playtest' and card['sourceRecipe']==bible['recipes'][card['sourceRecipeIndex']] and card['sourceRecipe']['id']==rid)
  recipecomparisons.append({'source':b,'pointer':'/cards/'+str(n),'completeCard':deepcopy(card),
    'completeSharedOperationalProfile':deepcopy(d['sharedOperationalProfile']),'completeBaseModels':deepcopy(d['baseModels']),
    'qualification':'Actual reviewed item comparison, not automatic Eternal Forge eligibility, free base bodies, recipe access or batch quantity. Full native recipe, body, charge, rider and economy contracts retained.'})
 materialstatus={'completeSource':info(biblep),'reviewCatalog':info(recipep),'reviewCatalogSourceHash':recipes['sourceSha256'],'reviewCatalogSourceHashMatchesCurrentBible':recipes['sourceSha256']==info(biblep)['sha256'],'totals':deepcopy(recipes['totals']),
   'recipeVisibility':dict(Counter(r['visibility'] for r in recipes['recipes'])),
   'materialVisibility':dict(Counter(r['visibility'] for r in bible['materials'])),
   'qualification':'The review catalog source hash differs from the current crafting Bible hash. All687 recipe identities, names, visibility and source statuses map to current rows, but detailed changes are not automatically covered by the older review cards. Treat those cards as comparison context and inspect current full rows. Authored-review status is not runtime/balance approval or universal public knowledge. Historical Mithral remaps do not amend current mithril trade-good or coin sources.'}
 ck('Distinct material and recipe visibility',materialstatus['recipeVisibility']=={'public':433,'restricted':39,'director-only':215} and materialstatus['materialVisibility']=={'public':604,'restricted':92} and len(bible['materials'])==696)
 moneylines=[]
 for num in [6542,6576,6577,6578]:
  ck('Exact currency/material source line '+str(num),lines[num-1]==reference[num-1]); moneylines.append({'line':num,'exactText':lines[num-1]})
 classcomparisons=[]
 for name in ['wizard','mage','druid','mirrorsage','manifest']: bind(R/('data/public/class_playtests/'+name+'.json'))
 wp=R/'data/public/class_playtests/wizard.json'; wiz=read(wp)
 for sid in ['wizard.base.minor-conjuration','wizard.hero.elementalist.arcane-experimentation']:
  n=next(i for i,c in enumerate(wiz['cards']) if c['id']==sid)
  classcomparisons.append({'source':info(wp),'pointer':'/cards/'+str(n),'completeCard':deepcopy(wiz['cards'][n]),
   'qualification':'Actual legally acquired class feature only. No free recipe, materials, downtime or feat. Conjuration creature HP does not automatically become item durability.'})
 inherited=[]
 interface_binding_mismatches=[]
 nums=list(range(12))+[13,14,22,23,24,36,39,40,41,49,50,58,75,78,79,80,108,109,110,112,113,115,116,143,144,145,149,150,151]
 ck('No repeated interface entries',len(nums)==len(set(nums)))
 for n in nums:
  e=registry['entries'][n]; b=e['currentAuthoritativeSource']; actual=bind(G/b['path']); stored_binding_matches=all(actual[k]==b[k] for k in ['bytes','sha256'])
  if not stored_binding_matches: interface_binding_mismatches.append({'registryPointer':'/entries/'+str(n),'interfaceId':e.get('id'),'storedBinding':deepcopy(b),'currentFileBinding':actual})
  inherited.append({'registryPointer':'/entries/'+str(n),'completeEntryUnchanged':deepcopy(e),'currentSourceFileBinding':actual,'storedRegistryBindingMatchesCurrent':stored_binding_matches,
   'scopeLimit':'Exact existing scope only. Permanent magical creation, arbitrary material conversion, new body initialization and economy permissions require explicit spell-local authorship. Do not generalize summon, spell, item-enchantment or recipe-work rules across boundaries.'})
 counterparts=[]
 acceptance_receipt_mismatches=[]
 envelope_binding_mismatches=[]
 for sid in ['resonance-forge','transmute-weapon','stone-shape','mending','fortify-object','identify','true-polymorph','greater-dispel','antimagic-field-lesser']:
  e=next(e for e in index['entries'] if e['id']==sid); ck('Applied comparison '+sid,e['authoredStatus']=='reviewed-authored-operational-playtest')
  p=(ip.parent/e['procedureFile']).resolve(); d=read(p); ptr=e.get('wholeCardPointer') or e['procedurePointer']; b=bind(p)
  envelope_binding_matches=None
  if e.get('completeEnvelopeBinding'):
   envelope_binding_matches=b==e['completeEnvelopeBinding']
   if not envelope_binding_matches: envelope_binding_mismatches.append({'spellId':sid,'storedBinding':deepcopy(e['completeEnvelopeBinding']),'currentFileBinding':b})
  current_acceptance_binding=None; acceptance_binding_matches=None
  if e.get('authoredAcceptanceReceipt'):
   current_acceptance_binding=bind(G/e['authoredAcceptanceReceipt']['path']); acceptance_binding_matches=current_acceptance_binding==e['authoredAcceptanceReceipt']
   if not acceptance_binding_matches: acceptance_receipt_mismatches.append({'spellId':sid,'storedBinding':deepcopy(e['authoredAcceptanceReceipt']),'currentFileBinding':current_acceptance_binding})
  card=deepcopy(at(d,ptr))
  for k in ['operational','operationalCandidate']:
   op=card.get(k)
   if isinstance(op,dict):
    for path in op.get('sourceReview',[])+op.get('reviewEvidence',[]): bind(G/path)
    if op.get('authoringFile'): bind(R/op['authoringFile'])
  for path in e.get('caseSourceReferenceAliases',{}).values(): bind(G/path)
  counterparts.append({'spellId':sid,'source':b,'pointer':ptr,'completeCurrentCard':card,'currentAcceptanceReceiptBinding':current_acceptance_binding,'storedAcceptanceReceiptMatchesCurrent':acceptance_binding_matches,'storedEnvelopeBindingMatchesCurrent':envelope_binding_matches,
   'completeSharedRules':deepcopy(at(d,e['sharedRulesPointer']) if e.get('sharedRulesPointer') else d.get('sharedRules',{})),
   'indexEntry':deepcopy(e),'qualification':'Applied authored comparison only in its exact scope. Preserve useful creation/conversion instead of silently replacing it with the lower-rank procedure.'})
 pending=[]
 pending_source_mismatches=[]
 for name in ['creation1','material-terrain8','vitality-matter10']:
  group=next(g for g in queue['groups'] if g['group']==name); b=bind(G/group['candidate']['path']); ab=bind(G/group['archive']['path'])
  candidate_binding_matches=b==group['candidate']; archive_binding_matches=ab==group['archive']
  if not candidate_binding_matches or not archive_binding_matches: pending_source_mismatches.append({'group':name,'storedCandidateBinding':deepcopy(group['candidate']),'currentCandidateBinding':b,'storedArchiveBinding':deepcopy(group['archive']),'currentArchiveBinding':ab})
  pending.append({'group':name,'candidate':b,'archive':ab,'storedCandidateBindingMatchesCurrent':candidate_binding_matches,'storedArchiveBindingMatchesCurrent':archive_binding_matches,'identities':deepcopy(group['identities']),'qualification':'Complete source-conference comparison only, not accepted rules or a lawful executable-case premise. Historical queue bindings are retained; current files are included separately.'})
 context={}
 for name in ['copy-ready-preparation-only-part5-successor-01/POLICY_SELECTION.json','COPY_READY_PREPARATION_ONLY_PART5_01_LOCAL_PREFLIGHT.json',
   'copy-ready-preparation-only-part5-successor-01/successor/CONTROL15_READY_REFERENCE_SUCCESSOR14.json',
   'CONTROL15_PART5_FULL_RETURN_02_LOCAL_RECEIPT.json','RANK7_IDENTITY_CASTING5_PART5_RETURN_01_SEMANTIC_REVIEW_68.json',
   'DD_Rank7_Identity_Casting5_Local_Corrections_01.zip','GPT_PART5_RANK7_IDENTITY_CORRECTIONS_12_DISPATCH_NATIVE.json',
   'RANK8_DAMAGE6_PART5_CORRECTION_RETURN_02_SEMANTIC_RECONCILIATION_70.json','DD_Rank8_Damage6_Cast_History_Correction_02.zip',
   'RANK8_DAMAGE6_CAST_HISTORY_CORRECTION_02_PREPARATION.json']:
  context[name]=bind(A/name)
 context['qualification']='Owner implementation remains reserved. Rank7 correction12 actually sent; Rank8 eight findings reconciled with one additional Anchor history question prepared unsent. Neither cohort independently accepted. Copied-feat preparation-only policy is settled within its seven-profile scope; implementation is separate.'
 for name in ['candidate.json','shared_rules.json','supplements.json']: bind(R/'data/public/feat_candidates/exact_01'/name)
 for name in ['CURRENT_COSMOLOGY_READ_FIRST.md','EPILOGUE_RELIC_NULL_REVIEWED_01.md','SOULS_RESEARCH_REVIEWED_01.md']: bind(R/'docs/director-only/cosmology'/name)
 for name in ['epilogue_relic_null_reviewed_01.json','souls_research_reviewed_01.json']: bind(R/'data/director/cosmology'/name)
 questions=[{'id':i,'spellIds':ids,'exactSourceOrConflict':s,'options':opts,'recommendationAndConsequences':rec,'decisionSelected':False} for i,ids,s,opts,rec in Q]
 ck('24 unique unselected questions',len(questions)==len({q['id'] for q in questions})==24 and not any(q['decisionSelected'] for q in questions))
 ck('Exactly two sources covered',set().union(*(set(q['spellIds']) for q in questions))==set(IDS))
 ck('Nine applied and three pending comparisons',len(counterparts)==9 and len(pending)==3 and len(recipecomparisons)==2)
 candidate={'id':'RANK9-MATERIAL-FORGING2-SOURCE-CONFERENCE02','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
  'status':'SOURCE_CONFERENCE_PREPARED_UNSENT','developmentDirection':'video-game-only','currentAuthorityEvidence':authority_evidence,'records':records,
  'historicalWorkflowQualification':'Original pre-push and early unreviewed-recipe statements are preserved as history. The historic GitHub state is cited only as provenance; this packet requests no GitHub or repository action. Current reviewed recipe catalog governs recipe-review status. No new cosmology is selected.',
  'currentAcceptedInterfaceComparisons':inherited,'staleInterfaceSourceBindings':interface_binding_mismatches,'completeAppliedCounterparts':counterparts,'staleAcceptanceReceiptBindings':acceptance_receipt_mismatches,'staleEnvelopeBindings':envelope_binding_mismatches,'completeClassFeatureComparisons':classcomparisons,
  'completeReviewedItemComparisons':recipecomparisons,'craftingReviewStatus':materialstatus,'exactCurrencyAndMaterialSourceRows':moneylines,
  'pendingComparisonsNotAuthority':pending,'stalePendingComparisonBindings':pending_source_mismatches,'laterCompleteReviewContext':context,'questions':questions,'riskCounts':{'C':2},
  'sourceFindings':FINDINGS,'futureCaseRequirements':CASES,
  'semanticDelta':[{'spellId':sid,'riskTier':'C','riskReason':TIERS[sid][1],'startingPoint':'Complete native source and historical question; no authored procedure or cases.',
   'genuineQuestionIds':[q['id'] for q in questions if sid in q['spellIds']]} for sid in IDS],
  'earlierOperationalWorkedCases':[],'currentVectors':[],'countsUnchanged':deepcopy(index['authoredCounts']),'currentAuthority':deepcopy(authority_evidence['currentAuthority']),
  'sourceBindings':list(sources.values()),'newRuleAdoptions':0,'runtimeTestsExecuted':0,'humanPlaytests':0,'sourceInformationDeleted':0,'cosmologyDecisions':0,'wholeGameComplete':False}
 root.mkdir(); frozen=[]
 for b in sources.values():
  p=G/b['path']; ck('Current complete source '+b['path'],info(p)==b)
  dst=root/'sources'/b['path']; target=Path('\\\\?\\'+str(dst.resolve())); target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes(p.read_bytes())
  ck('Frozen complete source '+b['path'],target.read_bytes()==p.read_bytes()); frozen.append({**b,'frozenCopy':dst.relative_to(G).as_posix()})
 for p,b in protected.items(): ck('Protected authority unchanged '+p.name,p.read_bytes()==b)
 out.write_bytes(enc(candidate)); check.write_bytes(enc({'candidate':info(out),'checks':checks,'checkCount':len(checks),'sourceCount':len(sources),
  'sourceIdentities':2,'placements':2,'questions':24,'riskCounts':{'C':2},'failures':0,'earlierCompleteProcedures':0,'newCurrentVectors':0,
  'validationScope':'Source/access/full-context preservation only; no selected semantics or runtime test.'}))
 manifest=root/'MANIFEST.json'; manifest.write_bytes(enc({'candidate':info(out),'check':info(check),'files':list(sources.values()),'frozenSources':frozen,'sourceCount':len(sources),'newRuleAdoptions':0}))
 readme=f'Current local ReviewBible authority: 804 applied, 44 pending. Return209 delivery manifest contains pre-application 802/46 counts; the exact application, acceptance, audit, and validation receipts establish 804/44. Two complete rank9 identities,2 original placements,24 unselected questions,9 applied spell comparisons,3 pending conference archives,and2 complete reviewed item examples with shared profiles. Both tierC. Preserve permanent magical creation and valuable stone-to-mithril conversion. 687 reviewed recipe identities map to current Bible names, visibility and source status; the recipe review catalog source hash is stale, so inspect current full rows and treat older cards only as comparison evidence. {len(interface_binding_mismatches)} of {len(inherited)} selected inherited interface source bindings disagree with current files; reconcile them against included snapshots. {len(acceptance_receipt_mismatches)} comparator acceptance receipt references and {len(envelope_binding_mismatches)} comparator envelope references have stale hashes. {len(pending_source_mismatches)} of {len(pending)} historical pending-group source pointers differ from current files. No GitHub or repository action is requested. No new rule,case,runtime,cosmology or balance approval.\n'
 (root/'README.md').write_text(readme,encoding='utf-8',newline='\n')
 with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p,name in [(out,'CANDIDATE.json'),(check,'SOURCE_CHECK.json'),(manifest,'MANIFEST.json')]: z.write(p,name)
  z.writestr('README.md',readme)
  for b in sources.values(): z.writestr('sources/'+b['path'],(G/b['path']).read_bytes())
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None and len(z.namelist())==len(set(z.namelist())) and z.read('CANDIDATE.json')==out.read_bytes()
  for b in sources.values(): assert z.read('sources/'+b['path'])==(G/b['path']).read_bytes()
 ab=info(archive)
 request.write_text(f'Review {archive.name}, {ab["bytes"]} bytes SHA256 {ab["sha256"]}. Current local ReviewBible authority is 804 applied/44 pending. The embedded Return209 manifest contains a pre-application 802/46 snapshot; use the exact application, acceptance, audit and validation receipts plus current index/queue as authority. No GitHub or repository action is requested. Read both complete original identities/placements,all24 unselected questions,9 full applied spell comparisons,3 full pending conference archives,2 complete reviewed item examples and current687-recipe review catalog with every linked full card/status file. The catalog source hash is stale: 687 reviewed recipe identities map to current names/visibility/source status, but inspect current full recipe/material rows and treat older review cards only as comparison evidence. Eternal Forge must preserve permanent magical weapon OR item creation at Director discretion and reconcile Core Until Dispelled explicitly. Matter Conversion must preserve any nonmagical material into any other,including useful stone-to-mithril conversion. Both Druid/Mage/Wizard rank9,class17,base26RP,Action,120feet; Conjuration V, S, F versus Transmutation V, S, M/F (material-or-focus), respectively. Do not replace Forge with lower-rank crafting work credit,ban valuable output by an unstated equal-value rule,confuse mithril with a5gp coin or historical Brightsteel aliases,or infer new material statistics from a price. Resolve exact Director authorization,input/quantity/mass/shape,body and enchantment identity,actual item profile and finite entitlements,ownership/material/economic provenance,real buyers,crafting/XP,hostile custody,structural state,dispelling/suppression/Null,destruction and serialization. Every added bound or permission is NEW scoped authorship. Review status grants no formula,trade,unique artifact,charge refill or free base body. Return full choices and source-linked reasoning,complete selected procedures and artifact bytes,exact reversible operations,at least two useful positive encounters per spell and meaningful full-state branches. Preserve actual class/feat acquisition,paid casting history,Action and timing ledgers. Preserve originals and owner implementation reservation; separate source,semantic,numerical,specification,runtime,human,balance,cosmology and release gates. This packet is prepared UNSENT until separately submitted.\n',encoding='utf-8',newline='\n')
 prep.write_bytes(enc({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PREPARED_UNSENT','candidate':info(out),'archive':ab,'manifest':info(manifest),'check':info(check),'request':info(request),
  'sourceCount':len(sources),'identityCount':2,'placementCount':2,'questionCount':24,'riskCounts':{'C':2},'allArchiveMembersVerified':True,'newRuleAdoptions':0,'sourceInformationDeleted':0}))
 print(json.dumps({'preparation':info(prep),'candidate':info(out),'archive':ab,'sources':len(sources),'checks':len(checks),'questions':24,'failures':0}))
if __name__=='__main__': main()
