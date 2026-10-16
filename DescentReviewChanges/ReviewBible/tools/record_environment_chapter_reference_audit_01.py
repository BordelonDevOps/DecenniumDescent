"""Preserve the actual climate cross-reference failure and index the next review need."""
from copy import deepcopy
from datetime import datetime, timezone
import ast, hashlib, json, subprocess, sys, zipfile
import xml.etree.ElementTree as ET
from apply_di7_ap_as_01 import G, R, A, info, encoded

NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
def read(p): return json.loads(p.read_bytes())
def paragraphs(p):
    with zipfile.ZipFile(p) as z: root=ET.fromstring(z.read('word/document.xml'))
    return [''.join(x.text or '' for x in q.findall('.//w:t',NS)) for q in root.findall('.//w:p',NS)]
def section(ps, prefix):
    start=next(i for i,t in enumerate(ps) if t.startswith(prefix))
    end=next((i for i in range(start+1,len(ps)) if ps[i].startswith('Chapter ')),len(ps))
    return {'heading':ps[start],'startParagraph':start,'endParagraphExclusive':end,'paragraphs':[{'paragraphIndex':i,'text':ps[i]} for i in range(start,end)]}
def objects(x):
    if isinstance(x,dict):
        yield x
        for v in x.values(): yield from objects(v)
    elif isinstance(x,list):
        for v in x: yield from objects(v)

