"""Validate original evidence without mistaking a snapshot for final rules."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT.parents[1]/'docs/audit/2026-10-08/full-game'
IDS={'harmonic-bulwark','polymorph','shapechange','true-polymorph','mass-polymorph'}
def main():
    source_text=(ROOT/'src/data/spells.js').read_text(encoding='utf-8')
    originals=json.JSONDecoder().raw_decode(source_text.split('export const SPELLS = ',1)[1])[0]
    core=json.loads((ROOT/'data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json').read_text(encoding='utf-8'))
    current={r['id']:r for r in json.loads((ROOT/'data/public/spell_playtests/catalog.json').read_text(encoding='utf-8'))['spells']}
    saved=json.loads((AUDIT/'TRANSFORMATION_SPELL_SOURCE_CANDIDATES.json').read_text(encoding='utf-8'))
    assert set(saved['spellIds'])==IDS and len(saved['spells'])==5
    entries=0;aliases=0
    for row in saved['spells']:
        ident=row['id'];snap=row['wholeOverlaySnapshot']
        assert row['catalogSource']==originals[ident]==snap['source']['original']==current[ident]['source']['original']
        assert row['classAccess']==snap['classAccess']==current[ident]['classAccess']
        assert row['overlaySha256']==hashlib.sha256(json.dumps(snap,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
        for v in row['coreEntries']:
            assert v['original']==core['spells'][v['index']]
            entries+=1
        for v in row['possibleHistoricalAliases']:
            assert v['original']==core['spells'][v['index']]
            aliases+=1
    assert saved['costByRank']==core['resonance_costs']
    report={'status':'PASS','spellOriginals':5,'exactCoreEntries':entries,'possibleAliasEntries':aliases,
            'scope':'Original identities, full captured objects, exact Core positions, class access and RP metadata. Source integrity only; no inferred operational approval.',
            'sourceFiles':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ('src/data/spells.js','data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json')}}
    (ROOT/'docs/mechanics/TRANSFORMATION_SPELL_SOURCE_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))
if __name__=='__main__':main()
