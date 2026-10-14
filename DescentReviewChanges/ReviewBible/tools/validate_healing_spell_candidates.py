"""Individual candidate validation before any active catalog promotion."""
from pathlib import Path
import json
from build_spell_playtests import FIELDS
from spell_playtest_rules import access_for,quote_cast,SpellRuleError
ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT.parents[1]/'docs/audit/2026-10-08/full-game'
IDS={'stitch-fate','death-ward','resurrection','mass-resurrection-denial','true-resurrection','soul-bind'}

def main():
    draft=json.loads((ROOT/'data/playtest/spell_drafts/candidate_healing_death.json').read_text(encoding='utf-8'))
    sources=json.loads((AUDIT/'HEALING_DEATH_SOURCE_CANDIDATES.json').read_text(encoding='utf-8'))
    captured={r['spellId']:r['spell'] for r in sources['spellCatalogRecords']}
    current={s['id']:s for s in json.loads((ROOT/'data/public/spell_playtests/catalog.json').read_text(encoding='utf-8'))['spells']}
    assert set(captured)==IDS
    assert len(draft['spells'])==6 and {s['id'] for s in draft['spells']}==IDS
    checks=[];gates=0
    for s in draft['spells']:
        ident=s['id'];original=captured[ident]
        assert all(current[ident][key]==original[key] for key in ('id','source','classAccess'))
        assert all(key in s for key in FIELDS)
        assert isinstance(s['rangeFeet'],int) and not isinstance(s['rangeFeet'],bool) and s['rangeFeet']>=0
        assert isinstance(s['concentration'],bool) and s['components']==['V','S','F']
        assert all(isinstance(s[k],str) and s[k].strip() for k in FIELDS if k not in ('rangeFeet','concentration','components'))
        candidate=dict(current[ident],operational=s,status='operational-playtest-draft')
        for cls,entry in original['classAccess'].items():
            for level in range(1,21):
                try:access_for(candidate,cls,level);allowed=True
                except SpellRuleError:allowed=False
                assert allowed==(level>=entry['minimumClassLevel']),(ident,cls,level)
                gates+=1
            cast=quote_cast(candidate,cls,20,available_spell_ids={ident},rp=100,max_rp=100,dissonance=0,proficiency=6,casting_modifier=3)
            assert cast['cost']==entry['baseRpCost'] and cast['rank']==entry['rank']
        checks.append({'spellId':ident,'status':'PASS','preservedClassAccess':original['classAccess'],
                       'operationalInCurrentCatalog':current[ident]['operational'] is not None})
    report={'status':'PASS','scope':'Six complete individual operational objects, preserved source identity/access/ranks/levels/RP and all authorized class-level boundaries. Source design review is separate; this validator does not promote anything.',
            'candidateCount':6,'classLevelGateCases':gates,'spells':checks}
    (ROOT/'docs/mechanics/HEALING_SPELL_CANDIDATE_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f'PASS6 healing/death spell candidates; {gates} class/level boundaries; preserved ranks/RP/source metadata.')
if __name__=='__main__':main()
