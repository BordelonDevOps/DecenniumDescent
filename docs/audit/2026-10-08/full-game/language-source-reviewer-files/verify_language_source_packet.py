#!/usr/bin/env python3
"""Read-only reproduction of LA source equality and declared reference arithmetic.

Python standard library only. Input archive bytes are never modified or extracted.
This is not a gameplay runtime or validation of actual campaign facts.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterator
from zipfile import ZipFile
import xml.etree.ElementTree as ET

EXPECTED_BYTES = 6057633
EXPECTED_SHA = '736b0928dafcd1b0cd46045b4c2466ed780170dac8b5d907bd8fc67c8fc96c0c'
BASE = 'DescentReviewChanges/ReviewBible/'
AUDIT = 'docs/audit/2026-10-08/full-game/'

def dictionaries(value: Any) -> Iterator[dict]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from dictionaries(child)
    elif isinstance(value, list):
        for child in value:
            yield from dictionaries(child)

def run(archive: Path) -> dict:
    raw = archive.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if len(raw) != EXPECTED_BYTES or digest != EXPECTED_SHA:
        raise ValueError('Archive differs from the frozen LA source submission; do not treat results as this review receipt.')
    checks: list[dict] = []
    def check(group: str, name: str, ok: bool) -> None:
        checks.append({'group': group, 'name': name, 'pass': bool(ok)})
    with ZipFile(archive) as z:
        def text(path: str) -> str:
            return z.read(path).decode('utf-8-sig')
        def data(path: str) -> Any:
            return json.loads(text(path))
        manifest = data('FILE_MANIFEST.json')
        for path, expected in manifest.items():
            payload = z.read(path)
            check('payload-integrity', path, len(payload) == expected['bytes'] and hashlib.sha256(payload).hexdigest() == expected['sha256'])
        prep = data(AUDIT + 'LANGUAGE_COMMUNICATION_SOURCE_PREPARATION.json')
        add = data(AUDIT + 'LANGUAGE_ADVANCED_INTERFACE_ADDENDUM.json')
        foundation = data(BASE + 'data/playtest/ancestry_background_candidate.json')
        ancestors = {a['id']: a for a in foundation['ancestries']}
        backgrounds = {b['id']: b for b in foundation['backgrounds']}
        for a in prep['ancestryGrants']:
            current = ancestors.get(a['ancestryId'])
            check('ancestry', a['ancestryId'], current == a['fullCurrentAncestryRecord'])
            for variant in a['fullCurrentAncestryRecord']['variants']:
                check('variant', variant['id'], current is not None and variant in current['variants'])
        for b in prep['backgroundGrants']:
            check('background', b['backgroundId'], backgrounds.get(b['backgroundId']) == b['fullCurrentBackgroundRecord'])
        for c in prep['classComparisonRecords']:
            current = data(c['file'])
            objects = list(dictionaries(current))
            check('class-file', c['class'], hashlib.sha256(z.read(c['file'])).hexdigest() == c['sha256'])
            for card in c['cards']:
                check('class-card', card['id'], card in objects)
            check('class-engine', c['class'], c['engine'] == current.get('engine') and c['engineFieldPresent'] == ('engine' in current))
        chapter = prep['playerLanguageChapter']
        from io import BytesIO
        with ZipFile(BytesIO(z.read(chapter['actualBook']))) as book:
            xml = ET.fromstring(book.read('word/document.xml'))
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        paragraphs = [''.join(t.text or '' for t in p.findall('.//w:t', ns)) for p in xml.findall('.//w:p', ns)]
        for p in chapter['paragraphs']:
            check('book-language', str(p['sourceLine']), all(paragraphs[i] == p['text'] for i in p['actualDocxParagraphs']))
        catalog = {s['id']: s for s in data(BASE + 'data/public/spell_playtests/catalog.json')['spells']}
        for s in prep['spellComparisonRecords']:
            check('selected-spell', s['id'], catalog.get(s['id']) == s)
        internal_path = BASE + 'data/director/advanced_craft_recipe_candidate_internal.json'
        public_path = BASE + 'data/crafting/advanced_craft_recipe_candidate_public.json'
        internal = {c['recipeId']: c for c in data(internal_path)['cards']}
        for c in add['completeScribingCards']:
            check('scribing-card', c['recipeId'], internal.get(c['recipeId']) == c)
        check('advanced-file', 'advanced-internal', hashlib.sha256(z.read(internal_path)).hexdigest() == add['currentInternalCandidateSha256'])
        check('advanced-file', 'advanced-public', hashlib.sha256(z.read(public_path)).hexdigest() == add['currentPublicCandidateSha256'])
        feat_array = json.JSONDecoder().raw_decode(text(BASE + 'src/data/feats.js').split('export const feats = ', 1)[1])[0]
        feats = {f['id']: f for f in feat_array}
        for f in prep['pendingFeatSourceComparisons']:
            check('feat-source', f['id'], feats.get(f['id']) == f)
        lines = text(chapter['sourceFile']).splitlines()
        for a in prep['ancestryGrants']:
            t = a['exactLanguageTrait']
            check('grant-book-line', t['id'], t['text'] in lines[t['sourceLine']-1])
        for b in prep['backgroundGrants']:
            for evidence in b['languageEvidence']:
                check('grant-book-line', b['backgroundId'], lines[evidence['line']-1] == evidence['text'])
        for sid, route in prep['pendingSpellQuestionRouting'].items():
            matching = [d for d in dictionaries(data(route['preparationFile'])) if d.get('spellId') == sid and d.get('questionId') == route['questionId']]
            check('pending-spell-route', sid, len(matching) == 1)
        for alternative in prep['runtimeLanguageAlternatives']:
            check('runtime-alternative-hash', alternative['file'], hashlib.sha256(z.read(alternative['file'])).hexdigest() == alternative['sha256'])

    def tuition_cp(minutes: int) -> int:
        amount = Fraction(minutes, 60) * Fraction(100, 8)
        return (amount.numerator + amount.denominator - 1) // amount.denominator
    calculations = [
        ('full ordinary course hours', 240+40+40, 320),
        ('known matching script course hours', 240+40, 280),
        ('known semantic language full literacy hours', 40+40, 80),
        ('known script literacy increment hours', 40, 40),
        ('full course reference gp', tuition_cp(320*60)//100, 40),
        ('matching-script full course reference gp', tuition_cp(280*60)//100, 35),
        ('forty-minute single invoice cp', tuition_cp(40), 9),
        ('forty-minute interrupted course credit minutes', (40//15)*15, 30),
        ('ninety credited minutes less real Tongues loss', 90-10, 80),
        ('three new one-point studies then Insight passage hours', 3+8, 11),
        ('two prior points then one new study plus passage hours', 1+8, 9),
        ('at Insight cap six additional one point credited', min(6,6+1)-6, 0),
        ('one Insight spend from six', 6-3, 3),
        ('routine 250-word prose translation minutes', max(1, math.ceil(10*250/250)), 10),
        ('routine 251-word prose translation minutes', max(1, math.ceil(10*251/250)), 11),
        ('routine 1-word prose translation minutes', max(1, math.ceil(10*1/250)), 1),
        ('three-second source plus three-second rendition seconds', 3+3, 6),
        ('two High Elf/Imperial direct language additions', sum(v['id'] in ('high-elf','imperial-human') for a in prep['ancestryGrants'] for v in a['fullCurrentAncestryRecord']['variants']), 2),
    ]
    for name, actual, expected in calculations:
        check('reference-arithmetic', name, actual == expected)
    if len(checks) != 460:
        raise ValueError(f'Unexpected coverage count {len(checks)}; expected460')
    return {'archiveSha256': digest, 'count': len(checks),
            'scope': 'Source equality/book binding/route checks and18 declared reference calculations only; no gameplay runtime or human/world-fact verification.',
            'checks': checks, 'failed': [c for c in checks if not c['pass']]}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--output', type=Path, required=True, help='A report path outside the immutable source archive')
    args = parser.parse_args()
    try:
        report = run(args.archive)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        parser.exit(2, f'Validation could not complete: {exc}\n')
    print(f"{report['count']} checks; {len(report['failed'])} failures. {args.output}")
    return 1 if report['failed'] else 0

if __name__ == '__main__':
    raise SystemExit(main())
