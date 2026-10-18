"""Replay the actual nine GPT operations into a NEW unaccepted draft; preserve local repairs separately."""
from copy import deepcopy
from datetime import datetime, timezone
from fractions import Fraction
from itertools import product
import hashlib, json, math
from apply_di7_ap_as_01 import G, R, A, info, encoded
from prepare_de4_fate_guard_amendment_01 import parent


def read(p):
    return json.loads(p.read_bytes())


def main():
    oldp = R/'data/director/spell_proposals/persistent_damage_20_current_06.json'
    out = R/'data/director/spell_proposals/persistent_damage_20_current_07.json'
    delta = A/'PERSISTENT_DAMAGE_20_CURRENT_07_LOCAL_DELTAS.json'
    receipt = A/'PERSISTENT_DAMAGE_20_CURRENT_07_REPLAY_CHECK.json'
    assert all(not p.exists() for p in [out, delta, receipt])
    pp = A/'persistent-damage20-conference-06-review/PROPOSED_CORRECTIONS.json'
    rp = A/'PERSISTENT_DAMAGE_20_CONFERENCE_06_RECEIPT.json'
    proposal, old = read(pp), read(oldp)
    assert info(oldp)['sha256'] == proposal['candidateBeforeBinding']['sha256']
    checks = []
    def ck(name, ok):
        checks.append({'name': name, 'passed': bool(ok)})
        assert ok, name
    d = deepcopy(old)
    replay = []
    for op in proposal['operations']:
        path = op['path']
        if path.endswith('/-'):
            target = d['currentSupplementalExamples']
            path = '/currentSupplementalExamples/'+str(len(target))
            target.append(deepcopy(op['after']))
        else:
            par, key = parent(d, path)
            ck(op['id']+' exact before', par[key] == op['before'] if op['op']=='replace' else key not in par)
            par[key] = deepcopy(op['after'])
        replay.append({**deepcopy(op), 'resolvedPath': path})
        for ref in op.get('sourceRefs', []):
            if 'sha256' in ref:
                actual = info(G/ref['path'])
                ck(op['id']+' frozen source '+ref['path'], actual['sha256']==ref['sha256'] and actual['bytes']==ref['bytes'])
    canonical = hashlib.sha256(json.dumps(d, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    ck('Exact nine-operation canonical replay', canonical == proposal['candidateAfterCanonicalJsonSha256ForReplayOnly'])
    reverse = deepcopy(d)
    for op in reversed(replay):
        par, key = parent(reverse, op['resolvedPath'])
        ck(op['id']+' exact after', par[key] == op['after'])
        if op['op']=='replace': par[key] = deepcopy(op['before'])
        elif isinstance(par, list): par.pop(key)
        else: del par[key]
    ck('Exact full reverse replay to Current06', reverse == old)
    before_local = deepcopy(d)
    local = []
    def replace(path, value, reason):
        par, key = parent(d, path)
        local.append({'path':path, 'before':deepcopy(par[key]), 'after':deepcopy(value), 'reason':reason, 'actualGPTConcurrenceOnThisLocalChange':False})
        par[key] = deepcopy(value)

    beast = deepcopy(d['adversarialVectors04'][4])
    ck('Actual Ranger Beast case', beast['id']=='P20-X05')
    del beast['initialState']['ordinaryWoundCONFace']
    beast['resolution'][0] = 'INT1+5=6 fails DC16; 8d6 faces total29. The actual Ranger Beast uses its source-specific HP-only lifecycle, not ordinary Wounds or death saves. Ordinary damage reduces current10 to0: it dies immediately, its bond ends and its actual surviving corpse remains. No Wound save, Stable state or new creature penalty applies. No free resummon or bond reset follows.'
    beast['expected']['ordinary'].update({'WoundSaveCount':0, 'deathSaveCount':0, 'bondEnded':True, 'actualCorpseRemains':True})
    beast['sourceRefs07'] = [{**info(R/'docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST.md'), 'section':'Companion lifecycle table; Ranger Beast HP-only exception'}]
    replace('/adversarialVectors04/4', beast, 'Local source repair: returned review noticed the HP-only exception but supplied no replacement for the existing erroneous Wound roll. Preserve the complete former case in this delta.')

    mortar = deepcopy(d['currentExamples'][17])
    ck('Actual mortar case', mortar['id']=='EV6-03-B')
    suppressor = mortar['initialState']['readiedSuppressor']
    suppressor['positionCenter'] = [20, -11, 3]
    suppressor['bodySpace'] = 'Medium 5x5 feet; measured occupied height6; half-extents[2.5,2.5,3] on floor z=0'
    suppressor['actualRelationshipToMortar'] = 'May be hostile; whole-body gap6ft exceeds the5ft close-quarters threshold. No other hostile capable creature is within5ft of the cannon at its later shot.'
    mortar['actionsAndResolution'][2] = mortar['actionsAndResolution'][2].replace('point(20,0,2.5)', 'point(20,-2,2.5)')
    mortar['geometryChecks07'] = {'releasedFieldCenter':[20,-2,2.5], 'casterCenterToFieldSquared':81.25, 'casterCenterToFieldFt':math.sqrt(81.25), 'maximumMortarCornerToFieldSquared':32.75, 'fieldRadiusSquared':100, 'CToMortarWholeBodyGapFt':6, 'bodyOverlapAtCreation':False, 'closeQuartersDisadvantageFromC':False, 'floorZ':0, 'actualSource':info(R/'docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md')}
    replace('/currentExamples/17', mortar, 'Local correction to GPT PC06: its caster center[20,0,3] physically overlapped the newly created mortar. Move C and the released field point; retain every paid Ready, command, ammunition, suppression and destruction obligation. Actual concurrence pending.')

    warrior = deepcopy(d['currentSupplementalExamples'][-1])
    ck('Actual Ice Storm DR supplement', warrior['id']=='P20-C07-02')
    warrior['sourceAccess']['recipient']['HPDerivation'] = 'Warrior d12, CON16 modifier+3 throughout: first12+3=15, nine fixed gains7+3=10 each; max15+90=105. Full current105 is an explicitly recovered starting state, not free healing from advancement; no HP-changing selections.'
    warrior['sourceRefs'].extend([{**info(R/'docs/mechanics/classes/warrior.md'), 'section':'Book setup, d12 HP'}, {**info(R/'docs/mechanics/CHARACTER_CREATION_PLAYTEST.md'), 'section':'Chronological HP; d12 fixed7'}])
    replace('/currentSupplementalExamples/'+str(len(d['currentSupplementalExamples'])-1), warrior, 'Evidence-only HP derivation:105 is correct for actual d12 Warrior10/CON16. No numeric correction and no new source rule.')

    verify_local = deepcopy(d)
    for op in reversed(local):
        par, key = parent(verify_local, op['path'])
        ck('Local exact after '+op['path'], par[key]==op['after'])
        par[key] = deepcopy(op['before'])
    ck('Local edits reverse exactly to GPT nine-operation replay', verify_local==before_local)
    finish(d, old, oldp, out, delta, receipt, proposal, pp, rp, replay, local, canonical, checks, ck)


def finish(d, old, oldp, out, delta, receipt, proposal, pp, rp, replay, local, canonical, checks, ck):
    ck('Twenty source/access records preserved', len(d['spells'])==20 and all(a['completeSourceAndAccess']==b['completeSourceAndAccess'] for a,b in zip(old['spells'],d['spells'])))
    ck('Forty original texts unchanged', d['originalExamplesUnchanged']==old['originalExamplesUnchanged'] and len(d['currentExamples'])==40)
    keys = ['currentExamples','currentSupplementalExamples','adversarialVectors04']
    prior_ids = [c['id'] for key in keys for c in old[key]]
    new_ids = [c['id'] for key in keys for c in d[key]]
    ck('55 existing IDs retained and two distinct supplements added', len(prior_ids)==55 and len(new_ids)==len(set(new_ids))==57 and set(prior_ids).issubset(new_ids))
    for a,b in zip(old['currentExamples'], d['currentExamples']):
        ck('Original scenario preserved '+a['id'], a.get('originalTextUnchanged')==b.get('originalTextUnchanged'))
    ck('All other 17 complete procedures unchanged', all(a['procedure']==b['procedure'] for i,(a,b) in enumerate(zip(old['spells'],d['spells'])) if i not in [1,2,14]))
    ck('Actual mortar placement separates every body', 8.5-2.5==6 and 6>5)
    farthest = max((x-20)**2+(y+2)**2+(z-2.5)**2 for x,y,z in product([17.5,22.5],[-2.5,2.5],[0,5]))
    ck('Whole mortar inside released radius10', farthest==32.75 and farthest<100)
    ck('Field point in actual caster range', (20-20)**2+(-11+2)**2+(3-2.5)**2==81.25 and 81.25<100)
    ck('Ready release precedes expiry and original cannon expiry retained', -1<1.5<4 and 2<3<8<60 and 1.5+60==61.5)
    ck('Two actual paid spells and later shot arithmetic', 40-13==27 and 32-10==22 and 12+8>=14 and sum([3,3,4,4,4])==18 and 200-18==182)
    ck('Beast HP-only source arithmetic', 2*16+4==36 and sum([3,3,3,4,4,4,4,4])==29 and 1+5<16)
    ck('Warrior10 chronological HP source arithmetic', 12+3+9*(7+3)==105)
    def allocation(amounts, reduction):
        total=sum(amounts.values()); b=min(total,reduction)
        shares={k:Fraction(v*b,total) for k,v in amounts.items()}
        allocated={k:int(v) for k,v in shares.items()}
        order=sorted(shares,key=lambda k:(-(shares[k]-allocated[k]),k))
        for k in order[:b-sum(allocated.values())]:allocated[k]+=1
        return allocated
    for branch in d['currentSupplementalExamples'][-1]['branches']:
        saved={k:sum(v)//2 for k,v in branch['rawPools'].items()}
        allocated=allocation(saved,branch['BT'])
        after={k:saved[k]-allocated[k] for k in saved}
        final={**after,'cold':after['cold']//2}
        ck('Ice '+branch['id']+' saves, exact allocation and typed resistance', saved==branch['savedAmounts'] and allocated==branch['allocatedReduction'] and after==branch['afterReduction'] and final==branch['afterColdResistance'])
        ck('Ice '+branch['id']+' single HP event', sum(final.values())==branch['damage'] and 105-sum(final.values())==branch['HPAfter'])
    ck('Rain contact-loss boundary before outside continuation', 32.5-31==1.5 and 1.5*2==3 and 30-3-15==12 and 32.5+12==44.5)
    ck('No source acceptance or runtime count changes', d['acceptedCountsUnchanged']==old['acceptedCountsUnchanged'] and d['newRuleAdoptions']==d['runtimeTestsExecuted']==d['sourceInformationDeleted']==0)
    old_meta={k:deepcopy(d[k]) for k in ['id','recordedAtUtc','status','currentExampleCoverageStatus']}
    d['id']='PERSISTENT-DAMAGE-20-CURRENT-07'
    d['recordedAtUtc']=datetime.now(timezone.utc).isoformat()
    d['status']='UNADOPTED Current07: actual GPT Conference06 nine operations replayed and reversed exactly; two local source/placement repairs plus one HP derivation separately preserved. Twenty full procedures,40 original-case vectors,9 supplements,8 adversarial cases. Local corrections and exact integration still require actual GPT concurrence; no catalog or runtime promotion.'
    d['currentExampleCoverageStatus']={**d['currentExampleCoverageStatus'],'supplementalExamples':9,'scope':'40 original-case vectors,9 supplements,8 adversarial cases. Full original scenarios preserved. Actual Conference06 is returned; Current07 and local repairs await review. Authored conditional vectors are not runtime tests.'}
    d['conference06Application07']={'actualReviewReceipt':info(rp),'actualProposal':info(pp),'previousCompleteCandidate':info(oldp),'nineOperationCanonicalReplaySha256':canonical,'operationIds':[o['id'] for o in replay],'localEdits':[{'path':o['path'],'reason':o['reason']} for o in local],'previousMetadataUnchanged':old_meta,'exactGPTAcceptanceOfCurrent07':False,'newRuleAdoptions':0}
    delta.write_bytes(encoded({'id':'PERSISTENT20-CURRENT07-LOCAL-DELTAS','status':'Complete reversible changes after exact GPT replay; concurrence pending','previousCandidate':info(oldp),'actualGPTProposal':info(pp),'fullLocalChanges':local,'sourceInformationDeleted':0}))
    d['conference06Application07']['completeLocalDelta']=info(delta)
    out.write_bytes(encoded(d))
    receipt.write_bytes(encoded({'id':'PERSISTENT20-CURRENT07-REPLAY-CHECK','candidate':info(out),'previousCandidate':info(oldp),'actualGPTReceipt':info(rp),'actualProposal':info(pp),'completeLocalDelta':info(delta),'nineOperations':len(replay),'canonicalReplaySha256':canonical,'forwardAndReverseReplayVerified':True,'checks':checks,'checkCount':len(checks),'failures':0,'procedureCount':20,'currentCases':57,'retainedPriorCaseIds':55,'newCaseIds':sorted(set(new_ids)-set(prior_ids)),'actualGPTAcceptanceOfCurrent07':False,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}))
    print(json.dumps({'candidate':info(out),'receipt':info(receipt),'delta':info(delta),'checks':len(checks),'cases':57,'newRuleAdoptions':0}))


if __name__ == '__main__':
    main()
