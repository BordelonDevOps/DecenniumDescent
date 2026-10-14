"""Adversarial probes of malformed admitted collection values; isolated fixtures."""
from pathlib import Path
import sys
import json
audit=Path(__file__).resolve().parent
root=audit.parents[3]/'DescentReviewChanges/ReviewBible'
sys.path.insert(0,str(root/'tools'))
from validate_temporal_control_world import world,pulse,attach,capture
from temporal_control_world import NativeOccurrenceLedger,ClockMarker
from temporal_control_playtest_rules import CanonicalPulseWallet

results=[]
for malformed in ('guard-consumed','recipient-history','pulse-declarations','native-consumed'):
    w,c=world()
    if malformed=='native-consumed':
        r=attach(c,'native',NativeOccurrenceLedger(),'cleric.hero.saint.aura-of-grace','regular-heal',
                 identity='native',targets=('a',),deadline=None)
        capture(w);w.regular_start('a',6);r.holder.consumed=[]
        action=lambda:c.native_occurrence(w,'native','event',eligible=True,opted_in=True)
    else:
        profile='transcendent-meditation' if malformed=='guard-consumed' else 'song-of-mending'
        r=pulse(c,profile)
        r.holder.resolve(0,ClockMarker(0),(),CanonicalPulseWallet(w,'a'),round_number=1)
        capture(w);w.regular_start('a',6)
        if malformed=='guard-consumed':c.outputs.consumed=[]
        elif malformed=='recipient-history':c.recipients.history=[]
        else:r.holder.declarations=[]
        action=lambda:c.resolve_pulse(w,'pulse','event',1,('b',))
    before={'rp':w.wallets['a'].rp,'rc':w.scheduler.rc['a'],'holder':repr(vars(r.holder))}
    try:outcome=repr(action())
    except Exception as error:outcome=type(error).__name__+': '+str(error)
    after={'rp':w.wallets['a'].rp,'rc':w.scheduler.rc['a'],'holder':repr(vars(r.holder))}
    results.append({'case':malformed,'outcome':outcome,'stateChanged':before!=after,
                    'before':before,'after':after})
p=audit/'TEMPORAL_CONTROL_WORLD_SCHEMA_PROBES.json'
assert not p.exists()
p.write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
print(json.dumps([{'case':r['case'],'outcome':r['outcome'],'stateChanged':r['stateChanged']} for r in results],indent=2))
