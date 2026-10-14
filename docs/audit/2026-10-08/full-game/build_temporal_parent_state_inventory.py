"""Inventory actual state fields; this is an implementation checklist, not runtime approval."""
from pathlib import Path
import ast
import hashlib
import json

audit=Path(__file__).resolve().parent
root=audit.parents[3]/'DescentReviewChanges/ReviewBible'
policies={
 'DruidState':{
  'owner circle':'immutable original identity / structural source; classify current eligibility',
  'buffers creatures cadence':'canonical shared references; never clone or replace with a second world',
  'current instances':'same-instance anatomy restoration and historical registry; full parent adapter required',
  'long_epoch short_epoch rest_uses attuned shifts buffer_capacity reserve surges surge_capacity':'current real-rest economy and eligibility; never replenish by rewind',
  'regular_index recharges recharge_clock':'current owner recharge timeline; no restore-time tick',
 },
 'OwnerRechargeClock':{'mode now next_tick ticks last_regular anchored':'current one-owner clock across initiative/downtime; all fields conserved and watched'},
 'FormInstance':{
  'instance_id source_id variant large':'same physical/source/profile identity; no fresh entry',
  'expiry':'absolute endpoint plus authenticated same-instance renewal history; policy conference',
  'spent':'snapshot local permission subject to current global payment; historical use retained separately',
  'state':'snapshot anatomy/lifecycle subject to valid current endpoint and parent closure',
  'entry_open':'must be closed at capture/commit; no Broodmother spawn replay',
 },
 'ConcentrationLedger':{'current':'one shared owner/ID/callback slot map; participant restoration needs explicit reference-safe staging; outsiders remain current'},
 'TransformationWorld':{
  'buffers concentration druids':'exact shared host references; no copied callback world',
  'bodies casts links':'canonical object registries; restore classified fields on retained objects',
  'slots':'current persistent enrollment and exact lineage; no duplicate occupant',
  'damage_rounds regular_ends':'current helper numeric/event windows need authenticated iteration-qualified wrapper',
  'damage_events events':'retain complete historical event identity/audit; no replay at restore',
  'commands':'queued/attached source and shared command-ledger adapter required',
 },
 'PhysicalOrigin':{'identity kind size type_tags mass value':'immutable original physical evidence; never replace with current transformed statistics'},
 'Body':{
  'origin':'same immutable original physical record',
  'life':'same canonical Core life object, no independent transformation HP',
  'size mass anatomy':'proposed operative anatomy after lifetime/permanence/external reconciliation',
  'equipment melded lost_items':'current ownership and survival; intersect snapshot meld; legal simultaneous drops',
  'destroyed':'physical provenance/life reconciliation, not a refillable form flag',
  'slot_sponsor controller':'current persistent enrollment/control reconciliation, not generic snapshot assignment',
  'placement_pending placement_conflict':'must be solved in simultaneous geometry preflight; cannot clear by assertion',
 },
 'Cast':{
  'identity spell_id caster rank stats casting_regular_index':'original cast authority and identity; same price/save provenance; actual turn-wrapper required',
  'links':'one complete source closure including protected outsiders',
  'state':'proposed lifecycle subject to terminal/permanent historical events',
 },
 'Link':{
  'identity cast_id target willing':'same target/application/source identities',
  'profile object_template object_size object_mass':'snapshot operative selection plus permanent/current physical reconciliation',
  'deadline':'original absolute endpoint/stabilization marker; never now plus duration',
  'state':'snapshot or conserved permanent lifecycle needs receipts for terminal events',
  'last_switch':'authenticated logical new-iteration turn permission; numeric marker alone insufficient',
  'suppressed':'current exact external suppression authority; cannot rewind a bare flag',
 },
}
files={name:'tools/form_temphp_playtest_rules.py' for name in ('DruidState','OwnerRechargeClock','FormInstance')}
files.update({name:'tools/transformation_spell_playtest_rules.py' for name in policies if name not in files})
rows=[]
for name,groups in policies.items():
    p=root/files[name];tree=ast.parse(p.read_text(encoding='utf-8'))
    cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name==name)
    found=set()
    for n in ast.walk(cls):
        if isinstance(n,ast.Attribute) and isinstance(n.value,ast.Name) and n.value.id=='self' and isinstance(n.ctx,ast.Store):found.add(n.attr)
    for n in cls.body:
        if isinstance(n,ast.AnnAssign) and isinstance(n.target,ast.Name):found.add(n.target.id)
    mapped={field:meaning for names,meaning in groups.items() for field in names.split()}
    assert found==set(mapped),(name,sorted(found-set(mapped)),sorted(set(mapped)-found))
    rows.append({'holder':name,'source':files[name],'sourceSha256':hashlib.sha256(p.read_bytes()).hexdigest(),
                 'fields':mapped,'runtimeAdapterImplemented':False})
forms=json.loads((root/'data/playtest/druid_form_profiles.json').read_text(encoding='utf-8'))['profiles']
packet={'status':'Source-linked state inventory; temporal parent implementation pending',
        'fullTimeLoopOperational':False,'remainingMajorIntegrations':7,'holderCount':len(rows),
        'fieldCount':sum(len(r['fields']) for r in rows),'holders':rows,
        'druidProfiles':[{'sourceId':k,'sourceSha256':v['sourceSha256'],'band':v['sourceProcedure']['band'],
                         'entryBuffer':v['entryBuffer'],'specialPayments':{s:q['payment'] for s,q in v['specials'].items()},
                         'temporalStatus':'PARENT ADAPTER REQUIRED'} for k,v in forms.items()]}
out=audit/'TEMPORAL_PARENT_STATE_INVENTORY.json'
assert not out.exists()
out.write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f"Classified {packet['fieldCount']} actual fields in {len(rows)} holder types; linked {len(forms)} Druid profiles. No runtime/catalog promotion.")
