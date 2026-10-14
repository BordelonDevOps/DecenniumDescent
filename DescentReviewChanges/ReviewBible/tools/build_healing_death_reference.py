"""Maintain source-qualified coverage; preserve dispositions across rebuilds."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT.parents[1]/'docs/audit/2026-10-08/full-game'
DATA=ROOT/'data/playtest/healing_death_bindings.json'
def main():
    initial=json.loads((AUDIT/'HEALING_DEATH_SOURCE_CANDIDATES.json').read_text(encoding='utf-8'))
    extra=json.loads((AUDIT/'HEALING_INTERFACE_SUPPLEMENT.json').read_text(encoding='utf-8'))
    old=json.loads(DATA.read_text(encoding='utf-8')) if DATA.exists() else {'bindings':[]}
    known={b['bindingId']:b for b in old['bindings']}
    bindings=[]
    for r in initial['classRecords']+extra['classRecords']:
        if r['kind']=='class-card':
            c=r['card'];ident=c['id'];digest=r['sourceObjectSha256']
            procedure={k:c.get(k) for k in ('name','activation','cost','rangeAndTarget','duration','frequency','effect','prerequisite')}
        else:
            ident=r['engineIndex'];digest=r['textSha256'];procedure={'text':r['text']}
        bindings.append({'bindingId':f"{r['kind']}:{r['owner']}:{ident}",'sourceKind':r['kind'],'sourcePath':r['path'],'sourceId':ident,'sourceSha256':digest,'sourceProcedure':procedure,
                         'scope':'Healing/death-related parts of this exact source; not all-card execution.'})
    for r in initial['spellCatalogRecords']:
        s=r['spell']
        bindings.append({'bindingId':'ordinary-spell:'+r['spellId'],'sourceKind':'ordinary-spell-catalog','sourcePath':'data/public/spell_playtests/catalog.json','sourceId':r['spellId'],'sourceSha256':r['sourceObjectSha256'],
                         'sourceProcedure':{'name':s['name'],'classAccess':s['classAccess'],'coreEntries':s['source']['coreEntries']},
                         'scope':'Preserved catalog source; the operational overlay has separate individual review and validation.'})
    for b in bindings:
        prior=known.get(b['bindingId'])
        defaults={'status':'UNREVIEWED','classification':None,'operationalOverrides':[],'reviewEvidence':[],
                  'openIssues':['Finish exact source disposition and implementation review.']}
        if prior:
            assert prior['sourceSha256']==b['sourceSha256'],('Source changed',b['bindingId'])
        for key,value in defaults.items():b[key]=prior.get(key,value) if prior else value
    data={'schemaVersion':'1.0','status':old.get('status','IN_PROGRESS'),
          'scope':'Original85 sources plus68 selected supplemental passages. The further131 semantic candidates and other content domains remain separately open.',
          'bindings':bindings}
    DATA.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Healing and death source reference','',f"**{data['status']} — {len(bindings)} selected source records.** An index is not a reviewed procedure.",'',
           'Exact costs, actions, target limits, clocks and restrictions are retained below. Operational overrides only supersede the stated part of a procedure; original objects remain unchanged.','']
    for b in bindings:
        lines.extend([f"## {b['bindingId']}",'',f"**{b['status']}** · {b['classification'] or 'Awaiting classification'}",'',
                      f"Source: `{b['sourcePath']}` / `{b['sourceId']}`. SHA256 `{b['sourceSha256']}`.",''])
        for key,value in b['sourceProcedure'].items():
            if value is not None:lines.extend([f'**{key}:** '+(json.dumps(value,ensure_ascii=False) if isinstance(value,(dict,list)) else str(value)),''])
        if b['operationalOverrides']:lines.extend(['**Operational overlay:** '+' '.join(b['operationalOverrides']),''])
    (ROOT/'docs/mechanics/HEALING_DEATH_SOURCE_BINDINGS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(f'Rendered {len(bindings)} source records; {sum(b["status"]=="UNREVIEWED" for b in bindings)} still unreviewed.')
if __name__=='__main__':main()
