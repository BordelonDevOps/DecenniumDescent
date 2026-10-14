"""Render80 exact source roles without inferring approval from source integrity."""
from pathlib import Path
import json
from validate_remaining_lifecycle_sources import main as validate_sources
ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT.parents[1]/'docs/audit/2026-10-08/full-game'
PATH=ROOT/'data/playtest/remaining_lifecycle_bindings.json'

def main():
    validate_sources()
    source=json.loads((AUDIT/'REMAINING_LIFECYCLE_CONFERENCE_SOURCES.json').read_text(encoding='utf-8'))
    prior=json.loads(PATH.read_text(encoding='utf-8')) if PATH.exists() else {}
    known={r['bindingId']:r for r in prior.get('bindings',[])}
    rows=[]
    for r in source['classRecords']:
        if r['kind']=='class-card':
            c=r['card'];ident=source_id=c['id'];sha=r['sourceObjectSha256']
            proc={k:c.get(k) for k in ('name','activation','cost','rangeAndTarget','duration','frequency','effect','prerequisite')}
        else:
            source_id=r['engineIndex'];ident=f"{r['owner']}.engine[{source_id}]";sha=r['textSha256'];proc={'text':r['text']}
        old=known.get(ident,{})
        if old:assert old['sourceSha256']==sha
        rows.append({'bindingId':ident,'sourceKind':r['kind'],'sourcePath':r['path'],'sourceId':source_id,
                     'sourceSha256':sha,'sourceProcedure':proc,'candidateOrigin':r.get('candidateOrigin','Remaining original lexical candidate'),
                     'classification':old.get('classification'),'status':old.get('status','UNREVIEWED; first source conference pending'),
                     'operationalOverrides':old.get('operationalOverrides',[]),'reviewEvidence':old.get('reviewEvidence',[]),
                     'openIssues':old.get('openIssues',['Classify exact source role and resolve source exceptions before implementation.'])})
    data={k:v for k,v in prior.items() if k!='bindings'}
    data.setdefault('status','UNREVIEWED:80+5 first source conference submitted')
    data.setdefault('scope','80 exact passages:74 remaining original candidates+6 semantic supplements;5 frozen shared supports. Includes incidental tempHP/guards and prior component reviews; not full-card/system completion.')
    data['bindings']=rows
    PATH.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Remaining lifecycle source register','',f"**{data['status']}**",'',data['scope'],'',
           '[Source integrity](REMAINING_LIFECYCLE_SOURCE_VALIDATION.json). Original text is preserved.','']
    for r in rows:
        lines+=['## '+r['bindingId'],'',f"**{r['status']}** · {r['classification'] or 'Awaiting classification'}",'',
                f"Source {r['sourcePath']} / {r['sourceId']} · SHA256 {r['sourceSha256']}",'']
        for k,v in r['sourceProcedure'].items():
            if v is not None:lines += [f'**{k}:** {v}','']
        for v in r['operationalOverrides']:lines+=['**Overlay:** '+v,'']
        for v in r['openIssues']:lines+=['**Open:** '+v,'']
    (ROOT/'docs/mechanics/REMAINING_LIFECYCLE_SOURCE_BINDINGS.md').write_text('\n'.join(lines),encoding='utf-8')
    print('Rendered80 exact roles preserving individual review/deferred statuses.')

if __name__=='__main__':main()
