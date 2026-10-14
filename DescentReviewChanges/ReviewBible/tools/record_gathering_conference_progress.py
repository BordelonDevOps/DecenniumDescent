"""Record actual gathering dispatch and the new spell-source cohort; preserve navigation."""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT.parents[1]
AUDIT = GAME / 'docs/audit/2026-10-08/full-game'


def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def dump(p, value):
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')


def main():
    receipt_path = AUDIT / 'GATHERING_CONFERENCE_AND_EVOCATION5_PROGRESS.json'
    assert not receipt_path.exists()
    navigation = [GAME / 'START_HERE.md', AUDIT / 'PREPARED_SPELL_SOURCE_INDEX.md',
                  AUDIT / 'FOCUSED_SPELL_SOURCE_PREPARATION_COVERAGE.json',
                  AUDIT / 'GPT_REVIEW_CONTINUATION_HANDOFF.md',
                  AUDIT / 'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json',
                  ROOT / 'data/playtest/game_development_coverage.json']
    before = {p.relative_to(GAME).as_posix(): sha(p) for p in navigation}
    backup = AUDIT / 'navigation-before-gathering-conference-and-evocation5'
    assert not backup.exists()
    for p in navigation:
        dest = backup / p.relative_to(GAME)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dest)
    dump(backup / 'MANIFEST.json', before)
    coverage = read(navigation[2])
    assert coverage['distinctPreparedPendingSpellIds'] == 202
    files = coverage['cohortFiles'] + ['EVOCATION_RANK5_SOURCE_PREPARATION.json']
    records, bindings, protected = [], [], {}
    for filename in files:
        data = read(AUDIT / filename)
        status = read(AUDIT / filename.replace('PREPARATION', 'STATUS'))
        assert all(x['pass'] for x in data['checks']) and data['spellsApproved'] == 0
        packet = AUDIT / status['packetFile']
        assert sha(packet) == status['packetSha256']
        records.extend(data['selectedSpells'])
        bindings.extend(data['currentBookBindings'])
        for p, h in data['protectedFiles'].items():
            assert p not in protected or protected[p] == h
            protected[p] = h
    ids = [r['spellId'] for r in records]
    assert len(ids) == len(set(ids)) == 210 and len(bindings) == 219
    assert all(sha(GAME / p) == h for p, h in protected.items())
    catalog = read(ROOT / 'data/public/spell_playtests/catalog.json')['spells']
    pending = {r['id']: r for r in catalog if r['operational'] is None}
    minimum = lambda r: min(v['rank'] for v in r['classAccess'].values())
    unprepared = {i: r for i, r in pending.items() if i not in ids}
    by_rank = dict(sorted(Counter(minimum(r) for r in unprepared.values()).items()))
    assert len(unprepared) == 362 and by_rank[5] == 61 and len(pending) == 572
    coverage.update({'distinctPreparedPendingSpellIds': 210, 'currentBookBindings': 219,
                     'prePushMechanicalQuestions': 207, 'cohortFiles': files,
                     'protectedInputsUnchanged': len(protected),
                     'minimumRank5SourceIdentitiesPrepared': 8,
                     'remainingUnpreparedIdentities': 362,
                     'remainingUnpreparedByMinimumClassRank': by_rank,
                     'remainingUnpreparedSpellIds': sorted(unprepared)})
    dump(navigation[2], coverage)
    index = navigation[1].read_text(encoding='utf-8')
    index = index.replace('Eleven packets prepared', 'Twelve packets prepared').replace(
        '202 distinct unfinished identities and 210 exact current-book placements',
        '210 distinct unfinished identities and 219 exact current-book placements').replace(
        'There are 199 mechanical source questions', 'There are 207 mechanical source questions').replace(
        'The370 pending identities at higher minimum ranks still need preparation.',
        'Eight minimum-rank5 Evocation identities are also prepared;362 higher-rank identities still need preparation.').replace(
        '| 5 | 69 |', '| 5 | 61 |').replace(
        'Fishing exact review remains the current notebook request.',
        'The gathering-tool source conference is the current notebook work; Mining Part B is awaiting its verdict.')
    row = '| [Rank-five Evocation](EVOCATION_RANK5_SOURCE_AUDIT.md) | 8 | 8 | 0 | 9 | 11 |'
    index = index.replace('\n\nEvery unfinished identity', '\n' + row + '\n\nEvery unfinished identity', 1)
    index = index.replace('\n| Minimum class-access rank', '\nSynaptic Static retains both school versions and their different area/penalty wording. Frozen Tomb and Immolation retain their recurring/control durations alongside Instantaneous metadata. Destructive Wave keeps the unresolved thunder/radiant notation. These are source questions, not new mechanics.\n\n| Minimum class-access rank', 1)
    navigation[1].write_text(index, encoding='utf-8', newline='\n')
    paragraph = ('**Current gathering conference:** [Part A](GATHERING_TOOL_PART2_A_CAPTURE.json) was acknowledged in actual reply679b6ea9-7edc-4bba-9b1c-112384e899d4. '
        '[Part B](GATHERING_TOOL_PART2_DISPATCH.json) supplies all43 Mining originals, shared evidence and32 cases; its source verdict is pending. '
        'The [current staged packet](GATHERING_TOOL_PART2_SUBMISSION.json) retains all128 sources/82 book bindings,23 current rule excerpts and82 protected inputs. '
        'Skinning43 and Salvaging42 follow, then a joint source integration pass and separate exact-card review. No gathering card is promoted.\n\n')
    handoff = navigation[3].read_text(encoding='utf-8')
    handoff = handoff.replace('Next: rebase and confer on the128 gathering-tool sources,then167 advanced-trade sources and remaining whole-game systems.',
                              'The gathering-tool source conference is underway; Mining Part B is awaiting its verdict, followed by Skinning and Salvaging.')
    handoff = handoff.replace('### Current prepared spell coverage — ranks zero through four',
                              '### Prepared spell coverage checkpoint — ranks zero through four')
    new_spell = ('### Current prepared spell coverage — twelve cohorts\n\n'
                 'The [source index](PREPARED_SPELL_SOURCE_INDEX.md) now retains210 pending identities and219 exact book bindings:207 mechanical questions and three unchanged post-push receipts. '
                 'All pending minimum-rank0–4 sources and eight rank5 Evocation identities are prepared.362 higher-rank sources remain to prepare, including61 at rank5. '
                 'The new cohort passes11 source checks with73 protected inputs unchanged; the twelve-cohort protected union is unchanged. All spell packets remain unsent and no spell approval is added. Earlier checkpoints below are historical.\n\n')
    handoff = handoff.replace('## Next prepared source evidence', '## Next prepared source evidence\n\n' + paragraph + new_spell, 1)
    navigation[3].write_text(handoff, encoding='utf-8', newline='\n')
    start = navigation[0].read_text(encoding='utf-8')
    start = start.replace('Next: rebase and confer on the128 gathering-tool sources,then167 advanced-trade sources and remaining whole-game systems.',
                          'The [gathering-tool conference](docs/audit/2026-10-08/full-game/GATHERING_TOOL_PART2_DISPATCH.json) is underway: current rules acknowledged; all43 Mining sources sent for a verdict; Skinning and Salvaging follow.')
    start = start.replace('eleven unsent cohorts, 202 identities, 210 book bindings, 199 mechanical questions',
                          'twelve unsent cohorts, 210 identities, 219 book bindings, 207 mechanical questions')
    navigation[0].write_text(start, encoding='utf-8', newline='\n')
    observation = read(navigation[4])
    observation.update({'gatheringSourceConference': {'stage': 'Part B Mining/shared source verdict pending',
                        'threadId': '6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b',
                        'partAAcknowledgement': '679b6ea9-7edc-4bba-9b1c-112384e899d4',
                        'partBTurnId': '40e5360a-7ae5-4116-ab6e-49750c4d3bfd',
                        'recipesApproved': 0},
                        'currentGoalTurnClassification': 'progress: current gathering rules acknowledged; full Mining/shared evidence sent; eight further spell sources prepared',
                        'consecutiveBlockedGoalTurns': 0})
    observation.setdefault('independentProgress', {}).update({
        'focusedPendingSpellSourcesPrepared': 210, 'preparedSpellCohorts': 12,
        'currentBookBindingsAcrossPreparedSpellPackets': 219,
        'prePushSpellQuestionsAcrossPreparedPackets': 207,
        'higherRankUnpreparedSpellIdentities': 362, 'evocationRank5SourcesPrepared': 8})
    observation['independentProgressUpdatedAtUtc'] = datetime.now(timezone.utc).isoformat()
    dump(navigation[4], observation)
    game = read(navigation[5])
    for aspect in game['aspects']:
        if aspect['id'] in ['DD-03', 'DD-11', 'DD-12', 'DD-13', 'DD-18', 'DD-21', 'DD-26', 'DD-35', 'DD-49']:
            for key, suffix in [('sourceEvidence', 'PREPARATION.json'), ('draftEvidence', 'AUDIT.md'), ('validationEvidence', 'STATUS.json')]:
                aspect.setdefault(key, []).append('docs/audit/2026-10-08/full-game/EVOCATION_RANK5_SOURCE_' + suffix)
        if aspect['id'] == 'DD-12':
            retained = []
            for issue in aspect['openIssues']:
                if 'unsent' in issue and ('cohorts' in issue or 'source cohorts' in issue):
                    aspect.setdefault('historicalSourcePreparationCheckpoints', []).append(issue)
                else:
                    retained.append(issue)
            aspect['openIssues'] = retained + ['Twelve unsent cohorts preserve210 pending identities/219 book bindings:207 mechanical questions and three post-push receipts. All minimum-rank0–4 sources and eight rank5 Evocation sources are prepared;362 higher-rank sources remain. No new approval;276 operational/572 pending unchanged.']
            aspect['currentPreparedSpellSourceCoverage'] = {'identities': 210, 'bookBindings': 219,
                'mechanicalQuestions': 207, 'deferredReceipts': coverage['postPushReceiptOnlyIds'],
                'allPendingMinimumRank0To4Prepared': True, 'rank5SourcesPrepared': 8,
                'higherRankSourcesUnprepared': 362, 'newApprovals': 0}
    dump(navigation[5], game)
    # These edits concern navigation, not the protected game rules/source records.
    assert all(sha(GAME / p) == h for p, h in protected.items())
    assert all(sha(backup / p) == h for p, h in before.items())
    receipt = {'status': 'PASS source preservation and current navigation', 'spellCohorts': 12,
               'preparedSpellIdentities': 210, 'bookBindings': 219, 'mechanicalQuestions': 207,
               'spellProtectedInputsUnchanged': len(protected), 'higherRankUnprepared': 362,
               'gatheringSourceConference': observation['gatheringSourceConference'],
               'navigationBackup': backup.relative_to(GAME).as_posix(),
               'newApprovals': 0, 'sourceInformationDeleted': 0, 'githubPushed': False,
               'cosmology': 'post-verified-push only'}
    dump(receipt_path, receipt)
    print(json.dumps(receipt, ensure_ascii=False))


if __name__ == '__main__':
    main()
