"""Freeze EPI08-14 evidence and operational questions for actual Part3 review."""
from datetime import datetime, timezone
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib, json, xml.etree.ElementTree as ET
from apply_di7_ap_as_01 import G, R, A, info, encoded

REVIEW = 'COSMOLOGY-EPILOGUE-RELIC-NULL-01'
REQUEST = '''Continue the existing Calibration Review Part3 collaboration. Your exact LP01–LP10 candidate has now been applied locally: current EPI01–07 data and both chapters are included, with110 authored cases preserved. That bounded review is closed. Please now fully author EPI08–14: four relics, twelve chamber seeds, residual Null and four flora/antidote procedures.

Read CURRENT_REVIEW_CONTEXT.json, INTERFACE_QUESTIONS.json and all relevant supplied actual sources. Original manuscript evidence governs subject to explicit owner corrections. Our suggestions are NEW reviewable proposals, not owner orders or recovered canon. Cite exact original paragraphs and current operative rules; do not infer mechanics from names or import another game's attunement, nonlethal, monster or crafting rules silently. All DOCX indices count every w:p including blanks/table cells. Historical workflow statuses in older follow-up files are superseded by CURRENT_REVIEW_CONTEXT and the current EPI01–07 application.

Resolve ordinary mechanical choices now with complete rules. Keep genuine identity/chronology gaps open. In particular retain the original heading 'Dungeon Seeds after Infinite Yield'. The owner has not chosen before/during/after Proof War. Author the12 complete local scenes with a conditional placement record requiring an appropriate actual existing undocumented-floor site; choose no numbered floor, no campaign epoch, no automatic teleport or new hub. Any use outside the original temporal premise must be explicitly recorded as NEW alternate staging, not an assertion that Infinite Yield happened. The scenes can be fully authored while campaign placement remains conditional. Leave EPI15–17 and all wider pending catalogs separate.

Each relic needs a complete physical/magical profile, lawful use/eligibility, actual finite acquisition scene, weight/size/wearing/hand needs, attunement if required, costs/actions/ranges/targets, trigger/commit/recheck, interrupt/miss/failure/depletion, expiry/refresh, transfer/duplicate/loss/destruction rules and exact compatibility with current systems. Finite acquisition must be playable, not 'Director decides later' and not a retroactive gift. New local stock is labeled NEW and only exists when that specific scene is adopted; no repopulation, shared-cache cloning or free class proficiency. New special-item attunement is scoped to these items, not an unannounced universal replacement or borrowed three-item cap.

Each of12 chambers needs concrete local dimensions and connectivity, entrances/exits, what players see/hear, telegraphed danger, actual finite actors/stat blocks, props, objectives, timed choices/checks, fixed success/failure, fallback/withdrawal, rewards, persistent depletion and source/new provenance. Supply self-contained NEW profiles for every creature needed (including toys, Silence Wraith and Echo Doppelganger); do not promote the pending67-dossier bestiary. A fixed illustrative encounter for four level11 PCs is acceptable NEW test tuning, explicitly unbalanced/unplayed; do not assume an actual party exists or auto-scale. Give all AC/HP/speed/senses/ability mods/proficiencies/defenses/actions/attack+damage/DC/duration/behavior needed, and life/death classification. Copies cannot duplicate PCs, inventories, class engines, XP or resources. Do not solve all scenes by forbidding interaction. Players need real finite choices, ordinary exits and consequences.

The existing Floor68 Melted Annex, Floor50 service fallback, finite books, route findings and current research timing are authoritative only for that route. A separate Wax Library seed never resets, relocates or clones them, supplies free Equation evidence, or bypasses library prerequisites. Plane/timeline scenes need deterministic movement/landing/deadlines/return/failure and actual bounded destination contents. They do not approve pending planar/time spells or rewrite history. Every condition uses the current exact envelope or an explicitly NEW local effect. Separate character fiction from real-player personal disclosure; preserve source text while openly adapting coercive source directions for session-zero consent.

For Null resolve the actual damage/Wound/InstantDeath interface explicitly. Our proposed source-specific interpretation is a NEW broad nonlethal override for damage attributed to a currently Veiled character: after ordinary mitigation/TempHP, HP loss can reach0 but that damage packet does not create Wounds, death-save failures or Instant Death; a newly0 living recipient becomes Unconscious/Stable. Already-present death/Wounds and non-damage lethal costs are not undone. This is a proposal, not recovered Core law. You may choose a different coherent rule, but spell out exactly which stages are overridden and why all damage nonlethal remains meaningful. Define objects/constructs, all recipient branches, delayed/shared/reflected damage and independent companions. Do not reinterpret a source's suppression as global immunity or a new Corruption cure. Keep KT/PT, Hunt finality, Dissonance, both Strains and Exhaustion separate.

Bind purge precisely to the now-current mask/petition rules. Do not rewrite the accepted EPI01–07 module under an assumed prior approval: if a narrow extension is needed, list its exact proposed added trigger and costs and distinguish it from the existing fear/Null-lullaby advantage, safe-removal confession and temporary class blessing. All three original purge avenues must be concretely usable; do not require a random future undefined Archon appearance. Finite flora and Bastion flame-water access must be physically authored and stocked without adding a plane-travel right or a quiet ingredient deadlock. This special antidote procedure does not change the687 reviewed trade-recipe count unless separately authorized in a later catalog review.

Return one downloadable DD_Cosmology_Epilogue_Relic_Null_01_Return.zip containing exactly eight root files:
1 REGISTER.json: seven issues EPI-08..14, evidence, decisions and source/preserved/NEW distinctions.
2 RELIC_NULL_MODEL.json: complete current structured candidate with stable IDs,4relics,12complete chambers and actor profiles,Null exposure/suppression/purge/life rules,4flora,antidote,finite access/stock. No dependence on unstated prior proposals.
3 PLAYER_CHAPTER.md: complete discoverable player procedures without Director-only puzzle answers/hidden identities. Label the optional NEW module and actual access conditions.
4 DIRECTOR_CHAPTER.md: complete playable setup, all scenes/answers/stat blocks/stock and exact adjudication. Model/prose must agree; do not replace actual procedures with 'see JSON'.
5 CASEBOOK.json: at least42 fully worked situations: at least4 per relic, one per chamber,8Null cases and6flora/antidote cases. Give initial state, exact actions/rolls/modifiers/DCs, elapsed time, consumed stock and final state. Include adverse/expiry/equality/missing-access cases. These are authored cases, not executed runtime or human tests.
6 SOURCE_HASHES.json: {"sources":[...]} reproducing every supplied SOURCE_BINDINGS.json path/bytes/sha256 from the actual files.
7 VERDICT.md: concrete scope/resolutions and remaining real owner/source questions; no full cosmology/runtime/human/balance/whole-game/publication approval.
8 EVIDENCE_MANIFEST.json: {"files":[{"path":...,"bytes":...,"sha256":...}]} for preceding seven files only.

Use direct citations in register/model/cases: path plus paragraphIndexZeroBased and part, jsonPointer, or firstLineOneBased/lastLineOneBased. Whole located text or its UTF8 SHA256 must match exactly; JSON root pointer is empty string, not '/'. A source supports only what it actually states; invented numbers/stats/stock are explicitly NEW. Verify output manifests, all source bindings, arithmetic, ordinary rest/time/action/skill requirements, finite resources and duplicate wording before returning. Return the download link and concise decision summary. Perform the authoring now, rather than only restating questions.
'''

