"""Preserve mechanical source excerpts without adjudicating cosmology or rewriting sources."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT.parents[1]
AUDIT = GAME / 'docs/audit/2026-10-08/full-game'
SOURCE = GAME / 'docs/reference/Player_Rulebook_v6_source_text.txt'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def js_array(path, quoted=False):
    text = path.read_text(encoding='utf-8-sig')
    text = text[text.index('['):text.rindex('];') + 1]
    if not quoted:
        text = re.sub(r'(?m)^(\s*)([A-Za-z]\w*):', r'\1"\2":', text)
        text = re.sub(r',\s*([}\]])', r'\1', text)
    return json.loads(text)

def main():
    lines = SOURCE.read_text(encoding='utf-8-sig').splitlines()
    index = json.loads((AUDIT / 'ANCESTRY_BACKGROUND_MECHANICAL_SOURCE_INDEX.json').read_text(encoding='utf-8-sig'))
    builders = js_array(ROOT / 'src/data/builder-races.js', True)
    variants = json.loads((ROOT / 'src/data/racial-variants.json').read_text(encoding='utf-8-sig'))
    backgrounds = js_array(ROOT / 'src/data/backgrounds.js')
    by_name = {row['name']: row for row in builders}
    bg_by_name = {row['name']: row for row in backgrounds}
    omitted = []
    unknown = []

    def traits(lo, hi):
        result = []
        for n in range(lo, hi + 1):
            text = lines[n - 1].strip()
            if not text:
                continue
            if text.startswith(('Age.', 'Alignment.', 'Your ', 'As a ', 'As an ')):
                omitted.append({'line': n, 'reason': 'age/alignment/introductory narrative; original preserved'})
            elif '. ' in text and len(text.split('. ', 1)[0]) < 60:
                title, body = text.split('. ', 1)
                result.append({'name': title, 'sourceLine': n, 'text': body})
            elif result:
                result[-1].setdefault('continuationLines', []).append(n)
                result[-1]['text'] += '\n' + text
            else:
                unknown.append({'line': n, 'text': text})
        return result

    ancestry_rows = []
    for a in index['ancestries']:
        name = a['name']
        builder = by_name[name]
        start = a['traitsHeadingLine']
        variant_heading = a['variantHeadingLine']
        next_index = index['ancestries'].index(a) + 1
        if next_index < len(index['ancestries']):
            next_name = index['ancestries'][next_index]['name']
            end = next(n for n in range(variant_heading + 1, len(lines)) if lines[n - 1].strip() == next_name) - 1
        else:
            end = 1640
        variant_starts = [(v, next(n for n in range(variant_heading + 1, end + 1) if lines[n - 1].strip() == v)) for v in builder['subraces']]
        variant_rows = []
        for i, (v, n) in enumerate(variant_starts):
            upper = variant_starts[i + 1][1] - 1 if i + 1 < len(variant_starts) else end
            variant_rows.append({'name': v, 'headingLine': n, 'traits': traits(n + 1, upper)})
        ancestry_rows.append({'name': name, 'traits': traits(start + 1, variant_heading - 1), 'variants': variant_rows,
                              'builderMechanicalAlternative': {k:v for k,v in builder.items() if k != 'info'},
                              'variantAlternatives': [v for v in variants if v['parentRace'] == name]})

    bg_rows = []
    for b in index['backgrounds']:
        skill_line = b['skillLine']
        names = [lines[n - 1].strip() for n in range(skill_line - 5, skill_line) if lines[n - 1].strip() in bg_by_name]
        assert len(names) == 1, (skill_line, names)
        name = names[0]
        bg_rows.append({'name': name,
                        'source': [{'line':n, 'text':lines[n-1]} for n in range(skill_line, b['featureLine'] + 1) if lines[n-1].strip()],
                        'builderMechanicalAlternative': {k:v for k,v in bg_by_name[name].items() if k not in ('description','alignmentTendency')}})
    paths = [SOURCE, ROOT/'src/data/builder-races.js',ROOT/'src/data/races.js',ROOT/'src/data/racial-variants.json',ROOT/'src/data/backgrounds.js', ROOT/'src/data/reputation.js', ROOT/'src/data/spells.js']
    protected = {str(p.relative_to(GAME)).replace('\\','/'):digest(p) for p in paths}
    data = {'status':'source-evidence-not-approved', 'cosmology':'No cosmology review or changes before verified GitHub push; all original lore retained.',
            'sourcePath':str(SOURCE.relative_to(GAME)).replace('\\','/'), 'sourceSha256':digest(SOURCE), 'protectedSources':protected,
            'ancestries':ancestry_rows, 'backgrounds':bg_rows, 'omittedNarrativeLineIndex':omitted, 'unclassified':unknown}
    assert not unknown, unknown
    assert len(ancestry_rows)==14 and sum(len(a['variants']) for a in ancestry_rows)==45 and len(bg_rows)==20
    (AUDIT/'ANCESTRY_BACKGROUND_SOURCE_EVIDENCE.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    out=['# Complete ancestry/background mechanical source evidence', 'Source: '+str(SOURCE), 'SHA-256: '+digest(SOURCE), data['cosmology']]
    for a in ancestry_rows:
        out.append('\n## '+a['name'])
        for trait in a['traits']:
            out.append(f"L{trait['sourceLine']} {trait['name']}. {trait['text']}")
        for variant in a['variants']:
            out.append('\n### '+variant['name'])
            for trait in variant['traits']:
                out.append(f"L{trait['sourceLine']} {trait['name']}. {trait['text']}")
        out.append('BUILDER ALTERNATIVE: '+json.dumps(a['builderMechanicalAlternative'],ensure_ascii=False))
        out.append('VARIANT ALTERNATIVES: '+json.dumps(a['variantAlternatives'],ensure_ascii=False))
    for b in bg_rows:
        out.append('\n## '+b['name'])
        out.extend(f"L{s['line']} {s['text']}" for s in b['source'])
        out.append('BUILDER ALTERNATIVE: '+json.dumps(b['builderMechanicalAlternative'],ensure_ascii=False))
    text='\n'.join(out)+'\n'
    (AUDIT/'ANCESTRY_BACKGROUND_MECHANICAL_EXCERPTS.txt').write_text(text,encoding='utf-8')
    print(json.dumps({'ancestries':len(ancestry_rows),'variants':45,'backgrounds':len(bg_rows),'traits':sum(len(a['traits'])+sum(len(v['traits']) for v in a['variants']) for a in ancestry_rows),'characters':len(text),'unknown':unknown}))

if __name__=='__main__':
    main()
