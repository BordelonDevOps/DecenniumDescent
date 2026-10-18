"""Exactly replay and reverse the two actual GPT repairs into a preserved successor."""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import zipfile
from apply_di7_ap_as_01 import G, R, A, info, encoded
from prepare_ac5_current_interfaces_01 import at
from prepare_de4_fate_guard_amendment_01 import parent


def read(p):
    return json.loads(p.read_bytes())


def binding(path, raw):
    return {'path':path,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}


def differences(a, b, path=''):
    if type(a) != type(b):
        return [path]
    if isinstance(a, dict):
        if set(a) != set(b):
            return [path]
        return [p for k in a for p in differences(a[k], b[k], path+'/'+k.replace('~','~0').replace('/','~1'))]
    if isinstance(a, list):
        if len(a) != len(b):
            return [path]
        return [p for n, (x,y) in enumerate(zip(a,b)) for p in differences(x,y,path+'/'+str(n))]
    return [] if a == b else [path]


def main():
    root = A/'illusion-perception14-part5-return-01'
    oldp = R/'data/director/spell_proposals/illusion_perception_14_current_12.json'
    out = oldp.with_name('illusion_perception_14_current_13.json')
    report = A/'ILLUSION_PERCEPTION_14_CURRENT_13_REPLAY_CHECK.json'
    receiptp = A/'ILLUSION_PERCEPTION_14_CURRENT_13_REPLAY_RECEIPT.json'
    assert not any(p.exists() for p in [out, report, receiptp])
    checks = []
    def ck(name, value):
        checks.append({'check':name,'passed':bool(value)})
        assert value, name
    source = read(oldp)
    oldraw = oldp.read_bytes()
    proposal = read(root/'POINTER_OPERATIONS.json')
    declaration = read(root/'SUCCESSOR_DECLARATION.json')
    rr = read(A/'ILLUSION_PERCEPTION_14_PART5_RETURN_01_RECEIPT.json')
    ck('Exact actual base candidate',info(oldp) == proposal['baseCandidate'] == declaration['baseCurrent12'])
    ck('Actual assistant identity',rr['actualAssistantMessageId'] == '1329ce3a-137c-4789-928c-b0eda39df21e')
    ck('Exact returned archive',info(G/rr['returnedArchive']['path']) == rr['returnedArchive'])
    frozen, context = {}, {}
    for filename, key, prefix, target, expected in [
        ('DD_Illusion_Perception_14_Conference_12.zip','files','files/',frozen,72),
        ('DD_Control_Illusion_Current_Acceptance_Context_01.zip','sources','sources/',context,34),
    ]:
        with zipfile.ZipFile(A/filename) as z:
            ck('ZIP CRC '+filename,z.testzip() is None)
            manifest = json.loads(z.read('MANIFEST.json'))
            ck('Complete input manifest '+filename,len(manifest[key]) == expected)
            for b in manifest[key]:
                raw = z.read(prefix+b['path'])
                ck('Frozen input '+b['path'],binding(b['path'],raw) == {k:b[k] for k in ['path','bytes','sha256']})
                target[b['path']] = raw
    ck('Exact original candidate from submitted archive',frozen[proposal['baseCandidate']['path']] == oldraw)
    for b in source['sourceBindings']:
        ck('Retained nested source '+b['path'],binding(b['path'],frozen[b['path']]) == b)
    d = deepcopy(source)
    operations = proposal['operations']
    paths = ['/spells/4/procedure','/spells/11/procedure']
    ck('Exactly two scoped replacements',[o['jsonPointer'] for o in operations] == paths and all(o['op'] == 'replace' for o in operations))
    for o in operations:
        par, key = parent(d, o['jsonPointer'])
        ck('Exact before '+o['spellId'],par[key] == o['before'])
        par[key] = deepcopy(o['after'])
    returnedp = root/declaration['exactPatchedPayload']['file']
    rb = info(returnedp)
    ck('Exact returned repaired bytes',all(rb[k] == declaration['exactPatchedPayload'][k] for k in ['bytes','sha256']))
    ck('Full replay equals actual repaired payload',d == read(returnedp))
    ck('Exactly two actual JSON differences',differences(source,d) == paths)
    reverse = deepcopy(d)
    for o in reversed(operations):
        par,key = parent(reverse,o['jsonPointer'])
        ck('Exact reverse after '+o['spellId'],par[key] == o['after'])
        par[key] = deepcopy(o['before'])
    ck('Full reverse equals original candidate',reverse == source)
    for key in source:
        if key != 'spells':
            ck('Entire unchanged top-level field '+key,source[key] == d[key])
    for before, after in zip(source['spells'], d['spells']):
        ck('Complete source/access/history '+before['id'],all(before[k] == after[k] for k in before if k != 'procedure'))
    cases = read(root/'CASE_REVIEW.json')
    actualcases = {c['id']:c for c in cases['currentCases']}
    originals = {c['id']:c for c in d['originalExamplesUnchanged']}
    ck('28 originals and28 current complete cases',len(originals) == len(actualcases) == len(d['currentExamples']) == 28)
    for c in d['currentExamples']:
        reviewed = actualcases[c['id']]
        ck('Exact complete current reviewed case '+c['id'],reviewed['completeCurrentCase'] == c)
        ck('Exact complete original scenario '+c['id'],reviewed['completeOriginalScenario'] == originals[c['id']]['exactOriginalText'] == c['originalTextUnchanged'])
        ref = originals[c['id']]['sourceReference']
        ck('Exact native scenario text '+c['id'],at(json.loads(frozen[ref['path']]),ref['pointer']) == originals[c['id']]['exactOriginalText'])
    supp = {c['id']:c for c in cases['supplementalCases']}
    ck('Three complete supplements',len(supp) == len(d['supplementalVectors09']) == 3)
    for c in d['supplementalVectors09']:
        ck('Exact complete supplemental case '+c['id'],supp[c['id']]['completeCurrentCase'] == c)
    questions = read(root/'QUESTION_DISPOSITIONS.json')
    ck('16 question IDs retained',[q['id'] for q in questions['dispositions']] == [q['id'] for q in d['conferenceDecisions10']])
    for before, after in zip(d['conferenceDecisions10'],questions['dispositions']):
        ck('Exact submitted question '+before['id'],before['question'] == after['submittedQuestion'])
    ck('All14 exact accepted identities',[s['id'] for s in d['spells']] == declaration['acceptedSpellIds'] and len(d['spells']) == 14)
    ck('Creation explicitly excluded',declaration['excludedSpellIds'] == ['creation'] and questions['dispositions'][-1]['disposition'] == 'HOLD_SEPARATE')
    catp = R/'data/public/spell_playtests/catalog.json'
    cat = {s['id']:s for s in read(catp)['spells']}
    indexp = R/'data/public/spell_playtests/authored_review_index.json'
    idx = read(indexp)
    byid = {s['id']:s for s in idx['entries']}
    ck('Current index matches accepted supplement',indexp.read_bytes() == context[indexp.relative_to(G).as_posix()])
    ck('525/323 membership unchanged',idx['authoredCounts'] == {'reviewed':525,'pending':323})
    for s in d['spells']:
        ck('Current catalog source and actual class access '+s['id'],s['completeSourceAndAccess'] == cat[s['id']] and 'pending' in byid[s['id']]['authoredStatus'])
    ck('Steed endpoint names only its scoped rule','NEW IP14-STEED-SUPPRESS-13' in d['spells'][4]['procedure'] and 'no other summon, mount or magical body gains it' in d['spells'][4]['procedure'])
    ck('Spectral hidden-target bridge remains local','NEW IP14-SPECTRAL-HIDDEN-TARGET-13' in d['spells'][11]['procedure'] and 'does not modify ordinary casting globally' in d['spells'][11]['procedure'])
    ck('Original bytes untouched',oldp.read_bytes() == oldraw)
    history = {k:deepcopy(d[k]) for k in ['id','recordedAtUtc','status']}
    d.update(id='ILLUSION-PERCEPTION-14-CURRENT-13',recordedAtUtc=datetime.now(timezone.utc).isoformat(),status='Exact Part5 repaired payload semantically accepted for integration; two operations replayed and reversed. Canonical rendering/application pending. All original sources/cases and conditional holds preserved. No authored-index membership or runtime approval yet.')
    d['part5SemanticApplication13'] = {
        'actualReturnReceipt':info(A/'ILLUSION_PERCEPTION_14_PART5_RETURN_01_RECEIPT.json'),
        'actualOperations':info(root/'POINTER_OPERATIONS.json'),'actualRepairedPayload':info(returnedp),
        'actualReview':info(root/'REVIEW.json'),'actualQuestionDispositions':info(root/'QUESTION_DISPOSITIONS.json'),
        'actualCaseDispositions':info(root/'CASE_REVIEW.json'),'previousCandidate':info(oldp),
        'previousMetadataUnchanged':history,'onlySemanticDiffPointers':paths,
        'codexConcurrence':'Both exact repairs inspected in their full procedures and actual question/case dispositions. The Steed-only endpoint removes unsupported shared inheritance; the Spectral-only apparent-target bridge supplies the paid hidden-eligibility ordering required by N31. No additional local rule change.',
        'holds':read(root/'REVIEW.json')['holds'],
        'authorityRouting':'Selected complete spells[].procedure plus source-specific routed shared clauses; actual Part5 dispositions resolve prior pending questions. Frozen prior status labels and unresolved issue text are history, not a second competing authority.',
        'authoredCountsUnchanged':idx['authoredCounts'],'sourceInformationDeleted':0,'runtimeTestsExecuted':0,
        'canonicalApplicationComplete':False,'futureUnseenArtifactAcceptanceClaimed':False,
    }
    out.write_bytes(encoded(d))
    report.write_bytes(encoded({'id':'ILLUSION-PERCEPTION14-CURRENT13-REPLAY-CHECK','candidate':info(out),'original':info(oldp),'actualRepairedPayload':info(returnedp),'checks':checks,'checkCount':len(checks),'failures':0,'operations':2,'frozenConferenceSources':72,'acceptedContextSources':34,'originalScenarios':28,'currentCases':28,'supplementalCases':3,'questions':16,'membershipChanged':False,'scope':'Exact source/hash/pointer replay/reversal and complete case preservation. No runtime execution, numerical balance, human gameplay or domain closure.'}))
    receiptp.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'SEMANTICALLY_ACCEPTED_PAYLOAD_REPLAYED; CANONICAL_APPLICATION_PENDING','candidate':info(out),'original':info(oldp),'actualReturnReceipt':info(A/'ILLUSION_PERCEPTION_14_PART5_RETURN_01_RECEIPT.json'),'replayCheck':info(report),'operationsApplied':2,'originalReplaced':False,'semanticRuleChangesBeyondActualReturn':0,'authoredCountsUnchanged':idx['authoredCounts'],'holds':d['part5SemanticApplication13']['holds'],'sourceInformationDeleted':0,'nextStep':'Render complete source-routed model, casebook, player and Director views; verify convergence and exact canonical artifacts before authored-index application.'}))
    print(json.dumps({'candidate':info(out),'replayCheck':info(report),'receipt':info(receiptp),'checks':len(checks),'operations':2,'caseRewrites':0}))


if __name__ == '__main__':
    main()