def main():
    now=datetime.now(timezone.utc).isoformat()
    audit=A/'ENVIRONMENT_CHAPTER_REFERENCE_AUDIT_01.json'
    target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_ENVIRONMENT_REFERENCE_AUDIT_01.json'
    delta=A/'ENVIRONMENT_REFERENCE_AUDIT_01_NAVIGATION_DELTA.json'
    preserved=A/'navigation-before-environment-reference-audit-01'
    assert all(not p.exists() for p in [audit,target,delta,preserved])
    receipt=A/'CORE_CONSUMABLE_FOUR_HOLDS_TEXT_REVIEW_01.json'
    delivery=read(receipt);assert delivery['delivery']['verified'] and not delivery['delivery']['assistantReplyObserved']
    player=R/'books/player/Decennium_Descent_Player_Rulebook_v6.docx'
    director=G/'docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx'
    director_review=R/'docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx'
    ancestry=R/'data/playtest/ancestry_background_candidate.json'
    druid=R/'data/public/class_playtests/druid.json'
    guide=R/'docs/mechanics/ANCESTRY_BACKGROUND_PLAYTEST.md'
    core=R/'data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json'
    recon=A/'ENVIRONMENT_HAZARD_SOURCE_RECONNAISSANCE.json'
    sources=[player,director,director_review,ancestry,druid,guide,core,recon]
    source_info=[info(p) for p in sources]
    pp=paragraphs(player);dp=paragraphs(director);rp=paragraphs(director_review)
    chapter=section(pp,'Chapter 5:')
    assert chapter['startParagraph']==6496 and chapter['endParagraphExclusive']==7153
    refs=[{'paragraphIndex':i,'text':t} for i,t in enumerate(pp) if 'environmental rules in Chapter 5' in t or 'environmental rules in chapter 5' in t]
    assert [x['paragraphIndex'] for x in refs]==[508,518,634,1319,2758]
    ancestor_records=[x for x in objects(read(ancestry)) if x.get('sourceLine') in [509,519,635,1320] and 'text' in x]
    assert len(ancestor_records)==4
    druid_records=[x for x in objects(read(druid)) if x.get('id')=='druid.base.winterfang.cold-resistance']
    assert len(druid_records)==1
    climate_lines=[{'line':i,'text':t} for i,t in enumerate(guide.read_text(encoding='utf-8').splitlines(),1) if 'Climate adaptation grants' in t]
    assert len(climate_lines)==1
    original_sections=[section(dp,p) for p in ['Chapter 20 ','Chapter 28 ','Chapter 30 ']]
    review_sections=[section(rp,p) for p in ['Chapter 20 ','Chapter 28 ','Chapter 30 ']]
    section_comparison=[{'heading':a['heading'],'originalStart':a['startParagraph'],'reviewStart':b['startParagraph'],'paragraphTextsEqual':[x['text'] for x in a['paragraphs']]==[x['text'] for x in b['paragraphs']]} for a,b in zip(original_sections,review_sections)]
    findings=[
      {'id':'HZ-REF-01','kind':'source-cross-reference-failure','finding':'Five climate-adaptation source traits point to environmental rules in Chapter 5. The complete referenced chapter is Equipment, paragraphs 6496–7152; its reading does not supply a cold/heat exposure scale, temperature bands, check cadence or recovery procedure. This is a conclusion about this complete chapter, not a claim of absence from every project source.','affectedSourceParagraphs':[508,518,634,1319,2758],'affectedCharacters':['Flame Drakari','Frost Drakari','Mountain Dwarf','Mountain Ogre','Winterfang Druid']},
      {'id':'HZ-REF-02','kind':'authority-distinction','finding':'The original Director Chapter 28 explicitly says its Noise/Supply/Exposure/Attention tracks are Director instruments, not universal player statistics. Its example Exposure thresholds 2/4/6 do not define the first personal cold-weather exposure level promised by Stoneback Stout. Chapter 20 supplies tier themes and logistics advice; Chapter 30 supplies difficulty bands, clues and finite-failure guidance, without the missing personal cold progression.'},
      {'id':'HZ-REF-03','kind':'current-integration-boundary','finding':'The reviewed ancestry integration retains only the actual environmental benefit of climate adaptation and excludes damage/suffocation immunity. It does not instantiate that missing baseline. The current Winterfang Druid card already grants advantage on nonmagical extreme-cold exposure saves, but a particular hazard must still supply the actual save trigger, DC and consequence. No current ancestry/class card is changed.'},
      {'id':'HZ-REF-04','kind':'source-variant-preservation','finding':'The original Director book and ReviewBible Director copy have different paragraph counts and file hashes. Their three full hazard-related chapter excerpts are retained separately and compared by exact paragraph text. Neither entire book is declared duplicate or obsolete.'},
      {'id':'HZ-REF-05','kind':'required-authoring-before-integration','finding':'HZ-03 needs an explicit source reconciliation and full environmental procedure, or a consciously NEW replacement interpretation, before the four ancestry climate traits and CB-03 can be called mechanically complete. Preserve the original promises and current protection limits. A recipe approval, an ordinary cold damage resistance, the Director pressure track and the unadopted sky-voyage hazard are not substitutes.'}
    ]
    acceptance=[
      'Define the actual hot/cold threshold, exposure trigger, elapsed interval and save/outcome for a character initially unexposed.',
      'State whether personal cold exposure is a distinct track or an explicit NEW use of existing Exhaustion; show the complete progression and ending.',
      'Apply Stoneback before the first cold exposure level and specify what is ignored: a gain, a numbered level’s penalties, or a different explicit replacement.',
      'Apply Stoneback after cold exposure already exists; specify retroactive suppression and what returns when four hours expire.',
      'Resolve four-hour dose expiry at the same instant as an exposure check without an extra check or free erased consequence.',
      'Keep Exhaustion from marching, starvation or another non-cold cause distinct from whatever the item suppresses.',
      'Resolve repeated/overlapping doses without resetting the hazard history or fabricating multiple first levels.',
      'Give actual shelter, dry/wet clothing and warming recovery requirements, including interrupted recovery and return to exposure.',
      'Apply Flame/Frost Drakari, Mountain Dwarf/Ogre adaptation and Winterfang advantage to the chosen exact hazard, preserving their distinct altitude/damage clauses.',
      'Resolve damage resistance, true environmental immunity and ordinary-penalty suppression separately; maintain actual breathing and life-state rules.',
      'Advance time through rest, Watch boundaries, combat and travel once; distinguish Director pressure consequences from the same exposure already resolved.'
    ]
    record={'id':'ENVIRONMENT-CHAPTER-REFERENCE-AUDIT-01','recordedAtUtc':now,'status':'source-findings-recorded; environmental-procedure-unresolved','indexConvention':'zero-based all w:p including table cells; guide lines one-based','sources':source_info,'playerParagraphCount':len(pp),'referencedEquipmentChapter':chapter,'brokenClimateReferences':refs,'currentAncestrySourceRecords':ancestor_records,'currentDruidCard':druid_records[0],'currentReviewedGuideLines':climate_lines,'originalDirectorParagraphCount':len(dp),'reviewDirectorParagraphCount':len(rp),'originalDirectorChapters':original_sections,'reviewDirectorChapters':review_sections,'directorChapterComparison':section_comparison,'stonebackOriginal':read(core)['brews'][2],'findings':findings,'acceptanceQuestions':acceptance,'acceptanceAnswersAuthored':0,'localSemanticsApproved':False,'actualGptReview':info(receipt),'newRulesAdopted':False,'sourceInformationDeleted':0,'scope':'Full referenced Equipment chapter and three full Director chapters in each existing copy; source binding and semantic source audit, not whole-project absence proof or a new hazard rule.'}
    assert source_info==[info(p) for p in sources]
    record['checks']={'fiveOriginalReferencesBound':True,'fourCurrentAncestryRecordsBound':True,'oneCurrentDruidRecordBound':True,'oneReviewedGuideBoundaryBound':True,'allEightSourceFilesUnchanged':True,'failures':0,'scope':'Source identity/selection checks, not behavioral or balance tests.'}
    audit.write_bytes(encoded(record))

    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_CORE_CONSUMABLE_ITEMS_DRAFT_01.json'
    state=read(previous);start=G/'START_HERE.md';nav=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json'
    originals={};saved=[]
    for p in [start,nav,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        raw=p.read_bytes();out=preserved/p.relative_to(G);out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw);originals[p]=raw;saved.append({**info(p),'preservedCopy':out.relative_to(G).as_posix()})
    (preserved/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    oldstart=originals[start].decode();newstart=oldstart
    oldcheckpoint=previous.relative_to(G).as_posix();newcheckpoint=target.relative_to(G).as_posix();assert newstart.count(oldcheckpoint)==1
    newstart=newstart.replace(oldcheckpoint,newcheckpoint,1)
    oldparagraph=next(x for x in newstart.split('\n\n') if x.startswith('**Current independent development:**'))
    paragraph=oldparagraph+' The [full-chapter climate reference audit](docs/audit/2026-10-08/full-game/ENVIRONMENT_CHAPTER_REFERENCE_AUDIT_01.json) now identifies five broken references to environmental rules in the Equipment chapter, preserves both Director versions and specifies eleven unanswered integration cases. The [four-item text-only review request](docs/audit/2026-10-08/full-game/CORE_CONSUMABLE_FOUR_HOLDS_TEXT_REVIEW_01.json) was delivered but ended with no assistant reply and a system-error chat state; the connection issue is not limited to archive exports.'
    newstart=newstart.replace(oldparagraph,paragraph,1);start.write_text(newstart,encoding='utf-8',newline='\n')
    coverage=json.loads(originals[ledger]);before=deepcopy(coverage);row=next(x for x in coverage['aspects'] if x['id']=='DD-22');oldaspect=deepcopy(row)
    row['draftEvidence'].append(audit.relative_to(G).as_posix())
    row.setdefault('currentEvidenceAddenda',[]).append({'id':'environment-chapter-reference-audit01','recordedAtUtc':now,'brokenSourceReferences':5,'wholePlayerChapterRead':True,'wholeDirectorChaptersPerVersion':3,'originalsPreserved':True,'acceptanceQuestions':11,'answersAuthored':0,'newRulesAdopted':False,'scope':'The promised climate baseline is not supplied by the referenced Equipment chapter or the distinct Director pressure procedure. Full hazard authoring and actual joint review remain required.'})
    for k in ['status','closure','humanEvidence','completionClass']:assert row[k]==oldaspect[k]
    assert [x for x in coverage['aspects'] if x['id']!='DD-22']==[x for x in before['aspects'] if x['id']!='DD-22']
    ledger.write_bytes(encoded(coverage))
    scope='EPI01–07 applied; EPI08–14 return unretrieved. The new four-consumable text-only source request was delivered as b6e2e145-d54e-452a-93ea-4a172f23040c, terminal user-only/systemError; no live generation verified. Prepared consumable27-source/80-case and arc44-source/67-case packets remain unsubmitted/unadopted. Full chapter audit establishes five broken climate references; HZ03 full procedure and eleven acceptance answers remain open. No sources deleted, rules adopted or whole-game approval.'
    code=originals[nav].decode();tail=' + read(A / "CORE_CONSUMABLE_ITEMS_DRAFT_01_NAVIGATION_DELTA.json")["changes"]\n';assert code.count(tail)==1
    code=code.replace(tail,tail.rstrip('\n')+' + read(A / "ENVIRONMENT_REFERENCE_AUDIT_01_NAVIGATION_DELTA.json")["changes"]\n',1)
    nodes=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(nodes)==1
    code=code.replace(ast.get_source_segment(code,nodes[0]),repr(scope),1)
    items=[('Climate — five broken source references and full chapter evidence',audit.name),('Actual GPT — four held items, text-only review delivery',receipt.name)]
    code=code.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(x)+',\n' for x in items),1);compile(code,str(nav),'exec');nav.write_text(code,encoding='utf-8',newline='\n')
    changes=[{'before':next(x for x in saved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,ledger,nav]]
    changes[0]['operations']=[{'old':oldcheckpoint,'replacement':newcheckpoint},{'old':oldparagraph,'replacement':paragraph}]
    changes[1]['operations']=[{'aspectId':'DD-22','old':oldaspect,'replacement':row}]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'newRulesAdopted':False,'fullDomainClosureChanged':False,'humanOrOwnerEvidenceChanged':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout[-1000:]);print(run.stderr[-2500:]);raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',previousGoalTurnClassification='no progress',coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),newRuleAdoptions=0,newRuleAdoptionScope='Source evidence and failed text-review delivery only; no environment/item rule adopted.',navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]})
    state['environmentChapterReferenceAudit']={'audit':info(audit),'sourceReferences':5,'acceptanceQuestions':11,'environmentProcedureAuthored':False,'newRulesAdopted':False}
    state['latestActualGptTextReviewEvidence']={'receipt':info(receipt),'threadId':delivery['threadId'],'userTurnId':delivery['delivery']['userTurnId'],'status':'terminal-user-only/systemError','assistantReplyObserved':False,'liveGenerationVerified':False}
    state['resumedBlockedAudit']={'resumedTurn':1,'sameConnectionBlockerObserved':True,'meaningfulProgress':'Five source references now bound to a complete chapter read; full environmental prerequisite identified; text-only delivery established the issue is not archive-export-specific.','status':'active; do not mark blocked at the first resumed turn'}
    state['safeNextActions']=['Do not duplicate the text request. Its delivery is verified and its turn is terminal without an assistant response. Continue actual review when a working chat or external-state change is available.','HZ03 requires a full environment procedure or explicit reviewed replacement: five climate references target Equipment, which supplies no exposure scale. The Director pressure track is distinct. Preserve all five original promises and existing reviewed class/ancestry limits.',*state['safeNextActions']]
    state.setdefault('preservationManifests',[]).append(info(preserved/'PRESERVATION_MANIFEST.json'));target.write_bytes(encoded(state))
    assert source_info==[info(p) for p in sources]
    print(json.dumps({'audit':info(audit),'checkpoint':info(target),'playerChapterParagraphs':len(chapter['paragraphs']),'directorChapterComparison':section_comparison,'links':navigation['existingDistinctLinks'],'missingLinks':0,'newRulesAdopted':False}))

if __name__=='__main__':main()
