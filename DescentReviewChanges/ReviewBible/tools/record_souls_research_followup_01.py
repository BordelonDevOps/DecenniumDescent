"""Preserve the first candidate and record the active gameplay revision conference."""
from datetime import datetime,timezone
import ast,json,subprocess,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_PLANES_SOULS_SUBMISSION_01.json'
    target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_SOULS_RESEARCH_FOLLOWUP_01.json'
    receipt=A/'COSMOLOGY_SOULS_RESEARCH_01_FOLLOWUP_RECEIPT.json'
    delta=A/'SOULS_RESEARCH_FOLLOWUP_01_NAVIGATION_DELTA.json';preserved=A/'navigation-before-souls-research-followup-01'
    assert all(not p.exists() for p in [target,receipt,delta,preserved])
    now=datetime.now(timezone.utc).isoformat();state=read(previous)
    check=A/'COSMOLOGY_SOULS_RESEARCH_01_RETURN_SOURCE_CHECK_01.json';assert read(check)['failureCount']==0
    dom=A/'COSMOLOGY_SOULS_RESEARCH_01_FOLLOWUP_SUBMISSION_DOM.txt';assert 'ChatGPT is responding' in dom.read_text(encoding='utf-8')
    receipt.write_bytes(encoded({'reviewId':'COSMOLOGY-SOULS-RESEARCH-01-FOLLOWUP','recordedAtUtc':now,'status':'seven gameplay revisions submitted once; GPT responding at observation','conversationUrl':state['activeGptReview']['conversationUrl'],'tabId':state['activeGptReview']['tabId'],'firstReturn':info(A/'COSMOLOGY_SOULS_RESEARCH_01_Addendum_and_Evidence.zip'),'sourceCheck':info(check),'sourceChecksPassed':381,'request':info(A/'COSMOLOGY_SOULS_RESEARCH_01_FOLLOWUP_REQUEST.txt'),'submissionDom':info(dom),'visibleProof':info(A/'COSMOLOGY_SOULS_RESEARCH_01_FOLLOWUP_SUBMISSION.png'),'issueIds':[f'SR-F{i:02d}' for i in range(1,8)],'newCandidateAdopted':False,'sourceInformationDeleted':0}))
    scope='Planes successor is verified and saved. The first souls/Research candidate passed381source/hash/citation/count checks and is preserved. Seven concrete gameplay revisions SR-F01–07 were sent to GPT in Part3: personal qualification/borrowed proficiency and pausable work; optional copying/translation; knowledge-based taint milestones; actual taint consequences and recovery; Hunt warning/trigger ordering; exceptional-return identity/state; synthesis DC/authentication/retry. Revised output is pending; no new rules adopted. Ordinary spells419reviewed429pending; latest verified GitHub18c6e3a, later work local.'
    start=G/'START_HERE.md';current=R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md';nav=R/'tools/build_review_map.py';old={};pres=[]
    for p in [start,current,nav,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        dest=preserved/p.relative_to(G);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(p.read_bytes());assert dest.read_bytes()==p.read_bytes()
        pres.append({**info(p),'preservedCopy':dest.relative_to(G).as_posix()})
        if p in [start,current,nav]:old[p]=p.read_text(encoding='utf-8')
    (preserved/'PRESERVATION_MANIFEST.json').write_bytes(encoded(pres))
    oldline=next(x for x in old[start].splitlines() if x.startswith('**Current joint review:**'))
    newline='**Current joint review:** The [planes Director chapter](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/PLANES_REVIEWED_01.md) is verified and saved. The first souls/Equation Research candidate passed its source checks; [seven gameplay revisions are now with GPT in Part 3](docs/audit/2026-10-08/full-game/COSMOLOGY_SOULS_RESEARCH_01_FOLLOWUP_RECEIPT.json), covering borrowed skills, research progression, taint consequences, Hunt triggers and exceptional returns. Use the [cosmology guide](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md), [review map](REVIEW_MAP.html) and [current checkpoint](docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_AFTER_SOULS_RESEARCH_FOLLOWUP_01.json). Ordinary spells remain **419 reviewed / 429 pending**. New research/Hunt mechanics remain under revision. Latest verified GitHub backup is 18c6e3a; later work is local. **You are monitoring usage; the earlier 50% stop is withdrawn.**'
    start.write_text(old[start].replace(oldline,newline,1),encoding='utf-8',newline='\n')
    paragraph='\nThe [first souls/Research return](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_SOULS_RESEARCH_01_Addendum_and_Evidence.zip) is preserved and passed 381 exact source/file/citation/count checks. Its proposed procedures are being revised through [seven concrete gameplay questions](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_SOULS_RESEARCH_01_FOLLOWUP_RECEIPT.json). The follow-up covers earned qualifications with borrowed proficiency, legal work intervals, optional copying/translation, knowledge-based taint, usable exposure/consequences/recovery, warning-before-Hunt commitment, one-time intervention state and precise synthesis DC/retries. This latest workflow status supersedes the initial-submission status above; no new operating design has been adopted yet.\n'
    current.write_text(old[current]+paragraph,encoding='utf-8',newline='\n')
    text=old[nav];chain=' + read(A / "PLANES_SOULS_SUBMISSION_01_NAVIGATION_DELTA.json")["changes"]\n';assert text.count(chain)==1
    text=text.replace(chain,chain.rstrip('\n')+' + read(A / "SOULS_RESEARCH_FOLLOWUP_01_NAVIGATION_DELTA.json")["changes"]\n',1)
    nodes=[v for node in ast.walk(ast.parse(text)) if isinstance(node,ast.Dict) for k,v in zip(node.keys,node.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(nodes)==1
    text=text.replace(ast.get_source_segment(text,nodes[0]),repr(scope),1).replace('    pending = [\n','    pending = [\n        '+repr(('Souls/Research — first return verified; seven gameplay revisions submitted',receipt.name))+',\n',1)
    compile(text,str(nav),'exec');nav.write_text(text,encoding='utf-8',newline='\n')
    changes=[{'before':next(x for x in pres if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [current,start,nav]]
    changes[0]['operations']=[{'old':old[current],'replacement':old[current]+paragraph}];changes[1]['operations']=[{'old':oldline,'replacement':newline}]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'fullDomainClosureChanged':False,'newRulesAdopted':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout[-1000:]);print(run.stderr[-4000:]);raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,coverageDelta=info(delta),ownerStartPage=info(start),navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]})
    state['activeGptReview'].update(reviewId='COSMOLOGY-SOULS-RESEARCH-01-FOLLOWUP',status='first return source-verified; seven gameplay revisions running at submission observation',submission=info(receipt),firstCandidateSourceCheck=info(check),verdictReceived=False)
    state['cosmologySoulsResearchSubmission']['firstReturn']=info(A/'COSMOLOGY_SOULS_RESEARCH_01_Addendum_and_Evidence.zip');state['cosmologySoulsResearchSubmission']['followup']=info(receipt)
    state['ownerCosmologyCorrections']['readingOrder']=info(current)
    state['safeNextActions'][0]='Observe the same live Part3 follow-up in Chrome tab125746244. Expect COSMOLOGY_SOULS_RESEARCH_01_Revised_Addendum_and_Evidence.zip; verify files/citations and SR-F01–07 substantive revisions. Do not resend, stop the response or ask continuation permission.'
    state['safeNextActions'].insert(1,'First return passed381source checks but is not adopted. Review revised qualification/borrowed-work, epistemic states, knowledge-based taint, real consequence/recovery rules, warning/trigger ordering, unique intervention and research DC/retry examples. Once coherent, adopt only agreed NEW provisional playtest procedures, preserving original canon and separate runtime/human evidence gates.')
    state.setdefault('preservationManifests',[]).append(info(preserved/'PRESERVATION_MANIFEST.json'));target.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(target),'receipt':info(receipt),'navigationLinks':navigation['existingDistinctLinks'],'missingLinks':0,'newRulesAdopted':False}))

if __name__=='__main__':main()
