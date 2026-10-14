"""Preserve26 pending rank0..2 Illusion identities and ask full-source questions."""
from pathlib import Path
from collections import Counter
import json,hashlib,re
from prepare_combat_feat_source_audit import section

ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1];AUDIT=GAME/'docs/audit/2026-10-08/full-game'
QUESTIONS={
 'flickerstep':'Preserve +1AC versus one attack and Core one Action/30ft. Decide self or other target, actual cast/attack timing and expiry despite Instantaneous duration. Define one-use consumption at the attack commitment and interaction with a miss/canceled attack, cover, Shield and other AC families. The name does not grant teleportation.',
 'silent-echo':'Define a finite captured last word/phrase within10ft: actual hearing, maximum length, languages, source voice fidelity, projection location/audibility and instant playback. Resolve simultaneous speech and repeated casting. Mimicry creates neither translation, a compelled response nor automatic social or spell-component authentication.',
 'illusive-flash':'Preserve the printed next-enemy-attack disadvantage and Core spell-attack resolution. Specify attack type, eligible perceived target, hit/miss effect, sight/sense dependence, expiry and one-use event. The spell attack delivering the mark is distinct from the target attack consuming it; no automatic cantrip blindness or multiple-disadvantage stacking.',
 'shadow-puppet':'Resolve both small-object movement and shadow movement as printed, with a finite selectable mode. Define object size/mass, attended resistance, origin/radius, travel, support, manipulation and end placement. Keep real mass/custody and distinguish moving an object from animating its image; no unprinted attack, extra hand, remote tool proficiency or magical-body creation.',
 'blurred-visage':'The effect names the caster while Core range is30ft. Set the actual target and precise one-round expiry. Define the scope of half cover versus ranged attacks, how visual illusion interacts with true/alternate senses, and whether its source-limited cover grants any DEX-save benefit. Preserve ordinary cover arbitration and no physical barrier.',
 'prestidigitation':'Preserve both Illusion and Universal placements and both Core versions: concentration up to1minute versus Instantaneous. Give one explicit access/variant disposition and finite harmless modes with sizes, durations, simultaneous limits and material/thermal boundaries. No implied food, water, valuable goods, tool work, healing, damage, identity authentication or external-game menu.',
 'disguise-self-minor':'Define exactly which minor visible self changes are admitted for1minute, including size/silhouette/clothes versus actual body. Separate it from reviewed Disguise Self, actual transformation and other-sense detection. Establish interaction/examination and disclosure rules; no new anatomy, voice, traits, gear, concealment condition or automatic identity success.',
 'phantom-footsteps':'Specify one finite audible footstep sequence, moving path, sound origin/range, pace, obstruction and end under Instantaneous Core duration. Distinguish audible source from physical tracks or a creature. Resolve knowledge, examination, hearing limits and distraction without forced targeting, automatic searching or automatic stealth success.',
 'shadow-mark':'The source promises a persistent-looking mark but Core says Instantaneous. Set target/surface, size, duration, maximum outstanding marks, application to attended objects/creatures and removal/suppression. Only the caster sees the mark under actual line of sight; no tracking through walls, map beacon, remote knowledge or universal identification permission.',
 'blur-vision':'Preserve disadvantage on the next Perception check. Define target eligibility, save or other resolution, expiry and consumption on one real check despite Instantaneous duration. Decide which senses are affected from the actual effect; passive/no-roll procedures do not silently become rolls or inherit a numeric penalty. Maintain source-specific mark identity.',
 'color-spray':'Retain cone, lowest-HP allocation, one-round Blinded and explicit no save. Define cone geometry, budget/dice or other finite target cap, actual HP versus temporary/form pools, ordering/ties, immune or unseeing targets and expiry. Source has no HP-budget number; any completion is NEW. Do not copy an external Color Spray stat block.',
 'veil-of-mist':'Reconcile20ft Core range with20ft-radius illusion. Specify point of origin, immobility/motion, actual obscuration degree, inside/outside sight, alternate senses, knowing observers and interaction. Concentration up to1minute is supplied. Illusory fog is not physical moisture, wind obstruction, fire control or automatic Hide permission.',
 'phantom-grasp':'Preserve1d6 psychic and DEX-save-or-Restrained1round, while Core duration is concentration up to1minute. Define save timing and damage on success/failure, one target, whether restraint expires earlier than the parent, escape/repeat saves and possible maintenance. No actual creature/hand, Grappled alias, repeated unprinted damage or physical hauling.',
 'mask-voice':'Preserve60ft mimicry and WIS-save-to-detect. Decide whether the caster voice changes or a remote sound is projected, required original-voice sample, duration despite Instantaneous, listener timing/rechecks and what a success reveals. Keep hearing, language, agency and spell components distinct; failed detection is not compulsion or guaranteed fraud.',
 'false-footsteps':'Preserve audible steps and printed3round duration despite Core Instantaneous. Define origin, controllable path/pace, sound obstruction, concentration choice and stable expiry. Explain difference from cantrip Phantom Footsteps and reviewed Ghost Sound. No actual tracks/creature, free sustained tactical actions or mandatory enemy pursuit.',
 'illusory-script':'Define actual writing surface, message length/language, intended-recipient specification, visible fallback, reading conditions, duration/removal and copied/moved documents. Resolve Instantaneous source duration versus restricted readability. No translation, remote reading, automatic secrecy from every sense, signature authority or unlimited valuable/consumed ink.',
 'distort-value':'Set one actual item and finite cosmetic value appearance, observer investigation/appraisal procedure, duration, concentration and visibility/touch limits. It does not change mass, grade, material, actual reference price or compel a sale. Preserve economy and social adjudication; no fixed sale multiplier is present in the source.',
 'uncontrollable-laughter':'Preserve exact catalog identity separately from the possible historical Tasha-name alias until explicitly reconciled. Define resistance, eligible creature/senses, duration/concentration, repeat saves/damage endings, Prone and Incapacitated timing and what remains after either ends. Core Instantaneous cannot silently authorize indefinite action denial.',
 'illusory-terrain':'Define a bounded small terrain area, shape/range, visual and other sensory scope, duration/concentration and examination/physical contradiction. Distinguish actual traversability/hazards from perceived terrain and from higher Hallucinatory Terrain. No real cover, support, difficult terrain, water, bridge, maps or hazard immunity through an image.',
 'blur':'Effect states attacks against you for duration but Core gives30ft/Instantaneous. Explicitly settle self targeting, duration/concentration, which senses/attacks qualify, conditions suppressing the visual defense and recast identity. Keep ordinary advantage cancellation; no teleport, opacity, AC candidate or immunity to area/save effects.',
 'phantom-decoy':'Preserve caster image and2d6 psychic in10ft burst on detonation. Define where image appears, size/senses, lifetime, trigger/manual detonation action, eligibility/save and damage on success. Separate cast range from burst radius, once-only damage and simultaneous trigger ordering. No creature, extra action engine or automatically targetable combatant.',
 'invisibility':'Preserve1minute or until action taken, rather than importing an attack/spell-only ending. Define target, willingness, concentration choice, carried/worn gear boundaries and exactly which Action/BonusAction/Reaction/free interactions end it and at what checkpoint. Apply reviewed Invisible/sight/Hide distinctions; movement, sound and actual location remain meaningful.',
 'illusory-flames':'Preserve3d6 psychic and WIS-failure panicked clause. Define full save outcome, duration, concentration and finite source-specific control; Panicked is not a named current condition. Decide whether to bind to reviewed Frightened or author a distinct bounded behavior, including immunity/senses. No real fire, Burning or flammable material damage is implied.',
 'phantasmal-force':'Retain both rank2 and rank3 placements/Core versions, including30/60ft range and3/5RP. Explicitly reconcile one ordinary identity and actual class rank without silently promoting an unassigned variant. Define private target perception, resistance/investigation,1d6-per-round checkpoint, duration/concentration, physical contradictions and single damage event; no real support or infinite repeat triggers.',
 'shadow-blade':'Preserve a conjured blade doing2d8 psychic, with Core Action/30ft/Instantaneous requiring an explicit duration/body interpretation. Define actual holder, weapon/attack proficiency and ability, hands, properties, attack action cost, dismissal/loss/transfer, suppression and equipment/meld treatment. No companion, ordinary market material, bonus attack or automatic scaling from external rules.',
 'silence':'Preserve20ft-radius sphere and resolve Core20ft range versus origin/area and Instantaneous versus ongoing effect. Define duration/concentration, sound crossing boundaries, inside/outside hearing, moving creatures and verbal casting/commands. Distinguish the area from the Silenced condition; no assumed thunder immunity, vacuum or soundless physical event unless explicitly authorized.'}
