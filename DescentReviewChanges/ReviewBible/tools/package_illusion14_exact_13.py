"""Render the actual Part5 accepted payload without further semantic changes."""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import zipfile
from apply_di7_ap_as_01 import G, R, A, info, encoded
from prepare_ac5_current_interfaces_01 import at
from package_damage_control25_exact_09 import render


def read(p):
    return json.loads(p.read_bytes())


def binding(path, raw):
    return {'path':path,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}


def main():
    root = A/'illusion-perception14-exact-13'
    zp = A/'DD_Illusion_Perception_14_Exact_13.zip'
    prep = A/'ILLUSION_PERCEPTION_14_EXACT_13_PREPARATION.json'
    checkp = A/'ILLUSION_PERCEPTION_14_EXACT_13_CHECK.json'
    requestp = A/'ILLUSION_PERCEPTION_14_EXACT_13_REQUEST.txt'
    assert not any(p.exists() for p in [root,zp,prep,checkp,requestp])
    source = R/'data/director/spell_proposals/illusion_perception_14_current_13.json'
    d = read(source)
    returned = A/'illusion-perception14-part5-return-01'
    reviewp = returned/'REVIEW.json'
    review = read(reviewp)
    questions = read(returned/'QUESTION_DISPOSITIONS.json')
    actualcases = read(returned/'CASE_REVIEW.json')
    declaration = read(returned/'SUCCESSOR_DECLARATION.json')
    replayp = A/'ILLUSION_PERCEPTION_14_CURRENT_13_REPLAY_CHECK.json'
    replay = read(replayp)
    checks, sources, frozen, context, buffers = [], {}, {}, {}, {}
    def ck(name, value):
        checks.append({'check':name,'passed':bool(value)})
        assert value, name
    def include(p):
        name = p.relative_to(G).as_posix()
        raw = p.read_bytes()
        if name in sources:
            assert sources[name] == raw
        sources[name] = raw
        return binding(name, raw)
    def put(name, raw):
        assert name not in buffers
        buffers[name] = raw
    def planned(name):
        return {'name':name,'bytes':len(buffers[name]),'sha256':hashlib.sha256(buffers[name]).hexdigest()}
    ck('Verified actual339-check replay',info(source) == replay['candidate'] and replay['checkCount'] == 339 and replay['failures'] == 0 and replay['operations'] == 2)
    ck('Actual14 semantic acceptance for integration',review['verdict']['repairedPayload'] == 'SEMANTICALLY_ACCEPTED_FOR_INTEGRATION' and review['verdict']['acceptedIdentities'] == 14)
    for filename, key, prefix, target, count in [
        ('DD_Illusion_Perception_14_Conference_12.zip','files','files/',frozen,72),
        ('DD_Control_Illusion_Current_Acceptance_Context_01.zip','sources','sources/',context,34),
    ]:
        with zipfile.ZipFile(A/filename) as z:
            manifest = json.loads(z.read('MANIFEST.json'))
            ck('Input ZIP integrity '+filename,z.testzip() is None and len(manifest[key]) == count)
            for b in manifest[key]:
                raw = z.read(prefix+b['path'])
                ck('Frozen exact input '+b['path'],binding(b['path'],raw) == {k:b[k] for k in ['path','bytes','sha256']})
                target[b['path']] = raw
                include(G/b['path'])
    navigation_path = (R/'docs/DEVELOPMENT_DIRECTION.md').relative_to(G).as_posix()
    context_drift = []
    for name,raw in context.items():
        if sources[name] != raw:
            ck('Only navigation differs from accepted context '+name,name == navigation_path)
            context_drift.append({'path':name,'frozen':binding(name,raw),'current':binding(name,sources[name]),'meaning':'Current development navigation only; all operative accepted-context sources remain exact.'})
        else:
            ck('Accepted-context source unchanged '+name,True)
    indexp = R/'data/public/spell_playtests/authored_review_index.json'
    idx = read(indexp)
    oldidx = json.loads(frozen[indexp.relative_to(G).as_posix()])
    byid = {s['id']:s for s in idx['entries']}
    oldby = {s['id']:s for s in oldidx['entries']}
    catp = R/'data/public/spell_playtests/catalog.json'
    cat = {s['id']:s for s in read(catp)['spells']}
    ids = [s['id'] for s in d['spells']]
    ck('All14 exact accepted pending identities',ids == declaration['acceptedSpellIds'] and len(set(ids)) == 14 and all('pending' in byid[i]['authoredStatus'] for i in ids))
    ck('Current525/323/249 baseline',idx['authoredCounts'] == {'reviewed':525,'pending':323} and idx['representationCounts']['completeReviewedStandaloneProcedures'] == 249)
    for s in d['spells']:
        ck('Exact full native source and access '+s['id'],s['completeSourceAndAccess'] == cat[s['id']] and byid[s['id']] == oldby[s['id']])
    changed = [i for i in byid if byid[i] != oldby[i]]
    dc = read(R/'data/public/spell_candidates/damage_control_25_reviewed_10.json')
    persistent = read(R/'data/public/spell_candidates/persistent_damage_20_reviewed_07.json')
    accepted45 = [s['id'] for m in [dc,persistent] for s in m['spells']]
    ck('Exactly45 actual accepted membership changes',len(changed) == 45 and set(changed) == set(accepted45))
    drift = [{'path':p,'frozen':binding(p,raw),'current':binding(p,sources[p])} for p,raw in frozen.items() if sources[p] != raw]
    ck('Only current index and navigation drift',{x['path'] for x in drift} == {indexp.relative_to(G).as_posix(),(R/'docs/DEVELOPMENT_DIRECTION.md').relative_to(G).as_posix()})
    for p in [source,catp,indexp,replayp,A/'ILLUSION_PERCEPTION_14_CURRENT_13_REPLAY_RECEIPT.json',A/'ILLUSION_PERCEPTION_14_PART5_RETURN_01_RECEIPT.json',A/'ILLUSION_PERCEPTION_14_PART5_RETURN_01_NATIVE.json',R/'tools/apply_illusion14_part5_to_current13.py',R/'tools/record_part5_illusion_return_companion_submission_01.py',R/'tools/package_illusion14_exact_13.py',A/'CONTROL_ILLUSION_CURRENT_ACCEPTANCE_CONTEXT_01.json',A/'CONTROL_ILLUSION_CURRENT_ACCEPTANCE_CONTEXT_01_CHECK.json']:
        include(p)
    for p in returned.iterdir():
        if p.is_file():
            include(p)
    ctx = read(A/'CONTROL_ILLUSION_CURRENT_ACCEPTANCE_CONTEXT_01.json')
    convergence = {
        'frozenConferenceArchive':info(A/'DD_Illusion_Perception_14_Conference_12.zip'),
        'acceptedContextArchive':info(A/'DD_Control_Illusion_Current_Acceptance_Context_01.zip'),
        'frozenConferenceSourceCount':72,'acceptedContextSourceCount':34,
        'currentIndex':info(indexp),'originalCounts':oldidx['authoredCounts'],'currentCounts':idx['authoredCounts'],
        'currentRepresentationCounts':idx['representationCounts'],
        'completeMembershipChanges':[{'id':i,'before':oldby[i],'after':byid[i]} for i in changed],
        'actualAcceptedApplications':deepcopy(ctx['acceptedApplications']),
        'sourceDrift':drift,'acceptedContextNavigationDrift':context_drift,
        'driftMeaning':'The conference retains its480/368 index; the separately submitted accepted-context supplement supplies the45 actual accepted identities and current525/323/249 index. Current DEVELOPMENT_DIRECTION navigation has progressed; no rule source or any of these14 pending entries changed.',
        'currentAcceptedAuthorityPolicy':'The accepted supplement and its exact named receipts/models govern current DamageControl25/Persistent20 use. Historical pending comparisons remain evidence. Greater Phantasmal Killer is accepted only in Persistent20 scope; Mental Prison and Control15 remain pending.',
    }
    shared, selectors = {}, {}
    routes = {r['spellId']:r for r in d['sharedContractRouting10']}
    for s in d['spells']:
        route = routes[s['id']]
        group = int(route['currentSharedContextPointer'].split('/')[2])+1
        rawrules = at(d,route['currentSharedContextPointer'])
        selectors[s['id']] = []
        for key in route['applicableKeys']:
            rid = 'IP14-SOURCE'+str(group)+'-'+key
            if rid not in shared:
                shared[rid] = {'id':rid,'completeText':deepcopy(rawrules[key]),'applicableSpellIds':[],'source':deepcopy(route['fullOriginalSource']),'candidatePointer':route['currentSharedContextPointer']+'/'+key,'scope':'Only listed accepted Illusion14 cards. Named rules for other cards grant no capability here. Actual accepted interfaces and each selected current procedure control their explicit scopes and exceptions.'}
            ck('Identical routed shared clause '+s['id']+'/'+key,shared[rid]['completeText'] == rawrules[key])
            shared[rid]['applicableSpellIds'].append(s['id'])
            selectors[s['id']].append(rid)
    spells = []
    for n,s in enumerate(d['spells']):
        spells.append({
            'id':s['id'],'name':s['completeSourceAndAccess']['name'],
            'completeSourceAndAccess':deepcopy(s['completeSourceAndAccess']),
            'procedure':s['procedure'],'selectedProcedureSource':{'candidate':info(source),'pointer':'/spells/'+str(n)+'/procedure'},
            'sharedRuleIds':selectors[s['id']],'completeEarlierRecordUnchanged':deepcopy(s['completeEarlierRecordUnchanged']),
            'originalSourceReference':deepcopy(s['originalSourceReference']),
            'actualDispositions':[deepcopy(q) for q in questions['dispositions'] if s['id'] in q['spells']],
        })
    limits = {'holds':deepcopy(review['holds']),'originalScenarios':28,'currentCases':28,'supplementalCases':3,
        'conditionalCasePolicy':'Semantic acceptance preserves every conditional premise. A pending counterpart, a historical mid-resolution interrupt premise or an unspecified event source is not proven executable content. N29 remains conditional Mental Prison composition; Mind Maze ordinary Ready occurs after the actual completed attack.',
        'runtimeImplemented':False,'runtimeTestsExecuted':0,'humanPlaytested':False,'numericalBalanceApproved':False,'cosmologyCanonModified':False,'domainGatesDistinct':75,'wholeGameComplete':False,'releaseApproved':False,'sourceInformationDeleted':0}
    routing = 'Only spells[].procedure and its listed sharedRuleIds are the selected complete current rules. Actual Part5 question/case dispositions resolve frozen pending labels. Exact source-specific exceptions override their contrary earlier proposal text only for the named card. Earlier records, questions, statuses and replaced procedures remain history. Accepted external interfaces retain their actual scopes; no other pending card or class access is approved by inclusion.'
    model = {'schemaVersion':'1.0','moduleId':'ILLUSION-PERCEPTION14-EXACT13','status':'Actual repaired semantics accepted for integration; exact canonical rendering pending final review','candidate':info(source),'spells':spells,'sharedRules':shared,'actualSemanticReview':info(reviewp),'actualSemanticReturn':info(A/'ILLUSION_PERCEPTION_14_PART5_RETURN_01_RECEIPT.json'),'actualQuestionDispositions':deepcopy(questions),'actualReversibleApplication':deepcopy(d['part5SemanticApplication13']),'currentSourceConvergence':convergence,'authorityRouting':routing,'contentLimits':limits,'runtimeSelectionEnabled':False,'newRuleAdoptions':0,'sourceInformationDeleted':0}
    casebook = {'schemaVersion':'1.0','id':'ILLUSION-PERCEPTION14-CASEBOOK13','status':'Actual complete cases semantically accepted with stated conditions; no runtime execution','cases':deepcopy(d['currentExamples']),'supplementalCases':deepcopy(d['supplementalVectors09']),'originalScenarioTextsUnchanged':deepcopy(d['originalExamplesUnchanged']),'completeActualCaseReview':deepcopy(actualcases),'contentLimits':limits,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}
    header = '# Illusion and perception spells — video game candidate\n\nFourteen existing spell identities. The repaired procedures have completed semantic review; this exact rendering awaits final integration review. Creation is a separate review.\n\n'
    player, director = header, header
    for s in spells:
        chapter = '## '+s['name']+'\n\n| Class | School | Rank | Minimum class level | Base RP |\n|---|---|---:|---:|---:|\n'
        for cl,x in s['completeSourceAndAccess']['classAccess'].items():
            chapter += f"| {cl} | {x['school']} | {x['rank']} | {x['minimumClassLevel']} | {x['baseRpCost']} |\n"
        chapter += '\n'+s['procedure']+'\n\n'
        player += chapter
        director += chapter+'Applicable shared clauses: '+', '.join(s['sharedRuleIds'])+'.\n\n'
    common = '## Shared procedures by source and applicable spell\n\nThe following clauses apply only to their listed spells. Each spell’s complete procedure controls its expressly stated local exception. Clauses about other named spells supply no additional ability.\n\n'
    for rid,rule in shared.items():
        common += '### '+rid+'\n\nApplies to: '+', '.join(rule['applicableSpellIds'])+'.\n\n'+rule['completeText']+'\n\n'
    player += common+'## Conditional interactions\n\nTrue Seeing’s Mental Prison interaction applies only if that separately reviewed procedure becomes operative. It does not approve Mental Prison. Mind Maze’s ordinary Ready example releases after the attack finishes; the historical mid-resolution example remains conditional on a genuine interrupt source. Runtime implementation, human gameplay and balance remain separate.\n'
    director += common+'## Authority routing\n\n'+routing+'\n\n## Actual question dispositions\n\n'+render(questions)+'## Source convergence\n\n'+render(convergence)+'## Remaining gates and conditions\n\n'+render(limits)
    for label,data in [('Complete current cases',casebook['cases']),('Complete supplemental cases',casebook['supplementalCases']),('Original scenario texts, unchanged',casebook['originalScenarioTextsUnchanged']),('Actual complete case review',actualcases)]:
        director += '## '+label+'\n\n```json\n'+json.dumps(data,ensure_ascii=False,indent=2)+'\n```\n\n'
    for name,chapter in [('PLAYER_CHAPTER.md',player),('DIRECTOR_REVIEW.md',director)]:
        for s in spells:
            ck('Full selected procedure '+name+'/'+s['id'],s['procedure'] in chapter)
        for rid,rule in shared.items():
            ck('Full routed clause '+name+'/'+rid,rule['completeText'] in chapter)
    ck('No local case rewrites',casebook['cases'] == d['currentExamples'] and casebook['supplementalCases'] == d['supplementalVectors09'])
    ck('Both explicit repair paragraphs retained','IP14-STEED-SUPPRESS-13' in player and 'IP14-SPECTRAL-HIDDEN-TARGET-13' in player)
    put('SPELLS_MODEL.json',encoded(model))
    put('CASEBOOK.json',encoded(casebook))
    put('PLAYER_CHAPTER.md',player.encode())
    put('DIRECTOR_REVIEW.md',director.encode())
    put('SOURCE_HASHES.json',encoded({'id':'ILLUSION-PERCEPTION14-SOURCES13','currentSources':[dict(binding(p,b),archivePath='sources/'+p) for p,b in sorted(sources.items())],'frozenConferenceSources':[dict(binding(p,b),archivePath='historical-conference12/'+p) for p,b in sorted(frozen.items())],'acceptedContextSources':[dict(binding(p,b),archivePath='accepted-context01/'+p) for p,b in sorted(context.items())],'sourceConvergence':convergence,'scope':'Complete source bytes remain separate from current authored routing. No pending counterpart, cosmology or future artifact is approved by inclusion.'}))
    register = {'id':'ILLUSION-PERCEPTION14-EXACT13-REGISTER','status':'Actual repaired semantics accepted; exact rendered artifacts pending review','spellIds':ids,'candidate':info(source),'placementCount':sum(len(s['completeSourceAndAccess']['source']['original']['placements']) for s in spells),'mainCases':28,'supplementalCases':3,'originalScenarios':28,'sharedClauses':len(shared),'replayedOperations':2,'caseRewrites':0,'contentLimits':limits,'applicationPlan':{'preconditions':'Confirm these exact eight complete rendered artifacts preserve the actual accepted repaired semantics. Record exact GPT verdict and independently verify unchanged source/access and current pending membership before canonical copies and separate authored-index application.','canonicalByteCopies':{'SPELLS_MODEL.json':'DescentReviewChanges/ReviewBible/data/public/spell_candidates/illusion_perception_14_reviewed_13.json','CASEBOOK.json':'DescentReviewChanges/ReviewBible/data/playtest/spell_candidates/illusion_perception_14_cases_13.json','PLAYER_CHAPTER.md':'DescentReviewChanges/ReviewBible/docs/spells/candidates/ILLUSION_PERCEPTION_14_REVIEWED_13.md','DIRECTOR_REVIEW.md':'DescentReviewChanges/ReviewBible/docs/director-only/spells/ILLUSION_PERCEPTION_14_REVIEWED_13.md'},'membership':'All14 at the frozen525/323/249 baseline project539/309/263 only after verified application. Recompute from live index; pending Companion10 review may change the baseline separately. No future unseen index or registry is preapproved.','runtimeSelectionEnabled':False,'unrelatedAuthoritiesUnchanged':True},'newRuleAdoptions':0,'sourceInformationDeleted':0}
    put('REGISTER.json',encoded(register))
    notes = '''# Illusion/Perception14 exact13 integration review

Actual Part5 assistant1329ce3a-137c-4789-928c-b0eda39df21e semantically accepted the exact repaired payload for integration after two necessary procedure repairs. Current13 exactly replays both and reverses to Current12, with339 passing source/hash/case/pointer checks. No local semantic alterations, source deletions or case rewrites were added. Current13 metadata records the actual decision; the exact returned payload remains unchanged in full.

Greater Phantom Steed full creating-source suppression is an explicit Steed-only ending event, not inherited AC5/AC6 summon pause. Spectral Army's unrecognized-image creature-target bridge permits an otherwise legal paid attempt, then actual noncreature eligibility fails before rolls without diagnostic. It neither makes images creatures nor grants their ordinary Attack Action detonation exception to creature-only spells.

All14 procedures,28 original scenarios,28 current cases,three supplements and16 decisions remain complete. This rendering selects only the previously routed shared clauses and preserves their exact text. Actual external interfaces retain their scope; selected card-specific procedures override contrary historical text only for their card. True Seeing's two source placement benefits remain united with actual class school access unchanged. Mental Prison, Control15 and Creation remain pending; historical Mind Maze mid-resolution interrupt remains conditional. No additional DE4 information channel is added.

All72 frozen conference sources and34 separately reviewed current acceptance sources are supplied. The current source tree differs from the frozen conference only in the accepted45/index progression and current DEVELOPMENT_DIRECTION navigation. All14 pending identity records and full native catalog/access objects remain unchanged. The exact source-convergence record and complete current authority files preserve these distinctions.

Review the eight exact files for faithful canonical rendering and cross-document flow. Reuse the completed semantic review; reopen only a concrete new contradiction or omission. If coherent return ACCEPT_BYTE_IDENTICAL_FOR_PROVISIONAL_AUTHORED_ILLUSION_PERCEPTION14_VIDEO_GAME_CANDIDATE_WITH_CONDITIONAL_HOLDS, binding all eight filenames/bytes/SHA256, all14 identity dispositions and explicit preserved holds. Otherwise return only necessary full before/after pointer corrections. Do not approve future unseen repository changes, runtime, human playtests, balance, cosmology,75-domain closure, whole-game completion or release.
'''
    put('LOCAL_REVIEW_NOTES.md',notes.encode())
    put('EVIDENCE_MANIFEST.json',encoded({'id':'ILLUSION-PERCEPTION14-EXACT13-MANIFEST','files':[planned(n) for n in sorted(buffers)],'selfHashConvention':'Seven companion files bound here; outer preparation binds the eighth manifest.','pendingActualExactRenderingReview':True}))
    ck('Eight exact canonical artifacts',len(buffers) == 8)
    root.mkdir()
    for n,raw in buffers.items():
        (root/n).write_bytes(raw)
    checkp.write_bytes(encoded({'candidate':info(source),'checks':checks,'checkCount':len(checks),'failures':0,'currentSources':len(sources),'frozenConferenceSources':72,'acceptedContextSources':34,'sharedClauses':len(shared),'mainCases':28,'supplementalCases':3,'originalScenarios':28,'localSemanticChangesBeyondActualReturn':0,'caseRewrites':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}))
    readme = 'Read current/REGISTER.json and LOCAL_REVIEW_NOTES.md. Then review all eight current artifacts, using the complete actual Part5 return and replay evidence in sources/. historical-conference12/ and accepted-context01/ preserve the exact prior inputs. Actual semantic acceptance is established; this packet asks only faithful exact canonical integration review and any concrete remaining defect.\n'
    with zipfile.ZipFile(zp,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        z.writestr('README.md',readme)
        z.writestr('LOCAL_ARTIFACT_CHECK.json',checkp.read_bytes())
        for name,raw in buffers.items():
            z.writestr('current/'+name,raw)
        for prefix,data in [('sources/',sources),('historical-conference12/',frozen),('accepted-context01/',context)]:
            for name,raw in sorted(data.items()):
                z.writestr(prefix+name,raw)
    with zipfile.ZipFile(zp) as z:
        ck('Final ZIP CRC and unique members',z.testzip() is None and len(z.namelist()) == len(set(z.namelist())))
        for name,raw in buffers.items():
            assert z.read('current/'+name) == raw
        for prefix,data in [('sources/',sources),('historical-conference12/',frozen),('accepted-context01/',context)]:
            assert all(z.read(prefix+name) == raw for name,raw in data.items())
        membercount = len(z.namelist())
    b = info(zp)
    requestp.write_text(f'Please review {zp.name} ({b["bytes"]} bytes; SHA256 {b["sha256"]}) for faithful exact canonical integration. Your actual Part5 repaired payload is semantically accepted for integration; Current13 exactly replayed/reversed both procedure changes with339 checks and zero case rewrites. No further local semantic alteration. Eight complete canonical artifacts contain14 procedures, source-routed shared clauses,28 original scenarios,28 current cases,three supplements and16 actual dispositions. Preserve all conditional holds and actual class access. Reuse accepted decisions; reopen only a concrete new contradiction or omission. If coherent return ACCEPT_BYTE_IDENTICAL_FOR_PROVISIONAL_AUTHORED_ILLUSION_PERCEPTION14_VIDEO_GAME_CANDIDATE_WITH_CONDITIONAL_HOLDS with all eight filename/bytes/SHA256 and14 individual identity dispositions. Otherwise exact full before/after operations only. No future unseen application, runtime, human gameplay, balance, cosmology,75-domain, whole-game or release approval.\n',encoding='utf8',newline='\n')
    prep.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PREPARED UNSENT; CompanionExact05 actual GPT review active at preparation','archive':b,'candidate':info(source),'currentFiles':[info(root/n) for n in sorted(buffers)],'artifactCheck':info(checkp),'request':info(requestp),'currentSourceCount':len(sources),'frozenConferenceSourceCount':72,'acceptedContextSourceCount':34,'archiveMemberCount':membercount,'allArchiveMembersVerified':True,'postArchiveIntegrityCheckPassed':True,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}))
    print(json.dumps({'archive':b,'preparation':info(prep),'checksInFrozenReport':len(checks)-1,'postArchiveIntegrityChecks':1,'sharedClauses':len(shared),'currentSources':len(sources),'members':membercount}))


if __name__ == '__main__':
    main()
