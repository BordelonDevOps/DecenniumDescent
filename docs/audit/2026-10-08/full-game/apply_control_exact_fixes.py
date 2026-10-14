"""Apply the four exact-review findings; keep raw conferences and originals intact."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
BASE='docs/audit/2026-10-08/full-game/'
p=ROOT/'data/playtest/control_state_bindings.json'
d=json.loads(p.read_text(encoding='utf-8'))
index={c['mechanicalId']:c for c in d['componentIndex']}
fallbacks='''oracle.bone-whisper.soft-fallback oracle.ledger-command.soft-fallback oracle.marquis-glimpse.soft-fallback oracle.slumber-glimpse.soft-fallback oracle.moments-pause.soft-fallback paladin.decree-of-submission.soft-fallback paladin.echo-of-ages.soft-fallback'''.split()
for ident in fallbacks:
 if 'eligibility.slowed-foe' not in index[ident]['metadata']:index[ident]['metadata'].append('eligibility.slowed-foe')
 index[ident]['activeHookRule']='Only while the printed fallback Speed0/half-Speed component actually applies and is not suppressed/expired; Reaction denial or Charmed alone is insufficient.'
ident='oracle.spiral-opens.player-speed-zero'
index[ident]={'mechanicalId':ident,'applicationBindings':[],'modifierBindings':[],
 'metadata':['eligibility.slowed-foe'],
 'applicationRule':'Only the actual selected player Speed0 branch. Not NPC Forced Echo or a player choosing to repeat the action type.',
 'activeHookRule':'Actual Speed0 branch active and unsuppressed only.'}
for ident in ('ordinary.ray-of-frost.slow','ordinary.frost-arrow.slow'):
 if 'classification.elemental-control' not in index[ident]['metadata']:index[ident]['metadata'].append('classification.elemental-control')
 index[ident]['metadataProvenance']='NEW exact-source semantic classification approved in GPT_CONTROL_EXACT_FINDINGS; not a global cold-spell inference.'
for b in d['bindings']:
 b.setdefault('modifiesComponents',[])
 b.setdefault('referencesComponents',[])
 if b['classification']=='HOOK':
  b['referencesComponents']=sorted(set(b['referencesComponents']+b['componentIds']))
  b['componentIds']=[]
 if b['sourceId']=='oracle.supplement.stars.stars-revelation-mastery':
  b['classification']='HOOK'
  b['componentIds']=[]
  b['modifiesComponents']=['oracle.guiding-bolt.enhanced-slow','oracle.guiding-bolt.star-mark','oracle.constellation-mark']
  b['operationalOverrides'].append('Passive mastery selection; only a later legal Guiding Bolt with the relevant enhancement selected applies the downstream slow. Other selected mastery upgrades retain exact source rules.')
 if b['sourceId']=='oracle.supplement.stars.guiding-bolt':
  if 'oracle.guiding-bolt.enhanced-slow' not in b['componentIds']:b['componentIds'].append('oracle.guiding-bolt.enhanced-slow')
  b['operationalOverrides'].append('Enhanced-slow component applies only if the relevant Stars Revelation Mastery enhancement is selected; no unmodified Guiding Bolt slow.')
 if b['sourceId']=='shaman.base.flask-use':
  b['componentIds']=[]
  b['referencesComponents']=['shaman.flask.burn','shaman.flask.root','shaman.flask.weaken']
  b['operationalOverrides'].append('BOOK wrapper references all three Base profiles. Actual application is source engine[4] selected mode, never duplicate wrapper+engine states.')
 if b['sourceId']=='mage.arch.elemental-mastery':
  b['referencesComponents']=[]
  b['modifiesComponents']=['mage.fire-focus.burn','mage.inferno-lance.burn','mage.elemental-bolt.burn','mage.cold-focus.flat','mage.cold-focus.glacier']
 if b['sourceId']=='shaman.arch.enhanced-elemental-attunement':b['modifiesComponents']=['shaman.elemental-affinity.ice-slow']
 if b['sourceId']=='shaman.hero.soothsayer.balanced-elements':
  b['modifiesComponents']=[c['mechanicalId'] for c in index.values() if 'classification.elemental-control' in c['metadata']]
  b['modifierScope']='Only an owned eligible application with source costs/limits paid; elemental slow and existing eligible Burn procedure remain distinct alternatives. No automated source dispatch.'
 if b['sourceId']=='oracle.supplement.time.the-spiral-opens':
  if 'oracle.spiral-opens.player-speed-zero' not in b['componentIds']:b['componentIds'].append('oracle.spiral-opens.player-speed-zero')
 if b['sourceId']=='mage.hero.elementalist.elemental-fusion':
  b['operationalOverrides'].append('NEW missing-endpoint bridge: Fire+Cold slow ends target next regular END; Cold+Lightning slow/opportunity denial same target-END; Fire+Lightning Reaction denial target next regular START. Non-Focus secondary profiles do not receive Arch Mastery.')
 if b['sourceId']=='mage.hero.elementalist.cascade-storm':
  b['operationalOverrides'].append('Printed cold slow ends SOURCE next regular END; printed lightning Reaction denial SOURCE next regular START. Current-Cold passive may independently trigger on positive cold damage with its own target-END deadline.')
 if b['modifiesComponents'] or b['referencesComponents'] or b['operationalOverrides']:
  if BASE+'GPT_CONTROL_EXACT_FINDINGS.md' not in b['reviewEvidence']:b['reviewEvidence'].append(BASE+'GPT_CONTROL_EXACT_FINDINGS.md')
# Rebuild reverse links with role separation. Existing indexes keep metadata.
for c in index.values():
 c['applicationBindings']=[];c['modifierBindings']=[];c['referenceBindings']=[]
for b in d['bindings']:
 for field,reverse in (('componentIds','applicationBindings'),('modifiesComponents','modifierBindings'),('referencesComponents','referenceBindings')):
  b[field]=sorted(set(b[field]))
  for ident in b[field]:
   assert ident in index,ident
   index[ident][reverse].append(b['bindingId'])
d['componentIndex']=list(index.values())
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
cp=ROOT/'data/playtest/control_state_coverage.json'
coverage=json.loads(cp.read_text(encoding='utf-8'))
bindings={b['bindingId']:b for b in d['bindings']}
for row in coverage['candidates']:
 b=bindings[row['candidateId']]
 row['classification']=b['classification']
 row['bindingIds']=sorted(set(b['componentIds']+b['modifiesComponents']+b['referencesComponents']))
 row['reviewEvidence']=b['reviewEvidence']
coveragepath=cp.write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f"Four findings fixed; {len(index)} component identities; modifier/reference roles explicit.")
