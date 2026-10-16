"""Preserve current browser uncertainty and independent source findings."""
from copy import deepcopy
from datetime import datetime, timezone
import ast, json, subprocess, sys
from apply_di7_ap_as_01 import G,R,A,info,encoded
def read(p):return json.loads(p.read_bytes())

def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_RELIC_NULL_SUBMISSION_01.json'
    target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_RELIC_NULL_RECOVERY_01.json'
    receipt=A/'COSMOLOGY_EPILOGUE_RELIC_NULL_01_BROWSER_RECOVERY_01.json'
    delta=A/'EPILOGUE_RELIC_NULL_RECOVERY_01_NAVIGATION_DELTA.json'
    preserved=A/'navigation-before-epilogue-relic-null-recovery-01'
    assert all(not p.exists() for p in [target,receipt,delta,preserved])
    now=datetime.now(timezone.utc).isoformat();state=read(previous)
    spell=A/'COSMOLOGY_EPILOGUE_RELIC_DIVINATION_INTERFACE_READING_01.json'
    calendar=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_CALENDAR_FOLLOWUP_01.json'
    receipt.write_bytes(encoded({'recordedAtUtc':now,'reviewId':'COSMOLOGY-EPILOGUE-RELIC-NULL-01',
        'browserId':'3','conversationUrl':state['activeGptReview']['conversationUrl'],
        'previousTabMissing':'125746268','observedExistingTab':'125746280','newSameConversationTab':'125746283',
        'observations':['Existing280 listed with same Part3 URL/title; repeated focus/read timeout.',
            'Fresh283 initially showed loading shell; later DOM, screenshot, reload and lightweight visible-text reads timed out.',
            'CUA client reset and rebind did not recover page reads. Browser inventory remained available.',
            'Attempt to close only the duplicate283 timed out; fresh inventory still listed280and283. No tab closure claimed.',
            'Downloads contains only earlier character returns; no relic/Null return downloaded.'],
        'generationState':'UNKNOWN; browser timeouts do not establish stopped or completed generation',
        'requestResent':False,'conversationRecreated':False,'userObservationQuestionPending':True,
        'localFilesAccessible':True,'independentWork':[info(spell),info(calendar)],
        'previousGoalTurnClassification':'progress','currentGoalTurnClassification':'progress',
        'consecutiveGoalTurnsWithThisBrowserFailure':1,'sourceInformationDeleted':0,'newRulesAdopted':False}))
    start=G/'START_HERE.md';guide=R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md'
    nav=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json'
    originals={};pres=[]
    for p in [start,guide,nav,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        raw=p.read_bytes();out=preserved/p.relative_to(G);out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw)
        originals[p]=raw;pres.append({**info(p),'preservedCopy':out.relative_to(G).as_posix()})
    (preserved/'PRESERVATION_MANIFEST.json').write_bytes(encoded(pres))
    old_start=originals[start].decode();line=next(v for v in old_start.splitlines() if v.startswith('**Current joint review:**'))
    new_line=line.replace('Return pending.','Return not yet retrieved; [Chrome page reads are timing out](docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_NULL_01_BROWSER_RECOVERY_01.json), and GPT generation state is unverified.').replace('ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_RELIC_NULL_SUBMISSION_01.json','ACTIVE_AUTHORING_CHECKPOINT_AFTER_EPILOGUE_RELIC_NULL_RECOVERY_01.json')
    assert new_line!=line;start.write_text(old_start.replace(line,new_line,1),encoding='utf-8',newline='\n')
    anchor='First, revised and integrated return archives remain immutable.'
    para='A [browser recovery record](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_NULL_01_BROWSER_RECOVERY_01.json) supersedes the old live-tab pointer: tab 125746268 is missing; the same Part 3 conversation is listed at 125746280 and recovery view 125746283, but both page reads time out. The request has not been resent, and generation is neither confirmed running nor confirmed stopped. Local files remain accessible. Independent [relic/divination interface reading](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_DIVINATION_INTERFACE_READING_01.json) verifies two reviewed spell examples and keeps Divine Truth pending. The [campaign calendar follow-up](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_CAMPAIGN_CALENDAR_FOLLOWUP_01.json) records the original 400-day civil year, ten 40-day months and separate primordial/celestial intervals; it chooses no epoch or Equinox date.\n\n'
    old_guide=originals[guide].decode();assert old_guide.count(anchor)==1
    guide.write_text(old_guide.replace(anchor,para+anchor,1),encoding='utf-8',newline='\n')
    coverage=json.loads(originals[ledger]);before=deepcopy(coverage);row=next(v for v in coverage['aspects'] if v['id']=='DD-50');before_row=deepcopy(row)
    row['reviewEvidence'].extend(p.relative_to(G).as_posix() for p in [spell,calendar,receipt])
    row['currentEvidenceAddenda'].append({'id':'epilogue-relic-null-recovery-01','recordedAtUtc':now,
        'reviewEvidence':[spell.relative_to(G).as_posix(),calendar.relative_to(G).as_posix()],
        'browserState':'observation unavailable; generation unknown','newRulesAdopted':False,'fullDomainClosed':False})
    for k in ['status','closure','humanEvidence','ownerDirectionEvidence','completionClass']:assert row[k]==before_row[k]
    assert [v for v in coverage['aspects'] if v['id']!='DD-50']==[v for v in before['aspects'] if v['id']!='DD-50']
    ledger.write_bytes(encoded(coverage))
    scope='EPI01–07 applied;110authored cases. EPI08–14 submitted with83sources;return not retrieved. Part3 Chrome3 tabs280/283 read timeout; generation UNKNOWN, request not resent. New source readings verify two reviewed divination interfaces, pendingDivineTruth,400day civil calendar distinct from primordial/celestial clocks. Wholegame/runtime/human/balance/publication open.'
    text=originals[nav].decode();tail=' + read(A / "EPILOGUE_RELIC_NULL_SUBMISSION_01_NAVIGATION_DELTA.json")["changes"]\n';assert text.count(tail)==1
    text=text.replace(tail,tail.rstrip('\n')+' + read(A / "EPILOGUE_RELIC_NULL_RECOVERY_01_NAVIGATION_DELTA.json")["changes"]\n',1)
    nodes=[v for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(nodes)==1
    text=text.replace(ast.get_source_segment(text,nodes[0]),repr(scope),1)
    items=[('Part3 browser recovery — generation unverified',receipt.name),('Relic divination — exact current spell boundaries',spell.name),('Later arcs — original400day calendar and unresolved Equinox',calendar.name)]
    text=text.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(x)+',\n' for x in items),1)
    compile(text,str(nav),'exec');nav.write_text(text,encoding='utf-8',newline='\n')
    changes=[{'before':next(x for x in pres if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [guide,start,ledger,nav]]
    changes[0]['operations']=[{'old':anchor,'replacement':para+anchor}];changes[1]['operations']=[{'old':line,'replacement':new_line}];changes[2]['operations']=[{'aspectId':'DD-50','old':before_row,'replacement':row}]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'newRulesAdopted':False,'fullDomainClosureChanged':False,'humanOrOwnerEvidenceChanged':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout[-1200:]);print(run.stderr[-3000:]);raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),goalTurnClassification='progress',previousGoalTurnClassification='progress',status=scope,
        coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),newRuleAdoptions=0,newRuleAdoptionScope='No new rules this turn; earlier EPI01–07 remains adopted.',
        navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]})
    state['activeGptReview'].update(status='Return not retrieved; browser read timeouts; generation state unknown',tabId='125746283',otherObservedTabId='125746280',browserRecovery=info(receipt),generationConfirmedLiveNow=False,generationConfirmedTerminal=False)
    state['cosmologyEpilogueRelicNullReview'].update(status='Submitted;return not retrieved;browser observation unavailable',spellInterfaceReading=info(spell),browserRecovery=info(receipt))
    state['cosmologyEpilogueCampaignCalendarFollowup']=info(calendar);state['ownerCosmologyCorrections']['readingOrder']=info(guide)
    state['safeNextActions']=[
        'Check user response to the pending question about Part3 screen state. Revalidate same Chrome3 conversation; tabs280and283 were last inventoried. CUA reset: resumeBrowser restored, pantheonsTab bound283; filesystem handle heartcellFs must be reimported if needed.',
        'Do not resend the EPI08–14 packet or assume generation stopped based on timeouts. Recover actual final response/download when page responds. No relic/Null return is currently on disk.',
        'Use prepared83-source/eight-file return verifier, then inspect full semantic content before adoption. New independent divination check and400day calendar follow-up are preserved.',
        'Previous turn applied EPI01–07 and submitted next packet. This turn made source-interface progress despite browser failure; this is only first consecutive goal turn with this browser blockage. Do not mark whole goal blocked while meaningful local work is available.',
        'Originals, identities,87/710AE and unanswered frame remain intact.419ordinary spells reviewed;429pending includes428pending-authored entries plus1receipt-onlyBlink entry. No spell promotion or count change occurred. Latest GitHub18c6e3a;later work local.'
    ]
    state.setdefault('preservationManifests',[]).append(info(preserved/'PRESERVATION_MANIFEST.json'));target.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(target),'browserRecovery':info(receipt),'mapLinks':navigation['existingDistinctLinks'],'missingLinks':0}))
if __name__=='__main__':main()
