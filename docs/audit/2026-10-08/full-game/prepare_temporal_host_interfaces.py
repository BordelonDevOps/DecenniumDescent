"""Read-only structural inventory of existing state holders for temporal design."""
import ast
import hashlib
import json
from pathlib import Path
AUDIT=Path(__file__).resolve().parent;ROOT=AUDIT.parents[3]/'DescentReviewChanges/ReviewBible'
names=['core_playtest_rules.py','control_playtest_rules.py','healing_playtest_rules.py',
       'healing_pulse_playtest_rules.py','form_temphp_playtest_rules.py',
       'transformation_spell_playtest_rules.py','device_lifecycle_playtest_rules.py',
       'creature_lifecycle_playtest_rules.py','remaining_lifecycle_playtest_rules.py',
       'buffer_feat_playtest_rules.py']
records=[]
for name in names:
    path=ROOT/'tools'/name
    if not path.exists():continue
    tree=ast.parse(path.read_text(encoding='utf-8'));classes=[]
    for node in tree.body:
        if not isinstance(node,ast.ClassDef):continue
        fields={};methods=[]
        for item in node.body:
            if isinstance(item,ast.AnnAssign) and isinstance(item.target,ast.Name):
                fields[item.target.id]=ast.unparse(item.annotation)
            if isinstance(item,(ast.FunctionDef,ast.AsyncFunctionDef)):
                methods.append({'name':item.name,'line':item.lineno})
                for assign in ast.walk(item):
                    if isinstance(assign,(ast.Assign,ast.AnnAssign)):
                        targets=assign.targets if isinstance(assign,ast.Assign) else [assign.target]
                        for target in targets:
                            for attr in ast.walk(target):
                                if isinstance(attr,ast.Attribute) and isinstance(attr.value,ast.Name) and attr.value.id=='self':
                                    fields.setdefault(attr.attr,'runtime assignment in '+item.name+'; see exact code')
        if fields:classes.append({'class':node.name,'line':node.lineno,'fields':fields,'methods':methods})
    records.append({'path':'tools/'+name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'stateHolders':classes})
data={'status':'PREPARED V2 code-structure inventory; no fields approved for temporal rewind by this list',
      'scope':'Time Loop must choose restore/conserve/reconcile rules; neither AST field names nor deepcopy authorize copying',
      'revisionNote':'V1 submitted with the twelve questions captured declarations and __init__ assignments. V2 also captures assignments in other methods (including DruidState._refill reserve/shift/surge fields). Neither version proves all dynamically attached external state is covered.',
      'knownExternalDynamicState':[{'holder':'BufferLedger','attribute':'ordinary_cast_events','source':'tools/transformation_spell_playtest_rules.py:harmonic_bulwark','policy':'Unclassified temporal state; unique paid cast-event history cannot be silently dropped.'}],
      'files':records}
(AUDIT/'TEMPORAL_EXISTING_STATE_HOLDERS_V2.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'files':len(records),'stateHolders':sum(len(r['stateHolders']) for r in records)}))
