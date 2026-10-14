"""Read-only, bounded numeric data/prose comparison for all recipe identities.

Matching source numbers do not establish playable semantics. Uncompared fields,
data-only numbers and already-reviewed exceptions are explicitly distinguished.
"""
from collections import Counter
from pathlib import Path
import hashlib
import json
import re
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT.parents[1]
AUDIT = GAME / 'docs/audit/2026-10-08/full-game'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def integer(token):
    return {'one': 1, 'two': 2, 'three': 3}.get(token.lower(), int(token) if token.isdigit() else None)


PATTERNS = {
    'armorBonus': r'granting \+(\d+) AC',
    'armorClass': r'\(AC (\d+),',
    'attackBonus': r'with \+(\d+) to attack and damage rolls',
    'damageBonus': r'(?:with|Gain) \+(\d+) to (?:attack and damage rolls|Strength checks and melee damage rolls)',
    'capacityPounds': r'(?:carrying|holding) (\d+) pounds',
    'commandTargets': r'coordinate up to (\d+|one|two|three) constructs',
    'extraYield': r'(?:gain|yields) (\d+) additional (?:unit|usable part)',
    'fishingBonus': r'Grants \+(\d+) to Fishing checks',
    'hitPoints': r', (\d+) HP\)',
    'languageInsight': r'Provides (\d+|one|two|three) Language Insight',
    'miningBonus': r'Grants \+(\d+) to Mining checks',
    'navigationBonus': r'Grants \+(\d+) to navigation, engineering, or research checks',
    'radiusFeet': r'(?:in a (\d+)-foot radius|within (\d+) feet)',
    'rangeFeet': r'within (\d+) feet',
    'recoveryPercent': r'recovers up to (\d+)%',
    'researchBonus': r'(?:grants|and) \+(\d+) to (?:the relevant|research checks|cross-disciplinary research checks|navigation, engineering, or research checks)',
    'salvageBonus': r'Grants \+(\d+) to Salvaging checks',
    'saveDC': r'DC (\d+) ',
    'skillBonus': r'granting \+(\d+) to a related',
    'skinningBonus': r'Grants \+(\d+) to Skinning checks',
    'spellLevel': r'up to (\d+)(?:st|nd|rd|th) level',
    'stealthBonus': r'Gain \+(\d+) to Stealth checks',
    'temporaryHP': r'gain (\d+) temporary hit points',
    'resonanceRestored': r'Restore (\d+) expended Resonance Point',
}
BONUS_PATTERNS = {
    'item_enchantment': r'with a \+(\d+) enhancement',
    'worn_accessory': r'grants \+(\d+) to one ',
    'container': r'(?:grants )?\+(\d+) to checks to (?:secure or retrieve|conceal or organize)',
    'remedy_buff': r'Grants \+(\d+) to saves and checks',
    'rune': r'gain \+(\d+) AC and saving throws',
    'device': r'granting \+(\d+) to one ',
}
SELECTED = set(PATTERNS) | {'bonus', 'charges', 'qualityStep', 'uses', 'languages'}


