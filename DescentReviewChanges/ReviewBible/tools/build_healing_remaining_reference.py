"""Track the remaining131 sources without expanding the prior153-scope closure."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT.parents[1]/'docs/audit/2026-10-08/full-game'
DATA=ROOT/'data/playtest/healing_remaining_bindings.json'

def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()

def main():
    sources=json.loads((AUDIT/'HEALING_REMAINING_SOURCE_CANDIDATES.json').read_text(encoding='utf-8'))
    prior=json.loads(DATA.read_text(encoding='utf-8')) if DATA.exists() else {'bindings':[]}
    known={b['bindingId']:b for b in prior['bindings']};rows=[];issues=[];loaded={}
    for r in sources['classRecords']:
        path=r['path']
        if path not in loaded:loaded[path]=json.loads((ROOT/path).read_text(encoding='utf-8'))
        if r['kind']=='class-card':
            ident=r['card']['id'];captured=r['card'];sha=r['sourceObjectSha256']
            actual=next((c for c in loaded[path]['cards'] if c['id']==ident),None)
            valid=actual==captured and digest(captured)==sha
            procedure={k:captured.get(k) for k in ('name','activation','cost','rangeAndTarget','duration','frequency','effect','prerequisite')}
        else:
            ident=r['engineIndex'];captured=r['text'];sha=r['textSha256']
            valid=loaded[path]['engine'][ident]==captured and hashlib.sha256(captured.encode()).hexdigest()==sha
            procedure={'text':captured}
        key=f"{r['kind']}:{r['owner']}:{ident}"
        if not valid:issues.append('Source mismatch '+key)
        old=known.get(key,{})
        if old and old['sourceSha256']!=sha:issues.append('Recorded provenance drift '+key)
        rows.append({'bindingId':key,'sourceKind':r['kind'],'sourcePath':path,'sourceId':ident,'sourceSha256':sha,
                     'sourceProcedure':procedure,'status':old.get('status','UNREVIEWED'),
                     'classification':old.get('classification'),
                     'operationalOverrides':old.get('operationalOverrides',[]),
                     'reviewEvidence':old.get('reviewEvidence',[]),
                     'reviewedInterfaces':old.get('reviewedInterfaces',[]),
                     'openIssues':old.get('openIssues',['Individual source disposition and identified interface decisions pending.'])})
    if len(rows)!=131 or len({r['bindingId'] for r in rows})!=131:issues.append('Expected131 distinct sources')
    status='FAIL' if issues else 'PASS'
    report={'status':status,'scope':'Exact source identity/procedure/hash only; no semantic completion claim.',
            'exactRecords':len(rows),'issues':issues}
    (ROOT/'docs/mechanics/HEALING_REMAINING_SOURCE_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    if issues:raise AssertionError(issues)
    data={'status':'IN_PROGRESS','scope':'Remaining131 class matches outside the previously closed153-source interface. Roles/dependencies and exact source procedures tracked individually.',
          'bindings':rows}
    DATA.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Remaining healing/recovery source register','',
           '**IN PROGRESS —131 exact passages.** This register does not expand the prior153-source closure. Source integrity is distinct from a discussed or operational rule.','',
           '[Healing interface](HEALING_DEATH_PLAYTEST.md) · [Source integrity](HEALING_REMAINING_SOURCE_VALIDATION.json)','']
    for b in rows:
        lines.extend(['## '+b['bindingId'],'',f"**{b['status']}** · {b['classification'] or 'Awaiting individual classification'}",'',
                      f"Source `{b['sourcePath']}` / `{b['sourceId']}` · SHA256 `{b['sourceSha256']}`.",''])
        for key,value in b['sourceProcedure'].items():
            if value is not None:lines.extend([f'**{key}:** {value}',''])
        if b['operationalOverrides']:lines.extend(['**Discussion/overlay:** '+' '.join(b['operationalOverrides']),''])
        for review in b['reviewedInterfaces']:
            lines.extend([f"**Reviewed interface:** [{review['scope']}]({Path(review['guide']).name}). Wider card status remains separate.",''])
        if b['openIssues']:lines.extend(['**Open:** '+' '.join(b['openIssues']),''])
    (ROOT/'docs/mechanics/HEALING_REMAINING_SOURCE_BINDINGS.md').write_text('\n'.join(lines),encoding='utf-8')
    print(f'PASS131 exact remaining sources; {sum(b["status"]=="UNREVIEWED" for b in rows)} awaiting individual disposition.')
if __name__=='__main__':main()
