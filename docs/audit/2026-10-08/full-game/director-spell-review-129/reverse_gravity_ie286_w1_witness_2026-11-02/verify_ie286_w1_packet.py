from pathlib import Path
import json, hashlib, math
ROOT=Path(__file__).resolve().parent
def h(b): return hashlib.sha256(b).hexdigest()
def cj(v): return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
manifest=json.loads((ROOT/'WITNESS_PACKET_MANIFEST.json').read_text(encoding='utf-8'))
assert len(manifest['cases'])==3
checks=[]
for ent in manifest['cases']:
 p=ROOT/ent['path']; raw=p.read_bytes(); d=json.loads(raw)
 assert h(raw)==ent['sha256'],('file hash',p.name)
 assert d['sourceBinding']['caseId']==ent['caseId']
 assert d['sourceBinding']['eventId']==ent['eventId']
 assert h(cj(d['historicalSourceStates']['beforeLanding']))==d['sourceBinding']['observedBeforeSHA256']
 assert h(cj(d['historicalSourceStates']['afterLandingBeforeDamage']))==d['sourceBinding']['observedAfterSHA256']
 assert d['historicalSourceStates']['sourceLayerHashes']=={'before':d['sourceBinding']['observedBeforeSHA256'],'after':d['sourceBinding']['observedAfterSHA256']}
 before=d['historicalSourceStates']['beforeLanding']; landed=d['historicalSourceStates']['afterLandingBeforeDamage']; height=d['timeline']['landingFeet']
 assert before['time']==6.133 and landed['time']==6.15
 assert before['items']['crate']['position']==[20,0,height] and landed['items']['crate']['position']==[20,0,0]
 overlays=d['testOnlyOverlayStates']; assert h(cj(overlays['beforeLanding']))==overlays['canonicalSha256']['beforeLanding']
 assert h(cj(overlays['afterLandingBeforeImpact']))==overlays['canonicalSha256']['afterLandingBeforeImpact']
 assert h(cj(overlays['afterImpactAndSettlement']))==overlays['canonicalSha256']['afterImpactAndSettlement']
 assert [x['sequence'] for x in d['operations']['forward']]==[1,2,3]
 assert [x['sequence'] for x in d['operations']['inverse']]==[1,2,3]
 assert d['operations']['forward'][0]['beforeSHA256']==d['operations']['inverse'][2]['toSHA256']
 assert d['operations']['forward'][0]['afterSHA256']==d['operations']['inverse'][2]['fromSHA256']
 assert d['operations']['forward'][1]['fromOverlayState']=='beforeLanding' and d['operations']['forward'][1]['toOverlayState']=='afterLandingBeforeImpact'
 assert d['operations']['forward'][2]['fromOverlayState']=='afterLandingBeforeImpact' and d['operations']['forward'][2]['toOverlayState']=='afterImpactAndSettlement'
 assert d['timeline']['noAdditionalTimeAdvance'] is True
 assert d['impactLedger']['impactOnce'] is True
 assert d['propertyAndMassLedger']['conserved'] is True
 assert d['propertyAndMassLedger']['physicalMassAfterLb']==20
 assert d['propertyAndMassLedger']['ownershipTransfer'] is False and d['propertyAndMassLedger']['duplication'] is False and d['propertyAndMassLedger']['lootAward'] is False
 assert d['classification']=='OWNER_ADOPTED_BRANCH_SCOPED_TEST_ONLY_WITNESS_NOT_SEALED'
 assert d['status']['sealed'] is False and d['status']['identityAccepted'] is False and d['status']['identityApplied'] is False
 objs=overlays['afterImpactAndSettlement']['objects']
 if height==60:
  assert len(objs)==2 and objs[0]['id']=='crate' and objs[0]['durability']['current']==5 and objs[1]['id']=='crate:content:cloth-01' and objs[1]['durability']['current']==4
  assert d['propertyAndMassLedger']['componentsLb']=={'crateStructure':18,'crateContentCloth01':2}
  assert objs[1]['containedBy']=='crate' and objs[1]['minCorner']==[22,2,0.02]
  assert all(f['caseId'].endswith('-A') for f in [d['sourceBinding']]) if ent['caseId'].endswith('-A') else True
 else:
  assert [o['id'] for o in objs]==['crate','crate:content:cloth-01','crate:fragment:01','crate:fragment:02','crate:fragment:03','crate:fragment:04']
  frags=objs[2:]; assert sum(x['massLb'] for x in frags)==18
  assert d['propertyAndMassLedger']['componentsLb']=={'crateStructureFragments':[4.5,4.5,4.5,4.5],'crateContentCloth01':2}
  assert objs[0]['physicalObject'] is False and objs[0]['massLb']==0
  # Check strict positive-volume intersection; boundary contact is allowed.
  physical=[o for o in objs if o.get('massLb',0)>0]
  def overlap(a,b):
   return all(min(a['minCorner'][i]+a['envelopeFeet'][i],b['minCorner'][i]+b['envelopeFeet'][i])-max(a['minCorner'][i],b['minCorner'][i])>1e-9 for i in range(3))
  for i,a in enumerate(physical):
   for b in physical[i+1:]: assert not overlap(a,b),(a['id'],b['id'])
 checks.append({'file':p.name,'sha256':h(raw),'sourceBefore':d['sourceBinding']['observedBeforeSHA256'],'sourceAfterLanding':d['sourceBinding']['observedAfterSHA256'],'overlayHashes':overlays['canonicalSha256'],'massAfterLb':d['propertyAndMassLedger']['physicalMassAfterLb'],'result':'PASS'})
print(json.dumps({'packet':manifest['id'],'caseCount':len(checks),'checks':checks},indent=2))
