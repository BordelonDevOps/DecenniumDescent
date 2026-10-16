"""Preserve navigation, publish the bounded review status, and record next conference."""
from datetime import datetime,timezone
from copy import deepcopy
import ast,json,subprocess,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_SOULS_RESEARCH_FOLLOWUP_01.json'
    target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_SOULS_CHRONOLOGY_01.json'
    receipt=A/'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_SUBMISSION_RECEIPT.json'
    delta=A/'SOULS_CHRONOLOGY_01_NAVIGATION_DELTA.json';preserved=A/'navigation-before-souls-chronology-01'
    assert all(not p.exists() for p in [target,receipt,delta,preserved])
    state=read(previous);now=datetime.now(timezone.utc).isoformat()
    application=A/'COSMOLOGY_SOULS_RESEARCH_01_APPLICATION_CHECK.json';app=read(application)
    assert app['sourceCheckFailures']==0 and app['newProvisionalOperatingRulesAdopted']
    dom=A/'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_SUBMISSION_DOM.txt';observed=dom.read_text(encoding='utf-8')
    assert 'button "Stop"' in observed and 'DD_Cosmology_Chronology_Research_Route_01.zip' in observed
    receipt.write_bytes(encoded({'recordedAtUtc':now,'reviewId':'COSMOLOGY-CHRONOLOGY-RESEARCH-ROUTE-01','status':'submitted once; GPT responding at observation',
      'conversationUrl':state['activeGptReview']['conversationUrl'],'tabId':'125746244','archive':info(A/'DD_Cosmology_Chronology_Research_Route_01.zip'),
      'preparation':info(A/'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_PREPARATION.json'),'sourceCount':83,'issues':[f'CE{i:02d}' for i in range(1,9)],
      'submissionDom':info(dom),'visibleProof':info(A/'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_SUBMISSION.png'),'soulsApplication':info(application),
      'chronologyOrRouteAdopted':False,'sourceInformationDeleted':0}))
    start=G/'START_HERE.md';guide=R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md';nav=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json'
    originals={};pres=[]
    for p in [start,guide,nav,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        raw=p.read_bytes();dest=preserved/p.relative_to(G);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw);assert dest.read_bytes()==raw
        originals[p]=raw;pres.append({**info(p),'preservedCopy':dest.relative_to(G).as_posix()})
    (preserved/'PRESERVATION_MANIFEST.json').write_bytes(encoded(pres))
    scope='Souls/Research integrated candidate is locally adopted as NEW provisional Director/playtest rules after392source/file/citation checks and an explicit GPT patch confirmation. All79sources,21issues and64authored examples/situations are preserved. Chronology/research route CE01–08 with83frozen sources is now submitted in Part3. No epoch, identities, epilogue, runtime/human/whole-game approval or pending spell promoted. Ordinary spells419reviewed429pending. GitHub backup18c6e3a; later work local.'
    old_start=originals[start].decode('utf-8');line=next(s for s in old_start.splitlines() if s.startswith('**Current joint review:**'))
    new_line='**Current joint review:** The [souls, research, taint and Hunt chapter](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/SOULS_RESEARCH_REVIEWED_01.md) is now saved as a jointly reviewed **provisional Director/playtest reference**, with 64 authored situations/examples. The [chronology and library-route conference](docs/audit/2026-10-08/full-game/COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_SUBMISSION_RECEIPT.json) is active in Part 3. Start with the [current cosmology guide](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md), [review map](REVIEW_MAP.html) or [current checkpoint](docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_AFTER_SOULS_CHRONOLOGY_01.json). Ordinary spells remain **419 reviewed / 429 pending**. Epoch, remaining lore decisions and full-game validation remain open. Latest verified GitHub backup is 18c6e3a; later work is local. **You are monitoring usage; the earlier 50% stop is withdrawn.**'
    start.write_text(old_start.replace(line,new_line,1),encoding='utf-8',newline='\n')
    guide_text='''# Current cosmology reading order

Start with [the latest Heartcell owner update](HEARTCELL_OWNER_UPDATE_02.md), then [the earlier eleven corrections](OWNER_RECONCILIATION_REVIEWED_01.md). Original Cosmology, Matrix and surviving World manuscripts govern source reading, with explicit owner corrections applied. Original passages, mortal beliefs and new designs retain separate provenance. Primordial Cycles are ages; new Equation drafts do not recover the missing original formula or World I–VI.

Read [creation and origins](CREATION_ORIGINS_REVIEWED_01.md) and [gods and pantheons](GODS_PANTHEONS_REVIEWED_01.md) subject to those owner updates. Mephistopheles is Cania only; the devouring-to-one and no-essence-tether corrections remain current. The Heartcell builder, survivor identity, Maladomini replacement, named Harmony mapping and full Choir chronology remain unresolved.

The [Q6 endgame reference](Q6_LATER_LOCK_REVIEWED_01.md) preserves the registered crystal path and public knowledge ceiling without resolving all identities or encounter mechanics. The [planes reference](PLANES_REVIEWED_01.md) preserves original accounts, saved website and mortal teaching with their different authority. Its 468 checks include 64 frozen source bindings and 18 actual travel-card matches; pending spells and planar-time proposals remain unadopted.

The [souls, research, taint and Hunt chapter](SOULS_RESEARCH_REVIEWED_01.md) is the current **NEW provisional Director/playtest operating reference**. Its [application receipt](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_SOULS_RESEARCH_01_APPLICATION_CHECK.json) records 392 source/file/citation checks, 79 frozen sources, 21 issues and 64 authored situations/examples. GPT explicitly confirmed the small final patch. Research qualifications, real borrowed-skill intervals, evidence, work clocks, separate KT/PT, Hunt warning/trigger timing, complete death-event resolution and rare same-identity intervention now have concrete procedures. They are not recovered cosmological canon or human/runtime validation.

The [chronology and library-route conference](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_SUBMISSION_RECEIPT.json) is now active in Part 3 with 83 frozen sources. It covers CE01–CE08, the calendar/epoch/Choir seams, actual research holdings and a playable route, plus next-work ordering for the existing 17 epilogue groups. No chronology date, new clue, placement or epilogue rule is adopted merely by submission.

For that work, use the [chronology/source comparison](CHRONOLOGY_RESEARCH_SITES_DRAFT_01.md): 16 relative events, 9 site qualifications, 8 issues and 173 exact locations. It preserves both original printed dates and original P324 independent/multi-era adaptation permission. The campaign epoch and library placements remain open. Saved website findings are static-source evidence, not a rendered release test.

The [library inventory](EQUATION_LIBRARY_SOURCE_INVENTORY_01.md) preserves 22 qualified records and 125 evidence locations; these are not 22 usable Descent libraries. Cantor’s Archive is Floor 47. Wax Library is an original Dungeon chamber seed without an assigned floor or recovered Equation holding. Cosmic archives are not silently relocated. Two-library route slots in the new operating model still need actual scene/clue authorship.

The [earlier souls/Hunt draft](SOULS_DEATH_HUNT_CONFERENCE_DRAFT_01.md) and [research-interface draft](EQUATION_RESEARCH_INTERFACE_DRAFT_01.md) remain preserved source/discussion history. Their unanswered operating questions and creation-time workflow status are superseded only where the current reviewed chapter supplies a disposition. Soul Mirror is reviewed-authored as a reflecting ward; Clone/Arcane Clone remain pending. All real language procedures retain their scope.

First, revised and integrated return archives remain immutable. The current chapter and confirmed patch govern this bounded interface; superseded proposal text is nonoperative history. Part 3 is active and no continuation permission is pending. Full cosmology, runtime, human balance, whole-game flow and publication remain open. Latest verified GitHub backup is 18c6e3a; this later work is local.
'''
    guide.write_text(guide_text,encoding='utf-8',newline='\n')
    coverage=json.loads(originals[ledger]);before_coverage=deepcopy(coverage);row=next(x for x in coverage['aspects'] if x['id']=='DD-50');before_row=deepcopy(row)
    for key,names in [('reviewEvidence',[app['data']['path'],app['chapter']['path'],'docs/audit/2026-10-08/full-game/COSMOLOGY_SOULS_RESEARCH_01_PATCH_CONFIRMATION_DOM.txt']),('validationEvidence',[application.relative_to(G).as_posix(),receipt.relative_to(G).as_posix()])]:
        for name in names:
            if name not in row[key]:row[key].append(name)
    row['completedScopes'].append('Bounded souls/Equation Research operating candidate jointly reviewed and locally adopted as NEW provisional design:21issues,64authored examples,392source checks; original sources and return history preserved. This does not close full cosmology.')
    row['currentEvidenceAddenda'].append({'id':'souls-chronology-01','recordedAtUtc':now,'application':application.relative_to(G).as_posix(),'nextConference':receipt.relative_to(G).as_posix(),'newProvisionalOperatingRulesAdopted':True,'fullDomainClosed':False})
    for key in ['status','closure','humanEvidence','ownerDirectionEvidence','completionClass']:assert row[key]==before_row[key]
    assert [x for x in coverage['aspects'] if x['id']!='DD-50']==[x for x in before_coverage['aspects'] if x['id']!='DD-50']
    ledger.write_bytes(encoded(coverage))
    text=originals[nav].decode('utf-8');tail=' + read(A / "SOULS_RESEARCH_FOLLOWUP_01_NAVIGATION_DELTA.json")["changes"]\n';assert text.count(tail)==1
    text=text.replace(tail,tail.rstrip('\n')+' + read(A / "SOULS_CHRONOLOGY_01_NAVIGATION_DELTA.json")["changes"]\n',1)
    nodes=[v for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(nodes)==1
    text=text.replace(ast.get_source_segment(text,nodes[0]),repr(scope),1)
    text=text.replace('    pending = [\n','    pending = [\n        '+repr(('Souls/Research candidate applied; chronology and library route with GPT',receipt.name))+',\n        '+repr(('Souls/Research — integrated operating candidate and confirmed patch',application.name))+',\n',1)
    compile(text,str(nav),'exec');nav.write_text(text,encoding='utf-8',newline='\n')
    changes=[{'before':next(x for x in pres if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [guide,start,ledger,nav]]
    changes[0]['operations']=[{'old':originals[guide].decode('utf-8'),'replacement':guide_text}]
    changes[1]['operations']=[{'old':line,'replacement':new_line}]
    changes[2]['operations']=[{'aspectId':'DD-50','old':before_row,'replacement':row}]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'fullDomainClosureChanged':False,'humanOrOwnerEvidenceChanged':False,'newProvisionalOperatingRulesAdopted':True}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout[-1000:]);print(run.stderr[-3000:]);raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]})
    state.update(newRuleAdoptions=1,newRuleAdoptionScope='One bounded new provisional souls/research operating package, with explicitly confirmed final patch; not recovered canon.',newRuleAdoptionCountScope='Count denotes one adopted package, not a count of individual mechanics. Prior checkpoint counts remain historical.',cosmologyReviewScope='Authority, creation, gods, Q6 and planes scoped references plus souls/research provisional operating candidate; full cosmology remains open.')
    state['activeGptReview'].update(recordedAtUtc=now,reviewId='COSMOLOGY-CHRONOLOGY-RESEARCH-ROUTE-01',status='submitted; GPT responding at observation',submission=info(receipt),archive=info(A/'DD_Cosmology_Chronology_Research_Route_01.zip'),attachmentDisplayName='DD_Cosmology_Chronology_Research_Route_01.zip',verdictReceived=False,responsePendingAtSubmission=True)
    state['cosmologySoulsResearchReview']={'application':info(application),'chapter':app['chapter'],'data':app['data'],'sourceChecks':392,'sourceFailures':0,'issues':21,'authoredExamplesAndSituations':64,'newProvisionalOperatingRulesAdopted':True,'fullCosmologyClosed':False}
    state['cosmologySoulsResearchSubmission'].update(newOperatingRulesAdopted=True,finalApplication=info(application))
    state['cosmologyChronologyResearchSites'].update(status='CE01–08 source comparison and concrete route conference submitted in Part3; no decision adopted',submission=info(receipt))
    state['ownerCosmologyCorrections']['readingOrder']=info(guide)
    state['safeNextActions']=['Observe the same Part3 chronology/research-route conference in Chrome tab125746244. Do not resend or ask continuation permission. Download its completed eight-file package and verify source bindings/citations and substantive CE01–08/route content.',
      'Current souls/research rules are locally adopted NEW provisional design in SOULS_RESEARCH_REVIEWED_01 and currentStateModel. Restore only those current rules; earlier draft/return operating proposals are preserved nonoperative history. KT3 duration and PT1 naming have an explicit GPT-confirmed patch.',
      'Review chronology without silently changing87AE/710AE, primordial ages, Choir/identity distinctions or choosing epoch. Review concrete new library/clue/qualification route against actual floor sources and current research rules. Ask the owner only for genuinely necessary unresolved creative choices after independent work.',
      'Continue the established17EPIgroups, pending ordinary spells419reviewed/429pending and other whole-game backlog. Keep runtime/human balance/whole-game gates separate.',
      'Latest verified GitHub18c6e3a; later cosmology work remains local. No sources deleted. Owner monitors usage.']
    state.setdefault('preservationManifests',[]).append(info(preserved/'PRESERVATION_MANIFEST.json'))
    target.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(target),'submission':info(receipt),'navigationLinks':navigation['existingDistinctLinks'],'missingLinks':0,'wholeGameApproved':False}))

if __name__=='__main__':main()
