"""Freeze EPI-01..07 sources and concrete interface questions for the actual notebook."""
from datetime import datetime, timezone
from zipfile import ZipFile, ZIP_DEFLATED
from xml.etree import ElementTree as ET
import hashlib, json
from apply_di7_ap_as_01 import G, R, A, info, encoded

REVIEW = 'COSMOLOGY-EPILOGUE-CHARACTER-01'

REQUEST = '''Continue our Decennium Descent review in this existing Part 3 notebook. The owner asked us to discuss and develop every aspect of the game, preserving source information. The chronology/research route is now adopted locally with your exact LP01..08 confirmation. That work is closed within its bounded scope. This conference is EPI-01 through EPI-07: turn these original epilogue directions into a complete provisional character-facing module and a separate Director implementation chapter.

Read CURRENT_REVIEW_CONTEXT.json, INTERFACE_QUESTIONS.json and SOURCE_BINDINGS.json, then the actual supplied sources. Original manuscripts govern subject to explicit owner corrections. Read all original EPI-01..07 evidence in the inventory and verify it against the DOCX; indices count ALL w:p elements including blanks and tables. Read current class engines/cards and the shared mechanics needed by each decision. Do not infer missing rules from familiar games, descriptive names or old runtime data. Distinguish preserved source wording, explicit owner direction, current reviewed integration, and NEW provisional authorship. Our local suggestions are reviewable suggestions, not owner instructions or recovered canon.

The supplied live current sources supersede older frozen workflow statements in this long chat. Part 3 is active; no chat-creation permission is pending. Campaign epoch remains an unanswered owner choice; do not select one or make the 710 AE phase assumption historical fact. Source manuscripts and existing adopted data must not be rewritten. This is an additional provisional module, not an unannounced global replacement. EPI-08..17 remain separate later work, except bounded interface definitions needed here. No full cosmology, runtime, human balance, whole-game or publication approval.

Produce complete, executable rules, not only a list of unresolved questions. You may change the local suggestions if you explain why and supply a concrete alternative. Resolve the ordinary mechanical decisions now. Preserve actual identity/epoch gaps as gaps. Include every class in the mask/key-ability table, every one of the seven listed motifs and all seven virtue pairings. Preserve the source's nine-verses/seven-benefits accounting gap without inventing missing historical verses. Do not erase Paladin and Mirrorsage's dual pairings. Respect Base/Arch/Hero progression and the distinct class engines.

Required output: one downloadable ZIP named DD_Cosmology_Epilogue_Character_01_Return.zip with exactly these eight files:
1 REGISTER.json: issues EPI-01..EPI-07, exact source evidence and decisions, kept/clarified/NEW distinctions, status and remaining genuine boundaries.
2 EPILOGUE_CHARACTER_MODEL.json: complete procedures, fixed limits, resources, triggers, actions, targets, exact clocks, save/check formulae, costs, failure/interruption/expiry handling, all17 class mask rows, seven motifs, seven virtue rows, finite petition feature menu, seven challenge scenes and finite Sentinel information examples. Use stable IDs and structure usable for later consistency checks. It must be the complete current candidate, not a patch requiring hidden older state.
3 PLAYER_CHAPTER.md: readable, playable player rules that reveal no Director-only identities, Equation route or undocumented deep-floor cosmology. Explain what a player actually chooses and records. Do not call a partial presentation secure software.
4 DIRECTOR_CHAPTER.md: full setup, finite inventory/availability, adjudication, NPC Witness and Sentinel procedures, explicit answers and outcomes for challenge scenes, authority boundaries and source/new-design distinctions.
5 CASEBOOK.json: at least28 worked cases with stated starting state, exact event order, rolls/modifiers/DCs where used, elapsed time, costs and final state. At minimum cover all the adversarial cases in INTERFACE_QUESTIONS.json, not just happy-path vignettes. Do not call these executed runtime tests.
6 SOURCE_HASHES.json: {"sources": [...]} reproducing every supplied SOURCE_BINDINGS.json path/bytes/sha256 exactly, calculated from the actual archive files. Include direct source references with path plus paragraphIndexZeroBased (and part), jsonPointer, or firstLineOneBased/lastLineOneBased throughout REGISTER/model/cases. An excerpt at a location must equal its exact whole located text; do not silently normalize spaces. Exact text SHA256 is acceptable instead of repeating a long paragraph. Source citations justify only what they actually say, not a new number or new scene placement.
7 VERDICT.md: scope, concrete resolutions, remaining genuine owner/source questions and a candid completeness verdict. Full runtime/human/balance/whole-game/publication gates remain false. List any issue you could not complete rather than pretending it is solved.
8 EVIDENCE_MANIFEST.json: {"files": [{"path": ..., "bytes": ..., "sha256": ...}]} for the preceding seven output files, not itself.

Make duplicated prose/model/cases mechanically identical. Check the real elapsed-clock arithmetic, eligibility, same-source duplicate stacking, action economy, item identity and depleted-resource cases yourself before returning the archive. A successful source-hash check is not a semantic approval. Return the file link and a short decision summary. Please perform the actual authoring now.
'''

