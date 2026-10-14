"""Preserve actual weight/space/cargo source conflicts for the body conference."""
from pathlib import Path
import hashlib,json
audit=Path(__file__).resolve().parent;game=audit.parents[3];root=game/'DescentReviewChanges/ReviewBible'
out=audit/'CODEX_TEMPORAL_CARRYING_EVIDENCE.md';assert not out.exists()
v6=game/'docs/reference/Player_Rulebook_v6_source_text.txt';lines=v6.read_text(encoding='utf-8').splitlines()
loop=game/'data/public/Decennium_Descent_Gameplay_Loop_v1.json';ld=json.loads(loop.read_text(encoding='utf-8'))
core=game/'data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json';cd=json.loads(core.read_text(encoding='utf-8'))
matches=[]
def walk(value,path=()):
 if isinstance(value,dict):
  if value.get('name') in ('Petrified','Secure Cargo','Carrying'):matches.append({'path':path,'record':value})
  for k,v in value.items():walk(v,path+(k,))
 elif isinstance(value,list):
  for i,v in enumerate(value):walk(v,path+(i,))
walk(cd)
packet={'qualification':'Direct source comparison, not adoption of one conflict side.',
 'v6':{'path':str(v6.relative_to(game)),'sha256':hashlib.sha256(v6.read_bytes()).hexdigest(),
       'lines':[{'line':i+1,'text':text} for i,text in enumerate(lines) if 7866<=i+1<=7883 or 8141<=i+1<=8151]},
 'gameplay':{'path':str(loop.relative_to(game)),'sha256':hashlib.sha256(loop.read_bytes()).hexdigest(),
             'sections':{k:ld[k] for k in ('load','extractionClass','casualtyLoad','durability') if k in ld}},
 'core':{'path':str(core.relative_to(game)),'sha256':hashlib.sha256(core.read_bytes()).hexdigest(),'records':matches},
 'alreadyReviewedCombatQualification':[
  'Secure Cargo is an Action for one actual operation involving up to one Extraction Load class; actual load/handling/hands/harnesses/checks/limits/durability remain equipment/extraction dependencies.',
  'The reviewed movement candidate preserves ordinary squeezing: added movement cost, disadvantage on attacks and Dexterity saves, attacks against the creature have advantage.',
  'Current temporal kernel supports finite integer-cell ground geometry only; this is not complete game geometry.']}
(audit/'TEMPORAL_CARRYING_SOURCE_EVIDENCE.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
text='''# Additional exact sources: carrying, size, cargo and condition mass

This follow-up is material to the shared body/equipment conference, before adopting a mass/load bridge.

Direct source comparison found V6 carrying capacity STR×15 lb, push/drag/lift twice capacity, size multipliers, optional encumbrance, and Tiny combat space2.5×2.5ft. The existing Gameplay Loop JSON instead uses Load≈10lb, carry limit STR Load, Small−2 and Large×2, burdened at half capacity, and fixed casualty loads. These are not interchangeable formulas. Core's Secure Cargo refers to an Extraction Load class while the gameplay data separately defines physical Load and Extraction Class. The already-reviewed combat overlay explicitly leaves this terminology and capacity/durability reconciliation unfinished.

Core also says Petrified weight×10. A body/form mass rule must preserve applicable current condition effects instead of overwriting them with a bare form/default mass. Carrying a transformed body, carried containers and current melded contents need explicit treatment; casualty Load must not silently become physical body mass.

Please reconcile these exact sources with the three conference questions. Distinguish preserved V6 wording, existing Gameplay mechanics, and any new provisional precedence/conversion/size/condition rule. Do not infer that a newer filename automatically supersedes a domain source. We need one coherent candidate with explicit handling of Tiny space, fractional Loads, capacity versus extraction danger, and mass-changing conditions; the original records stay preserved. If your preceding reply assumed another carrying rule, please correct it before implementation.

## Exact local evidence

```json
'''+json.dumps(packet,ensure_ascii=False,indent=2)+'\n```\n'
out.write_text(text,encoding='utf-8')
print(out.stat().st_size,'bytes; core named records:',len(matches))
