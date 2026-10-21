"""One-shot evidence preparation. Does not import project/downloaded modules or edit rules."""
from pathlib import Path, PurePosixPath
from fractions import Fraction
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib, json, re, zipfile

G = Path(r'C:\Github\DecenniumDescent')
R = G / 'DescentReviewChanges/ReviewBible'
A = G / 'docs/audit/2026-10-08/full-game'
ROOT = A / 'bestiary-complete-source-prepared-v3-81'
ZIP = A / 'DD_Bestiary_Complete_Source_Prepared_v3_81.zip'
RECEIPT = A / 'BESTIARY_COMPLETE_FILE_HANDOFF_V3_PREPARATION_81.json'
CHECK = A / 'BESTIARY_COMPLETE_FILE_HANDOFF_V3_CHECK_81.json'
REPORT = A / 'BESTIARY_CURRENT_SOURCE_INTERFACES_81.json'
REQUEST = A / 'CODEX_BESTIARY_V3_SOURCE_REQUEST_PREPARED_81.txt'
SAVED_SCRIPT = A / Path(__file__).name

def sha(b): return hashlib.sha256(b).hexdigest()
def readj(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def jb(x): return (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
def rel(p): return p.relative_to(G).as_posix()
def info(p):
    b = p.read_bytes()
    return {'path': rel(p), 'bytes': len(b), 'sha256': sha(b)}
checks=[]
def ck(name, ok, detail=None):
    checks.append({'check': name, 'pass': bool(ok), 'detail': detail})
    if not ok: raise AssertionError(name + ': ' + str(detail))
def safe(n):
    p=PurePosixPath(n)
    return not p.is_absolute() and '..' not in p.parts and ':' not in n and '\\' not in n
def write_new(p,b):
    lp=Path('\\\\?\\' + str(p.resolve()))
    lp.parent.mkdir(parents=True, exist_ok=True)
    with lp.open('xb') as f: f.write(b)

for p in [ROOT,ZIP,RECEIPT,CHECK,REPORT,REQUEST,SAVED_SCRIPT]:
    ck('new output absent '+str(p),not p.exists())
v2p=A/'BESTIARY_COMPLETE_FILE_HANDOFF_V2_PREPARATION.json'; v2=readj(v2p)
v2zip=A/v2['bundleFile']; v2bytes=v2zip.read_bytes()
ck('V2 exact archive identity',len(v2bytes)==v2['bundleBytes'] and sha(v2bytes)==v2['bundleSha256'])
payload={}; reasons={}; changed=[]
def add(p,reason):
    b=p.read_bytes(); n='sources/'+rel(p)
    if n in payload: ck('duplicate source agrees '+rel(p),payload[n]==b)
    payload[n]=b
    reasons.setdefault(n,[]).append(reason)
    return n
with zipfile.ZipFile(v2zip) as z:
    names=z.namelist(); mf=json.loads(z.read('FILE_MANIFEST.json'))
    ck('V2 unique safe archive names',len(names)==len(set(names)) and all(safe(n) for n in names))
    ck('V2 CRC',z.testzip() is None)
    ck('V2 complete payload membership',set(mf)==set(v2['currentFileHashes']) and len(mf)==370)
    for n,row in mf.items():
        old=z.read(n)
        ck('V2 payload '+n,len(old)==row['bytes'] and sha(old)==row['sha256']==v2['currentFileHashes'][n])
        p=G/n; current=p.read_bytes(); add(p,'Complete current version of V2 member')
        if old!=current:
            oldn='history/v2-before/'+n; payload[oldn]=old
            changed.append({'path':n,'before':{'member':oldn,'bytes':len(old),'sha256':sha(old)},'current':{'member':'sources/'+n,'bytes':len(current),'sha256':sha(current)}})
    ck('V2 archive metadata retained',set(names)==set(mf)|{'README_V2.md','FILE_MANIFEST.json'})
payload['history/'+v2zip.name]=v2bytes
add(v2p,'Immutable V2 preparation and earlier-history bindings')
ck('Seven observed dependency changes',len(changed)==7)

internal=R/'data/director/bestiary_source_candidate_internal.json'; data=readj(internal)
pub=R/'data/playtest/bestiary_public_source_candidate.json'
ck('67-record original candidate unchanged',sha(internal.read_bytes())=='66d3d54ec0e70d9515f14789a697b379c648dc604af9f1035194c5230f09663c' and len(data['records'])==67)
ck('26-route public candidate unchanged',sha(pub.read_bytes())=='a9c86af89b900b1c5426757d3eb31d4992cf2b66bbbd2c3d465abab29d4c2af1')
records=data['records']; stat_records=[r for r in records if r.get('statBlock')]
ck('66 stat blocks and distinct nonstat historical record',len(stat_records)==66 and [r['id'] for r in records if not r.get('statBlock')]==['lumen-sixth-gate-disaster-record'])
traits=defaultdict(list); action_rows=[]; ability_rows=[]; mean_rows=[]; exact_cr2=[]; undead=[]; missing=[]
for i,r in enumerate(records):
    src=R/r['source']['path']; sb=src.read_bytes()
    ck('Exact dossier bytes '+r['id'],sha(sb)==r['source']['sha256'] and sb.decode('utf-8')==r['source']['originalUtf8Text'])
    add(src,'Original complete dossier; original candidate embedded text verified')
    for j,item in enumerate(r['unresolvedSourceInterfaces']):
        missing.append({'creatureId':r['id'],'pointer':f'/records/{i}/unresolvedSourceInterfaces/{j}','source':rel(src),'original':item})
    s=r.get('statBlock')
    if not s: continue
    core=s['printedCoreFields']; brief={'id':r['id'],'name':r['name'],'printedType':core['type'],'printedCR':core['challengeRating'],'source':rel(src)}
    if core['challengeRating']=='2':exact_cr2.append(brief)
    if core['type'].casefold()=='undead':undead.append(brief)
    for ability,v in s['abilities'].items():
        expected=(v['score']-10)//2
        row={'creatureId':r['id'],'pointer':f'/records/{i}/statBlock/abilities/{ability}',**v,'floorHalfScoreMinusTenDiagnostic':expected}
        ability_rows.append(row);ck('Printed modifier '+r['id']+'/'+ability,v['printedModifier']==expected)
    for j,t in enumerate(s['traits']):
        traits[(t['name'],t['sourceText'])].append({'creatureId':r['id'],'pointer':f'/records/{i}/statBlock/traits/{j}','source':rel(src)})
    for j,a in enumerate(s['actions']):
        row={'creatureId':r['id'],'pointer':f'/records/{i}/statBlock/actions/{j}','source':rel(src),**a}
        action_rows.append(row)
        m=re.search(r'(\d+)d(\d+)\s*([+-])?\s*(\d+)?[^.]*?average\s+(\d+)',a['sourceText'])
        if m:
            n,die,sign,bonus,printed=m.groups(); mean=Fraction(int(n)*(int(die)+1),2)+int(bonus or 0)*(-1 if sign=='-' else 1)
            q,rem=divmod(mean.numerator,mean.denominator)
            rounded=q+(2*rem>mean.denominator or (2*rem==mean.denominator and q%2==1))
            mrow={**row,'diceCount':int(n),'dieSides':int(die),'constant':int(bonus or 0)*(-1 if sign=='-' else 1),'exactMeanNumerator':mean.numerator,'exactMeanDenominator':mean.denominator,'printedAverage':int(printed),'nearestTiesToEvenDiagnostic':rounded,'printedMinusExactMean':str(Fraction(int(printed))-mean)}
            mean_rows.append(mrow);ck('Printed damage mean diagnostic '+r['id']+'/'+a['name'],rounded==int(printed))
ck('Source action and harvest occurrence counts',len(action_rows)==162 and sum(len((r.get('harvest') or {}).get('components',[])) for r in records)==178)
ck('Full ability and printed damage diagnostics',len(ability_rows)==396 and len(mean_rows)==119)
ck('Previously known source interfaces preserved',len(missing)==13)
ck('Bounded exact CR2 finding',len(exact_cr2)==7 and len(undead)==4 and not any(x['printedType'].casefold()=='undead' for x in exact_cr2))

# Source references are full, local files. No code from any dependency is executed.
context_paths=[
 A/'ACTIVE_AUTHORING_CHECKPOINT_ALL_PENDING_GROUPED_80.json', A/'ACTIVE_AUTHORING_CHECKPOINT_ALL_PENDING_GROUPED_80_CHECK.json',
 R/'data/director/spell_review/remaining_work_queue_67.json', R/'data/director/spell_review/accepted_interface_registry_06.json',
 R/'data/public/spell_playtests/authored_review_index.json', R/'data/playtest/game_development_coverage.json',
 A/'PERTINENT_GPT_DECISIONS_2026_10_20_02.json',A/'GPT_PART5_STATUS_SYNC_16_COMPLETED_NATIVE.json',
 A/'RANK9_RESONANCE_FIELDS3_ACTUAL_DISPATCH_80.json',A/'RANK7_IDENTITY_CASTING5_PART5_EXACT_AUTHORING_ACCEPTANCE_79.json',
 A/'RANK7_READY_DEADLINE_RECOVERY_01_SEMANTIC_RECONCILIATION_79.json',
 A/'TEACHING_TEX_EXACT_FULFILLMENT.json', A/'TC_RECYCLING_01_CONTROLLING_ERRATUM.md',
 A/'TEX_CONTROLLING_ADDENDUM_2026_10_11.md', A/'TEACHING_TEX_ADDENDUM_FULFILLMENT.json',
 A/'LANGUAGE_EXACT_FULFILLMENT.json',R/'docs/mechanics/LANGUAGE_REVIEW_STATUS.json',
 A/'LANGUAGE_WORKSHEET_PREPARATION.json',A/'CHARACTER_ENTRYPOINT_EDITORIAL_FOLLOWUP.json',
 R/'docs/playtest/CHARACTER_LANGUAGE_WORKSHEET.md',R/'docs/playtest/CLASS_RESOURCE_REFERENCE.md',
 A/'COSMOLOGY_SOULS_RESEARCH_01_CONFIRMED_PATCH.json',A/'COSMOLOGY_SOULS_RESEARCH_01_INTEGRATION_RECEIPT.json',
 A/'COSMOLOGY_Q6_LATER_LOCK_01_RECEIVED_DECISION.json',
 G/'docs/audit/2026-10-20/github-snapshot-material-forging72/PUSH_RECEIPT.json',
]
for n in ['CREATURE_LIFECYCLE_PLAYTEST.md','CREATURE_LIFECYCLE_SOURCE_BINDINGS.md','BODY_EQUIPMENT_PLAYTEST.md','COMBAT_ACTION_PLAYTEST.md','CONDITIONS_PLAYTEST.md','CONDITION_RECOVERY_PLAYTEST.md','CUSTOM_CONDITION_BINDINGS.md','DAMAGE_SHARING_PLAYTEST.md','COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md']:
    context_paths.append(R/'docs/mechanics'/n)
lax=readj(A/'LANGUAGE_EXACT_FULFILLMENT.json')
context_paths += [G/n for n in lax['finalHashes']]+[G/lax['authorityFile']]
for n,h in lax['finalHashes'].items():ck('Current exact LAX file '+n,sha((G/n).read_bytes())==h)
ck('LAX complete final verdict',lax['exactLanguageApproval'] and sha((G/lax['authorityFile']).read_bytes())==lax['authoritySha256'])
for n in ['souls_research_reviewed_01.json','chronology_research_route_reviewed_01.json','epilogue_relic_null_reviewed_01.json','epilogue_relic_null_cases_01.json','q6_later_lock_reviewed_01.json']:
    context_paths.append(R/'data/director/cosmology'/n)
comp=A/'companion-life10-exact05-part5-return-01'
context_paths.extend((comp/'accepted/current').glob('*'))
context_paths += [comp/n for n in ['ACCEPTANCE.json','CASE_DISPOSITIONS.json','BRANCH_DISPOSITIONS.json','CONTENT_EVIDENCE_DISPOSITION.json','SPELL_DISPOSITIONS.json','REVIEW.md']]
rank7=A/'rank7-identity-casting5-part5-ready-deadline-recovery-01'
context_paths += [rank7/n for n in ['MODEL.json','DIRECTOR_REVIEW.md','PLAYER_CHAPTER.md','DECISIONS.md','QUESTION_DISPOSITIONS.json','CASE_DISPOSITIONS.json','HOLD_REGISTER.json','CLOCK_AND_BODY_MATRIX.json','SOURCE_AUTHORITY.json','SOURCE_REFERENCES.json','REVIEW.md','MANIFEST.json']]
for p in context_paths: add(p,'Intervening complete current contract or exact accepted-but-unapplied comparison')
cp=readj(A/'ACTIVE_AUTHORING_CHECKPOINT_ALL_PENDING_GROUPED_80.json')
for h in cp['canonicalHelperBaselinesUnchanged']:
    p=G/h['path'];ck('Reserved helper unchanged '+h['path'],info(p)==h)
canonical_paths=[internal,pub,R/'data/public/spell_playtests/catalog.json',R/'data/public/spell_playtests/authored_review_index.json',R/'data/director/spell_review/accepted_interface_registry_06.json',R/'data/playtest/game_development_coverage.json']+[G/h['path'] for h in cp['canonicalHelperBaselinesUnchanged']]
baseline=[info(p) for p in canonical_paths]

questions=[]
def q(topic,prompt,ids=None,trait=None):
    refs=[]
    for i,r in enumerate(records):
        if ids is not None and r['id'] not in ids:continue
        if trait is not None and not any(t['name']==trait for t in (r.get('statBlock') or {}).get('traits',[])):continue
        refs.append({'creatureId':r['id'],'pointer':f'/records/{i}','source':rel(R/r['source']['path'])})
    questions.append({'id':f'BV3-{len(questions)+1:02d}','topic':topic,'status':'UNSELECTED_SOURCE_CONFERENCE_QUESTION','question':prompt,'records':refs})
q('Creature field authority','Resolve the 184 previously recorded source/runtime field differences from the full original dossier and workbook provenance. Preserve names, printed CR/XP/HP/AC/ability/attack/damage values and distinct sources; justify any proposed change individually as a source correction or NEW authorship. A match to generated runtime data does not confer approval.')
q('Attack geometry and damage provenance','For every one of the 162 listed actions, bind melee/ranged classification, reach/range, line and acquisition, occupied-body geometry, target eligibility, delivery type, magical versus intrinsic source, attack/save ability, costs, timings, interruption, damage packets and cleanup. Preserve actual printed values. Mark absent inputs NEW rather than infer ranged or magical effects from an evocative action name.')
q('Multiattack and recharge budget','Specify which listed attacks each of the 42 Multiattack procedures may select, repeat and mix; preserve printed attack count. Resolve eligibility of recharge or save-only abilities, Action/Reaction budgets, target change, interrupt/death and interrupted sequence remainder. Bind all eight recharge actions to initial availability, charge-up telegraph, recharge event, RNG and use/expiry; no hidden extra attacks from a pulse label.')
q('Pressure Wave missing save and effect','The full Pact Automaton source supplies DC15, 3d8 force and a described control effect but does not name a save ability or actually define that control effect. Author a finite source-faithful ability, range, success/failure outcomes, motion/condition duration and interruption procedure; distinguish it from its separate Strength-save Containment Pulse.',ids=['pact-automaton-sentinel'])
q('Missing named attacks','Resolve Cave Bear Bite, Dimetrodon Tail Sweep and Giant Constrictor Snake Constrict referenced in tactics without listed actions. Preserve the references; return complete proposed mechanics or an explained exact editorial disposition, not a substitute imported stat block.',ids=['cave-bear','dimetrodon','giant-constrictor-snake'])
q('Printed mean display policy','All119 parsed printed damage averages equal nearest-integer ties-to-even of their exact listed dice means; 38 are half-integer and81 integral. This observed pattern is not an accepted game-wide rounding rule. Decide a dossier-local display policy while preserving every original dice formula and printed average. Actual RNG damage, fractional mitigation and global rounding retain their own accepted contracts.')
q('Emotional Feeding','Define concrete qualifying behaviors and their evidence/observation predicates, nearby geometry, event timing/frequency, tier selection where the printed range spans tiers, temporary-HP stacking/expiry and interruption. Preserve the emotional-loop counter and its encounter significance; no cosmological truth inferred.',trait='Emotional Feeding')
q('Gate-Bound','Define the source arena/Seal identity, boundary, temporary versus permanent displacement, return event/destination/occupied geometry, Seal invalidation, death and conflict order with current teleportation and Null rules. Preserve the ability without making an unstated universal immunity.',trait='Gate-Bound')
q('Aerial Hunter','Separate the printed difficult-ground exemption from legal aerial movement, vertical geometry, cover and path acquisition. Bind existing printed movement modes and define only missing behavior; seeking a bypass angle is not permission to ignore cover.',trait='Aerial Hunter')
q('Territorial Morale','Give each affected creature deterministic food/young/escape predicates and retreat/break-off state transitions. Preserve noncombat solutions and distinguish a Director-authored encounter objective from a new charm or an automatic success.',trait='Territorial Morale')
q('Unstable Geometry','Define replay identity for movement paths and action sequences, relevant actor history, geometry tolerance, first-time-per-round scope, qualifying observation and reset event. Specify the granted defensive reaction payload, cost, availability, expiry and nonrecursive triggers.',trait='Unstable Geometry')
q('Living Substrate','Specify lair/substrate eligibility, source and target acquisition, origin substitution, maximum geometry, which action/use is permitted, budget and frequency, substrate destruction, damage provenance and suppression. Preserve roots/spores/corpses/standing water without creating unlimited extra creatures or attacks.',trait='Living Substrate')
q('Prepared Ground','Define fortified position/lair eligibility, first attack-or-check scope, reset/re-entry conditions, advantage stacking and consumption on invalid or interrupted attempts.',trait='Prepared Ground')
q('Contract-Bound','Bind each empowered attack to a concrete visible seal or clause and operational object/contract conditions. Specify invalidation/destruction action, inspection/language, ownership, suppression timing through end of next round, restoration and Null classification. No new universal pact cosmology.',trait='Contract-Bound')
q('Anchored Absence','Turn unreliable teleportation/forced movement into a finite exact outcome with anchor identity, activation/destruction state, acquisition and event order, accepted travel/protection precedence, legal destinations and failure costs. Label any added probability or exclusion NEW.',trait='Anchored Absence')
q('Formation Intelligence and distributed bodies','Resolve pair/tetrad/quintet as one tactical intelligence across bodies: actor identity, per-body/shared HP, target/area counting, movement, Action/Reaction budgets, damage/death, unit membership,20ft geometry,+1Armor and surprise immunity. Give a complete playable encounter instance without multiplying attacks or silently merging bodies.',trait='Formation Intelligence')
q('Court Seal','Define promise/brand/accepted-gift mark provenance, informed acceptance, recipient identity, duration/removal, anti-forgery/ownership, attack advantage timing and perception. Preserve social options and accepted language and faction contracts.',trait='Court Seal')
q('Seasonal Anchor','Define anchor object/encounter boundary, tier assignment, intact test, START regeneration and HP cap,0HP/death ordering, suppression, movement of anchor, restoration and nonstacking where multiple anchors exist.',trait='Seasonal Anchor')
q('Tremor Approach','Bind ground entry/exit to printed movement and collision, traversable materials, emergence occupied-body geometry, prepared-point evidence and reaction trigger order. Specify suffocation/burial and blocked exits only as needed; no universal wall traversal.',trait='Tremor Approach')
q('House-trained Darkvision','Bind ordinary-darkness perception and bright-light disruption of stealth routes to explicit ranges, lighting snapshots, concealment/acquisition and existing visual-sense contracts; preserve distinctions between supernatural darkness and ordinary darkness.',trait='House-trained Darkvision')
q('Disease and defense categories','Map the four printed disease immunities to the actual disease/effect system and distinguish poison damage from poisoned condition. Preserve all defense labels, stacking/order and tactical weakness text without inventing unprinted damage vulnerabilities.',ids=['order-drone-pair','order-drone-quintet','order-drone-tetrad','pact-automaton-sentinel'])
q('Alias and publication conflicts','Preserve Fleshwright/Sibriex and Nightreaver/Nabassu as separate source identities pending explicit resolution. Propose save-safe identity/alias routing with provenance, and exact missing build routes for Fleshwright and Nightreaver; never infer a public route.',ids=['fracture-kin-fleshwright','fracture-kin-sibriex','fracture-kin-nightreaver','fracture-kin-nabassu'])
q('Harvest missing procedures and units','Complete Crystal Shardling and Pact Automaton harvest skill/DC/time and Director-set drop/value with exact source distinctions. Across all178 printed occurrences resolve quantity units, eligibility, damage/quality, roll timing, failures, preservation and rate/value/time context against accepted crafting. Preserve source text and mark added numeric quantities NEW.')
q('Materials and recipe identities','Resolve all34 literal material matches,144 unmatched occurrences and38 unresolved printed recipe links individually using complete current recipe cards. Similar names/tier-stripped matches are diagnostics only; neither recipes nor same-name components prove donor identity, availability or quantity. Return the full mapping and retained unresolved evidence.')
q('Knowledge and player disclosure','Bind printed Knowledge skill/DC tiers, languages, observed tells, research/recon/resource actions and in-world reliability to deterministic reveal records and useful encounter counterplay. Keep public26, licensed/deep references and five sealed routing-only dossiers separated. Sealed contents remain outside this conference.')
q('Accepted companion boundaries and exactCR2 hold','Use the complete accepted Companion10 and Rank7 models as their scoped rules. Create Undead profiles are NEW unrated outcomes; Soul Wraith/Bone Colossus/Simulacrum procedures are already accepted but unapplied. Preserve Command Undeath exactCR2 eligibility and IN6-09A/B whole-case holds: seven exactCR2 Known Descent entries contain no printed Undead, and all four printed Undead here have other ratings. This bounded finding does not prove absence elsewhere or authorize changing CR/type to satisfy a test.')
q('Whole useful creature procedures and cases','Return complete proposed operations for every known creature with full initial actor/body/geometry/timing/resource/knowledge state and meaningful success/failure/interruption/death cases. Include party encounter construction, telegraphs, retreat and aftermath/harvest. Keep Lumen Sixth Gate disaster as historical record, not a missing stat block. Use inherited contracts with exact IDs; narrow external content holds must not replace all useful creature behavior with placeholders.')

profile_context={
 'status':'Prepared UNSENT; complete source refresh, not creature approval',
 'applied':{'reviewedSpells':525,'pendingSpells':323,'standaloneProcedures':249,'acceptedInterfaces':173},
 'acceptedButUnapplied':50,'pendingPreparedGroups':56,'allPendingGrouped':True,
 'ownerImplementationReservation':True,
 'acceptedCompanionRules':'Complete eight accepted current artifacts and exact dispositions are included. Native output profiles do not automatically certify same-name historical runtime creatures or their CR.',
 'acceptedRank7Rules':'Complete exact recovered MODEL and selected procedures/cases/holds are included. Simulacrum/Sequester/Erase/CastEcho/MetaSurge are accepted but unapplied; do not reopen them without concrete source conflict.',
 'wholePositiveCaseHolds':['IN6-09A','IN6-09B','EN5-01A','EN5-01B','EN6-03B'],
 'oldProfileDependencyIndex':'The historical BESTIARY_SPELL_PROFILE_DEPENDENCY_INDEX.md is retained in full; pending labels for now-accepted profile procedures are superseded only by their exact included current models and receipts.',
 'crafting':'Current recipe/sourceCard bodies remain governed by exact AEX approval and subsequent TC-RECYCLING-01/TEX addenda; full current dependencies and old seven changed files are retained.',
 'language':'LAX-EXACT-2026-10-11 seven current final artifacts verified. Do not carry historical language-pending labels forward.',
 'cosmology':'Verified GitHub backup through72 preceded already completed scoped cosmology work. Relevant current souls/research/Null/Q6 records are included to prevent old status labels reopening accepted contracts. This bestiary refresh makes no cosmology decision. Sealed dossiers are preservation/routing only.',
 'currentGptConference':'Actual Resonance Fields3 source review dispatched80 remains independently active at preparation; no final or acceptance inferred.',
 'implementationRuntimeHumanBalanceRelease':'None advanced by this evidence preparation.'}
report={
 'id':'BESTIARY-CURRENT-SOURCE-INTERFACES-81','status':'SOURCE_DIAGNOSTICS_AND_UNSELECTED_QUESTIONS',
 'scope':'Exactly67 Known Descent dossier records and their existing harvesting/recipe dependencies; sealed contents not inspected.',
 'sourceCandidate':info(internal),'publicSourceCandidate':info(pub),
 'counts':{'dossiers':67,'statBlocks':66,'publicSourceRoutes':26,'listedActions':162,'multiattackActions':sum(a['name']=='Multiattack' for a in action_rows),'traitOccurrences':sum(len(v) for v in traits.values()),'distinctTraitTextVariants':len(traits),'harvestOccurrences':178,'existingUnresolvedInterfaces':13,'abilityModifierDiagnostics':396,'damageMeanDiagnostics':119,'questions':len(questions)},
 'sourceBoundaries':profile_context,'changedDependencies':changed,
 'exactCR2KnownDossiers':exact_cr2,'printedUndeadKnownDossiers':undead,
 'boundedCR2Conclusion':'No printed exactCR2 Undead in these66 source stat blocks. No all-history absence claim and no eligibility promotion.',
 'abilityDiagnostics':ability_rows,'damageMeanDiagnostics':mean_rows,
 'damageMeanConclusion':'All119 parsed printed averages match exact rational means rounded to nearest integer, ties to even;38 means are half-integer and81 integral. This source pattern is a diagnostic, not a selected engine rounding rule.',
 'traitSourceInventory':[{'name':name,'sourceText':text,'records':refs} for (name,text),refs in traits.items()],
 'completeActionInventory':action_rows,'existingUnresolvedInterfaces':missing,'identityRelationsUnchanged':data['identityRelations'],
 'questions':questions,'selectedDecisions':[],'canonicalChanges':False,'downloadedCodeExecuted':False,'runtimeTests':0,'sourceInformationDeleted':0}
request='''Prepared full bestiary source conference, UNSENT. Read README_V3.md and BESTIARY_CURRENT_SOURCE_INTERFACES_81.json, then the full current source payload and retained V2 history. Preserve all67 known dossiers,66 printed stat blocks,26 public routes,162 actions,178 harvest occurrences,707 workbook/runtime bindings and184 historical field differences. The27 new source-mapped question dispositions supplement every original source/runtime/history/crafting question; they do not replace them.

Current language LAX approval and advanced crafting TEX errata are included in full. The exact Companion10 and Rank7 accepted-but-unapplied models govern their scoped spell outcomes. Applied525/323/249/173 and accepted-but-unapplied50 remain unchanged. The seven changed V2 dependencies retain complete before/current bytes. Historical pending labels are not current authority. Do not execute supplied scripts or regenerate old runtime data.

Resolve every mapped source conflict and author complete useful video-game creature operations: geometry, actor/body/unit identity, defenses, budgets, attacks/saves/damage, traits, recharge telegraphs, counterplay, knowledge and language, retreat, death and harvest/material provenance. Preserve original values; absent mechanics are NEW scoped authorship with explained tradeoffs. All119 listed damage averages follow ties-to-even of exact dice means as an observed display pattern, not new global rounding law. The42 Multiattacks and all trait families need explicit operational treatment. Pressure Wave's missing save/effect and formation-body identity require actual decisions.

Return the full source-linked model/manuscript, finite dispositions for all27 questions plus existing13 unresolved interfaces and every material/recipe comparison; meaningful full-state encounters and branches; complete exact reversible before/after values or full artifact references; retained holds and source manifest. Do not import another game's profiles, merge aliases by name, change CR/type to satisfy a spell test, or reduce useful effects for tabletop bookkeeping. Keep all five whole positive-case holds and all conditional qualifications. Seven exactCR2 creatures in this bounded catalog include no printed Undead; the four printed Undead have other CRs. This finding does not establish absence elsewhere.

Five sealed dossiers are containment/routing evidence only; do not review or publicly disclose their contents. Use current scoped souls/research/Null contracts without reopening origins. This is source authorship for later independent exact review. Owner-reserved canonical integration, runtime execution, human testing, balance, cosmology decisions and release remain distinct and unapplied. No deletion or publication.
'''
ck('Expected source-mapped question count',len(questions)==27)
ck('Source inventories match request',report['counts']['multiattackActions']==42)
payload['BESTIARY_CURRENT_SOURCE_INTERFACES_81.json']=jb(report)
payload['CURRENT_AUTHORITY_AND_PROFILE_BOUNDARIES.json']=jb(profile_context)
payload['SOURCE_CONFERENCE_REQUEST.txt']=request.encode('utf-8')
payload['prepare_bestiary_v3_81.py']=Path(__file__).read_bytes()
readme='''# Bestiary complete source conference V3 — prepared, unsent

This is a current evidence packet for the67 Known Descent dossiers. No original source, gameplay procedure or approval label was changed. Read the complete source inventory and27 unselected questions; retain all earlier questions and exact source identities.

`sources/` holds every current V2 source member plus complete intervening dependencies. `history/` retains the entire immutable V2 ZIP and separate full before-files for the seven changed dependencies. The V2 ZIP already retains its earlier source history. FILE_MANIFEST binds every payload; CURRENT_SOURCE_BINDINGS names why each current file is included.

The authority/profile boundary file separates exact accepted but unapplied spell outcomes from old generated runtime creatures, and records current language/crafting/Null context. Current applied baseline525/323/249/173;50 accepted but unapplied. No new mechanics are selected in this packet. All323 pending spells are grouped for source review; grouping does not mean completion. The separate Resonance Fields3 review remains active.

Full source text, dice expressions and printed averages are preserved. The new396 ability and119 exact-rational damage-mean checks are bounded source diagnostics, not gameplay or balance tests. No downloaded or project code is executed. Five sealed dossier contents remain unreviewed preservation/routing evidence; public26 does not expand.

Return proposed complete creature operations and source-mapped reasoning, with exact reversible artifacts and meaningful deterministic cases. Owner-reserved implementation and all independent review/runtime/human/balance/cosmology/release gates remain open.
'''
payload['README_V3.md']=readme.encode('utf-8')
payload['CURRENT_SOURCE_BINDINGS.json']=jb({n:{'bytes':len(payload[n]),'sha256':sha(payload[n]),'reasons':reasons[n]} for n in sorted(reasons)})
ck('Safe unique prepared payload names',len(payload)==len(set(payload)) and all(safe(n) for n in payload))
manifest={n:{'bytes':len(b),'sha256':sha(b)} for n,b in sorted(payload.items())}
payload['FILE_MANIFEST.json']=jb(manifest)
for n,b in payload.items():write_new(ROOT/n,b)
with zipfile.ZipFile(ZIP,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for n,b in sorted(payload.items()):z.writestr(n,b)
with zipfile.ZipFile(ZIP) as z:
    ck('V3 safe unique exact member set',len(z.namelist())==len(payload) and set(z.namelist())==set(payload))
    ck('V3 CRC',z.testzip() is None)
    for n,b in payload.items():ck('V3 full-byte archive roundtrip '+n,z.read(n)==b and (Path('\\\\?\\'+str((ROOT/n).resolve()))).read_bytes()==b)
for row in baseline:ck('Canonical baseline remains unchanged '+row['path'],info(G/row['path'])==row)
receipt={'id':'BESTIARY-COMPLETE-V3-81','preparedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PASS_COMPLETE_SOURCE_PREPARATION_UNSENT','sent':False,
 'archive':info(ZIP),'previousArchive':info(v2zip),'previousPreparation':info(v2p),'payloadMembers':len(payload),'currentSourceFiles':len(reasons),'v2CurrentDependencies':370,'unchangedV2Dependencies':370-len(changed),'changedDependencies':changed,
 'sourceCounts':report['counts'],'candidateSourceIdentityUnchanged':True,'completeHistoricalV2Preserved':True,'all27QuestionsUnselected':True,
 'currentAuthority':profile_context,'canonicalBaselines':baseline,'report':{'path':rel(REPORT),'bytes':len(jb(report)),'sha256':sha(jb(report))},
 'checks':len(checks),'failures':0,'checksScope':'Full-byte source/history/archive preservation;396 printed modifier and119 exact-rational printed-mean diagnostics; current contract binding. Not game engine execution or substantive creature approval.',
 'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'downloadedCodeExecuted':False,'wholeGameComplete':False,
 'nextAction':'Finish the active ResonanceFields3 exchange, recheck any intervening relevant authority, then send this prepared bestiary conference. Do not interrupt a running GPT reply.'}
write_new(REPORT,jb(report));write_new(REQUEST,request.encode('utf-8'));write_new(SAVED_SCRIPT,Path(__file__).read_bytes())
write_new(CHECK,jb({'id':'BESTIARY-V3-CHECK-81','checks':checks,'passed':len(checks),'failed':0,'scope':receipt['checksScope']}))
receipt['checkReport']=info(CHECK);write_new(RECEIPT,jb(receipt))
print(json.dumps({'status':receipt['status'],'archive':receipt['archive'],'sourceFiles':len(reasons),'payloadMembers':len(payload),'counts':report['counts'],'checks':len(checks),'failures':0,'receipt':info(RECEIPT)},ensure_ascii=False))
