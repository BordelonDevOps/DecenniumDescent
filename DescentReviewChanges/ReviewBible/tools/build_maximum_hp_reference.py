"""Validate58 captured maximumHP candidates without promoting an interpretation."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT.parents[1]/'docs/audit/2026-10-08/full-game'
DATA=ROOT/'data/playtest/maximum_hp_bindings.json'

def digest(v):
    return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()

def main():
    sources=json.loads((AUDIT/'MAXIMUM_HP_SOURCE_CANDIDATES.json').read_text(encoding='utf-8'))
    prior=json.loads(DATA.read_text(encoding='utf-8')) if DATA.exists() else {'bindings':[]}
    known={r['bindingId']:r for r in prior['bindings']}
    rows=[];issues=[];loaded={}
    feats=json.JSONDecoder().raw_decode((ROOT/'src/data/feats.js').read_text(encoding='utf-8').split('export const feats = ',1)[1])[0]
    for r in sources['classRecords']+sources['featRecords']:
        kind=r.get('kind','feat')
        path=r.get('path',r.get('sourcePath'))
        if kind=='feat':
            ident='feat:'+r['sourceId'];source_id=r['sourceId'];sha=r['sourceObjectSha256']
            captured=r['sourceObject'];actual=next((v for v in feats if v['id']==source_id),None)
            valid=actual==captured and digest(captured)==sha
            proc={k:captured.get(k) for k in ('name','description','prerequisite','effect','legacyEffect','status','source')}
        else:
            if path not in loaded:loaded[path]=json.loads((ROOT/path).read_text(encoding='utf-8'))
            if kind=='class-card':
                captured=r['card'];source_id=ident=captured['id'];sha=r['sourceObjectSha256']
                actual=next((c for c in loaded[path]['cards'] if c['id']==ident),None)
                valid=actual==captured and digest(captured)==sha
                proc={k:captured.get(k) for k in ('name','activation','cost','rangeAndTarget','duration','frequency','effect','prerequisite')}
            else:
                source_id=r['engineIndex'];ident=f"{r['owner']}.engine[{source_id}]"
                sha=r['textSha256'];captured=r['text'];proc={'text':captured}
                valid=loaded[path]['engine'][source_id]==captured and hashlib.sha256(captured.encode()).hexdigest()==sha
        old=known.get(ident,{})
        if not valid or (old and old['sourceSha256']!=sha):issues.append('Source drift '+ident)
        rows.append({'bindingId':ident,'sourceKind':kind,'sourcePath':path,'sourceId':source_id,
                     'sourceSha256':sha,'sourceProcedure':proc,
                     'status':old.get('status','UNREVIEWED; source conference submitted'),
                     'classification':old.get('classification'),
                     'operationalOverrides':old.get('operationalOverrides',[]),
                     'reviewEvidence':old.get('reviewEvidence',[]),
                     'openIssues':old.get('openIssues',['Individual maximumHP/threshold role and composition review pending.'])})
    if len(rows)!=58 or len({r['bindingId'] for r in rows})!=58:issues.append('Expected58 distinct sources')
    report={'status':'FAIL' if issues else 'PASS','exactRecords':len(rows),
            'scope':'51 exact class passages and7 feat records: live source equality and captured hashes only. Not semantic completion of maximumHP or all listed sources.','issues':issues}
    (ROOT/'docs/mechanics/MAXIMUM_HP_SOURCE_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    if issues:raise AssertionError(issues)
    data={k:v for k,v in prior.items() if k!='bindings'}
    data.setdefault('status','IN_PROGRESS')
    data.setdefault('scope','Selected58-source maximumHP/threshold interface. Includes guards/exclusions and prior reviewed percentage healing; no complete feat/companion/character build promotion.')
    data['bindings']=rows
    DATA.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Maximum HP and threshold source register','',f"**{data['status']} —58 exact source records.**",'',
           'Original sources are preserved. Each disposition applies only to the stated maximumHP/threshold role; unrelated card/feat mechanics retain their own review requirements.','',
           '[Source integrity](MAXIMUM_HP_SOURCE_VALIDATION.json)','']
    for b in rows:
        lines += ['## '+b['bindingId'],'',f"**{b['status']}** · {b['classification'] or 'Awaiting individual classification'}",'',
                  f"Source {b['sourcePath']} / {b['sourceId']} · SHA256 {b['sourceSha256']}.",'']
        for k,v in b['sourceProcedure'].items():
            if v is not None:lines += [f'**{k}:** {v}','']
        for v in b['operationalOverrides']:lines += ['**Overlay:** '+v,'']
        for v in b['openIssues']:lines += ['**Open:** '+v,'']
    (ROOT/'docs/mechanics/MAXIMUM_HP_SOURCE_BINDINGS.md').write_text('\n'.join(lines),encoding='utf-8')
    print('PASS58 exact maximumHP/threshold sources; original data unchanged.')
if __name__=='__main__':main()
