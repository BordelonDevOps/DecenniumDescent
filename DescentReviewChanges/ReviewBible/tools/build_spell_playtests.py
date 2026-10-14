"""Build a provisional spell layer; never overwrite the approved catalog or Core V2."""
from pathlib import Path
import collections
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT.parents[1] / 'docs/audit/2026-10-08/spell-integration'
OUT = ROOT / 'data/public/spell_playtests'
DOC = ROOT / 'docs/mechanics'
DRAFT = ROOT / 'data/playtest/spell_drafts'
SOURCE = ROOT / 'data/playtest/spell_sources'
CATALOG_PATH = ROOT / 'src/data/spells.js'
CORE_PATH = ROOT / 'data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json'
FIELDS = ['activation', 'rangeFeet', 'targets', 'duration', 'concentration', 'components',
          'resolution', 'effect', 'scaling', 'limitations', 'designNotes']
ALIASES = {
    'resonance-kindle': 'Mana Kindle', 'resonance-furnace': 'Mana Furnace',
    'scorching-line': "Aganazzar's Scorcher", 'snowball-swarm': "Snilloc's Snowball Swarm",
    'acid-arrow': "Melf's Acid Arrow", 'horrid-wilting': "Abi-Dalzim's Horrid Wilting",
    'uncontrollable-laughter': "Tasha's Hideous Laughter", 'resonance-tether': 'Mana Tether',
    'harmonic-bulwark': 'Mana Shield', 'veiled-chest': "Leomund's Secret Chest",
    'concordant-mindlink': "Rary's Telepathic Bond",
}


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_catalog():
    text = CATALOG_PATH.read_text(encoding='utf-8')
    return json.JSONDecoder().raw_decode(text.split('export const SPELLS = ', 1)[1])[0]


def load_drafts():
    drafts = {}
    for path in sorted(DRAFT.glob('batch_*.json')):
        for row in read(path)['spells']:
            assert row['id'] not in drafts, ('duplicate draft', row['id'])
            assert all(field in row for field in FIELDS), ('missing draft fields', row['id'])
            drafts[row['id']] = dict(row, authoringFile=path.relative_to(ROOT).as_posix())
    return drafts


