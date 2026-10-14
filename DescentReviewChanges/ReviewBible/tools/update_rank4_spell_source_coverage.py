"""Record complete pending rank0-4 source preparation; approval stays separate."""
from collections import Counter
from datetime import datetime, timezone
import json
import re
import shutil
from prepare_low_illusion_spell_source_audit import ROOT, GAME, AUDIT
from prepare_low_necromancy_spell_source_audit import sha, dump
from update_prepared_spell_source_index import COHORTS as FIRST_NINE

COHORTS = FIRST_NINE + [
    ('Remaining rank-four Illusion and Necromancy', 'ILLUSION_NECROMANCY_RANK4'),
    ('Remaining rank-four Transmutation and Universal', 'TRANSMUTATION_UNIVERSAL_RANK4')]


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def main():
    records = []; bindings = []; protected = {}; table = []; files = []
    for name, prefix in COHORTS:
        filename = prefix + '_SOURCE_PREPARATION.json'; files.append(filename)
        data = read(AUDIT / filename); status = read(AUDIT / (prefix + '_SOURCE_STATUS.json'))
        assert data['spellsApproved'] == 0 and all(x['pass'] for x in data['checks'])
        packet = AUDIT / status['packetFile']
        assert sha(packet) == status['packetSha256'] and len(packet.read_text(encoding='utf-8')) == status['characters']
        records += data['selectedSpells']; bindings += data['currentBookBindings']
        for p, h in data['protectedFiles'].items():
            assert p not in protected or protected[p] == h, p
            protected[p] = h
        deferred = sum(r.get('scope') == 'post-push receipt only' for r in data['selectedSpells'])
        count = len(data['selectedSpells'])
        table.append(f"| [{name}]({prefix}_SOURCE_AUDIT.md) | {count} | {count-deferred} | {deferred} | {len(data['currentBookBindings'])} | {status['checkCount']} |")
    ids = [r['spellId'] for r in records]
    deferred = [r['spellId'] for r in records if r.get('scope') == 'post-push receipt only']
    assert len(ids) == len(set(ids)) == 202 and len(bindings) == 210
    assert set(deferred) == {'blink', 'banishment', 'veiled-chest'}
    assert all(sha(GAME / p) == h for p, h in protected.items())
    catalog = read(ROOT / 'data/public/spell_playtests/catalog.json')['spells']
    pending = {r['id']: r for r in catalog if r['operational'] is None}
    minimum = lambda r: min(v['rank'] for v in r['classAccess'].values())
    all_low = {r['id'] for r in pending.values() if minimum(r) <= 4}
    rank4 = {r['id'] for r in pending.values() if minimum(r) == 4}
    assert set(ids) == all_low and len(rank4) == 65 and len(pending) == 572 and len(catalog) == 848
    unprepared = {i: r for i, r in pending.items() if i not in ids}
    assert len(unprepared) == 370
    by_rank = dict(sorted(Counter(minimum(r) for r in unprepared.values()).items()))
    navigation = [GAME / 'START_HERE.md', AUDIT / 'PREPARED_SPELL_SOURCE_INDEX.md',
                  AUDIT / 'FOCUSED_SPELL_SOURCE_PREPARATION_COVERAGE.json',
                  AUDIT / 'GPT_REVIEW_CONTINUATION_HANDOFF.md',
                  AUDIT / 'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json',
                  ROOT / 'data/playtest/game_development_coverage.json']
    before = {p.relative_to(GAME).as_posix(): sha(p) for p in navigation}
    backup = AUDIT / ('navigation-before-rank4-source-coverage-' + sha(navigation[2])[:12])
    if not backup.exists():
        for p in navigation:
            target = backup / p.relative_to(GAME); target.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(p, target)
        dump(backup / 'MANIFEST.json', before)
    else:
        assert all(sha(backup / p) == h for p, h in read(backup / 'MANIFEST.json').items())
    coverage = read(navigation[2]); coverage.update({
        'distinctPreparedPendingSpellIds': 202, 'currentBookBindings': 210, 'prePushMechanicalQuestions': 199,
        'postPushReceiptOnlyIds': deferred, 'protectedInputsUnchanged': len(protected), 'cohortFiles': files,
        'minimumRank4SourceIdentitiesPrepared': 65, 'minimumRank4SourceIdentitiesRemaining': [],
        'allPendingMinClassRankZeroToFourSourcesCovered': True, 'reviewApprovalsGranted': 0, 'packetsSent': 0,
        'remainingUnpreparedIdentities': 370, 'remainingUnpreparedByMinimumClassRank': by_rank,
        'remainingUnpreparedSpellIds': sorted(unprepared)})
    dump(navigation[2], coverage)
    index = '\n'.join(['# Prepared spell source conferences', '',
        '**Eleven packets prepared; none sent or approved.** These retain 202 distinct unfinished identities and 210 exact current-book placements. There are 199 mechanical source questions and three unchanged receipts (Blink, Banishment and Veiled Chest) for the post-push cosmology review. Ordinary spell totals remain 276 operational drafts and 572 unfinished identities out of 848.', '',
        '| Source cohort | Identities | Mechanical questions | Post-push receipts | Book bindings | Local source checks |',
        '|---|---:|---:|---:|---:|---:|', *table, '',
        'Every unfinished identity whose minimum class-access rank is0–4 now has source preparation, including all65 at rank4. This does not make those spells selectable or reviewed. The370 pending identities at higher minimum ranks still need preparation. GPT source decisions, authored cards and separate exact review remain necessary.', '',
        'Preserved conflicts include Elemental Drain\'s2/5RP loss, Spell Shield\'s level/Tier wording, both Alignment Anchor placements and the two Confusion/Phantasmal Killer school versions. Recurring Evocation effects retain their Instantaneous metadata as explicit questions.', '',
        'Soulburn Pact retains20HP/up-to3RP in the catalog versus20HP/5RP in Core, alongside the7RP casting cost. Monk and Oracle Shadow Step, and Druid/Ranger Blight mentions, retain distinct class source records. No same-name class feature is silently treated as the ordinary spell.', '',
        'Fabricate keeps both school placements and raises explicit crafting/material/instant-work questions. Spell Theft\'s Fly example has no exact entry in the current catalog, Core or book spell rows; the missing reference is recorded without importing another game\'s spell or substituting Fleeting Flight. Veiled Chest and its possible historical alias are preserved for later cosmology only.', '',
        '| Minimum class-access rank | Pending identities still to prepare |', '|---|---:|',
        *[f'| {rank} | {count} |' for rank, count in by_rank.items()], '',
        'The [coverage manifest](FOCUSED_SPELL_SOURCE_PREPARATION_COVERAGE.json) records exact membership, duplicate checks and protected-input validation. Rebase dependencies before dispatch and preserve prepared revisions. Fishing exact review remains the current notebook request.', ''])
    navigation[1].write_text(index, encoding='utf-8', newline='\n')
    start = navigation[0].read_text(encoding='utf-8')
    old = 'nine unsent cohorts, 176 identities, 183 book bindings, 174 mechanical questions and two post-push receipts (Blink and Banishment)'
    new = 'eleven unsent cohorts, 202 identities, 210 book bindings, 199 mechanical questions and three post-push receipts (Blink, Banishment and Veiled Chest)'
    assert old in start or new in start
    navigation[0].write_text(start.replace(old, new), encoding='utf-8', newline='\n')
    handoff = navigation[3].read_text(encoding='utf-8')
    paragraph = ('### Current prepared spell coverage — ranks zero through four\n\n'
        'The [eleven-packet index](PREPARED_SPELL_SOURCE_INDEX.md) preserves202 distinct pending identities and210 book bindings:199 mechanical questions plus Blink, Banishment and Veiled Chest as unchanged post-push receipts. '
        'All65 pending minimum-rank4 identities now have source preparation. The370 higher-minimum-rank identities remain to prepare. '
        'The latest13 Illusion/Necromancy sources pass11 checks across76 protected inputs, preserving Soulburn Pact\'s3/5RP conflict and four class comparisons. '
        'The13 Transmutation/Universal sources pass12 checks across78 protected inputs, retaining both Fabricate placements and Spell Theft\'s unresolved Fly reference. '
        'All packets remain unsent; source preparation grants no approval. Fishing exact review remains active. The checkpoints below preserve prior progress.\n\n')
    handoff = handoff.replace('### Current prepared spell coverage — nine cohorts', '### Prepared spell coverage checkpoint — nine cohorts')
    if '### Current prepared spell coverage — ranks zero through four' not in handoff:
        assert '## Next prepared source evidence' in handoff
        handoff = handoff.replace('## Next prepared source evidence', '## Next prepared source evidence\n\n' + paragraph, 1)
    navigation[3].write_text(handoff, encoding='utf-8', newline='\n')
    observation = read(navigation[4]); progress = observation.setdefault('independentProgress', {})
    progress.update({'focusedPendingSpellSourcesPrepared': 202, 'preparedSpellCohorts': 11,
        'currentBookBindingsAcrossPreparedSpellPackets': 210, 'prePushSpellQuestionsAcrossPreparedPackets': 199,
        'postPushSpellReceipts': deferred, 'rank4SourcesPrepared': 65, 'rank4SourcesRemaining': 0,
        'allPendingMinimumRankZeroToFourSourcesPrepared': True, 'higherRankUnpreparedSpellIdentities': 370,
        'illusionNecromancyRank4SourcesPrepared': 13, 'transmutationUniversalRank4SourcesPrepared': 13})
    observation['independentProgressUpdatedAtUtc'] = datetime.now(timezone.utc).isoformat()
    observation['currentGoalTurnClassification'] = 'progress:26 further sources prepared; all pending minimum-rank0-4 identities have source evidence; unresolved Fly reference retained and Veiled Chest deferred; active Fishing C verdict still pending'
    observation['consecutiveBlockedGoalTurns'] = 0; dump(navigation[4], observation)
    game_coverage = read(navigation[5])
    for aspect in game_coverage['aspects']:
        if aspect['id'] in ['DD-03', 'DD-11', 'DD-12', 'DD-13', 'DD-18', 'DD-21', 'DD-26', 'DD-35', 'DD-49']:
            for prefix in ['ILLUSION_NECROMANCY_RANK4', 'TRANSMUTATION_UNIVERSAL_RANK4']:
                for key, suffix in [('sourceEvidence', 'PREPARATION.json'), ('draftEvidence', 'AUDIT.md'), ('validationEvidence', 'STATUS.json')]:
                    p = f'docs/audit/2026-10-08/full-game/{prefix}_SOURCE_{suffix}'
                    if p not in aspect.setdefault(key, []): aspect[key].append(p)
        if aspect['id'] == 'DD-12':
            issue = 'Eleven unsent cohorts preserve202 pending identities/210 book bindings:199 mechanical questions and three post-push receipts. All pending minimum-rank0-4 sources are prepared;370 higher-rank sources remain. No new approval;276 operational/572 pending unchanged.'
            if issue not in aspect['openIssues']: aspect['openIssues'].append(issue)
            aspect['currentPreparedSpellSourceCoverage'] = {'identities':202,'bookBindings':210,'mechanicalQuestions':199,'deferredReceipts':deferred,'allPendingMinimumRank0To4Prepared':True,'higherRankSourcesUnprepared':370,'newApprovals':0}
    dump(navigation[5], game_coverage)
    for p in navigation[:2]:
        for link in re.findall(r'\]\(([^)]+)\)', p.read_text(encoding='utf-8')):
            if not re.match(r'^[a-z]+:', link): assert (p.parent / link.split('#')[0]).exists(), (p.name, link)
    receipt = {'status':'PASS complete pending rank0-4 source preparation only','cohorts':11,'identities':202,
        'bookBindings':210,'mechanicalQuestions':199,'deferredReceipts':deferred,'protectedInputsUnchanged':len(protected),
        'rank4IdentitiesPrepared':65,'higherRankIdentitiesUnprepared':370,'higherRanks':by_rank,
        'navigationBackup':backup.relative_to(AUDIT).as_posix(),'sourceInformationDeleted':False,'newApprovals':0,'cosmology':'post-push only'}
    dump(AUDIT / 'RANK4_SOURCE_COVERAGE_NAVIGATION_RECEIPT.json', receipt); print(json.dumps(receipt))


if __name__ == '__main__':
    main()
