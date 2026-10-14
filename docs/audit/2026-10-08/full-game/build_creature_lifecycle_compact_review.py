from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
original=(HERE/'CODEX_CREATURE_LIFECYCLE_IMPLEMENTATION_REVIEW.md').read_text(encoding='utf-8')
parts=[original.split('## docs/mechanics/')[0].replace('# Exact creature lifecycle implementation review','# Exact creature lifecycle implementation review — compact transport')]
parts+=['The earlier322,149-character transport did not appear in either the persisted notebook read or refreshed Chrome. This compact transport includes the same implementation, checks, exact100 source procedures and5 supports; repeated metadata and unrelated device methods are omitted. No rules were changed between packets.','']
for name in ('docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST.md','tools/creature_lifecycle_playtest_rules.py',
             'tools/validate_creature_lifecycle_playtests.py','docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST_VALIDATION.json',
             'docs/mechanics/CREATURE_LIFECYCLE_SOURCE_VALIDATION.json'):
    parts+=['## '+name,'',(ROOT/name).read_text(encoding='utf-8'),'']
code=(ROOT/'tools/device_lifecycle_playtest_rules.py').read_text(encoding='utf-8')
parts+=['## Exact shared wallet/command ledger (remaining device module unchanged)','',code.split('@dataclass\nclass Entity:')[0],'']
data=json.loads((ROOT/'data/playtest/creature_lifecycle_bindings.json').read_text(encoding='utf-8'))
parts+=['## Exact100 source procedures with classifications','']
for r in data['bindings']:
    parts+=['### '+r['bindingId']+' — '+r['classification'],json.dumps(r['sourceProcedure'],ensure_ascii=False),'']
source=json.loads((HERE/'CREATURE_LIFECYCLE_SOURCE_CANDIDATES.json').read_text(encoding='utf-8'))
supports=source['supportingSources']+json.loads((HERE/'CREATURE_LIFECYCLE_SUPPORTING_SOURCES.json').read_text(encoding='utf-8'))['supportingSources']
parts+=['## Five frozen supporting paragraphs',json.dumps(supports,ensure_ascii=False),'']
out='\n'.join(parts)
(HERE/'CODEX_CREATURE_LIFECYCLE_IMPLEMENTATION_COMPACT.md').write_text(out,encoding='utf-8')
print(f'Compact exact review:{len(out)} characters.')