def main():
    source = source_catalog()
    core = read(CORE_PATH)
    drafts = load_drafts()
    assert set(drafts) <= set(source), 'Draft introduced an unknown spell ID'
    progression = read(ROOT / 'data/playtest/class_sources/supplements.json')['class-spell-progression']['CLASS_SPELL_PROGRESSION']
    groups = read(DRAFT / 'selected_sources.json')
    for folder in [AUDIT, OUT, SOURCE]:
        folder.mkdir(parents=True, exist_ok=True)
    dump(SOURCE / 'catalog.json', source)
    dump(SOURCE / 'core_v2_spells.json', core['spells'])
    sources = [CATALOG_PATH, CORE_PATH, ROOT / 'src/data/class-spell-progression.js',
               ROOT / 'docs/mechanics/CLASS_PLAYTEST_RULES.md']
    ledger = [{'path':p.relative_to(ROOT).as_posix(), 'sha256':sha(p)} for p in sources]
    # Capture once: later runs detect source changes rather than silently blessing them.
    if not (SOURCE / 'source_hashes.json').exists():
        dump(SOURCE / 'source_hashes.json', ledger)
    assert read(SOURCE / 'source_hashes.json') == ledger, 'Source changed: review and version before rebuilding'
    entries = []
    for key, original in source.items():
        matches = [(i, x) for i, x in enumerate(core['spells'])
                   if x['name'].casefold() == original['name'].casefold()]
        aliases = [(i, x) for i, x in enumerate(core['spells'])
                   if key in ALIASES and x['name'] == ALIASES[key]]
        draft = drafts.get(key)
        access = {cls: {'rank':rank, 'minimumClassLevel':original['classLearnLevels'][cls],
                        'school':original['classSchools'][cls], 'baseRpCost':core['resonance_costs'][str(rank)]}
                  for cls, rank in original['classRanks'].items()}
        row = {
            'id':key, 'name':original['name'], 'schools':original['schools'],
            'status':'operational-playtest-draft' if draft else 'blocked-pending-operational-review',
            'visibility':'public-source-review', 'classAccess':access,
            'operational':draft,
            'additionalRpCost':1 if key == 'resonance-shield' else 0,
            'source':{'catalogPath':sources[0].relative_to(ROOT).as_posix(),
                      'catalogSha256':ledger[0]['sha256'], 'catalogKey':key,
                      'original':original, 'corePath':sources[1].relative_to(ROOT).as_posix(),
                      'coreSha256':ledger[1]['sha256'],
                      'coreEntries':[{'index':i, 'original':x} for i, x in matches],
                      'possibleHistoricalAliases':[{'index':i, 'original':x} for i, x in aliases]},
            'reviewFlags':[],
        }
        if not matches:
            row['reviewFlags'].append('Core V2 name differs; possible alias retained for comparison, not an automatic rules merge')
        if len(set(original['classRanks'].values())) > 1:
            row['reviewFlags'].append('Class-specific ranks differ; never use global minimum rank for every class')
        if any(x['resolution'] in ['Automatic or opposed as described', 'Appropriate saving throw'] for _, x in matches):
            row['reviewFlags'].append('Core resolution requires an explicit operational interpretation')
        if not draft:
            row['reviewFlags'].append('Not selectable in this spell playtest packet until individual operational review')
        entries.append(row)
    packet = {'schemaVersion':'1.0', 'version':'0.1', 'status':'PARTIAL-DEVELOPMENT-NOT-CANON',
              'scope':'All source records accounted for; operational status applies only to individually drafted entries.',
              'costByRank':core['resonance_costs'], 'classProgression':progression, 'spells':entries}
    dump(OUT / 'catalog.json', packet)
    dump(OUT / 'incomplete_queue.json', [{'id':r['id'], 'name':r['name'], 'schools':r['schools'],
          'lowestSourceRank':min(p['level'] for p in r['source']['original']['placements']),
          'priority':'early-rank' if min(p['level'] for p in r['source']['original']['placements']) <= 3 else 'later-rank',
          'reviewFlags':r['reviewFlags']} for r in entries if not r['operational']])
    bindings, mentions = class_references(entries)
    dump(OUT / 'class_spell_bindings.json', bindings)
    dump(OUT / 'class_name_mentions_for_review.json', mentions)
    summary = {'sourceSpells':len(source), 'sourcePlacements':sum(len(s['placements']) for s in source.values()),
               'coreEntries':len(core['spells']), 'operationalDrafts':len(drafts), 'blocked':len(source)-len(drafts),
               'catalogFieldsUnspecified':{k:sum(s[k]=='Not specified in current rulebook' for s in source.values())
                                           for k in ['castingTime','range','components','duration']},
               'coreGenericResolutions':sum(x['resolution']=='Automatic or opposed as described' for x in core['spells']),
               'exactCoreNameMatches':sum(bool(r['source']['coreEntries']) for r in entries),
               'possibleAliasRecords':sum(bool(r['source']['possibleHistoricalAliases']) for r in entries),
               'classSpellCards':len(bindings), 'textualMentionCandidates':len(mentions),
               'sourceHashes':ledger, 'status':'IN PROGRESS; source accounting does not mean spell completion'}
    dump(OUT / 'manifest.json', summary)
    render(entries, groups, summary)
    print(f"Accounted {len(source)} spells / {summary['sourcePlacements']} placements; {len(drafts)} operational drafts, {len(source)-len(drafts)} blocked")


def class_references(entries):
    bindings, mentions = [], []
    patterns = [(spell,re.compile(r'(?<![\w])' + re.escape(spell['name']) + r'(?![\w])')) for spell in entries]
    for path in sorted((ROOT / 'data/public/class_playtests').glob('*.json')):
        if path.name == 'manifest.json':
            continue
        packet = read(path)
        cls = packet['class']
        for card in packet['cards']:
            if card.get('spellRank') is not None:
                same = [s['id'] for s in entries if s['name'].casefold() == card['name'].casefold()]
                bindings.append({'class':cls, 'cardId':card['id'], 'name':card['name'],
                                 'rank':card['spellRank'], 'status':'operational-class-card',
                                 'authority':path.relative_to(ROOT).as_posix(),
                                 'sameNameCatalogIds':same,
                                 'rule':'Use the class card and its printed cost; name overlap grants no second ordinary spell.'})
        texts = [('engine', '\n'.join(packet['engine']))] + [(c['id'], c['effect']) for c in packet['cards']]
        for location, text in texts:
            for spell, pattern in patterns:
                # Case-sensitive names limit ordinary-noun false positives, but every result remains a candidate.
                if pattern.search(text):
                    mentions.append({'class':cls, 'location':location, 'spellId':spell['id'],
                                     'spellStatus':spell['status'], 'status':'semantic-review-required',
                                     'rule':'Textual mention only, not proof of a spell grant or executable dependency.'})
    return bindings, mentions


