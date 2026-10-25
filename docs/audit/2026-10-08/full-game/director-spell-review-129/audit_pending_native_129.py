from pathlib import Path
import json, hashlib, datetime, collections
G=Path(r'C:\Github\DecenniumDescent')
A=G/'docs/audit/2026-10-08/full-game'
D=A/'director-spell-review-129'
R=G/'DescentReviewChanges/ReviewBible'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,o): p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
q=read(A/'spell-review-resume-116/CURRENT_SPELL_QUEUE_129.json')
catpath=R/'data/public/spell_playtests/catalog.json'; cat=read(catpath)
ixpath=R/'data/public/spell_playtests/authored_review_index.json'; ix=read(ixpath)
pending={x['id']:x for x in ix['entries'] if x['authoredStatus'] in ('pending-authored-procedure','receipt-only-post-push-cosmology')}
catalog={s['id']:(i,s) for i,s in enumerate(cat['spells'])}
rows=[]; issues=[]; bindings=[]
for g in q['groups']:
    if g['currentPhase'].startswith('applied'): continue
    cp=G/g['candidate']['path']; c=read(cp)
    bindings.append({'group':g['group'],'path':str(cp),'sha256':sha(cp),'bytes':cp.stat().st_size,'matchesQueue':sha(cp)==g['candidate']['sha256']})
    for sid in g['identities']:
        ci,n=catalog[sid]
        rr=[(j,r) for j,r in enumerate(c['records']) if r.get('spellId')==sid]
        assert len(rr)==1,(sid,len(rr))
        j,r=rr[0]; native=r.get('completeCurrentCatalogSourceAndAccess')
        assert native is not None,(sid,list(r))
        comparisons={k:native.get(k)==n.get(k) for k in ['id','name','schools','classAccess','additionalRpCost','source']}
        if not all(comparisons.values()): issues.append({'id':sid,'comparisons':comparisons})
        rows.append({'id':sid,'group':g['group'],'currentIndexEntry':pending[sid],'candidatePath':str(cp),'candidateRecordPointer':'/records/'+str(j),'candidateNativePointer':'/records/'+str(j)+'/completeCurrentCatalogSourceAndAccess','currentCatalogPointer':'/spells/'+str(ci),'completeNativeRecord':n,'candidateNativeFieldsMatch':comparisons})
ids=[r['id'] for r in rows]
assert len(ids)==232 and len(set(ids))==232 and set(ids)==set(pending)
out={'id':'PENDING232-NATIVE-SOURCE-GUARD-129','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Read-only source/access and queue audit. Does not accept any spell, select new mechanics or execute supplied programs. Use exact native costs and placements in every review and case.','counts':{'pending':len(rows),'groups':len(bindings),'nativeClassAccessRows':sum(len(r['completeNativeRecord']['classAccess']) for r in rows),'nativePlacements':sum(len(r['completeNativeRecord']['source']['original'].get('placements',[])) for r in rows),'issues':len(issues)},'currentIndex':{'path':str(ixpath),'bytes':ixpath.stat().st_size,'sha256':sha(ixpath)},'currentCatalog':{'path':str(catpath),'bytes':catpath.stat().st_size,'sha256':sha(catpath)},'candidateBindings':bindings,'records':rows,'issues':issues}
write(D/'PENDING232_NATIVE_SOURCE_GUARD_129.json',out)
print(json.dumps({'counts':out['counts'],'issues':issues,'candidateBindingFailures':[x for x in bindings if not x['matchesQueue']]},indent=2))