def compare(recipe, key, value):
    effect, kind = recipe['effects'], recipe['mechanics']['type']
    out = {'field': key, 'dataValue': value}
    if value == 0:
        return out | {'status': 'zero-default; no positive benefit asserted by this field'}
    if kind == 'consumable_buff' and key == 'attackBonus':
        return out | {'status': 'recorded-source-conflict-already-reviewed', 'decisionKey': 'alchemy-strength-checks-not-attack-accuracy'}
    if kind == 'remedy' and key == 'bonus':
        return out | {'status': 'recorded-source-conflict-already-reviewed', 'decisionKey': 'herbalism-antidote-advantage-not-numeric-bonus'}
    if key == 'uses':
        return out | {'status': 'use-count-not-expressed-in-prose', 'note': 'The prose says storing one spell or ritual; storage capacity does not itself specify a one-use consumption rule.'}
    if key == 'languages':
        pattern = r'provides (one|two|three|\d+) Language Insight'
        label_note = 'The number labels Language Insight, not automatic learned languages.'
    elif key == 'charges' and recipe['mechanics'].get('deviceKind') == 'automaton':
        pattern = r'functions for (\d+) encounters? before servicing'
        label_note = 'The data field charges labels encounters before servicing in the prose; per-activation charges cannot be inferred.'
    elif key == 'charges':
        pattern = r'(\d+) charges?'
        label_note = None
    elif key == 'qualityStep':
        pattern = r'(one|two|three|\d+) quality step'
        label_note = None
    elif key == 'bonus':
        pattern = BONUS_PATTERNS.get(kind)
        label_note = ('Container check scopes remain exactly as printed: secure/retrieve and conceal/organize are different tasks. Matching bonus values does not merge them.' if kind == 'container' else None)
    else:
        pattern = PATTERNS.get(key)
        label_note = None
    match = re.search(pattern, effect, re.I) if pattern else None
    if match is None:
        return out | {'status': 'positive-number-not-found-in-corresponding-prose-clause', 'pattern': pattern}
    token = next(v for v in match.groups() if v is not None)
    number = integer(token)
    out |= {'proseValue': number, 'proseSpan': [match.start(), match.end()], 'proseQuote': match.group(0),
            'status': 'number-matches' if number == value else 'number-mismatch'}
    if label_note:
        out['semanticBoundary'] = label_note
    return out


