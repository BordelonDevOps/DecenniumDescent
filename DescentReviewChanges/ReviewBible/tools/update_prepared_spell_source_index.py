"""Reconcile prepared source coverage without modifying any frozen packet."""
from pathlib import Path
from datetime import datetime, timezone
import json
import re
import shutil
from prepare_low_illusion_spell_source_audit import ROOT, GAME, AUDIT
from prepare_low_necromancy_spell_source_audit import sha, dump

COHORTS = [
    ('Low-rank Illusion', 'LOW_ILLUSION_SPELL'),
    ('Low-rank Universal', 'LOW_UNIVERSAL_SPELL'),
    ('Low-rank Transmutation', 'LOW_TRANSMUTATION_SPELL'),
    ('Low-rank Necromancy', 'LOW_NECROMANCY_SPELL'),
    ('Rank-three Evocation', 'EVOCATION_RANK3'),
    ('Remaining rank-three spells', 'REMAINING_RANK3_SPELL'),
    ('Rank-four Abjuration and Conjuration', 'ABJURATION_CONJURATION_RANK4'),
    ('Rank-four Divination and Enchantment', 'DIVINATION_ENCHANTMENT_RANK4'),
    ('Rank-four Evocation', 'EVOCATION_RANK4'),
]


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    all_records = []; bindings = []; protected = {}; table = []; files = []
    for name, prefix in COHORTS:
        filename = prefix + '_SOURCE_PREPARATION.json'; files.append(filename)
        data = read(AUDIT / filename); status = read(AUDIT / (prefix + '_SOURCE_STATUS.json'))
        assert data['spellsApproved'] == 0 and all(x['pass'] for x in data['checks'])
        packet = AUDIT / status['packetFile']
        assert sha(packet) == status['packetSha256']
        assert len(packet.read_text(encoding='utf-8')) == status['characters']
        all_records += data['selectedSpells']; bindings += data['currentBookBindings']
        for p, h in data['protectedFiles'].items():
            assert p not in protected or protected[p] == h, p
            protected[p] = h
        deferred = sum(r.get('scope') == 'post-push receipt only' for r in data['selectedSpells'])
        n = len(data['selectedSpells'])
        table.append(f"| [{name}]({prefix}_SOURCE_AUDIT.md) | {n} | {n-deferred} | {deferred} | {len(data['currentBookBindings'])} | {status['checkCount']} |")
    ids = [r['spellId'] for r in all_records]
    deferred = [r['spellId'] for r in all_records if r.get('scope') == 'post-push receipt only']
    assert len(ids) == len(set(ids)) == 176 and len(bindings) == 183
    assert set(deferred) == {'blink', 'banishment'}
    assert all(sha(GAME / p) == h for p, h in protected.items())
    catalog = read(ROOT / 'data/public/spell_playtests/catalog.json')['spells']
    pending = {r['id']: r for r in catalog if r['operational'] is None}
    assert set(ids).issubset(pending) and len(pending) == 572 and len(catalog) == 848
    low_ids = {r['id'] for r in pending.values() if min(v['rank'] for v in r['classAccess'].values()) <= 3}
    rank4_ids = {r['id'] for r in pending.values() if min(v['rank'] for v in r['classAccess'].values()) == 4}
    assert low_ids.issubset(ids) and len(rank4_ids) == 65
    missing_rank4 = sorted(rank4_ids - set(ids)); assert len(missing_rank4) == 26
    navigation = [GAME / 'START_HERE.md', AUDIT / 'PREPARED_SPELL_SOURCE_INDEX.md',
                  AUDIT / 'FOCUSED_SPELL_SOURCE_PREPARATION_COVERAGE.json',
                  AUDIT / 'GPT_REVIEW_CONTINUATION_HANDOFF.md',
                  AUDIT / 'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json',
                  ROOT / 'data/playtest/game_development_coverage.json']
    before = {p.relative_to(GAME).as_posix(): sha(p) for p in navigation}
    # Preserve each distinct input revision. Rerunning cannot overwrite an older
    # archive, and never copies or changes source books or submitted candidates.
    backup = AUDIT / ('navigation-before-nine-spell-cohorts-' + sha(navigation[2])[:12])
    if not backup.exists():
        for p in navigation:
            dest = backup / p.relative_to(GAME); dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dest)
        dump(backup / 'MANIFEST.json', before)
    else:
        archived = read(backup / 'MANIFEST.json')
        assert all(sha(backup / p) == h for p, h in archived.items())
    coverage = read(navigation[2])
    coverage.update({'distinctPreparedPendingSpellIds': 176, 'currentBookBindings': 183,
                     'prePushMechanicalQuestions': 174, 'postPushReceiptOnlyIds': deferred,
                     'protectedInputsUnchanged': len(protected), 'cohortFiles': files,
                     'minimumRank4SourceIdentitiesPrepared': 39, 'minimumRank4SourceIdentitiesRemaining': missing_rank4,
                     'allPendingMinClassRankZeroToThreeSourcesCovered': True,
                     'allPendingMinClassRankZeroToFourSourcesCovered': False,
                     'reviewApprovalsGranted': 0, 'packetsSent': 0})
    dump(navigation[2], coverage)
    text = '\n'.join(['# Prepared spell source conferences', '',
        '**Nine packets prepared; none sent or approved.** These retain 176 distinct unfinished identities and 183 exact current-book placements. There are 174 mechanical source questions and two unchanged receipts (Blink and Banishment) for the post-push cosmology review. Ordinary spell totals remain 276 operational drafts and 572 unfinished identities out of 848.', '',
        '| Source cohort | Identities | Mechanical questions | Post-push receipts | Book bindings | Local source checks |',
        '|---|---:|---:|---:|---:|---:|', *table, '',
        'All unfinished identities with minimum class-access rank 0–3 have source preparation. At minimum rank four, 39 of 65 identities are prepared; 26 remain. Higher-rank sources also remain. Source preparation precedes GPT decisions, authored cards and separate exact review. It is not operational approval.', '',
        'The Abjuration/Conjuration cohort preserves Elemental Drain\'s 2-RP/5-RP conflict, Spell Shield\'s level/Tier conflict and both Alignment Anchor placements, including Cleric rank7/17RP versus Druid rank4/7RP.', '',
        'The Divination/Enchantment cohort preserves both Confusion and Phantasmal Killer school versions, with seventeen Core/book placements across fifteen identities. Fate Reversal, Locate Creature, mental-attribute changes and emotion/compulsion boundaries have individual source questions.', '',
        'The eight Evocation sources retain their exact dice, explicit terrain/ignition clauses and delayed/recurring promises. Freezing Rain and Storm Sphere retain their Instantaneous metadata alongside their per-round effects; Wall of Fire keeps both passing-through and nearby damage clauses. These conflicts remain questions rather than unreviewed rule changes.', '',
        'The [coverage manifest](FOCUSED_SPELL_SOURCE_PREPARATION_COVERAGE.json) records duplicate checks, remaining rank-four identities and current protected-input validation. Rebase dependencies before dispatch and preserve prepared revisions. Fishing exact review is still the current notebook request.', ''])
    navigation[1].write_text(text, encoding='utf-8', newline='\n')
    start = navigation[0].read_text(encoding='utf-8')
    old = 'seven unsent cohorts, 153 identities, 158 book bindings, 151 mechanical questions'
    new = 'nine unsent cohorts, 176 identities, 183 book bindings, 174 mechanical questions'
    assert old in start or new in start
    navigation[0].write_text(start.replace(old, new), encoding='utf-8', newline='\n')
    handoff = navigation[3].read_text(encoding='utf-8')
    paragraph = ('### Current prepared spell coverage — nine cohorts\n\n'
        'The [source index](PREPARED_SPELL_SOURCE_INDEX.md) now records176 identities and183 book bindings:174 mechanical questions and the unchanged Blink/Banishment post-push receipts. '
        'The newest15 Divination/Enchantment sources pass10 source checks across71 protected inputs, preserving both Confusion/Phantasmal Killer school versions. '
        'Eight rank-four Evocation sources pass9 checks across73 protected inputs, retaining recurring-damage versus Instantaneous conflicts. '
        'All packets remain unsent and all23 new identities remain unapproved. Rank-four preparation covers39 of65 identities;26 remain, plus higher ranks. '
        'Fishing exact review remains the active notebook request. Earlier checkpoint totals below are historical.\n\n')
    if '### Current prepared spell coverage — nine cohorts' not in handoff:
        assert '## Next prepared source evidence' in handoff
        handoff = handoff.replace('## Next prepared source evidence', '## Next prepared source evidence\n\n' + paragraph, 1)
    navigation[3].write_text(handoff, encoding='utf-8', newline='\n')
    observation = read(navigation[4]); progress = observation.setdefault('independentProgress', {})
    progress.update({'focusedPendingSpellSourcesPrepared': 176, 'preparedSpellCohorts': 9,
                     'currentBookBindingsAcrossPreparedSpellPackets': 183,
                     'prePushSpellQuestionsAcrossPreparedPackets': 174, 'postPushSpellReceipts': deferred,
                     'rank4SourcesPrepared': 39, 'rank4SourcesRemaining': 26,
                     'divinationEnchantmentRank4SourcesPrepared': 15, 'evocationRank4SourcesPrepared': 8})
    observation['independentProgressUpdatedAtUtc'] = datetime.now(timezone.utc).isoformat()
    observation['currentGoalTurnClassification'] = 'progress: navigation preservation verified;23 additional rank-four sources prepared with both school variants and timing conflicts preserved; Fishing exact review still active on actual C turn'
    observation['consecutiveBlockedGoalTurns'] = 0; dump(navigation[4], observation)
    game_coverage = read(navigation[5])
    for aspect in game_coverage['aspects']:
        if aspect['id'] in ['DD-03', 'DD-11', 'DD-12', 'DD-13', 'DD-18', 'DD-21', 'DD-26', 'DD-35', 'DD-49']:
            for prefix in ['DIVINATION_ENCHANTMENT_RANK4', 'EVOCATION_RANK4']:
                for key, suffix in [('sourceEvidence', 'PREPARATION.json'), ('draftEvidence', 'AUDIT.md'), ('validationEvidence', 'STATUS.json')]:
                    p = f'docs/audit/2026-10-08/full-game/{prefix}_SOURCE_{suffix}'
                    if p not in aspect.setdefault(key, []): aspect[key].append(p)
        if aspect['id'] == 'DD-12':
            issue = 'Nine unsent source cohorts preserve176 identities/183 book bindings:174 mechanical questions and Blink/Banishment post-push receipts. Rank-four preparation covers39 of65 identities;26 remain, plus higher ranks. No approvals;276 operational/572 pending unchanged.'
            if issue not in aspect['openIssues']: aspect['openIssues'].append(issue)
    dump(navigation[5], game_coverage)
    for p in navigation[:2]:
        for link in re.findall(r'\]\(([^)]+)\)', p.read_text(encoding='utf-8')):
            if not re.match(r'^[a-z]+:', link): assert (p.parent / link.split('#')[0]).exists(), (p.name, link)
    receipt = {'status': 'PASS source coverage and navigation; zero approvals', 'cohorts': 9,
               'identities': 176, 'bookBindings': 183, 'mechanicalQuestions': 174, 'deferredReceipts': deferred,
               'protectedInputsUnchanged': len(protected), 'remainingRank4Identities': missing_rank4,
               'navigationBackup': backup.relative_to(AUDIT).as_posix(),
               'sourceInformationDeleted': False, 'cosmology': 'post-push only'}
    dump(AUDIT / 'NINE_SPELL_COHORT_NAVIGATION_RECEIPT.json', receipt); print(json.dumps(receipt))


if __name__ == '__main__':
    main()
