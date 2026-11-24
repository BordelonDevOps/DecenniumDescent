"""Reconcile exact reviewed native parameter proposals; this does not execute the engine."""
import hashlib
import json
from pathlib import Path

PACKET = Path(__file__).resolve().parent

def read(name):
    return json.loads((PACKET / name).read_text(encoding='utf-8-sig'))

names = ['PHYSICAL_CARE_PARAMETER_CONTRACT_PROPOSAL.json',
         'MAGIC_ADVANCEMENT_PARAMETER_CONTRACT_PROPOSAL.json',
         'MANAGEMENT_WORK_PARAMETER_CONTRACT_PROPOSAL.json',
         'TACTICAL_OPERATOR_PARAMETER_CONTRACT_PROPOSAL.json']
inventory = read('OPERATION_INVENTORY.json')
expected = {o['kind']: o['semanticBranchesToDisposition'] for o in inventory['operations']}
bindings = {}
inputs = []
for name in names:
    report = read(name)
    inputs.append({'path':name,'sha256':hashlib.sha256((PACKET/name).read_bytes()).hexdigest()})
    for i, op in enumerate(report['operations']):
        kind = op['kind']
        assert kind not in bindings, kind
        axes = op.get('axes', op.get('exactAxes', [a['axis'] for a in op.get('axisBindings',[])]))
        operator = kind in inventory['operatorKinds']
        if not operator:
            assert axes == expected[kind], (kind, 'ordered axes differ')
        if 'variants' in op:
            variants = [{'variantKey':v['variantKey'], 'source':name+'#/operations/'+str(i)+'/variants/'+str(j)} for j,v in enumerate(op['variants'])]
        elif kind == 'CastKnownSpell':
            variants = [{'variantKey':'cast.'+v['spellId'],'source':name+'#/operations/'+str(i)+'/spellVariants/'+str(j)} for j,v in enumerate(op['spellVariants'])]
            variants.append({'variantKey':'cast.legacy-repertoire-denial','source':name+'#/operations/'+str(i)+'/nativeOnlyAndDenialBoundaries/repertoireOnly','positiveExamples':False})
            variants.append({'variantKey':'cast.native-source-boundary-control','source':name+'#/operations/'+str(i)+'/nativeOnlyAndDenialBoundaries/flareSparkAndLight','positiveExamples':False})
        elif kind == 'AdvanceCharacterLevel':
            variants = [{'variantKey':'advance.cleric2','source':name+'#/operations/'+str(i)+'/admittedSelections/0'},
                        {'variantKey':'advance.bishop3','source':name+'#/operations/'+str(i)+'/admittedSelections/1'}]
        else:
            variants = [{'variantKey':kind+'.native','source':name+'#/operations/'+str(i)}]
        assert len({v['variantKey'] for v in variants}) == len(variants), kind
        for j,v in enumerate(variants):
            v['variantOrdinal'] = j
            v['exampleOrdinalPolicy'] = 'After current authorization filtering, sort exact candidate payloads by the explicit typed domain order in EXAMPLE_DOMAIN_ORDER.md; zero-based within this variant. No native/private index gaps.'
            v['actualDerivedIdentityConstraints'] = name+'#/derivedIdentityRules' if 'derivedIdentityRules' in report else name+'#/derivedIdentityLimits'
        bindings[kind] = {'kind':kind,'operatorOnly':operator,'proposal':name+'#/operations/'+str(i),
                          'exactAxes':axes,'variants':variants,
                          'conditionReadDependency':'CONDITION_READ_BOUNDARY.md, including actual GPT04/05 corrections; no legacy lazy journal fallback',
                          'effectiveCorrections':'PARAMETER_CONTRACT_CORRECTIONS_05.md',
                          'exampleConstructionQualified':False,'runtimeQualified':False}
assert set(bindings) == set(expected) | set(inventory['operatorKinds'])
rows = [bindings[o['kind']] for o in inventory['operations']]
operators = [bindings[k] for k in inventory['operatorKinds']]
result = {'schemaVersion':1,'status':'RECONCILED_PARAMETER_DESIGN_WITH_FROZEN_LOCAL_VARIANT_ORDINALS_FULL_HC_OPEN',
          'sourceApiAccepted':False,'runtimeAuthorized':False,
          'counts':{'candidateKinds':len(rows),'operatorKinds':len(operators),
                    'exactSemanticAxes':sum(len(x['exactAxes']) for x in rows),
                    'registeredVariants':sum(len(x['variants']) for x in rows+operators),
                    'runtimeQualifiedKinds':0},
          'inputs':inputs,'operations':rows,'operatorKinds':operators,
          'remaining':['Per-variant current example construction and payload ordering must be proven against native bounds, including dynamic derived IDs',
                       'Normalize every exact parameter type/domain/choice with all selected profile variants',
                       'Complete full field/source/purity and genuine five-path expected-output allocation',
                       'Actual GPT and Codex full HC acceptance before runtime']}
assert result['counts']['candidateKinds'] == 78 and result['counts']['operatorKinds'] == 2
assert result['counts']['exactSemanticAxes'] == 204
(PACKET/'PARAMETER_CONTRACT_INDEX.json').write_bytes((json.dumps(result,indent=2,ensure_ascii=False)+'\n').encode('utf-8'))
print(json.dumps(result['counts']))
