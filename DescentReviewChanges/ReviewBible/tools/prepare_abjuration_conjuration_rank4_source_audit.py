"""Preserve16 rank-four Abjuration/Conjuration identities; no spell approval.

Banishment is an unchanged post-push receipt. Questions about existing alignment,
faction or teleportation mechanics do not authorize new cosmology or doctrine.
"""
from copy import deepcopy
import json
from prepare_low_illusion_spell_source_audit import ROOT,GAME,AUDIT,current_book_rows,digest
from prepare_low_necromancy_spell_source_audit import sha,dump
from prepare_combat_feat_source_audit import section

QUESTIONS={
 'banishment':'POST-PUSH RECEIPT ONLY. Preserve the source promise of temporary transport to another plane, Core Action/60ft/Instantaneous and all access records without inventing a destination, planar relation, return procedure or new cosmic origin. Carry this unchanged source to the owner-directed careful cosmology review after the successful authorized GitHub push and verified remote commit. Exclude it from present mechanical authoring and approval.',
 'greater-warding':'Preserve +2 AC and saves, resistance to spells, Action/60ft and concentration up to1minute. Define recipient/willingness and the exact resistance scope: spell-origin damage, effects or another finite meaning must be decided explicitly. Distinguish flat save modifier from advantage; apply current strongest-stat families and damage ordering with Warding Bond, Shield and Elemental Resistance. It grants no automatic immunity, extra armor formula or absorption/reflection unless expressly authored as NEW. Specify suppress/return/end and multiple-source handling without healing or resource refresh.',
 'spell-shield':'Preserve reflection of spells of3rd level or lower in the catalog and Tier3 or lower in Core, with printed Action/60ft/Instantaneous. Resolve that exact terminology conflict and whether an Action establishes protection, readies a later reflection or has another finite source-compatible operation. Define eligible actual spell events, protected recipient, lifetime, trigger/commit timing, destination/range, attack/save/caster ownership, concentration and effect identity. Reflection must preserve real costs and a finite causal history; no new free cast, arbitrary nonspell-power reflection, area immunity or endless mirror loop. Compare Counterspell and pending Soul Mirror/Spell Mirror without merging their identities.',
 'dimensional-anchor':'Preserve prevention of teleportation and planar travel in a60ft radius, Action/60ft/Instantaneous. Resolve radius versus casting range, actual center/shape and duration/concentration for this prevention. Define origin,destination,path/boundary eligibility, preflight and committed failures, willing/hostile travel, ongoing portals and suppression/ending under existing spell-event ownership. Do not invent a new plane or alter existing topology; only evaluate already established location/transport records. It supplies no physical cage, movement prohibition, resource refund or generic immunity to unrelated displacement by its name.',
 'corruption-barrier':'Preserve a wall that both blocks and damages corrupted creatures, Action/60ft and concentration up to1minute. Supply finite geometry, eligible support/placement, sight/line/cover, damage/type/resolution, trigger cadence and entry/forced-movement cases. Corrupted eligibility must reference current mechanically established corruption records, not donor names, appearance, morality or a new cosmological category. Determine nonmatching creatures, objects, attacks and caster crossing without silently making a universal solid wall or automatic corruption detector. Preserve both printed functions and actual material/creature identity.',
 'resonance-dampening-field':'Preserve all spellcasting in the area costing +2 RP, Action/60ft/Instantaneous. Define finite area/center/lifetime/concentration, qualifying caster position and final-price checkpoint, including cantrips, reactions, rituals, item activations and effects that merely continue. Resolve duplicate fields and interaction with reviewed Resonance Influence without silently dropping the printed surcharge. Apply current affordability-before-payment and actual-cast identity; no partial payments, repeated child-effect charges, retroactive drain/refund or extra cost on noncasting powers inferred from a tag.',
 'faction-sanctuary':'Preserve an area sacred to a faction with benefits for members, Action/60ft/Instantaneous. Author a finite mechanical benefit menu and area/lifetime/concentration, actual faction choice and membership evidence, entry/exit/suppression, overlap and visitors. Distinguish membership from reputation and from opposing alignment; compare Faction Ward, Faction Seal and Greater Faction Emblem. The word sacred supplies no new deity, ownership, legal immunity, cosmology or automatic change in allegiance/reputation. Retain any unresolved faction identity/membership facts as explicit dependencies rather than fabricating a roster.',
 'alignment-lock':'Preserve preventing a target from changing alignment for24hours, Action/60ft. Resolve target/save/willingness, scope of prevented transitions, existing masks versus true underlying records, suppression and ending. Use current alignment record distinctions and reviewed Alignment Suggestion/Revelation/Sanctuary. No new axis, moral doctrine, cosmic influence or prediction of player choices is requested. Preventing a state change does not itself grant behavioral compulsion, reveal alignment or erase an existing effect; specify the actual rule at each attempted transition without refund/reset.',
 'alignment-anchor':'Preserve both placements: Abjuration rank7/17RP/120ft/seven days fixes one creature alignment and prevents acting against it; Conjuration rank4/7RP/60ft/Instantaneous creates a zone preventing alignment change. Decide identity and placement-specific procedures explicitly; never grant Cleric the global minimum rank/cost or silently merge the two promises. Define target/zone/save/willingness, finite duration for the zone, actual recorded alignment, masks versus underlying changes, and handling of the rank7 behavior clause under current compulsion rules. Preserve player agency boundaries without deleting the printed clause. This is a mechanical source question, not a new moral axis, cosmological force or theology review.',
 'summon-water-pet':'Preserve HP35, AC14 and a choice of healing an ally for2d6 or attacking for1d10 cold, Action/60ft and concentration up to1minute. Supply finite body/size/speed/senses/saves, attack modifier/reach and healing range/target requirements, placement, initiative/commands and the shared offensive-action budget. Resolve whether heal and attack are mutually exclusive uses of its ordinary action and healing of Downed targets using current procedures. Preserve one body, damage/custody history, ending/return placement and no-resource remains. No aquatic adaptation, free water, unlimited independent actions or cosmetic elemental name expands its profile without explicit NEW authoring.',
 'crystalline-barrier':'Preserve a wall of elemental glass with AC18, HP40 and blocked line of sight, Core Action/range Sight/concentration up to1minute. Define finite dimensions/sections, orientation/support, sight to the casting location, occupancy/escape, line of effect/cover, passage, structural damage and section loss. Resolve whether HP40 applies to one whole wall or sections explicitly; do not silently multiply the pool. Appearance as glass does not erase printed sight blocking. No unbounded length, indestructible force-wall traits, duplicated cargo, permanent raw materials or unsupported building support follows from the name.',
 'elemental-drain':'Preserve the exact conflict: catalog target loses2 RP, Core target loses5 RP; both retain3d6 damage of a random element, Action/60ft/Instantaneous. Resolve the drain amount explicitly without rewriting either original. Define attack/save and branch ordering, finite random-element table and one committed draw, current RP floor/target eligibility, damage resolution, suppression and repeat casting. Losing RP does not say the caster gains it. Do not silently create a transfer, draw extra elements on rerolls, let prevention of one component erase the other, or import familiar external-game damage types.',
 'bind-element':'Preserve one elemental creature, WIS save or Paralyzed for2rounds, Action/60ft/Instantaneous. Bind elemental eligibility to an actual established creature-type/profile record, not any elemental-tagged spell or ingredient. Specify initial success/failure, source-clock endpoints, any repeat saves, parent lifetime/concentration and interaction with the current hard-denial cap and Paralyzed condition. Keep the two-round source clause visible while resolving any cap conflict explicitly; no silent replacement with Restrained, Stunned or arbitrary immunity. Physical position, support and actual custody remain separately governed.',
 'dimensional-door':'Preserve teleporting up to500ft to a known location, Core Action/range500ft/Instantaneous. Define who travels, what knowledge establishes the destination, legal space/support, source/destination geometry, actual gear/cargo and willingness/contested cases. Distinguish this Conjuration identity from the separate Universal Dimension Door record. Actual clocks, falling, custody, existing transport-prevention effects and spent resources survive the transit. No bonus passenger, off-map knowledge, interplanar destination or missing-item recreation is inferred from a familiar external spell.',
 'resonance-beacon':'Preserve a created point that allies can teleport to using RP, Action/60ft/Instantaneous. Define the actual point/body, finite lifetime/concentration, destination capacity, eligible allies, access/range, trigger action, participant RP cost and one transfer transaction. Distinguish initial7RP casting cost from any explicit later traveler payment. Decide anchoring/movement, occupancy, obstruction, hostile custody, suppression/destruction/ending and whether multiple travelers can use it, without free repeated movement, duplicate payment, child-triggered refill or invented planar connections. Compare existing Resonance Conduit/Well and Faction Portal, not an automatic stronger copy.',
 'faction-ally':'Preserve summoning one CR3 creature aligned with the caster faction, Action/60ft/concentration up to1minute. Define an actual finite eligible source roster or explicit missing-profile dependency, faction evidence, body, initiative/commands/offense budget, summon count/replacement and ending. CR3 alone is not a complete combat profile and must not authorize arbitrary unpublished traits, copied Director secrets or a free adaptable stat block. Faction alignment is not automatically moral alignment. Preserve actual cargo and no-resource summon history, and do not grant faction knowledge, legal access or reputation through the temporary body.'
}
COUNTERPARTS=['arcane-ward','warding-gesture','nullify-element','shield','warding-bond','elemental-resistance',
 'alignment-shield','corruption-ward','faction-seal','faction-ward','alignment-sanctuary','resonance-lock',
 'resonance-anchor','dispel-magic','counterspell','summon-fire-pet','summon-air-pet','summon-earth-pet',
 'resonance-bridge','elemental-displacement','mist-step','faction-portal','resonance-conduit','resonance-well',
 'faction-emblem-greater','resonance-influence','alignment-suggestion','sense-alignment','alignment-revelation']