PENDING_COUNTERPARTS=['major-image','greater-invisibility','hallucinatory-terrain','mislead','magic-mouth','light','mage-hand','true-strike','arcane-mark']
REFS={
 'SPELL_INTEGRATION_RULES.md':None,
 'CORE_RESOLUTION_PLAYTEST.md':['Which rule applies','Rolls','Resolve a damage event'],
 'COMBAT_ACTION_PLAYTEST.md':['Encounter and action resources','Time and event ordering — NEW','Standard Actions','Ready','Movement and geometry','Cover, sight, Hide and Search'],
 'CONTROL_STATES_PLAYTEST.md':['Records, clocks and precedence','Marks and one-use components','Compulsion, action denial and initiative'],
 'CONDITIONS_PLAYTEST.md':['Shared handling','Blinded','Deafened','Frightened','Incapacitated','Invisible','Prone','Restrained','Silenced'],
 'EQUIPMENT_ACQUISITION_PLAYTEST.md':['Hands and focuses','Weapons and ammunition','Carrying and containers'],
 'BODY_EQUIPMENT_PLAYTEST.md':None,
 'CHARACTER_CREATION_PLAYTEST.md':['One shared RP pool','Shared strain, recovery and concentration']}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def current_book_rows():
    # Current preserved extraction is BOM-marked UTF16 plain text. The historical
    # catalog builder expects UTF8 Markdown; do not rewrite either source to fit.
    p=ROOT/'rulebook_output.txt';raw=p.read_bytes()
    assert raw[:2] in (b'\xff\xfe',b'\xfe\xff')
    rows=[];school=None;level=None;school_counts=Counter()
    for i,line in enumerate(raw.decode('utf-16').splitlines()):
        m=re.match(r'^Expanded (Abjuration|Conjuration|Divination|Enchantment|Evocation|Illusion|Necromancy|Transmutation|Universal) Spell List',line)
        if m:school=m[1];level=None;continue
        if not school or school_counts[school]>=104:continue
        if re.match(r'^Cantrips \(Level 0\)',line):level=0;continue
        m=re.match(r'^Level (\d+) Spells',line)
        if m:level=int(m[1]);continue
        if level is not None and ' – ' in line:
            name,summary=line.split(' – ',1)
            rows.append({'line':i+1,'name':name,'school':school,'level':level,'summary':summary,'exactText':line});school_counts[school]+=1
    assert len(rows)==936 and dict(Counter(school_counts.values()))=={104:9}
    return rows
