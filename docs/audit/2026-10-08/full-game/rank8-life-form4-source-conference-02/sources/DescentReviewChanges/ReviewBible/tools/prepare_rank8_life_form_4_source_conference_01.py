"""Prepare four complete native sources, scoped comparisons and unselected choices."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json, zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded
from prepare_ac5_current_interfaces_01 import at
from rank8_life_form_4_questions_01 import IDS,TIERS,Q

def read(p):return json.loads(p.read_bytes())

def main():
 stem='RANK8_LIFE_FORM_4_SOURCE_CONFERENCE_01';root=A/'rank8-life-form4-source-conference-01';out=R/'data/director/spell_review/rank8_life_form_4_source_conference_01.json'
 check,prep,request=[A/(stem+s) for s in ['_CHECK.json','_PREPARATION.json','_REQUEST.txt']];archive=A/'DD_Rank8_Life_Form_4_Source_Conference_01.zip'
 assert not any(p.exists() for p in [root,out,check,prep,request,archive])
 sources={};checks=[]
 def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
 def bind(p):
  b=info(p);sources[b['path']]=b;return b
 catp=R/'data/public/spell_playtests/catalog.json';ip=catp.parent/'authored_review_index.json';qp=R/'data/director/spell_review/remaining_work_queue_28.json';regp=R/'data/director/spell_review/accepted_interface_registry_06.json';cov=R/'data/playtest/game_development_coverage.json'
 protected={p:p.read_bytes() for p in [catp,ip,qp,regp,cov]};catalog,index,queue,registry=map(read,[catp,ip,qp,regp])
 oldpaths=[A/'ILLUSION_NECROMANCY_RANK8_SOURCE_PREPARATION.json',A/'TRANSMUTATION_UNIVERSAL_RANK8_SOURCE_PREPARATION.json'];old=[read(p) for p in oldpaths]
 ck('Applied525 reviewed323 pending249 standalone',index['authoredCounts']=={'reviewed':525,'pending':323} and index['representationCounts']['completeReviewedStandaloneProcedures']==249)
 ck('173 registered scoped interfaces',len(registry['entries'])==173)
 for p in [catp,ip,qp,regp,cov,*oldpaths,Path(__file__),Path(__file__).with_name('rank8_life_form_4_questions_01.py'),R/'rulebook_output.txt',G/'docs/reference/Player_Rulebook_v6_source_text.txt',A/'ACTIVE_AUTHORING_CHECKPOINT_PART5_ACCEPTED_STAGING_35.json',A/'GPT_PART5_PERTINENT_RETURNS_01_RECEIPT.json',A/'PART5_ACCEPTED24_INTEGRATION_STAGING_01_CHECK.json',A/'part5-accepted24-integration-staging-01/INTEGRATION_PLAN.json',A/'GPT_HEALING_FINAL_CLOSURE.md',A/'GPT_MAXIMUM_HP_FINAL_CLOSURE.md',A/'GPT_TRANSFORMATION_SPELL_FINAL_INTERFACES.md',R/'data/playtest/bestiary_public_source_candidate.json']:
  bind(p)
 lines=(R/'rulebook_output.txt').read_text('utf-16').splitlines();reference=(G/'docs/reference/Player_Rulebook_v6_source_text.txt').read_text('utf8').splitlines();records=[]
 for ident in IDS:
  oldindex=next(j for j,v in enumerate(old) if any(s['spellId']==ident for s in v['selectedSpells']));prior=old[oldindex];n=next(n for n,s in enumerate(prior['selectedSpells']) if s['spellId']==ident);historical=prior['selectedSpells'][n]
  card=next(s for s in catalog['spells'] if s['id']==ident);row=next(s for s in queue['rows'] if s['id']==ident);entry=next(s for s in index['entries'] if s['id']==ident)
  ck('Full exact catalog/source/access '+ident,historical['fullSourceAndCurrentAccessRecord']==card==row['completeCurrentSourceAndAccess'])
  ck('No prior complete procedure or assigned conference '+ident,row['currentGroup'] is None and not row['previousAuthoringMapRowUnchanged']['completeEarlierProposalRecords'])
  ck('Pending actual membership '+ident,entry['authoredStatus']=='pending-authored-procedure')
  ck('Exact rank8 level15 base21 '+ident,all(x['rank']==8 and x['minimumClassLevel']==15 and x['baseRpCost']==21 for x in card['classAccess'].values()))
  ck('Exact native classes '+ident,set(card['classAccess'])==({'Cleric','Druid','Wizard'} if ident in ['clone','flesh-to-grave'] else {'Druid','Mage','Wizard'}))
  books=[deepcopy(b) for b in prior['currentBookBindings'] if b['spellId']==ident]
  ck('One native school placement '+ident,len(books)==len(card['source']['original']['placements'])==1)
  for b in books:
   pos=b['currentBookRow']['line']-1;ck('Both full manuscript source lines '+ident,lines[pos]==b['currentBookRow']['exactText']==reference[pos])
  for kind in ['catalog','core']:ck('Underlying exact '+kind+' '+ident,bind(R/card['source'][kind+'Path'])['sha256']==card['source'][kind+'Sha256'])
  ck('No alias merged '+ident,card['source']['possibleHistoricalAliases']==[])
  records.append({'spellId':ident,'riskTier':TIERS[ident][0],'riskReason':TIERS[ident][1],'completeCurrentCatalogSourceAndAccess':deepcopy(card),'currentIndexEntry':deepcopy(entry),'originalQuestionSource':info(oldpaths[oldindex]),'originalQuestionPointer':'/selectedSpells/'+str(n),'completeOriginalSourceQuestionUnchanged':deepcopy(historical),'completeHistoricalCommonQuestionUnchanged':prior['commonOperationalQuestion'],'completeHistoricalScopeExceptionUnchanged':prior['commonQuestionException'],'completeCurrentBookBindings':books,'earlierCompleteProcedures':[],'earlierOperationalWorkedCases':[],'status':'Source conference prepared; all recommendations unselected.'})
 for cls in ['wizard','cleric','druid','mage']:bind(R/('data/public/class_playtests/'+cls+'.json'))
 for name in ['VIDEO_GAME_ONLY_DIRECTIVE.md','CLASS_PLAYTEST_RULES.md','SPELL_INTEGRATION_RULES.md','COMBAT_ACTION_PLAYTEST.md','CORE_RESOLUTION_PLAYTEST.md','CONDITIONS_PLAYTEST.md','BODY_EQUIPMENT_PLAYTEST.md','CREATURE_LIFECYCLE_PLAYTEST.md','HEALING_DEATH_PLAYTEST.md','TRANSFORMATION_SPELL_PLAYTEST.md','CONDITION_RECOVERY_PLAYTEST.md','MAXIMUM_HP_PLAYTEST.md','CHARACTER_CREATION_PLAYTEST.md','COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md']:
  bind(R/'docs/mechanics'/name)
 inherited=[]
 for n in list(range(0,12))+[13,14,36,39,40,47,48]:
  e=registry['entries'][n];b=e['currentAuthoritativeSource'];actual=bind(G/b['path']);ck('Exact current inherited authority '+str(n),all(actual[k]==b[k] for k in ['bytes','sha256']))
  inherited.append({'registryPointer':'/entries/'+str(n),'completeEntryUnchanged':deepcopy(e),'scopeLimit':'Reuse only actual accepted source scope. A new ordinary spell needs explicit source binding; geometry/Null/placement analogies cannot create an ungranted global permission.'})
 counterparts=[]
 for ident in ['polymorph','shapechange','true-polymorph','mass-polymorph','resurrection','true-resurrection','soul-bind','death-ward','stitch-fate','mass-resurrection-denial','enhance-ability','antimagic-field-lesser','greater-dispel']:
  e=next(x for x in index['entries'] if x['id']==ident);ck('Actually reviewed counterpart '+ident,e['authoredStatus']=='reviewed-authored-operational-playtest');p=(ip.parent/e['procedureFile']).resolve();doc=read(p);ptr=e.get('wholeCardPointer',e['procedurePointer']);b=bind(p)
  if e.get('completeEnvelopeBinding'):ck('Exact counterpart envelope '+ident,b==e['completeEnvelopeBinding'])
  if e.get('authoredAcceptanceReceipt'):ck('Exact actual counterpart receipt '+ident,bind(G/e['authoredAcceptanceReceipt']['path'])==e['authoredAcceptanceReceipt'])
  for alias in e.get('caseSourceReferenceAliases',{}).values():bind(G/alias)
  card=deepcopy(at(doc,ptr));op=card.get('operational')
  if isinstance(op,dict):
   for rel in op.get('sourceReview',[])+op.get('reviewEvidence',[]):bind(G/rel)
   if op.get('authoringFile'):bind(R/op['authoringFile'])
  counterparts.append({'spellId':ident,'source':b,'pointer':ptr,'completeCurrentCard':card,'completeSharedRules':deepcopy(doc.get('sharedRules',{})),'indexEntry':deepcopy(e),'qualification':'Exact accepted source scope; no automatic approval for a new spell.'})
 companionroot=A/'companion-life10-exact-05';companion=read(companionroot/'SPELLS_MODEL.json');cap=A/'companion-life10-exact05-part5-return-01/ACCEPTANCE.json';acceptance=read(cap)
 ck('Actual Companion exact acceptance exists',acceptance['acceptedSelectedIdentityCount']==10 and acceptance['artifactMutationCount']==0)
 for name in ['SPELLS_MODEL.json','CASEBOOK.json','SOURCE_HASHES.json','REGISTER.json']:bind(companionroot/name)
 bind(cap);bind(A/'GPT_PART5_EXACT_ACCEPTANCES_01_NATIVE.json')
 exact_companions=[]
 for ident in ['create-undead','grave-gift']:
  n=next(n for n,s in enumerate(companion['spells']) if s['id']==ident);exact_companions.append({'spellId':ident,'source':info(companionroot/'SPELLS_MODEL.json'),'pointer':'/spells/'+str(n),'completeCurrentCard':deepcopy(companion['spells'][n]),'completeSharedRules':deepcopy(companion['sharedRules']),'actualAcceptance':info(cap),'localIntegrationApplied':False,'qualification':'Actually accepted exact candidate with retained content holds, staged but not installed in the live index. Reusing any scope for these four new spells still requires explicit concurrence.'})
 pending=[]
 for groupname in ['body-defense8','vitality-matter10','rank8-memory-control4','rank8-resource6']:
  group=next(g for g in queue['groups'] if g['group']==groupname);b=bind(G/group['candidate']['path']);ck('Exact pending comparison '+groupname,b==group['candidate']);pending.append({'group':groupname,'candidate':b,'identities':group['identities'],'qualification':'Pending proposal comparison only; no accepted extension. Metaburst, later memory/score and other life proposals may not silently supply rules.'})
 questions=[{'id':i,'spellIds':ids,'exactSourceOrConflict':src,'options':opts,'recommendationAndConsequences':rec,'decisionSelected':False} for i,ids,src,opts,rec in Q]
 ck('24 unique unselected decisions',len(questions)==len({q['id'] for q in questions})==24 and all(q['decisionSelected'] is False for q in questions))
 ck('All four identities covered',set().union(*(set(q['spellIds']) for q in questions))==set(IDS))
 findings=['All four source identities and actual class/school/level/price rows remain exact. No earlier complete procedure or operative case is found in the current review queue.','Animal Shapes is plural and willing; no arbitrary monster, CR ceiling, duration or profile follows from the title. Existing named finite forms explicitly grant no Beast tag.','Clone has no printed vessel, costly reagent, maturation interval, independent actor or soul route. Every storage/return completion remains unselected.','Flesh to Grave retains strict currentHP<100, CON save, death AND rising. Nondamage death cannot be replaced with a necrotic damage packet. The resulting undead profile/control/identity must be fully decided.','Perfect Form retains all three physical-stat benefits and ignores Exhaustion effects for the printed minute. Temporary CON capacity is not automatically covered by permanent advancement. Exhaustion6 is a consequential explicit question, not silently excluded.','The older CONDITION_RECOVERY_PLAYTEST paragraph saying every return at Exhaustion6 immediately dies is superseded by actual later HEALING_DEATH protected-return collapse. Both original files are preserved; maximum recomputation itself performs no lethal transition.','Companion10 Exact05 has actual byte-identical acceptance; its exact accepted procedures and holds are included as source-scoped comparisons, with local integration still staged. No rating for its four undead profiles is invented.','All four are individually tierC: choices affect actual body/identity/capacity/life-state transitions. No cosmological identity or topology is decided.']
 candidate={'id':'RANK8-LIFE-FORM4-SOURCE-CONFERENCE01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'SOURCE_CONFERENCE_PREPARED_UNSENT','developmentDirection':'video-game-only','records':records,'currentAcceptedInterfaceComparisons':inherited,'completeAcceptedCounterparts':counterparts,'exactAcceptedCompanionComparisonsNotLocallyApplied':exact_companions,'pendingComparisonsNotAuthority':pending,'questions':questions,'riskCounts':{'C':4},'semanticDelta':[{'spellId':r['spellId'],'riskTier':r['riskTier'],'riskReason':r['riskReason'],'startingPoint':'Complete native sources; no existing full procedure/case.','genuineQuestionIds':[q['id'] for q in questions if r['spellId'] in q['spellIds']]} for r in records],'sourceFindings':findings,'futureCaseRequirements':['At least two full legal-provider deterministic cases per identity after decisions, plus every consequential independent branch.','Animal Shapes:multiple willing targets, real beast mappings, current anatomy and O/T mixed-fit checks, actual gear/mass/HP, same-caster concentration replacement, independent link death/rejection/suppression and no free form/resource refresh.','Clone:distinct source/body anchors, maturity equality, suppressed/destroyed/occupied body, actual completed death versus survival replacement, barrier/identity claim ordering, one living character and no duplicated gear or spent resources.','Flesh to Grave:99 versus100 normalHP with temporaryHP; hidden legality, failed/successful CON, exact nondamage death defenses and original-caster Null classification, real resulting body claim, exact undead profile and no guessed CR.','Perfect Form:STR/DEX/CON actual scores and per-level floors, capacity-only increase/clamp, stacked systemic factors, living Exhaustion4/5/6, protected return collapse, new gain at6, expiry/suppression, actual rest/recovery and independent strain namespaces.','Keep profiles, body geometry, actual return barriers and cosmology-dependent facts as explicit missing-content holds if not supplied; do not label conditional fixtures complete.'],'earlierOperationalWorkedCases':[],'currentVectors':[],'gptCommunication':'Prepared while the real full Control15 review is active in Calibration Review Part5. Not sent, decided, applied or counted as authored review.','sourceBindings':list(sources.values()),'countsUnchanged':deepcopy(index['authoredCounts']),'newRuleAdoptions':0,'runtimeTestsExecuted':0,'humanPlaytests':0,'sourceInformationDeleted':0,'cosmologyDecisions':0,'wholeGameComplete':False}
 root.mkdir();frozen=[]
 for b in sources.values():
  p=G/b['path'];ck('Source unchanged '+b['path'],info(p)==b);dst=root/'sources'/b['path'];dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(p.read_bytes());ck('Exact full frozen source '+b['path'],dst.read_bytes()==p.read_bytes());frozen.append({**b,'frozenCopy':dst.relative_to(G).as_posix()})
 for p,b in protected.items():ck('Protected live authority unchanged '+p.name,p.read_bytes()==b)
 out.write_bytes(encoded(candidate));check.write_bytes(encoded({'candidate':info(out),'checks':checks,'checkCount':len(checks),'sourceCount':len(sources),'sourceIdentities':4,'placements':4,'earlierCompleteProcedures':0,'earlierOperationalWorkedCases':0,'newCurrentVectors':0,'questions':24,'riskCounts':{'C':4},'failures':0,'validationScope':'Full source/access/hash preservation and scoped authority comparison only. No new procedure adoption or runtime execution.'}))
 manifest=root/'MANIFEST.json';manifest.write_bytes(encoded({'candidate':info(out),'check':info(check),'files':list(sources.values()),'frozenSources':frozen,'sourceCount':len(sources),'newRuleAdoptions':0}))
 readme='Four full rank8 life/form sources, four placements and24 unselected decisions. Read CANDIDATE.json and every relevant full source. Thirteen current reviewed counterparts plus two actual accepted Companion10 comparisons retain their own scopes. Complete body, death, maximumHP and protected-return interfaces are supplied; original older contrary recovery wording remains historical. All four individually tierC; no external-game profile, CR, ingredient, duration or cosmology imported. No new procedure, case or rule adopted.\n'
 (root/'README.md').write_text(readme,encoding='utf8',newline='\n')
 with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p,n in [(out,'CANDIDATE.json'),(check,'SOURCE_CHECK.json'),(manifest,'MANIFEST.json')]:z.write(p,n)
  z.writestr('README.md',readme)
  for b in sources.values():z.write(root/'sources'/b['path'],'sources/'+b['path'])
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))
  assert z.read('CANDIDATE.json')==out.read_bytes()
  for b in sources.values():assert z.read('sources/'+b['path'])==(G/b['path']).read_bytes()
 ab=info(archive);request.write_text(f'Review {archive.name}, {ab["bytes"]} bytes SHA256 {ab["sha256"]}. Four exact native sources/placements and24 unselected questions: Animal Shapes, Clone, Flesh to Grave, Perfect Form. Preserve full class access, printed plural/willing beast transformation, stored death insurance, strict<100HP CON death-and-rising, and+4 physical scores/Exhaustion-effect suppression for a minute. Review the full original passages, existing transformation/death/maxHP contracts, all13 reviewed counterparts and two actual accepted Companion10 comparisons. Explicitly decide each new form/lifecycle/return/score/fatal-Exhaustion choice; label new authorship and supply missing content rather than inferring CR or external-game rules. Later protected-return collapse supersedes the older recovery sentence; preserve both histories. Return per-question decisions and full next authoring directions. Do not adopt unseen runtime, local membership, numerical balance, cosmology or whole-game closure.\n',encoding='utf8',newline='\n')
 prep.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PREPARED_UNSENT','candidate':info(out),'archive':ab,'manifest':info(manifest),'check':info(check),'request':info(request),'sourceCount':len(sources),'identityCount':4,'placementCount':4,'questionCount':24,'riskCounts':{'C':4},'allArchiveMembersVerified':True,'newRuleAdoptions':0,'sourceInformationDeleted':0}))
 print(json.dumps({'preparation':info(prep),'candidate':info(out),'archive':ab,'sources':len(sources),'checks':len(checks),'questions':24,'failures':0}))

if __name__=='__main__':main()
