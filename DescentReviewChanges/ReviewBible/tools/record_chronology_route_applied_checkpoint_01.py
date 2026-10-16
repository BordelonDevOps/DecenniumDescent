"""Record the bounded adopted route and refresh preserved navigation."""
from copy import deepcopy
from datetime import datetime,timezone
import ast,json,subprocess,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_CHRONOLOGY_LOCAL_PATCH_01.json'
    target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_CHRONOLOGY_ROUTE_01.json'
    delta=A/'CHRONOLOGY_ROUTE_01_NAVIGATION_DELTA.json';preserved=A/'navigation-before-chronology-route-01'
    assert all(not p.exists() for p in [target,delta,preserved])
    state=read(previous);now=datetime.now(timezone.utc).isoformat();application=A/'COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_APPLICATION_CHECK.json';app=read(application)
    assert app['newProvisionalRouteAdopted'] and app['failureCount']==0 and not app['wholeGameApproved']
    start=G/'START_HERE.md';guide=R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md';nav=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json'
    originals={};pres=[]
    for p in [start,guide,nav,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        raw=p.read_bytes();dest=preserved/p.relative_to(G);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw);originals[p]=raw;pres.append({**info(p),'preservedCopy':dest.relative_to(G).as_posix()})
    (preserved/'PRESERVATION_MANIFEST.json').write_bytes(encoded(pres))
    old_start=originals[start].decode();line=next(v for v in old_start.splitlines() if v.startswith('**Current joint review:**'))
    new_line='**Current joint review:** The [Equation research route](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/CHRONOLOGY_RESEARCH_ROUTE_REVIEWED_01.md) is now a jointly confirmed **provisional Director/playtest reference**:6scenes,10qualification findings,3prediction tests and a complete worked schedule. Its [application receipt](docs/audit/2026-10-08/full-game/COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_APPLICATION_CHECK.json) separates263source checks from115patch/clock checks. The [chronology source reference](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/CHRONOLOGY_SOURCE_REVIEWED_01.md) and [local companion reader changes](docs/audit/2026-10-08/full-game/COSMOLOGY_COMPANION_READER_01_APPLICATION_CHECK.json) are saved with originals intact. Continue from the [current cosmology guide](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md), [review map](REVIEW_MAP.html) or [latest checkpoint](docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_AFTER_CHRONOLOGY_ROUTE_01.json). Next:17epilogue groups and remaining full-game work. Ordinary spells remain **419 reviewed / 429 pending**. Campaign frame and unresolved identities remain open. Latest verified GitHub backup is18c6e3a; later work is local. **You are monitoring usage; the earlier50%stop is withdrawn.**'
    start.write_text(old_start.replace(line,new_line,1),encoding='utf-8',newline='\n')
    old_guide=originals[guide].decode();old_para=next(v for v in old_guide.split('\n\n') if v.startswith('The [exact local route patch]'))
    new_para='The [Equation research route](CHRONOLOGY_RESEARCH_ROUTE_REVIEWED_01.md) is now the current **NEW provisional Director/playtest route**. GPT explicitly confirmed the exact42change local candidate and independently checked its56interval clock. The [application receipt](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_CHRONOLOGY_RESEARCH_ROUTE_01_APPLICATION_CHECK.json) records263source/file/location checks and115exact-patch/clock checks, separately from runtime/human testing. The route supplies6scenes, finite handouts/provenance,10qualification findings,3prediction tests, a12hour local change cycle, a finite Floor50fallback library and actual research/rest/KnowledgeTransfer schedules. The same researcher can earn all5marks; existing Expertise remains valid. Current souls/research, actual language scope, equivalent knowledge, separate KT/PT/Hunt and full3test progression remain controlling. This adopts authored scenes/mechanics only, not a710AEcalendar convention, epoch, identity, fullT6–7campaign or EPImechanic.'
    guide_text=old_guide.replace(old_para,new_para,1)
    guide_text=guide_text.replace('The revised route has authored holdings and scenes, but its operational integration remains under review; proposed Floor68 Wax geography is not an original source fact.','The current jointly reviewed route now adopts a Floor68Melted Annex and a Floor50service-ledger fallback as explicit NEW design. Neither placement nor those new holdings are recovered original geography/text. Existing cosmic libraries remain unmoved.')
    guide_text=guide_text.replace('First, revised and integrated return archives remain immutable. The current chapter and confirmed patch govern this bounded interface; superseded proposal text is nonoperative history.','First, revised and integrated return archives remain immutable. The current souls/research and route chapters plus their confirmed patches govern their bounded interfaces; superseded proposal text is nonoperative history.')
    guide.write_text(guide_text,encoding='utf-8',newline='\n')
    coverage=json.loads(originals[ledger]);before=deepcopy(coverage);row=next(v for v in coverage['aspects'] if v['id']=='DD-50');before_row=deepcopy(row)
    row['reviewEvidence'].extend([app['chapter']['path'],app['data']['path'],app['confirmation']['path']]);row['validationEvidence'].append(application.relative_to(G).as_posix())
    row['completedScopes'].append('Bounded authored Equation research route jointly confirmed and locally adopted:6scenes,10findings,3tests,56interval clock;263source checks plus115patch/arithmetic checks. Original sources/archives preserved; epoch/identity/EPI/runtime/human/full-domain gates remain open.')
    row['currentEvidenceAddenda'].append({'id':'chronology-route-01','recordedAtUtc':now,'application':application.relative_to(G).as_posix(),'newProvisionalRouteAdopted':True,'fullDomainClosed':False})
    for k in ['status','closure','humanEvidence','ownerDirectionEvidence','completionClass']:assert row[k]==before_row[k]
    assert [v for v in coverage['aspects'] if v['id']!='DD-50']==[v for v in before['aspects'] if v['id']!='DD-50'];ledger.write_bytes(encoded(coverage))
    scope='Jointly confirmed Equation research route locally adopted as NEW provisional design:6nodes,10findings,3tests,56intervals;263source checks and115patch/clock checks. Original text/archives preserved. Chronology source comparison and narrow companion reader change saved. Next17EPIgroups; owner epoch and identity choices remain open. Ordinary spells419reviewed429pending. Fullgame/runtime/human approval open. GitHub18c6e3a; later work local.'
    text=originals[nav].decode();tail=' + read(A / "CHRONOLOGY_LOCAL_PATCH_01_NAVIGATION_DELTA.json")["changes"]\n';assert text.count(tail)==1
    text=text.replace(tail,tail.rstrip('\n')+' + read(A / "CHRONOLOGY_ROUTE_01_NAVIGATION_DELTA.json")["changes"]\n',1)
    nodes=[v for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(nodes)==1
    text=text.replace(ast.get_source_segment(text,nodes[0]),repr(scope),1)
    text=text.replace('    pending = [\n','    pending = [\n        '+repr(('Equation research route — jointly confirmed provisional candidate applied',application.name))+',\n',1)
    compile(text,str(nav),'exec');nav.write_text(text,encoding='utf-8',newline='\n')
    changes=[{'before':next(v for v in pres if v['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [guide,start,ledger,nav]]
    changes[0]['operations']=[{'old':old_guide,'replacement':guide_text}];changes[1]['operations']=[{'old':line,'replacement':new_line}];changes[2]['operations']=[{'aspectId':'DD-50','old':before_row,'replacement':row}]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'fullDomainClosureChanged':False,'humanOrOwnerEvidenceChanged':False,'newProvisionalRouteAdopted':True}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout[-1000:]);print(run.stderr[-3000:]);raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]},newRuleAdoptions=1,newRuleAdoptionScope='One bounded jointly confirmed NEW provisional research-route package; source chronology/epoch/identity/EPI decisions not adopted.',newRuleAdoptionCountScope='Package count for this checkpoint, not a count of individual rules. Earlier package history remains preserved.')
    state['activeGptReview'].update(status='LP01..08 explicitly confirmed by actual GPT Part3; exact route locally applied. Ready for next epilogue conference.',verdictReceived=True,verdictStatus='Bounded acceptance of exact candidate010af70d88ccd56c5f876b96afa3119392a4e4ae2fef8bdb5275cbe17d22c491',responsePendingAtSubmission=False,confirmation=app['confirmation'],application=info(application))
    state['cosmologyChronologyRouteReview'].update(newRouteRulesAdopted=True,application=info(application),chapter=app['chapter'],data=app['data'],confirmation=app['confirmation'])
    state['cosmologyChronologyResearchSites'].update(status='Source comparison saved; jointly confirmed new route adopted locally; EPIandepoch remain open',routeApplication=info(application))
    state['ownerCosmologyCorrections']['readingOrder']=info(guide)
    state['safeNextActions']=['The exact research route has now been jointly confirmed and applied. Use CHRONOLOGY_RESEARCH_ROUTE_REVIEWED_01 and chronology_research_route_reviewed_01/currentRoute; do not resume the already completed42patch review or use superseded route cases as current.',
      'Prepare the next source-bound EPI01–17 conference. Original epilogue inventory has17groups; allsourceparagraphs were read. Review actual current class abilities/conditions/resources and finite item/crafting/encounter interfaces before authoring. Preserve EPIIDs and source distinctions; frame-dependent15–17 await the pending owner campaign-frame answer.',
      'Actual GPT Part3 remains Chrome3/tab125746244. Same conversation is ready; no continuation permission/new chat is needed. Send a concrete bounded source packet for the next mechanics cohort rather than ungrounded whole-domain claims.',
      'Chronology source comparison preserves87AE/710AE; no prospective710anchor, epoch or identity merge is adopted. Owner before/during/afterProofWar answer remains pending; independent work continues.',
      'Companion reader change is locally verified; preview tab closed/server stopped. Broader deep-floor listings, companion implementation, human balance and full-game validation remain open.',
      'Continue419reviewed/429pending ordinary spells and the full-game backlog after the current source-bound cosmology development. Latest verified GitHub18c6e3a; later work local; no sources deleted.']
    state.setdefault('preservationManifests',[]).append(info(preserved/'PRESERVATION_MANIFEST.json'))
    target.write_bytes(encoded(state));print(json.dumps({'checkpoint':info(target),'application':info(application),'mapLinks':navigation['existingDistinctLinks'],'missingLinks':0,'wholeGameApproved':False}))

if __name__=='__main__':main()