def read(p): return json.loads(p.read_bytes())

def main():
    root=A/'cosmology-epilogue-relic-null-01'
    archive=A/'DD_Cosmology_Epilogue_Relic_Null_01.zip'
    receipt=A/'COSMOLOGY_EPILOGUE_RELIC_NULL_01_PREPARATION.json'
    assert all(not p.exists() for p in [root,archive,receipt])
    initial=read(A/'cosmology-epilogue-character-01/SOURCE_BINDINGS.json')
    paths=[G/x['path'] for x in initial]
    notes=[A/name for name in ['COSMOLOGY_EPILOGUE_RELIC_NULL_READING_01.json','COSMOLOGY_EPILOGUE_RELIC_SOURCE_FOLLOWUP_01.json','COSMOLOGY_EPILOGUE_NULL_LIFE_SOURCE_FOLLOWUP_01.json']]
    paths += notes + [A/'COSMOLOGY_EPILOGUE_CHARACTER_01_APPLICATION_CHECK.json',
        R/'data/director/cosmology/epilogue_character_reviewed_01.json',
        R/'data/director/cosmology/epilogue_character_cases_01.json',
        R/'docs/mechanics/COSMOLOGY_EPILOGUE_CHARACTER_PLAYTEST.md',
        R/'docs/director-only/cosmology/EPILOGUE_CHARACTER_REVIEWED_01.md']
    paths += [R/'docs/mechanics'/name for name in ['HEALING_DEATH_PLAYTEST.md','DAMAGE_SHARING_PLAYTEST.md',
        'HERBALISM_RECIPE_PLAYTEST.md','HERBALISM_REVIEW_STATUS.json','ALCHEMY_RECIPE_PLAYTEST.md','ALCHEMY_REVIEW_STATUS.json']]
    paths += [R/'data/playtest'/name for name in ['equipment_source_catalog.json','equipment_acquisition_candidate.json','bestiary_public_source_candidate.json','alchemy_recipe_candidate.json','herbalism_recipe_candidate.json']]
    paths += [R/'data/director'/name for name in ['bestiary_source_candidate_internal.json','alchemy_recipe_candidate_internal.json','herbalism_recipe_candidate_internal.json']]
    # Include exact source files referenced by prior bounded dependency readings.
    def visit(v):
        if isinstance(v,dict):
            if isinstance(v.get('path'),str) and (G/v['path']).is_file(): paths.append(G/v['path'])
            for x in v.values(): visit(x)
        elif isinstance(v,list):
            for x in v: visit(x)
    for note in notes: visit(read(note))
    paths=list(dict.fromkeys(paths))
    assert all(p.is_file() for p in paths), [str(p) for p in paths if not p.is_file()]
    inventory=read(A/'ORIGINAL_COSMOLOGY_EPILOGUE_RULE_INVENTORY_01.json')
    assert inventory['source']==info(G/'The Cosmology of Decennium Descent.docx')
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    with ZipFile(G/'The Cosmology of Decennium Descent.docx') as z:
        ps=[''.join(t.text or '' for t in p.findall('.//w:t',ns)) for p in ET.fromstring(z.read('word/document.xml')).findall('.//w:p',ns)]
    checks=[]
    for unit in inventory['units'][7:14]:
        for evidence in unit['evidence']:
            text=ps[evidence['paragraphIndexZeroBased']]
            assert text==evidence['text'] and hashlib.sha256(text.encode()).hexdigest()==evidence['textSha256']
            checks.append({'id':unit['id'],'paragraphIndexZeroBased':evidence['paragraphIndexZeroBased'],'pass':True})
    questions=read(notes[0])['interfaceQuestions']
    extra={
        'EPI-08':['Classify motive-certainty by actual promised output, not merely Divination school. Give at least two actual reviewed spell examples and one pending counterexample from the419/429 index; never promote pending text.', 'Define bearer/caster/target consent timing, multi-target cancellation unit, concentration and no refunds. Actual character communication is separate from player agreement. Item swap cannot reset charges.'],
        'EPI-09':['Actual source Spear:1d6piercing,versatile1d8,Thrown20/60,3lb; relic overrides must be explicit. Soldier eligibility does not itself confer weapon proficiency. Finesse STR/DEX same ability attack/damage; Heavy Small disadvantage is an actual source interface.', 'Concrete proposed hesitation: spend Bonus Action before one actual spear attack on same turn; lose stored benefit at turn end, miss consumes it, no idle precharge. Define floor(characterLevel/2) vs class level openly, crit behavior and thrown/return/recovery. Alternative coherent finite cost is acceptable.'],
        'EPI-10':['Define a single pending mirror-linked beneficiary rather than unbounded gifting. Account for a WIS save made off-turn, successful reroll after initial failure, expiry, destruction away from user and another activation.', 'Finite Sentinel reformation must coexist with EPI07 one information boon per encounter without resetting either ledger. Do not equate reconstructed mirror with an automatically refreshed new item.'],
        'EPI-11':['Source created from dissolved Matrix dust is not a recovered crafting procedure. Provide one finite dust provenance and an explicitly NEW contained fictional fabrication recipe, or a finite already-crafted example, with real acquisition.', 'Determine each observer readability at observation time without using it as infallible allegiance/mind-reading. State whether copying is mundane ciphertext, translation requirements, line of sight and darkness.'],
        'EPI-12':['Supply ordinary exit and one noncombat path in each seed; fixed creature profiles cannot rely on the pending bestiary or vague scale-to-party instructions.', 'Resolve all travelers and full footprints for Shardpool, exact return deadline/equality and blocked origin; no trapping by omitted return machinery. Twin Wind merges no histories/resources and creates no second party.', 'Preserve finite scene identity on repeated visits. Rerolling d12 cannot refill relics, creatures, harvest sites or rewards. Quiet Well uses the exact current Living/Cracked distinction without adding a permanent boon exploit.'],
        'EPI-13':read(notes[2])['nextConferenceQuestions'],
        'EPI-14':['Define units, weight, freshness/storage, stock and one-dose output. Nature identification is separate from harvest work; poison lore and actual tools matter only if current rules grant them.', 'Show a fully timed procurement-to-dose example plus exhausted stock, failed harvest, failed brewing, unwilling/unconscious patient and remaining exposure after purge. New harmless Tranquilthorn/Blackhush uses are allowed if explicitly authored; names alone confer no effects.', 'Provide an actual finite source of Bastion flame water accessible by the stated local scene sequence; home affiliation and the four finite Concord alcoves do not automatically create water stock or an onward route.']
    }
    for q in questions: q['additionalInterfaces']=extra[q['id']]
    now=datetime.now(timezone.utc).isoformat();root.mkdir()
    rows=[]
    for p in paths:
        raw=p.read_bytes();row=info(p,raw);out=root/'sources'/row['path'];out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw);rows.append(row)
    (root/'SOURCE_BINDINGS.json').write_bytes(encoded(rows))
    (root/'REQUEST.txt').write_text(REQUEST,encoding='utf-8',newline='\n')
    (root/'INTERFACE_QUESTIONS.json').write_bytes(encoded({'reviewId':REVIEW,'status':'questions and NEW proposals for review, not adopted','issues':questions,'originalParagraphChecks':checks}))
    context={'reviewId':REVIEW,'recordedAtUtc':now,'scope':[f'EPI-{i:02d}' for i in range(8,15)],
        'currentCharacterModule':info(R/'data/director/cosmology/epilogue_character_reviewed_01.json'),
        'characterApplication':info(A/'COSMOLOGY_EPILOGUE_CHARACTER_01_APPLICATION_CHECK.json'),
        'characterModuleStatus':'Actual Part3 LP01–LP10 exact confirmation received; current module applied. No pending EPI01–07 correction request.',
        'sourceCount':len(rows),'originalParagraphChecks':len(checks),'sourceFailures':0,
        'authority':'Original manuscripts subject to explicit owner corrections. Current reviewed operating sources apply within their bounded domains; missing content is explicitly NEW provisional authorship.',
        'epoch':'Owner choice remains unanswered. Do not select before/during/after Proof War; preserve after Infinite Yield qualification.',
        'spellStatus':{'reviewed':419,'pending':429,'ordinaryTotal':848,'ancestrySeparate':10},
        'tradeRecipes':{'reviewed':687,'public':433,'unchangedBySpecialRelicAndAntidoteDesign':True},
        'bestiary':'67-dossier candidate remains pending; supplied bestiary is source/reference only, not automatically approved.',
        'currentNotebook':'Existing Calibration Review Part3; continue here, no new-chat request.',
        'boundaries':['No87/710date correction','NoBuilder/survivor/OldGod/Ul’nak identity merge','No full Equation recovery','Public reliable ceiling remains failedSixthGate','No free travel or restored consumed research stock','No source deletion','No runtime/human/balance/wholegame/publication approval'],
        'newRulesAdopted':False}
    (root/'CURRENT_REVIEW_CONTEXT.json').write_bytes(encoded(context))
    payloads=[{'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(root.rglob('*')) if p.is_file()]
    (root/'PACKAGE_MANIFEST.json').write_bytes(encoded({'reviewId':REVIEW,'sourceCount':len(rows),'payloads':payloads}))
    with ZipFile(archive,'w',ZIP_DEFLATED) as z:
        for p in sorted(root.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(root).as_posix())
    receipt.write_bytes(encoded({'reviewId':REVIEW,'recordedAtUtc':now,'status':'prepared-not-submitted',
        'archive':info(archive),'sourceCount':len(rows),'originalParagraphChecks':len(checks),'failureCount':0,
        'issues':7,'relicsRequested':4,'chambersRequested':12,'floraRequested':4,'minimumCasesRequested':42,
        'sourceInformationDeleted':0,'newRulesAdopted':False,'runtimeTestsExecuted':0,'humanPlaytested':False}))
    print(json.dumps(read(receipt)))

if __name__=='__main__':main()