QUESTIONS = [
 {'id':'EPI-01','title':'Home plane, Inspiration and Disquiet',
  'source':'Original P270–276; symbolic Spiral Map, one home-plane token, benefit or consequence on a long rest away according to conduct.',
  'interfaces':['Define whether home plane is an elective spiritual affiliation or literal origin; do not grant planar ancestry, resistance, access, travel or factual knowledge by choosing it. Supply a finite table of eligible choices/principles using the current planes authority; all artwork labels are not equivalent primary planes.',
   'No general hero-point, Inspiration or Disquiet engine was located in targeted Core/current-mechanics reads. This is a bounded search result, not universal absence. Bard Echo of Inspiration is a specific delayed damage/healing technique and is not an Inspiration pool. Do not restore RP, RC, Ki, BG, Momentum, Conviction, healing reserves or items under an undefined equivalent-resource clause.',
   'Bind benefits to actual beneficial completed 8h Long Rests and the 24h reward limit, with exact away/home tests and evaluation window. Short rests, extra sleeping, session breaks and plane changes cannot manufacture rewards. Define the neutral/no-relevant-choice case and fair advance notice of conduct conflicts.',
   'Provide a complete Inspiration die size, cap, gain/spend timing, eligible rolls, duration, stacking and duplicate-source rule. Disquiet needs an explicit bounded penalty, trigger, expiry and clearance; it is neither Corrupted, KT/PT, Dissonance, Strain nor Exhaustion unless explicitly proposed and reviewed.'],
  'localSuggestion':'NEW starting point only: elective home affiliation; personal epilogue Inspiration d6, capacity2, one die on an ability check declared before the d20; no attacks/saves/automatic resource conversion. Treat neutral conduct as no reward or penalty. Consider Disquiet a one-use task penalty with a finite expiry rather than another lethal attrition track. Explain any departure from the source either/or sentence.',
  'cases':['Home affiliation without birth or travel permission','Two rests within24h; actual second eligible rest','Neutral, aligned and knowingly contrary conduct','Inspiration full/empty/duplicate gains; Disquiet overlap and expiry']},
 {'id':'EPI-02','title':'Seven Choir motifs',
  'interfaces':['Who can perform or access each motif? Define tangible score/training, language/audibility, action or elapsed performance time, target/range/line of effect, interruption, cooldown and outcome expiry. Repetition by multiple performers or recordings must not create unlimited recovery or denial.',
   'Courage restores the specified finite module resource only; it cannot refill encounter currencies out of combat or refresh a feature. Define all characters and spent-resource history.',
   'Balance is a swap within a real existing prepared loadout, with known/owned/level/path prerequisites preserved. Wizard matrices, Druid prepared spells/Arch forms, Warrior mutations and other class systems differ. An ability known/selected permanently is not a prepared ability. Define each eligible system and exhausted use counters, and supply a no-eligible-loadout outcome.',
   'Law must state save or other resistance, exact behavior, hostility/attack interruption, duration, source-target denial limits, communication and boss defenses. Compelled parley does not compel agreement, truth, surrender or player consent.',
   'Sorrow requires an executable failed-WIS-save reroll timing and final-result replacement rule, including instant consequences, death already resolved and no repeated reroll chains. Pattern and Contradiction require finite pending benefits, exact qualifying checks and expiry.',
   'Transition needs a finite eligible-task rule and stacking/rounding, when declared, effects on actual workers and completion, interrupted work and minimum time. Preserve active vs elapsed clocks: never halve rests, natural waits, opening season, spell duration, travel, borrowed-proficiency duration or required observation. Explicitly decide its interface with 8h mask work, 4h research finding/synthesis, 8h deciphering, crafting, training and fixed rituals. It cannot create missing access, qualifications or materials.'],
  'localSuggestion':'NEW starting point only: one shared party motif activation allowance per beneficial rest interval, with an independent24h ceiling if needed; not seven separately farmable replenishments. For Transition, an explicit finite eligible work table is preferable to unrestricted all-time halving. Keep its effect recognizably meaningful and label narrowed source scope as NEW.',
  'cases':['Two performers/recorded loop and same-source target','Courage at full capacity and after expiry','Balance selected feature versus actual preparation and missing spellbook','Law target harmed by ally/environment and immune boss','Sorrow failed save before/after consequence','Transition+other speed modifiers, pausing, helper hours and 1h Knowledge Transfer']},
 {'id':'EPI-03','title':'Unfinished vow',
  'interfaces':['Provide creation, fulfillment, revision/retirement and record rules. All17 classes can participate. Distinguish a fictional personal unfinished vow from a Paladin Sacred Oath, a pact, legal contract and enforced mind control.',
   'Confession/secret/emotional truth refer to character fiction, not a demand for a player to reveal private facts. Respect the existing session-zero agreement. Explain what an NPC or ally must actually hear/understand and alternative communication consistent with in-world limits.',
   'Changing a vow must not reset resources, repair a mask for free, clear ordinary Corruption or KT/PT, grant XP, trigger an Oathbreaker inversion or reroll a failed crafting attempt. Define what happens to its existing mask.'],
  'cases':['Vow completed or revised with a cracked mask','Paladin declines/revises vow without an Oath breach','Written/signed confession and unavailable witness']},
 {'id':'EPI-04','title':'Living and Cracked Masks for all17 classes',
  'interfaces':['Preserve original8h shaping, actual class-significant reflective material, class-key ability and DC10+remaining fictional vow secrets, success Living/failure working Cracked, fear/Null-lullaby save advantage, once/rest reveal CHA save/Stunned1round, truthful free-action safe removal. Supply every missing operational field with NEW provenance.',
   'All17 key abilities must follow actual engines or an explicit bounded mask-only resolution: BardCHA, ClericWIS, CrimsonAgenthemomancyINT vs weaponDEX seam, DragoonSTR, DruidWIS, MageINT, MirrorsageINT, MonkDEX, OracleCHA, PaladinCHA, RangerprimalWIS vs weaponDEX seam, ShamanWIS, SoldierCON vs weaponDEX seam, ThiefDEX vs noncombatINT/WIS seam, TinkerINT, WarriorpermanentchosenSTR/DEX, WizardINT. State multiclass choice before creation and no free selection of highest stat each use.',
   'Define finite predeclared character-secret counting, actual proficiency eligibility, assistants, four-degree collapse, costs/tool/station, material quantities/acquisition, interruption/retry/repair and output count. Keep source Ranger frozen moonlit water, Wizard condensed ArcaneCrucible silver and Thief black glass; newly supply the other14 without presenting them as recovered canon. Avoid a missing ingredient availability loop and no real-world hazardous synthesis.',
   'The reviewed687 trade recipes remain687 unless a later explicit catalog addition occurs. Decide whether this is a separate vow ritual with specific craft exceptions, not an automatically approved new trade recipe. No generic quality rule may duplicate a personal mask or add stun charges/DC.',
   'Specify unique creator/wearer/binding, wearing slot/compatible anatomy, attunement if any, donned/revealed/removed states, meld suppression, visibility, target saveDC/action/6m conversion, repeat/save immunity and hard-denial integration. Safe removal needs exact timing outside own turn, speech restriction, unwilling removal/loss and suppression. Do not invent a death/curse/identity-loss punishment for unsafe removal merely because source says safely.',
   'Once per rest means which actual beneficial rest? Charges belong to a character or mask, duplicates/replacements/loans cannot reset them. Define exact Stunned endpoint for off-turn targets, new initiative and combat exit; fear and Null-lullaby advantage do not imply immunity, cleansing, truth detection or KT/PT protection.'],
  'localSuggestion':'NEW starting point only: one personal operative mask, no generic attunement capacity change, one reveal allowance per wearer refreshed only by a qualifying beneficial short/long rest. Treat reveal as Action with source-target hard-denial sharing the class guard; save8+PB+fixedmaskkey modifier. Propose20ft grid conversion openly. Use a finite predeclared0–3 secret ledger and a bare ability check unless a specific applicable grant permits PB; do not quietly turn it into generic crafting expertise. A different justified design is welcome.',
  'cases':['All17 rows including mixed weapon/DC classes and multiclass choice','Mask work interrupted and restarted, exhausted ingredients and failed roll','Natural1/20 four-degree effects without invented extra quality','Swapping/loaning two masks across rests','Stun plus existing class denial on same target; immunity','Mask melding or no suitable face/hands/voice; honest removal versus forced loss']},
 {'id':'EPI-05','title':'Virtue opposition and Conflict Die',
  'interfaces':['Preserve all exact7 pairings, including dual Paladin/Mirrorsage rows. Natural resonance is descriptive, not a class restriction. A virtue absent from a class row is not necessarily philosophically opposed.',
   'Define an explicit choice of present class strength, a meaningful fictional tension with selected virtue, notice/agreement and multiclass handling. Do not force alignment, belief, personality, loyalty or Paladin breach.',
   'Preserve once per sessiond12 added to an ability check and successful outcome fatigue. Define session IDs/continuations, declaration timing, eligible task vs attack/save, four-degree/natural shift order, critical success, opposed checks, stacking with Inspiration and source bonuses, resource spending on failure and immunity behavior.',
   'The original says risk of exhaustion then one level fatigue. Bind deliberately and explain. Existing core.exhaustion, expedition.strain and warrior.serum-strain are independent. Do not apply all three. If choosing Exhaustion, explicitly acknowledge cumulative effects and lethal6, actual immunity and 8h/24h recovery; a neutral name does not make its consequence mild.'],
  'localSuggestion':'NEW proposal for review: bind fatigue here to one core Exhaustion level, because P291 says exhaustion, with explicit pre-use warning in rules and success evaluation after core degree/natural rules. This is an interpretive decision, not a recovered definition. Decide whether immunity prevents the gain or instead makes this priced benefit unavailable; do not silently import a generic immunity-cost rule.',
  'cases':['Dual-resonant Paladin/Mirrorsage and nonopposed unlisted virtue','Failed and critical-success Conflict checks including natural1/20','Exhaustion5 success and whole event consequence','Immunity, other tracks, simultaneous Inspiration and session break']},
 {'id':'EPI-06','title':'Archon petitions',
  'interfaces':['Keep Cleric/Monk/actual spiritual mentor eligibility, local Witness recording motive, uninterrupted1h meditation, and virtue-symbolic act. Define actual Witness/mentor credentials and availability, finite act costs and downtime action clocks. Source did not require a witnessed Archon appearance. No repeated petition fishing: finite cooldown, one result, real success/failure and expiry.',
   'd12 1–4 Guidance: define eligible check set in advance, one-day clock and nonstacking. 5–8 Blessing: a finite menu of self-contained actual class features from virtue-paired classes, exact card IDs and transferred text, any level/stat/cost exceptions expressly NEW. Avoid borrowing whole engines, selected Arch/Hero powers, unlimited resource generation or advancement credentials. The attached seven candidate passives are suggestions; replace with another verified finite menu if better.',
   'For already-known feature use, duplicates and expired sources, define outcome without reroll fishing. Actual class-specific scaling never becomes total level unless explicitly adapted. Full temporary feature records must agree between JSON, prose and examples.',
   '9–11 Test: seven finite playable challenge scenes, one per virtue, actual NPCs/props/tasks/DCs/options, concrete success/failure, bounded time and no preselected moral answer forced on the player. Inspiration pool two dice must reconcile with EPI-01, not create unlimited independent pools. Vow revision needs player agency and explicit mechanical effects.',
   '12 Revelation: complete bounded planar-step permission and finite usable destination/access setup, departure/return/location/party/cargo/hazard/clock rules. Once between sessions is cadence, not unlimited off-screen distance/time or bypass of an existing travel barrier. Do not promote pending PlanarGate, PlaneShift, TeleportationCircle, time-travel or class spells by name. If creating a new route, label it NEW and choose explicit endpoints rather than whatever plane the party wants.',
   'Define dawn underground/across planes without adding a universal source chronology: maintain actual elapsed24h/day campaign clock and explicit recorded expiry. Session breaks never produce a beneficial rest or skip costs.'],
  'localSuggestion':'Candidate finite boon menu: Courage warrior.base.combat-instinct; Balance ranger.base.natural-explorer; Law soldier.base.tactical-awareness; Sorrow shaman.base.alchemical-knowledge; Pattern wizard.base.scholarly-mind; Contradiction thief.base.trap-intuition; Transition monk.base.unarmored-speed. These are actual Base passives; temporary grants must explicitly bypass only acquisition, not import their entire classes. For Transition, retain5ft baseline and only actual Monk11 raises10ft. No class levels/proficiencies/material ownership arise from a grant. Verify all actual cards.',
  'cases':['Petition interrupted/missingWitness/falsementor/repeated retries','Allfour die bands and exact24h/dawn expiry','Already-known boon, nonmember class, actual Monk11 scaling','Seven challenges with declined revision and no resource refresh','Planarstep lawful destination, occupied return, impossible destination and oneuse']},
 {'id':'EPI-07','title':'Sentinel encounters and finite information',
  'interfaces':['Author a finite encounter procedure and at least one playable example each of puzzle solution, local map fragment and contingent future vision. Include the actual puzzle/answer, small local graph and uncertain proposition; not just the phrase Director provides a clue.',
   'Sentinel neutral observer does not imply omniscience or universal truth access. Earnest question is fictional intent adjudication with a safe failure path, not a real-player sincerity test. State what is known/unavailable, repeat limits and alternative ordinary investigation route.',
   'Do not give Equation fragments, hidden identity certainty, a floor shortcut, guaranteed future, cosmological retcon, permanent class feature or travel permission as an inferred information reward. Preserve public SixthGate ceiling when writing player text; newly invented scenes have no recovered geographic authority.'],
  'cases':['Earnest unanswered question and repeat request','Finite puzzle answer usable without automatic checksuccess','Map fragment exact graph with real doors not teleport','Future vision contradicted by later choice without retcon']}
]

