"""Verify expanded control candidates without claiming semantic completeness."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()


def main():
    packets=[json.loads((GAME/'docs/audit/2026-10-08/full-game'/name).read_text(encoding='utf-8')) for name in ('CONTROL_STATE_SOURCE_PACKET.json','CONTROL_STATE_SUPPLEMENT_SOURCE_PACKET.json')]
    records=[row for packet in packets for row in packet['records']]
    loaded={}
    seen=set()
    issues=[]
    counts={'class-card':0,'class-engine':0,'ordinary-spell':0}
    for row in records:
        path=row['path']
        if path not in loaded:
            loaded[path]=json.loads((ROOT/path).read_text(encoding='utf-8'))
        source=loaded[path]
        kind=row['kind']
        counts[kind]+=1
        if kind=='class-card':
            ident=row['card']['id']
            actual=next((c for c in source['cards'] if c['id']==ident),None)
            valid=actual==row['card'] and canonical_hash(actual)==row['sourceObjectSha256']
        elif kind=='class-engine':
            ident=row['engineIndex']
            actual=source['engine'][ident]
            valid=actual==row['text'] and hashlib.sha256(actual.encode()).hexdigest()==row['textSha256']
        else:
            ident=row['spellId']
            actual=next((s.get('operational') for s in source['spells'] if s['id']==ident),None)
            valid=actual==row['operational'] and canonical_hash(actual)==row['operationalSha256']
        key=(path,kind,ident)
        if key in seen:
            issues.append('Duplicate source:'+str(key))
        seen.add(key)
        if not valid:
            issues.append('Source mismatch:'+str(key))
    if len(seen)!=sum(packet['recordCount'] for packet in packets):
        issues.append('Record count mismatch')
    report={'status':'FAIL' if issues else 'PASS','scope':'Exact supplied candidate integrity only. No claim of exhaustive semantic coverage or operational closure.',
            'sourceCounts':counts,'exactRecords':len(seen),'issues':issues}
    (ROOT/'docs/mechanics/CONTROL_STATE_SOURCE_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f"{report['status']}: {len(seen)} exact control candidates; {counts}")
    if issues:
        raise SystemExit(1)


if __name__=='__main__':
    main()
