"""Preserve exact boss-interface sources and finite unresolved questions.

No creature is tagged, operationalized or rebalanced by this source preparation.
The Known Descent candidate is scanned mechanically; sealed records are excluded.
"""
from pathlib import Path
from datetime import datetime, timezone
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import hashlib, json, re

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'
OUT = A / 'BOSS_INTERFACE_SOURCE_PREPARATION.json'
DOC = A / 'BOSS_INTERFACE_SOURCE_AUDIT.md'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
PATTERN = re.compile(r'\bboss(?:es)?\b|\btenacity\b|\bnonlegendary\b|\blegendary (?:actions?|resistance|defenses?|rules|powers)|\bGate (?:Guardians?|Actions?)\b', re.I)
protected = {}


def rel(p): return p.relative_to(G).as_posix()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def text(p): protected[rel(p)] = sha(p); return p.read_text(encoding='utf-8-sig')
def read(p): return json.loads(text(p))
def dump(p, d): p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
def section(value, heading):
    lines = value.splitlines(); i = lines.index(heading); depth = len(heading) - len(heading.lstrip('#'))
    j = next((k for k in range(i+1, len(lines)) if re.match(r'^#{1,'+str(depth)+r'} ', lines[k])), len(lines))
    return '\n'.join(lines[i:j])


CASES = [
    ('BI-01', 'Explicit creature predicates', 'Define source-qualified boss, Gate Guardian and legendary predicates, their authority and where a Director records them. CR, size, unique name, Tier or dramatic role alone must not silently supply immunities or class exclusions. Resolve actual missing creature properties through the full bestiary conference.'),
    ('BI-02', 'Boss construction authority', 'Reconcile Core Chapter10 phase/objective guidance with the Loop requirement for two phases or a meaningful escalation. Preserve Tier1 one-phase/zero-Gate-Action source and later printed counts; distinguish recommendations from mandatory mechanics. Tier6 unknown/historical fields remain literal deferred receipts.'),
    ('BI-03', 'Phase transitions and ongoing identity', 'Give actual phase thresholds, trigger detection and execution order relative to Core end-round events, current effects, death and simultaneous objectives. A phase change does not silently create a fresh creature, clear conditions/denial history, refill pools or award duplicate loot. Each explicit exception needs a sourced or labeled NEW procedure.'),
    ('BI-04', 'Gate Actions', 'Preserve the source end-round timing and counts0/1/1/1/2 for Tiers1–5. Define each actual action, target legality, cost, order, repeat limits and control/suppression interactions. Reconcile these explicit encounter actions with the shared extra-action cap without deleting the source Tier5 second action or granting unlimited normal turns.'),
    ('BI-05', 'Phase reactions and defenses', 'Define the actual phase-reaction trigger, frequency, resource and interruption window. Determine whether a printed rule uses the ordinary Reaction or an explicit separate budget; the phrase alone grants no complete menu of legendary actions/resistances or imported external-game defaults.'),
    ('BI-06', 'Repeated-tactic adaptation', 'Core says after the same tagged ability affects a Guardian twice in one encounter it gains+2 on saves against that exact tactic unless the party changes setup. Specify affected, exact tactic identity, caster sharing, tag/variant treatment, threshold timing, nonstacking versus renewed gains and what material setup change actually resets. Retain one encounter history across phases and mode changes.'),
    ('BI-07', 'Tenacity trigger and budget', 'Reconcile the Loop first qualifying event per round with actual source immunities, prevention, saves and hard-denial eligibility. Define Stunned/Paralyzed/full-turn-loss coverage, compound effects, simultaneous events and round reset. Gate Guardian may have two uses is not an automatic two-use grant for every Guardian.'),
    ('BI-08', 'Tenacity replacement state', 'Bind the unspecified replacement Staggered to the appropriate exact existing condition authority, preserving current Core/Monk/Warrior distinctions. Define the next-turn expiry through the reviewed clock, forced-movement rider, Guard removal, named cures and independently active sources. Do not merge custom same-name penalties into Core Staggered.'),
    ('BI-09', 'Class and spell denial history', 'Settle whether a Tenacity-converted or otherwise prevented hard denial consumes the source-character/target encounter allowance, using actual applied-effect semantics. Preserve damage and soft riders when a hard rider is barred. Repeated saves, Gate Actions, reactions, phase changes and artificial encounter restarts must not reset the history.'),
    ('BI-10', 'Copying, control and companions', 'Bind Mirrorsage boss exceptions, Oracle nonlegendary-undead eligibility and companion restrictions to explicit creature/source fields. Carry actual INT/CR/type, scripted exceptions, ownership and shared command budgets. A renamed, transformed, copied or summoned creature must not gain unsourced boss powers or evade its actual identity constraints.'),
    ('BI-11', 'Specific immunity and passive guards', 'Map source-specific restrictions on disabling passives, stealing powers, forced movement, damage reflection and execution to actual stat features. Do not invent blanket boss immunity or automatically treat every defense as a dispellable spell. Record which fields each reader/guard uses and what happens when a required field is missing.'),
    ('BI-12', 'Executable encounter examples', 'After authoring the source decisions, supply complete Base/Arch/Hero examples with actual actors, objectives, telegraphs, budgets, phases, control attempts, end-round events and retreat/failure. Preserve current encounter-calibration limits; authored examples and deterministic checks do not certify human balance or Tier6 cosmology.'),
]


