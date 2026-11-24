"""Index source extraction allocations without claiming implementation or tested purity."""
import hashlib
import json
from pathlib import Path

PACKET=Path(__file__).resolve().parent
def read(name):
    return json.loads((PACKET/name).read_text(encoding='utf-8-sig'))

inventory=read('OPERATION_INVENTORY.json')
expected={x['kind']:x['semanticBranchesToDisposition'] for x in inventory['operations']}
names=['PHYSICAL_CARE_READ_EXTRACTION_PLAN.json','MAGIC_READ_EXTRACTION_PLAN.json',
       'MANAGEMENT_READ_EXTRACTION_PLAN.json','TACTICAL_OPERATOR_READ_EXTRACTION_PLAN.json']
bindings={}
inputs=[]
for name in names:
    report=read(name)
    inputs.append({'path':name,'sha256':hashlib.sha256((PACKET/name).read_bytes()).hexdigest()})
    for i,op in enumerate(report['operations']):
        kind=op['kind'];assert kind not in bindings
        axes=op.get('exactAxes',op.get('semanticBranchesToDisposition'))
        if axes and isinstance(axes[0],dict):
            axes=[x['exactAxis'] for x in axes]
        if kind in expected:assert axes==expected[kind],kind
        else:assert kind in inventory['operatorKinds'],kind
        bindings[kind]={'kind':kind,'operatorOnly':kind in inventory['operatorKinds'],
                        'exactAxes':axes,'plan':name+'#/operations/'+str(i),
                        'status':'NATIVE_EXTRACTION_SEAM_ALLOCATED_NOT_IMPLEMENTED_OR_QUALIFIED',
                        'runtimeQualified':False}
assert set(bindings)==set(expected)|set(inventory['operatorKinds'])
rows=[bindings[x['kind']] for x in inventory['operations']]
operators=[bindings[k] for k in inventory['operatorKinds']]
result={'schemaVersion':1,'status':'COMPLETE_KIND_AXIS_ALLOCATION_BOUNDED_SOURCE_PLANS_FULL_HC_OPEN',
        'counts':{'candidateKinds':78,'operatorKinds':2,'candidateSemanticAxes':204,'unmappedKinds':0,'runtimeQualifiedKinds':0},
        'inputs':inputs,'operations':rows,'operatorKinds':operators,
        'commonReadBoundary':['CONDITION_READ_BOUNDARY.md','PURE_CHECKPOINT_CONTRACT.md','CURRENT_FACT_HELPER_AUDIT.json','CURRENT_PERMISSION_SIGHT_AUDIT.json','PROCEDURE_INVENTORY_READ_AUDIT.json'],
        'remaining':['Exact shared API signatures and full outer host/Core/native branch precedence',
                     'Selected remaining spatial/pressure/speed, sale/meal pure capacity and episode closure helper dependencies',
                     'All-profile copy/policy/stamp binding and actual instrumentation/parity evidence',
                     'Full field/domain/example/choice and finite branch/profile/five-path expected-output agreement',
                     'Actual full GPT and Codex source/API concurrence before runtime'],
        'sourceApiAccepted':False,'runtimeAuthorized':False}
(PACKET/'READ_EXTRACTION_INDEX.json').write_bytes((json.dumps(result,indent=2,ensure_ascii=False)+'\n').encode('utf-8'))
print(json.dumps(result['counts']))
