"""Ask the notebook to settle real body/equipment gaps before parent integration."""
from pathlib import Path
import ast,hashlib,json
audit=Path(__file__).resolve().parent;root=audit.parents[3]/'DescentReviewChanges/ReviewBible'
out=audit/'CODEX_TEMPORAL_BODY_EQUIPMENT_CONFERENCE.md';assert not out.exists()
parts=['''# Complete parent integration: ordinary body/equipment gaps

Both prerequisites now have actual notebook closure: the59-method operation journal and the15-method exact-reference Transaction extension (207 regression methods remain passing). Full parent restoration and all seven larger domains remain open. I am now joining the actual source holders, rather than declaring reference transport to be full restoration.

The source comparison exposes an ordinary-play gap relevant to the full game: the reviewed form guide says Druid gear melds, but DruidState has no Body/equipment reference. Its shift/revert/end methods do not update TransformationWorld.Body.equipment/melded/size/mass or request reversion placement. The current operation journal calls those native methods directly. In contrast, transformation spells do update the same Body and maintain melded/lost gear, sponsor slots and placement flags. A complete temporal planner cannot restore an ordinary state that the shared world never actually represented.

Please settle these three connected issues from the attached actual code and rules. Label recovered rules versus new provisional decisions. We need a complete implementable ordinary bridge, not a Boolean claiming gear/geometry is handled. Keep current stat/cadence/conservation and no-refund rules intact.

1. SHARED BODY / ORDINARY DRUID EVENTS. Confirm the exact bridge over the one real Body: initial Druid entry melds eligible currently equipped items; form-to-form changes preserve the original meld set without returning/re-equipping items or replenishing them; actual final reversion/expiry/damage ending returns only surviving, still-owned original melded items. A spell replacing a Druid form is a continuous transformation and must not briefly make gear usable. Describe when Body.size, placement flags and geometry must update on entry/change/end, and how a failed placement is resolved without granting a free move or consuming entry costs before legality is known. Address Tiny Hawk, optional Large forms, flying/burrowing/unsupported endings, and the fact that the present kernel's geometry supports only finite level ground. We must develop the missing interactions, not silently call the limited geometry a complete game.

2. MASS AND SAME PHYSICAL IDENTITY. The Druid profiles specify size but no mass. Body.mass participates in True Polymorph object-output caps, so borrowing unchanged root mass would become an unspoken gameplay rule. Please identify existing mass authority if present; otherwise settle a usable explicit provisional rule for mass across these bounded Druid forms/variants. Compare retaining root mass versus a profile-based mass rule, including Tiny flight, Large forms, carrying/load and True Polymorph's min(current mass, original mass) cap. Do not introduce harvestable/saleable derivative material or duplicate physical roots. Specify what must be recorded at actual entry and what current conserved inventory/load owns.

3. EQUIPMENT / PHYSICAL CUSTODY / RECONCILIATION. The selected form guide leaves the complete item/anatomy compatibility matrix unfinished. Establish common source-grounded defaults now for worn armor, shields/held weapons, passive numeric magic, carried containers, and newly acquired external gear, distinguishing all26 Druid profiles from the12 finite spell profiles with explicit hands. Define what restores to the original meld set, what remains usable external equipment, what must drop at the legal current/nearest adjacent placement, and which real transfer/destruction blocks versus survives temporal restoration. Identify any exact remaining source exception rather than treating every item as a generic Boolean certificate. Current item charges/stock/durability and ownership stay conserved. The original item and class catalogs remain authoritative and intact.

The current profile/equipment rules and actual native fields follow. This is a source/design conference for the next integrated ordinary/temporal body layer, not a request to approve unimplemented behavior. Once settled, I will implement the ordinary bridge and full proposed-state/watch/commit path and submit actual tests. Full-game flow and GitHub delivery remain open.
''']
hashes={}
def add(name,text=None):
 p=root/name;hashes[name]=hashlib.sha256(p.read_bytes()).hexdigest()
 parts.append('\n## '+name+'\nSource SHA-256 `'+hashes[name]+'`\n\n```\n'+(p.read_text(encoding='utf-8') if text is None else text)+'\n```\n')
add('docs/mechanics/FORM_TEMP_HP_PLAYTEST.md')
add('docs/mechanics/TRANSFORMATION_SPELL_PLAYTEST.md')
add('tools/form_temphp_playtest_rules.py')
add('tools/transformation_spell_playtest_rules.py')
p=root/'tools/temporal_playtest_rules.py';source=p.read_text(encoding='utf-8');tree=ast.parse(source)
segments=[]
for n in tree.body:
 if isinstance(n,ast.ClassDef) and n.name in ('PhysicalRecord','Inventory','Pose','EnvironmentAnchor','Geometry'):
  segments.append(ast.get_source_segment(source,n))
 if isinstance(n,ast.ClassDef) and n.name=='TemporalKernel':
  for m in n.body:
   if isinstance(m,ast.FunctionDef) and m.name in ('_physical_plan','_space','_reachable','_geometry_plan'):
    segments.append(ast.get_source_segment(source,m))
add('tools/temporal_playtest_rules.py','\n\n'.join(segments))
d=json.loads((root/'data/playtest/druid_form_profiles.json').read_text(encoding='utf-8'))
forms=d['profiles']
summary={key:{k:v for k,v in row.items() if k in ('id','minimumLevel','circle','size','mayLarge','variant','movement','speech','hands','entryBuffer','sourceProcedure','sourceSha256')} for key,row in forms.items()}
add('data/playtest/druid_form_profiles.json',json.dumps(summary,ensure_ascii=False,indent=2))
add('data/playtest/spell_form_profiles.json')
d=json.loads((root/'data/playtest/class_sources/druid.json').read_text(encoding='utf-8'))
add('data/playtest/class_sources/druid.json',json.dumps({'sourcePath':d['sourcePath'],'sourceSha256':d['sourceSha256'],
 'qualification':'Preserved historical source; already reviewed provisional form overlay controls conflicts. Do not re-import monster-stat replacement.',
 'bookLines':[x for x in d['bookLines'] if 2433<=x['line']<=2448]},ensure_ascii=False,indent=2))
out.write_text(''.join(parts),encoding='utf-8')
(audit/'TEMPORAL_BODY_EQUIPMENT_CONFERENCE_SUBMISSION.json').write_text(json.dumps({
 'status':'Prepared source conference; no new rulings adopted','sourceHashes':hashes,
 'packetSha256':hashlib.sha256(out.read_bytes()).hexdigest(),'druidProfiles':len(forms),
 'fullTimeLoopOperational':False,'remainingMajorIntegrations':7},indent=2)+'\n')
print(out.stat().st_size,'bytes prepared; profiles:',len(forms))