def main():
    assert not OUT.exists() and not DOC.exists()
    active = read(A / 'LOW_RANK_SPELL_FILE_HANDOFF_V3_PREPARATION.json')['currentFileHashes']
    assert all(sha(G / p) == h for p, h in active.items())
    core_path = R / 'books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx'
    protected[rel(core_path)] = sha(core_path)
    with ZipFile(core_path) as z: xml = z.read('word/document.xml'); root = ET.fromstring(xml)
    ps = [''.join(t.text or '' for t in p.findall('.//w:t', NS)) for p in root.findall('.//w:p', NS)]
    start = ps.index('10. Bosses, Guardians, and Raid Encounters', 100)
    end = next(i for i in range(start+1, len(ps)) if ps[i].startswith('11. '))
    chapter = [{'paragraphIndex': i, 'exactText': ps[i]} for i in range(start, end)]
    tables = []
    for i, e in enumerate(root.find('w:body', NS)):
        if e.tag != f"{{{NS['w']}}}tbl": continue
        rows = [[[''.join(t.text or '' for t in p.findall('.//w:t', NS)) for p in c.findall('.//w:p', NS)]
                 for c in row.findall('w:tc', NS)] for row in e.findall('w:tr', NS)]
        if rows and rows[0] == [['Tier'], ['Phases'], ['Gate Actions/Round'], ['Required Objectives'], ['Recommended Fail State']]:
            tables.append({'bodyElementIndex': i, 'completeCellParagraphs': rows, 'xmlSha256': hashlib.sha256(ET.tostring(e)).hexdigest()})
    assert len(tables) == 1 and len(tables[0]['completeCellParagraphs']) == 7
    loop_path = R / 'docs/mechanics/GAMEPLAY_LOOP_CANON.md'; loop = text(loop_path)
    loop_boss = section(loop, '### Boss structure')
    condition_path = R / 'docs/mechanics/CONDITIONS_PLAYTEST.md'
    staggered = section(text(condition_path), '## Staggered')
    classes = []; engines = []
    for p in sorted((R / 'data/public/class_playtests').glob('*.json')):
        if p.name == 'manifest.json': continue
        d = read(p)
        for i, s in enumerate(d['engine']):
            if PATTERN.search(s): engines.append({'file': rel(p), 'class': d['class'], 'engineIndex': i, 'exactText': s})
        for c in d['cards']:
            if PATTERN.search(str(c.get('effect', ''))): classes.append({'file': rel(p), 'class': d['class'], 'completeCard': c})
    catalog = read(R / 'data/public/spell_playtests/catalog.json')
    spells = [s for s in catalog['spells'] if PATTERN.search(json.dumps(s['operational'], ensure_ascii=False))]
    known = read(R / 'data/director/bestiary_source_candidate_internal.json')
    stat_records = [r for r in known['records'] if r['statBlock']]
    literal_matches = [{'id': r['id'], 'name': r['name'], 'completeStatBlock': r['statBlock']} for r in stat_records
                       if PATTERN.search(json.dumps(r['statBlock'], ensure_ascii=False))]
    keys = sorted({k for r in stat_records for k in r['statBlock']})
    expedition = read(A / 'EXPEDITION_HAVEN_FLOW_SOURCE_PREPARATION.json')
    # The source object has explicit cases; retain the complete current source
    # as a dependency regardless of its local representation of the case list.
    director = read(A / 'DIRECTOR_TABLECRAFT_SOURCE_PREPARATION.json')
    director_cases = [c for c in director['cases'] if c['id'] in ['DR-07', 'DR-08']]
    guide_names = ['CLASS_PLAYTEST_RULES.md', 'COMBAT_ACTION_PLAYTEST.md', 'CONTROL_STATES_PLAYTEST.md',
        'ENCHANTMENT_CONTROL_INTEGRATION_PLAYTEST.md', 'MONSTER_COMBAT_SCHEMA.md', 'CORE_RESOLUTION_PLAYTEST.md',
        'CREATURE_LIFECYCLE_PLAYTEST.md', 'REMAINING_LIFECYCLE_PLAYTEST.md']
    guides = [{'file': rel(p), 'exactText': text(p), 'sha256': sha(p)} for p in [R / 'docs/mechanics' / n for n in guide_names]]
    control_path = R / 'docs/mechanics/CONTROL_SOURCE_BINDINGS.md'
    binding_lines = text(control_path).splitlines()
    references = [{'line': i+1, 'exactText': s} for i,s in enumerate(binding_lines) if PATTERN.search(s) or 'Custom -1 attacks/-5Speed only; not Core Staggered.' in s]
    counts = {'bookParagraphs': len(chapter), 'completeBossTables': len(tables), 'classCards': len(classes),
        'classEngineReferences': len(engines), 'ordinaryOperationalSpellRecords': len(spells),
        'knownDossiersMechanicallyScanned': len(known['records']), 'statBlocksMechanicallyScanned': len(stat_records),
        'literalBossStatMatches': len(literal_matches), 'questions': len(CASES)}
    result = {'preparedAtUtc': datetime.now(timezone.utc).isoformat(), 'status': 'Prepared source/interface conference; UNSENT; no new rule or creature approval',
        'coverageAreas': ['DD-34', 'DD-18', 'DD-33', 'DD-36'], 'sourceBook': rel(core_path), 'sourceBookSha256': sha(core_path),
        'indexConvention': 'zero-based all w:p including table cells; direct bodyElementIndex for table; all table cell paragraphs retained',
        'completeCoreChapter10': chapter, 'completeCoreBossTable': tables[0],
        'sourceScopeNotes': ['Tier6 Unknown/historical-failure cells are preserved as uninterpreted deferred receipts; no new phases, actions or lore.',
            'The chapter final PvP/hidden-state paragraph is preserved, but no PvP authorization or hidden-state interpretation is inferred by this boss audit.',
            'Core end-round procedure is read through the current reviewed combat guide.'],
        'loopBossSource': {'file': rel(loop_path), 'sha256': sha(loop_path), 'exactText': loop_boss},
        'currentCoreStaggered': {'file': rel(condition_path), 'sha256': sha(condition_path), 'exactText': staggered},
        'completeClassCards': classes, 'classEngineReferences': engines, 'completeOperationalSpellRecords': spells,
        'knownStatBlockScan': {'candidatePath': rel(R / 'data/director/bestiary_source_candidate_internal.json'),
            'recordCount': len(known['records']), 'statBlockCount': len(stat_records), 'statBlockKeys': keys,
            'pattern': PATTERN.pattern, 'literalMatches': literal_matches,
            'scope': 'The66 supplied Known Descent stat blocks only. Does not prove absence from every original source or all707 runtime records. Sealed records were not scanned or interpreted.'},
        'currentBindingReferences': {'file': rel(control_path), 'sha256': sha(control_path), 'lines': references},
        'wholeGoverningGuides': guides, 'directorRelatedCases': director_cases,
        'existingExpeditionCase': 'FL-16 in EXPEDITION_HAVEN_FLOW_SOURCE_PREPARATION.json; existing full source conference remains required',
        'questions': [{'id': i, 'title': t, 'question': q, 'status': 'open; no decision or approval'} for i,t,q in CASES],
        'counts': counts, 'protectedFiles': protected, 'sourceInformationDeleted': 0, 'newRules': 0, 'newApprovals': 0,
        'runtimeChanged': False, 'submitted': False, 'cosmologyReviewed': False}
    assert len(stat_records) == 66 and len(known['records']) == 67
    assert all(sha(G / p) == h for p,h in protected.items())
    assert all(sha(G / p) == h for p,h in active.items())
    result['all342ActiveSpellInputsUnchanged'] = True
    dump(OUT, result)
    lines = ['# Boss interfaces — source reconciliation', '',
        '**Prepared and unsent; no new creature tag, rule or approval.** [Complete sources and questions](BOSS_INTERFACE_SOURCE_PREPARATION.json).', '',
        'Core Chapter10 gives Gate Actions, phase reactions and a+2 saving-throw bonus after the same tagged tactic affects a Guardian twice. '
        'The older gameplay loop separately supplies Tenacity and boss-building guidance. These require an explicit shared procedure alongside current conditions, '
        'hard-denial history and source-specific class restrictions.', '',
        f"This preparation preserves all{len(chapter)} chapter paragraphs and its complete table, {len(classes)} full class cards, "
        f"{len(engines)} class-engine references and {len(spells)} current operational spell records selected by the documented boss-interface terms.", '',
        f"The67 Known Descent dossiers have66 supplied stat blocks. The documented mechanical scan found{len(literal_matches)} literal boss/Tenacity/legendary-interface matches in those stat blocks. "
        'This is a scoped finding, not proof about every original or all707 runtime records. No boss status is inferred from CR, names or size. '
        'Sealed records were not scanned or interpreted.', '',
        'Core Staggered is already defined; Monk/Warrior same-name riders have their own reviewed identities. '
        'The boss replacement must use an explicit binding rather than combining their penalties. '
        'Existing expedition case FL-16 and Director encounter cases remain part of the reconciliation.', '',
        '| Case | Interface | Decision needed |', '|---|---|---|']
    lines += [f'| {i} | {t} | {q} |' for i,t,q in CASES]
    lines += ['', 'Tier6 Unknown/historical cells and incidental setting references remain preserved receipts. '
        'No cosmology interpretation, runtime modification, balancing claim, deletion or spell approval has occurred. '
        'All342 inputs to the live137-spell conference remain unchanged.', '']
    DOC.write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps({'counts': counts, 'protectedInputs': len(protected), 'newRules': 0}, indent=2))


if __name__ == '__main__': main()
