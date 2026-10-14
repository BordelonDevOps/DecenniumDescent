"""Source integrity only; cannot imply form/tempHP review or implementation."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]
AUDIT=GAME/'docs/audit/2026-10-08/full-game'
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def validate_reviewed_overlay_evolution(record,current):
 ident=record['sourceId']
 assert ident in {'harmonic-bulwark','polymorph','shapechange','true-polymorph','mass-polymorph'},'Unreviewed overlay evolution'
 path=ROOT/'data/playtest/form_temphp_overlay_evolution.json'
 evidence=json.loads(path.read_text(encoding='utf-8'))['spells'][ident]
 assert evidence['oldOverlaySha256']==record['overlayObjectSha256']==digest(record['overlayObject'])
 assert evidence['newOverlaySha256']==digest(current),'Unrecorded change to reviewed overlay'
 closure=GAME/evidence['reviewClosure']
 assert hashlib.sha256(closure.read_bytes()).hexdigest()==evidence['reviewClosureSha256'],'Review closure changed'
 assert 'REVIEWED / reference-VALIDATED' in closure.read_text(encoding='utf-8')
 mutable={'status','operational','reviewFlags'}
 assert {k:v for k,v in record['overlayObject'].items() if k not in mutable}=={k:v for k,v in current.items() if k not in mutable},'Original/access/cost metadata changed'
 assert current['status']=='operational-playtest-draft'
 assert current['operational']['authoringFile']=='data/playtest/spell_drafts/batch_transformations.json'
 assert evidence['reviewClosure'] in current['operational']['reviewEvidence']
def main():
 data=json.loads((AUDIT/'FORM_TEMP_HP_CONFERENCE_SOURCES.json').read_text(encoding='utf-8'))
 cache={};ids=set()
 for r in data['records']:
  ident=r['bindingId'];assert ident not in ids;ids.add(ident)
  kind=r['kind'];p=r.get('path',r.get('sourcePath'))
  if kind=='v6-source-passage':
   lines=(GAME/p).read_text(encoding='utf-8').splitlines();text=lines[r['line']-1]
   assert text==r['text'] and hashlib.sha256(text.encode()).hexdigest()==r['textSha256'];continue
  if p not in cache:
   text=(ROOT/p).read_text(encoding='utf-8')
   if kind=='feat':obj=json.JSONDecoder().raw_decode(text.split('export const feats = ',1)[1])[0]
   elif kind=='ordinary-spell':obj=json.JSONDecoder().raw_decode(text.split('export const SPELLS = ',1)[1])[0]
   else:obj=json.loads(text)
   cache[p]=obj
  obj=cache[p]
  if kind=='class-engine':
   text=obj['engine'][r['engineIndex']];assert text==r['text'] and hashlib.sha256(text.encode()).hexdigest()==r['textSha256'];continue
  if kind in ('class-card','bard-card'):original=next(c for c in obj['cards'] if c['id']==r['card']['id'])
  elif kind=='feat':original=next(c for c in obj if c['id']==r['sourceId'])
  else:
   original=obj[r['sourceId']];op=r['overlayPath']
   if op not in cache:cache[op]=json.loads((ROOT/op).read_text(encoding='utf-8'))
   overlay=next(c for c in cache[op]['spells'] if c['id']==r['sourceId'])
   if digest(overlay)!=r['overlayObjectSha256']:validate_reviewed_overlay_evolution(r,overlay)
  assert digest(original)==r['sourceObjectSha256'],ident+' original changed'
 for s in data['supportingSources']:
  root=GAME if s.get('sourceRoot')=='game' else ROOT
  file=root/s['sourcePath'];text=file.read_text(encoding='utf-8')
  assert s['text'] in text,s['sourcePath']
  if 'fullFileSha256' in s:assert hashlib.sha256(file.read_bytes()).hexdigest()==s['fullFileSha256']
  if 'textSha256' in s:assert hashlib.sha256(s['text'].encode()).hexdigest()==s['textSha256']
 druid=json.loads((ROOT/'data/public/class_playtests/druid.json').read_text(encoding='utf-8'))
 assert digest({k:druid[k] for k in data['druidMetadata']})==data['druidMetadataSha256']
 assert len(ids)==175 and len(data['supportingSources'])==5
 result={'status':'PASS','meaning':'Source preservation/integrity only, not discussion or implementation approval',
         'sourceRecords':len(ids),'supportingPassages':5,'druidMetadata':'PASS'}
 (ROOT/'docs/mechanics/FORM_TEMP_HP_SOURCE_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print('PASS175 form/tempHP source records+5 supports and Druid metadata; integrity only.')
if __name__=='__main__':main()
