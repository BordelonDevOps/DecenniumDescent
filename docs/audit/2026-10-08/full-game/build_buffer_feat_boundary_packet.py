from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
text=(HERE/'CODEX_BUFFER_FEAT_BOUNDARY_QUESTIONS.md').read_text(encoding='utf-8')
for name in ('BUFFER_FEAT_DEPENDENCY_SUPPLEMENT.json','BUFFER_FEAT_SOUL_DEPENDENCY.json'):
    text+='\n## Exact supporting evidence: '+name+'\n\n```json\n'+(HERE/name).read_text(encoding='utf-8')+'\n```\n'
text+='\n## Exact original Necrotic Affinity wording (scope conflict)\n\n'
capture=json.loads((HERE/'BUFFER_FEAT_COMPLETION_SOURCES.json').read_text(encoding='utf-8'))
text+='```json\n'+json.dumps(next(r for r in capture['records'] if r['id']=='necrotic_affinity'),ensure_ascii=False,indent=2)+'\n```\n'
(HERE/'CODEX_BUFFER_FEAT_BOUNDARY_CONFERENCE.md').write_text(text,encoding='utf-8')
print('Prepared8-feat dependency/boundary conference:',len(text.encode('utf-8')),'bytes; not yet submitted.')
