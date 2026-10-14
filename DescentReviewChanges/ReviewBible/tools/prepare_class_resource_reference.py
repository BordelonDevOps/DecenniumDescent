"""Stage the complete class-resource handout without changing governing rules."""
from pathlib import Path
import copy
import hashlib
import json
import re
import shutil
from datetime import datetime, timezone

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'
HANDOUT = R / 'docs/playtest/CLASS_RESOURCE_REFERENCE.md'
REPORT = A / 'CLASS_RESOURCE_REFERENCE_SOURCE_CHECK.json'
STAGE = A / 'TEACHING_NAVIGATION_REVIEW_STAGING.json'
QUESTIONS = A / 'TEACHING_NAVIGATION_REVIEW_CHECKLIST.json'
README = A / 'TEACHING_NAVIGATION_REVIEW_README.md'
DATA = R / 'data/playtest/game_development_coverage.json'
HANDOFF = A / 'GPT_REVIEW_CONTINUATION_HANDOFF.md'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def rel(path):
    return path.relative_to(G).as_posix()


def fingerprint(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def slug(text):
    return ''.join(c for c in text.lower() if c.isalnum() or c in '_- ').replace(' ', '-')


def check_files(files, allow_archive_only=False):
    checked = 0
    for name, expected in files.items():
        path = G / name
        if allow_archive_only and name in ('ORIGINAL_SOURCE_V3_FILE_MANIFEST.json', 'README_LOW_RANK_EXACT_V1.md'):
            continue
        assert fingerprint(path) == expected, name
        checked += 1
    return checked


def main():
    assert not REPORT.exists(), 'One-use preparation already completed; inspect saved result.'
    stage = read(STAGE)
    assert stage['draftCount'] == 6 and stage['reviewQuestions'] == 23
    assert not stage['submitted'] and not stage['archiveFrozen']
    assert check_files(stage['sourceFiles']) == 91
    frozen = read(A / 'LOW_RANK_136_EXACT_V1_PREPARATION.json')['manifest']
    assert check_files(frozen, True) == 391
    for p in (HANDOUT, REPORT, STAGE, QUESTIONS, README, DATA, HANDOFF):
        assert rel(p) not in frozen, rel(p)
    backup = A / 'teaching-before-class-resource-reference'
    backup.mkdir(exist_ok=False)
    protected = (STAGE, QUESTIONS, README, DATA, HANDOFF, R / 'docs/mechanics/GAME_DEVELOPMENT_COVERAGE.md')
    for p in protected:
        dest = backup / rel(p)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dest)
    write(backup / 'MANIFEST.json', {rel(p): fingerprint(p) for p in protected})

    text = HANDOUT.read_text(encoding='utf-8')
    classes = ['Bard', 'Cleric', 'Crimson Agent', 'Dragoon', 'Druid', 'Mage', 'Mirrorsage', 'Monk', 'Oracle', 'Paladin', 'Ranger', 'Shaman', 'Soldier', 'Thief', 'Tinker', 'Warrior', 'Wizard']
    for name in classes:
        assert text.count('\n## ' + name + '\n') == 1, name
    links = []
    source_paths = set()
    for reference in re.findall(r'\[[^\]]+\]\(([^)]+)\)', text):
        assert '://' not in reference
        filepart, _, fragment = reference.partition('#')
        target = (HANDOUT.parent / filepart).resolve() if filepart else HANDOUT
        assert target.is_file(), reference
        assert target.is_relative_to(G)
        headings = [slug(h) for h in re.findall(r'^#+ (.+)$', target.read_text(encoding='utf-8-sig'), re.M)]
        if fragment:
            assert headings.count(fragment) == 1, (reference, headings)
        if target != HANDOUT:
            source_paths.add(target)
        links.append({'from': rel(HANDOUT), 'reference': reference, 'target': rel(target), 'headingAnchorVerified': bool(fragment)})

    class_sources = []
    for name in classes:
        stem = name.lower().replace(' ', '-')
        data_path = R / ('data/public/Decennium_Descent_Bard_Playtest_v0_1.json' if name == 'Bard' else f'data/public/class_playtests/{stem}.json')
        source_paths.add(data_path)
        packet = read(data_path)
        class_sources.append({'class': name, 'file': rel(data_path), 'completeCards': len(packet['cards']), 'completeEngineParagraphs': len(packet.get('engine', [])), 'bardEngineInLinkedManuscript': name == 'Bard'})
    assert sum(c['completeCards'] for c in class_sources) == 1223
    for extra in ('GPT_HEALING_REMAINING_CORRECTIONS.md', 'GPT_HEALING_EXTENSIONS_CLOSURE.md', 'CODEX_HEALING_EXTENSIONS_REVIEW.md', 'CROSS_GUIDE_EFFICIENT_RECYCLING_CONFLICT.json'):
        source_paths.add(A / extra)
    sources = {rel(p): fingerprint(p) for p in sorted(source_paths)}
    now = datetime.now(timezone.utc).isoformat()
    report = {
        'status': 'complete-resource-reference-authored-presentation-review-pending',
        'preparedAtUtc': now,
        'draft': rel(HANDOUT), 'draftFingerprint': fingerprint(HANDOUT),
        'classes': class_sources, 'sourceFiles': sources, 'localLinks': links,
        'sourceChecks': {
            'classSectionsPresent': 17, 'fullClassCardsSuppliedForReview': 1223,
            'linkedFilesAndExplicitHeadingsExist': True,
            'paladinWaveUsesExistingCadenceAmendment': True,
            'recyclingConflictRemainsExplicitlyPending': True,
            'all391ActiveExactReviewPayloadsUnchanged': True,
        },
        'limitations': [
            'This check verifies file preservation, coverage and link destinations; it does not prove every editorial paraphrase mechanically equivalent.',
            'The complete handout and governing sources require the bounded joint presentation review.',
            'No rendered anchor-click or human two-lookup usability test was performed.',
            'No gameplay runtime, class acquisition or human balance test was run for this handout.',
        ],
        'newRuleAuthority': False, 'sourceCardsModified': 0,
        'presentationApproved': False, 'runtimeImplemented': False,
        'humanEvidenceAdded': False, 'sourceInformationDeleted': 0,
    }
    write(REPORT, report)

    questions = read(QUESTIONS)
    assert questions['questions'][0]['subject'] == 'All six complete draft files'
    questions['questions'][0]['subject'] = 'All seven complete draft files'
    questions['questions'].extend([
        {'id': 'TE-24', 'subject': 'Class-resource reference — all 17 families', 'question': 'Read the complete new handout against all 17 linked class guides and complete class datasets. Verify resource capacities, earning and spending limits, expiries and recovery, including distinct Base/Arch/Hero gates, Druid reserves, Monk gain windows, Oracle refunds, prepared stocks and Wizard matrix-family history. This is consolidation, not a fresh grant or approval of every optional card.'},
        {'id': 'TE-25', 'subject': 'Class-resource reference — existing amendments and conflicts', 'question': 'Verify that Paladin level-17 Wave uses the already-authored long-rest cadence amendment rather than preserved short-rest card wording, and that Oath/Oathbreaker transitions preserve current resources. Keep TC-RECYCLING-01 for its explicit TE-23 resolution. Identify any other actual conflict with current governing directions instead of silently importing older guide text.'},
        {'id': 'TE-26', 'subject': 'Class-resource reference — shared recovery and records', 'question': 'Check the blank counter fields, current versus maximum values, separate class resources versus merged RP, ordinary-spell strain and actual beneficial-rest eligibility. The 17-class summary is a navigation and tracking aid, not a replacement for full source-specific triggers or all acquired-card limits. Distinguish static heading checks from rendered or human usability evidence.'},
    ])
    questions['candidateFiles'].append(rel(HANDOUT))
    write(QUESTIONS, questions)
    readme = README.read_text(encoding='utf-8')
    assert 'Six complete drafts' in readme and 'for23 exact subjects' in readme
    readme = readme.replace('Six complete drafts', 'Seven complete drafts', 1).replace('and complete character-foundation navigation copy.', 'complete character-foundation navigation copy and all-class resource reference.', 1).replace('for23 exact subjects', 'for26 exact subjects', 1)
    readme += '\nThe class-resource handout covers all17 families and supplies all1223 complete cards with the class guides for context. TE-24–26 review its exact paraphrases, current recovery rules and existing Paladin cadence amendment; no class source is modified. The resource sheet explicitly leaves TC-RECYCLING-01 pending.\n'
    README.write_text(readme, encoding='utf-8')

    stage['draftFiles'].append(rel(HANDOUT))
    stage['draftCount'] = 7
    stage['reviewQuestions'] = 26
    stage['directLinkOccurrences'].extend(links)
    stage['sourceFiles'].update(sources)
    for p in (HANDOUT, REPORT, QUESTIONS, README):
        stage['sourceFiles'][rel(p)] = fingerprint(p)
    stage['sourceFiles'] = dict(sorted(stage['sourceFiles'].items()))
    stage['currentSourceFileCount'] = len(stage['sourceFiles'])
    stage['existingSourceReportsVerified'].append({'report': rel(REPORT), 'allRecordedSourcesUnchanged': True, 'sourceCount': len(sources)})
    stage['classResourceReferenceAddedAtUtc'] = now
    write(STAGE, stage)

    coverage = read(DATA)
    before = copy.deepcopy(coverage)
    n = len(stage['sourceFiles'])
    for row in coverage['aspects']:
        for i, issue in enumerate(row['openIssues']):
            if issue.startswith('Six complete teaching/navigation drafts'):
                row['openIssues'][i] = issue.replace('Six complete', 'Seven complete', 1).replace('and full character-foundation navigation copy.', 'full character-foundation navigation copy and all-class resource reference.', 1).replace('23 explicit review questions and91 complete source files', f'26 explicit review questions and{n} complete source files', 1)
        if row['id'] in ('DD-05', 'DD-61', 'DD-66'):
            row['draftEvidence'].append(rel(HANDOUT))
            row['validationEvidence'].append(rel(REPORT))
            row['openIssues'].append('The complete resource-reference draft consolidates all17 class families, current recovery rules and existing amendments, with full class sources supplied. It awaits bounded joint presentation review under TE-24–26; no new card, runtime behavior or human usability evidence is granted.')
    for old, new in zip(before['aspects'], coverage['aspects']):
        for key in ('acceptanceGate', 'status', 'closure', 'completedScopes', 'humanEvidence', 'completionClass'):
            assert old.get(key) == new.get(key), (old['id'], key)
    write(DATA, coverage)
    handoff = HANDOFF.read_text(encoding='utf-8')
    assert handoff.count('Six complete manuscripts and91 supporting files') == 1
    handoff = handoff.replace('Six complete manuscripts and91 supporting files', f'Seven complete manuscripts and{n} supporting files', 1).replace('[23 exact review questions]', '[26 exact review questions]', 1)
    handoff = handoff.replace('three examples and a full separate character-foundation navigation copy.', 'three examples, a full separate character-foundation navigation copy and the all17-class resource reference.', 1)
    handoff = handoff.replace('**Focused reconciliation pending, TC-RECYCLING-01:**', 'The [class-resource handout](../../../../DescentReviewChanges/ReviewBible/docs/playtest/CLASS_RESOURCE_REFERENCE.md) is complete and unsent. Its [source check](CLASS_RESOURCE_REFERENCE_SOURCE_CHECK.json) supplies all17 full class datasets and linked guides; TE-24–26 cover the consolidation and existing Paladin long-rest Wave amendment. This does not alter any governing source or approve its presentation.\n\n**Focused reconciliation pending, TC-RECYCLING-01:**', 1)
    HANDOFF.write_text(handoff, encoding='utf-8')

    assert check_files(sources) == len(sources)
    assert check_files(stage['sourceFiles']) == n
    assert check_files(frozen, True) == 391
    print(json.dumps({'classes': 17, 'completeSourceCards': 1223, 'referenceSources': len(sources), 'links': len(links), 'stagedDrafts': 7, 'questions': 26, 'stagedFiles': n, 'activeExactPayloadsUnchanged': 391, 'all75AcceptanceStatesUnchanged': True}))


if __name__ == '__main__':
    main()
