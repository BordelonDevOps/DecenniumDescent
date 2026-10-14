"""Capture crafting framework evidence without modifying source or runtime data."""
from pathlib import Path
import collections
import hashlib
import json
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT.parents[1]
AUDIT = GAME / 'docs/audit/2026-10-08/full-game'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def dump(name, value):
    (AUDIT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def main():
    target = AUDIT / 'CRAFTING_ENGINE_SOURCE_EVIDENCE.json'
    if target.exists():
        raise SystemExit('Archived evidence exists; do not replace the review record.')
    source = ROOT / 'data/crafting/Decennium_Descent_Crafting_Bible_v4.json'
    book = GAME / 'books/player/Decennium_Descent_Crafting_Bible_v5_Known_Descent.docx'
    d = json.loads(source.read_text(encoding='utf-8-sig'))
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    with zipfile.ZipFile(book) as z:
        xml = ET.fromstring(z.read('word/document.xml'))
    ps = [''.join(t.text or '' for t in p.findall('.//w:t', ns)) for p in xml.findall('.//w:p', ns)]
    system = {k:v for k,v in d['system'].items() if k not in ('matrixResearch', 'designPillars', 'recipeDiscovery')}
    system['recipeDiscovery'] = {k:v for k,v in d['system']['recipeDiscovery'].items() if k != 'libraries'}
    # P93's encoded-library lore is deliberately outside the mechanical review.
    public = [{'paragraph': i, 'text': ps[i]} for i in range(119) if i != 93]
    loop = ROOT / 'docs/mechanics/GAMEPLAY_LOOP_CANON.md'
    ls = loop.read_text(encoding='utf-8-sig').splitlines()
    loop_ranges = [(43, 50), (52, 90), (297, 306), (502, 511), (645, 650)]
    passages = [{'line': i, 'text': ls[i-1]} for a,b in loop_ranges for i in range(a,b+1)]
    recipes = d['recipes']
    counts = lambda key: dict(collections.Counter(str(x[key]) for x in recipes))
    allowed_bands = [(1,4,1,2),(5,8,2,4),(9,12,4,6),(13,16,6,8),(17,19,8,9),(20,20,10,10)]
    rank_conflicts = [x['id'] for x in recipes if not any(a<=x['skillLevel']<=b and lo<=x['tier']<=hi for a,b,lo,hi in allowed_bands)]
    consumed_tools = [{'id':x['id'],'component':c} for x in recipes for c in x['components'] if c['role']=='tool' and c['consumed']]
    audit = {'recipes':len(recipes),'materials':len(d['materials']), 'trades':len(d['tradeskills']),
        'recipeVisibility':counts('visibility'), 'materialVisibility':dict(collections.Counter(x['visibility'] for x in d['materials'])),
        'timeConversions':[{'printed':t,'activeHours':h} for t,h in sorted(set((x['craftingTime'],x['workRequirements']['activeWorkHours']) for x in recipes))],
        'specialUnresolvedTimes':[x['id'] for x in recipes if x['workRequirements']['activeWorkHours'] is None],
        'rankBandConflicts':rank_conflicts,'consumedToolRows':consumed_tools,
        'maxAssistants':dict(collections.Counter(x['workRequirements']['maximumAssistants'] for x in recipes)),
        'allFormulaFlagsMatchSkillAbove4':all(x['discovery']['requiresFormula']==(x['skillLevel']>4) for x in recipes),
        'allResultQuantitiesMatch':all(x['quantity']==x['resultItem']['quantity'] for x in recipes),
        'allResultValuesMatchRecommended':all(x['resultItem']['value']==x['economy']['recommendedMarketValue'] for x in recipes),
        'allCheckDCsMatch':all(x['difficulty']==x['craftingCheck']['targetDC'] for x in recipes),
        'mishapBookReferences':[{'paragraph':i,'text':s} for i,s in enumerate(ps) if 'mishap' in s.lower()],
        'effectReviewStatus':'All recipe effects still require individual/family review; structural checks grant no approval.'}
    evidence = {'scope':'Crafting/harvesting operational framework. Cosmology excluded until after verified authorized GitHub push.',
        'crafting':{'path':str(source.relative_to(GAME)), 'sha256':sha(source),'system':system,'tradeskills':d['tradeskills']},
        'publicBook':{'path':str(book.relative_to(GAME)), 'sha256':sha(book),'paragraphConvention':'zero-based all w:p including table cells','passages':public},
        'loop':{'path':str(loop.relative_to(GAME)), 'sha256':sha(loop),'passages':passages},'structuralAudit':audit}
    dump(target.name,evidence)
    dump('CRAFTING_ENGINE_STRUCTURAL_AUDIT.json',audit)
    frozen=[source, book, loop, GAME/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json', ROOT/'src/data/crafting-recipes.json', GAME/'src/data/crafting-recipes.json', GAME/'docs/canon/CANON_MANIFEST.json']
    frozen+=list((ROOT/'docs/mechanics').glob('*PLAYTEST.md'))
    frozen+=list((ROOT/'docs/mechanics').glob('*REVIEW_STATUS.json'))
    frozen+=list((ROOT/'data/playtest').glob('*.json'))
    dump('CRAFTING_ENGINE_BASELINE.json', {'files':{str(p.relative_to(GAME)):sha(p) for p in frozen}})
    parts=['# Crafting engine source evidence',json.dumps(evidence,ensure_ascii=False,indent=2)]
    (AUDIT/'CRAFTING_ENGINE_SOURCE_EXCERPTS.txt').write_text('\n'.join(parts)+'\n',encoding='utf-8')
    print(json.dumps({'evidenceChars':len(parts[1]),'frozenFiles':len(frozen),'rankBandConflicts':len(rank_conflicts),'consumedToolRows':len(consumed_tools),'checks':{k:v for k,v in audit.items() if k.startswith('all')}},ensure_ascii=False))

if __name__ == '__main__': main()
