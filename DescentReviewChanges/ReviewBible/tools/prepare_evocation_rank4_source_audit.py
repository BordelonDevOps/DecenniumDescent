"""Preserve eight rank-four Evocation sources without authoring or approval."""
from copy import deepcopy
import json
from prepare_low_illusion_spell_source_audit import ROOT, GAME, AUDIT, current_book_rows, digest
from prepare_low_necromancy_spell_source_audit import sha, dump
from prepare_combat_feat_source_audit import section
from prepare_divination_enchantment_rank4_source_audit import PRIOR_FILES

PREFIX = 'EVOCATION_RANK4'
QUESTIONS = {
    'inferno-wave': 'Preserve a60ft line,6d6 fire and ignition of the ground, Action/60ft/Instantaneous. Define width/height/origin, target and object eligibility, save outcomes, shared roll and cover snapshot. Unlike fire spells without an ignition clause, this explicitly ignites ground: define what ground can burn, finite hazard area/duration/fuel and extinguishing, recurring damage if any, and how environmental fire differs from an applied Burning condition. Do not erase the clause or invent perpetual fire on water/stone. Damage and ignition timing must not produce a second initial wave through newly destroyed cover.',
    'orb-of-annihilation': 'Preserve exactly one target,8d8 force and DEX save for half, Action/60ft/Instantaneous. Define creature/object eligibility, perception/line of effect, legal target defenses and one damage event with current rounding. Annihilation in the name does not add disintegration, item erasure, HP thresholds, automatic death, antimagic or a persistent orb. Decide any object-save interface explicitly rather than borrowing creature defenses. No unprinted impact area, piercing through targets or retargeting after paid hidden ineligibility.',
    'freezing-rain': 'Preserve30ft radius,4d6 cold per round and slippery terrain, Core Action/range30ft/Instantaneous. Resolve casting-point range versus radius, finite vertical extent, lifetime/concentration and exact initial/periodic/entry timing. Define slippery movement/standing rules without silently importing another spell or adding Frozen. State shared versus individual damage, saves, recipient line of effect and whether terrain remains after magic ends. Reentry, forced movement, overlapping casts, extra turns and suppression/resumption cannot silently multiply ticks. Ice/water quantity and harvestable supplies are not granted by a weather name.',
    'voltaic-detonation': 'Preserve a point detonation,6d8 lightning and Stunned for one turn, Action/60ft/Instantaneous. Define point-centered geometry or an explicitly single-target interpretation, targets/objects, initial snapshot and shared roll. Specify damage save/outcomes separately from Stunned save/eligibility and the actual one-turn endpoint, including midturn casting, extra turns and outside initiative. Bind successful hard control to existing source-character/target/encounter history; blocked Stunned must not erase otherwise legal damage or create a later application. No conductive chain, elemental immunity inferred beyond its scope or repeated shock is added.',
    'ice-storm': 'Preserve4d6 bludgeoning PLUS4d6 cold and difficult terrain, Action/60ft/Instantaneous. Define area shape/dimensions/height, perception/placement, target/object eligibility and save outcomes. Resolve one mixed-type damage event under current typed-packet defenses, rounding and damage-sharing rules; do not silently reduce the source dice. Give a finite difficult-terrain area and endpoint, overlap/clearing/suppression rules and whether its persistence is physical or magical. No extra Prone, slippery check, recurring hail tick, cold vulnerability or useful material supply is inferred.',
    'wall-of-fire': 'Preserve5d8 fire when passing through AND5d8 to nearby creatures, Action/60ft/concentration up to one minute. Define finite shape, length/height/thickness, placement and occupied-space resolution; nearby distance/sides, initial effects and exact ongoing trigger times. Resolve whether one movement/turn can meet both clauses and how many real packets result, with actual shared-roll and per-source event identities. Distinguish voluntary movement, forced movement, moving wall and teleportation. Define sight/cover/passage and ignition only if supported or expressly NEW. No familiar-game opaque wall, one-sided heat, unlimited crossing damage or stock-producing flame is silently imported.',
    'vitriolic-sphere': 'Preserve10d4 acid initially and5d4 next round, Action/60ft/Instantaneous. Define sphere radius/center/geometry, target/object eligibility, save/outcomes for each component and whether later damage requires initial failure, actual damage or only initial eligibility. Bind exactly one delayed packet to a named future marker and actual original recipients; decide cleanup/cure/death and suppression without an invented repeat exposure. No extra tick from recasting identity, extra turns or entering the old area. Preserve the later packet even though metadata says Instantaneous by an explicit source-clock ruling; no retroactive doubling or imported external dice.',
    'storm-sphere': 'Preserve4d6 bludgeoning in an area and4d6 lightning to a nearby target each round, Core Action/60ft/Instantaneous. Define finite geometry, lifetime/concentration, area bludgeoning timing and each-round lightning opportunity; whether command/action/Bonus Action is required must be explicit NEW authoring. Define nearby distance from the sphere or caster, target perception and line of effect, attack/save and ordering of independently typed events. Specify target commitment, skipped unavailable opportunities, source caps, movement of the sphere if any and ending/suppression. No unlimited off-turn bolts, automatic hostile selection, free additional Actions, unprinted difficult terrain or banked missed attacks.'
}


