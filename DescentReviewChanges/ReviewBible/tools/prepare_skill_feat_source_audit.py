"""Complete remaining source-category Skill feat packet; no new rules."""
from pathlib import Path
import json,re
from prepare_combat_feat_source_audit import ROOT,GAME,AUDIT,read,sha,digest,write,dump,section

QUESTIONS={
'acrobatic_mastery':"Bind Failure versus Critical Failure under task degrees, opposed-check loss, selection of the rerolled d20 under advantage/disadvantage, natural shifts, information window and mandatory new result. Define Long Rest recovery and interaction with other rerolls without assuming a daily clock.",
'battlefield_tactician':"Bind Soldier to the actual class or another sourced credential and define tactics rolls against the20 basic skills. Preserve+2 as a task bonus, not an automatic attack, class save-DC or engine-resource improvement. Identify actual tactics situations and stacking.",
'beast_whisperer':"Resolve natural1→2 before task-degree shifts, both dice under advantage/disadvantage and repeated rerolls. A2 can still fail critically by margin: preserve the current effect separately from the broader inactive legacy promise. Bound simple emotional communication, actual beast senses and no language/command authority.",
'climb_anywhere':"Resolve Athletics4+ and the actual walking-to-climb Speed binding, handholds/hands/anatomy, encumbrance, armor, terrain and dynamic Speed changes. Define checks on sheer/inverted surfaces, failure/fall consequences and which angle-only disadvantage is removed without granting adhesive support.",
'cold_reader':"Resolve Insight5+, the full minute of actual observable speech, hearing/language/access requirements and the opposed Insight/Deception tie rule. Define one genuine surface motive/pressure/goal, retries, duration and no telepathy, hidden fact creation or compelled truth.",
'cultural_expert':"Choose actual History, Religion or supported culture-specific Lore credential; resolve duplicate training and whether expertise applies only to the listed cultural subject matter. Define an unsupported Lore label without inventing automatic knowledge, new histories or cosmology.",
'disguise_expert':"Resolve Deception4+, actual10-minute materials/kit procedure, creator versus wearer, identity constraints and detection. Define the+2 bonus layer alongside current Tailoring/Leatherworking task families and actor-specific attire checks without publishing private garment formulas.",
'dungeon_cartographer':"Define normal travel pace, actual visibility/recording tools, ten-minute mapping requirement and what reliable means. Bind map access/copies, actual users, retrace-check scope, changing routes and reshape invalidation; no omniscient floor map or automatic navigation.",
'field_surgeon':"Bind genuine stabilization of a dying creature through Medicine or an actual kit, action/payment and successful event timing. Resolve once-per-Long-Rest per recipient versus practitioner, positive-healing gates, anti-loop ledgers and coexistence with reviewed Field Medic tempHP. Stable/already-conscious/dead subjects do not manufacture a new stabilization event.",
'forensic_investigator':"Resolve Investigation5+, ten-minute scene examination, appropriate senses/access, actual successful check and a finite additional physical clue. Define no-extra-clue cases, repeat examinations, lost/moved evidence and no fabricated suspect identity or Director duty to create impossible evidence.",
'intuitive_reflex':"Bind+2 initiative as the actual Dexterity check bonus, stacking with Alert/Alertness and other bonus families, future rolls versus rewriting established order, rerolls, injuries and extra turns. Resolve whether its source category affects acquisition only.",
'librarian_s_eye':"Define substance versus verbatim recall, actual prior reading/study, language/decoding, damaged or altered memory, and quote/locate/compare check domains. Bind+2 to actual tasks without remote text access, automatic factual truth or free research/formula acquisition.",
'lock_savant':"Resolve Thievery5+ against current tools/skills; define complex locks, required implements/access, actual+2 check and trap eligibility. Resolve fail-by5 versus natural1 task downgrade, repeated attempts, multiple/independent triggers and magical locks. It does not waive physically triggered traps merely by renaming the task.",
'master_tracker':"Preserve compatibilityAliases as an alias of this source identity, not another acquisition or bonus. Resolve Survival4+, normal travel pace, actual track availability and environment, approximate count/size/age on success, task degrees and no information from nonexistent tracks.",
'rogue_s_escape':"Define declaration and charge use for automatic success on an actual allowed grapple/restraint escape check or save. Bind action/time, source-specific escape availability, multiple restraints, no-save/no-check prisons and physical destination. It does not automatically grant teleportation or an escape roll absent from the source.",
'runic_scholar':"Resolve Arcana5+, one-minute real study/sight/language requirements, school and activation-method information, harmfulness and mythic concealment. Define the no-trigger protection's exact scope against proximity/touch/time triggers without making all runes inert or granting activation/control/formula knowledge.",
'silent_movement':"Identify source authority for any difficult-terrain Stealth disadvantage; remove only the actual nonmagical terrain cause. Define half-Speed silent travel, costs on debris, sound versus visual detection, armor noise, legal Hide and magical terrain. No automatic Hidden or ignored movement cost.",
'silver_tongue':"Define formal diplomacy/negotiation/mediation and the actual Persuasion checks receiving+2. Resolve other skill/tool/attire bonus families, genuine social stakes and no automatic consent, compelled attitude change or universal discount.",
'spell_scribe':"Distinguish spellbook learning/copying, actual scroll duplication and Scribing craft formulas. Bind source access, repertoire/rank/language, half active time and25-percent mundane-material reduction with exact quantities/rounding; rare inks/unique components unchanged. Resolve Craftsman/Forge Dwarf/research reductions without creating a copying procedure or free outputs.",
'steady_hands':"Define motion, poor footing and minor injury causes of Sleight of Hand disadvantage, especially existing Injury penalties versus disadvantage. Remove only qualifying causes; keep blindness, hostile interference, bad tools, no hands and other restrictions. Apply ordinary cancellation afterward.",
'trap_sense':"Resolve Perception4+, normal travel pace, passive detection procedure, actual senses and detectable clues. Define trap versus creature/spell/hazard, sight at the saving-throw event and the+2 save modifier. Detecting a trap neither disarms it nor cancels unseen portions or independent triggers.",
'unshakeable':"Bind intimidation/coercion/fear as actual saves or opposed checks and identify the defending skill/ability, preserving+2. Resolve ordinary fixed-DC tasks, social influence, Frightened condition/escape saves and immunity versus bonus; no universal mind-control immunity.",
'wilderness_chef':"Resolve Nature4+ and define what the source's two bonus effects are, to which real forage output they attach, activation/duration/frequency/recipients and consumable cost. Compare reviewed Chef/Cooking/Herbalism/finite harvest without inventing extra biomass or treating legacy+10% as a second benefit.",
'anatomy_lore':"Bind Knowledge (Monstrous Humanoids) OR Survival to actual credentials; Bonus Action, range/line, one weak-point mark and expiry. Define next-hit+50% damage OR Huge-target advantage choice, payment/miss handling, short-rest Strength save DC and half-Speed timing. Resolve Precision Strike/Giant Slayer/critical multipliers without anatomical or cosmological retcons.",
'beast_lore':"Preserve all three clauses: actual Animal Handling/Survival advantage, successful knowledge check granting allies+2 to hit for1minute, and once-per-Short-Rest call within300ft/DC15 for one nonhostile CR≤1 beast and a simple task. Define action/time/targets/beneficiary range, existing eligible beast availability, travel, agency, communication, duration and command budgets; no summoned or duplicate creature."
}
RELATED=['alert','alertness','animalAffinity','burglar','chef','craftsman','diligent_researcher','field_medic','healer','keen_mind','linguist','giant_slayer','precision_strike']
CONTEXT={
 'CORE_RESOLUTION_PLAYTEST.md':['Which rule applies','Rolls','Zero HP and recovery'],
 'COMBAT_ACTION_PLAYTEST.md':['Encounter and action resources','Time and event ordering — NEW','Movement and geometry','Cover, sight, Hide and Search'],
 'CHARACTER_CREATION_PLAYTEST.md':['Abilities and training','Gain a level'],
 'CHARACTER_FOUNDATION_TABLES.md':['Ability-check skills'],
 'HEALING_DEATH_PLAYTEST.md':['ZeroHP permissions and start timing','Ordinary healing arithmetic','Recovery gates, triggers and loops'],
 'BUFFER_FEAT_PLAYTEST.md':['Shared rules','Chef — General; no prerequisite','Field Medic — General; trained in Medicine'],
 'CRAFTING_HARVEST_PLAYTEST.md':['One work order, one batch','Training and recipe access','The crafting check','Active time and expedition scheduling','Quality and finite output','Identify and harvest','Salvage, research and sale'],
 'EQUIPMENT_ITEM_PROCEDURES.md':None,
 'SPELL_INTEGRATION_RULES.md':['Select a spell','Reviewed Divination cantrip information boundaries','Mark Omen and Fate Coin: reviewed spell-specific rerolls']}