def main():
    root=A/'cosmology-epilogue-character-01'
    archive=A/'DD_Cosmology_Epilogue_Character_01.zip'
    receipt=A/'COSMOLOGY_EPILOGUE_CHARACTER_01_PREPARATION.json'
    assert all(not p.exists() for p in [root,archive,receipt])
    paths=[
      G/'The Cosmology of Decennium Descent.docx', G/'The Decennium Descent and the Matrix of Oblivion.docx', G/'The_World_of_Aethel_Lore.docx',
      G/'books/player/Decennium_Descent_Player_Rulebook_v6.docx', G/'books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx',
      A/'ORIGINAL_COSMOLOGY_EPILOGUE_RULE_INVENTORY_01.json',
      R/'data/public/Decennium_Descent_Bard_Playtest_v0_1.json', R/'docs/mechanics/BARD_PLAYTEST_v0_1.md',
      R/'docs/playtest/SESSION_ZERO_PLAYTEST.md', R/'docs/playtest/CLASS_RESOURCE_REFERENCE.md',
    ]
    paths += sorted(p for p in (R/'data/public/class_playtests').glob('*.json') if p.name!='manifest.json')
    paths += [R/'docs/mechanics'/name for name in [
      'CORE_RESOLUTION_PLAYTEST.md','CLASS_PLAYTEST_RULES.md','COMBAT_ACTION_PLAYTEST.md','CONDITIONS_PLAYTEST.md','CONDITION_RECOVERY_PLAYTEST.md','STRAIN_PLAYTEST.md',
      'CHARACTER_FOUNDATION_TABLES.md','CHARACTER_CREATION_PLAYTEST.md','ADVANCEMENT_PLAYTEST_PROPOSAL.md','PALADIN_OATHS_AND_OATHBREAKERS.md',
      'BODY_EQUIPMENT_PLAYTEST.md','EQUIPMENT_ITEM_PROCEDURES.md','EQUIPMENT_ACQUISITION_PLAYTEST.md','CRAFTING_HARVEST_PLAYTEST.md','CRAFTING_TRADE_REFERENCE.md','CRAFTING_RECIPE_REVIEW_INDEX.md',
      'SPELL_INTEGRATION_RULES.md','LANGUAGE_COMMUNICATION_PLAYTEST.md','TEMPORAL_KERNEL_PLAYTEST.md']]
    paths += [R/'data/director/expedition_candidate'/f'part{x:02}.json' for x in [1,3]]
    for stem in ['heartcell_owner_update_02','gods_pantheons_reviewed_01','planes_reviewed_01','q6_later_lock_reviewed_01','souls_research_reviewed_01','chronology_source_reviewed_01','chronology_research_route_reviewed_01']:
        paths.append(R/'data/director/cosmology'/f'{stem}.json')
    paths += [R/'docs/director-only/cosmology'/name for name in ['CURRENT_COSMOLOGY_READ_FIRST.md','PLANES_REVIEWED_01.md','SOULS_RESEARCH_REVIEWED_01.md','CHRONOLOGY_RESEARCH_ROUTE_REVIEWED_01.md']]
    paths += [R/'data/public/spell_playtests'/name for name in ['catalog.json','authored_review_index.json']]
    assert len(paths)==len(set(paths))
    assert all(p.is_file() for p in paths), [str(p) for p in paths if not p.is_file()]
    inv=json.loads((A/'ORIGINAL_COSMOLOGY_EPILOGUE_RULE_INVENTORY_01.json').read_bytes())
    assert inv['source']==info(G/'The Cosmology of Decennium Descent.docx')
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    with ZipFile(G/'The Cosmology of Decennium Descent.docx') as z:
        ps=[''.join(t.text or '' for t in p.findall('.//w:t',ns)) for p in ET.fromstring(z.read('word/document.xml')).findall('.//w:p',ns)]
    paragraph_checks=[]
    for u in inv['units'][:7]:
        for e in u['evidence']:
            actual=ps[e['paragraphIndexZeroBased']]
            assert actual==e['text'] and hashlib.sha256(actual.encode()).hexdigest()==e['textSha256']
            paragraph_checks.append({'id':u['id'],'paragraphIndexZeroBased':e['paragraphIndexZeroBased'],'passed':True})
    menu={'Courage':('warrior','warrior.base.combat-instinct'),'Balance':('ranger','ranger.base.natural-explorer'),'Law':('soldier','soldier.base.tactical-awareness'),'Sorrow':('shaman','shaman.base.alchemical-knowledge'),'Pattern':('wizard','wizard.base.scholarly-mind'),'Contradiction':('thief','thief.base.trap-intuition'),'Transition':('monk','monk.base.unarmored-speed')}
    candidate_menu=[]
    for virtue,(cl,cid) in menu.items():
        path=R/'data/public/class_playtests'/f'{cl}.json';d=json.loads(path.read_bytes())
        ix=next(i for i,c in enumerate(d['cards']) if c['id']==cid);card=d['cards'][ix]
        assert card['band']=='Base' and card['minimumClassLevel']==1 and card['activation']=='Passive' and card['cost']=='0'
        candidate_menu.append({'virtue':virtue,'status':'NEW proposed temporary menu; not adopted','path':path.relative_to(G).as_posix(),'jsonPointer':f'/cards/{ix}','value':card})
    now=datetime.now(timezone.utc).isoformat();root.mkdir()
    rows=[]
    for p in paths:
        raw=p.read_bytes();row=info(p,raw);out=root/'sources'/row['path'];out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw);rows.append(row)
    (root/'SOURCE_BINDINGS.json').write_bytes(encoded(rows))
    (root/'REQUEST.txt').write_text(REQUEST,encoding='utf-8',newline='\n')
    (root/'INTERFACE_QUESTIONS.json').write_bytes(encoded({'reviewId':REVIEW,'status':'prepared local questions and proposals; not adopted','issues':QUESTIONS,'candidateBlessingMenu':candidate_menu,'sourceParagraphChecks':paragraph_checks}))
    context={'reviewId':REVIEW,'recordedAtUtc':now,'scope':['EPI-01','EPI-02','EPI-03','EPI-04','EPI-05','EPI-06','EPI-07'],'frozenSourceCount':len(rows),
      'authority':'Original manuscripts subject to explicit owner corrections; current reviewed rules within their bounded domains; NEW module proposals require joint semantic review.',
      'currentRoute':info(R/'data/director/cosmology/chronology_research_route_reviewed_01.json'),
      'currentSouls':info(R/'data/director/cosmology/souls_research_reviewed_01.json'),
      'currentNotebook':'Existing Calibration Review Part3; do not create a new chat. Route LP01..08 confirmed and adopted locally.',
      'epoch':'Owner choice pending; no default chosen.',
      'spellStatus':{'reviewed':419,'pending':429,'total':848,'ancestryOnlySeparate':10},
      'recipeStatus':{'reviewed':687,'public':433,'maskNotAutomaticallyAdded':True},
      'unchangedBoundaries':['EPI08..17 not adopted by this conference','Original9verses/7benefits accounting gap','Unresolved cosmological identities','Public reliable expedition ceiling failedSixthGate','No new pending spell promotion','Current source-specific KT/PT/Hunt and death rules','No source deletions; no human/runtime/balance/publication/whole-game approval'],
      'originalSourceVerification':{'paragraphChecks':len(paragraph_checks),'failures':0},'newRulesAdopted':False}
    (root/'CURRENT_REVIEW_CONTEXT.json').write_bytes(encoded(context))
    payloads=[{'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(root.rglob('*')) if p.is_file()]
    (root/'PACKAGE_MANIFEST.json').write_bytes(encoded({'reviewId':REVIEW,'sourceCount':len(rows),'payloads':payloads}))
    with ZipFile(archive,'w',ZIP_DEFLATED) as z:
        for p in sorted(root.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(root).as_posix())
    receipt.write_bytes(encoded({'reviewId':REVIEW,'recordedAtUtc':now,'status':'prepared-not-submitted','archive':info(archive),'sourceCount':len(rows),'originalParagraphChecks':len(paragraph_checks),'verifiedProposedCardMenu':7,'allClassCardFiles':17,'sourceInformationDeleted':0,'newRulesAdopted':False,'runtimeTestsExecuted':0,'humanPlaytested':False}))
    print(json.dumps(json.loads(receipt.read_bytes()),ensure_ascii=False))

if __name__=='__main__':main()
