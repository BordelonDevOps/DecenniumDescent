"""Integrity/coverage of supplied bindings, not proof of full mechanical execution."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]


def main():
 data=json.loads((ROOT/'data/playtest/control_state_bindings.json').read_text(encoding='utf-8'))
 coverage=json.loads((ROOT/'data/playtest/control_state_coverage.json').read_text(encoding='utf-8'))
 packets=[json.loads((GAME/'docs/audit/2026-10-08/full-game'/name).read_text(encoding='utf-8')) for name in ('CONTROL_STATE_SOURCE_PACKET.json','CONTROL_STATE_SUPPLEMENT_SOURCE_PACKET.json')]
 expected={}
 for packet in packets:
  for r in packet['records']:
   kind=r['kind'];owner=r.get('owner','ordinary')
   ident=r['card']['id'] if kind=='class-card' else r['engineIndex'] if kind=='class-engine' else r['spellId']
   key=f'{kind}:{owner}:{ident}'
   if kind=='class-card': procedure={k:r['card'].get(k) for k in ('name','activation','cost','rangeAndTarget','duration','frequency','effect','prerequisite')}
   elif kind=='class-engine':procedure={'effect':r['text']}
   else:procedure=r['operational']
   expected[key]=(r,procedure)
 bindings={b['bindingId']:b for b in data['bindings']}
 assert len(bindings)==len(data['bindings'])==219
 assert set(bindings)==set(expected)=={r['candidateId'] for r in coverage['candidates']}
 components={c['mechanicalId']:c for c in data['componentIndex']}
 assert len(components)==len(data['componentIndex'])
 definitions=json.loads((ROOT/'data/playtest/condition_playtests.json').read_text(encoding='utf-8'))['conditions']
 core={'core.'+d['id'] for d in definitions}
 counts={}
 for ident,b in bindings.items():
  source,procedure=expected[ident]
  assert b['sourcePath']==source['path'],ident
  assert b['sourceSha256']==source.get('sourceObjectSha256',source.get('textSha256',source.get('operationalSha256'))),ident
  assert b['sourceProcedure']==procedure,ident
  assert b['classification'] in ('STATE','APPLY','HOOK','BOOK','NONSTATE','DEFER','ALREADY'),ident
  counts[b['classification']]=counts.get(b['classification'],0)+1
  if b['classification'] in ('STATE','APPLY'):assert b['componentIds'],ident
  for component in b['componentIds']:
   assert component in components,(ident,component)
   assert ident in components[component]['applicationBindings'],(ident,component)
   if component.startswith('core.'):assert component in core,component
  for field,reverse in (('modifiesComponents','modifierBindings'),('referencesComponents','referenceBindings')):
   for component in b[field]:
    assert component in components,(ident,field,component)
    assert ident in components[component][reverse]
  for evidence in b['reviewEvidence']:assert (GAME/evidence).is_file(),evidence
 for c in components.values():
  assert len(c['applicationBindings'])==len(set(c['applicationBindings'])),c['mechanicalId']
  for ident in c['applicationBindings']:assert c['mechanicalId'] in bindings[ident]['componentIds']
  for field,reverse in (('modifiesComponents','modifierBindings'),('referencesComponents','referenceBindings')):
   for ident in c[reverse]:assert c['mechanicalId'] in bindings[ident][field]
 assert (ROOT/data['operationalGuide']).is_file()
 for ident in ('core.staggered','monk.echoing-guard.stagger','warrior.brutal-strike.stagger'):
  assert 'classification.staggered' in components[ident]['metadata']
 assert 'classification.elemental-control' not in components['shaman.flask.root']['metadata']
 assert 'eligibility.slowed-foe' not in components['core.restrained']['metadata']
 assert 'eligibility.slowed-foe' not in components['core.grappled']['metadata']
 for ident in ('oracle.bone-whisper.soft-fallback','oracle.ledger-command.soft-fallback','oracle.marquis-glimpse.soft-fallback','oracle.slumber-glimpse.soft-fallback','oracle.moments-pause.soft-fallback','paladin.decree-of-submission.soft-fallback','paladin.echo-of-ages.soft-fallback','oracle.spiral-opens.player-speed-zero'):
  assert 'eligibility.slowed-foe' in components[ident]['metadata'],ident
 assert 'eligibility.slowed-foe' not in components['oracle.spiral-opens.forced-echo']['metadata']
 for ident in ('ordinary.ray-of-frost.slow','ordinary.frost-arrow.slow'):
  assert 'classification.elemental-control' in components[ident]['metadata']
 stars=bindings['class-card:oracle:oracle.supplement.stars.stars-revelation-mastery']
 assert stars['classification']=='HOOK' and not stars['componentIds']
 assert 'oracle.guiding-bolt.enhanced-slow' in stars['modifiesComponents']
 flask=bindings['class-card:shaman:shaman.base.flask-use']
 assert not flask['componentIds'] and set(flask['referencesComponents'])=={'shaman.flask.burn','shaman.flask.root','shaman.flask.weaken'}
 arch=bindings['class-card:mage:mage.arch.elemental-mastery']
 assert not arch['componentIds'] and 'mage.cold-focus.glacier' in arch['modifiesComponents']
 report={'status':'PASS','scope':'219 supplied binding/source/coverage identities and component links. No complete-card execution, exhaustive-source or balance claim.',
         'sourceBindings':len(bindings),'componentIdentities':len(components),'classifications':counts,
         'issues':[],'reviewStatus':data['status']}
 (ROOT/'docs/mechanics/CONTROL_BINDING_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
 print(f"PASS {len(bindings)} source bindings; {len(components)} component identities; exact procedures preserved.")


if __name__=='__main__':main()
