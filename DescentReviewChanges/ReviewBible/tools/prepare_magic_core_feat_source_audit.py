"""Preserve 31 Magic source feats and explicit casting-dependency questions."""
from pathlib import Path
import json,re,hashlib
from prepare_combat_feat_source_audit import section
ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1];AUDIT=GAME/'docs/audit/2026-10-08/full-game'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(d):return hashlib.sha256(json.dumps(d,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def write(p,t):p.write_text(t,encoding='utf-8',newline='\n')
def dump(p,d):write(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
QUESTIONS={
 'arcaneResonance':'Define ranked-spell recovery against the actual shared RP engine: recoverable amount, paid-cost ceiling, timing, natural20 attack eligibility, attack type, frequency and rest/event ledger. Preserve the level3 gate and avoid unlimited RP from harmless attacks, cantrips, extra attacks or repeated/copied results. No spell-slot system is inferred.',
 'astral_projection':'Resolve Wisdom17 and character-level15 versus the ordinary rank9/class-level17 route; define only the feat grant, casting ability/DC, charge and Long Rest recovery, components and interruption/payment. The named ordinary spell remains blocked. Do not develop planes, destinations, souls, projection ontology or deferred cosmology to complete this feat; retain that dependency explicitly.',
 'battleMage':'Bind spellcasting and martial-weapon prerequisites to actual grants, then specify somatic hand permissions while holding weapons/shields. Keep verbal components, priced/consumed materials, focus eligibility, nonproficient-armor costs and genuine hand availability separate. Do not import unprinted War Caster reaction-spell benefits.',
 'cantrip_mastery':'Define the single permanent cantrip choice, replacement rules, natural20 attack versus target-natural1 save, critical dice before maximization, multiple targets/packets, delayed/repeated damage and added rider dice. Ordinary saves have no generic natural1 failure: resolve this feat trigger separately from success and damage entitlement.',
 'dispel_mastery':'Use the actual Dispel Magic operational card; define selecting one additional effect, same/different carrier, range/visibility, each effect eligibility and separate checks, rank thresholds and interruption. The feat does not automatically dispel a second item, creature, spell or innate magic merely by calling it an effect.',
 'divine_favor':'Resolve Charisma15 and existing worship credential without inventing a deity or doctrine. Define eligible save/ability check, declaration window, opposed ties, degrees and critical outcomes, information available, action/cadence and Long Rest ledger. Automatic success grants no new roll, physical possibility or permission to alter cosmology.',
 'elementalAdept':'Give a finite eligible damage-type choice and its acquisition/replacement rule. Define resistance bypass without immunity bypass, damage1-to2 ordering with critical/maximized/rerolled dice, multiple packets and nonspell riders; preserve real spellcasting prerequisite and no new damage entitlement.',
 'elemental_affinity':'Resolve level5, finite elemental choice, which actual damage sources qualify, the exact10-percent arithmetic/rounding stage and stacking with resistance, criticals, extra dice, multi-hit/area/ongoing effects. Current percentage text is active source, not a discarded legacy clause.',
 'elemental_mastery':'Resolve the3rd-level-spell prerequisite by actual casting route/rank. Define element choice, declaration, partial/mixed damage conversion and whether nondamage riders, school, creature exclusions and condition types stay unchanged. No generic upcasting, free cast or environmental transformation.',
 'enchantment_focus':'Bind actual Enchantment school and current repertoire, initial and repeated saving throws, spells with multiple schools/placements and copied or item casts. Define ordinary advantage cancellation and source-specific control protections; do not extend disadvantage to opposed ability checks or all social influence.',
 'evocation_focus':'Define+1 per actual eligible damage die, school/placement, critical bonus dice, maximized/nonrolled dice, rerolls, shared area rolls, delayed/ongoing packets and added nonspell riders. Flat damage and repeated references to one rolled result must not manufacture extra dice.',
 'familiar_bond':'Use the full Find Familiar card and actual companion command/stat rules. Define maximum versus current HP change, level scaling/damage deficit, one physical familiar identity, eligible attack profile, action/command cost and casting ability. Spell attack bonus supplies no missing attack damage, reach, weapon, extra turn or resurrection.',
 'feyTouched':'Preserve both spell grants and separate once-per-Long-Rest casts. Misty Step exists only as an ancestry-grant supplemental card, not an ordinary-class spell: decide an explicit feat route without silently changing the ordinary catalog. Resolve rank1 school choices, ability/DC, components, charges versus RP/repertoire and all spell-review dependencies. Preserve flavor; no Feywild cosmology review.',
 'greater_spell_focus':'No exact Spell Focus feat occurs among335 source names. Identify a real prerequisite dependency or propose an explicitly NEW bounded completion; do not alias Mystic Focus, spellPenetration or school-focus feats by similar names. Define additional+1 DC scope and stacking without assuming a missing earlier+1.',
 'heighten_spell':'Map expending one-level-higher ranked recovery to actual rank/RP pricing, known spell access and maximum legal rank. Define declaration/payment, duration of+1 DC, multi-save spells and stacking; do not infer general upcasting, extra damage or a spell-slot pool.',
 'metamagicAdept':'Preserve two selected metamagic options and two sorcery points, but neither a point-to-RP exchange nor an imported external option list is authorized. Compare the complete provisional Mage Metaspell Access card; explicitly resolve feat option identities, costs, recovery, timing and combining modes. A matching metamagic tag does not grant class acquisition or convert one-per-rest uses into points.',
 'planar_binding':'Resolve Charisma15 and rank5 casting access, actual feat casting route/ability, once-per-Long-Rest ledger and waived recovery versus components and concentration. The ordinary Planar Binding card remains blocked. Do not invent creature origins, planes, souls or binding ontology; record deferred dependencies separately from the mechanical grant.',
 'ritual_caster':'Define eligible learned/recorded rituals, actual ritual tags, access/preparation/components, Intelligence-or-Wisdom13, base casting time plus10minutes and interruption/concentration. Bind no-recovery wording to RP precisely, preserving typo in source. Quick Ritualist/Ritual Channeler are pending counterparts, not approved multipliers or free formula access.',
 'shadow_touched':'Preserve Invisibility and one rank1 Necromancy/Illusion choice, each once per Long Rest. The ordinary Invisibility card is still blocked. Define casting ability, spell-access route, charge and RP separation, components and replacement rules; preserve Shadowfell flavor without reviewing or extending cosmology.',
 'spell_echo_chamber':'The source only states next spell affects area twice. Define activation, cost, cadence, duration/expiry, qualifying area spell, two areas versus two resolutions, placement/overlap, saves/damage/control/concentration and delayed packets as explicit NEW decisions. Compare pending Echo Spell without adopting its half-effect rule by name.',
 'spellPenetration':'Define an actual spell-resistance predicate from sourced mechanics, including the supplied Shaman Spell Resistance card, versus resistance to damage or save advantage. Preserve+2 to spell attack only, level5 and spellcasting; resolve target qualification and stacking without inventing a resistance stat or granting bypass.',
 'spell_sniper':'Define actual ranged-spell-attack qualification, double printed range versus radius, Self/Touch/unlimited ranges, maintained-control distances and source placement differences. No unprinted cover ignoring, critical expansion or extra cantrip grant. Cast and attack must remain legally possible.',
 'telekinetic':'Mage Hand exists as an ordinary blocked spell; preserve learning it and waived V/S while keeping any other components. Define an explicit shove action/target/range/size/ability/DC, push/pull distance, resistance and repeated-use cadence. No invisible hand, free attack or extra command budget inferred from outside rules.',
 'telepathic':'No exact Detect Thoughts definition was found in the848 ordinary plus10 ancestry catalogs. Define telepathy range, willing/aware recipients, senses/languages, directionality and actions; separately resolve once-per-Long-Rest spell grant and actual dependency. Do not invent mind-reading content, a spell profile or creature cognition taxonomy from the feat name.',
 'war_caster':'Preserve its sole printed effect: advantage on Constitution saves maintaining concentration on spells. Bind current concentration/strain procedure, damage-event timing, normal advantage cancellation and nonproficient-armor disadvantage. Do not import somatic exceptions, reaction spells or nonspell concentration benefits.'
}
for cls in ['bard','cleric','druid','sorcerer','warlock','wizard']:
    QUESTIONS['magic_initiate_'+cls]='Preserve two '+cls+'-list cantrips and one rank1 spell, with the ranked spell once per Long Rest. Resolve the actual named list, casting ability/DC, cantrip cadence/scaling, permanent choices, components, charge versus RP use and repertoire/multiclass prerequisites. '+('No Sorcerer/Warlock class exists in the17-class foundation or supplied spell-progression map; do not silently alias this list to Mage/Wizard or import external rules. ' if cls in ('sorcerer','warlock') else 'Use the actual class-specific ranks in the supplied choice pool; source visibility/review status remains separate from eligibility. ')+'Blocked spell cards remain dependencies and this feat grants no class-level advancement.'
RELATED=['arcaneFocus','arcane_recall','blood_magic','echo_spell','efficient_caster','flash_cast','quick_ritualist','ritual_channeler','spell_reservoir','twin_cast','mystic_focus']
NAMES=['Astral Projection','Dispel Magic','Find Familiar','Misty Step','Planar Binding','Invisibility','Mage Hand','Detect Thoughts']
CONTEXT={
 'CORE_RESOLUTION_PLAYTEST.md':['Which rule applies','Rolls','Resolve a damage event'],
 'CHARACTER_CREATION_PLAYTEST.md':['Abilities and training','Gain a level','Multiclass entry and class features','One shared RP pool','Shared strain, recovery and concentration'],
 'CLASS_PLAYTEST_RULES.md':['Ordinary spells: one explicit test configuration','Spell repertoires and acquisition'],
 'SPELL_INTEGRATION_RULES.md':['What owns each decision','Select a spell','Resolve a cast at the table','Counterspell checks and interruption','Components, summons and ongoing effects','Reviewed ancestry spell access'],
 'EQUIPMENT_ACQUISITION_PLAYTEST.md':['Armor and shields','Hands and focuses'],
 'ANCESTRY_BACKGROUND_PLAYTEST.md':['Recharge, recovery and action clocks','Ancestry spellcasting'],
 'CREATURE_LIFECYCLE_PLAYTEST.md':['At the table','Different kinds of creature life','Stats and ownership'],
 'COMBAT_ACTION_PLAYTEST.md':['Encounter and action resources','Time and event ordering — NEW']}

def main():
    protected={}
    def read(p):
        protected[p.relative_to(GAME).as_posix()]=sha(p)
        return json.loads(p.read_text(encoding='utf-8-sig'))
    p=ROOT/'src/data/feats.js';source_text=p.read_text(encoding='utf-8-sig');protected[p.relative_to(GAME).as_posix()]=sha(p)
    raw=json.JSONDecoder().raw_decode(source_text.split('export const feats = ',1)[1])[0];by={f['id']:f for f in raw}
    reviewed=set(read(ROOT/'data/public/feat_playtests/manifest.json')['operationalIds'])
    routed={z['featId'] for n in ['CRAFTING_FEAT_INTERFACE_PREPARATION.json','COMBAT_FEAT_SOURCE_PREPARATION.json','SKILL_FEAT_SOURCE_PREPARATION.json'] for z in read(AUDIT/n)['selectedFeats']}
    pending=read(AUDIT/'REMAINING_FEAT_CATALOG_PREPARATION.json')
    selected=[f for f in raw if f['type']=='Magic' and 'status' not in f and f['id'] not in reviewed|routed]
    assert len(selected)==31 and {f['id'] for f in selected}==set(QUESTIONS)
    rows=[{'featId':f['id'],'questionId':f'MF-{i+1:02}','sourceObject':f,'sourceObjectSha256':digest(f),'fullClauseQuestion':QUESTIONS[f['id']],'currentOperationalStatus':'full-feat-review-pending'} for i,f in enumerate(selected)]
    sources=read(ROOT/'data/playtest/spell_sources/catalog.json');public=read(ROOT/'data/public/spell_playtests/catalog.json');spells={s['id']:s for s in public['spells']}
    ancestry=read(ROOT/'data/public/ancestry_playtests/spells.json')['spells']
    dependencies=[]
    for name in NAMES:
        ordinary=[{'id':id,'completeSourceObject':s,'sourceObjectSha256':digest(s),'completeCurrentPublicCard':spells[id]} for id,s in sources.items() if s['name'].casefold()==name.casefold()]
        anc=[s for s in ancestry if s['name'].casefold()==name.casefold()]
        dependencies.append({'requestedName':name,'matchMethod':'exact case-insensitive printed name; no inferred alias','ordinaryMatches':ordinary,'ancestryOnlyMatches':anc,'missingFromTheseTwoCatalogs':not ordinary and not anc,'scope':'source/card evidence only; pending operational status and ancestry-only access preserved'})
    foundation=read(ROOT/'data/playtest/character_foundation.json')
    progression=public['classProgression']
    pools={cls:[{'id':s['id'],'name':s['name'],'schools':s['schools'],'classAccess':s['classAccess'][cls],'currentStatus':s['status']} for s in public['spells'] if cls in s['classAccess'] and s['classAccess'][cls]['rank'] in (0,1)] for cls in ['Bard','Cleric','Druid','Sorcerer','Warlock','Wizard']}
    class_cards=[]
    for cls,id in [('mage','mage.arch.metaspell-access'),('shaman','shaman.hero.bloodcaller.spell-resistance')]:
        d=read(ROOT/f'data/public/class_playtests/{cls}.json')
        class_cards.append({'file':f'data/public/class_playtests/{cls}.json','catalogStatus':d['status'],'completeCard':next(c for c in d['cards'] if c['id']==id)})
    excerpts=[]
    for name,heads in CONTEXT.items():
        p=ROOT/'docs/mechanics'/name;t=p.read_text(encoding='utf-8');protected[p.relative_to(GAME).as_posix()]=sha(p)
        for h in heads:excerpts.append({'file':p.relative_to(GAME).as_posix(),'heading':h,'sha256':sha(p),'exactText':section(t,h),'scope':'current manuscript with its own stated review limits'})
    related=[{'sourceObject':by[id],'sourceObjectSha256':digest(by[id]),'currentOperationalReviewed':id in reviewed,'scope':'counterpart evidence only; full-feat review remains pending'} for id in RELATED]
    checks=[
      ('Both335 feat source registries byte-identical',len(raw)==335 and (ROOT/'src/data/feats.js').read_bytes()==(GAME/'src/data/feats.js').read_bytes()),
      ('All327 pending original source objects retained',[f for f in raw if f['id'] not in reviewed]==[r['sourceObject'] for r in pending['records']]),
      ('Exact31 Magic records without status field selected',len(selected)==31 and all('status' not in z['sourceObject'] for z in rows)),
      ('No overlap with96 prepared or8 reviewed',len(routed)==96 and len(reviewed)==8 and not set(QUESTIONS).intersection(routed|reviewed)),
      ('All31 full source objects hashes and questions exact',all(z['sourceObject']==by[z['featId']] and z['sourceObjectSha256']==digest(z['sourceObject']) and len(z['fullClauseQuestion'])>150 for z in rows)),
      ('Eight exact-name spell lookups with original review states',len(dependencies)==8 and all(m['completeCurrentPublicCard']==spells[m['id']] for z in dependencies for m in z['ordinaryMatches'])),
      ('Misty Step ancestry-only and Detect Thoughts unresolved',next(z for z in dependencies if z['requestedName']=='Misty Step')['ancestryOnlyMatches'] and not next(z for z in dependencies if z['requestedName']=='Misty Step')['ordinaryMatches'] and next(z for z in dependencies if z['requestedName']=='Detect Thoughts')['missingFromTheseTwoCatalogs']),
      ('Spell Focus exact prerequisite absent from335 names',not any(f['name'].casefold()=='spell focus' for f in raw)),
      ('Sorcerer Warlock have no current progression or choice pool',all(n not in progression and not pools[n] for n in ('Sorcerer','Warlock')) and len(foundation['classes'])==17),
      ('Eleven full unapproved counterpart records',len(related)==11 and not any(z['currentOperationalReviewed'] for z in related)),
      ('Two complete provisional class dependency cards',len(class_cards)==2 and all(z['completeCard']['designStatus']=='provisional-playtest' for z in class_cards)),
      ('Every governing excerpt exactly present',all(z['exactText'] in (GAME/z['file']).read_text(encoding='utf-8') for z in excerpts)),
      ('All protected sources and current manuscript files unchanged',all(sha(GAME/q)==h for q,h in protected.items()))]
    assert all(v for _,v in checks),[n for n,v in checks if not v]
    counts={'sourceFeats':335,'operationalReviewed':8,'pending':327,'selectedMagicCore':31,'otherPendingFocusedPreparation':200,'pendingMagicAfterThisCohort':58,'counterpartRecords':11,'namedSpellLookups':8,'ordinaryNamedMatches':sum(len(z['ordinaryMatches']) for z in dependencies),'ancestryOnlyNamedMatches':sum(len(z['ancestryOnlyMatches']) for z in dependencies),'missingNamedSpells':sum(z['missingFromTheseTwoCatalogs'] for z in dependencies),'classCards':2,'currentGuideExcerpts':len(excerpts),'choicePoolCounts':{k:len(v) for k,v in pools.items()}}
    data={'status':'prepared-not-sent; source evidence and questions only','sourceFile':'DescentReviewChanges/ReviewBible/src/data/feats.js','sourceFileSha256':sha(ROOT/'src/data/feats.js'),'selection':'31 pending source-category Magic records lacking a status key; grouping only, no implication about historical approval or priority','selectedFeats':rows,'counterpartSources':related,'namedSpellDependencies':dependencies,'currentClassProgression':progression,'currentRankCosts':public['costByRank'],'currentClassIdentities':[{'class':c['class'],'slug':c['slug']} for c in foundation['classes']],'lowRankClassChoicePools':pools,'classCardDependencies':class_cards,'currentGoverningExcerpts':excerpts,'counts':counts,'checks':[{'name':n,'pass':v} for n,v in checks],'protectedFiles':protected,'featsApproved':0,'newRules':False,'cosmology':'post-push only; preserve flavor and named sources without defining planes, souls, deities or creature origins'}
    dump(AUDIT/'MAGIC_CORE_FEAT_SOURCE_PREPARATION.json',data)
    lines=['# Magic feat source preparation — first31','',data['status'],'','All31 pending Magic records without a source status key are retained completely. That field-based grouping is navigation only; it does not discard existing draft/needsReview/deprecated fields or invalidate historical work. The remaining58 Magic-category feats retain their separate pending route.','',
      'The named-spell lookup finds six exact ordinary identities, one ancestry-only Misty Step and no exact Detect Thoughts in these two catalogs. Astral Projection, Planar Binding, Invisibility and Mage Hand remain blocked in the ordinary operational catalog. Dispel Magic and Find Familiar retain their current operational card status. A feat grant must explicitly establish access; it cannot silently make an ancestry-only spell ordinary or complete an unfinished spell.','',
      'Spell Focus has no exact-name source identity among335 feats. Sorcerer and Warlock have no entries in the actual17-class progression/low-rank choice pools. Eleven complete pending counterpart feats and two provisional class cards preserve relevant alternative wording without approving aliases, sorcery-point conversion or a borrowed metamagic list.','',
      '| Case | Source feat | Prerequisite | Full-clause decision needed |','|---|---|---|---|']
    for z in rows:
        f=z['sourceObject'];lines.append(f"| {z['questionId']} | {f['name']} ({f['id']}) | {f['prerequisite']} | {z['fullClauseQuestion']} |")
    lines+=['','Every named spell source/card and relevant ancestry supplement is supplied in full. Low-rank choice pools carry exact class access and current operational status; a listed choice is not automatically approved. Casting ability, rank, repertoire, RP versus finite charge, components, action, concentration, damage arithmetic, rest recovery and classless access require explicit decisions.','',
      'Prepared only; finish the active Jewelcrafting source conference before another dispatch. Subsequent authoring and exact review remain necessary. Original feat records, spell catalogs and classes are unchanged. No cosmology review, runtime installation, human balance approval or new full-feat approval is claimed.','']
    audit='\n'.join(lines);write(AUDIT/'MAGIC_CORE_FEAT_SOURCE_AUDIT.md',audit)
    packet='\n\n'.join(['PREPARED MAGIC FEAT SOURCE CONFERENCE — NOT SENT.\n31 complete Magic sources,31 full-clause questions,11 full pending counterparts,eight exact spell lookups,two provisional class cards and actual rank/access rules. Give finite numbered authoring decisions only after current dependencies are refreshed and the active Jewelcrafting conference completes. Preserve every source field and distinguish NEW completions. Missing/blocked spell and class definitions remain explicit dependencies. No external D&D rules or cosmology decisions may be silently imported.',audit,'FULL SOURCE AND DEPENDENCY EVIDENCE',json.dumps(data,ensure_ascii=False,separators=(',',':'))])
    p=AUDIT/'CODEX_MAGIC_CORE_FEAT_SOURCE_PREPARED.txt';write(p,packet)
    status={'status':'prepared-not-sent','packetFile':p.name,'characters':len(packet),'packetSha256':sha(p),'counts':counts,'checkCount':len(checks),'protectedFilesUnchanged':len(protected),'featsApproved':0,'sourceInformationDeleted':0,'cosmology':'post-push only'}
    dump(AUDIT/'MAGIC_CORE_FEAT_SOURCE_STATUS.json',status)
    print(json.dumps(status))
if __name__=='__main__':main()
