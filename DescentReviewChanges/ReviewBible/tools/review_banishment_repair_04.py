"""Verify Repair04 preservation and record independent bounded acceptance review."""
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded, digest
from review_banishment_repair_02 import at


def read(path):
    return json.loads(path.read_bytes())


def main():
    out = A / 'banishment-repair-04-return'
    target = A / 'BANISHMENT_REPAIR_04_LOCAL_AUDIT.json'
    request = A / 'BANISHMENT_EXACT_ACCEPTANCE_04_REQUEST.txt'
    assert not target.exists() and not request.exists()
    inputs = read(A / 'banishment-current-review-01-input/CURRENT_REVIEW_INPUT.json')
    model = read(out / 'SPELL_MODEL.json')
    register = read(out / 'REGISTER.json')
    cases = read(out / 'CASEBOOK.json')['cases']
    old = read(A / 'banishment-repair-03-return/CASEBOOK.json')['cases']
    sources = read(out / 'SOURCE_HASHES.json')
    manifest = read(out / 'EVIDENCE_MANIFEST.json')
    checks, refs, sections = [], [], []

    def check(label, ok):
        checks.append({'check': label, 'pass': bool(ok)})

    expected = {'REGISTER.json','SPELL_MODEL.json','PLAYER_CHAPTER.md','DIRECTOR_REVIEW.md','CASEBOOK.json','SOURCE_HASHES.json','VERDICT.md','EVIDENCE_MANIFEST.json'}
    check('exact8root files', {p.name for p in out.iterdir()} == expected)
    check('source bindings unchanged', sources['bindings'] == inputs['sourceBindings'])
    for b in sources['bindings']:
        raw = (G / b['path']).read_bytes()
        check('current source: ' + b['path'], len(raw) == b['bytes'] and digest(raw) == b['sha256'])
    for b in manifest['files']:
        raw = (out / b['name']).read_bytes()
        check('output: ' + b['name'], len(raw) == b['bytes'] and digest(raw) == b['sha256'])
    check('original source/access exact', model['sourceAndAccess'] == inputs['sourceCard'])
    check('register/model access agree', register['spell']['accessRows'] == model['procedure']['access'])
    check('all35prior case IDs retained in order', [c['id'] for c in cases[:35]] == [c['id'] for c in old])
    check('two added resolution cases', len(cases) == 37 and [c['id'] for c in cases[35:]] == ['BAN-X06','BAN-X07'])
    for original in inputs['originalAuthoredExamples'] + inputs['additionalReviewScenarios']:
        check('historical scenario: ' + original['id'], next(c for c in cases if c['id'] == original['id'])['historicalSourceScenario'] == original)
    check('all10question IDs retained', [q['id'] for q in model['questionDispositions']] == [f'BAN-{i:02}' for i in range(1,11)])
    check('four current dispositions', [q['id'] for q in model['repairDispositions']] == [f'BAN-R04-{i:02}' for i in range(1,5)])
    check('register/model questions agree', register['questionDispositions'] == model['questionDispositions'])
    check('register/model repairs agree', register['repairDispositions'] == model['repairDispositions'])
    for case in cases:
        check(case['id'] + ' source refs present', bool(case['sourceRefs']))
        for ref in case['sourceRefs']:
            entry = {'caseId':case['id'],**ref}
            if ref['pointer'].startswith('section:'):
                sections.append(entry)
                continue
            path = out / ref['path'] if ref['path'] == 'SPELL_MODEL.json' else G / ref['path']
            try:
                value = at(read(path),ref['pointer'])
                ok = value is not None
                entry['resolvedIdentity'] = ({k:value[k] for k in ['id','name'] if k in value} if isinstance(value,dict) else None)
            except (KeyError,IndexError,ValueError,FileNotFoundError):
                ok = False
            refs.append(entry)
            check(case['id'] + ' JSON reference ' + ref['path'] + ref['pointer'],ok)
    case17 = next(c for c in cases if c['id']=='BAN-C17')
    oracle_ref = next(r for r in case17['sourceRefs'] if r['path'].endswith('/oracle.json'))
    check('Oracle reroll reference has correct semantic identity', at(read(G/oracle_ref['path']),oracle_ref['pointer'])['id']=='oracle.supplement.spiral-touched.spiral-touched-boon-i')
    wizard_ref = next(r for r in case17['sourceRefs'] if r['path'].endswith('/wizard.json'))
    check('Wizard class counter has correct semantic identity', at(read(G/wizard_ref['path']),wizard_ref['pointer'])['id']=='wizard.base.counterspell')
    door_ref = next(r for r in cases[-1]['sourceRefs'] if r['path'].endswith('abjuration_conjuration_rank4_reviewed_03.json'))
    check('actual Door referenced by relocation case', '/spells/12/procedure' == door_ref['pointer'] and read(G/door_ref['path'])['spells'][12]['spellId']=='dimensional-door')
    resolutions = [
        {'findingId':'BAN-R04-01','disposition':'resolved','evidence':'C17 cites Oracle31, uses1/long rest/new result, and retains actual Wizard17 Reaction3RP, DC10+2rank,2-round recharge. Current source cards independently read.'},
        {'findingId':'BAN-R04-02','disposition':'resolved','evidence':'C27 tracks actual corpse/cargo/absent expired summon; no operative reservation. Model cosmologyBoundary namesBAN-CELL-03. Earlier archives preserve superseded dispositions even though this return carries only the immediate prior repair array.'},
        {'findingId':'BAN-R04-03','disposition':'resolved','evidence':'C13 same-center10x10 fits explicitly open terrain. C24 Pet square inside initial cell; east clearance expansion after creation. C30 movement5ft precedes legal Steed creation, subsequent x[-12.5,12.5]/y[-10,10] bounds contain an already free western Pet square before concentration replacement. All costs/source lifetimes remain real.'},
        {'findingId':'BAN-R04-04','disposition':'resolved as explicit NEW Banishment-only authorship','evidence':'BAN-CONFLICT-04 logical anchor preserves real location/range/terrain/source tests while withholding legal occupancy and ordinary movement. Does not globally rewrite body rules or forbid all spatial actions. X06 obstruction removal and X07 actual Action7RP/500ft/same-plane known destination Dimensional Door resolve conflict. Mandatory anatomy and absolute closure remain independent of return fit. Numerical balance and human adjudication quality remain unproven.'},
    ]
    audit = {
        'recordedAtUtc':datetime.now(timezone.utc).isoformat(),
        'status':'Independent bounded authored-coherence review passes; exact GPT acceptance requested before canonical application.',
        'archive':info(A/'DD_Banishment_Repair_04_Return.zip'),
        'browserResponse':info(A/'BANISHMENT_REPAIR_04_RETURN_ACTUAL_DOM.txt'),
        'checks':checks,'checkCount':len(checks),'failureCount':sum(not c['pass'] for c in checks),
        'resolvedJsonReferences':refs,'resolvedJsonReferenceCount':len(refs),'descriptiveSectionReferences':sections,'sourceReferenceCount':len(refs)+len(sections),
        'repairFindingDispositions':resolutions,'remainingBlockingFindings':[],
        'independentReviewScope':'Complete Repair03 model/register/Player/Director and35current adjudications were read. Complete Repair04 semantic diffs, changed source references and added cases were then read against actual authority. All unchanged content and historical objects verified structurally. This is authored review, not runtime execution.',
        'historicalPreservation':'Original49bindings/source card and28historical objects exact. All35prior case IDs retained. Complete prior archives/manifests remain preserved; no historical deletion.',
        'sourceInformationDeleted':0,'newRulesAdopted':False,'runtimeTestsExecuted':0,'humanPlaytested':False,
        'countsUnchanged':{'reviewed':434,'pending':414,'total':848},
    }
    assert audit['failureCount']==0
    target.write_bytes(encoded(audit))
    text = [
        'I have completed the independent local review of your exact Banishment Repair04 return. The four BAN-R04 findings are resolved within the explicit authored-playtest scope. Please perform the final exact-file coherence confirmation so I can apply this one ordinary spell without reopening AC4 or changing any source material.',
        'Exact archive: DD_Banishment_Repair_04_Return.zip;47,505bytes;SHA256004fff0990d1518da7317bfaca91a2cc06f661d83af20b5c6c2464e940d545a3.',
        f'Local verification:{len(checks)}checks,0failures;49source bindings unchanged;original complete source/access exact;35previous case IDs plusX06/X07=37;28historical objects exact;{len(refs)}JSON references resolve and{len(sections)}descriptive section references retained. Full current differences were independently read, including semantic identities rather than just pointer existence.',
    ]
    for item in resolutions:
        text.append(item['findingId']+': '+item['evidence'])
    text += [
        'Exact seven companion payloads:',
        json.dumps(manifest['files'],ensure_ascii=False,indent=2),
        'Scope to confirm: ordinary Banishment only; Action60ftV/S/F/base7RP/rank4 and all7class access records unchanged;CHA save/60elapsed-seconds concentration/one-live/hard-control guard explicitly authored; distinct nonteleport planar classification and exact Paladin predicates; same identities/real custody/mandatory body endings; legal preflight before cell expansion; all actual clocks; finite mandatory origin-plane closure with narrowly stated terminal endpoint-blocker exception; inherited body placement order plus explicitly NEW BAN-CONFLICT-04 only for Banishment-origin conflict. No global body-rule rewrite. Primary legal escape closes residual bodies/objects once. No natural-origin, named-plane, soul, deity or era settlement. Cleric Banish Unholy separate.',
        'If you find a concrete remaining contradiction, identify the exact file/pointer and actual source. Otherwise return DD_Banishment_Exact_Acceptance_04.zip containing ACCEPTANCE.json and EVIDENCE_MANIFEST.json. ACCEPTANCE.json should say ACCEPT FOR PROVISIONAL AUTHORED PLAYTEST APPLICATION, identify the exact archive and all seven payload hashes/lengths above,37case IDs,49source bindings,28preserved historical objects, all7new scoped rule IDs includingBAN-CONFLICT-04, and no remaining blocking authored-coherence finding. You are approving exact source-linked authored procedure only; no runtime/human/balance/canon/soul/origin/era/whole-game/publication approval. Do not revise payloads during this acceptance step; flag a concrete issue instead. Application will preserve all prior archives and record catalog/index integration separately.',
    ]
    request.write_text('\n\n'.join(text)+'\n',encoding='utf8',newline='\n')
    print(json.dumps({'audit':info(target),'request':info(request),'checks':len(checks),'failures':0,'blockingFindings':0}))


if __name__ == '__main__':
    main()
