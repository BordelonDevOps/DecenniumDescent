"""Render preserved100 source candidates without promoting their review status."""
from pathlib import Path
import json
from validate_creature_lifecycle_sources import main as validate_sources
ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT.parents[1]/'docs/audit/2026-10-08/full-game'
PATH=ROOT/'data/playtest/creature_lifecycle_bindings.json'
def main():
    validate_sources()
    source=json.loads((AUDIT/'CREATURE_LIFECYCLE_SOURCE_CANDIDATES.json').read_text(encoding='utf-8'))
    prior=json.loads(PATH.read_text(encoding='utf-8')) if PATH.exists() else {}
    known={r['bindingId']:r for r in prior.get('bindings',[])}
    rows=[]
    for r in source['classRecords']:
        if r['kind']=='class-card':
            c=r['card'];source_id=ident=c['id'];sha=r['sourceObjectSha256']
            procedure={k:c.get(k) for k in ('name','activation','cost','rangeAndTarget','duration','frequency','effect')}
        else:
            source_id=r['engineIndex'];ident=f"{r['owner']}.engine[{source_id}]";sha=r['textSha256'];procedure={'text':r['text']}
        old=known.get(ident,{})
        if old:assert old['sourceSha256']==sha
        rows.append({
            'bindingId':ident,'sourceKind':r['kind'],'sourcePath':r['path'],
            'sourceId':source_id,'sourceSha256':sha,
            'candidateOrigin':r.get('candidateOrigin','Original broad lifecycle inventory'),
            'sourceProcedure':procedure,'status':old.get('status','UNREVIEWED; source discussion pending'),
            'classification':old.get('classification'),
            'operationalOverrides':old.get('operationalOverrides',[]),
            'reviewEvidence':old.get('reviewEvidence',[]),
            'openIssues':old.get('openIssues',['Classify exact creature, form, tempHP or guard role before implementation.'])})
    data={k:v for k,v in prior.items() if k!='bindings'}
    data.setdefault('status','UNREVIEWED: source inventory preserved')
    data.setdefault('scope','100 exact five-family candidates:83 original broad passages plus17 semantic supplements;3 frozen shared supporting paragraphs. Not a complete class or companion-system claim.')
    data['bindings']=rows
    PATH.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Creature companion source register','',f"**{data['status']}**",'',
           data['scope'],'','[Source integrity](CREATURE_LIFECYCLE_SOURCE_VALIDATION.json). Original sources remain preserved.','']
    for b in rows:
        lines+=['## '+b['bindingId'],'',f"**{b['status']}** · {b['classification'] or 'Awaiting classification'}",'',
                f"Source {b['sourcePath']} / {b['sourceId']} · SHA256 {b['sourceSha256']}.",'',b['candidateOrigin'],'']
        for k,v in b['sourceProcedure'].items():
            if v is not None:lines += [f'**{k}:** {v}','']
        for v in b['operationalOverrides']:lines+=['**Overlay:** '+v,'']
        for v in b['openIssues']:lines+=['**Open:** '+v,'']
    (ROOT/'docs/mechanics/CREATURE_LIFECYCLE_SOURCE_BINDINGS.md').write_text('\n'.join(lines),encoding='utf-8')
    print('Rendered100 creature/form/tempHP candidate roles without promoting status.')
if __name__=='__main__':main()
