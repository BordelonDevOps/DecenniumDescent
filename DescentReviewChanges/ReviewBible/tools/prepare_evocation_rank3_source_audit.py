"""Preserve the eight unfinished rank-three Evocation sources and decisions needed."""
from copy import deepcopy
import json
from prepare_low_illusion_spell_source_audit import ROOT, GAME, AUDIT, current_book_rows, digest
from prepare_low_necromancy_spell_source_audit import sha, dump
from prepare_combat_feat_source_audit import section

QUESTIONS = {
 'flame-geyser': 'Preserve5x5 vertical area,5d6 fire,upward launch and Core60ft/concentration up to1minute. Define actual horizontal dimensions,height,placement,support and whether damage is initial only or a finite recurring hazard; concentration alone supplies no tick schedule. Set save/outcomes,launch height/timing,ceiling collision,landing and existing falling markers. Distinguish forced movement from flight and forbid extra entry/reentry ticks unless explicitly authorized. Core Ward tag grants no defensive benefit.',
 'chain-lightning-jr': 'Preserve three distinct targets and4d6 lightning each. Decide whether exactly three are required or up to three,initial range and later chain distances,source versus prior-recipient line of effect,snapshot selection,attack/save and shared versus individual rolls. Define lost illegal allocations and ordered damage without retargeting after outcomes. No repeat hit on one identity,conductive environmental chaining or free fourth target.',
 'shardstorm': 'Preserve a cone and5d4 piercing plus5 cold. Resolve whether Core60ft is cone length or casting-point range,with explicit origin/width/three-dimensional geometry. Give save outcomes and one mixed-type event per recipient,shared roll,defenses and rounding. Decide eligible objects under existing scoped patterns; no free ice/shards,additional slow/Frozen,terrain or persistent zone.',
 'arc-flash': 'Preserve enemies in20ft radius,3d6 lightning and blindness. Resolve Core20ft casting range versus radius/origin and snapshot enemy eligibility. Define damage save and blindness save/duration/ending separately,sight and alternate-sense interactions,and damage versus condition immunity. No permanent blindness,automatic ally harm/exemption outside the selected source scope,conductive chaining or second damage wave through newly destroyed cover.',
 'fireball': 'Preserve8d6 fire and20ft radius,with Core range20ft explicitly separate. Decide actual casting-point range and geometry without silently importing a longer familiar-game range. Define save/full-or-half,shared roll,cover/obstructions,creature/object snapshot and any source-authorized ignition. Existing fire damage does not automatically establish Burning or a continuing zone. Source changes,including any range repair,must be labeled NEW and preserve the printed original.',
 'lightning-bolt': 'Preserve8d6 lightning in100ft line. Define finite width,height,origin and direction,save/full-or-half,shared roll,cover/obstructions and actual creature/object eligibility. Apply per-recipient defenses once and preserve source time ordering. No unstated rebound,forking,metal/water damage multiplier,door-penetrating second wave or permanent electrical resource.',
 'minute-meteors': 'Preserve exactly six meteors,each2d6 fire in5ft radius. Resolve Core5ft range and Instantaneous versus simultaneous casting or a finite stored firing sequence. If stored,define duration/concentration,release action/count/range,commitment,remaining-use ledger and expiry/suppression; if simultaneous,define six centers/allocations and ordered independent explosions explicitly. Decide overlaps,recipient snapshots and interruption without importing an external spell or quietly reducing six to one.',
 'tidal-wave': 'Preserve3d8 bludgeoning,knocking Prone and extinguishing flames. Define finite area geometry distinct from Core60ft range,save/outcome for damage and Prone,eligible targets/objects and precise order. Bind extinguishing to present ordinary/special fire records under reviewed cure rules,including suppressed records. Decide whether transient water remains,with explicit finite volume/quality if so; no implicit drinking supply,flood,creature transport or infinite harvested material.'
}

