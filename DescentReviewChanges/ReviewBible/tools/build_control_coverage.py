"""Track individual candidate dispositions without counting lexical matches as review."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]


def key_for_source(source):
    if source['kind']=='card':
        return (source['path'],'class-card',source['cardId'])
    if source['kind']=='engine':
        return (source['path'],'class-engine',source['engineIndex'])
    if source['kind']=='operational-spell':
        return (source['path'],'ordinary-spell',source['spellId'])
    return None


def main():
    packet_names=['CONTROL_STATE_SOURCE_PACKET.json','CONTROL_STATE_SUPPLEMENT_SOURCE_PACKET.json']
    records=[]
    for name in packet_names:
        records.extend(json.loads((GAME/'docs/audit/2026-10-08/full-game'/name).read_text(encoding='utf-8'))['records'])
    custom=json.loads((ROOT/'data/playtest/custom_condition_bindings.json').read_text(encoding='utf-8'))
    known={}
    for definition in custom['definitions']:
        for source in definition['applicationSources']:
            key=key_for_source(source)
            if key:
                known.setdefault(key,set()).add(definition['mechanicalId'])
    output=ROOT/'data/playtest/control_state_coverage.json'
    previous=json.loads(output.read_text(encoding='utf-8')) if output.exists() else {'candidates':[]}
    old={r['candidateId']:r for r in previous['candidates']}
    rows=[]
    for source in records:
        kind=source['kind']
        ident=source['card']['id'] if kind=='class-card' else source['engineIndex'] if kind=='class-engine' else source['spellId']
        candidate_id=f"{kind}:{source.get('owner','ordinary')}:{ident}"
        digest=source.get('sourceObjectSha256',source.get('textSha256',source.get('operationalSha256')))
        row={'candidateId':candidate_id,'sourceKind':kind,'sourcePath':source['path'],
             'sourceId':ident,'sourceSha256':digest,
             'existingPartialBindings':sorted(known.get((source['path'],kind,ident),set())),
             'status':'UNREVIEWED','classification':None,'bindingIds':[],
             'rationale':'','reviewEvidence':[],'openIssues':[]}
        if candidate_id in old and old[candidate_id]['sourceSha256']==digest:
            for field in ('status','classification','bindingIds','rationale','reviewEvidence','openIssues'):
                row[field]=old[candidate_id][field]
        rows.append(row)
    data={'status':'IN_PROGRESS','scope':f'{len(rows)} supplied lexical and explicitly selected supplemental candidates. Existing partial bindings do not prove whole-source semantics or exhaustive all-source coverage.',
          'sourcePackets':['docs/audit/2026-10-08/full-game/'+name for name in packet_names],
          'candidates':rows}
    output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    addressed=sum(r['status']!='UNREVIEWED' for r in rows)
    lines=['# Control-state candidate coverage','',
           f'**IN PROGRESS: {addressed}/{len(rows)} candidates have a recorded disposition.** This is a supplied lexical candidate set, not exhaustive game-wide semantic coverage. A previous partial binding does not resolve every component of its source.','',
           'See [source checks](CONTROL_STATE_SOURCE_VALIDATION.json) and [structured dispositions](../../data/playtest/control_state_coverage.json).','',
           '| Source identity | Status | Existing partial bindings | Classification |',
           '|---|---|---|---|']
    for row in rows:
        lines.append(f"| `{row['candidateId']}` | {row['status']} | {', '.join(row['existingPartialBindings']) or '—'} | {row['classification'] or 'Pending'} |")
    (ROOT/'docs/mechanics/CONTROL_STATE_COVERAGE.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(f'Control candidates: {len(rows)}; recorded dispositions: {addressed}; no completeness inferred.')


if __name__=='__main__':
    main()