def main():
    inherited_path = AUDIT / 'EVOCATION_RANK3_SOURCE_PREPARATION.json'
    inherited = json.loads(inherited_path.read_text(encoding='utf-8'))
    protected = deepcopy(inherited['protectedFiles'])
    assert all(sha(GAME / p) == h for p, h in protected.items())

    def read(path):
        protected[path.relative_to(GAME).as_posix()] = sha(path)
        return json.loads(path.read_text(encoding='utf-8-sig'))

    catalog = read(ROOT / 'data/public/spell_playtests/catalog.json'); rows = catalog['spells']; by = {r['id']: r for r in rows}
    selected = [r for r in rows if r['operational'] is None and 'Evocation' in r['schools'] and min(v['rank'] for v in r['classAccess'].values()) == 4]
    assert len(selected) == 8 and {r['id'] for r in selected} == set(QUESTIONS)
    original = read(ROOT / 'data/playtest/spell_sources/catalog.json')
    core = read(ROOT / 'data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json')
    book = current_book_rows(); bindings = []; core_count = 0
    for row in selected:
        assert row['source']['original'] == original[row['id']]
        for entry in row['source']['coreEntries'] + row['source']['possibleHistoricalAliases']:
            assert entry['original'] == core['spells'][entry['index']]; core_count += 1
        for placement in row['source']['original']['placements']:
            matches = [b for b in book if b['name'] == row['name'] and b['school'] == placement['school'] and b['level'] == placement['level']]
            assert len(matches) == 1
            bindings.append({'spellId': row['id'], 'catalogPlacement': placement, 'currentBookRow': matches[0],
                             'summaryDifferencePreserved': placement['summary'] != matches[0]['summary']})
    counterpart_ids = ['chain-jolt', 'burning-hands', 'earth-tremor', 'ice-knife', 'thunderwave',
                       'scorching-raystorm', 'lightning-pulse', 'frost-nova', 'arcane-implosion',
                       'scorching-line', 'shatter', 'snowball-swarm', 'acid-arrow']
    pending_ids = ['flame-geyser', 'arc-flash', 'fireball', 'lightning-bolt', 'minute-meteors', 'tidal-wave']
    assert all(by[x]['operational'] is not None for x in counterpart_ids)
    assert all(by[x]['operational'] is None for x in pending_ids)
    counterparts = [by[x] for x in counterpart_ids + pending_ids]
    mentions = [r for r in read(ROOT / 'data/public/spell_playtests/class_name_mentions_for_review.json') if r.get('spellId') in QUESTIONS]
    manifest = read(ROOT / 'data/public/class_playtests/manifest.json'); classes = {r['class']: r for r in manifest['classes']}; class_records = []
    for mention in mentions:
        path = (ROOT / 'docs/mechanics' / classes[mention['class']]['data']).resolve(); data = read(path)
        if mention['location'] == 'engine': record = {'engine': data.get('engine', [])}
        else:
            found = [c for c in data['cards'] if c['id'] == mention['location']]; assert len(found) == 1; record = {'card': found[0]}
        class_records.append({'mention': mention, **record, 'file': path.relative_to(GAME).as_posix(), 'scope': 'Textual comparison only; no automatic grant.'})
    excerpts = deepcopy(inherited['currentGoverningExcerpts'])
    path = ROOT / 'docs/mechanics/CONDITIONS_PLAYTEST.md'; text = path.read_text(encoding='utf-8')
    protected[path.relative_to(GAME).as_posix()] = sha(path)
    excerpts.append({'file': path.relative_to(GAME).as_posix(), 'sha256': sha(path), 'heading': 'Stunned', 'exactText': section(text, 'Stunned')})
    prior = []
    for filename in PRIOR_FILES + ['DIVINATION_ENCHANTMENT_RANK4_SOURCE_PREPARATION.json']:
        prior.extend(r['spellId'] for r in read(AUDIT / filename)['selectedSpells'])
    records = [{'spellId': r['id'], 'questionId': f'EV4-{i+1:02}', 'scope': 'pre-push mechanical source question',
                'fullSourceAndCurrentAccessRecord': r, 'recordSha256': digest(r), 'individualQuestion': QUESTIONS[r['id']]} for i, r in enumerate(selected)]
    checks = [('Eight exact pending rank-four Evocation identities', len(records) == 8),
              ('All original catalog/Core records retained exactly', core_count == 8),
              ('Eight exact current-book bindings', len(bindings) == 8),
              ('Thirteen reviewed and six pending full comparison records', len(counterparts) == len(set(counterpart_ids + pending_ids)) == 19),
              ('Every registered class mention retains its whole actual record', len(class_records) == len(mentions)),
              ('No duplication with168 already prepared identities', len(prior) == len(set(prior)) == 168 and not set(prior).intersection(QUESTIONS)),
              ('Ordinary totals remain276 operational and572 pending', len(rows) == 848 and sum(r['operational'] is not None for r in rows) == 276),
              ('All exact excerpts remain current', all(e['exactText'] in (GAME / e['file']).read_text(encoding='utf-8') for e in excerpts)),
              ('All protected inputs remain unchanged', all(sha(GAME / p) == h for p, h in protected.items()))]
    assert all(ok for _, ok in checks), [n for n, ok in checks if not ok]
    counts = {'selectedEvocationRank4': 8, 'sourceSpells': 848, 'operationalSpells': 276, 'remaining': 572,
              'prePushMechanicalQuestions': 8, 'postPushReceiptOnly': 0, 'currentBookBindings': 8, 'exactCoreEntries': 8,
              'reviewedCounterparts': 13, 'pendingCounterparts': 6, 'classComparisonRecords': len(class_records),
              'governingExcerpts': len(excerpts), 'focusedPendingSourceIdentitiesIncludingThisCohort': 176,
              'prePushPreparedSpellQuestionsIncludingThisCohort': 174, 'postPushReceiptsIncludingThisCohort': 2}
    data = {'status': 'prepared-not-sent; eight mechanical source questions; no approvals',
            'commonOperationalQuestion': inherited['commonOperationalQuestion'], 'selectedSpells': records,
            'currentBookBindings': bindings, 'completeCounterparts': counterparts, 'classComparisonRecords': class_records,
            'currentGoverningExcerpts': excerpts, 'precedingEvocationExactVerdict': inherited['precedingEvocationExactVerdict'],
            'currentRankCosts': catalog['costByRank'], 'currentClassProgression': catalog['classProgression'],
            'counts': counts, 'checks': [{'name': n, 'pass': ok} for n, ok in checks], 'protectedFiles': protected,
            'spellsApproved': 0, 'sourceInformationDeleted': 0, 'cosmology': 'post-push only',
            'futureDispatch': 'After active Fishing exact review, rebase dependencies. Source decisions precede separate exact-card review.'}
    dump(AUDIT / f'{PREFIX}_SOURCE_PREPARATION.json', data)
    lines = ['# Rank-four Evocation source audit', '', data['status'], '',
             'Eight identities retain eight full Core records and eight current-book placements. Source damage dice, explicit terrain/ignition clauses and the distinction between range and area remain unchanged. Recurring effects marked Instantaneous need finite timing decisions; no external spell implementation is assumed.', '',
             '| Case | Spell | Mechanical source question |', '|---|---|---|']
    lines += [f"| {r['questionId']} | {r['fullSourceAndCurrentAccessRecord']['name']} | {r['individualQuestion']} |" for r in records]
    lines += ['', 'All eight remain unfinished. Nine prepared cohorts now retain176 distinct pending identities and183 book bindings, with174 mechanical questions and the earlier two post-push receipts. No source changed, no spell approved and no cosmology reviewed.', '']
    report = '\n'.join(lines); (AUDIT / f'{PREFIX}_SOURCE_AUDIT.md').write_text(report, encoding='utf-8', newline='\n')
    packet = 'PREPARED RANK-FOUR EVOCATION SOURCE CONFERENCE — NOT SENT.\n\n' + report + '\nCOMPLETE SOURCE AND CURRENT DEPENDENCY EVIDENCE\n' + json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    path = AUDIT / f'CODEX_{PREFIX}_SOURCE_PREPARED.txt'; path.write_text(packet, encoding='utf-8', newline='\n')
    status = {'status': data['status'], 'packetFile': path.name, 'characters': len(packet), 'packetSha256': sha(path),
              'counts': counts, 'checkCount': len(checks), 'protectedFilesUnchanged': len(protected),
              'spellsApproved': 0, 'sourceInformationDeleted': 0, 'cosmology': 'post-push only'}
    dump(AUDIT / f'{PREFIX}_SOURCE_STATUS.json', status); print(json.dumps(status))


if __name__ == '__main__':
    main()
