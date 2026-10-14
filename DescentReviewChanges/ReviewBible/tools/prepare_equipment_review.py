"""Capture the equipment sources and crafting interfaces; never modify a source."""
from pathlib import Path
import collections
import hashlib
import json
import re
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT.parents[1]
AUDIT = GAME / 'docs/audit/2026-10-08/full-game'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def write(name, data):
    (AUDIT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def main():
    player = GAME / 'docs/reference/Player_Rulebook_v6_source_text.txt'
    core = GAME / 'books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx'
    craft = ROOT / 'data/crafting/Decennium_Descent_Crafting_Bible_v4.json'
    lines = player.read_text(encoding='utf-8-sig').splitlines()
    # Deliberately exclude the soul-coin origin and all cosmology adjudication.
    ranges = [(79, 83), (123, 123), (2407, 2411), (6500, 6548),
              (6555, 7152), (7867, 7885)]
    passages = [{'line': i, 'text': lines[i-1]} for a,b in ranges for i in range(a,b+1)]
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    with zipfile.ZipFile(core) as z:
        xml = ET.fromstring(z.read('word/document.xml'))
    ps = [''.join(t.text or '' for t in p.findall('.//w:t', ns)) for p in xml.findall('.//w:p', ns)]
    # Existing audits use zero-based all-paragraph indexes, including table cells.
    core_ranges = [(8309, 8337), (8357, 8389)]
    armor = [{'paragraph': i, 'text': s} for i,s in enumerate(ps) if s.startswith('Armor never prevents casting')]
    core_evidence = [{'paragraph': i, 'text': ps[i]} for a,b in core_ranges for i in range(a,b+1)] + armor
    tables=[]
    for i in range(6503,7100):
        s=lines[i]
        if not s.startswith('|') or (i and lines[i-1].startswith('|')): continue
        end=i
        while end<len(lines) and lines[end].startswith('|'): end+=1
        heading=next((lines[j] for j in range(i-1,max(0,i-6),-1) if lines[j].strip()), '')
        headers=[c.strip() for c in s.strip('|').split('|')]
        group=None; rows=[]
        for j in range(i+2,end):
            cells=[c.strip() for c in lines[j].strip('|').split('|')]
            if len(cells)==1:
                group=cells[0]; continue
            if len(cells)!=len(headers): raise ValueError((j+1,headers,cells))
            rows.append({'line':j+1,'group':group,'fields':dict(zip(headers,cells)),'raw':lines[j]})
        tables.append({'heading':heading,'startLine':i+1,'headers':headers,'rows':rows})
    c=json.loads(craft.read_text(encoding='utf-8-sig'))
    runtime=ROOT/'src/data/crafting-recipes.json'
    rt=json.loads(runtime.read_text(encoding='utf-8-sig'))
    recipes=c['recipes']; public=[x for x in recipes if x['visibility']=='public']
    # Report structural facts only: a developed status never means effects are reviewed.
    counts=lambda key:dict(collections.Counter(str(x.get(key)) for x in recipes))
    audit={'recipeCount':len(recipes),'materialCount':len(c['materials']),
           'visibility':counts('visibility'),'outputTypes':counts('outputType'),
           'mechanicsTypes':dict(collections.Counter(x.get('mechanics',{}).get('type') for x in recipes)),
           'statuses':counts('status'),'publicRuntimeCount':len(rt),
           'publicRuntimeIdsMatch':{x['id'] for x in public}=={x['id'] for x in rt},
           'publicRuntimeExactRecordsMatch':{x['id']:x for x in public}=={x['id']:x for x in rt},
           'sourceQualityIsNotReviewApproval':True,
           'staleSeasonPointers':['/system/designPillars','/system/stationsAndTime/seasonRule'],
           'openInterfaces':['craft outcome vs equipment quality vs Core market quality',
             'batch or unit recommendedMarketValue','component identity/retail mismatch',
             'complete output activation, targets, duration, stacking and destruction',
             'craft access/training, tool/facility bonuses and mishap procedures',
             'preservation intervals and partial harvest quantities'],
           'samplePublicRecipe':{k:v for k,v in public[0].items() if k not in ['matrixResearch','discovery']}}
    system_keys=['craftingCheck','skillAdvancement','stationsAndTime','economy']
    craft_evidence={'path':str(craft.relative_to(GAME)).replace('\\','/'),'sha256':sha(craft),
        'system':{k:c['system'][k] for k in system_keys},
        'tradeskills':{k:{a:b for a,b in v.items() if a!='rankBands'} for k,v in c['tradeskills'].items()},
        'audit':audit}
    evidence={'scope':'Source capture only; equipment decisions pending GPT. Cosmology deferred until verified GitHub push.',
        'player':{'path':str(player.relative_to(GAME)).replace('\\','/'),'sha256':sha(player),'lineRanges':ranges,'passages':passages},
        'core':{'path':str(core.relative_to(GAME)).replace('\\','/'),'sha256':sha(core),'paragraphConvention':'zero-based all w:p including tables','passages':core_evidence},
        'crafting':craft_evidence,'tables':tables}
    write('EQUIPMENT_SOURCE_EVIDENCE.json',evidence)
    write('CRAFTING_INTERFACE_AUDIT.json',audit)
    text=['# Exact equipment source excerpts',f'Player source SHA-256 {sha(player)}']
    text += [f"L{x['line']}: {x['text']}" for x in passages]
    text += ['\n# Core equipment and valuation excerpts',f'Core DOCX SHA-256 {sha(core)}']
    text += [f"P{x['paragraph']}: {x['text']}" for x in core_evidence]
    text += ['\n# Crafting interface source and structural audit',json.dumps(craft_evidence,ensure_ascii=False,indent=2)]
    (AUDIT/'EQUIPMENT_SOURCE_EXCERPTS.txt').write_text('\n'.join(text)+'\n',encoding='utf-8')
    protected=[player,core,craft,runtime,GAME/'docs/canon/CANON_MANIFEST.json']
    protected += list((ROOT/'docs/mechanics').glob('*PLAYTEST.md'))
    protected += list((ROOT/'data/public').glob('*Playtest_v0_1.json'))
    protected += [ROOT/'data/playtest/character_foundation.json',ROOT/'data/playtest/ancestry_background_candidate.json',ROOT/'docs/mechanics/SPELL_INTEGRATION_RULES.md']
    baseline={'scope':'No source deletion or mutation authorized by this capture','files':{str(p.relative_to(GAME)).replace('\\','/'):sha(p) for p in protected}}
    if not (AUDIT/'EQUIPMENT_REVIEW_BASELINE.json').exists(): write('EQUIPMENT_REVIEW_BASELINE.json',baseline)
    write('EQUIPMENT_SOURCE_VALIDATION.json',{'status':'PASS','tables':len(tables),'rows':sum(len(t['rows']) for t in tables),'playerPassages':len(passages),'corePassages':len(core_evidence),'protectedFiles':len(protected),'sourceHashesVerified':all(sha(GAME/p)==h for p,h in baseline['files'].items())})
    print(json.dumps({'tables':[(t['heading'],len(t['rows'])) for t in tables],'crafting':{k:v for k,v in audit.items() if k not in ['samplePublicRecipe','openInterfaces']},'excerptChars':len('\n'.join(text))},ensure_ascii=False))

if __name__=='__main__': main()
