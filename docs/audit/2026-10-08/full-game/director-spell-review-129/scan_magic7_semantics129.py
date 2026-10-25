from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
D=Path(__file__).parent;E=D/'magic7_return02_received';read=lambda n:json.loads((E/n).read_text(encoding='utf-8-sig'))
cases=[]
def visit(c):
 cases.append(c)
 for b in c['branches']:visit(b)
for c in read('CASEBOOK.json')['completeCases']:visit(c)
out=[]
for c in cases:
 for e in c['timeline']:
  for aid,a in e['before']['actors'].items():
   b=e['after']['actors'][aid];p=a['phase'];s=p['lastStart'];end=p['lastEnd'];active=s is not None and (end is None or s>end)
   spent=[k for k in ['action','bonusAction'] if a['wallet'][k] and not b['wallet'][k]]
   moved=a['body']!=b['body']
   if (spent or moved) and not active and 'outside' not in (e['event']+json.dumps(e['inputs'])+json.dumps(e['observations'])).lower():out.append({'event':e['id'],'name':e['event'],'actor':aid,'time':e['time'],'spent':spent,'moved':moved,'phase':p})
(D/'MAGIC7_TIMING_FINDINGS_129.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(out,indent=2))
print('QUESTION ANSWERS')
for q in read('QUESTION_DISPOSITIONS.json'):print(q['id'],q['answer'],q.get('reason',''))
