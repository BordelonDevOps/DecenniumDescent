"""Verify the preserved healing/death evidence; no operational completeness claim."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT.parents[1]/'docs/audit/2026-10-08/full-game'
def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def main():
    data=json.loads((AUDIT/'HEALING_DEATH_SOURCE_CANDIDATES.json').read_text(encoding='utf-8'))
    supplement=json.loads((AUDIT/'HEALING_INTERFACE_SUPPLEMENT.json').read_text(encoding='utf-8'))
    issues=[];seen=set();loaded={}
    for r in data['classRecords']+supplement['classRecords']:
        if r['path'] not in loaded:loaded[r['path']]=json.loads((ROOT/r['path']).read_text(encoding='utf-8'))
        source=loaded[r['path']]
        if r['kind']=='class-card':
            ident=r['card']['id'];captured=r['card']
            actual=next((c for c in source['cards'] if c['id']==ident),None)
            valid=actual==captured and digest(captured)==r['sourceObjectSha256']
        else:
            ident=r['engineIndex'];captured=r['text'];actual=source['engine'][ident]
            valid=actual==captured and hashlib.sha256(captured.encode()).hexdigest()==r['textSha256']
        key=(r['kind'],r['path'],str(ident))
        if key in seen:issues.append('Duplicate '+str(key))
        seen.add(key)
        if not valid:issues.append('Source mismatch '+str(key))
    catalog=json.loads((ROOT/'data/public/spell_playtests/catalog.json').read_text(encoding='utf-8'))
    current={s['id']:s for s in catalog['spells']}
    for r in data['spellCatalogRecords']:
        key=('spell',r['spellId']);captured=r['spell'];actual=current.get(r['spellId'])
        if key in seen:issues.append('Duplicate '+str(key))
        seen.add(key)
        # Operational overlays can later be authored; preserved source identity/access may not drift.
        if digest(captured)!=r['sourceObjectSha256'] or actual is None or any(actual[k]!=captured[k] for k in ('id','source','classAccess')):
            issues.append('Spell evidence mismatch '+r['spellId'])
    expected=data['counts']['classCards']+data['counts']['classEngines']+data['counts']['spellCatalogObjects']+sum(supplement['counts'].values())
    if len(seen)!=expected:issues.append('Source count mismatch')
    report={'status':'FAIL' if issues else 'PASS','scope':'Preserved original85 plus68 supplemental objects/passages and unchanged source provenance only; not semantic closure or individual spell approval.',
            'exactRecords':len(seen),'originalCounts':data['counts'],'supplementCounts':supplement['counts'],'issues':issues}
    (ROOT/'docs/mechanics/HEALING_DEATH_SOURCE_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f"{report['status']}: {len(seen)} exact healing/death source records")
    if issues:raise SystemExit(1)
if __name__=='__main__':main()
