"""Validate the lexical pulse candidate set while preserving review decisions."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT.parents[1]/'docs/audit/2026-10-08/full-game'
DATA=ROOT/'data/playtest/healing_pulse_bindings.json'
def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def main():
    sources=json.loads((AUDIT/'HEALING_PULSE_SOURCE_CANDIDATES.json').read_text(encoding='utf-8'))
    prior=json.loads(DATA.read_text(encoding='utf-8')) if DATA.exists() else {'bindings':[]}
    known={b['bindingId']:b for b in prior['bindings']}
    loaded={};rows=[];issues=[]
    for r in sources['classRecords']:
        path=r['path']
        if path not in loaded:loaded[path]=json.loads((ROOT/path).read_text(encoding='utf-8'))
        if r['kind']=='class-card':
            captured=r['card'];ident=source_id=captured['id'];sha=r['sourceObjectSha256']
            actual=next((c for c in loaded[path]['cards'] if c['id']==ident),None)
            valid=actual==captured and digest(captured)==sha
            procedure={k:captured.get(k) for k in ('name','activation','cost','rangeAndTarget','duration','frequency','effect')}
        else:
            source_id=r['engineIndex'];ident=f"{r['owner']}.engine[{source_id}]"
            captured=r['text'];sha=r['textSha256'];procedure={'text':captured}
            valid=loaded[path]['engine'][source_id]==captured and hashlib.sha256(captured.encode()).hexdigest()==sha
        old=known.get(ident,{})
        if not valid or (old and old['sourceSha256']!=sha):issues.append('Source drift '+ident)
        rows.append({'bindingId':ident,'sourceKind':r['kind'],'sourcePath':path,'sourceId':source_id,'sourceSha256':sha,
                     'sourceProcedure':procedure,'status':old.get('status','UNREVIEWED; conference submitted'),
                     'classification':old.get('classification'),'operationalOverrides':old.get('operationalOverrides',[]),
                     'reviewEvidence':old.get('reviewEvidence',[]),
                     'openIssues':old.get('openIssues',['Individual scheduling role and boundaries pending; candidate inclusion is not semantic completion.'])})
    if len(rows)!=100 or len({r['bindingId'] for r in rows})!=100:issues.append('Expected100 distinct candidates')
    report={'status':'FAIL' if issues else 'PASS','exactRecords':len(rows),'scope':'100 exact class candidate passages, including guards and exclusions. Source integrity only, not complete game zone coverage.','issues':issues}
    (ROOT/'docs/mechanics/HEALING_PULSE_SOURCE_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    if issues:raise AssertionError(issues)
    data={k:v for k,v in prior.items() if k!='bindings'}
    data.setdefault('status','IN_PROGRESS')
    data.setdefault('scope','100 lexical healing/zone/turn candidates. Classify exclusions and already-reviewed interfaces separately; no broad class or zone completeness claim.')
    data['bindings']=rows
    DATA.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Recurring healing and zone source register','',f"**{data['status']} —100 supplied records.**",'',
           'Original sources remain unchanged. Inclusion can mean a guard or exclusion; review status applies only to the stated role.','',
           '[Source integrity](HEALING_PULSE_SOURCE_VALIDATION.json)','']
    for b in rows:
        lines += ['## '+b['bindingId'],'',f"**{b['status']}** · {b['classification'] or 'Awaiting classification'}",'',
                  f"Source {b['sourcePath']} / {b['sourceId']} · SHA256 {b['sourceSha256']}.",'']
        for k,v in b['sourceProcedure'].items():
            if v is not None:lines += [f'**{k}:** {v}','']
        for v in b['operationalOverrides']:lines += ['**Overlay:** '+v,'']
        for v in b['openIssues']:lines += ['**Open:** '+v,'']
    (ROOT/'docs/mechanics/HEALING_PULSE_SOURCE_BINDINGS.md').write_text('\n'.join(lines),encoding='utf-8')
    print('PASS100 exact pulse candidate sources; originals preserved.')
if __name__=='__main__':main()
