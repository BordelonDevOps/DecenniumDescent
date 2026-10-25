"""Read-only display of authored case observations and newly permitted views."""
from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8');E=Path(__file__).parent/'information8_return01_received'
read=lambda n:json.loads((E/n).read_text(encoding='utf-8-sig'))
def show(c):
 print('\nCASE',c['id'],c['description']);print('QUALIFICATION',json.dumps(c['wholeCaseQualification'],ensure_ascii=False))
 print('WORLD',json.dumps(c['initialState']['world'],ensure_ascii=False))
 print('ACTORS',json.dumps({a:{k:v[k] for k in ['template','body','phase','rp','hp','concentration']} for a,v in c['initialState']['actors'].items()},ensure_ascii=False))
 for e in c['timeline']:
  o=e['observations']
  if 'regularMarker' in o:continue
  print(e['id'],e['time'],e['event'])
  if 'finalRPPaid' in o:print('CAST',o['caster'],o['spellId'],'RP',o['finalRPPaid'],'Action',o['actualAction'],'Plan',json.dumps(o['plan'],ensure_ascii=False))
  else:print('OBS',json.dumps(o,ensure_ascii=False))
  new={a:v[len(e['before']['views'].get(a,[])):] for a,v in e['after']['views'].items() if v!=e['before']['views'].get(a,[])}
  if new:print('NEW-VIEWS',json.dumps(new,ensure_ascii=False))
 for b in c['branches']:show(b)
for caseid in sys.argv[1:]:show(read('cases/'+caseid+'.json'))
