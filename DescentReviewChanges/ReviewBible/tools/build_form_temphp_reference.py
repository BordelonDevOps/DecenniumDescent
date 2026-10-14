"""Preserve175 exact role records without inferring discussion/approval."""
from pathlib import Path
import json
from validate_form_temphp_sources import main as validate_sources, digest
ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT.parents[1]/'docs/audit/2026-10-08/full-game'
PATH=ROOT/'data/playtest/form_temphp_bindings.json'
def main():
 validate_sources()
 src=json.loads((AUDIT/'FORM_TEMP_HP_CONFERENCE_SOURCES.json').read_text(encoding='utf-8'))
 prior=json.loads(PATH.read_text(encoding='utf-8')) if PATH.exists() else {}
 known={r['bindingId']:r for r in prior.get('bindings',[])}
 overlays={r['id']:r for r in json.loads((ROOT/'data/public/spell_playtests/catalog.json').read_text(encoding='utf-8'))['spells']}
 rows=[]
 for r in src['records']:
  kind=r['kind'];ident=r['bindingId'];old=known.get(ident,{})
  if kind in ('class-card','bard-card'):
   source_id=r['card']['id'];sha=r['sourceObjectSha256'];proc={k:v for k,v in r['card'].items() if k not in ('source','designStatus')}
  elif kind=='class-engine':source_id=r['engineIndex'];sha=r['textSha256'];proc={'text':r['text']}
  elif kind=='v6-source-passage':source_id=r['line'];sha=r['textSha256'];proc={'text':r['text']}
  else:source_id=r['sourceId'];sha=r['sourceObjectSha256'];proc=r['sourceObject']
  if old:assert old['sourceSha256']==sha
  row={'bindingId':ident,'sourceKind':kind,'sourcePath':r.get('path',r.get('sourcePath')),
       'sourceRoot':r.get('sourceRoot','ReviewBible'),'sourceId':source_id,'sourceSha256':sha,
       'sourceProcedure':proc,'classification':old.get('classification'),
       'status':old.get('status','UNREVIEWED: source conference submitted; individual discussion pending'),
       'operationalOverrides':old.get('operationalOverrides',[]),'reviewEvidence':old.get('reviewEvidence',[]),
       'openIssues':old.get('openIssues',['Classify exact source role, reconcile actual gaps, and implement agreed interfaces before closure.'])}
  if kind=='ordinary-spell':
   current=overlays[source_id]
   row.update(currentOverlay=current,overlaySha256=digest(current))
   for key in ('historicalClassifications','historicalOverlay','historicalOverlaySha256'):
    if key in old:row[key]=old[key]
  rows.append(row)
 data={k:v for k,v in prior.items() if k!='bindings'}
 data.setdefault('status','UNREVIEWED:175+5 first source conference submitted')
 data.setdefault('scope',src['scope']);data['bindings']=rows
 PATH.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 lines=['# Form and temporary-HP source register','',f"**{data['status']}**",'',data['scope'],'',
        '[Source integrity](FORM_TEMP_HP_SOURCE_VALIDATION.json). Original objects and historical alternatives remain preserved.','']
 for r in rows:
  lines+=['## '+r['bindingId'],'',f"**{r['status']}** · {r['classification'] or 'Awaiting classification'}",'',
          f"Source {r['sourceRoot']}/{r['sourcePath']} / {r['sourceId']} · SHA256 {r['sourceSha256']}",'',
          '```json',json.dumps(r['sourceProcedure'],ensure_ascii=False,indent=2),'```','']
  for v in r['operationalOverrides']:lines+=['**Overlay:** '+v,'']
  for v in r['openIssues']:lines+=['**Open:** '+v,'']
 (ROOT/'docs/mechanics/FORM_TEMP_HP_SOURCE_BINDINGS.md').write_text('\n'.join(lines),encoding='utf-8')
 print('Rendered175 exact form/tempHP roles preserving individual status; no inferred approval.')
if __name__=='__main__':main()
