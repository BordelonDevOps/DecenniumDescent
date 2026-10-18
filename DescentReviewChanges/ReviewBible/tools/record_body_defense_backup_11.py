"""Preserve navigation history and point the owner to current packets and verified backup."""
from copy import deepcopy
from datetime import datetime,timezone
import ast,json,subprocess,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded


def read(p):return json.loads(p.read_bytes())


def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_GEOMETRY_LIFE_CONFERENCE_10.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_BODY_DEFENSE_BACKUP_11.json'
    delta=A/'BODY_DEFENSE_BACKUP_11_NAVIGATION_DELTA.json';report=A/'BODY_DEFENSE_BACKUP_11_NAVIGATION_CHECK.json';keep=A/'navigation-before-body-defense-backup-11'
    assert all(not p.exists() for p in [checkpoint,delta,report,keep])
    start=G/'START_HERE.md';guide=R/'docs/DEVELOPMENT_DIRECTION.md';builder=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json';mapfile=G/'REVIEW_MAP.html';buildfile=A/'REVIEW_MAP_BUILD.json'
    raw={p:p.read_bytes() for p in [start,guide,builder,ledger,mapfile,buildfile]};now=datetime.now(timezone.utc).isoformat();saved=[]
    for p,b in raw.items():
        copy=keep/p.relative_to(G);copy.parent.mkdir(parents=True,exist_ok=True);copy.write_bytes(b);saved.append({'source':info(p),'preservedCopy':info(copy)})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    receiptp=G/'docs/audit/2026-10-18/github-snapshot-geometry/PUSH_RECEIPT.json';receipt=read(receiptp)
    assert receipt['commit']==receipt['remoteMain']=='dcf2fc47a507795d093745968d37c8934cc98368' and receipt['expectedBlobsVerified']==23403 and receipt['trackedEntriesDeleted']==0
    evidence=[A/'ILLUSION_PERCEPTION_14_CONFERENCE_12_PREPARATION.json',A/'BODY_DEFENSE_8_CONFERENCE_01_PREPARATION.json',A/'REMAINING_WORK_QUEUE_06_CHECK.json',receiptp]
    text=raw[start].decode('utf8').replace(previous.name,checkpoint.name)
    before='Latest verified GitHub backup is **9cfd0ab**; subsequent returned reviews, corrected draft packets and this navigation update remain local.'
    after='Latest verified GitHub backup is **dcf2fc4**, including checkpoint10 and its review packets. The subsequent illusion12 repair, body/defense8 conference, queue06 and checkpoint11 remain local.'
    assert text.count(before)==1;text=text.replace(before,after)
    before='Illusion14 conference11 remains prepared; its no-match geometry search is not a complete semantic clearance audit. The [current queue](DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_05.json) maps95 pending identities to actual/prepared packets,40 other earlier proposals and233 source/receipt work items.'
    after='[Illusion14 conference12](docs/audit/2026-10-08/full-game/ILLUSION_PERCEPTION_14_CONFERENCE_12_PREPARATION.json) is prepared with a corrected Shadow Step grapple: distinct actual Medium bodies and40ft final occupied-box separation. All14 procedures,28 original cases,3 supplements and16 questions remain. The [body/defense8 preauthorship conference](docs/audit/2026-10-08/full-game/BODY_DEFENSE_8_CONFERENCE_01_PREPARATION.json) preserves8 full proposals and16 original scenarios with14 design questions; zero new current encounters are claimed. The [current queue](DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_06.json) maps103 pending identities to actual/prepared packets,32 other earlier proposals and233 source/receipt work items.'
    assert text.count(before)==1;text=text.replace(before,after)
    i=text.index('**Owner-directed sequence:**');j=text.index('\n\n',i)
    text=text[:i]+'**Owner-directed sequence:** The latest preservation push is [dcf2fc4](docs/audit/2026-10-18/github-snapshot-geometry/PUSH_RECEIPT.json), with23,403 expected blobs verified and every prior tracked file retained. Illusion12,body/defense8,queue06 and checkpoint11 are subsequent local work. GPT’s actual companion/life10 review remains active; its next handoff will include this verified backup and all subsequent changes, followed by the complete exact25 rebound10. No new cosmology is inferred from spell mechanics. Continue until review completion or20% allowance remains; latest observation29% used /71% remaining. A backup does not close whole-game review.'+text[j:]
    start.write_text(text,encoding='utf8',newline='\n')
    text=raw[guide].decode('utf8').replace(previous.name,checkpoint.name);i=text.index('## Current continuation');j=text.index('The [current checkpoint]')
    text=text[:i]+'''## Current continuation

- Ordinary spell counts remain480 reviewed/368 pending across848 identities;204 standalone procedures and108 accepted interfaces. AC6/DE4 remain within their actual accepted scopes.
- Actual companion/life10 conference01 is still active in Review Continuation Part4, user turn e064c030-16dc-47a0-85d0-e361fdef35b1. Ten full original procedures,20 scenarios and16 questions were submitted before new systemic authorship, with zero new current encounter vectors. Wait for its actual final response without interrupting or duplicating it.
- Returned persistent20 corrections are preserved and all nine operations replayed/reversed. Exact rebound07 is prepared with57 current cases and separate local Beast lifecycle/mortar placement/Warrior HP-source repairs. Exact damage/control25 rebound10 retains all25 procedures and70 cases, with eight body/HP repairs and three earlier local supplemental repairs. Neither exact packet has been submitted or adopted.
- Control15 conference12, memory2/Creation/material-terrain8 conference02 remain prepared with full preserved sources, questions and scenario history. All actual body/range repairs are explicitly separated from procedure changes.
- Illusion14 Current12/conference12 preserves all14 procedures,28 original/current cases,3 supplements and16 questions. One Shadow Step grapple case now has distinct5x5 bodies, legal support and40ft final whole-body separation. The prior package supplies exact frozen source bytes, including its earlier navigation copy; no historical binding was silently pointed to new bytes.
- Body/defense8 preauthorship conference01 is prepared with8 complete original proposals,16 original scenarios,39 full sources,184 preflight checks and14 genuine questions. Permanent Petrified metabolism, Earthstep retreat, Wind Walk profile/lifecycle and Metaburst temporary-CON/capacity choices remain proposals. Fixed continuous meld ceilings and existing Core Corruption restrictions are inherited. Zero new current encounters or systemic adoptions are claimed.
- Queue06 maps103 pending identities to nine prepared/active packets,32 other earlier complete proposals and233 original source/receipt items, totaling368 without overlap or review promotion. This is not a whole-game percentage.
- GitHub main is verified atdcf2fc47a507795d093745968d37c8934cc98368, including all work through checkpoint10.23,403 expected blobs and every prior tracked entry were verified; no source files were deleted or history rewritten. Illusion12,body/defense8,queue06 and this checkpoint are subsequent local work.
- At the next actual GPT exchange, preserve its final first, report the new verified backup and complete cross-packet corrections, then send exact damage/control25 rebound10. Persistent20 exact07 and the remaining source conferences follow; substantive returned issues can change that order.
- All75 domain statuses and closure/human/completion gates remain unchanged. Runtime, human gameplay, balance, cosmology/canon, whole-game flow and release are distinct. Continue until review completion or a reported allowance reaches20% remaining; latest weekly observation29% used/71% remaining, secondary unavailable.

'''+text[j:];guide.write_text(text,encoding='utf8',newline='\n')
    coverage=read(ledger);oldcoverage=deepcopy(coverage)
    for row in coverage['aspects']:
        if row['id'] in ['DD-11','DD-12']:
            row['validationEvidence'].extend(p.relative_to(G).as_posix() for p in evidence)
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'body-defense-backup-11','recordedAtUtc':now,'reviewed':480,'pending':368,'newSpellIdentitiesAccepted':0,'preparedIdentityCount':103,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'fullDomainClosureChanged':False})
    for a,b in zip(oldcoverage['aspects'],coverage['aspects']):
        assert all(a[k]==b[k] for k in ['status','closure','humanEvidence','completionClass'])
        if a['id'] not in ['DD-11','DD-12']:assert a==b
    ledger.write_bytes(encoded(coverage))
    code=raw[builder].decode('utf8');tail=' + read(A / "GEOMETRY_LIFE_CONFERENCE_10_NAVIGATION_DELTA.json")["changes"]\n';assert code.count(tail)==1
    code=code.replace(tail,tail.rstrip('\n')+' + read(A / "BODY_DEFENSE_BACKUP_11_NAVIGATION_DELTA.json")["changes"]\n')
    additions=[('Illusion14 conference12 — prepared unsent',evidence[0].name),('Body/defense8 — preauthorship conference prepared unsent',evidence[1].name),('Current remaining queue06 —103 packet identities',evidence[2].name)]
    code=code.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(t)+',\n' for t in additions),1)
    scope='Video game only:480 reviewed/368 pending;108 accepted interfaces. Actual companion/life10 conference active. Damage25 exact10 and persistent20 exact07 prepared. Queue06 has103 pending identities in9 packets, including new body/defense8 and corrected illusion12. Verified GitHub dcf2fc4 through checkpoint10; subsequent work local. All75 domain gates unchanged;71percent remaining observed; stop at20percent.'
    nodes=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(nodes)==1
    code=code.replace(ast.get_source_segment(code,nodes[0]),repr(scope),1);compile(code,str(builder),'exec');builder.write_text(code,encoding='utf8',newline='\n')
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':[{'before':next({**s['source'],'preservedCopy':s['preservedCopy']['path']} for s in saved if s['source']['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,guide,ledger,builder]],'all75DomainGatesUnchanged':True,'newRuleAdoptionsByNavigation':0,'sourceInformationDeleted':0}))
    current=deepcopy(read(previous));current.update(id='ACTIVE-AUTHORING-BODY-DEFENSE-BACKUP-11',recordedAtUtc=now,status=scope,previousCheckpoint=info(previous),coverageLedger=info(ledger),navigationDelta=info(delta),preservedNavigation=info(keep/'PRESERVATION_MANIFEST.json'))
    current['priorChangedStatusEntries11']={k:deepcopy(current[k]) for k in ['illusion14','latestVerifiedGitHubBackup','currentWorkQueue']}
    queuep=R/'data/director/spell_review/remaining_work_queue_06.json';groups={x['group']:x for x in read(queuep)['groups']};current['currentWorkQueue']=info(queuep)
    current['illusion14'].update(draft=groups['illusion-perception14']['candidate'],preparation=groups['illusion-perception14']['preparation'],archive=groups['illusion-perception14']['archive'],latestFixtureCheck=info(A/'ILLUSION_PERCEPTION_14_GRAPPLE_CHECK_12.json'),submitted=False,adopted=False)
    current['bodyDefense8']=deepcopy(groups['body-defense8']);current['bodyDefense8'].update(originalScenarios=16,questions=14,newCurrentVectors=0,actualGptSubmitted=False)
    current['latestVerifiedGitHubBackup']={'receipt':info(receiptp),'commit':receipt['commit'],'remoteMainVerified':receipt['remoteMain'],'scope':receipt['scope'],'expectedBlobsVerified':23403,'laterLocalWork':['illusion14 Current12/conference12','body/defense8 conference01','queue06 and checkpoint11']};current['verifiedGitHubBackup']=deepcopy(current['latestVerifiedGitHubBackup'])
    current['nextGptProgressUpdate']='Preserve actual companion/life10 final before the next exchange. Report verified dcf2fc4 backup and all persistent/DC/control/body geometry repairs; illusion12 repairs distinct grapple bodies; body/defense8 conference01 newly prepared with14 forks, no selected new rule. Send full exact damage/control25 rebound10 next. Source history,480/368 and all75domain gates unchanged.'
    checkpoint.write_bytes(encoded(current))
    run=subprocess.run([sys.executable,'-X','utf8',str(builder)],capture_output=True,text=True,encoding='utf8');assert run.returncode==0,(run.stdout[-1500:],run.stderr[-1500:])
    build=read(buildfile);assert not build['missingLinks'];current['navigation']={'map':info(mapfile),'build':info(buildfile),'existingDistinctLinks':build['existingDistinctLinks'],'missingLinks':[]};checkpoint.write_bytes(encoded(current))
    report.write_bytes(encoded({'checkpoint':info(checkpoint),'delta':info(delta),'all75DomainGatesUnchanged':True,'existingDistinctLinks':build['existingDistinctLinks'],'missingLinks':[],'newRuleAdoptionsByNavigation':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}));print(json.dumps(read(report)))


if __name__=='__main__':main()