def main():
    inherited=json.loads((AUDIT/'LOW_ILLUSION_SPELL_SOURCE_PREPARATION.json').read_text(encoding='utf-8'))
    protected=deepcopy(inherited['protectedFiles']);assert all(sha(GAME/p)==h for p,h in protected.items())
    def read(path):
        protected[path.relative_to(GAME).as_posix()]=sha(path)
        return json.loads(path.read_text(encoding='utf-8-sig'))
    catalog=read(ROOT/'data/public/spell_playtests/catalog.json');rows=catalog['spells'];by_id={r['id']:r for r in rows}
    selected=[r for r in rows if r['operational'] is None and r['schools'][0]=='Evocation' and min(v['rank'] for v in r['classAccess'].values())==3]
    assert len(selected)==8 and {r['id'] for r in selected}==set(QUESTIONS)
    original=read(ROOT/'data/playtest/spell_sources/catalog.json');core=read(ROOT/'data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json');book=current_book_rows();bindings=[]
    for row in selected:
        assert row['source']['original']==original[row['id']]
        for entry in row['source']['coreEntries']+row['source']['possibleHistoricalAliases']:assert entry['original']==core['spells'][entry['index']]
        for placement in row['source']['original']['placements']:
            matches=[b for b in book if b['name']==row['name'] and b['school']==placement['school'] and b['level']==placement['level']];assert len(matches)==1
            bindings.append({'spellId':row['id'],'catalogPlacement':placement,'currentBookRow':matches[0],'summaryDifferencePreserved':placement['summary']!=matches[0]['summary']})
    counterpart_ids=['chain-jolt','burning-hands','earth-tremor','ice-knife','thunderwave','scorching-raystorm','lightning-pulse','frost-nova','arcane-implosion','scorching-line','shatter','snowball-swarm','acid-arrow','feather-fall']
    counterparts=[by_id[id] for id in counterpart_ids];assert all(r['operational'] is not None for r in counterparts)
    mentions=[r for r in read(ROOT/'data/public/spell_playtests/class_name_mentions_for_review.json') if r.get('spellId') in QUESTIONS]
    manifest=read(ROOT/'data/public/class_playtests/manifest.json');classes={r['class']:r for r in manifest['classes']};class_records=[]
    for mention in mentions:
        path=(ROOT/'docs/mechanics'/classes[mention['class']]['data']).resolve();data=read(path)
        if mention['location']=='engine':record={'engine':data.get('engine',[])}
        else:
            matches=[c for c in data['cards'] if c['id']==mention['location']];assert len(matches)==1;record={'card':matches[0]}
        class_records.append({'mention':mention,**record,'file':path.relative_to(GAME).as_posix(),'scope':'Registered textual comparison only; not a grant or identity merge.'})
    keep={'SPELL_INTEGRATION_RULES.md','CORE_RESOLUTION_PLAYTEST.md','COMBAT_ACTION_PLAYTEST.md','CHARACTER_CREATION_PLAYTEST.md'}
    control={'Records, clocks and precedence','Compulsion, action denial and initiative'}
    conditions={'Shared handling','Blinded','Prone','Incapacitated'}
    excerpts=[deepcopy(e) for e in inherited['currentGoverningExcerpts'] if e['file'].split('/')[-1] in keep or (e['file'].endswith('CONTROL_STATES_PLAYTEST.md') and e['heading'] in control) or (e['file'].endswith('CONDITIONS_PLAYTEST.md') and e['heading'] in conditions)]
    extra={'HEALING_DEATH_PLAYTEST.md':['Damage quantities and resolution','Removing suppressed Bleed and fire'],'CONDITIONS_PLAYTEST.md':['Burning'],'DAMAGE_SHARING_PLAYTEST.md':['Hit identity and final damage accounting'],'EQUIPMENT_ACQUISITION_PLAYTEST.md':['Object damage and Sunder'],'CRAFTING_HARVEST_PLAYTEST.md':['Material identity, consumption and substitution']}
    for name,headings in extra.items():
        path=ROOT/'docs/mechanics'/name;text=path.read_text(encoding='utf-8');protected[path.relative_to(GAME).as_posix()]=sha(path)
        for heading in headings:excerpts.append({'file':path.relative_to(GAME).as_posix(),'sha256':sha(path),'heading':heading,'exactText':section(text,heading)})
    verdict_path=AUDIT/'GPT_EVOCATION_RANK2_EXACT_AND_DELIVERY_REVIEW.md';protected[verdict_path.relative_to(GAME).as_posix()]=sha(verdict_path)
    verdict=verdict_path.read_text(encoding='utf-8')
    records=[{'spellId':r['id'],'questionId':f'EV3-{i+1:02}','fullSourceAndCurrentAccessRecord':r,'recordSha256':digest(r),'individualQuestion':QUESTIONS[r['id']]} for i,r in enumerate(selected)]
    checks=[('Eight exact pending primary-Evocation rank-three identities',len(records)==8),('All catalog/Core original records retained exactly',True),('Eight exact current-book bindings',len(bindings)==8),('All sources have individual full-clause questions',all(len(r['individualQuestion'])>240 for r in records)),('Fourteen operational counterparts remain separate',len(counterparts)==14),('Every registered class mention has its actual source',len(class_records)==len(mentions)),('276 operational and572 unfinished identities unchanged',sum(r['operational'] is not None for r in rows)==276 and sum(r['operational'] is None for r in rows)==572),('Current exact source excerpts verified',all(e['exactText'] in (GAME/e['file']).read_text(encoding='utf-8') for e in excerpts)),('All protected inputs unchanged',all(sha(GAME/p)==h for p,h in protected.items()))]
    assert all(ok for _,ok in checks),[name for name,ok in checks if not ok]
    counts={'selectedEvocationRank3':8,'sourceSpells':848,'operationalSpells':276,'remaining':572,'currentBookBindings':8,'exactCoreEntries':sum(len(r['source']['coreEntries']) for r in selected),'reviewedCounterparts':14,'classComparisonRecords':len(class_records),'governingExcerpts':len(excerpts),'currentBookSummaryDifferences':sum(b['summaryDifferencePreserved'] for b in bindings)}
    data={'status':'prepared-not-sent; source questions only','commonOperationalQuestion':inherited['commonOperationalQuestion'],'selectedSpells':records,'currentBookBindings':bindings,'completeCounterparts':counterparts,'classComparisonRecords':class_records,'currentGoverningExcerpts':excerpts,'precedingEvocationExactVerdict':{'file':verdict_path.relative_to(GAME).as_posix(),'sha256':sha(verdict_path),'exactText':verdict},'currentRankCosts':catalog['costByRank'],'currentClassProgression':catalog['classProgression'],'counts':counts,'checks':[{'name':name,'pass':ok} for name,ok in checks],'protectedFiles':protected,'spellsApproved':0,'sourceInformationDeleted':0,'cosmology':'post-push only','futureDispatch':'After active Fishing review; rebase dependencies. Source decisions precede exact authored manuscript review. Do not import external-game spell versions.'}
    dump(AUDIT/'EVOCATION_RANK3_SOURCE_PREPARATION.json',data)
    lines=['# Rank-three Evocation source audit','',data['status'],'',data['commonOperationalQuestion'],'','Eight full source identities are preserved with eight current-book bindings and eight exact Core records. Fourteen operational comparison spells and the preceding rank-two exact verdict supply reusable procedure boundaries. Source ranges and area dimensions are retained independently, including Fireball20ft and Minute Meteors5ft; no imported range or firing sequence is assumed.','', '| Case | Spell | Decision needed |','|---|---|---|']
    lines += [f"| {r['questionId']} | {r['fullSourceAndCurrentAccessRecord']['name']} | {r['individualQuestion']} |" for r in records]
    lines += ['','All eight remain unfinished. The Fishing source conference remains the active GPT request; these questions are unsent. No sources changed or deleted, no spells promoted, and no cosmology reviewed.','']
    report='\n'.join(lines);(AUDIT/'EVOCATION_RANK3_SOURCE_AUDIT.md').write_text(report,encoding='utf-8')
    packet='PREPARED RANK-THREE EVOCATION SOURCE CONFERENCE — NOT SENT.\n\n'+report+'\nCOMPLETE SOURCE AND CURRENT DEPENDENCY EVIDENCE\n'+json.dumps(data,ensure_ascii=False,separators=(',',':'))
    path=AUDIT/'CODEX_EVOCATION_RANK3_SOURCE_PREPARED.txt';path.write_text(packet,encoding='utf-8',newline='\n')
    status={'status':'prepared-not-sent','packetFile':path.name,'characters':len(packet),'packetSha256':sha(path),'counts':counts,'checkCount':len(checks),'protectedFilesUnchanged':len(protected),'spellsApproved':0,'sourceInformationDeleted':0,'cosmology':'post-push only'};dump(AUDIT/'EVOCATION_RANK3_SOURCE_STATUS.json',status);print(json.dumps(status))

if __name__=='__main__':main()
