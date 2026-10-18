"""Refresh owner navigation after actual persistent return and cross-packet body repairs."""
from copy import deepcopy
from datetime import datetime,timezone
import ast,json,subprocess,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded


def read(p):return json.loads(p.read_bytes())


def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_CONFERENCE_QUEUE_BACKUP_09.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_GEOMETRY_LIFE_CONFERENCE_10.json'
    delta=A/'GEOMETRY_LIFE_CONFERENCE_10_NAVIGATION_DELTA.json';report=A/'GEOMETRY_LIFE_CONFERENCE_10_NAVIGATION_CHECK.json'
    keep=A/'navigation-before-geometry-life-conference-10'
    assert all(not p.exists() for p in [checkpoint,delta,report,keep])
    start=G/'START_HERE.md';guide=R/'docs/DEVELOPMENT_DIRECTION.md';builder=R/'tools/build_review_map.py'
    ledger=R/'data/playtest/game_development_coverage.json';mapfile=G/'REVIEW_MAP.html';buildfile=A/'REVIEW_MAP_BUILD.json'
    raw={p:p.read_bytes() for p in [start,guide,builder,ledger,mapfile,buildfile]};now=datetime.now(timezone.utc).isoformat();saved=[]
    for p,b in raw.items():
        copy=keep/p.relative_to(G);copy.parent.mkdir(parents=True,exist_ok=True);copy.write_bytes(b);saved.append({'source':info(p),'preservedCopy':info(copy)})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    evidence_names=['PERSISTENT_DAMAGE_20_CONFERENCE_06_RECEIPT.json','PERSISTENT_DAMAGE_20_EXACT_REBOUND_07_PREPARATION.json','DAMAGE_CONTROL_25_EXACT_REBOUND_10_PREPARATION.json','CONTROL_15_CONFERENCE_12_PREPARATION.json','MEMORY_2_CONFERENCE_02_PREPARATION.json','CREATION_CONFERENCE_02_PREPARATION.json','MATERIAL_TERRAIN_8_CONFERENCE_02_PREPARATION.json','COMPANION_LIFE_10_CONFERENCE_01_PREPARATION.json','COMPANION_LIFE_10_CONFERENCE_01_ACTUAL_SUBMISSION.json','REMAINING_WORK_QUEUE_05_CHECK.json']
    evidence=[A/n for n in evidence_names];assert all(p.exists() for p in evidence)
    text=raw[start].decode('utf8').replace(previous.name,checkpoint.name)
    text=text.replace('the subsequently prepared memory and Creation conferences and this navigation update are local.','subsequent returned reviews, corrected draft packets and this navigation update remain local.')
    replacements={
      '**Current GPT conference:**':'**Current GPT conference:** The [companion/life10 conference](docs/audit/2026-10-08/full-game/COMPANION_LIFE_10_CONFERENCE_01_PREPARATION.json) is actually active in Review Continuation Part4, with [native submission evidence](docs/audit/2026-10-08/full-game/COMPANION_LIFE_10_CONFERENCE_01_ACTUAL_SUBMISSION.json). It supplies ten complete original procedures, twenty preserved scenarios and sixteen design questions before new systemic authorship. GPT received the verified 9cfd0ab backup, returned persistent20 acknowledgment and occupied-space audit warning. Preserve the actual final response before the next exchange; do not interrupt or duplicate it.',
      '**Accelerated digital spell review:**':'**Accelerated digital spell review:** Counts remain **480 reviewed / 368 pending**, with 108 accepted interfaces. The [damage/control25 exact rebound10](docs/audit/2026-10-08/full-game/DAMAGE_CONTROL_25_EXACT_REBOUND_10_PREPARATION.json) is prepared unsent: Current09 preserves all23 actual conference corrections,25 full procedures,26 placements,36 original scenarios and70 current cases. Eight current body/placement cases were repaired, including whole-body Lance stopping and concrete Wizard HP; three earlier supplemental repairs remain. Full before/after evidence is supplied for actual GPT concurrence. Superseded exact09 was never submitted.',
      '**Persistent spell development:**':'**Persistent spell development:** The [actual persistent20 final](docs/audit/2026-10-08/full-game/PERSISTENT_DAMAGE_20_CONFERENCE_06_RECEIPT.json) is preserved and its nine operations replayed/reversed exactly. [Exact rebound07](docs/audit/2026-10-08/full-game/PERSISTENT_DAMAGE_20_EXACT_REBOUND_07_PREPARATION.json) is prepared unsent with20 procedures,40 original scenarios and57 current cases; separate local Ranger Beast, mortar-placement and HP-derivation changes require concurrence. [Control15 conference12](docs/audit/2026-10-08/full-game/CONTROL_15_CONFERENCE_12_PREPARATION.json), [memory2 conference02](docs/audit/2026-10-08/full-game/MEMORY_2_CONFERENCE_02_PREPARATION.json), [Creation conference02](docs/audit/2026-10-08/full-game/CREATION_CONFERENCE_02_PREPARATION.json) and [material/terrain8 conference02](docs/audit/2026-10-08/full-game/MATERIAL_TERRAIN_8_CONFERENCE_02_PREPARATION.json) preserve all original procedures/questions/scenarios and correct occupied-space examples. Illusion14 conference11 remains prepared; its no-match geometry search is not a complete semantic clearance audit. The [current queue](DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_05.json) maps95 pending identities to actual/prepared packets,40 other earlier proposals and233 source/receipt work items. No packet is adopted.',
      '**Owner-directed sequence:**':'**Owner-directed sequence:** The last verified preservation push is [9cfd0ab](docs/audit/2026-10-18/github-snapshot-conferences/PUSH_RECEIPT.json), with22,916 expected blobs checked and all prior tracked files retained. Returned persistent20, subsequent corrected/systemic packets and checkpoint10 remain local. Careful cosmology work began after its required push; no new cosmology is being inferred from these spells. Continue actual GPT conferences and development until review completion or20% allowance remains. Latest observed usage is29% used /71% remaining; a progress backup does not close whole-game review.'}
    for marker,replacement in replacements.items():
        i=text.index(marker);j=text.index('\n\n',i);text=text[:i]+replacement+text[j:]
    start.write_text(text,encoding='utf8',newline='\n')
    text=raw[guide].decode('utf8').replace(previous.name,checkpoint.name);i=text.index('## Current continuation');j=text.index('The [current checkpoint]')
    text=text[:i]+'''## Current continuation

- Counts remain480 reviewed /368 pending,848 identities,204 standalone procedures and108 accepted interfaces. AC6/DE4 scope remains closed.
- Companion/life10 conference01 is actually active in Review Continuation Part4, user turn e064c030-16dc-47a0-85d0-e361fdef35b1. Ten original procedures,20 original scenarios and16 genuine questions are submitted before new systemic authorship; zero new current vectors are claimed. Do not interrupt or duplicate the review.
- Actual persistent20 Conference06 final is verified and preserved. All nine operations replayed and reversed exactly into Current07. Its complete exact rebound07 is prepared unsent with57 cases and separate local Beast lifecycle, mortar placement and Warrior HP derivation corrections awaiting concurrence.
- Damage/control25 Current09 and exact rebound10 are prepared unsent. All25 procedures and70 case IDs survive; eight whole-body/HP fixture repairs and three earlier supplemental repairs require concurrence. Superseded exact09 was never sent.
- Control15 conference12 corrects body spaces, five illegal Lesser Antimagic ranges, crowding, mental-prison boundaries and contact distances. All15 procedures,30 original scenarios and13 questions remain unchanged. Illusion14 conference11 remains prepared, with no complete new geometry clearance claim.
- Memory2/Creation/material-terrain8 conference02 packets repair conditional body geometry while preserving all original procedures, scenarios and unresolved choices. No new systemic memory, material or companion rule is inferred. Missing creature CR/contest profiles and conditional physical permissions remain explicit.
- Queue05 has95 pending identities in prepared/actual conference packets,40 other earlier complete proposals and233 source/receipt work items, totaling368. Spell counts are not a whole-game completion percentage.
- GitHub main was last verified at9cfd0ab4029176a5e1075344a908f50a3fb8fdde. Subsequent returned reviews, corrected packets, new source conferences and this checkpoint are local and preserved. No source deletion or history rewrite occurred.
- At the next actual GPT exchange, report the full cross-packet body/range findings, persistent nine-operation replay/local corrections and corrected exact25 packet. Send the actual files, not summaries in place of source evidence. Prefer the prepared exact25 review next, then persistent20 exact review and the remaining source conferences.
- All75 domain states remain unchanged. Runtime, human gameplay, numerical balance, cosmology/canon, whole-game flow and release remain separate. Continue until review completion or any reported allowance reaches20% remaining; latest weekly observation29% used /71% remaining, secondary window unavailable.

'''+text[j:];guide.write_text(text,encoding='utf8',newline='\n')
    coverage=read(ledger);oldcoverage=deepcopy(coverage)
    for row in coverage['aspects']:
        if row['id'] in ['DD-11','DD-12']:
            row['validationEvidence'].extend(p.relative_to(G).as_posix() for p in evidence)
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'geometry-life-conference-10','recordedAtUtc':now,'reviewed':480,'pending':368,'newSpellIdentitiesAccepted':0,'actualCompanionLifeConferenceSubmitted':True,'persistentConferenceReturnedAndNineOperationsReplayed':True,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'fullDomainClosureChanged':False})
    for a,b in zip(oldcoverage['aspects'],coverage['aspects']):
        assert all(a[k]==b[k] for k in ['status','closure','humanEvidence','completionClass'])
        if a['id'] not in ['DD-11','DD-12']:assert a==b
    ledger.write_bytes(encoded(coverage))
    code=raw[builder].decode('utf8');tail=' + read(A / "CONFERENCE_QUEUE_BACKUP_09_NAVIGATION_DELTA.json")["changes"]\n';assert code.count(tail)==1
    code=code.replace(tail,tail.rstrip('\n')+' + read(A / "GEOMETRY_LIFE_CONFERENCE_10_NAVIGATION_DELTA.json")["changes"]\n')
    for a,b in [('Damage25 exact rebound09 — prepared unsent','Damage25 exact rebound09 — superseded unsent history'),('Memory2 systemic conference01 — prepared unsent','Memory2 conference01 — superseded unsent history'),('Creation economic conference01 — prepared unsent','Creation conference01 — superseded unsent history')]:code=code.replace(a,b)
    additions=[('Companion/life10 — actual GPT conference active',evidence_names[7]),('Persistent20 — actual conference returned',evidence_names[0]),('Persistent20 exact rebound07 — prepared unsent',evidence_names[1]),('Damage25 exact rebound10 — prepared unsent',evidence_names[2]),('Control15 conference12 — prepared unsent',evidence_names[3]),('Memory2 conference02 — prepared unsent',evidence_names[4]),('Creation conference02 — prepared unsent',evidence_names[5]),('Material/terrain8 conference02 — prepared unsent',evidence_names[6]),('Current remaining queue05 —95 packet identities',evidence_names[9])]
    code=code.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(t)+',\n' for t in additions),1)
    scope='Video game only:480 reviewed/368 pending;108 accepted interfaces. Companion/life10 actual GPT review active. Persistent20 returned; exact07 prepared. Damage25 exact10,control15 conference12,illusion14 conference11,memory2/Creation/terrain8 conference02 prepared unsent. Latest verified GitHub9cfd0ab; subsequent work local. All75 domain gates unchanged;71percent remaining observed; stop at20percent.'
    nodes=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(nodes)==1
    code=code.replace(ast.get_source_segment(code,nodes[0]),repr(scope),1);compile(code,str(builder),'exec');builder.write_text(code,encoding='utf8',newline='\n')
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':[{'before':next({**s['source'],'preservedCopy':s['preservedCopy']['path']} for s in saved if s['source']['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,guide,ledger,builder]],'all75DomainGatesUnchanged':True,'newRuleAdoptionsByNavigation':0,'sourceInformationDeleted':0}))
    current=deepcopy(read(previous));current.update(id='ACTIVE-AUTHORING-GEOMETRY-LIFE-CONFERENCE-10',recordedAtUtc=now,status=scope,previousCheckpoint=info(previous),lastUsageObservation={'weeklyUsedPercent':29,'weeklyRemainingPercent':71,'shortWindowReported':False},coverageLedger=info(ledger),navigationDelta=info(delta),preservedNavigation=info(keep/'PRESERVATION_MANIFEST.json'),newRuleAdoptions=0)
    current['priorChangedStatusEntries10']={k:deepcopy(current[k]) for k in ['activeGptReview','next25','damageControl25Current','persistent20','control15','memory2','creation']}
    queuep=R/'data/director/spell_review/remaining_work_queue_05.json';queue=read(queuep);groups={x['group']:x for x in queue['groups']}
    current['currentWorkQueue']=info(queuep)
    current['activeGptReview']={'threadId':'6ad1acef-455c-83ea-bc33-56e4adaec9c8','threadTitle':'Review Continuation Part 4','userTurnId':'e064c030-16dc-47a0-85d0-e361fdef35b1','archive':groups['companion-life10']['archive'],'nativeEvidence':info(A/'COMPANION_LIFE_10_CONFERENCE_01_ACTUAL_SUBMISSION.json'),'actualMessage':info(A/'COMPANION_LIFE_10_CONFERENCE_01_SUBMITTED_REQUEST.txt'),'reviewStatus':'Actual companion/life10 source-design conference active; visible Stop confirms ongoing response. No final verdict or approval inferred.'}
    current['next25']={**deepcopy(groups['damage-control25']),'draft':groups['damage-control25']['candidate'],'exactSubmitted':False,'currentCases':70,'originalScenarios':36,'localSupplementCorrections':3,'localOccupiedSpaceCases':8,'actualFinalReceipt':info(A/'DAMAGE_CONTROL_25_CONFERENCE_07_RECEIPT.json')}
    current['damageControl25Current'].update(draft=groups['damage-control25']['candidate'],exactReboundPreparation=groups['damage-control25']['preparation'],exactSubmitted=False,check=info(A/'DAMAGE_CONTROL_25_GEOMETRY_CHECK_09.json'),remaining='Send prepared exact rebound10 after actual active GPT conference returns. Verify actual exact-file verdict before applying any membership/copy changes.')
    current['persistent20'].update(providedToGptForAwarenessOnly=False,semanticReviewRequested=True,semanticReviewReturned=True,actualReturnedReceipt=info(evidence[0]),currentDraft=groups['persistent-damage20']['candidate'],latestCheck=info(A/'PERSISTENT_DAMAGE_20_CURRENT_07_REPLAY_CHECK.json'),supplementalVectors=9,exactReboundPreparation=groups['persistent-damage20']['preparation'],exactReboundArchive=groups['persistent-damage20']['archive'],exactReboundSubmitted=False,adopted=False)
    for key,group in [('control15','control15'),('memory2','memory2'),('creation','creation1'),('materialTerrain8','material-terrain8'),('companionLife10','companion-life10')]:current[key]=deepcopy(groups[group])
    current['latestVerifiedGitHubBackup']['laterLocalWork']=['returned persistent20 and exact07','damage25 current09/exact10','control15 current12/conference12','memory2/Creation/material-terrain8 conference02','companion/life10 actual conference01','queue05 and checkpoint10']
    current['verifiedGitHubBackup']=deepcopy(current['latestVerifiedGitHubBackup'])
    current['nextGptProgressUpdate']='After preserving actual companion/life10 final, report actual persistent20 nine-operation replay plus separate Beast/mortar/HP evidence repairs; cross-packet5x5/10x10 occupancy and five illegal15ft Antimagic placements fixed; exact25 rebound10 and persistent20 exact07 ready; control12,memory2/Creation/terrain02 prepared. All original source/scenario history retained. Send exact25 full packet next unless actual returned design findings require immediate dependency work.'
    checkpoint.write_bytes(encoded(current))
    run=subprocess.run([sys.executable,'-X','utf8',str(builder)],capture_output=True,text=True,encoding='utf8');assert run.returncode==0,(run.stdout[-1500:],run.stderr[-1500:])
    build=read(buildfile);assert not build['missingLinks'];current['navigation']={'map':info(mapfile),'build':info(buildfile),'existingDistinctLinks':build['existingDistinctLinks'],'missingLinks':[]};checkpoint.write_bytes(encoded(current))
    report.write_bytes(encoded({'checkpoint':info(checkpoint),'delta':info(delta),'all75DomainGatesUnchanged':True,'existingDistinctLinks':build['existingDistinctLinks'],'missingLinks':[],'newRuleAdoptionsByNavigation':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}))
    print(json.dumps(read(report)))


if __name__=='__main__':main()