def main():
    source = ROOT / 'data/crafting/Decennium_Descent_Crafting_Bible_v4.json'
    book = GAME / 'books/player/Decennium_Descent_Crafting_Bible_v5_Known_Descent.docx'
    sources = {
        'mechanicalV4': source,
        'internalV4': GAME / 'data/director/Decennium_Descent_Crafting_Bible_v4_Full_Internal.json',
        'v2': GAME / 'DescentReviewChanges/crafting-bible/Decennium_Descent_Crafting_Bible_v2.json',
        'publicRuntime': GAME / 'src/data/crafting-recipes.json',
        'publicV5Book': book,
    }
    before = {p.relative_to(GAME).as_posix(): sha(p) for p in sources.values()}
    recipes = read(source)['recipes']
    variant_rows = {}
    for key, path in sources.items():
        if key == 'publicV5Book':
            continue
        data = read(path)
        variant_rows[key] = {r['id']: r for r in (data if isinstance(data, list) else data['recipes'])}
    catalog = read(ROOT / 'data/director/crafting_recipe_review_catalog.json')
    review_rows = {r['recipeId']: r for r in catalog['recipes']}
    with zipfile.ZipFile(book) as archive:
        doc = ET.fromstring(archive.read('word/document.xml'))
    word = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    ps = [''.join(t.text or '' for t in p.iter(word + 't')) for p in doc.iter(word + 'p')]
    book_index = {}
    for i, text in enumerate(ps):
        m = re.match(r'Formula ID: (recipe-\d+) ', text)
        if m:
            assert m[1] not in book_index
            book_index[m[1]] = i
    book_failures, rows = [], []
    for index, recipe in enumerate(recipes):
        rid = recipe['id']
        binding = None
        if recipe['visibility'] == 'public':
            i = book_index.get(rid)
            if i is None or ps[i - 4] != 'Effect. ' + recipe['effects']:
                book_failures.append(rid)
            else:
                binding = {'formulaIdParagraphIndex': i, 'nameParagraphIndex': i - 5,
                           'effectParagraphIndex': i - 4, 'effectText': ps[i - 4]}
        fields = [compare(recipe, k, v) for k, v in recipe['mechanics'].items()
                  if k in SELECTED and isinstance(v, (int, float)) and not isinstance(v, bool)]
        rows.append({'recipeId': rid, 'name': recipe['name'], 'trade': recipe['skill'],
                     'type': recipe['mechanics']['type'], 'visibility': recipe['visibility'],
                     'sourceRecipeIndex': index, 'sourceEffect': recipe['effects'],
                     'currentPassStatus': review_rows[rid]['status'], 'publicBookBinding': binding,
                     'selectedNumericFields': fields,
                     'uncomparedMechanicsKeys': [k for k in recipe['mechanics'] if k not in {x['field'] for x in fields}]})
    all_fields = [f for row in rows for f in row['selectedNumericFields']]
    candidate_statuses = {'positive-number-not-found-in-corresponding-prose-clause', 'number-mismatch'}
    issues = []
    for row in rows:
        for field in row['selectedNumericFields']:
            if field['status'] not in candidate_statuses:
                continue
            rid = row['recipeId']
            vals = {key: {'value': data[rid]['mechanics'].get(field['field']), 'effect': data[rid]['effects']}
                    for key, data in variant_rows.items() if rid in data}
            issues.append({'recipeId': rid, 'trade': row['trade'], 'name': row['name'], 'visibility': row['visibility'],
                           **field, 'sourceVersions': vals, 'bookEffect': row['publicBookBinding'],
                           'disposition': 'preserve both representations; GPT decision required before operational promotion'})

    resolved = {}
    for trade in ('alchemy', 'herbalism'):
        manifest = ROOT / f'docs/mechanics/{trade.upper()}_REVIEW_STATUS.json'
        review = read(manifest)
        assert review['status'].startswith('REVIEWED')
        assert all(sha(GAME / p) == h for p, h in review['artifactHashes'].items())
        before.update(review['artifactHashes'])
        before[manifest.relative_to(GAME).as_posix()] = sha(manifest)
        data = read(ROOT / f'data/director/{trade}_recipe_candidate_internal.json')
        ids = {'recipe-11', 'recipe-12', 'recipe-16'} if trade == 'alchemy' else {'recipe-200', 'recipe-220', 'recipe-238', 'recipe-646'}
        cards = [c for c in data['cards'] if c['recipeId'] in ids]
        assert len(cards) == len(ids)
        key = 'attackRollBonus' if trade == 'alchemy' else 'numericSaveBonus'
        assert all(c['operational']['effect'][key] == 0 for c in cards)
        resolved[trade] = {'reviewManifest': manifest.relative_to(GAME).as_posix(),
                           'exactReviewTurnId': review['exactReviewTurnId'],
                           'recipeIds': sorted(ids), 'inactiveNumericField': key,
                           'operationalEffects': {c['recipeId']: c['operational']['effect'] for c in cards}}

    controls = {
        'all687IdentitiesIndexed': len(rows) == len({r['recipeId'] for r in rows}) == 687,
        'all433PublicEffectsMatchExactBookParagraphs': not book_failures and sum(r['publicBookBinding'] is not None for r in rows) == 433,
        'bookContainsExactlyPublicFormulaIds': set(book_index) == {r['id'] for r in recipes if r['visibility'] == 'public'},
        'allCurrentEffectsAndMechanicsAgreeAcrossDataVersionsWherePresent': all(
            data[r['id']]['effects'] == r['effects'] and data[r['id']]['mechanics'] == r['mechanics']
            for r in recipes for key, data in variant_rows.items() if r['id'] in data),
        'knownSevenReviewedExceptionsRemainInactiveInTheirExactReviewedProjection': sum(len(v['recipeIds']) for v in resolved.values()) == 7,
        'originalAndReviewedArtifactHashesUnchanged': all(sha(GAME / p) == h for p, h in before.items()),
    }
    assert all(controls.values()), controls
    by_trade = []
    for trade in sorted({r['trade'] for r in rows}):
        subset = [r for r in rows if r['trade'] == trade]
        by_trade.append({'trade': trade, 'recipes': len(subset), 'public': sum(r['visibility'] == 'public' for r in subset),
                         'selectedNumericFields': sum(len(r['selectedNumericFields']) for r in subset),
                         'unresolvedNumericProseFindings': sum(i['trade'] == trade for i in issues)})
    report = {'status': 'SOURCE COMPARISON ONLY; unresolved findings are not approved rule changes',
              'scope': 'All 687 identities and 433 public effect paragraphs; only listed numeric-field patterns are compared. Matching numbers do not establish scope, actions, targets, clocks, balance, runtime or complete recipe semantics.',
              'sourceHashes': before, 'controls': controls, 'bookEffectFailures': book_failures,
              'fieldPatterns': PATTERNS, 'bonusPatternsByType': BONUS_PATTERNS,
              'selectedFieldStatusCounts': dict(Counter(f['status'] for f in all_fields)),
              'uncomparedFieldCounts': dict(Counter(k for row in rows for k in row['uncomparedMechanicsKeys'])),
              'typeCounts': dict(Counter(r['type'] for r in rows)), 'trades': by_trade,
              'unresolvedNumericProseFindings': issues, 'alreadyReviewedExceptions': resolved, 'recipes': rows,
              'noSourceEdits': True, 'noRecipePromotions': True, 'cosmologyReview': 'deferred until after verified push; original labels retained without interpretation'}
    path = AUDIT / 'CRAFTING_EFFECT_FIELD_AUDIT.json'
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    write_review_documents(report, recipes, path)
    print(json.dumps({'recipes': len(rows), 'publicBookBindings': len(book_index), 'selectedNumericFields': len(all_fields),
                      'statuses': report['selectedFieldStatusCounts'], 'issues': len(issues),
                      'issuesByTrade': dict(Counter(x['trade'] for x in issues)), 'issuesByField': dict(Counter(x['field'] for x in issues))}))


