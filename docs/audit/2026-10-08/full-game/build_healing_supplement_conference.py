from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
data=json.loads((HERE/'HEALING_INTERFACE_SUPPLEMENT.json').read_text(encoding='utf-8'))
rows=[]
for r in data['classRecords']:
 if r['kind']=='class-card':
  rows.append({'kind':r['kind'],'owner':r['owner'],'sourceObjectSha256':r['sourceObjectSha256'],**{k:r['card'].get(k) for k in ('id','name','activation','cost','rangeAndTarget','duration','frequency','effect','prerequisite')}})
 else:rows.append(r)
text=(HERE/'HEALING_SUPPLEMENT_QUESTIONS.md').read_text(encoding='utf-8')+'\n## Exact supplemental procedures\n\n```json\n'+json.dumps(rows,ensure_ascii=False,indent=2)+'\n```\n'
(HERE/'CODEX_HEALING_SUPPLEMENT_CONFERENCE.md').write_text(text,encoding='utf-8')
print(f'Supplement prepared, not submitted: {len(text)} characters')
