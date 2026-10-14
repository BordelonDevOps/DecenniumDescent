from pathlib import Path
import json
from healing_pulse_playtest_rules import PROFILES,NATIVE_COSTS
ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT.parents[1]/'docs/audit/2026-10-08/full-game'
def main():
    data=json.loads((ROOT/'data/playtest/healing_pulse_profiles.json').read_text(encoding='utf-8'))
    supplied=json.loads((ROOT/'data/playtest/healing_pulse_bindings.json').read_text(encoding='utf-8'))['bindings']
    ids={b['bindingId'] for b in supplied}
    support=json.loads((AUDIT/'HEALING_PULSE_SUPPORTING_SOURCES.json').read_text(encoding='utf-8'))
    for r in support:
        if r['key']=='cards':ids.add(r['value']['id'])
        elif r['key']=='engine':ids.add(Path(r['sourcePath']).stem+f".engine[{r['selector']}]")
    assert set(data['profiles'])==set(PROFILES)
    assert set(data['nativeRecurrences'])==set(NATIVE_COSTS)
    assert set(data['contactVariants'])=={'garden','enhanced-garden','resonant-seed'}
    checks=[]
    for category in ('profiles','nativeRecurrences','contactVariants'):
        for profile,refs in data[category].items():
            assert refs and set(refs)<=ids,(category,profile,refs)
            checks.append({'category':category,'profile':profile,'sourceIds':refs,'result':'PASS'})
    report={'status':'PASS','linkedProfiles':len(checks),'scope':'Every current scheduling/native/contact profile maps to exact supplied sources. This validates provenance, not balance or unsupplied card acquisition.','checks':checks}
    (ROOT/'docs/mechanics/HEALING_PULSE_PROFILE_PROVENANCE.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS',len(checks),'source-linked profiles; no unbound ability labels.')
if __name__=='__main__':main()