def write_review_documents(report, source_recipes, report_path):
    """Emit audit explanation and an unsent focused conference, not new rules."""
    issues = report['unresolvedNumericProseFindings']
    counts = report['selectedFieldStatusCounts']
    source_by_id = {r['id']: r for r in source_recipes}
    uses = [r for r in report['recipes'] if any(
        f['status'] == 'use-count-not-expressed-in-prose' for f in r['selectedNumericFields'])]
    boundaries = [r for r in report['recipes'] if any('semanticBoundary' in f for f in r['selectedNumericFields'])]
    lines = [
        '# Crafting effect-field source audit', '',
        'Status: local source comparison only. The focused GPT conference is prepared but **not sent**. No formula, source text or reviewed operational rule was changed.', '',
        'The audit indexes all **687 recipe identities across 16 trades** and binds all **433 public effects** to exact paragraphs in the V5 player crafting book. It inspects 1,268 selected numeric fields, distinguishing corresponding prose matches, omissions, prior decisions and fields not compared. This is a bounded comparison, not a complete semantic or playability review.', '',
        '| Selected field result | Count |', '|---|---:|',
        f"| Same number in the corresponding prose clause | {counts['number-matches']} |",
        f"| Zero-valued fields retained; no prose comparison performed | {counts['zero-default; no positive benefit asserted by this field']} |",
        f"| Source discrepancies already settled by recorded exact reviews | {counts['recorded-source-conflict-already-reviewed']} |",
        f"| Positive data values with no corresponding prose benefit | {len(issues)} |",
        f'| Scribing use counts without a prose consumption rule | {len(uses)} |', '',
        '## Unresolved source omissions', '',
        'The 36 findings cover seven public, four restricted and 25 Director-only formulas. All retain the same effect and mechanics in the mechanical V4, full-internal V4 and V2 data. The seven public variants also match public runtime data and actual V5 book paragraphs. Thus these are preserved source disagreements; selecting a different copy does not resolve them.', '',
        '| Trade | Field | Count | Exact recipe IDs |', '|---|---|---:|---|',
    ]
    for trade in ('Leatherworking', 'Mining', 'Skinning'):
        group = [i for i in issues if i['trade'] == trade]
        lines.append(f"| {trade} | `{group[0]['field']}` | {len(group)} | " + ', '.join(i['recipeId'] for i in group) + ' |')
    lines.extend([
        '',
        'Leatherworking has eight +1 and three +2 armorBonus values omitted from effects that describe mobility/handling benefits and, for some formulas, resistance. These are the same eleven findings already recorded in the Leatherworking conference preparation, not eleven additional cases.', '',
        'Mining and Skinning contribute **25 additional findings**. Their data records extraYield: 1, while the prose grants +2 to the relevant check and one quality step on a successful harvest. Quality and quantity remain distinct. The audit neither grants a free extra unit nor deletes the data value. Higher-tier clauses that explicitly grant two additional units/parts on a critical success are not these omissions.', '',
        '## Existing decisions remain in force', '',
        'Alchemy recipes 11, 12 and 16 retain source attackBonus: 1, but their exact-reviewed operational effects give Strength-check and melee-damage bonuses with attackRollBonus: 0. Herbalism recipes 200, 220, 238 and 646 retain source numeric bonus fields, while their exact-reviewed operational effects use poison-save advantage and numericSaveBonus: 0. The audit verifies both review manifests, the artifact hashes and all seven actual operational projections. It does not reopen these decisions.', '',
        '## Operational questions distinguished from numeric conflicts', '',
        '- All 22 Scribing script formulas have uses: 1. Storing one spell or ritual describes capacity; it does not alone define consumption, activation or access. These 15 public and seven Director-only formulas need a source conference before a usable procedure can be authored.',
        '- Eighteen Tinkering automatons use the field charges for the prose count of encounters before servicing. Matching those numbers does not turn them into per-activation charges or define encounter boundaries and servicing.',
        '- Twenty-four Leatherworking containers grant secure/retrieve-check bonuses; five Tailoring containers grant conceal/organize-check bonuses. Both sets have matching capacity/bonus numbers, but their task scopes remain distinct. Neither number comparison resolves physical capacity, carried weight relief, nesting, Load or custody.',
        '- Two Scribing reference records use languages: 1 for prose that grants one Language Insight. This is not automatically one learned language.', '',
        'All unexamined mechanics keys are listed per recipe in the JSON report. Dice expressions, duration strings, resistance, triggers, targets, material tags and other text were not semantically adjudicated. Zero-valued fields were retained without a prose comparison. No matching number establishes action economy, eligibility, clocks, stacking, balance or runtime readiness. Existing cosmology-related labels are retained without interpretation; cosmology review remains after verified GitHub delivery.', '',
        '## Evidence and reproducibility', '',
        '- [Machine-readable comparison](CRAFTING_EFFECT_FIELD_AUDIT.json): every identity, selected field result, source-version evidence, public book paragraph binding and hash.',
        '- [Prepared focused conference](CODEX_CRAFTING_EFFECT_CONFLICT_CONFERENCE_PREPARED.txt): actual relevant source text, full mechanics objects, unresolved questions and existing decision evidence. This is not a complete recipe-authoring packet and has not been sent.',
        '- [Preparation status](CRAFTING_EFFECT_CONFLICT_CONFERENCE_STATUS.json): prepared packet hash, comparison controls and explicit no-promotion status.',
        '- Reproduce with `DescentReviewChanges/ReviewBible/tools/audit_crafting_effect_fields.py`.', '',
        'Six source controls pass. These check identity coverage, exact public book bindings, agreement among stored data variants, retained prior decisions and unchanged source/reviewed-artifact hashes. The comparison does not approve the unresolved findings. Current-pass totals remain 175 reviewed recipes, 512 remaining and 43 drafted Blacksmithing recipes awaiting an exact verdict.', '',
    ])
    (AUDIT / 'CRAFTING_EFFECT_FIELD_AUDIT.md').write_text('\n'.join(lines), encoding='utf-8')

    def context(rid):
        r = source_by_id[rid]
        return {k: r[k] for k in ('id', 'name', 'skill', 'visibility', 'effects', 'mechanics')}

    packet = [
        'Prepared focused source-conflict conference — NOT SENT', '',
        'Purpose: discuss data/prose disagreements across the retained crafting catalog. This does not request full operational approval of these formulas. All originals remain preserved; no source precedence or extra benefit is inferred from this audit.',
        'The owner requires joint discussion of consequential mechanics. Preserve all source information. Cosmology is deliberately deferred until after the authorized GitHub push and remote-commit verification.',
        'All 687 identities are indexed; all 433 public effects match exact V5 book paragraphs. The 1,268 selected numeric fields yield 1,057 matching numbers, 146 retained zero values not compared to prose, seven already-reviewed discrepancies, 36 unresolved omissions and 22 Scribing use-count questions. The same effects/mechanics are present across V4 mechanical, V4 full internal and V2; public runtime entries also agree where present.', '',
        'Decision questions (no answer presumed):',
        '1. Leatherworking: resolve the eleven omitted armorBonus fields consistently with their actual source effects, body profiles, slots and pending Leatherworking source conference. Do not treat source labels as permission to add AC. The existing prepared Leatherworking conference carries the full source records and interface scenarios.',
        '2. Mining and Skinning: resolve extraYield: 1 in the 25 below formulas whose prose grants only a check bonus and one quality step. Keep yield and quality separate. If a retained benefit needs an operational overlay, define its trigger, quantity, duration, stacking and exact eligible harvest, preserving the original source record.',
        '3. Scribing: confirm how uses: 1 relates to storage and consumption, and list the activation/access dependencies needed before full cards can be authored. Spell/ritual level alone does not grant access, waive a cost, or supply a spell.',
        '4. Confirm the semantic boundaries for automaton encounter counts, distinct container task scopes and Language Insight; identify further source evidence needed. Matching numeric values is not a complete review.',
        '5. Keep the seven already exact-reviewed Alchemy/Herbalism resolutions below unless a concrete new conflict warrants a separately recorded change. No such new conflict is asserted here.', '',
        'UNRESOLVED NUMERIC OMISSIONS: actual effect, full mechanics object and per-copy evidence',
        json.dumps([{'sourceContext': context(i['recipeId']), 'finding': i} for i in issues], ensure_ascii=False, indent=2), '',
        'SCRIBING USE-COUNT QUESTIONS: actual source effects and full mechanics',
        json.dumps([{'sourceContext': context(r['recipeId']), 'publicBookBinding': r['publicBookBinding'],
                     'useField': [f for f in r['selectedNumericFields'] if f['field'] == 'uses']} for r in uses], ensure_ascii=False, indent=2), '',
        'NUMERIC MATCHES WITH DISTINCT SEMANTICS: actual source effects and full mechanics',
        json.dumps([{'sourceContext': context(r['recipeId']),
                     'boundaries': [f for f in r['selectedNumericFields'] if 'semanticBoundary' in f]} for r in boundaries], ensure_ascii=False, indent=2), '',
        'EXISTING EXACT-REVIEW DECISIONS: actual manifests, turns and operational effects',
        json.dumps(report['alreadyReviewedExceptions'], ensure_ascii=False, indent=2), '',
        'SOURCE HASHES AND CONTROLS',
        json.dumps({'sourceHashes': report['sourceHashes'], 'controls': report['controls'],
                    'uncomparedFieldCounts': report['uncomparedFieldCounts']}, ensure_ascii=False, indent=2), '',
        'No recipe promotion, source deletion, GitHub delivery or cosmology review is established by this packet. Blacksmithing exact review remains pending. This focused packet itself has not been submitted.', '',
    ]
    packet_path = AUDIT / 'CODEX_CRAFTING_EFFECT_CONFLICT_CONFERENCE_PREPARED.txt'
    packet_path.write_text('\n'.join(packet), encoding='utf-8')
    status = {'status': 'PREPARED_NOT_SENT', 'sent': False, 'reviewVerdict': None,
              'packet': packet_path.relative_to(GAME).as_posix(), 'packetSha256': sha(packet_path),
              'packetCharacters': len(packet_path.read_text(encoding='utf-8')),
              'sourceComparison': report_path.relative_to(GAME).as_posix(), 'sourceComparisonSha256': sha(report_path),
              'sourceControls': report['controls'], 'unresolvedNumericOmissions': len(issues),
              'separateScribingUseQuestions': len(uses), 'previouslyReviewedExceptions': 7,
              'noSourceEdits': True, 'noRecipePromotions': True, 'cosmologyDeferred': True}
    (AUDIT / 'CRAFTING_EFFECT_CONFLICT_CONFERENCE_STATUS.json').write_text(
        json.dumps(status, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