PENDING=['soul-mirror','spell-mirror','arcane-portal','dimension-door','mystic-gate','unravel-spell']


def main():
    inherited=json.loads((AUDIT/'LOW_ILLUSION_SPELL_SOURCE_PREPARATION.json').read_text(encoding='utf-8'))
    protected=deepcopy(inherited['protectedFiles']);assert all(sha(GAME/p)==h for p,h in protected.items())
    def read(path):
        protected[path.relative_to(GAME).as_posix()]=sha(path)
        return json.loads(path.read_text(encoding='utf-8-sig'))
    catalog=read(ROOT/'data/public/spell_playtests/catalog.json');rows=catalog['spells'];by={r['id']:r for r in rows}
    selected=[r for r in rows if r['operational'] is None and set(r['schools']).intersection({'Abjuration','Conjuration'}) and min(v['rank'] for v in r['classAccess'].values())==4]
    assert len(selected)==16 and {r['id'] for r in selected}==set(QUESTIONS)
    source=read(ROOT/'data/playtest/spell_sources/catalog.json')
    core=read(ROOT/'data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json')
    book=current_book_rows();bindings=[];differences=[]
    for row in selected:
        assert row['source']['original']==source[row['id']]
        for e in row['source']['coreEntries']+row['source']['possibleHistoricalAliases']:
            assert e['original']==core['spells'][e['index']]
        for placement in row['source']['original']['placements']:
            matches=[b for b in book if b['name']==row['name'] and b['school']==placement['school'] and b['level']==placement['level']]
            assert len(matches)==1,(row['id'],placement)
            bindings.append({'spellId':row['id'],'catalogPlacement':placement,'currentBookRow':matches[0],
                'summaryDifferencePreserved':placement['summary']!=matches[0]['summary']})
            for e in row['source']['coreEntries']:
                original=e['original']
                if placement['school']==original['school'] and placement['level']==original['level'] and placement['summary']!=original['effect']:
                    differences.append({'spellId':row['id'],'catalogSummary':placement['summary'],'coreEffect':original['effect'],'coreIndex':e['index']})
    counterparts=[by[x] for x in COUNTERPARTS+PENDING]
    assert all(by[x]['operational'] is not None for x in COUNTERPARTS)
    assert all(by[x]['operational'] is None for x in PENDING)
    mentions=[r for r in read(ROOT/'data/public/spell_playtests/class_name_mentions_for_review.json') if r.get('spellId') in QUESTIONS and r['spellId']!='banishment']
    manifest=read(ROOT/'data/public/class_playtests/manifest.json');classes={r['class']:r for r in manifest['classes']};class_records=[]
    for m in mentions:
        path=(ROOT/'docs/mechanics'/classes[m['class']]['data']).resolve();d=read(path)
        if m['location']=='engine':record={'engine':d.get('engine',[])}
        else:
            found=[c for c in d['cards'] if c['id']==m['location']];assert len(found)==1;record={'card':found[0]}
        class_records.append({'mention':m,**record,'file':path.relative_to(GAME).as_posix(),
            'scope':'Registered textual comparison only; no automatic spell grant or identity merge.'})
    excerpts=deepcopy(inherited['currentGoverningExcerpts'])
    extra={'CREATURE_LIFECYCLE_PLAYTEST.md':None,'HEALING_DEATH_PLAYTEST.md':None,'HEALING_PULSE_PLAYTEST.md':None,
        'DAMAGE_SHARING_PLAYTEST.md':None,'STRAIN_PLAYTEST.md':None,'ENCHANTMENT_CONTROL_INTEGRATION_PLAYTEST.md':None,
        'CONDITIONS_PLAYTEST.md':['Paralyzed'],'CONTROL_STATES_PLAYTEST.md':['Root, physical restraints and suppression'],
        'CRAFTING_HARVEST_PLAYTEST.md':['Material identity, consumption and substitution']}
    for name,heads in extra.items():
        path=ROOT/'docs/mechanics'/name;text=path.read_text(encoding='utf-8');protected[path.relative_to(GAME).as_posix()]=sha(path)
        for heading in heads or [None]:
            excerpts.append({'file':path.relative_to(GAME).as_posix(),'sha256':sha(path),'heading':heading or 'entire guide',
                'exactText':section(text,heading) if heading else text})
    records=[{'spellId':r['id'],'questionId':f'AC4-{i+1:02}',
        'scope':'post-push receipt only' if r['id']=='banishment' else 'pre-push mechanical source question',
        'fullSourceAndCurrentAccessRecord':r,'recordSha256':digest(r),'individualQuestion':QUESTIONS[r['id']]} for i,r in enumerate(selected)]
    previous=[]
    for filename in ['LOW_ILLUSION_SPELL_SOURCE_PREPARATION.json','LOW_UNIVERSAL_SPELL_SOURCE_PREPARATION.json',
            'LOW_TRANSMUTATION_SPELL_SOURCE_PREPARATION.json','LOW_NECROMANCY_SPELL_SOURCE_PREPARATION.json',
            'EVOCATION_RANK3_SOURCE_PREPARATION.json','REMAINING_RANK3_SPELL_SOURCE_PREPARATION.json']:
        d=read(AUDIT/filename);previous.extend(r['spellId'] for r in d['selectedSpells'])
    checks=[
        ('16 exact minimum-rank4 Abjuration/Conjuration identities',len(records)==16),
        ('Every full original catalog and Core object retained exactly',True),
        ('17 exact current-book placements including both Alignment Anchor versions',len(bindings)==17),
        ('Exact Elemental Drain and Spell Shield conflicts preserved',{d['spellId'] for d in differences}=={'elemental-drain','spell-shield'}),
        ('Alignment Anchor keeps rank7 Cleric and rank4 Druid access',by['alignment-anchor']['classAccess']['Cleric']['rank']==7 and by['alignment-anchor']['classAccess']['Cleric']['baseRpCost']==17 and by['alignment-anchor']['classAccess']['Druid']['rank']==4 and by['alignment-anchor']['classAccess']['Druid']['baseRpCost']==7),
        ('15 mechanical questions and one deferred Banishment receipt',sum(r['scope']=='pre-push mechanical source question' for r in records)==15 and [r['spellId'] for r in records if r['scope']=='post-push receipt only']==['banishment']),
        ('29 complete reviewed and six pending counterparts preserved',len(counterparts)==len(set(COUNTERPARTS+PENDING))==35),
        ('Every actual nondeferred class-name mention has its full source',len(class_records)==len(mentions)),
        ('No duplication with the137 already prepared pending identities',len(previous)==len(set(previous))==137 and not set(previous).intersection(QUESTIONS)),
        ('Ordinary catalog stays276 operational and572 pending',len(rows)==848 and sum(r['operational'] is not None for r in rows)==276 and sum(r['operational'] is None for r in rows)==572),
        ('Every exact excerpt and protected source remains unchanged',all(e['exactText'] in (GAME/e['file']).read_text(encoding='utf-8') for e in excerpts) and all(sha(GAME/p)==h for p,h in protected.items()))]
    assert all(ok for _,ok in checks),[n for n,ok in checks if not ok]
    counts={'sourceSpells':848,'operationalSpells':276,'remaining':572,'selectedAbjurationConjurationRank4':16,
        'prePushMechanicalQuestions':15,'postPushReceiptOnly':1,'exactCoreEntries':sum(len(r['source']['coreEntries']) for r in selected),
        'currentBookBindings':len(bindings),'reviewedCounterparts':29,'pendingCounterparts':6,'classComparisonRecords':len(class_records),
        'governingExcerpts':len(excerpts),'catalogCoreEffectDifferences':len(differences),'focusedPendingSourceIdentitiesIncludingThisCohort':153,
        'prePushPreparedSpellQuestionsIncludingThisCohort':151,'postPushReceiptsIncludingThisCohort':2}
    data={'status':'prepared-not-sent;15 mechanical questions and one deferred Banishment receipt',
        'commonOperationalQuestion':inherited['commonOperationalQuestion'],
        'commonQuestionException':'Banishment is receipt-only until post-push cosmology. Other questions concern existing mechanical records only; no new plane, moral axis, theology, faction roster or cosmic origin is authorized.',
        'selectedSpells':records,'currentBookBindings':bindings,'completeCounterparts':counterparts,
        'classComparisonRecords':class_records,'catalogCoreEffectDifferences':differences,'currentGoverningExcerpts':excerpts,
        'currentRankCosts':catalog['costByRank'],'currentClassProgression':catalog['classProgression'],
        'counts':counts,'checks':[{'name':n,'pass':ok} for n,ok in checks],'protectedFiles':protected,
        'spellsApproved':0,'sourceInformationDeleted':0,'cosmology':'post-push only; Banishment is unchanged receipt only',
        'futureDispatch':'After the active Fishing exact review, rebase relevant dependencies and submit source questions before authoring. This packet is unsent and cannot confer operational approval.'}
    prefix='ABJURATION_CONJURATION_RANK4';dump(AUDIT/f'{prefix}_SOURCE_PREPARATION.json',data)
    lines=['# Rank-four Abjuration and Conjuration source audit','',data['status'],'',
        'Sixteen ordinary identities are preserved. Fifteen have mechanical source questions; Banishment is only an unchanged receipt for the owner-directed post-push cosmology review. No spell is newly selectable or approved.','',
        'Elemental Drain retains the catalog two-RP loss and Core five-RP loss. Spell Shield retains its level-versus-Tier conflict. Alignment Anchor keeps both rank-seven Abjuration and rank-four Conjuration placements and each class\'s actual access/cost.','',
        '| Case | Spell | Scope and question |','|---|---|---|']
    lines += [f"| {r['questionId']} | {r['fullSourceAndCurrentAccessRecord']['name']} | {r['scope']}: {r['individualQuestion']} |" for r in records]
    lines += ['','The seven prepared cohorts now preserve153 distinct pending identities and158 current-book bindings:151 mechanical questions and two post-push-only receipts (Blink and Banishment). Ordinary totals remain276 operational and572 pending. Fishing exact review remains the active notebook request.','']
    report='\n'.join(lines);(AUDIT/f'{prefix}_SOURCE_AUDIT.md').write_text(report,encoding='utf-8',newline='\n')
    packet='PREPARED RANK-FOUR ABJURATION/CONJURATION SOURCE CONFERENCE — NOT SENT.\n\n'+report+'\nCOMPLETE SOURCE AND CURRENT DEPENDENCY EVIDENCE\n'+json.dumps(data,ensure_ascii=False,separators=(',',':'))
    path=AUDIT/f'CODEX_{prefix}_SOURCE_PREPARED.txt';path.write_text(packet,encoding='utf-8',newline='\n')
    status={'status':data['status'],'packetFile':path.name,'characters':len(packet),'packetSha256':sha(path),
        'counts':counts,'checkCount':len(checks),'protectedFilesUnchanged':len(protected),'spellsApproved':0,
        'sourceInformationDeleted':0,'cosmology':data['cosmology']}
    dump(AUDIT/f'{prefix}_SOURCE_STATUS.json',status);print(json.dumps(status))


if __name__=='__main__':main()
