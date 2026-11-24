"""Read-only lexical writer call census; not an exhaustive purity proof."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PERSISTENCE = ROOT / 'engine/com.decennium.foundation/Runtime/Persistence'
TOKENS = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|@"(?:""|[^"])*"|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[{}]')


def block(text, brace):
    depth = 0
    for match in TOKENS.finditer(text, brace):
        if match.group() == '{': depth += 1
        elif match.group() == '}':
            depth -= 1
            if depth == 0: return text[brace:match.end()]
    raise AssertionError('unclosed body')


methods = {}
paths = {}
for path in PERSISTENCE.glob('*.cs'):
    text = path.read_text(encoding='utf-8-sig')
    for cls_match in re.finditer(r'(?:public|internal|private)\s+(?:(?:sealed|static|partial|abstract)\s+)*class\s+(\w+)\b', text):
        cls = cls_match.group(1)
        paths[cls] = path
        brace = text.index('{', cls_match.end())
        scope = block(text, brace)
        for match in re.finditer(r'(?:public|private|internal)\s+(?:static\s+)?[\w<>\[\],?]+\s+(\w+)\s*\(', scope):
            body_start = scope.find('{', match.end())
            arrow = scope.find('=>', match.end())
            if arrow >= 0 and (body_start == -1 or arrow < body_start):
                end = scope.index(';', arrow) + 1
                implementation = scope[arrow+2:end]
            else:
                implementation = block(scope, body_start)
                end = body_start + len(implementation)
            body = scope[match.start():end]
            signature = body[:body.index('{')] if '{' in body and ('=>' not in body or body.index('{')<body.index('=>')) else body[:body.index('=>')]
            if 'BinaryReader' in signature:
                # The audited root passes writers to these overload families.
                continue
            key = cls + '.' + match.group(1)
            methods.setdefault(key, []).append({'line': text[:brace+match.start()].count('\n')+1,
                                               'body': body, 'implementation': implementation})

seen = set()
queue = ['SnapshotCodec.Encode']
edges = {}
external = {}
flagged = []
while queue:
    key = queue.pop()
    if key in seen: continue
    seen.add(key)
    cls, method = key.split('.')
    assert key in methods, key
    targets = set()
    unknown = set()
    for body in methods[key]:
        code = body['implementation']
        for receiver, name in re.findall(r'(?<![\w.])(?:(\w+)\.)?(\w+)\s*\(', code):
            dest = receiver+'.'+name if receiver in paths else cls+'.'+name if not receiver and cls+'.'+name in methods else None
            if dest: targets.add(dest)
            elif receiver and receiver[0].isupper(): unknown.add(receiver+'.'+name)
            if receiver == 'Validation' or re.search(r'^(Resolve|Replay|Draw|Roll|Advance|Validate|Initial)', name):
                flagged.append({'method': key, 'line': body['line'], 'call': (receiver+'.' if receiver else '')+name})
        for ctor in re.findall(r'new\s+(\w+Codec)\s*\([^)]*\)\.(\w+)\(', code):
            targets.add('.'.join(ctor))
    edges[key] = sorted(targets)
    external[key] = sorted(unknown)
    queue.extend(targets-seen)

report = {
    'status': 'STATIC_LEXICAL_CALL_CENSUS_NOT_TRANSITIVE_PURITY_PROOF',
    'roots': ['SnapshotCodec.Encode'],
    'methods': [{'key': key, 'path': paths[key.split('.')[0]].relative_to(ROOT).as_posix(),
                 'declarations': [{'line': x['line'], 'sha256': hashlib.sha256(x['body'].encode()).hexdigest()} for x in methods[key]],
                 'calls': edges[key], 'externalCalls': external[key]} for key in sorted(seen)],
    'flaggedCalls': flagged,
    'limitations': ['Non-BinaryReader overloads conservatively merged; BinaryReader overloads excluded because audited root passes writers',
                   'Instance calls/property getters, outside-persistence callees and interface dispatch need manual audit',
                   'SnapshotCodec.Encode includes known Validation.Snapshot entry; no pure writer exists yet',
                   'No C# code/build/test/gameplay execution']}
(Path(__file__).parent/'codec-write-call-census.json').write_bytes((json.dumps(report, indent=2)+'\n').encode())
print(json.dumps({'methodNames':len(seen),'files':len({paths[key.split('.')[0]] for key in seen}),
                  'flagged':flagged,'external':sorted(set().union(*(set(v) for v in external.values())))}))