def main():
    protected={}
    def read(p):protected[p.relative_to(GAME).as_posix()]=sha(p);return json.loads(p.read_text(encoding='utf-8-sig'))
    catalog=read(ROOT/'data/public/spell_playtests/catalog.json');rows=catalog['spells'];by={r['id']:r for r in rows}
    source=read(ROOT/'data/playtest/spell_sources/catalog.json');core=read(ROOT/'data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json')
    manifest=read(ROOT/'data/public/spell_playtests/manifest.json');queue=read(ROOT/'data/public/spell_playtests/incomplete_queue.json')
    for p in [ROOT/'src/data/spells.js',ROOT/'rulebook_output.txt',ROOT/'class_spell_school_mapping.csv',ROOT/'class_spell_progression.csv']:
        protected[p.relative_to(GAME).as_posix()]=sha(p)
    actual=json.JSONDecoder().raw_decode((ROOT/'src/data/spells.js').read_text(encoding='utf-8').split('export const SPELLS = ',1)[1])[0]
    assert actual==source and len(source)==848
    pending=[r for r in rows if r['operational'] is None]
    selected=[r for r in pending if r['schools'][0]=='Illusion' and min(v['rank'] for v in r['classAccess'].values())<=2]
    assert len(selected)==26 and {r['id'] for r in selected}==set(QUESTIONS)
    placements=current_book_rows();assert len(placements)==936
    for r in rows:
        assert r['source']['original']==source[r['id']]
        for x in r['source']['coreEntries']+r['source']['possibleHistoricalAliases']:assert x['original']==core['spells'][x['index']]
    book_bindings=[]
    for r in selected:
        names={r['name']}|{e['original']['name'] for e in r['source']['possibleHistoricalAliases']}
        for p in r['source']['original']['placements']:
            matches=[b for b in placements if b['name'] in names and b['school']==p['school'] and b['level']==p['level']]
            assert len(matches)==1 and matches[0]['summary']==p['summary'],r['id']
            book_bindings.append({'spellId':r['id'],'catalogPlacement':p,'currentBookRow':matches[0],'nameDifferencePreserved':p['name']!=matches[0]['name']})
    related=[r for r in rows if r['operational'] is not None and 'Illusion' in r['schools']]+[by[id] for id in PENDING_COUNTERPARTS]
    # Protect every individually authored spell batch and retain complete exact
    # counterpart rows, not just spell names or abbreviated summaries.
    for p in sorted((ROOT/'data/playtest/spell_drafts').glob('batch_*.json')):protected[p.relative_to(GAME).as_posix()]=sha(p)
    bindings=read(ROOT/'data/public/spell_playtests/class_spell_bindings.json');mentions=read(ROOT/'data/public/spell_playtests/class_name_mentions_for_review.json')
    selected_mentions=[r for r in mentions if r.get('spellId') in QUESTIONS]
    cm=read(ROOT/'data/public/class_playtests/manifest.json');class_records=[]
    for c in cm['classes']:
        p=(ROOT/'docs/mechanics'/c['data']).resolve();d=read(p)
        for card in d['cards']:
            text=json.dumps(card,ensure_ascii=False)
            hits=[r['id'] for r in selected if re.search(r'(?<!\w)'+re.escape(r['name'])+r'(?!\w)',text,re.I)]
            if hits:class_records.append({'class':c['class'],'path':p.relative_to(GAME).as_posix(),'card':card,'spellNameMatches':hits,'scope':'Textual comparison only; neither an ordinary spell grant nor an identity/effect merge.'})
        for i,para in enumerate(d.get('engine',[])):
            text=json.dumps(para,ensure_ascii=False);hits=[r['id'] for r in selected if re.search(r'(?<!\w)'+re.escape(r['name'])+r'(?!\w)',text,re.I)]
            if hits:class_records.append({'class':c['class'],'path':p.relative_to(GAME).as_posix(),'engineIndex':i,'paragraph':para,'spellNameMatches':hits,'scope':'Textual comparison only; no automatic spell grant.'})
    excerpts=[]
    for name,heads in REFS.items():
        p=ROOT/'docs/mechanics'/name;t=p.read_text(encoding='utf-8');protected[p.relative_to(GAME).as_posix()]=sha(p)
        for h in heads or [None]:excerpts.append({'file':p.relative_to(GAME).as_posix(),'sha256':sha(p),'heading':h or 'entire guide','exactText':section(t,h) if h else t})
    conflicts=[]
    for r in selected:
        entries=r['source']['coreEntries']
        if len(entries)>1:
            fields={k:[{'index':e['index'],'value':e['original'].get(k)} for e in entries] for k in set().union(*(e['original'] for e in entries)) if len({json.dumps(e['original'].get(k),sort_keys=True) for e in entries})>1}
            conflicts.append({'spellId':r['id'],'differingCoreFields':fields,'disposition':'joint decision pending; all versions preserved'})
    common='For every selected spell, settle all operational fields: actual activation and components, legal target/range/geometry, duration and concentration, resolution/DC/save or attack, full effect clauses, scaling, repeat casting/source identity, suppression/ending, limits and class-specific rank/cost access. Preserve printed clauses and every original source. Explicitly label NEW completions; no external-game import or automatic historical alias merge.'
    records=[{'spellId':r['id'],'questionId':f'IL-{i+1:02}','fullSourceAndCurrentAccessRecord':r,'recordSha256':digest(r),'individualQuestion':QUESTIONS[r['id']]} for i,r in enumerate(selected)]
    checks=[('848 complete canonical identities and936 placements preserved',len(rows)==848 and len(placements)==936 and len({r['id'] for r in rows})==848),('276 prior operational records and572 pending retained',sum(r['operational'] is not None for r in rows)==276 and len(pending)==572),('26 exact remaining low-rank Illusion identities',len(records)==26 and all(r['operational'] is None for r in selected)),('Every original matches actual catalog/Core;28 selected current-book rows bound',len(book_bindings)==28),('Every selected spell has individual full-source question',all(len(r['individualQuestion'])>190 for r in records)),('Both multiply placed source identities retained', {c['spellId'] for c in conflicts}=={'prestidigitation','phantasmal-force'}),('Uncontrollable Laughter historical alias retained without merge',len(by['uncontrollable-laughter']['source']['possibleHistoricalAliases'])==1 and not by['uncontrollable-laughter']['source']['coreEntries']),('All17 class catalog routes inspected including separate Bard',len(cm['classes'])==17),('Exact governing excerpts',all(z['exactText'] in (GAME/z['file']).read_text(encoding='utf-8') for z in excerpts)),('Panicked not a named current condition',not re.search(r'^## Panicked\s*$',(ROOT/'docs/mechanics/CONDITIONS_PLAYTEST.md').read_text(encoding='utf-8'),re.M)),('All protected inputs unchanged',all(sha(GAME/p)==h for p,h in protected.items()))]
    assert all(v for _,v in checks),[n for n,v in checks if not v]
    counts={'sourceSpells':848,'sourcePlacements':936,'reviewedOperational':276,'remaining':572,'selectedLowIllusion':26,'selectedPlacements':sum(len(r['source']['original']['placements']) for r in selected),'selectedExactCoreEntries':sum(len(r['source']['coreEntries']) for r in selected),'selectedAliasRecords':1,'reviewedCounterparts':16,'pendingCounterparts':len(PENDING_COUNTERPARTS),'classComparisonRecords':len(class_records),'classTextualMentionBindings':len(selected_mentions),'governingExcerpts':len(excerpts),'multiCoreConflicts':len(conflicts)}
    data={'status':'prepared-not-sent; source questions only','selection':'Remaining primary-Illusion identities with minimum current class rank0..2; placement/rank conflicts remain preserved','commonOperationalQuestion':common,'selectedSpells':records,'completeCounterparts':related,'classComparisonRecords':class_records,'existingTextualMentionBindings':selected_mentions,'classSpellBindings':[b for b in bindings if set(b.get('sameNameCatalogIds',[])).intersection(QUESTIONS)],'multiCoreSourceDifferences':conflicts,'currentRankCosts':catalog['costByRank'],'currentClassProgression':catalog['classProgression'],'currentGoverningExcerpts':excerpts,'counts':counts,'checks':[{'name':n,'pass':v} for n,v in checks],'protectedFiles':protected,'spellsApproved':0,'sourceInformationDeleted':0,'cosmology':'post-push only; no shadow/illusory/spectral term establishes an origin or plane','futureDispatch':'Finish active Fishing conference and recheck current dependencies before dispatch. Author full cards only after source decisions, then separate exact review.'}
    data['currentBookBindings']=book_bindings;data['currentBookEncoding']='UTF16 BOM plain text; original bytes unchanged; historical Markdown parser is not applicable'
    dump(AUDIT/'LOW_ILLUSION_SPELL_SOURCE_PREPARATION.json',data)
    lines=['# Low-rank Illusion spell source audit','',data['status'],'',common,'',f"All26 selected identities remain among572 unfinished spells;276 prior operational records are unchanged. Full27 exact Core rows andone historical alias are preserved alongside28 original placements. Prestidigitation and Phantasmal Force retain their conflicting Core variants. Panicked has no current named condition entry. All17 class catalogs, including the separately stored Bard, were inspected; textual overlaps never grant access.",'','| Case | Spell | Individual source question |','|---|---|---|']
    lines += [f"| {r['questionId']} | {r['fullSourceAndCurrentAccessRecord']['name']} ({r['spellId']}) | {r['individualQuestion']} |" for r in records]
    lines+=['','These are26 source discussions prepared,not26 operational cards or approvals. Nine additional pending comparison identities retain their own review routes. All sources and earlier operational spell batches remain unchanged. Fishing is the active conference; do not interrupt it or resend an active packet. Cosmology follows the verified GitHub push.','']
    text='\n'.join(lines);(AUDIT/'LOW_ILLUSION_SPELL_SOURCE_AUDIT.md').write_text(text,encoding='utf-8')
    packet='PREPARED LOW-RANK ILLUSION SOURCE CONFERENCE — NOT SENT.\n\n'+text+'\nCOMPLETE SOURCES, COMPARISONS AND CURRENT DEPENDENCIES\n'+json.dumps(data,ensure_ascii=False,separators=(',',':'))
    p=AUDIT/'CODEX_LOW_ILLUSION_SPELL_SOURCE_PREPARED.txt';p.write_text(packet,encoding='utf-8',newline='\n')
    status={'status':'prepared-not-sent','packetFile':p.name,'characters':len(packet),'packetSha256':sha(p),'counts':counts,'checkCount':len(checks),'protectedFilesUnchanged':len(protected),'spellsApproved':0,'sourceInformationDeleted':0,'cosmology':'post-push only'};dump(AUDIT/'LOW_ILLUSION_SPELL_SOURCE_STATUS.json',status);print(json.dumps(status))
if __name__=='__main__':main()
