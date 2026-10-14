#!/usr/bin/env python3
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'src/data/prestige-lorebook.json'
OUT=ROOT/'docs/prestige/prestige-registry-snapshot.json'
rows=json.loads(SOURCE.read_text(encoding='utf-8'))
normalized=[]
for i,row in enumerate(rows,1):
    hallmarks=[str(x).strip() for x in row.get('hallmarks',[]) if str(x).strip()]
    normalized.append({
        'id': f'prestige-{i:03d}',
        'name': str(row.get('name','')).strip(),
        'baseClass': str(row.get('baseClass','')).strip(),
        'requirements': str(row.get('requirements','')).strip(),
        'unlock': str(row.get('unlock') or row.get('entrance') or '').strip(),
        'hallmarks': hallmarks,
        'capstone': str(row.get('capstone','')).strip(),
        'draftCapstone': row.get('draftCapstone') is True,
        'combatRole': str(row.get('combatRole','')).split('Character Story')[0].replace('**','').strip(),
    })
payload={'schemaVersion':'1.0','generatedFrom':'src/data/prestige-lorebook.json','count':len(normalized),'paths':normalized}
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(OUT)
