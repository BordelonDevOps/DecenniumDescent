"""Freeze the new environment proposals and register their pending joint review."""
from copy import deepcopy
from datetime import datetime,timezone
import ast,hashlib,json,subprocess,sys,zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded
def read(p):return json.loads(p.read_bytes())
def main():
    now=datetime.now(timezone.utc).isoformat();draft=A/'environment-foundations-local-draft-01';packet=A/'environment-foundations-conference-01'
    archive=A/'DD_Environment_Foundations_01.zip';prep=A/'ENVIRONMENT_FOUNDATIONS_CONFERENCE_01_PREPARATION.json'
    target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_ENVIRONMENT_FOUNDATIONS_01.json';delta=A/'ENVIRONMENT_FOUNDATIONS_01_NAVIGATION_DELTA.json';preserved=A/'navigation-before-environment-foundations-01'
    assert all(not p.exists() for p in [packet,archive,prep,target,delta,preserved])
    m=read(draft/'MODEL.json');cases=read(draft/'CASEBOOK.json');assert len(m['sourceBindings'])==25 and cases['count']==59
    assert all(info(G/s['path'])==s for s in m['sourceBindings'])
    packet.mkdir()
    for name in ['MODEL.json','CASEBOOK.json','PLAYER_DISCUSSION.md','DIRECTOR_DISCUSSION.md','LOCAL_CHECKS.json']:(packet/name).write_bytes((draft/name).read_bytes())
    (packet/'DRAFT_REFINEMENT.json').write_bytes((A/'ENVIRONMENT_FOUNDATIONS_DRAFT_01A_REFINEMENT.json').read_bytes())
    for s in m['sourceBindings']:
        p=G/s['path'];out=packet/'sources'/s['path'];out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(p.read_bytes());assert hashlib.sha256(out.read_bytes()).hexdigest()==s['sha256']
    (packet/'SOURCE_BINDINGS.json').write_bytes(encoded(m['sourceBindings']))
    context={'scope':'Actual joint review of seven NEW environmental foundations and all59 authored situations; none adopted. Source references and current mechanics are distinct from proposed interpretations.','sourceFiles':25,'classCards':13,'recipeCards':5,'currentRulesUnchanged':True,'originalConsumablePacket':'DD_Core_Consumables_24_Proposals_01.zip','consumableStatus':'20 item procedures and four held source records remain unsubmitted/unadopted. This environment draft proposes a Stoneback interpretation without promoting it or rewriting the original packet.','actualNotebookStatus':'Calibration Review Continuation; last verified user turn b6e2e145-d54e-452a-93ea-4a172f23040c is terminal user-only/systemError. No live generation verified. This environment packet has never been submitted.','EPI08_14':'Completed notebook reply exists but exact return archive is unretrieved and not applied. Do not recreate, approve or infer its files.','otherOpenWork':['HZ08–14 disease/toxin/corrosion/trap/fall/protection catalogs and full expedition/Director/bestiary interfaces','Campaign era and unresolved cosmology','Ordinary spells419reviewed/429pending','Human playtesting, runtime, balance, publication and actual whole-game flow'],'approvalGranted':False}
    (packet/'CURRENT_REVIEW_CONTEXT.json').write_bytes(encoded(context))
    request='''# Environmental foundations — exact proposal conference

Please review the seven proposed environmental procedures and all 59 authored situations as one coherent set. This packet has 25 frozen source files, 13 current class cards, five current recipe cards, complete evidence for five broken Chapter 5 climate references, and eleven proposed answers to the climate acceptance questions. The full 25 files are under sources/ with their original relative paths. Other original-book hashes cited inside those evidence files identify source provenance; they are not a claim that every original book is included as a separate payload here.

Nothing in this draft has been adopted. Original books, current class cards, existing reviewed chapters and both older and current drafts remain preserved. The user requests a complete authored campaign-playtest candidate and actual conference on consequential mechanics. Please correct defects rather than merely approving isolated paragraphs.

Give particular attention to:

1. EF-01 elapsed time, initiative transitions, simultaneous source endings and nonduplicated pressure costs.
2. EF-02 breath reserve/grace, repeated short access to air, true nonbreathing bodies, transformation/resurrection, underwater V, state assignment rather than damage, real companion lifecycles, would-die replacements and the proposed exceptions to natural20/three-success stabilization. Do these interact coherently with the reviewed healing/death pipeline? Any replacement must be explicit NEW and fully specify cadence and costs.
3. EF-03 actual temperature/severity, fractional exposure across changing conditions, stage progression, Exhaustion ownership and recovery. Resolve the five source climate references with an explicit authored decision. Evaluate ancestry advantage and Warrior ordinary-penalty classification without claiming either was already agreed.
4. EF-04 Stoneback's exact interpretation. All four consumable source holds remain unapproved; this packet offers one concrete proposed resolution for CB-03. Do not approve the unseen other20 consumable procedures or change the preserved original four-hour, Tier2,1sp record.
5. EF-05 direct fire versus attached Burning, finite contact clocks and actual extinguishing resources; dense smoke, breathing and ventilation. Preserve current oil and existing ordinary-extinguish mechanics in their scopes.
6. EF-06 movement cost/caps, actual anatomy, current reactions, sinking abstraction and real weight/Load/tethers/towing. Do not infer a structural rescue rope from the explicitly ineligible Fiber-Husk Climbing Cord.
7. EF-07 weather forecasts, source-specific spells, mild StormMagic adjustments and exact overlap/recast priority. No cosmological calendar, season, origin, plane or campaign-era decision is authorized by this mechanics draft.

Return a complete corrected candidate, including every current procedure and case ID with explicit dispositions. Identify source-derived rules versus NEW adopted proposals versus unresolved questions. If an alternative is needed, supply its complete operational rule and update every affected example. Flag any genuine owner decision; do not invent prior owner canon. No human/runtime/balance/publication/whole-game approval is requested.

Requested return archive: DD_Environment_Foundations_01_Return.zip with eight root files: REGISTER.json, ENVIRONMENT_MODEL.json, PLAYER_CHAPTER.md, DIRECTOR_CHAPTER.md, CASEBOOK.json, SOURCE_HASHES.json, VERDICT.md, EVIDENCE_MANIFEST.json. Preserve all59 case IDs and list amendments; add further cases where necessary. Include exact source hashes, version-bound verdict and return size/SHA256. If file export is unavailable, say so rather than claiming an archive was created. The actual discussion and all decisions must remain readable in the notebook.
'''
    (packet/'REQUEST.md').write_text(request,encoding='utf-8',newline='\n')
    payload=[{'path':p.relative_to(packet).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(packet.rglob('*')) if p.is_file()]
    (packet/'PACKAGE_MANIFEST.json').write_bytes(encoded({'id':'ENVIRONMENT-FOUNDATIONS-CONFERENCE-01','payload':payload,'sources':m['sourceBindings'],'submitted':False,'newRulesAdopted':False}))
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(packet.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(packet).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for p in payload:assert len(z.read(p['path']))==p['bytes'] and hashlib.sha256(z.read(p['path'])).hexdigest()==p['sha256']
    prepared={'recordedAtUtc':now,'archive':info(archive),'request':info(packet/'REQUEST.md'),'currentModel':info(draft/'MODEL.json'),'currentCases':info(draft/'CASEBOOK.json'),'sources':25,'procedures':7,'authoredSituations':59,'climateAcceptanceAnswersProposed':11,'classCards':13,'recipeCards':5,'payloadFiles':len(payload),'zipManifestAdditional':1,'submitted':False,'newRulesAdopted':False,'sourceInformationDeleted':0}
    prep.write_bytes(encoded(prepared))

    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_ENVIRONMENT_REFERENCE_AUDIT_01.json';state=read(previous)
    start=G/'START_HERE.md';nav=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json';originals={};saved=[]
    for p in [start,nav,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        raw=p.read_bytes();out=preserved/p.relative_to(G);out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw);originals[p]=raw;saved.append({**info(p),'preservedCopy':out.relative_to(G).as_posix()})
    (preserved/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    text=originals[start].decode();oldcheckpoint=previous.relative_to(G).as_posix();newcheckpoint=target.relative_to(G).as_posix();assert text.count(oldcheckpoint)==1;text=text.replace(oldcheckpoint,newcheckpoint,1)
    oldparagraph=next(x for x in text.split('\n\n') if x.startswith('**Current independent development:**'))
    paragraph='**Current independent development:** The [environment foundation draft](docs/audit/2026-10-08/full-game/environment-foundations-local-draft-01/PLAYER_DISCUSSION.md) now supplies seven NEW proposed procedures for elapsed exposure, breath/suffocation/rescue, cold/heat, Stoneback, fire/smoke, swimming/currents and weather. Its [Director examples](docs/audit/2026-10-08/full-game/environment-foundations-local-draft-01/DIRECTOR_DISCUSSION.md) contain **59 authored situations**, and its [prepared conference packet](docs/audit/2026-10-08/full-game/ENVIRONMENT_FOUNDATIONS_CONFERENCE_01_PREPARATION.json) freezes25 current source files,13 class cards and5 recipe cards. Eleven climate acceptance questions now have proposed answers. All remain **unsubmitted and unadopted**; existing reviewed rules and source books are unchanged. The [Core consumable draft](docs/audit/2026-10-08/full-game/core-consumable-items-local-draft-01/DIRECTOR_DISCUSSION.md) still has20 unapproved procedures andfour source holds; the external environment proposal does not promote Stoneback or alter that original packet. Actual GPT exchange remains unavailable: the delivered [text-only four-item review](docs/audit/2026-10-08/full-game/CORE_CONSUMABLE_FOUR_HOLDS_TEXT_REVIEW_01.json) ended without an assistant reply. No live generation is verified.'
    text=text.replace(oldparagraph,paragraph,1);start.write_text(text,encoding='utf-8',newline='\n')
    coverage=json.loads(originals[ledger]);before=deepcopy(coverage);row=next(x for x in coverage['aspects'] if x['id']=='DD-22');oldaspect=deepcopy(row)
    row['draftEvidence'].extend(p.relative_to(G).as_posix() for p in [draft/'MODEL.json',draft/'PLAYER_DISCUSSION.md',draft/'DIRECTOR_DISCUSSION.md',draft/'CASEBOOK.json',prep])
    row['validationEvidence'].extend(p.relative_to(G).as_posix() for p in [draft/'LOCAL_CHECKS.json',A/'ENVIRONMENT_FOUNDATIONS_DRAFT_01A_REFINEMENT.json'])
    row.setdefault('currentEvidenceAddenda',[]).append({'id':'environment-foundations-local-draft01a','recordedAtUtc':now,'proceduresProposed':7,'authoredSituations':59,'currentSources':25,'actualClassCards':13,'actualRecipeCards':5,'climateAnswersProposed':11,'submitted':False,'newRulesAdopted':False,'behavioralTestsExecuted':0,'broaderHazardCatalogClosed':False,'scope':'Concrete source-linked proposals; source/arithmetic checks are not actual joint acceptance or gameplay tests.'})
    for k in ['status','closure','humanEvidence','completionClass']:assert row[k]==oldaspect[k]
    assert [x for x in coverage['aspects'] if x['id']!='DD-22']==[x for x in before['aspects'] if x['id']!='DD-22'];ledger.write_bytes(encoded(coverage))
    scope='Environmental foundations:7NEW proposals/59authored situations/25frozen sources/13class cards/5recipe cards, prepared-unsubmitted-unadopted. Eleven climate source questions have proposed answers; actual conference required. EPI08–14 exact return unretrieved; later arc and consumable packets still pending. Latest actual notebook text request b6e2e145-d54e-452a-93ea-4a172f23040c remains terminal user-only/systemError; no live generation verified. No original source, current approved rule or whole-game gate changed.'
    code=originals[nav].decode();tail=' + read(A / "ENVIRONMENT_REFERENCE_AUDIT_01_NAVIGATION_DELTA.json")["changes"]\n';assert code.count(tail)==1
    code=code.replace(tail,tail.rstrip('\n')+' + read(A / "ENVIRONMENT_FOUNDATIONS_01_NAVIGATION_DELTA.json")["changes"]\n',1)
    nodes=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(nodes)==1;code=code.replace(ast.get_source_segment(code,nodes[0]),repr(scope),1)
    items=[('Environment — seven proposed foundation procedures','environment-foundations-local-draft-01/PLAYER_DISCUSSION.md'),('Environment —59 proposed worked situations','environment-foundations-local-draft-01/DIRECTOR_DISCUSSION.md'),('Environment —25-source conference packet prepared',prep.name)]
    code=code.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(x)+',\n' for x in items),1);compile(code,str(nav),'exec');nav.write_text(code,encoding='utf-8',newline='\n')
    changes=[{'before':next(x for x in saved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,ledger,nav]]
    changes[0]['operations']=[{'old':oldcheckpoint,'replacement':newcheckpoint},{'old':oldparagraph,'replacement':paragraph}];changes[1]['operations']=[{'aspectId':'DD-22','old':oldaspect,'replacement':row}]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'newRulesAdopted':False,'fullDomainClosureChanged':False,'humanOrOwnerEvidenceChanged':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout[-1000:]);print(run.stderr[-2500:]);raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='progress',coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),newRuleAdoptions=0,newRuleAdoptionScope='Seven environment procedure proposals only, no adoption.',navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]})
    state['environmentFoundationsLocalDraft']={'model':info(draft/'MODEL.json'),'cases':info(draft/'CASEBOOK.json'),'playerDiscussion':info(draft/'PLAYER_DISCUSSION.md'),'directorDiscussion':info(draft/'DIRECTOR_DISCUSSION.md'),'initialPreparation':info(A/'ENVIRONMENT_FOUNDATIONS_DRAFT_01_PREPARATION.json'),'currentRefinement':info(A/'ENVIRONMENT_FOUNDATIONS_DRAFT_01A_REFINEMENT.json'),'conferencePreparation':info(prep),'conferenceArchive':info(archive),'sources':25,'procedures':7,'casesAuthored':59,'newRulesAdopted':False,'submitted':False,'runtimeExecuted':0}
    state['resumedBlockedAudit']={'resumedTurn':2,'sameConnectionBlockerObserved':True,'meaningfulProgress':'Seven full proposed environmental procedures and59 authored situations;25-source conference prepared. Independent authoring progressed, no joint acceptance inferred.','status':'active; meaningful independent progress remains'}
    state['safeNextActions']=['Environment packet DD_Environment_Foundations_01.zip is prepared but never submitted. Current01A supplies59 cases; initial56 remain preserved in history. No rule adoption. Prior syntax errors occurred before any draft output was written and were corrected before successful generation.','Actual GPT last authoritative state is still terminal user-only/systemError for b6e2e145-d54e-452a-93ea-4a172f23040c. No duplicate message sent this turn and no live generation verified. Restore actual exchange before any joint promotion.','Remaining environmental work includes HZ08–14 supported toxin/disease/corrosion/trap/fall/protection catalogs and real source-specific bestiary/Director/expedition interfaces. Do not treat this baseline draft as a complete environment domain.',*state['safeNextActions']]
    state.setdefault('preservationManifests',[]).append(info(preserved/'PRESERVATION_MANIFEST.json'));target.write_bytes(encoded(state))
    assert all(info(G/s['path'])==s for s in m['sourceBindings'])
    print(json.dumps({'preparation':info(prep),'archive':info(archive),'checkpoint':info(target),'links':navigation['existingDistinctLinks'],'missingLinks':0,'newRulesAdopted':False}))
if __name__=='__main__':main()
