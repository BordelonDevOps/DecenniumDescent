#!/usr/bin/env python3
"""New recovery-only finite diagnostic; does not import project/game code.

Reads the hash-bound MODEL and models ONLY the paid hold's release/expiry boundary.
At time 61/61.1 the ordinary regular-START scheduler is NOT executed: actor phase
and remaining-budget fields are deliberately frozen inputs, not a full live state.
Reports must be written to a new file. No source, archive or model is modified.
"""
from __future__ import annotations
import argparse
import copy
from decimal import Decimal
import hashlib
import json
from pathlib import Path
from typing import Any

EXPECTED_SHA256 = '949ef5c6a1f05c1b0823d9ec4e10cd3e387a0c8c918680e95fa0047b60e40e3a'
EXPECTED_BYTES = 12000315
BRANCH_POINTER = '/currentVectors/2/independentBranches/0'

def encode(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')

def step(snapshot: dict[str, Any], receipt: dict[str, int], now: Decimal,
         *, valid_completed_perceived_trigger: bool = True,
         actual_source_and_target_legal: bool = True) -> tuple[dict, dict, str]:
    """One isolated boundary callback. No START/turn/world dispatch is performed.

    Six damage is the supplied successful archived payload, NOT an RNG engine.
    The Ray-held concentration identity is a fixture identifier, not a new source.
    """
    state = copy.deepcopy(snapshot)
    counts = copy.deepcopy(receipt)
    hold = state['sourceLedger']['hold']
    mage = state['actors']['mage']
    if hold.get('state') in ('consumed', 'expired'):
        return state, counts, 'already-ended-no-transition'
    if now >= Decimal(str(hold['deadline'])):
        hold['state'] = 'expired'
        counts['holdEnds'] += 1
        if mage['concentration'] == 'Ray-held':
            mage['concentration'] = None
            counts['concentrationEnds'] += 1
        return state, counts, 'expired-no-release'
    if not (valid_completed_perceived_trigger and actual_source_and_target_legal
            and mage['reaction'] and mage['concentration'] == 'Ray-held'):
        return state, counts, 'no-valid-release-no-debit'
    # This existing paid hold is consumed once. No Action, cast, RP or metamagic fee.
    hold['state'] = 'consumed'
    hold['paidMetamagicCharge'] = 0
    mage['reaction'] = False
    counts['reactionDebits'] += 1
    state['actors']['target']['hp'] -= 6
    counts['payloadApplications'] += 1
    mage['concentration'] = None
    counts['concentrationEnds'] += 1
    counts['holdEnds'] += 1
    return state, counts, 'released-existing-paid-hold'

def generate(model_path: Path) -> dict:
    raw = model_path.read_bytes()
    if len(raw) != EXPECTED_BYTES or hashlib.sha256(raw).hexdigest() != EXPECTED_SHA256:
        raise ValueError('Exact recovered MODEL binding mismatch; refusing another candidate')
    model = json.loads(raw)
    branch = model['currentVectors'][2]['independentBranches'][0]
    event = branch['timeline'][2]
    paid = copy.deepcopy(event['before'])
    checks: list[dict] = []
    def ck(name: str, condition: bool) -> None:
        checks.append({'check': name, 'passed': bool(condition)})
        if not condition:
            raise AssertionError(name)
    ck('actual branch identity', branch['id'] == 'RIC5-02-A-a')
    ck('actual Mage55/61 cadence, stored deadline61',
       (paid['actors']['mage']['regularStart'], paid['actors']['mage']['nextRegularStart'],
        paid['sourceLedger']['hold']['deadline']) == (55, 61, 61))
    ck('preparation56.1, Surgeexpiry60.5, release60.9 retained',
       [e['timeSeconds'] for e in branch['timeline']] == [56.1, 60.5, 60.9])
    ck('source grants no START in release event', event['regularStartsBeforeEvent'] == [])
    ck('positive archived RNG unchanged', event['rng'] == {'attack': [7, 9, 16], '1d8': [6]})
    ck('paid Action is spent before release; real Reaction remains',
       paid['actors']['mage']['action'] is False and paid['actors']['mage']['reaction'] is True)
    cases = []
    initial_counts = {'payloadApplications': 0, 'reactionDebits': 0,
                      'holdEnds': 0, 'concentrationEnds': 0}
    for label in ('60.9', '61', '61.1'):
        t = Decimal(label)
        before = copy.deepcopy(paid)
        after, counts, result = step(before, initial_counts, t)
        expected_release = label == '60.9'
        ck(f'{label}: original input unmodified', before == paid)
        ck(f'{label}: stale62 predicate true', t < Decimal(62))
        ck(f'{label}: corrected61 predicate', (t < Decimal(61)) == expected_release)
        ck(f'{label}: event category', result == ('released-existing-paid-hold' if expected_release else 'expired-no-release'))
        ck(f'{label}: targetHP', after['actors']['target']['hp'] == (74 if expected_release else 80))
        ck(f'{label}: one or zero real Reaction debit', counts['reactionDebits'] == int(expected_release))
        ck(f'{label}: payload count', counts['payloadApplications'] == int(expected_release))
        ck(f'{label}: exactly one hold/concentration end', counts['holdEnds'] == counts['concentrationEnds'] == 1)
        ck(f'{label}: no Action refresh', after['actors']['mage']['action'] is False)
        ck(f'{label}: residual Reaction', after['actors']['mage']['reaction'] == (not expected_release))
        ck(f'{label}: Mage cadence not advanced by this diagnostic',
           (after['actors']['mage']['regularStart'], after['actors']['mage']['nextRegularStart']) == (55, 61))
        for key in ('rp','dissonance','refrain','metaspellUses','lastSpell','preparedFamiliesUsed',
                    'bonusAction','movementSpent','counterRecharge'):
            ck(f'{label}: preserve mage {key}', after['actors']['mage'][key] == paid['actors']['mage'][key])
        for key in ('deadline','range','metamagicCharge','preparation','trigger'):
            ck(f'{label}: preserve original hold {key}', after['sourceLedger']['hold'][key] == paid['sourceLedger']['hold'][key])
        ck(f'{label}: source applications remain exact', after['applications'] == paid['applications'])
        ck(f'{label}: uninvolved surger exact', after['actors']['surger'] == paid['actors']['surger'])
        ck(f'{label}: custody and private memories exact',
           after['objects'] == paid['objects'] and after['privateMemories'] == paid['privateMemories'])
        if expected_release:
            ck('60.9: entire outcome equals current archived event', after == event['after'])
            ck('60.9: entire outcome equals branch final', after == branch['expectedFinalState'])
        else:
            expected = copy.deepcopy(paid)
            expected['sourceLedger']['hold']['state'] = 'expired'
            expected['actors']['mage']['concentration'] = None
            ck(f'{label}: only hold expiry and its concentration cleanup mutate', after == expected)
        repeat_log = []
        saved_after = copy.deepcopy(after); saved_counts = copy.deepcopy(counts)
        for follow in (t, max(t, Decimal('61.1')), Decimal('62')):
            again, again_counts, again_result = step(after, counts, follow)
            ck(f'{label}: terminal callback@{follow}: no state replay', again == saved_after)
            ck(f'{label}: terminal callback@{follow}: no second debit/payload/cleanup', again_counts == saved_counts)
            ck(f'{label}: terminal callback@{follow}: ended result', again_result == 'already-ended-no-transition')
            repeat_log.append({'observedAt': str(follow), 'result': again_result,
                               'completeAfter': again, 'receiptAfter': again_counts})
            after, counts = again, again_counts
        cases.append({'id':'RIC5-RECOVERY-BOUNDARY-'+label.replace('.','_'),
          'triggerTime':label, 'scope':'Independent reset of the same complete paid pre-release snapshot; hold boundary only.',
          'premises':{'perceivedTriggerCompleted':True, 'actualSourceAndTargetLegal':True,
                      'nativePayloadOutcome':event['rng'], 'productionActionReachabilityProven':False},
          'obsoleteTimeLessThan62':True, 'correctedTimeLessThan61':expected_release,
          'completeBefore':before,'completeAfter':saved_after,'result':result,
          'receiptBefore':copy.deepcopy(initial_counts),'receiptAfter':saved_counts,
          'repeatCallbacks':repeat_log})
    # Invalid pre-expiry attempts leave the current paid source available, not refreshed.
    gate_checks=[]
    for kind in ('no-reaction','incomplete-or-unperceived-trigger','invalid-source-or-target'):
        v=copy.deepcopy(paid)
        if kind=='no-reaction':v['actors']['mage']['reaction']=False
        a,c,result=step(v,initial_counts,Decimal('60.9'),
            valid_completed_perceived_trigger=kind!='incomplete-or-unperceived-trigger',
            actual_source_and_target_legal=kind!='invalid-source-or-target')
        ck(f'{kind}: no mutation/debit or invented release',a==v and c==initial_counts and result=='no-valid-release-no-debit')
        gate_checks.append({'gate':kind,'completeBefore':v,'completeAfter':a,'receiptAfter':c,'result':result})
    return {'id':'RIC5-READY-DEADLINE-RECOVERY01-BOUNDARY-DIAGNOSTIC',
      'model':{'path':'MODEL.json','bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()},
      'branchPointer':BRANCH_POINTER,'completeActorDefinitions':branch['actorDefinitions'],
      'sourceRefs':branch['sourceRefs'],
      'scope':'New isolated finite diagnostic of stored hold expiry and once-only cleanup, using exact current fixture input and stipulated six-damage payload. Not a native scheduler, combat-engine execution or original Return03 test recovery.',
      'schedulerScope':{'regularStartDispatched':False,'worldClockOrOtherActorsAdvanced':False,
        'actualFullStateAt61Or61_1Asserted':False,'actionOrReactionRefreshGranted':False,
        'frozenFields':'At61/61.1 Mage regularStart55/next61 and residual budget fields remain the input snapshot because this diagnostic only processes the hold. The actual scheduler must process START separately; a new budget never revives an expired hold.',
        'stalePredicateLimit':'Old time<62 is shown only as a stale stored-data predicate. It is not proof that an actual old runtime scheduler would release at61.'},
      'independentBoundaryCases':cases,'preExpiryGateDiagnostics':gate_checks,
      'boundaryCaseCount':3,'gateDiagnosticCount':3,'checkCount':len(checks),
      'failures':0,'checks':checks,'projectRuntimeTestsExecuted':0,
      'suppliedOrDownloadedScriptsExecuted':False,'sourceInformationDeleted':0}

def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
    ap.add_argument('--report',type=Path)
    args=ap.parse_args()
    report=generate(args.root/'MODEL.json')
    if args.report:
        dest=args.report.resolve(); root=args.root.resolve()
        if dest==root or root in dest.parents:
            raise ValueError('Report must be a new path outside the recovery package')
        dest.parent.mkdir(parents=True,exist_ok=True)
        with dest.open('xb') as f:f.write(encode(report))
    print(json.dumps({'boundaryCases':3,'gateDiagnostics':3,'checks':report['checkCount'],'failures':0,'runtimeTests':0}))

if __name__=='__main__':main()
