"""Render the curated condition overlay while verifying exact Core provenance."""
from pathlib import Path
import json
import hashlib
from zipfile import ZipFile
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]


def main():
    source = json.loads((ROOT / 'data/playtest/core_condition_sources.json').read_text(encoding='utf-8'))
    packet = json.loads((ROOT / 'data/playtest/condition_playtests.json').read_text(encoding='utf-8'))
    originals = {entry['name']: entry for entry in source['conditions']}
    book = ROOT.parents[1] / source['source']
    assert hashlib.sha256(book.read_bytes()).hexdigest() == source['sha256'], 'Approved Core source changed'
    namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    with ZipFile(book) as archive:
        tree = ElementTree.fromstring(archive.read('word/document.xml'))
    paragraphs = [''.join(t.text or '' for t in p.findall('.//w:t', namespace))
                  for p in tree.findall('.//w:p', namespace)]
    conditions = packet['conditions']
    assert len(conditions) == len(originals) == 28
    assert len({c['id'] for c in conditions}) == 28
    assert {c['name'] for c in conditions} == set(originals)
    for condition in conditions:
        assert condition['coreText'] == originals[condition['name']]['sourceText'], condition['name']
        assert condition['source']['path'] == source['source']
        assert condition['source']['sha256'] == source['sha256']
        assert condition['source']['paragraph'] == originals[condition['name']]['paragraph']
        assert condition['source']['textParagraph'] == originals[condition['name']]['textParagraph']
        assert paragraphs[condition['source']['paragraph']] == condition['name']
        assert paragraphs[condition['source']['textParagraph']] == condition['coreText']
        for field in ('effect', 'application', 'durationAndEnding', 'stacking', 'immunitiesAndOverrides'):
            assert condition[field].strip(), (condition['id'], field)
    lines = ['# Conditions — integrated playtest reference', '',
             '**Status:** '+packet['status']+'. '+packet['scope'], '',
             '[Core resolution and Wounds](CORE_RESOLUTION_PLAYTEST.md) · [Recovery and exposure procedures](CONDITION_RECOVERY_PLAYTEST.md) · [Custom rider bindings](CUSTOM_CONDITION_BINDINGS.md) · [Development coverage](GAME_DEVELOPMENT_COVERAGE.md)', '',
             'The Core catalog contains all 28 conditions. The older shared class reference listed 15 of them; that was a reference omission, not lost source data. This overlay supplies the complete reference without modifying the books or that preserved class file.', '',
             '## Shared handling', '']
    for rule in packet['sharedRules']:
        lines += [rule, '']
    lines += ['## Quick index', '', '| Condition | Configuration |', '|---|---|']
    for c in conditions:
        lines.append(f"| [{c['name']}](#{c['id']}) | {c['configuration']} |")
    for c in conditions:
        lines += ['', f"<a id=\"{c['id']}\"></a>", f"## {c['name']}", '',
                  '**Preserved Core text:** '+c['coreText'], '', '**Effect:** '+c['effect'], '',
                  '**Application:** '+c['application'], '', '**Duration and ending:** '+c['durationAndEnding'], '',
                  '**Stacking:** '+c['stacking'], '', '**Immunities and specific exceptions:** '+c['immunitiesAndOverrides'], '']
        for label, field in [('Compatible V6/source details', 'compatibleV6Details'), ('Source conflicts', 'sourceConflicts'), ('Explicit integration decisions', 'provisionalDecisions'), ('Remaining wider integration work', 'openDependencies')]:
            if c[field]:
                lines += ['**'+label+':**', ''] + ['- '+s for s in c[field]] + ['']
        lines += [f"Provenance: Core V2 `{c['source']['path']}`, zero-based all-XML heading paragraph {c['source']['paragraph']}, definition paragraph {c['source']['textParagraph']}; both positions, exact text and book SHA-256 are verified against the approved book and retained in the [condition data](../../data/playtest/condition_playtests.json).", '']
    lines += ['## Verification limits', '',
              '`tools/condition_playtest_rules.py` computes selected action restrictions, attack modifiers, Exhaustion maximum HP/Speed, Corrupted healing, Petrified resistance and Prone movement. It does not decide legal applications, actual visibility, immunities, all source durations, treatment inventory or every spell/class interaction. Run `tools/validate_condition_playtests.py` for scoped regression evidence. An absent automated helper does not make a written table procedure absent, and a passing helper test does not prove game-wide balance.', '']
    (ROOT / 'docs/mechanics/CONDITIONS_PLAYTEST.md').write_text('\n'.join(lines), encoding='utf-8')
    report = {'status': 'PASS', 'source': source['source'], 'sha256': source['sha256'],
              'conditionCount': len(conditions), 'exactHeadingsVerified': len(conditions),
              'exactDefinitionsVerified': len(conditions),
              'paragraphConvention': 'Zero-based all w:p descendants: paragraph is the heading, textParagraph is its following definition.',
              'note': 'Earlier raw conference snapshots retained heading indexes next to quoted definition text. No original quote changed; the clarified positions are now verified directly against the unchanged approved book.'}
    (ROOT.parents[1] / 'docs/audit/2026-10-08/full-game/CONDITION_SOURCE_QUOTE_VALIDATION.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print('PASS: 28 unique condition entries; exact Core text and provenance retained; reference rendered')


if __name__ == '__main__':
    main()
