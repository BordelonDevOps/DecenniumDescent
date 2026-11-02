from __future__ import annotations
import hashlib, json, pathlib, zipfile, io, sys
sys.stdout.reconfigure(encoding='utf-8')
out=pathlib.Path(__file__).resolve().parent
root=out.parents[5]  # repository root from .../docs/audit/2026-10-08/full-game/director-spell-review-129/<packet>
record=json.loads((out/'B01_SOURCE_QUALIFICATION_470.json').read_text(encoding='utf-8'))
extract=json.loads((out/'B01_CANDIDATE_EXTRACTS_470.json').read_text(encoding='utf-8'))
cases=json.loads((out/'B01_HELD_CASE_EXTRACTS_470.json').read_text(encoding='utf-8'))

def digest(b): return hashlib.sha256(b).hexdigest()
for key in ['directorRequirements','directorHoldDecision','priorB02SourceQualification417','priorCrossbind466','currentCatalog','directorPacket306Archive']:
 b=record['sourceBindings'][key]; raw=(root/b['path']).read_bytes(); assert len(raw)==b['bytes'] and digest(raw)==b['sha256'], key
cat= json.loads((root/record['sourceBindings']['currentCatalog']['path']).read_text(encoding='utf-8'))
assert len(record['candidateProducers'])==10==extract['candidateCount']
for c in record['candidateProducers']:
 s=cat['spells'][c['catalogIndex']]
 assert s['id']==c['spellId'] and s['status']=='blocked-pending-operational-review' and s.get('operational') is None
 assert c['sourceSha256']==record['sourceBindings']['currentCatalog']['sha256']
 assert c['authoredSummary']==s['source']['original']['placements'][0]['summary']
arc=(root/record['sourceBindings']['directorPacket306Archive']['path']).read_bytes()
with zipfile.ZipFile(io.BytesIO(arc)) as z:
 for item_key, file_key in [('environmentCaseMember','heldEnvironmentLead'),('positiveShellCaseMember','creatureAttributedContrast')]:
  bind=record['sourceBindings'][item_key]; raw=z.read(bind['memberPath']); assert len(raw)==bind['memberBytes'] and digest(raw)==bind['memberSha256']
  d=json.loads(raw)
  if item_key=='environmentCaseMember':
   assert d['status']=='HELD_NOT_POSITIVE_EVIDENCE'
   assert d['events'][4]['kind']=='source-premise-held-no-packet-invented'
   assert d['events'][4]['evidence']['noDamageOrResourceClaim'] is True
   assert not any('damage' in e.get('kind','').lower() for e in d['events'])
  else:
   e=d['events'][12]
   assert e['evidence']['actualSource']=='RANK9DEFENSEFORM8129-ELEMENTAL-SHELL-A:cast:2'
   assert e['evidence']['damageType']=='cold' and e['evidence']['authoredRaw']==8
   cast=d['events'][9]['afterState']['actors']['A']['castHistory'][0]
   assert cast['id']==e['evidence']['actualSource'] and cast['spellId']=='ray-of-frost'
assert record['result']=='NO_QUALIFYING_SOURCE_FOUND'
assert record['currentDisposition']['queue']=={'reviewedApplied':830,'pending':18,'acceptedUnapplied':0}
assert record['decisionBoundary']['acceptance'] is False and record['decisionBoundary']['application'] is False
print('PASS: source bindings, all 10 blocked catalog candidates, held B2 negative case, creature-attributed contrast, and queue/decision boundary.')
