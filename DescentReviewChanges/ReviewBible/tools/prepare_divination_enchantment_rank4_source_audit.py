"""Preserve fifteen rank-four spell identities for a future source conference.

This makes no operational changes and sends no messages. Both school placements
of Confusion and Phantasmal Killer remain separate source evidence.
"""
from copy import deepcopy
import json
from prepare_low_illusion_spell_source_audit import ROOT, GAME, AUDIT, current_book_rows, digest
from prepare_low_necromancy_spell_source_audit import sha, dump
from prepare_combat_feat_source_audit import section

PREFIX = 'DIVINATION_ENCHANTMENT_RANK4'
QUESTIONS = {
    'fate-reversal': 'Preserve one forced reroll of an attack, save or check anywhere on the battlefield, alongside Core Action/60ft/Instantaneous. Resolve the Action-versus-live-roll timing and battlefield-versus-60ft reach explicitly. Define a finite pending permission or other source-compatible trigger, actual perception and ordinary information access, one canonical original roll and its entire replacement lineage, whole d20 procedure versus a single die, mandatory replacement and final natural-result processing. Decide its relationship to the reviewed Mark Omen/Fate Coin shared guard and actual class rerolls. No reversing completed consequences, rerolling damage under an attack permission, extra cost/on-hit hooks, remote secret-roll revelation or infinite mutual rerolls.',
    'seal-vision': 'Preserve blocking Divination spells from affecting an area or creature, Action/60ft/Instantaneous. Define the actual choice of target or fixed area, geometry, lifetime/concentration, initial and continuing eligibility, and what affecting means for remote sensors, information generated about a subject, and noninformational Divination such as reroll marks. Use exact school/source scopes and current information-protection rules. Decide existing effects, new casts, entry/exit, suppression, replacement and neutral blocked answers. A school name alone must not accidentally create blindness, broad antimagic, physical concealment, immunity to every detection technique or deletion of already learned facts.',
    'aspect-of-insight': 'Preserve advantage on all mental saves and +2 INT/WIS for one minute, Core Action/60ft. Resolve whether the printed Gain means self or an allowed recipient, what mental saves includes, and whether +2 changes scores, modifiers, checks/saves or another explicitly delimited quantity. Specify ceilings and derived-value recalculation, including spell DC, attacks, skills, maxima, prepared/repertoire permissions and concentration where actually dependent. Do not silently turn +2 into +1 or +2 everywhere; record the interpretation. Apply strongest-stat and advantage rules; ending, recasting or suppression must not refresh RP, heal, relearn or create retained resources.',
    'locate-creature': 'Preserve sensing direction to one specific creature within five miles, Core Action/60ft/Instantaneous. Resolve five-mile sensing scope versus 60ft metadata, identification/familiarity, actual creature identity through shapechange and direction meaning in three dimensions. Decide a snapshot versus maintained tracking, boundaries, movement after resolution, obstruction and existing information wards. Distinguish Locate Person and Soul Mark. No distance, safe route, destination sight, current condition, exact coordinates, new plane relationship or target knowledge is implied merely by a bearing; missing/protected/out-of-range results need a finite nonleaking procedure.',
    'faction-secrets': 'Preserve learning one secret about a faction, Action/60ft/Instantaneous. Define the actual faction and scope of inquiry, one finite useful fact, what qualifies as secret, inquiry history and handling of genuinely new facts versus equivalent repeated inquiries. Compare reviewed Faction Divination, Insight and Spy without silently reducing the source to public trivia or inventing absent lore. Resolve range and information protection against the real subject/generating source; unavailable/protected results must not disclose why. No reputation change, membership, universal archive access, cosmology, new faction roster or automatic public disclosure follows from learning a fact.',
    'alignment-forecast': 'Preserve predicting consequences of an action based on alignment influences, Action/60ft/Instantaneous. Define a declared action, intended beginning, finite horizon, beneficiary/question and answer vocabulary. Use actual already established alignment records and current circumstances; compare Augury and Alignment Prediction. Specify uncertainty, protected or undefined premises, repeated equivalent inquiries and changes in voluntary choices. This is only a mechanical question about current records, not authorization to invent alignment axes, cosmic forces, theology or guaranteed destiny; cosmology remains post-push. Do not force choices or reveal an entire hidden causal chain.',
    'resonance-divination': 'Preserve exactly how many RP a creature has, Action/60ft/Instantaneous. Define one actual perceived target and the exact snapshot checkpoint relative to the paid cast, interruptions, RP spending, transfers and recovery. Resolve current pool versus maximum, temporary/protected reserves, creatures without RP and failed or protected information. Retain the source promise of an exact permitted value rather than silently substituting the lower-rank colored aura. It grants no drain, transfer, capacity, repertoire list, hidden source identity or continuing live readout. Independent future inquiries pay normally and never rewind resource history.',
    'dominate-person': 'Preserve full control of a humanoid, WIS save each turn, Action/60ft and concentration up to one minute. Bind Humanoid eligibility to actual creature records. Explicitly define initial and repeat-save phase, order opportunities, communication, permitted behaviors, optional finite expenditures, commands involving self-harm, and interaction with actual player agency. Explain the finite meaning of full control relative to existing compulsion rules; do not silently import another game or erase the promise. Compare Dire Charm, Crown of Madness and Dominate Beast, shared hard-control reservation, compelled-budget arbitration and six-second/initiative transitions. Decide companion-phase behavior if a qualifying Humanoid uses that chassis. No extra turn, action budget, resource reset or fallback command arises from blocked control.',
    'mass-pacify': 'Preserve all enemies in a30ft radius being unable to attack unless attacked, Core Action/range30ft/Instantaneous. Resolve center, radius versus casting range, enemy eligibility, snapshot versus entering aura, save, lifetime and concentration. Define attack prohibition scope and the actual provoking event: attempt, hit, damage or other explicit interpretation; whether release is per creature or whole application; and whether allies or third parties can provoke it. Compare Group Pacify, Voice of Peace and Pacify without silently replacing unless attacked with the broader unless provoked wording. Preserve hostile agency outside the actual restriction, actual damage/event identities and independent source histories.',
    'confusion': 'Preserve BOTH rank4 placements: Enchantment one target, random actions for one minute, WIS each round, Action/60ft; Illusion creatures in a10ft radius, Core Action/range10ft/Instantaneous. Decide actual class-school modes versus an expressly justified harmonization. Retain all school-specific class access and range evidence. Author a finite neutral behavior table and target selection, save timing, duration/concentration, current/extra/virtual-turn handling and ordinary available budget. Compare Confusing Flash but do not assume its one-attack/flee table applies. Resolve hard-control reservation per real source/target, overlapping compulsory orders, unavailable behavior and self-destructive or prohibited resource use; no extra Actions, free rerolls or fresh control history from each random branch.',
    'erase-emotion': 'Preserve removal of anger, fear or pain and inability to use rage/fear abilities, Action/60ft/Instantaneous. Define recipient/save, choice of emotions, finite lifetime/concentration and whether underlying emotion/condition is removed or suppressed. Unlike Calm Emotions, this source expressly restricts abilities: define eligible actual mechanical rage/fear features from their source records, rather than treating every emotional name as a match or erasing the clause. Determine existing versus new activation and continuing effects, other recipients, Frightened immunity/suppression, and save/clock continuity. Removing pain is not HP healing, injury repair, revival, Strain/Dissonance removal or compelled friendliness.',
    'compulsion': 'Preserve forcing a creature to move in a chosen direction, WIS negates, Action/60ft/Instantaneous. Define when the movement occurs, finite distance or ordinary movement budget, what the direction anchors to, known safe/legal paths and blocked-route behavior. Decide whether it spends the target movement and provokes opportunity attacks, or is an explicit displacement; do not blend both models opportunistically. Resolve voluntary/forced transport, movement modes/support, hazards and actual absolute restrictions, current versus future turn timing, and the shared compelled-budget priority. No unprinted Dash, Action denial, extra movement, repeated off-turn movement or permission to spend optional resources.',
    'phantasmal-killer': 'Preserve BOTH rank4 placements: Enchantment a nightmare only the target can see, WIS or Frightened and4d10 psychic; Illusion Frightened and4d10 psychic PER ROUND. Both Core entries are Action/60ft/concentration up to one minute. Decide school-specific modes versus justified harmonization, initial/repeat save and damage checkpoints, initial versus periodic damage, fear and damage component dependencies, and actual sight/mental-perception requirements. Fear-only immunity or suppression does not automatically settle the damage component: state the rule. Keep caster clocks, actual damage source, duplicate casts and target death/endings finite, with no invented extra ticks on entry, extra turns or suppression/resumption.',
    'charm-monster': 'Preserve a creature regarding the caster as friendly, WIS negates, Action/60ft/Instantaneous. Resolve finite lifetime/concentration, Core Charmed versus a distinct attitude effect, harm/repeat-save/end triggers and perception/communication requirements. Monster in the title does not itself give a supported creature-type restriction or immunity. Compare Charm Person and the actual Charmed relation; friendly does not by itself authorize commands, consent, truth, access, loyalty or resource expenditure. Define multiple casters, existing hostility, suppressed relations, memories after ending and source-specific replacement without modifying faction standing or alignment.',
    'overwhelming-grief': 'Preserve Incapacitated through sorrow, WIS negates, Action/60ft/Instantaneous. Define finite lifetime/concentration, initial and any repeat saves, endings, actual component identity and successful establishment of the shared source-character/target/encounter hard-control allowance. Incapacitated retains its real effects, including concentration loss, without invented Prone, Unconscious, Speed0 or healing. Decide interaction with Calm Emotions and Erase Emotion through their actual scopes; emotional flavor alone is not blanket immunity or an automatic cure. Suppression and expiration preserve real clocks and spent hard-control history, with no deferred application when initial control was blocked.'
}
COUNTERPARTS = [
    'mark-omen', 'fate-coin', 'locate-object', 'locate-person', 'soul-mark',
    'faction-divination', 'faction-insight', 'faction-spy', 'augury', 'alignment-prediction',
    'resonance-sight', 'resonance-sight-greater', 'charm-person', 'pacify', 'voice-of-peace',
    'group-pacify', 'confusing-flash', 'dire-charm', 'crown-of-madness', 'dominate-beast',
    'calm-emotions', 'command', 'hypnotic-pattern', 'hideous-laughter', 'fear', 'suggestion'
]
PENDING = ['mind-blank', 'greater-invisibility', 'seal-vision']
PRIOR_FILES = [
    'LOW_ILLUSION_SPELL_SOURCE_PREPARATION.json', 'LOW_UNIVERSAL_SPELL_SOURCE_PREPARATION.json',
    'LOW_TRANSMUTATION_SPELL_SOURCE_PREPARATION.json', 'LOW_NECROMANCY_SPELL_SOURCE_PREPARATION.json',
    'EVOCATION_RANK3_SOURCE_PREPARATION.json', 'REMAINING_RANK3_SPELL_SOURCE_PREPARATION.json',
    'ABJURATION_CONJURATION_RANK4_SOURCE_PREPARATION.json'
]