def main():
    p=ROOT/'src/data/feats.js';raw=json.JSONDecoder().raw_decode(p.read_text(encoding='utf-8').split('export const feats = ',1)[1])[0];by={f['id']:f for f in raw}
    craft=read(AUDIT/'CRAFTING_FEAT_INTERFACE_PREPARATION.json');combat=read(AUDIT/'COMBAT_FEAT_SOURCE_PREPARATION.json')
    reviewed=set(read(ROOT/'data/public/feat_playtests/manifest.json')['operationalIds'])
    routed={z['featId'] for z in craft['selectedFeats']+combat['selectedFeats']}
    selected=[f for f in raw if f['type']=='Skill' and f['id'] not in reviewed|routed]
    assert len(selected)==25 and {f['id'] for f in selected}==set(QUESTIONS)
    pending=read(AUDIT/'REMAINING_FEAT_CATALOG_PREPARATION.json')
    protected=dict(combat['protectedFiles'])
    def protect(path):protected[str(path.relative_to(GAME)).replace('\\','/')]=sha(path)
    boundaries=[]
    for name,heads in CONTEXT.items():
        path=ROOT/'docs/mechanics'/name;t=path.read_text(encoding='utf-8');protect(path)
        for h in heads or [None]:
            boundaries.append({'file':str(path.relative_to(GAME)).replace('\\','/'),'fileSha256':sha(path),'heading':h,'exactText':section(t,h) if h else t,'scope':'current saved manuscript and its own stated review limits'})
    foundation_path=ROOT/'data/playtest/character_foundation.json';foundation=read(foundation_path);protect(foundation_path)
    soldier_path=ROOT/'data/public/class_playtests/soldier.json';soldier=read(soldier_path);protect(soldier_path)
    dependencies={'skillAbilities':foundation['skillAbilities'],'soldierFoundation':next(c for c in foundation['classes'] if c['slug']=='soldier'),'soldierEngine':soldier['engine'],'soldierStatus':soldier['status'],'interpretation':'preserved actual class and20 basic skills; does not itself map tactics/Thievery/Lore or approve feat prerequisites'}
    rows=[]
    for f in selected:
        signals=[]
        for field,pattern in [('prerequisite',r'\b(?:Athletics|Insight|Deception|Investigation|Thievery|Survival|Arcana|Stealth|Perception|Nature)\s+[45]\+'),('effect',r'\b\d+(?:\.\d+)?%|\b25 percent\b|\b(?:mythic concealment|bonus effects|tactics rolls|normal pace|normal travel pace)\b')]:
            for m in re.finditer(pattern,f.get(field,''),re.I):signals.append({'field':field,'span':[m.start(),m.end()],'exactText':m.group()})
        rows.append({'featId':f['id'],'sourceObject':f,'sourceObjectSha256':digest(f),'questionId':f'SF-{len(rows)+1:02}','fullClauseQuestion':QUESTIONS[f['id']],'literalReviewSignals':signals,'currentOperationalStatus':'full-feat-review-pending'})
    related=[{'sourceObject':by[id],'currentOperationalReviewed':id in reviewed,'scope':'dependency evidence, not another approval'} for id in RELATED]
    for name in ['COMBAT_FEAT_SOURCE_PREPARATION.json','CRAFTING_FEAT_INTERFACE_PREPARATION.json']:protect(AUDIT/name)
    checks=[
      ('Both335 source registries byte-identical',len(raw)==335 and p.read_bytes()==(GAME/'src/data/feats.js').read_bytes()),
      ('All327 pending source records unchanged',[f for f in raw if f['id'] not in reviewed]==[r['sourceObject'] for r in pending['records']]),
      ('All25 remaining source-category Skill records exact',len(selected)==25 and sum(f['type']=='Skill' and f['id'] not in reviewed for f in raw)==36),
      ('No overlap with71 already routed pending feats or8 reviewed',len(routed)==71 and len(reviewed)==8 and not set(QUESTIONS).intersection(routed|reviewed)),
      ('Complete source records and hashes retained',all(z['sourceObject']==by[z['featId']] and z['sourceObjectSha256']==digest(by[z['featId']]) for z in rows)),
      ('25 individual full-clause questions',len(QUESTIONS)==25 and all(len(z['fullClauseQuestion'])>100 for z in rows)),
      ('Every literal signal has exact field span',all(z['sourceObject'][s['field']][s['span'][0]:s['span'][1]]==s['exactText'] for z in rows for s in z['literalReviewSignals'])),
      ('Master Tracker compatibility alias unchanged',by['master_tracker']['compatibilityAliases']==['skill_feats1_master_tracker']),
      ('13 counterpart objects with correct prior status',len(related)==13 and sum(z['currentOperationalReviewed'] for z in related)==2),
      ('20 current basic skills andactual Soldier identity',sum(map(len,foundation['skillAbilities'].values()))==20 and dependencies['soldierFoundation']['slug']=='soldier'),
      ('All boundary excerpts exactly present',all(z['exactText'] in (GAME/z['file']).read_text(encoding='utf-8') for z in boundaries)),
      ('All protected sources andexisting candidates unchanged',all(sha(GAME/q)==h for q,h in protected.items()))]
    assert all(v for _,v in checks),[n for n,v in checks if not v]
    counts={'sourceFeats':335,'operationalReviewed':8,'pending':327,'selectedSkill':25,'previouslyPreparedCrafting':24,'previouslyPreparedCombat':47,'remainingFocusedPreparation':231,'counterpartRecords':13,'reviewedCounterparts':2,'currentGuideExcerpts':len(boundaries),'numericSkillPrerequisiteOccurrences':sum(s['field']=='prerequisite' for z in rows for s in z['literalReviewSignals'])}
    data={'status':'prepared-not-sent; source evidence andquestions only','sourceFile':str(p.relative_to(GAME)).replace('\\','/'),'sourceFileSha256':sha(p),'selection':'Every remaining pending source type Skill, excluding11 already in crafting packet; categories are navigation only','selectedFeats':rows,'counterpartSources':related,'foundationAndClassDependencies':dependencies,'currentGoverningExcerpts':boundaries,'counts':counts,'checks':[{'name':n,'pass':v} for n,v in checks],'protectedFiles':protected,'newRules':False,'featsApproved':0,'cosmology':'post-push only; no new cultures,ancestries orcreature ontology'}
    dump(AUDIT/'SKILL_FEAT_SOURCE_PREPARATION.json',data)
    lines=['# Skill feat source review preparation','',data['status'],'',
      'All 25 pending source-category Skill feats outside the earlier crafting packet are preserved in full. This includes Spell Scribe, Wilderness Chef, Anatomy Lore and Runic Scholar, whose interfaces must accompany later crafting/combat discussions. The selection is exhaustive for the remaining source category, not a claim that all skill-related feats in other categories are covered.','',
      'Each original description, effect, prerequisite, source status and legacy clause remains intact. Master Tracker retains its existing compatibility alias as a single identity. There are 13 complete counterpart records, including the previously reviewed Chef and Field Medic; neither source inclusion nor a matching name reopens or grants another approval.','',
      '| Case | Full feat | Source prerequisite | Full-clause decision needed |','|---|---|---|---|']
    for z in rows:
        f=z['sourceObject'];lines.append(f"| {z['questionId']} | {f['name']} ({f['id']}) | {f['prerequisite']} | {z['fullClauseQuestion']} |")
    lines+=['','## Shared interfaces','',
      'Resolve numeric skill prerequisites such as Athletics4+ or Insight5+ against actual character training; do not silently interpret them as trade levels, skill ranks or current total modifiers. Resolve Tactics, Thievery, culture-specific Lore and Knowledge (Monstrous Humanoids) against the preserved20 basic skills and actual tool/knowledge grants.','',
      'Use the actual Core task degrees, opposed ties, natural-die shifts, ordinary saves, proficiency once and reroll procedure. Define every information benefit without creating nonexistent clues, tracks, books, ingredients, beasts or willing NPC cooperation. Costs, hands, materials, real access, action timing, duration, cadence and use-recovery clocks remain separate from numerical bonuses.','',
      'Spell Scribe is not automatically a Scribing recipe or permission to duplicate spell scrolls. Wilderness Chef supplies no defined bonus-effect list. Disguise Expert needs the final Tailoring task/slot interface once exact review completes; do not treat the currently submitted draft as exact-approved. Anatomy Lore must be supplied with the Combat packet before Precision Strike/Giant Slayer decisions.','',
      'Prepared, not sent. Complete active Tailoring review before another conference. Before dispatch, attach current applicable revisions and any actual travel/exploration/scroll-copying procedures needed by these cases; those wider systems are not completed by this source packet. No new rule, source deletion, runtime integration, balance approval or cosmology review is claimed.','']
    audit='\n'.join(lines);write(AUDIT/'SKILL_FEAT_SOURCE_AUDIT.md',audit)
    packet='\n\n'.join(['PREPARED SKILL FEAT SOURCE CONFERENCE — NOT SENT.\n\nThis contains all25 remaining source-category Skill feats,25 specific full-clause questions,13 full counterpart records,actual20-skill/Soldier data and exact current guide excerpts. Return finite numbered authoring decisions, distinguishing existing authority from NEW completions. Preserve the full current and legacy wording. No other-category skill-related feat is silently completed. Current operational feat count remains8/335,327pending. Update current dependency status before dispatch; finish active Tailoring exact review first. Cosmology remains post-push only.',audit,'COMPLETE25 SOURCES AND QUESTIONS',json.dumps(rows,ensure_ascii=False,separators=(',',':')),'THIRTEEN COMPLETE COUNTERPART SOURCES AND CURRENT STATUS',json.dumps(related,ensure_ascii=False,separators=(',',':')),'ACTUAL FOUNDATION AND SOLDIER DEPENDENCIES',json.dumps(dependencies,ensure_ascii=False,separators=(',',':')),'EXACT CURRENT GUIDE EXCERPTS',json.dumps(boundaries,ensure_ascii=False,separators=(',',':')),'LOCAL PRESERVATION EVIDENCE',json.dumps({'counts':counts,'checks':data['checks'],'protectedFiles':protected},ensure_ascii=False,separators=(',',':'))])
    path=AUDIT/'CODEX_SKILL_FEAT_SOURCE_PREPARED.txt';write(path,packet)
    status={'status':'prepared-not-sent; no rule changes or operational approval','packetFile':path.name,'characters':len(packet),'sha256':sha(path),'counts':counts,'checks':len(checks),'protectedFiles':len(protected),'featsApproved':0}
    dump(AUDIT/'SKILL_FEAT_SOURCE_STATUS.json',status)
    supplement={'status':'prepared-not-sent; append tofuture Combat conference','reason':'Anatomy Lore is an explicit Precision Strike dependency; Core Rolls already governs broadest critical range andcheck families. Preserve original Combat packet andattach this supplement.','fullAnatomyLoreSource':by['anatomy_lore'],'skillCase':next(z for z in rows if z['featId']=='anatomy_lore'),'coreRolls':next(z for z in boundaries if z['heading']=='Rolls'),'sourceSha256':sha(p),'newRules':False}
    dump(AUDIT/'COMBAT_FEAT_SKILL_DEPENDENCY_SUPPLEMENT.json',supplement)
    print(json.dumps(status,ensure_ascii=True))
if __name__=='__main__':main()

