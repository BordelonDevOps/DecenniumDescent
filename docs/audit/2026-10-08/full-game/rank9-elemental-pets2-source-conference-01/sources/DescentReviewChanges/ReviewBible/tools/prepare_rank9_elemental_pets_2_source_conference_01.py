"""Freeze full sources for elemental pet convergence/fusion; select no new rules."""
from pathlib import Path
from datetime import datetime,timezone
from copy import deepcopy
import hashlib,json,zipfile
from rank9_elemental_pets_2_questions_01 import IDS,TIERS,Q,FINDINGS,CASES

G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_bytes())
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def info(p):
 b=p.read_bytes();return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def at(d,ptr):
 for key in ptr.strip('/').split('/') if ptr else []:
  key=key.replace('~1','/').replace('~0','~');d=d[int(key)] if isinstance(d,list) else d[key]
 return d
def main():
 stem='RANK9_ELEMENTAL_PETS_2_SOURCE_CONFERENCE_01'
 root=A/'rank9-elemental-pets2-source-conference-01'
 out=R/'data/director/spell_review/rank9_elemental_pets_2_source_conference_01.json'
 check,prep,request=[A/(stem+s) for s in ['_CHECK.json','_PREPARATION.json','_REQUEST.txt']]
 archive=A/'DD_Rank9_Elemental_Pets_2_Source_Conference_01.zip'
 assert not any(p.exists() for p in [root,out,check,prep,request,archive])
 sources={};checks=[]
 def ck(name,ok):checks.append({'check':name,'passed':bool(ok)});assert ok,name
 def bind(p):
  b=info(p);sources[b['path']]=b;return b
 catp=R/'data/public/spell_playtests/catalog.json';ip=catp.parent/'authored_review_index.json'
 qp=R/'data/director/spell_review/remaining_work_queue_55.json';regp=qp.parent/'accepted_interface_registry_06.json'
 cov=R/'data/playtest/game_development_coverage.json';cp=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK7_SEMANTIC_REVIEW_68.json'
 ledger=A/'PERTINENT_GPT_DECISIONS_2026_10_20_02.json';old=A/'CONJURATION_RANK9_SOURCE_PREPARATION.json'
 catalog,index,queue,registry,prior=map(read,[catp,ip,qp,regp,old])
 protected={p:p.read_bytes() for p in [catp,ip,qp,regp,cov,cp,ledger]}
 ck('Actual baseline counts',index['authoredCounts']=={'reviewed':525,'pending':323} and index['representationCounts']['completeReviewedStandaloneProcedures']==249)
 ck('Current scoped interface count',len(registry['entries'])==173)
 ck('Checkpoint68 actual bytes',info(cp)['sha256']=='2c2ebe319a7aaa634bcc21460716fce0115c013a6ceb9407f0b35792e9c37a52')
 for p in [catp,ip,qp,regp,cov,cp,ledger,old,Path(__file__),Path(__file__).with_name('rank9_elemental_pets_2_questions_01.py'),
           A/'GPT_PART5_PERTINENT_OWNER_CHOICES_2026_10_20_NATIVE.json',A/'GPT_UNITY_DEVELOPMENT_SETUP_2026_10_20_NATIVE.json',
           G/'docs/audit/2026-10-20/github-snapshot-illusion-reality65/PUSH_RECEIPT.json',
           R/'rulebook_output.txt',G/'docs/reference/Player_Rulebook_v6_source_text.txt',R/'books/player/Decennium_Descent_Player_Rulebook_v6.docx']:
  bind(p)
 lines=(R/'rulebook_output.txt').read_text('utf-16').splitlines()
 reference=(G/'docs/reference/Player_Rulebook_v6_source_text.txt').read_text('utf-8').splitlines()
 records=[]
 for sid in IDS:
  n=next(i for i,s in enumerate(prior['selectedSpells']) if s['spellId']==sid);hist=prior['selectedSpells'][n]
  card=next(c for c in catalog['spells'] if c['id']==sid);row=next(x for x in queue['rows'] if x['id']==sid);entry=next(x for x in index['entries'] if x['id']==sid)
  ck('Complete card preservation '+sid,hist['fullSourceAndCurrentAccessRecord']==card==row['completeCurrentSourceAndAccess'])
  ck('Ungrouped actual pending source '+sid,row['currentGroup'] is None and not row['previousAuthoringMapRowUnchanged']['completeEarlierProposalRecords'] and entry['authoredStatus']=='pending-authored-procedure')
  ck('Exact class access '+sid,card['classAccess']=={c:{'rank':9,'minimumClassLevel':17,'school':'Conjuration','baseRpCost':26} for c in ['Druid','Mage','Wizard']})
  duration='1 minute' if sid=='elemental-convergence' else 'Concentration, up to 1 minute'
  ck('Exact Core metadata '+sid,all(e['original']['casting_time']=='1 action' and e['original']['range']=='120 feet' and e['original']['components']=='V, S, F' and e['original']['duration']==duration for e in card['source']['coreEntries']))
  books=[deepcopy(x) for x in prior['currentBookBindings'] if x['spellId']==sid]
  ck('One complete native placement '+sid,len(books)==len(card['source']['original']['placements'])==1)
  for b in books:
   j=b['currentBookRow']['line']-1;ck('Both original manuscript rows exact '+sid,lines[j]==reference[j]==b['currentBookRow']['exactText'])
  for k in ['catalog','core']:ck('Underlying complete source '+sid+':'+k,bind(R/card['source'][k+'Path'])['sha256']==card['source'][k+'Sha256'])
  records.append({'spellId':sid,'riskTier':TIERS[sid][0],'riskReason':TIERS[sid][1],
    'completeCurrentCatalogSourceAndAccess':deepcopy(card),'currentIndexEntry':deepcopy(entry),
    'originalQuestionSource':info(old),'originalQuestionPointer':'/selectedSpells/'+str(n),
    'completeOriginalSourceQuestionUnchanged':deepcopy(hist),'completeHistoricalCommonQuestionUnchanged':prior['commonOperationalQuestion'],
    'completeHistoricalScopeExceptionUnchanged':prior['commonQuestionException'],'completeCurrentBookBindings':books,
    'earlierCompleteProcedures':[],'earlierOperationalWorkedCases':[],'status':'Prepared source conference only; no selected procedure or executable vectors.'})
 for name in ['VIDEO_GAME_ONLY_DIRECTIVE.md','CLASS_PLAYTEST_RULES.md','SPELL_INTEGRATION_RULES.md','COMBAT_ACTION_PLAYTEST.md',
   'CORE_RESOLUTION_PLAYTEST.md','CONDITIONS_PLAYTEST.md','CONTROL_STATES_PLAYTEST.md','BODY_EQUIPMENT_PLAYTEST.md',
   'CREATURE_LIFECYCLE_PLAYTEST.md','HEALING_DEATH_PLAYTEST.md','DAMAGE_SHARING_PLAYTEST.md','TRANSFORMATION_SPELL_PLAYTEST.md',
   'FORM_TEMP_HP_PLAYTEST.md','MAXIMUM_HP_PLAYTEST.md','RESONANCE_CANON.md','COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md',
   'CHARACTER_CREATION_PLAYTEST.md','CHARACTER_FOUNDATION_TABLES.md','CHARACTER_FOUNDATION_REVIEW_STATUS.json',
   'XP_ADVANCEMENT_CANON.md','STRAIN_PLAYTEST.md','CUSTOM_CONDITION_BINDINGS.md','CONTROL_SOURCE_BINDINGS.md',
   'EQUIPMENT_ITEM_PROCEDURES.md','CRAFTING_HARVEST_PLAYTEST.md','WORLD_DUNGEON_LOOP.md','EXPEDITION_STRUCTURE_CANON.md']:
  bind(R/'docs/mechanics'/name)
 for name in ['healing_playtest_rules.py','form_temphp_playtest_rules.py']:bind(R/'tools'/name)
 bind(R/'data/playtest/control_state_bindings.json')
 classes={}
 for name in ['wizard','mage','druid','mirrorsage','manifest']:
  p=R/('data/public/class_playtests/'+name+'.json');bind(p)
  if name!='manifest':classes[name]=read(p)
 classcomparisons=[]
 for name,ids in [('mage',['mage.hero.elementalist.elemental-fusion','mage.hero.archmage.empowered-link','mage.arch.metaspell-access']),
     ('wizard',['wizard.arch.spell-tether','wizard.hero.elementalist.arcane-fusion','wizard.supplement.dual-cast','wizard.supplement.tethered-cast'])]:
  cls=classes[name]
  for sid in ids:
   n=next(i for i,c in enumerate(cls['cards']) if c['id']==sid)
   classcomparisons.append({'source':info(R/('data/public/class_playtests/'+name+'.json')),'pointer':'/cards/'+str(n),'completeCard':deepcopy(cls['cards'][n]),
    'qualification':'Only genuinely acquired actual class feature; matching names do not grant ordinary spells. Complete engine/schedule are frozen separately.'})
 inherited=[]
 interface_indices=list(range(12))+[13,14,17,18,19,21,22,23,24,25,26,31,32,33,36,39,40,49,50,51,52,53,61,68,70]+list(range(78,93))+list(range(108,117))+[142]+list(range(143,152))
 ck('No duplicated interface comparisons',len(interface_indices)==len(set(interface_indices)))
 for n in interface_indices:
  e=registry['entries'][n];b=e['currentAuthoritativeSource'];actual=bind(G/b['path'])
  ck('Exact scoped interface '+str(n),all(actual[k]==b[k] for k in ['bytes','sha256']))
  inherited.append({'registryPointer':'/entries/'+str(n),'completeEntryUnchanged':deepcopy(e),
   'scopeLimit':'Exact existing scope only. Pet merger,nonconcentration group creation,shared statistics and extra casting opportunity require explicit local authorship. Do not generalize source-specific healing,suppression,projectile defense,body or companion exceptions.'})
 counterparts=[]
 counterpart_ids=['summon-fire-pet','summon-air-pet','summon-earth-pet','summon-water-pet','summon-greater-fire-pet','summon-greater-air-pet','summon-familiar','find-familiar','haste','shapechange','true-polymorph']
 for sid in counterpart_ids:
  entry=next(e for e in index['entries'] if e['id']==sid);ck('Applied counterpart '+sid,entry['authoredStatus']=='reviewed-authored-operational-playtest')
  path=(ip.parent/entry['procedureFile']).resolve();d=read(path);ptr=entry.get('wholeCardPointer') or entry['procedurePointer'];b=bind(path)
  if entry.get('completeEnvelopeBinding'):ck('Complete applied envelope '+sid,b==entry['completeEnvelopeBinding'])
  if entry.get('authoredAcceptanceReceipt'):ck('Exact applied acceptance '+sid,bind(G/entry['authoredAcceptanceReceipt']['path'])==entry['authoredAcceptanceReceipt'])
  card=deepcopy(at(d,ptr))
  for key in ['operational','operationalCandidate']:
   op=card.get(key)
   if isinstance(op,dict):
    for path in op.get('sourceReview',[])+op.get('reviewEvidence',[]):bind(G/path)
    if op.get('authoringFile'):bind(R/op['authoringFile'])
  for path in entry.get('caseSourceReferenceAliases',{}).values():bind(G/path)
  counterparts.append({'spellId':sid,'source':b,'pointer':ptr,'completeCurrentCard':card,
   'completeSharedRules':deepcopy(at(d,entry['sharedRulesPointer']) if entry.get('sharedRulesPointer') else d.get('sharedRules',{})),
   'indexEntry':deepcopy(entry),'qualification':'Applied authored comparison only in its exact scope. Original pending labels inside preserved sources do not override the actual index/acceptance.'})
 pending=[]
 for name in ['manifestation7','rank8-summon-structure5']:
  group=next(g for g in queue['groups'] if g['group']==name)
  b=bind(G/group['candidate']['path']);ab=bind(G/group['archive']['path'])
  ck('Complete pending candidate '+name,b==group['candidate']);ck('Complete pending archive '+name,ab==group['archive'])
  pending.append({'group':name,'candidate':b,'archive':ab,'identities':deepcopy(group['identities']),'qualification':'Complete pending Greater Earth/Water context, not accepted source or an executable main-case premise.'})
 context={}
 for name in ['companion-life10-exact-05/SPELLS_MODEL.json','companion-life10-exact-05/CASEBOOK.json',
   'companion-life10-exact-05/REGISTER.json','GPT_PART5_PERTINENT_RETURNS_01_RECEIPT.json',
   'copy-ready-preparation-only-part5-successor-01/POLICY_SELECTION.json','COPY_READY_PREPARATION_ONLY_PART5_01_LOCAL_PREFLIGHT.json',
   'copy-ready-preparation-only-part5-successor-01/successor/CONTROL15_READY_REFERENCE_SUCCESSOR14.json',
   'CONTROL15_PART5_FULL_RETURN_02_LOCAL_RECEIPT.json','RANK7_IDENTITY_CASTING5_PART5_RETURN_01_SEMANTIC_REVIEW_68.json',
   'RANK7_IDENTITY_CASTING5_LOCAL_CORRECTIONS_01_PREPARATION.json','DD_Rank7_Identity_Casting5_Local_Corrections_01.zip',
   'GPT_PART5_RANK7_IDENTITY_CORRECTIONS_12_REQUEST.txt','RANK8_DAMAGE6_PART5_RETURN_01_SEMANTIC_REVIEW_59.json',
   'DD_Rank8_Damage6_Local_Corrections_01.zip','GPT_PART5_RANK8_DAMAGE_CORRECTIONS_11_DISPATCH_NATIVE.json']:
  context[name]=bind(A/name)
 context['qualification']='Complete accepted-but-unapplied Companion/Control and owner Ready policy remain within scope. The five independent content/contest holds remain. Rank7 full return/correction archive has three unresolved local findings; Rank8 has eight pending correction findings. Neither is accepted authority. Do not execute archived code or treat structural reports as engine tests.'
 for name in ['candidate.json','shared_rules.json','supplements.json']:bind(R/'data/public/feat_candidates/exact_01'/name)
 for name in ['CURRENT_COSMOLOGY_READ_FIRST.md','EPILOGUE_RELIC_NULL_REVIEWED_01.md','SOULS_RESEARCH_REVIEWED_01.md']:
  bind(R/'docs/director-only/cosmology'/name)
 for name in ['epilogue_relic_null_reviewed_01.json','souls_research_reviewed_01.json']:bind(R/'data/director/cosmology'/name)
 questions=[{'id':i,'spellIds':ids,'exactSourceOrConflict':s,'options':opts,'recommendationAndConsequences':rec,'decisionSelected':False} for i,ids,s,opts,rec in Q]
 ck('24 unique unselected decisions',len(questions)==len({q['id'] for q in questions})==24 and not any(q['decisionSelected'] for q in questions))
 ck('Both source identities fully covered',set().union(*(set(q['spellIds']) for q in questions))==set(IDS))
 ck('Eleven applied comparisons',len(counterparts)==11)
 ck('Four actual complete base pet profiles',set(IDS).isdisjoint(counterpart_ids) and set(counterpart_ids[:4])=={'summon-fire-pet','summon-air-pet','summon-earth-pet','summon-water-pet'})
 candidate={'id':'RANK9-ELEMENTAL-PETS2-SOURCE-CONFERENCE01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
  'status':'SOURCE_CONFERENCE_PREPARED_UNSENT','developmentDirection':'video-game-only','records':records,
  'historicalWorkflowQualification':'Original pre-push and Water-pending questions preserved unchanged as history. Actual authorized GitHub backup through65 and current applied Water03 govern status; no new cosmology is selected.',
  'currentAcceptedInterfaceComparisons':inherited,'completeAppliedCounterparts':counterparts,'completeClassFeatureComparisons':classcomparisons,
  'pendingComparisonsNotAuthority':pending,'laterCompleteReviewContext':context,'questions':questions,'riskCounts':{'C':2},
  'sourceFindings':FINDINGS,'futureCaseRequirements':CASES,
  'semanticDelta':[{'spellId':sid,'riskTier':'C','riskReason':TIERS[sid][1],'startingPoint':'Full native source and historical question; no complete authored procedure or cases.',
    'genuineQuestionIds':[q['id'] for q in questions if sid in q['spellIds']]} for sid in IDS],
  'earlierOperationalWorkedCases':[],'currentVectors':[],'countsUnchanged':deepcopy(index['authoredCounts']),
  'sourceBindings':list(sources.values()),'newRuleAdoptions':0,'runtimeTestsExecuted':0,'humanPlaytests':0,'sourceInformationDeleted':0,'cosmologyDecisions':0,'wholeGameComplete':False}
 root.mkdir();frozen=[]
 for b in sources.values():
  p=G/b['path'];ck('Current complete source '+b['path'],info(p)==b)
  dst=root/'sources'/b['path'];target=Path('\\\\?\\'+str(dst.resolve()));target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(p.read_bytes())
  ck('Frozen complete source bytes '+b['path'],target.read_bytes()==p.read_bytes());frozen.append({**b,'frozenCopy':dst.relative_to(G).as_posix()})
 for p,b in protected.items():ck('Protected canonical/queue/checkpoint source unchanged '+p.name,p.read_bytes()==b)
 out.write_bytes(enc(candidate));check.write_bytes(enc({'candidate':info(out),'checks':checks,'checkCount':len(checks),
  'sourceCount':len(sources),'sourceIdentities':2,'placements':2,'questions':24,'riskCounts':{'C':2},'failures':0,
  'earlierCompleteProcedures':0,'newCurrentVectors':0,'validationScope':'Source/access/context preservation only; no selected semantics or runtime test.'}))
 manifest=root/'MANIFEST.json';manifest.write_bytes(enc({'candidate':info(out),'check':info(check),'files':list(sources.values()),'frozenSources':frozen,'sourceCount':len(sources),'newRuleAdoptions':0}))
 readme='Two full rank9 elemental-pet identities,2 native placements,24 unselected questions,11 complete applied comparisons and2 complete pending greater-pet conference archives. Both tierC. Preserve all four base bodies and an actual usable two-spell Fusion with concentration continuity. Complete class/body/custody/Null/copy/clock/action sources are bound. No selected procedure,case,runtime,canon or balance approval.\n'
 (root/'README.md').write_text(readme,encoding='utf-8',newline='\n')
 with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p,name in [(out,'CANDIDATE.json'),(check,'SOURCE_CHECK.json'),(manifest,'MANIFEST.json')]:z.write(p,name)
  z.writestr('README.md',readme)
  for b in sources.values():z.writestr('sources/'+b['path'],(G/b['path']).read_bytes())
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None and len(z.namelist())==len(set(z.namelist())) and z.read('CANDIDATE.json')==out.read_bytes()
  for b in sources.values():assert z.read('sources/'+b['path'])==(G/b['path']).read_bytes()
 ab=info(archive)
 request.write_text(f'Review {archive.name}, {ab["bytes"]} bytes SHA256 {ab["sha256"]}. Read both complete original identities/placements,all24 unselected decisions,11 full applied comparisons,seven actual class-feature comparisons and2 full pending greater-pet archives. Preserve Elemental Convergence ALL FOUR BASE PETS at once for1minute WITHOUT concentration. Preserve Elemental Fusion actual pet merge,shared stats and a real two-spell-per-round benefit with its printed concentration1minute. Both are Conjuration rank9,class17 for Druid/Mage/Wizard,base26RP,Action,120feet,V/S/F. Actual current base Water is applied; historical pending wording is not current. Explicitly resolve missing profile fields,arrival/caps/commands,concentration bridge,body/stat/resource maps,action opportunities and composition,components,damage/heal/Null,dealer provenance,source clocks,dispel/suppression,ending and split placement. Do not substitute one chosen pet,only a two-cast cap,free full-health bodies,unacquired Wizard features or arbitrary monster statistics. The separate Mage Hero damage card is distinct. Rank7/Rank8 unresolved correction contexts are comparisons only. Return every decision,full selected procedures and artifacts,exact reversible operations,at least two complete useful positive encounters per identity and meaningful independent branches with full legal actor acquisition and actual state ledgers. Preserve all originals and owner implementation reservation; distinguish source/semantic/arithmetic/specification/engine/human/balance/cosmology/release gates. This packet is prepared UNSENT until separately submitted.\n',encoding='utf-8',newline='\n')
 prep.write_bytes(enc({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PREPARED_UNSENT','candidate':info(out),'archive':ab,'manifest':info(manifest),'check':info(check),'request':info(request),'sourceCount':len(sources),'identityCount':2,'placementCount':2,'questionCount':24,'riskCounts':{'C':2},'allArchiveMembersVerified':True,'newRuleAdoptions':0,'sourceInformationDeleted':0}))
 print(json.dumps({'preparation':info(prep),'candidate':info(out),'archive':ab,'sources':len(sources),'checks':len(checks),'questions':24,'failures':0}))

if __name__=='__main__':main()
