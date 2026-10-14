"""Preserve exact39-source evidence and render reviewed/proposed dispositions."""
from pathlib import Path
import hashlib,json,re
from redirection_playtest_rules import PROFILES
ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT.parents[1]/'docs/audit/2026-10-08/full-game'
DATA=ROOT/'data/playtest/redirection_bindings.json'

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()

def main():
    captured=json.loads((AUDIT/'REDIRECTION_SOURCE_CANDIDATES.json').read_text(encoding='utf-8'))
    evidence=(AUDIT/'GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md').read_text(encoding='utf-8')
    discussed={m[0]:(m[1].strip(),m[2].strip()) for m in re.findall(r'^\| `([^`]+)` \| ([^|]+) \| (.+) \|$',evidence,re.M)}
    prior=json.loads(DATA.read_text(encoding='utf-8')) if DATA.exists() else {'bindings':[]}
    known={b['bindingId']:b for b in prior['bindings']}
    rows=[];issues=[];loaded={}
    for r in captured['classRecords']:
        path=r['path']
        if path not in loaded:loaded[path]=json.loads((ROOT/path).read_text(encoding='utf-8'))
        if r['kind']=='class-card':
            c=r['card'];ident=c['id'];sha=r['sourceObjectSha256']
            actual=next((c for c in loaded[path]['cards'] if c['id']==ident),None)
            valid=actual==c and digest(c)==sha
            proc={k:c.get(k) for k in ('name','activation','cost','rangeAndTarget','duration','frequency','effect','prerequisite')}
            source_id=ident
        else:
            source_id=r['engineIndex'];ident=f"{r['owner']}.engine[{source_id}]"
            sha=r['textSha256'];proc={'text':r['text']}
            valid=loaded[path]['engine'][source_id]==r['text'] and hashlib.sha256(r['text'].encode()).hexdigest()==sha
        old=known.get(ident,{})
        if not valid or (old and old['sourceSha256']!=sha):issues.append('Source drift '+ident)
        if ident not in discussed:issues.append('Missing individual classification '+ident)
        role,proposal=discussed.get(ident,('UNREVIEWED',''))
        profile=PROFILES.get(ident)
        contract=None if profile is None else {'phase':profile.phase,'formula':profile.formula,
            'flags':sorted(profile.flags),'blockedResources':sorted(profile.blocked_resources),
            'automatic':profile.automatic,'maximumTransferredRecipients':profile.max_recipients}
        rows.append({'bindingId':ident,'sourceKind':r['kind'],'sourcePath':path,'sourceId':source_id,
                     'sourceSha256':sha,'sourceProcedure':proc,
                     'classification':role,'firstProposal':proposal,'transferContract':contract,
                     'status':old.get('status','DISCUSSED; IMPLEMENTATION_PENDING'),
                     'operationalOverrides':old.get('operationalOverrides',[]),
                     'reviewEvidence':old.get('reviewEvidence',['GPT_REDIRECTION_FIRST_REVIEW_PARTIAL.md']),
                     'openIssues':old.get('openIssues',['Exact implementation and source-boundary review pending.'])})
    if len(rows)!=39 or len({b['bindingId'] for b in rows})!=39:issues.append('Expected39 unique records')
    supporting=prior.get('supportingSources',[])
    for extra in supporting:
        source=json.loads((ROOT/extra['sourcePath']).read_text(encoding='utf-8'))['engine'][extra['engineIndex']]
        if source!=extra['text'] or hashlib.sha256(source.encode()).hexdigest()!=extra['sha256']:
            issues.append('Supporting source drift '+extra['sourcePath'])
    report={'status':'FAIL' if issues else 'PASS','exactRecords':len(rows),'supportingEnginePassages':len(supporting),
            'scope':'Original source equality, hashes and complete individual classification; not proof of semantic completion.','issues':issues}
    (ROOT/'docs/mechanics/REDIRECTION_SOURCE_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    if issues:raise AssertionError(issues)
    data={k:v for k,v in prior.items() if k!='bindings'}
    data.setdefault('status','IN_PROGRESS')
    data.setdefault('scope','39 exact passages: damage transfer, prevention, retargeting, new damage and non-damage exclusions.')
    data['bindings']=rows
    DATA.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Damage sharing source register','',f"**{data['status']} —39 exact passages.** Source integrity and individual discussion do not prove complete feature execution.",'',
           '[Procedure](DAMAGE_SHARING_PLAYTEST.md) · [Integrity](REDIRECTION_SOURCE_VALIDATION.json)','']
    for b in rows:
        lines += ['## '+b['bindingId'],'',f"**{b['status']}** · {b['classification']}",'',
                  f"Source `{b['sourcePath']}` / `{b['sourceId']}` · SHA256 `{b['sourceSha256']}`.",'']
        for k,v in b['sourceProcedure'].items():
            if v is not None:lines += [f'**{k}:** {v}','']
        lines += ['**First proposal (historical; later overrides take precedence):** '+b['firstProposal'],'']
        if b['transferContract']:lines += ['**Transfer contract:** '+json.dumps(b['transferContract'],ensure_ascii=False),'']
        for text in b['operationalOverrides']:lines += ['**Overlay:** '+text,'']
        for text in b['openIssues']:lines += ['**Open:** '+text,'']
    (ROOT/'docs/mechanics/REDIRECTION_SOURCE_BINDINGS.md').write_text('\n'.join(lines),encoding='utf-8')
    print('PASS39 exact redirection sources; original objects preserved.')
if __name__=='__main__':main()
