"""Record the bounded reader change and observed browser checks, preserving sources."""
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded


def main():
    target = A / 'COSMOLOGY_COMPANION_READER_01_APPLICATION_CHECK.json'
    assert not target.exists()
    before = A / 'companion-before-cosmology-reader-01'
    manifest = json.loads((before / 'PRESERVATION_MANIFEST.json').read_bytes())
    for row in manifest:
        p = G / row['preservedCopy']
        assert info(p)['sha256'] == row['sha256']
    untouched = ['src/data/cosmology-lore.json', 'src/data/dungeon-mechanics.json', 'src/app/page.tsx']
    for rel in untouched:
        assert (R / rel).read_bytes() == (before / rel).read_bytes()
    old = (before / 'src/components/CosmologyViewer.tsx').read_text(encoding='utf-8')
    new = (R / 'src/components/CosmologyViewer.tsx').read_text(encoding='utf-8')
    original_body = old.split('export default function CosmologyViewer() {', 1)[1]
    assert new.split('function OriginalCosmologyReference() {', 1)[1] == original_body
    checks = []
    def check(name, ok):
        checks.append({'name': name, 'passed': bool(ok)})
        assert ok, name
    def dom(suffix):
        return (A / f'COSMOLOGY_COMPANION_READER_01_{suffix}_DOM.txt').read_text(encoding='utf-8')
    for suffix in ['PLAYER', 'RETURN']:
        text = dom(suffix)
        check(suffix + ': player entry and explicit selection', 'Open Director / source reference' in text)
        check(suffix + ': source reader absent', 'Before the story, before echo' not in text and 'button "First Song"' not in text)
        check(suffix + ': public ceiling', 'failed Sixth Gate' in text)
    text = dom('SOURCE')
    check('Source reader opens with review note and return control',
          'Preserved source reference.' in text and 'Return to player cosmology' in text)
    check('Original source body remains accessible', 'Before the story, before echo' in text)
    for suffix in ['TIMELINE_PLAYER', 'TIMELINE_CLOSED', 'RETEST']:
        text = dom(suffix)
        check(suffix + ': qualified dates', '87 AE:' in text and '710 AE:' in text and 'three-year phase mismatch' in text)
        check(suffix + ': original Binding claim not visible', 'An eleventh shard, unnamed and unclaimed' not in text)
    text = dom('TIMELINE_SOURCE')
    check('Timeline originals remain accessible after selection', 'An eleventh shard, unnamed and unclaimed' in text)
    check('Timeline source view carries identity qualification', 'does not establish identity among' in text)
    logs = json.loads((A / 'COSMOLOGY_COMPANION_READER_01_RETEST_LOGS.json').read_bytes())
    check('No new browser warning/error logs in recorded post-fix interval', logs['entries'] == [])
    check('No issues overlay in post-fix observed state', 'Open issues overlay' not in dom('RETEST'))
    for suffix in ['BEFORE', 'AFTER', 'FINAL']:
        check('TypeScript ' + suffix + ' output empty', not (A / f'COSMOLOGY_COMPANION_READER_01_TSC_{suffix}.txt').read_bytes().strip())
    changed = [R / 'src/components/CosmologyReadingNotes.tsx', R / 'src/components/CosmologyViewer.tsx', R / 'src/components/DungeonGuide.tsx']
    record = {
        'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Local player cosmology entry and Myth & Timeline presentation; deliberate source selection; source text preserved.',
        'conference': info(A / 'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_Revised_Addendum_and_Evidence.zip'),
        'conferenceLocation': 'Revised DIRECTOR_COMPANION.md CR-F08; integration request CR-I10',
        'preservationManifest': info(before / 'PRESERVATION_MANIFEST.json'),
        'changedFiles': [info(p) for p in changed],
        'unchangedSourceAndPageFiles': [info(R / rel) for rel in untouched],
        'originalReaderFunctionPreserved': True,
        'observedBrowserChecks': checks,
        'checkCount': len(checks), 'failureCount': 0,
        'typeScript': {'command': 'node <installed typescript>/bin/tsc --noEmit --incremental false',
                       'beforeExitCode': 0, 'afterReaderExitCode': 0, 'finalExitCode': 0},
        'markupFix': 'Existing DraftBadge rendered a div inside p in DungeonGuide. Changed this local badge to an inline span. Fresh reload/Mechanics traversal produced no new warning/error logs and no issues overlay.',
        'diagnostics': [info(A / f'COSMOLOGY_COMPANION_READER_01_{suffix}.json') for suffix in ['DEV_LOGS', 'RETEST_LOGS']],
        'browserEvidence': [info(p) for p in sorted(A.glob('COSMOLOGY_COMPANION_READER_01_*')) if p.suffix in ['.png', '.txt']],
        'preview': {'url': 'http://127.0.0.1:8517/', 'tabClosed': True, 'serverStopped': True},
        'limits': ['This is deliberate reader selection, not authentication or secure access control.',
                   'Other companion tabs and deeper-floor listings were not converted or approved by this change.',
                   'No production build/deployment, full companion regression, human balance or full-game approval.',
                   'No campaign-frame choice, date correction, identity merge or new route rule adopted.'],
        'sourceInformationDeleted': 0, 'newRulesAdopted': False, 'published': False,
    }
    target.write_bytes(encoded(record))
    print(json.dumps({'receipt': info(target), 'checks': len(checks), 'failures': 0}))


if __name__ == '__main__':
    main()
