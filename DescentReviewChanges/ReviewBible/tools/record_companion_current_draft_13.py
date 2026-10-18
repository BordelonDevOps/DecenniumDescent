"""Route current CL10 authorship without adopting spells or closing domain gates."""
from copy import deepcopy
from collections import Counter
from datetime import datetime,timezone
import ast,json,subprocess,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded

def main():
    read=lambda p:json.loads(p.read_bytes())
    oldq=R/'data/director/spell_review/remaining_work_queue_07.json';newq=R/'data/director/spell_review/remaining_work_queue_08.json';qcheck=A/'REMAINING_WORK_QUEUE_08_CHECK.json'
    oldcp=A/'ACTIVE_AUTHORING_CHECKPOINT_COMPANION_RETURN_HANDOFF_12.json';cp=A/'ACTIVE_AUTHORING_CHECKPOINT_COMPANION_CURRENT_DRAFT_13.json'
    delta=A/'COMPANION_CURRENT_DRAFT_13_NAVIGATION_DELTA.json';check=A/'COMPANION_CURRENT_DRAFT_13_NAVIGATION_CHECK.json';keep=A/'navigation-before-companion-current-draft-13'
    assert all(not p.exists() for p in [newq,qcheck,cp,delta,check,keep]);now=datetime.now(timezone.utc).isoformat()
    candidate=R/'data/director/spell_proposals/companion_life_10_current_04.json';preparation=A/'COMPANION_LIFE_10_CURRENT_04_PREPARATION.json';archive=A/'DD_Companion_Life_10_Current_04_Draft.zip'
    q=read(oldq);priorq=deepcopy(q);g=next(x for x in q['groups'] if x['group']=='companion-life10');oldgroup=deepcopy(g)
    g.update(phase='current-case-draft-prepared-unsent-with-explicit-questions',candidate=info(candidate),preparation=info(preparation),archive=info(archive),priorConferenceGroupUnchanged=oldgroup,
       latestObservedStatus='Actual Conference01 applied; Current04 has27 main cases,2 whole-case CR2 holds and5 explicit questions. Three complete local fixture repairs are preserved. Still UNSENT and unaccepted.',
       currentCaseCount=27,wholeCaseCRHolds=2,clarificationQuestions=5,currentDraftSubmitted=False)
    ids=set(g['identities'])
    for row in q['rows']:
        if row['id'] in ids:row.update(currentPhase=g['phase'],nextAction='Confer with actual GPT on Current04 cases and five precise questions; preserve exactCR2/profile holds. No final acceptance or new membership yet.')
    q['id']='REMAINING-WORK-QUEUE-08';q['recordedAtUtc']=now;q['previousQueue']=info(oldq);q['pendingDistribution']=dict(Counter(r['currentPhase'] for r in q['rows']))
    for p in [candidate,preparation,archive,A/'COMPANION_LIFE_10_CURRENT_04_LOCAL_DELTAS.json',A/'COMPANION_LIFE_10_CURRENT_04_PREFLIGHT.json']:
        q['sourceBindings'].append(info(p))
    assert len(q['rows'])==368 and [r['id'] for r in q['rows']]==[r['id'] for r in priorq['rows']]
    assert q['ordinarySpellCounts']==priorq['ordinarySpellCounts'] and sum(x['identityCount'] for x in q['groups'])==126
    assert len(set(i for x in q['groups'] for i in x['identities']))==126
    for b in q['sourceBindings']:assert info(G/b['path'])==b,b['path']
    newq.write_bytes(encoded(q));qcheck.write_bytes(encoded({'queue':info(newq),'sourceBindings':len(q['sourceBindings']),'exactBindingsVerified':True,'all368PendingIDsAndSourceObjectsPreserved':True,'preparedOrActualIdentityCount':126,'otherCompleteProposals':9,'sourceOrReceiptWork':233,'newRuleAdoptions':0}))
    start=G/'START_HERE.md';guide=R/'docs/DEVELOPMENT_DIRECTION.md';builder=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json';mapfile=G/'REVIEW_MAP.html';buildfile=A/'REVIEW_MAP_BUILD.json'
    raw={p:p.read_bytes() for p in [start,guide,builder,ledger,mapfile,buildfile]};saved=[]
    for p,b in raw.items():
        dst=keep/p.relative_to(G);dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(b);saved.append({'source':info(p),'preservedCopy':info(dst)})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    paragraph='''**Latest companion/life authorship — checkpoint13:** [Current04 preparation](docs/audit/2026-10-08/full-game/COMPANION_LIFE_10_CURRENT_04_PREPARATION.json) preserves all10 returned procedures and20 original scenario texts, with27 current main cases. Two whole-case Command Undeath examples still require a real operative exactCR2 Undead; five specific questions cover Soulburn/GrandReservoir, Wraith handling/mass, Ghast cone geometry and that missing profile. Current03’s335 local integrity/access/arithmetic/geometry checks and Current04’s92 preservation/correction checks are authored-data checks, not runtime or exact acceptance. [Three complete local corrections](docs/audit/2026-10-08/full-game/COMPANION_LIFE_10_CURRENT_04_LOCAL_DELTAS.json) retain actual Ghast armor, fully specify a counterer and bind a genuinely paid command before a readied suppression release. The draft is **UNSENT**, and480 reviewed/368 pending remains unchanged. [Queue08](DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_08.json) keeps126 identities in13 groups,9 other earlier proposals and233 source/receipt work items. GPT is still actively reviewing damage25 exact10; send persistent20 exact07 after its actual final unless substantive corrections change the order. Latest observed allowance35% used/65% remaining; stop at20% remaining or complete review.\n\n'''
    s=raw[start].decode('utf8').replace(oldcp.name,cp.name).replace('remaining_work_queue_07.json','remaining_work_queue_08.json')
    i=s.index('**Current GPT conference:**');s=s[:i]+paragraph+s[i:];start.write_text(s,encoding='utf8',newline='\n')
    s=raw[guide].decode('utf8').replace(oldcp.name,cp.name);i=s.index('## Current continuation');j=s.index('\n',i)+1
    gp=paragraph.replace('(docs/audit/','(../../../docs/audit/').replace('(DescentReviewChanges/ReviewBible/data/','(../data/')
    s=s[:j]+'\n'+gp+s[j:];guide.write_text(s,encoding='utf8',newline='\n')
    coverage=read(ledger);oldcoverage=deepcopy(coverage)
    evidence=[preparation,A/'COMPANION_LIFE_10_CURRENT_04_LOCAL_DELTAS.json',A/'COMPANION_LIFE_10_CURRENT_04_PREFLIGHT.json',qcheck]
    for row in coverage['aspects']:
        if row['id'] in ['DD-11','DD-12']:
            row['validationEvidence'].extend(p.relative_to(G).as_posix() for p in evidence)
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'companion-current-draft-13','recordedAtUtc':now,'mainCases':27,'wholeCaseCRHolds':2,'clarificationQuestions':5,'submitted':False,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'fullDomainClosureChanged':False})
    for a,b in zip(oldcoverage['aspects'],coverage['aspects']):
        assert all(a[k]==b[k] for k in ['status','closure','humanEvidence','completionClass'])
        if a['id'] not in ['DD-11','DD-12']:assert a==b
    ledger.write_bytes(encoded(coverage))
    code=raw[builder].decode('utf8');tail=' + read(A / "COMPANION_RETURN_HANDOFF_12_NAVIGATION_DELTA.json")["changes"]\n';assert code.count(tail)==1
    code=code.replace(tail,tail.rstrip('\n')+' + read(A / "COMPANION_CURRENT_DRAFT_13_NAVIGATION_DELTA.json")["changes"]\n')
    additions=[('Companion/life10 Current04 —27 authored cases,5 questions,UNSENT',preparation.name),('Companion current fixture corrections',evidence[1].name),('Current queue08 —126 identities, no adoption',qcheck.name)]
    code=code.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(t)+',\n' for t in additions),1)
    scope='Video game only.480 reviewed/368 pending. Companion Current04:27 main authored cases,2 exactCR2 holds,5 questions; UNSENT. Damage25 exact10 actual GPT review active; persistent20 exact07 next. Queue08 retains126 identities in13 groups. All75 domain gates unchanged; no runtime/balance/cosmology approval. Verified backupdcf2fc4 throughcheckpoint10; later work local. Latest allowance65percentremaining; stopat20percent.'
    nodes=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(nodes)==1
    code=code.replace(ast.get_source_segment(code,nodes[0]),repr(scope),1);compile(code,str(builder),'exec');builder.write_text(code,encoding='utf8',newline='\n')
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':[{'before':next({**b['source'],'preservedCopy':b['preservedCopy']['path']} for b in saved if b['source']['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,guide,ledger,builder]],'all75DomainGatesUnchanged':True,'newRuleAdoptionsByNavigation':0,'sourceInformationDeleted':0}))
    current=deepcopy(read(oldcp));current.update(id='ACTIVE-AUTHORING-COMPANION-CURRENT-DRAFT-13',recordedAtUtc=now,status=scope,previousCheckpoint=info(oldcp),coverageLedger=info(ledger),navigationDelta=info(delta),preservedNavigation=info(keep/'PRESERVATION_MANIFEST.json'))
    current['priorCompanionGroup12']=deepcopy(current['companionLife10']);current['companionLife10']=g;current['currentWorkQueue']=info(newq)
    current['lastUsageObservation']={'observedAtUtc':'2026-10-18T06:40:10Z','windowMinutes':10080,'usedPercent':35,'remainingPercent':65,'secondary':'unavailable'}
    current['nextGptProgressUpdate']='Actual companion proposal layer led to27 current main cases in Current04, with2 explicitCR2 holds and5 questions. Preserve and inspect actual damage25 final, then submit persistent20 exact07 with this current progress update. Do not claim GPT has seen Current04. No new identities adopted.'
    current['latestVerifiedGitHubBackup']['laterLocalWork'].append('Companion Current03/04 authored cases, local corrections,queue08/checkpoint13');current['verifiedGitHubBackup']=deepcopy(current['latestVerifiedGitHubBackup']);cp.write_bytes(encoded(current))
    run=subprocess.run([sys.executable,'-X','utf8',str(builder)],capture_output=True,text=True,encoding='utf8');assert run.returncode==0,(run.stdout[-1000:],run.stderr[-1000:])
    build=read(buildfile);assert not build['missingLinks'];current['navigation']={'map':info(mapfile),'build':info(buildfile),'existingDistinctLinks':build['existingDistinctLinks'],'missingLinks':[]};cp.write_bytes(encoded(current))
    check.write_bytes(encoded({'checkpoint':info(cp),'queue':info(newq),'delta':info(delta),'existingDistinctLinks':build['existingDistinctLinks'],'missingLinks':[],'all75DomainGatesUnchanged':True,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}))
    print(json.dumps(read(check)))

if __name__=='__main__':main()
