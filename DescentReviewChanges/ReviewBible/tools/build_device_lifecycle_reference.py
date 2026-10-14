"""Preserve individual source roles for the74-passage device/Totem review."""
from pathlib import Path
import json
from validate_device_lifecycle_sources import main as validate_sources
ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT.parents[1]/'docs/audit/2026-10-08/full-game'
DATA=ROOT/'data/playtest/device_lifecycle_bindings.json'
def main():
    validate_sources()
    source=json.loads((AUDIT/'DEVICE_LIFECYCLE_SOURCE_CANDIDATES.json').read_text(encoding='utf-8'))
    prior=json.loads(DATA.read_text(encoding='utf-8')) if DATA.exists() else {'bindings':[]}
    known={b['bindingId']:b for b in prior['bindings']};rows=[]
    for r in source['classRecords']:
        if r['kind']=='class-card':
            c=r['card'];ident=source_id=c['id'];sha=r['sourceObjectSha256']
            procedure={k:c.get(k) for k in ('name','activation','cost','rangeAndTarget','duration','frequency','effect')}
        else:
            source_id=r['engineIndex'];ident=f"{r['owner']}.engine[{source_id}]";sha=r['textSha256'];procedure={'text':r['text']}
        old=known.get(ident,{})
        if old:assert old['sourceSha256']==sha
        rows.append({'bindingId':ident,'sourceKind':r['kind'],'sourcePath':r['path'],'sourceId':source_id,'sourceSha256':sha,
                     'candidateOrigin':r.get('candidateOrigin','Lexical candidate inventory'),
                     'sourceProcedure':procedure,'status':old.get('status','UNREVIEWED; source conference submitted'),
                     'classification':old.get('classification'),'operationalOverrides':old.get('operationalOverrides',[]),
                     'reviewEvidence':old.get('reviewEvidence',[]),'openIssues':old.get('openIssues',['Individual lifecycle/command role and source conflicts pending.'])})
    data={k:v for k,v in prior.items() if k!='bindings'}
    data.setdefault('status','IN_PROGRESS')
    data.setdefault('scope','74 supplied Tinker/Shaman source roles plus3 shared paragraphs. Includes73 lexical candidates and MagneticWall semantic supplement; no full class or companion-system completion claim.')
    data['bindings']=rows
    DATA.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Device, Totem and command source register','',f"**{data['status']} —74 exact class records plus3 shared paragraphs.**",'',
           '[Source integrity](DEVICE_LIFECYCLE_SOURCE_VALIDATION.json). Original sources remain preserved. Individual roles below are separate from complete card behavior.','']
    for b in rows:
        lines+=['## '+b['bindingId'],'',f"**{b['status']}** · {b['classification'] or 'Awaiting classification'}",'',
                f"Source {b['sourcePath']} / {b['sourceId']} · SHA256 {b['sourceSha256']}.",'',b['candidateOrigin'],'']
        for k,v in b['sourceProcedure'].items():
            if v is not None:lines += [f'**{k}:** {v}','']
        for v in b['operationalOverrides']:lines+=['**Overlay:** '+v,'']
        for v in b['openIssues']:lines+=['**Open:** '+v,'']
    (ROOT/'docs/mechanics/DEVICE_LIFECYCLE_SOURCE_BINDINGS.md').write_text('\n'.join(lines),encoding='utf-8')
    print('Rendered74 source roles; review decisions preserved.')
if __name__=='__main__':main()
