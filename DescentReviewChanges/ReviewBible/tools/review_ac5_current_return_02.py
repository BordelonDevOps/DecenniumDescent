"""Verify the preserved AC5 return structurally; do not adopt it."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib, json, zipfile
from apply_di7_ap_as_01 import G, R, A, encoded, info
from prepare_ac5_current_interfaces_01 import at

def read(p):
    return json.loads(p.read_bytes())

def main():
    out = A / 'ac5-current-review-02-return'
    inp = A / 'ac5-current-review-02-input'
    dest = A / 'AC5_CURRENT_RETURN_02_STRUCTURAL_CHECK.json'
    assert not dest.exists()
    checks = []
    def check(label, value, **details):
        checks.append({'check': label, 'pass': bool(value), **details})
    archive = A / 'DD_AC5_Current_Review_02_Return.zip'
    b = archive.read_bytes()
    check('Returned archive exact byte length', len(b) == 142855)
    check('Returned archive published SHA256', hashlib.sha256(b).hexdigest() == '9ff02c40e398ff9edf9d7df7b7bbf7f26c9282496fab9f6a1407e0327908a82e')
    expected = {'REGISTER.json','SPELLS_MODEL.json','PLAYER_CHAPTER.md','DIRECTOR_REVIEW.md','CASEBOOK.json','SOURCE_HASHES.json','VERDICT.md','EVIDENCE_MANIFEST.json'}
    with zipfile.ZipFile(archive) as z:
        check('Exactly eight safe root files', len(z.namelist()) == 8 and set(z.namelist()) == expected)
        for n in sorted(expected): check('Extracted bytes equal archived member', (out/n).read_bytes() == z.read(n), path=n)
    mf = read(out/'EVIDENCE_MANIFEST.json')
    for x in mf['files']:
        raw = (out/x['name']).read_bytes()
        check('Output manifest exact bytes and digest', len(raw)==x['bytes'] and hashlib.sha256(raw).hexdigest()==x['sha256'], path=x['name'])
    bindings = read(inp/'SOURCE_MANIFEST.json')['bindings']
    check('Returned frozen bindings exactly preserved', read(out/'SOURCE_HASHES.json')['bindings'] == bindings)
    for x in bindings:
        for root, label in [(inp/'sources', 'Frozen input source'), (G,'Current project source')]:
            p=root/x['path'];raw=p.read_bytes()
            check(label+' unchanged',len(raw)==x['bytes'] and hashlib.sha256(raw).hexdigest()==x['sha256'],path=x['path'])
    model=read(out/'SPELLS_MODEL.json'); register=read(out/'REGISTER.json'); cases=read(out/'CASEBOOK.json')['cases']; source=read(inp/'CURRENT_REVIEW_INPUT.json')
    selected={x['spellId']:x for x in source['selectedRecords']}
    check('Sixteen unique identities in original order',[s['id'] for s in model['spells']]==list(selected) and len(selected)==16)
    for s in model['spells']:
        check('Full source/access object preserved',s['completeSourceAndAccess']==selected[s['id']]['completeCurrentSourceAndAccess'],spellId=s['id'])
        check('Original question preserved',s['historicalQuestion']==selected[s['id']]['historicalQuestionUnchanged'],spellId=s['id'])
        check('Complete current procedure exists',isinstance(s['procedure'],str) and len(s['procedure'])>300,spellId=s['id'])
        check('Exact procedure represented in both chapters',all(s['procedure'] in (out/n).read_text(encoding='utf8') for n in ['PLAYER_CHAPTER.md','DIRECTOR_REVIEW.md']),spellId=s['id'])
    check('Seventeen printed placements',sum(len(s['completeSourceAndAccess']['source']['original']['placements']) for s in model['spells'])==17)
    original={x['id']:x['originalText'] for x in source['originalExamples']}
    expected_case_ids=list(original)+[f'AC5-X{i:02}' for i in range(1,25)]+[f'AC5-K{i:02}' for i in range(1,9)]
    check('54 unique cases in required order',[x['id'] for x in cases]==expected_case_ids)
    for c in cases:
        if c['id'] in original:check('Historical example text exactly preserved',c['historicalOriginalText']==original[c['id']],caseId=c['id'])
        check('Current case has initial state, actions and outcome',bool(c['currentInitialState'] and c['actionsAndResolution'] and c['currentAdjudication']),caseId=c['id'])
    for mk,rk,ids in [('originalQuestionDispositions','questionDispositions',[x['questionId'] for x in source['selectedRecords']]),('currentInterfaceIssueDispositions','currentInterfaceIssueDispositions',[x['id'] for x in source['currentReviewIssues']]),('classInterfaceIssueDispositions','classInterfaceIssueDispositions',[x['id'] for x in source['currentClassInterfaceAddendum']['issues']])]:
        check('Disposition IDs and register/model consistency', [x['id'] for x in model[mk]]==ids and register[rk]==model[mk],kind=mk)
    pointer_count=0; descriptive=[];cache={}
    for parent in model['spells']+cases:
        refs=parent['sourceRefs'];check('Source references populated',bool(refs),owner=parent.get('id'))
        for ref in refs:
            path=ref['path'];pointer=ref.get('pointer','');p=(out/path) if path in expected else (inp/'sources'/path)
            check('Reference file exists',p.is_file(),owner=parent['id'],path=path)
            if pointer.startswith('/'):
                try:
                    if p not in cache:cache[p]=read(p)
                    at(cache[p],pointer);ok=True
                except (KeyError,IndexError,ValueError,TypeError):ok=False
                check('JSON pointer resolves structurally',ok,owner=parent['id'],path=path,pointer=pointer);pointer_count+=1
            else:descriptive.append({'owner':parent['id'],**ref})
    for k in ['runtimeTestsExecuted','humanPlaytested','balanceApproved']:check('No unsupported approval claimed',model[k] is False,flag=k)
    failures=[x for x in checks if not x['pass']]
    report={'id':'AC5-CURRENT-RETURN-02-STRUCTURAL-CHECK','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'Source/archive preservation and reference checks only; semantic review remains separate. No adoption.','archive':info(archive),'files':[info(out/n) for n in sorted(expected)],'sourceBindings':len(bindings),'spellIdentities':len(model['spells']),'placements':17,'caseCount':len(cases),'historicalTexts':len(original),'jsonPointersChecked':pointer_count,'descriptiveReferences':descriptive,'checks':checks,'checkCount':len(checks),'failureCount':len(failures),'failures':failures,'newSpellAdoptions':0,'runtimeTestsExecuted':0,'humanPlaytested':False,'sourceInformationDeleted':0}
    dest.write_bytes(encoded(report))
    print(json.dumps({'report':info(dest),'checks':len(checks),'failures':failures,'jsonPointersChecked':pointer_count,'descriptiveReferences':len(descriptive)}))

if __name__=='__main__':main()