def render(entries, groups, summary):
    by_id = {s['id']:s for s in entries}
    lines = ['# Ordinary spells — first playtest packet', '',
             '**Provisional spell development.** This packet adds individual operational specifications to preserved source spells. '
             'It does not replace the approved books or live companion catalog.', '',
             '[Development roadmap](DEVELOPMENT_ROADMAP.md) · [Spell integration rules](SPELL_INTEGRATION_RULES.md) · '
             '[All classes](CLASS_PLAYTEST_INDEX.md) · [Data](../../data/public/spell_playtests/catalog.json) · '
             '[Unfinished queue](../../data/public/spell_playtests/incomplete_queue.json)', '',
             f"**{summary['operationalDrafts']} drafted spells; {summary['blocked']} still awaiting operational review.** "
             f"All {summary['sourceSpells']} source IDs and {summary['sourcePlacements']} placements are retained.",
             '', 'Counts refer to stable spell identities, not closure of every source variant. '
             '[Unassigned variant register](SPELL_VARIANT_REVIEW_STATUS.json) preserves separately unfinished placement decisions.',
             '', 'A catalog record alone is not a playable spell. Only entries marked operational in this packet are available '
             'for this test configuration. Class spell cards remain usable under their own printed rules. '
             'Known/prepared counts, school access and class-level gates still apply.', '',
             '## Source reconciliation', '',
             'The companion catalog leaves four fields unspecified for every spell. Core V2 does supply additional blocks, '
             f"but {summary['coreGenericResolutions']} of its 936 entries say “Automatic or opposed as described.” "
             'Both sources are preserved per record. Eleven potential historical name changes are comparison evidence, '
             'not silent merges. Core V2 owns common RP costs; class-specific ranks come from the catalog. '
             'Exact targets, timing, component interpretation, limits and any changed values below are explicitly playtest proposals.', '',
             '## Starter selection by class', '', '| Class | First cantrips | First ranked spells | Available choices in this packet |',
             '|---|---:|---:|---|']
    progression = read(OUT / 'catalog.json')['classProgression']
    for cls, prog in progression.items():
        known = [s for s in entries if s['operational'] and cls in s['classAccess']]
        cantrips = [s for s in known if s['classAccess'][cls]['rank']==0]
        ranked = [s for s in known if s['classAccess'][cls]['rank']==1]
        lines.append(f"| {cls} | {prog['learnLevels'].get('0','—')} | {prog['learnLevels'].get('1','—')} | "
                     f"{len(cantrips)} cantrips; {len(ranked)} rank-1 spells |")
    lines += ['', 'Counts are available options, not automatic grants. Dragoon starts ordinary magic at class 3; Paladin at 2. '
              'Oracle, Soldier and Warrior receive no general Weave spell access. These low-rank options do not complete Arch/Hero spell coverage.', '']
    for school, ids in groups.items():
        lines += [f'## {school}', '']
        for key in ids:
            spell = by_id[key]
            op = spell['operational']
            if not op:
                continue
            lines += [f'<a id="spell-{key}"></a>', '', f"### {spell['name']}", '',
                      f"**ID:** `{key}` · **Concentration:** {'yes' if op['concentration'] else 'no'} · "
                      f"**Components:** {', '.join(op['components']) or 'none'}", '',
                      '| Activation | Range | Targets | Duration |', '|---|---|---|---|',
                      '| ' + ' | '.join(str(v).replace('|','/') for v in [op['activation'],f"{op['rangeFeet']} ft",op['targets'],op['duration']])+' |', '',
                      '**Resolution:** '+op['resolution'], '', op['effect'], '',
                      '**Scaling:** '+op['scaling'], '', '**Limits:** '+op['limitations'], '',
                      '**Design decisions:** '+op['designNotes'], '',
                      '| Eligible class | Rank | Earliest class level | Base RP |', '|---|---:|---:|---:|']
            for cls, access in spell['classAccess'].items():
                lines.append(f"| {cls} | {access['rank']} | {access['minimumClassLevel']} | {access['baseRpCost'] + spell['additionalRpCost']} |")
            lines += ['', 'Listed RP is before Dissonance surcharge. Resonance Shield includes its explicit 1 RP conversion cost; '
                      'other cantrips have base cost 0. All casts still obey Refrain.', '',
                      '<details><summary>Preserved source summaries and Core V2 blocks</summary>', '', '```json',
                      json.dumps({'catalogPlacements':spell['source']['original']['placements'],
                                  'coreEntries':spell['source']['coreEntries'],
                                  'possibleHistoricalAliases':spell['source']['possibleHistoricalAliases']},ensure_ascii=False,indent=2),
                      '```', '', '</details>', '']
    (DOC / 'SPELL_PLAYTEST_STARTER.md').write_text('\n'.join(lines),encoding='utf-8')


if __name__ == '__main__':
    main()