def main():
    inherited = json.loads((AUDIT / PRIOR_FILES[0]).read_text(encoding='utf-8'))
    protected = deepcopy(inherited['protectedFiles'])
    assert all(sha(GAME / p) == h for p, h in protected.items())

    def read(path):
        protected[path.relative_to(GAME).as_posix()] = sha(path)
        return json.loads(path.read_text(encoding='utf-8-sig'))

    catalog = read(ROOT / 'data/public/spell_playtests/catalog.json')
    rows = catalog['spells']; by = {r['id']: r for r in rows}
    selected = [r for r in rows if r['operational'] is None and
                set(r['schools']).intersection({'Divination', 'Enchantment'}) and
                min(v['rank'] for v in r['classAccess'].values()) == 4]
    assert len(selected) == 15 and {r['id'] for r in selected} == set(QUESTIONS)
    source = read(ROOT / 'data/playtest/spell_sources/catalog.json')
    core = read(ROOT / 'data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json')
    book = current_book_rows(); bindings = []; differences = []; source_verified = 0
    for row in selected:
        assert row['source']['original'] == source[row['id']]
        for e in row['source']['coreEntries'] + row['source']['possibleHistoricalAliases']:
            assert e['original'] == core['spells'][e['index']]
            source_verified += 1
        for placement in row['source']['original']['placements']:
            matches = [b for b in book if b['name'] == row['name'] and
                       b['school'] == placement['school'] and b['level'] == placement['level']]
            assert len(matches) == 1, (row['id'], placement)
            bindings.append({'spellId': row['id'], 'catalogPlacement': placement, 'currentBookRow': matches[0],
                             'summaryDifferencePreserved': placement['summary'] != matches[0]['summary']})
            for e in row['source']['coreEntries']:
                orig = e['original']
                if placement['school'] == orig['school'] and placement['level'] == orig['level'] and placement['summary'] != orig['effect']:
                    differences.append({'spellId': row['id'], 'catalogSummary': placement['summary'],
                                        'coreEffect': orig['effect'], 'coreIndex': e['index']})
    # Comparisons must be external to this cohort; selected spells already retain
    # their complete records and may compare against one another directly.
    pending = [x for x in PENDING if x not in QUESTIONS]
    assert all(by[x]['operational'] is not None for x in COUNTERPARTS)
    assert all(by[x]['operational'] is None for x in pending)
    counterparts = [by[x] for x in COUNTERPARTS + pending]
    mentions = [r for r in read(ROOT / 'data/public/spell_playtests/class_name_mentions_for_review.json')
                if r.get('spellId') in QUESTIONS]
    manifest = read(ROOT / 'data/public/class_playtests/manifest.json')
    classes = {r['class']: r for r in manifest['classes']}; class_records = []
    for mention in mentions:
        path = (ROOT / 'docs/mechanics' / classes[mention['class']]['data']).resolve(); data = read(path)
        if mention['location'] == 'engine':
            record = {'engine': data.get('engine', [])}
        else:
            found = [c for c in data['cards'] if c['id'] == mention['location']]
            assert len(found) == 1; record = {'card': found[0]}
        class_records.append({'mention': mention, **record, 'file': path.relative_to(GAME).as_posix(),
                              'scope': 'Textual source comparison; no automatic spell grant or identity merge.'})
    excerpts = deepcopy(inherited['currentGoverningExcerpts'])
    for name, headings in {
        'ENCHANTMENT_CONTROL_INTEGRATION_PLAYTEST.md': None,
        'ENCHANTMENT_RANK3_INTEGRATION_PLAYTEST.md': None,
        'CREATURE_LIFECYCLE_PLAYTEST.md': None,
        'CONDITIONS_PLAYTEST.md': ['Charmed'],
    }.items():
        path = ROOT / 'docs/mechanics' / name; text = path.read_text(encoding='utf-8')
        protected[path.relative_to(GAME).as_posix()] = sha(path)
        for heading in headings or [None]:
            excerpts.append({'file': path.relative_to(GAME).as_posix(), 'sha256': sha(path),
                             'heading': heading or 'entire guide',
                             'exactText': section(text, heading) if heading else text})
    prior = []
    for filename in PRIOR_FILES:
        prior.extend(r['spellId'] for r in read(AUDIT / filename)['selectedSpells'])
    records = [{'spellId': r['id'], 'questionId': f'DE4-{i+1:02}',
                'scope': 'pre-push mechanical source question',
                'fullSourceAndCurrentAccessRecord': r, 'recordSha256': digest(r),
                'individualQuestion': QUESTIONS[r['id']]} for i, r in enumerate(selected)]
    cross_school = [{ 'spellId': r['id'], 'placements': r['source']['original']['placements'],
                     'coreEntries': r['source']['coreEntries'], 'classAccess': r['classAccess']}
                    for r in selected if len(r['source']['original']['placements']) > 1]
    checks = [
        ('15 exact minimum-class-rank4 Divination/Enchantment identities', len(records) == 15),
        ('All original catalog objects and17 Core entries retained exactly', source_verified == 17),
        ('17 exact current-book placements retained', len(bindings) == 17),
        ('Confusion and Phantasmal Killer retain both school modes and access',
         {r['spellId'] for r in cross_school} == {'confusion', 'phantasmal-killer'} and
         all(len(r['placements']) == len(r['coreEntries']) == 2 for r in cross_school)),
        ('No same-placement catalog/Core prose conflict silently introduced', not differences),
        ('26 complete reviewed and two external pending comparisons retained', len(counterparts) == len(set(COUNTERPARTS + pending)) == 28),
        ('Every actual class-name mention retains its whole source record', len(class_records) == len(mentions)),
        ('No duplication with153 prior prepared identities', len(prior) == len(set(prior)) == 153 and not set(prior).intersection(QUESTIONS)),
        ('Ordinary spell totals stay276 operational/572 pending', len(rows) == 848 and sum(r['operational'] is not None for r in rows) == 276),
        ('All exact excerpts and protected inputs remain unchanged',
         all(e['exactText'] in (GAME / e['file']).read_text(encoding='utf-8') for e in excerpts) and
         all(sha(GAME / p) == h for p, h in protected.items())),
    ]
    assert all(ok for _, ok in checks), [n for n, ok in checks if not ok]
    counts = {'sourceSpells': 848, 'operationalSpells': 276, 'remaining': 572, 'selectedDivinationEnchantmentRank4': 15,
              'prePushMechanicalQuestions': 15, 'postPushReceiptOnly': 0, 'exactCoreEntries': source_verified,
              'currentBookBindings': len(bindings), 'reviewedCounterparts': len(COUNTERPARTS),
              'pendingCounterparts': len(pending), 'classComparisonRecords': len(class_records),
              'governingExcerpts': len(excerpts), 'crossSchoolConflicts': len(cross_school),
              'catalogCoreEffectDifferences': len(differences), 'focusedPendingSourceIdentitiesIncludingThisCohort': 168,
              'prePushPreparedSpellQuestionsIncludingThisCohort': 166, 'postPushReceiptsIncludingThisCohort': 2}
    data = {'status': 'prepared-not-sent; fifteen mechanical source questions; no approvals',
            'commonOperationalQuestion': inherited['commonOperationalQuestion'],
            'scopeBoundary': 'Existing mechanical records only. No new cosmology, alignment axis, theology, faction roster or guaranteed destiny. Cosmology is deferred until after authorized push and remote verification.',
            'selectedSpells': records, 'currentBookBindings': bindings, 'completeCounterparts': counterparts,
            'classComparisonRecords': class_records, 'crossSchoolConflicts': cross_school,
            'catalogCoreEffectDifferences': differences, 'currentGoverningExcerpts': excerpts,
            'currentRankCosts': catalog['costByRank'], 'currentClassProgression': catalog['classProgression'],
            'counts': counts, 'checks': [{'name': n, 'pass': ok} for n, ok in checks], 'protectedFiles': protected,
            'spellsApproved': 0, 'sourceInformationDeleted': 0, 'cosmology': 'post-push only',
            'futureDispatch': 'After active Fishing exact review, rebase relevant dependencies and submit source questions before authoring. Unsent preparation cannot confer approval.'}
    dump(AUDIT / f'{PREFIX}_SOURCE_PREPARATION.json', data)
    lines = ['# Rank-four Divination and Enchantment source audit', '', data['status'], '',
             'Fifteen identities and seventeen source/book placements are preserved. Confusion and Phantasmal Killer each retain both school versions, with their actual class access. Their targeting, duration and damage cadence differences require explicit decisions.', '',
             'Other printed tensions include Fate Reversal\'s Action/60-foot metadata versus a battlefield reroll, Locate Creature\'s five-mile direction promise versus 60-foot metadata, and several lasting control promises marked Instantaneous. Erase Emotion expressly disables rage/fear abilities; the Calm Emotions precedent cannot silently erase that clause.', '',
             '| Case | Spell | Mechanical source question |', '|---|---|---|']
    lines += [f"| {r['questionId']} | {r['fullSourceAndCurrentAccessRecord']['name']} | {r['individualQuestion']} |" for r in records]
    lines += ['', 'Existing alignment/faction records are mechanical premises only; this packet authorizes no cosmology or new lore. All fifteen spells remain unapproved. The eight prepared cohorts cover168 distinct pending identities and175 book bindings:166 mechanical questions and the earlier Blink/Banishment post-push receipts. Ordinary totals remain276 operational/572 pending.', '']
    report = '\n'.join(lines)
    (AUDIT / f'{PREFIX}_SOURCE_AUDIT.md').write_text(report, encoding='utf-8', newline='\n')
    packet = 'PREPARED RANK-FOUR DIVINATION/ENCHANTMENT SOURCE CONFERENCE — NOT SENT.\n\n' + report + '\nCOMPLETE SOURCE AND CURRENT DEPENDENCY EVIDENCE\n' + json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    path = AUDIT / f'CODEX_{PREFIX}_SOURCE_PREPARED.txt'; path.write_text(packet, encoding='utf-8', newline='\n')
    status = {'status': data['status'], 'packetFile': path.name, 'characters': len(packet), 'packetSha256': sha(path),
              'counts': counts, 'checkCount': len(checks), 'protectedFilesUnchanged': len(protected),
              'spellsApproved': 0, 'sourceInformationDeleted': 0, 'cosmology': 'post-push only'}
    dump(AUDIT / f'{PREFIX}_SOURCE_STATUS.json', status)
    print(json.dumps(status))


if __name__ == '__main__':
    main()
