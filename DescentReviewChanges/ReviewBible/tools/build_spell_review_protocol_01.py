"""Freeze authority and inventory for the user's accelerated review protocol.

This builds indexes, not new game rules or an execution engine.
"""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
from copy import deepcopy
import hashlib,json,re,zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded

P=R/'data/director/spell_review'; O=A/'accelerated-review-01'
def read(p): return json.loads(p.read_bytes())
def at(obj,pointer):
 for t in pointer.strip('/').split('/') if pointer else []:
  t=t.replace('~1','/').replace('~0','~');obj=obj[int(t)] if isinstance(obj,list) else obj[t]
 return obj
def section(path,heading):
 text=path.read_text(encoding='utf-8-sig');lines=text.splitlines(keepends=True)
 hits=[i for i,l in enumerate(lines) if l.rstrip()==heading];assert len(hits)==1,(path,heading,hits)
 start=hits[0];level=len(heading)-len(heading.lstrip('#'));end=len(lines)
 for i in range(start+1,len(lines)):
  m=re.match(r'^(#+) ',lines[i])
  if m and len(m[1])<=level:end=i;break
 return ''.join(lines[start:end]),start+1

def main():
 assert not O.exists() and not (P/'accepted_interface_registry_01.json').exists()
 O.mkdir(parents=True);P.mkdir(parents=True,exist_ok=True)
 now=datetime.now(timezone.utc).isoformat();checks=[];bindings={};entries=[];inactive=[]
 def check(name,passed,detail=None):checks.append({'check':name,'passed':bool(passed),**({'detail':detail} if detail is not None else {})})
 def freeze(path):
  rel=path.relative_to(G).as_posix()
  if rel not in bindings:
   q=O/'sources'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(path.read_bytes())
   bindings[rel]={**info(path),'frozenCopy':q.relative_to(G).as_posix()}
   check('frozen bytes '+rel,q.read_bytes()==path.read_bytes())
  return deepcopy(bindings[rel])
 original=Path(r'C:\Users\cbord\.codex\attachments\40f7ba60-b8f1-4fa2-a4a1-26e9910fdd0c\Pasted text.txt')
 protocol=R/'docs/mechanics/SPELL_REVIEW_PROTOCOL.md'
 assert not protocol.exists();protocol.write_bytes(original.read_bytes())
 check('user protocol preserved byte-for-byte',protocol.read_bytes()==original.read_bytes());freeze(protocol)
 ac4=R/'data/public/spell_candidates/abjuration_conjuration_rank4_reviewed_03.json'
 ac5=R/'data/public/spell_candidates/abjuration_conjuration_rank5_reviewed_05.json'
 ban=R/'data/public/spell_candidates/banishment_exact_model_04.json'
 receipts={}
 for key,name in [('AC4','AC4_EXACT_ACCEPTANCE_03_RECEIPT.json'),('AC5','AC5_EXACT_ACCEPTANCE_05_RECEIPT.json'),('Banishment','BANISHMENT_EXACT_ACCEPTANCE_04_RECEIPT.json')]:
  path=A/name;receipt=read(path);receipts[key]=freeze(path)
  for b in receipt['acceptedArtifactBindings']:
   check(key+' accepted artifact '+b['path'],info(G/b['path'])==b);freeze(G/b['path'])
  check(key+' acceptance authority binding',info(G/receipt['acceptanceAuthority']['path'])==receipt['acceptanceAuthority'])
  freeze(G/receipt['acceptanceAuthority']['path'])
  for pair in receipt['canonicalCopies']:
   check(key+' canonical copy '+pair['destination']['path'],(G/pair['source']['path']).read_bytes()==(G/pair['destination']['path']).read_bytes())
 def add(id,name,path,selector,scope,trigger,inputs,outputs,lifecycle,exceptions,usedBy,evidence=None,extensions=None):
  source=freeze(path)
  if selector.startswith('/'):
   exact=at(read(path),selector);location={'pointer':selector}
  else:
   exact,line=section(path,selector);location={'heading':selector,'line':line}
  raw=encoded(exact) if not isinstance(exact,str) else exact.encode('utf8')
  entries.append({'id':id,'name':name,'acceptanceStatus':'accepted-authored-campaign-playtest' if evidence else 'current-authoritative-provisional-interface',
   'acceptanceBasis':receipts[evidence] if evidence else {'basis':'Current operative integration text, reused by exact accepted cohorts; not a new claim of whole-document or canon approval.','cohortEvidence':[receipts['AC4'],receipts['AC5']]},
   'scope':scope,'currentAuthoritativeSource':{**source,**location},'exactAuthority':exact,'authoritySha256':hashlib.sha256(raw).hexdigest(),
   'trigger':trigger,'inputs':inputs,'outputs':outputs,'lifecycle':lifecycle,'exceptions':exceptions,'knownSourceSpecificExtensions':extensions or [],
   'usedBy':usedBy,'usageCoverage':'Explicit known users, not a claim of exhaustive reverse-dependency indexing.','reusableWithinScope':True,
   'summaryAuthority':'The exactAuthority and named source control; normalized fields index them and create no rules.','runtimeImplementedByRegistry':False})
 spell=R/'docs/mechanics/SPELL_INTEGRATION_RULES.md';combat=R/'docs/mechanics/COMBAT_ACTION_PLAYTEST.md';core=R/'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md';body=R/'docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md';null=R/'docs/mechanics/COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md';classes=R/'docs/mechanics/CLASS_PLAYTEST_RULES.md';conditions=R/'docs/mechanics/CONDITIONS_PLAYTEST.md'
 # Resource/heading IDs are stable addresses where the source has no named interface ID.
 defs=[
 ('spell-cast','Ordinary casting and pricing',spell,'## Resolve a cast at the table','Ordinary class-qualified casts','Legal cast commitment','Class/rank, repertoire, actions, components, pre-cast Dissonance, prior spell name, costs','Committed resources/concentration/cadence; attack/save/effect resolution','No refund/restoration on miss/save/interruption; generating rank retained','Exact class exceptions; no generic overcast',['AC4','AC5','all ordinary spells']),
 ('ready','Ready',combat,'## Ready','Ordinary Ready and held spells','Action preparation, perceivable trigger, Reaction release','Spell/mode, paid cost, next own regular START, release-time target/area legality','One pending Ready; paid spell held in concentration; target selected at release','Expiry next own regular START; effect duration begins at release; no second cast','Specific interrupt overrides ordinary trigger-first order',['AC5','AC6-N15 (candidate)']),
 ('falling','Falling',spell,'## Falling bridge — new provisional procedure','Unsupported bodies and printed Feather Fall interaction','Loss of support without a working aloft permission','Enclosing regular slot, support, movement mode, total/uncontrolled distance','Fixed next-round END marker; ordinary up-to300ft step; capped impact dice','Support/flight ends fall; original marker persists; positive impact Prone','Feather Fall has its exact Action/60ft/momentum and impact rules',['AC5','AC6-N15 (candidate)','Planar Barrier (candidate)']),
 ('time','Time and event ordering',combat,'## Time and event ordering — NEW','Original regular markers and elapsed time','A timed event or expiry becomes due','Regular schedule, original marker, phase, extra-turn status','Ordered due events without duplicate ticks','Preserve original markers through reorder/absence','Exact source-specific typed event order remains scoped',['AC4','AC5']),
 ('movement','Movement and geometry',combat,'## Movement and geometry','Ordinary movement, footprint and squeeze rules','Attempted movement/placement','Actual body, route, remaining movement, terrain, squeeze/crawl','Legal displacement and actual movement expenditure','No free budget reset from extra events','Spell-specific nonpath transport uses its own source',['AC4','AC5']),
 ('damage','Damage event and Wounds',core,'## Resolve a damage event','Ordinary real damage packets','One genuinely separate hit/damage event','Defenses, pre-event HP/Wounds, tempHP, maxHP, Maiming, critical flag','Ordered HP/InstantDeath/Wound/death-counter result','Single packet processed once; source lifecycle still applies','Qualifying Null endpoint overrides only its specified consequences',['AC4','AC5']),
 ('zero','Zero HP and recovery',core,'## Zero HP and recovery','Ordinary living character/significant NPC states','Zero HP, actual regular START, healing or stabilization','Dying/Stable/Dead, counters, HP, recovery deadline','Ordinary Unconscious; source-legal death saves, Stable recovery and reset','Absolute recovery clock; no extra-turn death saves','Finite summon NullDisabled0 is a separate exact source lifecycle',['AC4','AC5','AC6-N19 (candidate)']),
 ('rolls','Attack/save/task procedures',core,'## Rolls','Actual roll types','Source requires an attack, save or task check','Dice, modifiers, AC/DC, advantage/disadvantage','Actual source result; only task checks use ordinary degree shifts','Replace dice before consequences, no duplicate event','Death-save natural results are expressly separate',['all ordinary spells']),
 ('concentration','Concentration and control',classes,'## Targets, concentration and control','Shared concentration and bounded control','New concentration, damage check or condition ending','Old slot, source exception, actual damage/CON save, source-target guard','End incompatible old concentration at commitment; exact control effects','No restoration after failed new cast; source-specific linked effects only','Explicit limited class exceptions remain operative',['AC4','AC5','DE4 (unaccepted proposal)']),
 ('null-root','Null Veil damage provenance',null,'### Null Veil','Qualifying damage roots','Creation of actual damage root','Actual dealer, current operative Veil, root/descendant identity','Recorded Null flag retained by genuine descendants','Later dealer Veil changes do not rewrite existing root','Named dealer/source-specific creation checkpoints only',['AC5','AC6 (candidate)','DE4-N25 (proposal)']),
 ('null-life','Null recipient lifecycles',null,'### Recipient lifecycles for qualifying Null damage','Qualifying Null damage recipients','Null-marked packet reaches actual recipient','Body type/source, actual HP/tempHP, current zero state, root','Source-scoped nonlethal endpoint without phantom death/resources','Same extant body; true expiry/removal continues','Does not globally make every construct/summon living',['AC4','AC5','AC6 (candidate)']),
 ('companions','Components, companions and hard control',spell,'## Components, summons and ongoing effects','Ordinary component and companion overlay','Cast, companion command or hard control establishment','Actual profile, owner BA, round offense, body/deadline, history','One owner command/offense with exact multiattack exception','Same owner/round history survives replacement; no loot/resource loops','Named source profiles replace missing-value defaults; no universal CR profile',['AC4','AC5','DE4 (proposal)']),
 ('rerolls','Mark Omen and Fate Coin',spell,'## Mark Omen and Fate Coin: reviewed spell-specific rerolls','Only the accepted two-spell reroll family','Eligible source-specific reroll activation','Original event/lineage, perception, physical die where required, owner resources','One permitted reroll using each source exact eligibility','No replay/refund/lineage reset','Fate Reversal extension is proposed, not accepted',['Mark Omen','Fate Coin']),
 ('placement','Body placement and involuntary endings',body,'## Placement and involuntary endings','Actual anatomy/placement changes','Mandatory or voluntary body/placement transition','Body extent, original space, squeeze, nearest adjacent legal region','Legal placement or explicit conflict; no wall passage','Mandatory source ending remains real','Banishment conflict has separately accepted logical-anchor semantics',['AC4','Banishment','AC5']),
 ('cargo','Carrying and Load',body,'## Carrying and Load','Actual body/item custody and Load','Take, carry, release or transform cargo','Real items, weight, Load, hands, body/source limits','Source-legal custody and movement effects','Same items persist unless an actual source consumes/removes them','Summon/portal caps add their own explicit constraints',['AC4','AC5'])]
 aliases={}
 for short,name,path,heading,scope,trigger,inputs,outputs,life,exc,users in defs:
  id=path.relative_to(R).as_posix()+'#'+heading.lstrip('# ').lower().replace(' ','-');aliases[short]=id
  add(id,name,path,heading,scope,trigger,inputs,outputs,life,exc,users)
 for condition in ['Blinded','Frightened','Paralyzed','Prone','Stunned']:
  add('docs/mechanics/CONDITIONS_PLAYTEST.md#'+condition.lower(),condition,conditions,'## '+condition,'Exactly the named condition','Actual source establishes/ends this condition','Source identity, immunity, duration, current body/permissions','Only printed condition consequences','Source clock/removal and shared condition handling','No extra invented rider or blanket creature-type immunity',['next damage/control cohort'])
 add('AC4-ALIGN-01','Effective alignment with Lock/Anchor',ac4,'/sharedRules/alignment','Alignment Lock/Anchor target-side final snapshots','Read effective alignment under an actual eligible Lock/Anchor','Underlying AP-AS history, locked axes, eligible application order','Earliest eligible lock per axis applied last','Underlying history continues; expiry exposes then-current values','No global moral or cosmological inference',['AC4','AC5','DE4 (proposal)'],'AC4')
 add('AC4-SUMMON-TARGET-01','AC4 healing-target completion',ac4,'/sharedRules/summonTargeting','Only AC4 Water Pet and Faction Envoy','Ordinary living-ally/active-creature targeting','Same extant finite body, source deadline, target conditions','Mechanical eligible target without inventing soul/biology','NullDisabled0 same-body; ended body no longer target','No extension beyond named profiles',['AC4'],'AC4')
 for n,label in [(2,'Dimensional Anchor'),(4,'Resonance Dampening Field')]:
  s=read(ac4)['spells'][n];add(s['spellId']+'#procedure',label,ac4,f'/spells/{n}/procedure','Only '+label,'Exact spell application/endpoint or pricing checkpoint','Actual geometry, source state and predicates printed in procedure','Exact bounded outcome in authoritative procedure','Original source duration/concentration; no inferred reset','No generalization to other spells',['AC4','AC5','DE4 (proposal)'],'AC4')
 a5=read(ac5)
 # Exact accepted rule nodes, preserving original IDs and excluding superseded nodes.
 for key,value in a5['sharedRules'].items():
  if 'superseded by' in value.get('status','').lower():inactive.append({'id':key,'source':freeze(ac5),'pointer':'/sharedRules/'+key,'status':value['status']});continue
  users=[s['id'] for s in a5['spells'] if key in json.dumps({k:v for k,v in s.items() if k not in ['historicalQuestion','historicalProposalEvidence']},ensure_ascii=False)]
  add(key,value.get('classification',key),ac5,'/sharedRules/'+key,value.get('classification',key).replace('NEW ','Accepted scoped '),
   {'authority':'exactAuthority.rule','instruction':'Use only the event/checkpoint expressly identified by this accepted rule.'},
   {'authority':'exactAuthority.rule','instruction':'All source-named participants, geometry, history and resource records; no inferred missing input.'},
   {'authority':'exactAuthority.rule','instruction':'Exactly the accepted stated result; no promotion to global behavior.'},
   {'authority':'exactAuthority.rule','instruction':'Retain each stated identity, clock, operation snapshot and cleanup rule.'},
   {'authority':'exactAuthority.rule','instruction':'All named scope restrictions and overrides apply.'},users or ['AC5'], 'AC5')
 for n in [0,2,13,15]:
  s=a5['spells'][n];add(s['id']+'#procedure',s['name'],ac5,f'/spells/{n}/procedure','Only '+s['name'],'Exact activation/operation in source procedure','Actual source class rank, cost, eligible targets, geometry and current state','Exact source procedure result','Original identity, concentration/deadline and operation snapshots','No transport/antimagic/pricing classification exported beyond stated scope',['AC5','AC6 (candidate)'],'AC5')
 bp=read(ban)['procedure']
 for key in ['cell','admission','closure','transportClassification']:
  v=bp[key];add(v['ruleId'],key,ban,'/procedure/'+key,'Ordinary Banishment; only AC5-BANISH-EXT-01 extends its named portions','Exact Banishment '+key+' event','Existing identities/plane references, source predicates and real placement','Exact '+key+' result without inferred cosmology','Real source ending and clocks continue','No body creation or ignored physical placement',['banishment','banish-elemental','elemental-banishment'],'Banishment')
 for key,field in [('BAN-CONFLICT-04','placementConflictState'),('BAN-PLACEMENT-HANDOFF-03','creaturePlacement')]:
  add(key,field,ban,'/procedure/closure/'+field,'Banishment-origin closure only','Mandatory closure placement','Same body, closure anchor, actual terrain/occupancy/anatomy','Logical conflict or legal inherited placement','Cell still ends; identity and real clocks persist','No global untargetability, soul/native-plane claim or free movement',['banishment','AC5 named exiles'],'Banishment')
 # Inventory uses the authored index, not historical catalog selection labels.
 catalog=R/'data/public/spell_playtests/catalog.json';index=R/'data/public/spell_playtests/authored_review_index.json'
 c=read(catalog);idx=read(index);freeze(catalog);freeze(index);by={s['id']:(n,s) for n,s in enumerate(c['spells'])};ie={s['id']:s for s in idx['entries']}
 check('catalog/index exact identity coverage',set(by)==set(ie));check('unique catalog IDs',len(by)==len(c['spells']));check('unique exact names',len({s['name'] for s in c['spells']})==len(by))
 reviewed=[s['id'] for s in idx['entries'] if s['authoredStatus']=='reviewed-authored-operational-playtest'];pending=[s['id'] for s in idx['entries'] if s['id'] not in reviewed]
 ac6=read(A/'ac6-semantic-current-06/SPELLS_MODEL.json');ac6ids=[s.get('id',s.get('spellId')) for s in ac6['spells']]
 check('AC6 remains pending in local authored index',set(ac6ids)<=set(pending))
 inventory={'recordedAtUtc':now,'catalog':info(catalog),'authoredIndex':info(index),'uniqueIdentities':len(by),'printedPlacements':sum(len(s['source']['original']['placements']) for s in c['spells']),'classAccessPlacements':sum(len(s['classAccess']) for s in c['spells']),
  'reviewedRecordedCount':len(reviewed),'pendingRecordedCount':len(pending),'ac6ExactReceiptState':'GPT later conversation reports completion, but exact returned archive/bindings not yet recovered. Do not count as verified accepted or adopt.','ac6Identities':ac6ids,'conditionalRemainingAfterVerifiedAC6':len(pending)-len(ac6ids),'reviewedIds':reviewed,
  'pending':[{'id':id,'name':by[id][1]['name'],'catalogPointer':f'/spells/{by[id][0]}','placements':by[id][1]['source']['original']['placements'],'classAccess':by[id][1]['classAccess'],'indexStatus':ie[id]['authoredStatus'],'riskTier':'not-yet-assessed','authoringAllowedBeforeTierAssessment':False} for id in pending],
  'runtimeSelectionStatusCounts':dict(Counter(s['status'] for s in c['spells'])),'statusCaveat':'Historical runtime-selection labels are not authored-review counts.'}
 # Next interaction-based cohort: mixed A/B, 25 identities, no systemic C rules silently authored.
 rows=[
 ('orb-of-annihilation','A','Single-target type/perception/LoE completion; retain DEX half and 8d8 force.'),
 ('voltaic-detonation','B','Exact detonation target/area and resolution; one-turn Stunned endpoint with inherited hard guard.'),
 ('frozen-tomb','B','Exact two-round Paralysis endpoint; separate cold/condition immunity; no new time-freeze semantics.'),
 ('meteor-spear','B','Line width/occupancy and resolution; preserve enemy-only and both printed damage pools.'),
 ('arc-surge','A','Source enemy predicate and automatic-versus-authored save decision; preserve 40ft reach.'),
 ('cone-of-cold','A','Exact cone origin/body inclusion and source-unspecified resolution; no imported external rules.'),
 ('destructive-wave','B','Target/area scope and thunder/radiant allocation; Prone inherits condition, no push added.'),
 ('solar-flare','B','Blindness endpoint and damage/condition resolution; preserve enemy-only60ft.'),
 ('chain-lightning','B','Secondary-target range, distinct set, selection/order and resolution; do not borrow random Chain Arc behavior.'),
 ('sunbeam','B','Line width, Blindness endpoint and resolution; source is instantaneous, do not invent recurring beam.'),
 ('freezing-sphere','B','Exact water-freezing volume, persistence/support and creature interaction; no arbitrary global ice rules.'),
 ('blight','A','Exact plant eligibility and printed greater-damage amount; source-unspecified save/target scope.'),
 ('soulfire-nova','B','Explosion geometry and undead-only Blindness endpoint; title grants no soul ontology.'),
 ('circle-of-death','A','Center selection, inclusion and source-unspecified resolution; retain 60ft sphere.'),
 ('mental-bomb','B','Core explicitly says Reaction but supplies no trigger; resolve local trigger and next-Reaction loss endpoint.'),
 ('veil-of-terror','A','Frightened and psychic components, initial WIS outcome, concentration/end saves only as authored.'),
 ('phantom-swarm','B','Target set and exact compulsory movement opportunity/distance/safety; no free Action or indefinite instruction.'),
 ('invisible-tide','A','30ft inclusion and DEX failure Prone; no real water/body displacement from illusory title.'),
 ('wail-of-the-damned','A','30ft targets, WIS outcome, one-round Stunned endpoint and independent psychic component.'),
 ('horrid-wilting','B','Two matching Abi-Dalzim historical aliases need explicit metadata comparison; do not silently merge names.'),
 ('elemental-devastation','A','Permitted elemental type choice, enemy eligibility and resolution; preserve separate roll per enemy.'),
 ('supernova-lance','B','Line width/resolution and exact20ft push direction; inherit collision/Falling, no invented impact damage.'),
 ('crystalline-flash','B','Explosion dimensions, radiant/cold choice, Blindness endpoint and resolution.'),
 ('sunburst','B','Sphere placement, resolution and Blindness endpoint; preserve 12d6/60ft radius.'),
 ('death-tide','A','100ft radius placement/inclusion and resolution; no instant-death or soul rider from name.')]
 selected=[]
 for id,tier,gap in rows:
  n,s=by[id];check('next cohort pending '+id,id in pending);check('source identity '+id,s['source']['catalogKey']==id)
  for cl,a in s['classAccess'].items():
   check(id+' '+cl+' source rank',a['rank']==s['source']['original']['classRanks'][cl]);check(id+' '+cl+' source school',a['school']==s['source']['original']['classSchools'][cl]);check(id+' '+cl+' minimum class level',a['minimumClassLevel']==s['source']['original']['classLearnLevels'][cl]);check(id+' '+cl+' base RP',a['baseRpCost']==c['costByRank'][str(a['rank'])] if isinstance(c['costByRank'],dict) else a['baseRpCost']==c['costByRank'][a['rank']])
  selected.append({'id':id,'name':s['name'],'riskTier':tier,'sourcePreserved':True,'source':deepcopy(s),'sourcePointer':f'/spells/{n}','existingInterfacesSufficient':'For common engine only; card parameters below remain unresolved.','inheritedInterfaces':[aliases[k] for k in ['spell-cast','rolls','damage','zero','concentration','null-root','null-life','time','movement']]+['AC5-ANTIMAGIC-IO-04','greater-dispel#procedure'],
   'newScopedAuthorshipRequired':gap,'substantialNewSystemicRuleAuthorized':False,'caseObligations':['Preserve every existing cohort case and material obligation when migrated.','Add real-source fixtures for the specific unresolved parameters; no fabricated interrupt/ability.'],'authoringState':'inventory/preflight only; no new operative procedure authored'})
 for x in inventory['pending']:
  if x['id'] in {r['id'] for r in selected}:x.update(riskTier=next(r['riskTier'] for r in selected if r['id']==x['id']),proposedCohort='damage-control-25-01')
 registry={'schemaVersion':1,'recordedAtUtc':now,'protocol':info(protocol),'purpose':'Reuse current exact scoped interfaces; this index creates no game rules and performs no runtime execution.','entries':entries,'inactiveHistoricalInterfaces':inactive,'pendingExtensions':[{'id':'DE4-GUARD-01','status':'unaccepted; substantial shared-rule proposal requires user conference before further authorship/adoption','source':info(A/'DE4_FATE_GUARD_AMENDMENT_DRAFT_02.json')},{'id':'AC6','status':'exact review receipt recovery pending; no unverified AC6 entry registered as accepted'}],'idPolicy':'Reuse existing IDs. For unnamed interfaces use exact existing resource/heading addresses rather than cosmetic new game-rule IDs.'}
 for e in entries:
  for field in ['id','name','acceptanceStatus','scope','trigger','inputs','outputs','lifecycle','exceptions','knownSourceSpecificExtensions','usedBy','exactAuthority']:check('interface field '+e['id']+' '+field,field in e)
 check('unique registry IDs',len({e['id'] for e in entries})==len(entries))
 known={e['id'] for e in entries}
 for s in selected:
  for dep in s['inheritedInterfaces']:check(s['id']+' dependency '+dep,dep in known)
 # Preserve newly identified example findings without changing any procedure.
 de4=R/'data/director/spell_proposals/divination_enchantment_rank4_current_03.json';freeze(de4)
 findings=[{'id':'DE4-EX-ACCESS-04','classification':'EXAMPLE ERROR','severity':'material','source':info(de4),'pointer':'/currentExamples/24','evidence':'N25 makes caster C use Illusion then Enchantment Phantasmal Killer. Preserved class access gives Monk Illusion and the listed other classes Enchantment; no dual-mode access is supplied.','disposition':'Repair example only: legal same-Monk Illusion recast with new root after purge, plus separate Wizard Enchantment branch; preserve prior record and both scenario obligations.','replacementStatus':'Not yet written; no procedure redesign required.'},{'id':'DE4-EX-REPAIR-04','classification':'EXAMPLE ERROR','severity':'fixture completeness','source':info(de4),'pointer':'/currentExamples/23','evidence':'Field Repair source /cards/7 requires touch and Recharge2; current fixture lacks explicit touch/recharge availability.','disposition':'Add actual adjacent touch, Recharge0 before use and Recharge2 consumption; preserve same body and expired Compulsion.','replacementStatus':'Not yet written.'}]
 for p,data in [(P/'accepted_interface_registry_01.json',registry),(P/'ordinary_spell_inventory_01.json',inventory),(P/'damage_control_25_semantic_delta_01.json',{'id':'damage-control-25-01','status':'Proposed risk-tiered next large cohort; source-frozen preflight, no operative authorship','riskCounts':dict(Counter(s['riskTier'] for s in selected)),'identities':len(selected),'placements':sum(len(s['source']['source']['original']['placements']) for s in selected),'spells':selected}),(O/'DE4_EXAMPLE_FINDINGS_04.json',findings)]:p.write_bytes(encoded(data))
 freeze(A/'DE4_FATE_GUARD_AMENDMENT_DRAFT_02.json')
 (O/'SOURCE_MANIFEST.json').write_bytes(encoded({'recordedAtUtc':now,'sourceCount':len(bindings),'bindings':list(bindings.values())}))
 md=['# Next damage/control cohort — semantic delta','',f'{len(selected)} identities; tiers '+', '.join(f'{k}: {v}' for k,v in Counter(s['riskTier'] for s in selected).items())+'. No new operative rules authored.','', '| Spell | Tier | Source preserved | New scoped authorship required |','|---|---|---|---|']
 md += [f"| {s['name']} | {s['riskTier']} | yes | {s['newScopedAuthorshipRequired']} |" for s in selected]
 md += ['', 'Common casting, damage/Null, condition, timing and suppression rules are inherited by exact registry references. Only the listed card-specific gaps require semantic decisions. Substantial systemic changes require user conference first.','', 'The existing DE4 work and all original scenarios remain preserved. DE4 guard, Seal and control-clock proposals are not treated as accepted infrastructure.','']
 (O/'SEMANTIC_DELTA.md').write_text('\n'.join(md),encoding='utf8')
 errors=[c for c in checks if not c['passed']]
 report={'recordedAtUtc':now,'checkCount':len(checks),'failureCount':len(errors),'checks':checks,'scope':'Source byte freeze, existing acceptance artifact/canonical bindings, identity/access/price arithmetic, index inventory, registry schema and dependency resolution. No spell procedure, case arithmetic, runtime or semantic acceptance claimed for the unbuilt next cohort.','notYetRun':['Next-cohort worked-case arithmetic and geometry (cases not authored yet)','Next-cohort semantic review','Runtime execution','Human playtesting','Numerical balance testing'],'sourceCount':len(bindings),'registryCount':len(entries),'inventoryCounts':{'total':len(by),'recordedReviewed':len(reviewed),'recordedPending':len(pending)},'riskCounts':dict(Counter(s['riskTier'] for s in selected)),'newSpellAdoptions':0,'sourceInformationDeleted':0}
 (O/'PREFLIGHT.json').write_bytes(encoded(report));assert not errors,errors[:5]
 summary={'registry':info(P/'accepted_interface_registry_01.json'),'inventory':info(P/'ordinary_spell_inventory_01.json'),'semanticDelta':info(P/'damage_control_25_semantic_delta_01.json'),'protocol':info(protocol),'preflight':info(O/'PREFLIGHT.json'),'sourceManifest':info(O/'SOURCE_MANIFEST.json'),'checks':len(checks),'failures':len(errors),'interfaces':len(entries),'counts':report['inventoryCounts'],'riskCounts':report['riskCounts'],'newSpellAdoptions':0}
 (O/'RECEIPT.json').write_bytes(encoded(summary));print(json.dumps(summary))
if __name__=='__main__':main()
