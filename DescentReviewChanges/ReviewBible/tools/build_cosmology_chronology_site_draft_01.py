"""Consolidate chronology and research-site dependencies; preserve all source dates."""
from datetime import datetime, timezone
from zipfile import ZipFile
from xml.etree import ElementTree as E
import hashlib,json
from apply_di7_ap_as_01 import G,R,A,info,encoded


def read(p):return json.loads(p.read_bytes())


def main():
    target=R/'data/director/cosmology/chronology_research_sites_draft_01.json'
    chapter=R/'docs/director-only/cosmology/CHRONOLOGY_RESEARCH_SITES_DRAFT_01.md'
    check=A/'COSMOLOGY_CHRONOLOGY_RESEARCH_SITES_DRAFT_01_CHECK.json'
    assert all(not p.exists() for p in [target,chapter,check])
    bindings={};evidence={};ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    def bind(p):
        row=info(p);bindings[row['path']]=row;return row['path']
    def obj(key,p,ptr):
        path=bind(p);v=read(p)
        for t in ptr.strip('/').split('/'):
            t=t.replace('~1','/').replace('~0','~');v=v[int(t)] if isinstance(v,list) else v[t]
        evidence[key]={'id':key,'path':path,'jsonPointer':ptr,'value':v}
    def txt(key,p,lo=1,hi=None):
        path=bind(p);lines=p.read_text(encoding='utf-8-sig').splitlines();hi=hi or len(lines);assert hi<=len(lines)
        value='\n'.join(lines[lo-1:hi]);evidence[key]={'id':key,'path':path,'firstLineOneBased':lo,'lastLineOneBased':hi,'text':value,'textSha256':hashlib.sha256(value.encode()).hexdigest()}
    headings=[0,22,40,60,75,101,125,160,194,215,241,263]
    openings=[1,23,41,61,76,102,126,161,195,216,242]
    originals=sorted(set(headings+openings+[27,33,34,35,39,103,104,105,106,107,184,185,198,214,226,229,230,231,236,237,238,239,240]+list(range(253,263))+list(range(264,326))))
    sources=[('O',G/'The Cosmology of Decennium Descent.docx',originals),
             ('W',G/'The_World_of_Aethel_Lore.docx',[3,5,7,9]+list(range(50,60))+list(range(77,94))),
             ('C',G/'books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx',[28,29])]
    docx_text={}
    for prefix,p,inds in sources:
        path=bind(p)
        with ZipFile(p) as z:root=E.fromstring(z.read('word/document.xml'))
        ps=[''.join(t.text or '' for t in q.findall('.//w:t',ns)) for q in root.findall('.//w:p',ns)];docx_text[p]=ps
        for i in inds:evidence[f'{prefix}{i}']={'id':f'{prefix}{i}','path':path,'part':'word/document.xml','paragraphIndexZeroBased':i,'text':ps[i],'textSha256':hashlib.sha256(ps[i].encode()).hexdigest()}
    owner=R/'data/director/cosmology/heartcell_owner_update_02.json'
    for i in [0,1,2,4,5]:obj(f'HC02-{i+1:02d}',owner,f'/decisions/{i}')
    gods=R/'data/director/cosmology/gods_pantheons_reviewed_01.json'
    for key,ptr in [('GP-EPOCH','/unresolvedDependencies/13'),('GP-EPI','/followupDispositions/5'),('GP-CHRON','/followupDispositions/7'),('GP-REVEAL','/factBeliefRevelation/10')]:obj(key,gods,ptr)
    txt('Q6-CURRENT',R/'docs/director-only/cosmology/Q6_LATER_LOCK_REVIEWED_01.md')
    obj('Q6-QUALIFICATION',R/'data/director/cosmology/q6_later_lock_reviewed_01.json','/currentQualification')
    for prefix,p in [('MAIN',G/'src/data/dungeon-mechanics.json'),('RB',R/'src/data/dungeon-mechanics.json')]:
        for suffix,ptr in [('TIMELINE','/timeline'),('ROTATION','/cycle/rotation'),('CALENDAR','/cycle/calendar'),('BINDING','/cycle/mythHistory/1')]:obj(prefix+'-'+suffix,p,ptr)
    txt('RB-UI',R/'src/components/DungeonGuide.tsx',700,731)
    epi=A/'ORIGINAL_COSMOLOGY_EPILOGUE_RULE_INVENTORY_01.json';bind(epi)
    obj('EPI-COUNT',epi,'/count');obj('EPI-GROUPS',epi,'/groupCounts')
    assert evidence['EPI-COUNT']['value']==17
    old_units=read(epi)['units'];review_units=evidence['GP-EPI']['value']['epilogueRuleGroups']
    assert [(x['id'],x['title']) for x in old_units]==[(x['id'],x['title']) for x in review_units]
    context=[info(R/'data/director/cosmology/equation_library_source_inventory_01.json'),info(R/'data/director/cosmology/equation_research_interface_draft_01.json'),info(R/'data/director/cosmology/souls_death_hunt_conference_draft_01.json')]
    chapter_order=[{'ordinal':j+1,'paragraphIndexZeroBased':i,'heading':docx_text[G/'The Cosmology of Decennium Descent.docx'][i],'classification':'printed document order; not a chosen current campaign date'} for j,i in enumerate(headings)]
    events=[]
    def event(n,title,refs,fact,limit):events.append({'id':f'CH{n:02d}','title':title,'evidenceIds':refs,'sourceFinding':fact,'currentCampaignLimit':limit})
    event(1,'First Choir formation and assault — contested timing',['O27','O33','O34','O35','O39','HC02-03'],
          'The original presents unnamed chords, invitation/formation and active seal repair before the direct scarlet-fire assault opening the Sundering. The owner says the First Choir arose in response to Asmodeus attacking Calanthir.',
          'Owner intent is recorded; exact event/awakening timing remains unresolved. Do not restore the withdrawn no-agency-before-assault or one-to-one Harmony mapping.')
    event(2,'Pillar realms mature after the Sundering',['O61','O76'],
          'The Planes Ascendant opening explicitly follows the Sundering and describes four differentiating realms; the next chapter begins with all four contributing to the Weave.',
          'This is relative narrative order, not a numbered-year or floor mapping.')
    event(3,'Watch Convocation and aspirant gates',['O102','O103','O104','O105','O106','O107'],
          'During the Lucent Interregnum, nascent divinity leads the Choir to open access to seven long-vacant Thrones. A gate appears at an unnamed Mirrorsage monastery library.',
          'The Thrones are described as older than this opening. The monastery has no supplied numbered floor; current gate availability is not selected.')
    event(4,'Candescent Loom and Weave refraction',['O126'],
          'After the Argent Gate shines, the narrative describes small acts leaving visible intention records, called the Candescent Loom.',
          'A source episode does not automatically make every intention visible through current spells or provide a universal moral detection rule.')
    event(5,'Pact sentience',['O161'],
          'Accumulated resonance gives the Pact a will distinct from a god or Choir chord in the narrative.',
          'Do not use this development to identify the Heartcell builder or assign a calendar date.')
    event(6,'Archon sites and living records',['O184','O185'],
          'Within the Pact-sentience chapter, Valcendyr forms the Oath Archive in Crystal Bastion and Quorilith establishes Library of Shifting Sigils.',
          'These are source-established events, with no chosen present-campaign access or Equation holdings.')
    event(7,'Shardfall and Silver Prism Year',['O195','O198'],
          'The Moment of First Scatter is called Shardfall; the ensuing Silver Prism Year has elastic length measured by transformed lives. Sixth Archive cartographers meet at Sigil Navigators Library.',
          'Do not convert the Year into one standard 400-day year or treat Sixth Archive as Floor 6. The library alias remains unresolved.')
    event(8,'Epoch of Chosen Threads',['O214','O216'],
          'The Silver Prism Year closes; scholars call the transition the Epoch of Chosen Threads. Community story keys can manifest resource-bearing Dungeon enclaves in the source.',
          'Epoch terminology supplies no fixed elapsed duration or automatically usable new portal mechanic.')
    event(9,'Counter-expression and Unbound Academy',['O226','O229','O230','O231'],
          'The Matrix broadcast prompts the Spiral Integral counter-expression. Quiet Wells later collapse and the Matrix equation fades; after the Sunrise of Chosen Threads a council builds the Unbound Academy.',
          'The narrative subsequently develops a renewed threat; this episode is not proof that all Oblivion danger has permanently ended or that Academy access is guaranteed now.')
    event(10,'Quiet Masquerade and Citadel of Many Echoes',['O236','O237','O238'],
          'Following the Masquerade confrontation, the Academy and Yieldheart guilds build the Citadel at Crystalfall Summit. Its galleries preserve songs, prototypes and restricted chronicles; later the Matrix develops deliberate calculus.',
          'Do not merge the Citadel with a numbered dungeon floor or assume Selene’s foundation journal is freely accessible.')
    event(11,'Matrix Horizon and imminent campaign',['O239','O240','O242'],
          'The Dawn Loom concert identifies the approaching Matrix Horizon. A later chapter places its arrival on the twentieth eve after the Citadel Vigil.',
          'The passage gives a relative marker, not a bridge to AE dating. Do not equate the Vigil with the Citadel’s founding date without evidence.')
    event(12,'High Chancel ascent',['O253','O254','O255','O256'],
          'The fellowship ascends a ladder of living light toward the High Chancel to confront the Matrix edge.',
          'The route is not a normal descent to Floor 97 or Floor 100 merely because the same saga discusses the Dungeon.')
    event(13,'Silent Library and Final Ledger',['O257','O258','O259'],
          'Inside the Matrix, the Silent Library tries to reduce cognition to zero. Memory-rope and song stabilize its books; the Final Ledger is answered and blanks before the walls open onward.',
          'Keep the encounter’s transformation. An untouched reusable library, a fixed floor or guaranteed access is not supplied.')
    event(14,'Shard of Absolute Rest, victory and Charter',['O260','O261','O262'],
          'The black Shard of Absolute Rest splits; the Matrix curve scatters and Null breaches seal. The Charter of Infinite Yield follows. Ul nak’s dream recedes rather than vanishing; Stillness may try again in ages.',
          'Do not identify this shattered shard with Q6’s focusing crystal, or convert receding dream into death of the survivor/Old God. No identity bridge is established.')
    event(15,'Explicit post-Proof-War epilogue',['O264','O265','O266','O267','O270','O275','O279'],
          'Movement One explicitly places its scene after the Proof War. Later movements give the Spiral cosmograph and Choir chorus around the Charter.',
          'The document’s later setting does not select the current campaign epoch. Map symbols and coils are not numbered dungeon floors.')
    event(16,'Epilogue toolbox and express portability',['O307','O308','O309','O318','O319','O320','O321','O322','O323','O324','GP-EPI'],
          'Dungeon seeds are headed after Infinite Yield, and three arcs continue beyond the epilogue. P324 expressly permits tables and relics to be used independently of the saga or in multi-era campaigns.',
          'Preserve both original placement and permission to adapt. Portability does not choose a floor, public truth, chronology or automatic mechanical replacement. Reuse the existing seventeen EPI groups.')
    sites=[]
    def site(id,name,refs,placement,decision):sites.append({'libraryRecordId':id,'name':name,'evidenceIds':refs,'sourcePlacement':placement,'remainingPlacementDecision':decision})
    site('LIB03','Mirrorsage monastery library',['O104','O106','O107'],'Aspirant-gate opening in the Gods’ Awakening narrative.','Specify present access and location; do not treat the destination’s deep Dungeon hall as the monastery’s address.')
    site('LIB06','Oath Archive',['O184'],'Created during the Pact-sentience chapter, inside Crystal Bastion.','Current availability and actual research text remain unassigned.')
    site('LIB07','Library of Shifting Sigils',['O185'],'Established during the Pact-sentience chapter, before the later Shardfall episode in document order.','Do not resolve its identity with Sigil Navigators Library by proximity of names.')
    site('LIB09','Sigil Navigators Library',['O198'],'A meeting site during the elastic Silver Prism Year.','Choose its current state only after the era and alias questions are answered.')
    site('LIB10','Unbound Academy library',['O229','O230','O231'],'The Academy is founded after the Sunrise of Chosen Threads.','A proposed pre-Academy campaign needs an explicit adaptation if using this institution.')
    site('LIB11','Citadel of Many Echoes',['O237','O238','O262','O275'],'Built after the Masquerade; later hosts the Charter. Its cosmograph symbol represents a relationship between shadow and dream.','Choose current access and distinguish the historical archive from the symbolic diagram; no floor number follows.')
    site('LIB12','Silent Library',['O253','O258','O259','O260'],'Matrix interior during the Proof War approach; its books and Ledger change during that encounter.','If reused, specify whether the scene is historical, transformed, reconstructed or an explicitly authored adaptation; no option is selected here.')
    site('LIB13','Wax Library',['O307','O308','O309','O324'],'Original chamber seed appears under Dungeon Seeds after Infinite Yield; P324 permits independent/multi-era adaptation.','This qualifies the earlier library inventory: neither automatic campaign-start availability nor an absolute postwar-only ban is justified. A concrete floor, contents and adaptation still need review.')
    site('LIB14','Cantor’s Archive',['C29','Q6-CURRENT'],'Existing library inventory binds it to Floor 47 in secondary mapped setting sources, within the documented six-band scope. No supplied source ties it to an AE/Proof-War date.','Keep its mapped setting fact and its unresolved relative epoch separate. No newly assigned Equation fragment.')
    gaps=[
        {'id':'CE01','subject':'Current campaign anchor','evidenceIds':['GP-EPOCH','GP-CHRON','GP-REVEAL','C29','Q6-CURRENT'],'finding':'GPT already leaves the campaign epoch and public revelation unresolved. The current reliable-floor boundary does not select before/after the original forward saga.','nextDecision':'Agree one named current Opening’s relation to the relevant original events, retaining explicit unknown intervals rather than dating every cosmic age.'},
        {'id':'CE02','subject':'Primordial ages, mortal years and work clocks','evidenceIds':['HC02-02','O23','O198','W52','W91','W92','W93'],'finding':'Owner primordial Cycles are qualitative ages; Silver Prism Year is explicitly elastic; the World extract separately states a 400-day mortal year and ten-year rotation. These are not interchangeable units.','nextDecision':'Label each timeline unit and define only the bridges actually wanted for the campaign. Do not convert twenty primordial cycles into two hundred mortal years.'},
        {'id':'CE03','subject':'87 AE to 710 AE cadence tension','evidenceIds':['W52','W80','W81','W82','W83','W84','MAIN-TIMELINE','RB-TIMELINE','MAIN-ROTATION','RB-ROTATION'],'finding':'The dates differ by623years. Under the additional assumption of one uninterrupted ten-year rotation measured from the87AEFirstCycle in the same calendar,710AE is not on that cadence (remainder3). The selected sources do not supply the missing calendar/event bridge.','nextDecision':'Discuss a supported date correction, epoch/calendar discontinuity, different event meaning or other explicit explanation. Choose none by inference and preserve both original dates.'},
        {'id':'CE04','subject':'World history versus source sequence and Q6','evidenceIds':['W5','W7','W9','W80','W81','W83','Q6-CURRENT','Q6-QUALIFICATION'],'finding':'The World outline lists Binding before FirstCycle, while its dated appendix places the666AE imprisonment after87AEFirstCycle. Bullet order alone does not prove a causal chronology. Q6 separately qualifies the public reliability of Binding and leaves entity identities open.','nextDecision':'Keep these as distinct source assertions. Do not identify World FirstLight with a specific original FirstSong moment or merge eleventh shard, survivor, Ulnak and OldGod to force agreement.'},
        {'id':'CE05','subject':'Crystal identity and narrative victory','evidenceIds':['O260','O261','O262','Q6-CURRENT'],'finding':'The original Shard of Absolute Rest is shattered and the dream recedes. Q6’s Floor100 confrontation produces or exposes a focusing crystal needed for vulnerability. Similar materials do not establish sameness.','nextDecision':'Retain distinct object records until explicit evidence or owner/GPT decision supplies a relationship; no guaranteed drop, completed kill or no-future-danger inference.'},
        {'id':'CE06','subject':'Epilogue portability versus adoption','evidenceIds':['O276','O280','O283','O287','O288','O293','O298','O309','O313','O314','O315','O316','O324','GP-EPI'],'finding':'The original permits adapting its toolbox. Existing GPT review preserves17EPIgroups but leaves mechanics/balance/epoch decisions open. That permission is important but does not itself resolve actions, units, class gates, fatigue, rest resets, hazard types or modern taint interactions.','nextDecision':'Use the established EPI IDs for targeted operating proposals. Do not create a competing epilogue inventory or silently apply motif time-halving, NullVeil cures or borrowed class features to the current candidate.'},
        {'id':'CE07','subject':'Website and candidate source timeline','evidenceIds':['MAIN-TIMELINE','RB-TIMELINE','MAIN-BINDING','RB-BINDING','RB-UI','Q6-CURRENT'],'finding':'Both source JSONs retain the same eight timeline strings and explicit Level97Binding prose. The inspected ReviewBible DungeonGuide source directly renders mythHistory and timeline under Myth & Timeline. This is static source evidence, not a rendered-site or release-build test.','nextDecision':'When applying the public-reliability scrub, inspect the actual export/runtime path and qualify claims at their reader-visible location. Do not treat these copies as independent historical witnesses or proof the current released UI has been tested.'},
        {'id':'CE08','subject':'Choir timing and chorus count','evidenceIds':['HC02-03','O27','O33','O34','O35','O39','O279','O280','GP-EPI'],'finding':'Owner intent and original formation/assault order remain an explicit seam. The epilogue says nine verses while its motif table enumerates seven virtues; this does not authorize inventing an eighth virtue, mapping every Harmony, or silently editing the verse count.','nextDecision':'Carry the existing gods/Choir open issue into a focused chronology decision with exact text. Do not use a count correction to establish new entity identity.'},
    ]
    examples=[
        ('CT01','A Director places the Wax Library before the Proof War.','Original P324 allows independent or multi-era adaptation, so do not reject it solely because of its heading. Label the adaptation and choose its placement/content explicitly; the old seed supplies no Equation fragment.',['O307','O309','O324']),
        ('CT02','A party opens a current-campaign map and sees the Citadel symbol between coils two and three.','This is a cosmological relationship, not proof that the archive occupies Floor2or3. Current access and the selected epoch remain separate.',['O270','O275']),
        ('CT03','The source’s postwar victory is treated as proof that the Floor97OldGod is already dead.','The original says Ulnak’s dream recedes, and Q6identity remains unresolved. Do not erase the endgame threat or merge objects/entities by analogy.',['O262','Q6-CURRENT']),
        ('CT04','The timeline’s710AEcurrentCycle is used to backdate the Proof War exactly.','No selected source maps the War to AE. Keep710as its source claim and the War’s relative sequence separately.',['W84','GP-EPOCH']),
        ('CT05','Twenty primordial Cycles are converted to200mortal years.','Owner primordial Cycles mean ages without a fixed calendar conversion; a separate ten-year mortal rotation does not define them.',['HC02-02','W52']),
        ('CT06','The Transition motif is used to halve an eight-hour Equation decipher project immediately.','The effect exists in the preserved epilogue, but its current operational adoption remains open underGPR06. It is not already an exception to the reviewed language procedure.',['O280','GP-EPI']),
        ('CT07','Silent Library is reused after its described encounter as shelves of permanently unwritten books.','Preserve the narrated stabilization of books and the blanked Ledger, or identify the new treatment as an explicit adaptation needing review.',['O258','O259','O324']),
        ('CT08','A repeated website timeline is offered as independent corroboration of the87/710dates.','Both JSONs carry the same source-derived strings. Preserve copies but count provenance honestly; repetition does not resolve the calendar tension.',['W81','W84','MAIN-TIMELINE','RB-TIMELINE']),
    ]
    cases=[{'id':i,'situation':s,'expectedDiscussionBoundary':o,'evidenceIds':refs,'runtimeOrHumanTest':False} for i,s,o,refs in examples]
    for row in events+sites+gaps+cases:assert all(x in evidence for x in row['evidenceIds'])
    assert 710-87==623 and (710-87)%10==3
    timeline_equal=evidence['MAIN-TIMELINE']['value']==evidence['RB-TIMELINE']['value'];assert timeline_equal
    result={'reviewId':'COSMOLOGY-CHRONOLOGY-RESEARCH-SITES-DRAFT-01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
        'status':'Local chronology/source reconciliation draft; unsubmitted; no dates, identities, rules or public claims changed',
        'authority':'Original source content, explicit owner corrections and already-reviewed scope decisions are separately identified. This extends GP-U14/GPR06/GPR08; it does not reopen settled original-source preference.',
        'sourceBindings':list(bindings.values()),'evidenceLocations':list(evidence.values()),'contextArtifacts':context,'printedChapterOrder':chapter_order,'relativeEvents':events,'researchSitePlacement':sites,'openIssues':gaps,'reviewSituations':cases,
        'existingEpilogueInventory':{'artifact':info(epi),'groups':review_units,'idAndTitleCrosscheck':True,'newCompetingInventoryCreated':False},
        'calendarCheck':{'startClaimAE':87,'currentClaimAE':710,'differenceYears':623,'statedRotationYears':10,'remainder':3,'conditionalAssumption':'same uninterrupted fixed cadence and calendar measured from the FirstCycle claim','resolutionSelected':False},
        'runtimeTimelineComparison':{'mainAndReviewBibleSourceArraysEqual':timeline_equal,'arrayEntries':len(evidence['RB-TIMELINE']['value']),'staticComponentRead':True,'renderedBrowserOrPublishedBuildVerified':False},
        'libraryInventoryQualification':'LIB13WaxLibrary is explicitly framed afterInfiniteYield inO307, whileO324permits independent/multi-era adaptation. Preserve both facts; no automatic current placement and no unsupported absolute era restriction.',
        'currentCampaignEpochChosen':False,'sourceDatesEdited':False,'entityIdentityMerged':False,'epilogueRulesAdopted':False,'newRulesAdopted':False,'sourceInformationDeleted':0,'publicExportEnabled':False,'runtimeApproved':False,'fullCosmologyApproved':False,
        'jointReviewStatus':'ExistingPart3choice pending afterPart2terminal conversation-length limit. No new GPT verdict; frozen planes packet unchanged.',
        'coverageLimit':'Selected full paragraphs and objects only. Printed chapter order is not a claim to have solved every transition. Source-code rendering evidence is not runtime or publication validation.'}
    target.write_bytes(encoded(result))
    lines=['# Cosmology chronology and research-site availability','',
        'Director discussion draft · extends GP-U14, GPR-06 and GPR-08 · not a chosen campaign epoch','',
        'The original contains a forward saga, a successful Proof War and an explicitly postwar workbook. It also expressly permits its tables and relics to be adapted independently of that saga. Existing GPT review already preserves both source content and the unresolved campaign-epoch/mechanics decision. This document connects that decision to the actual research sites, dates and current revelation boundary.','',
        'The [Heartcell owner corrections](HEARTCELL_OWNER_UPDATE_02.md) and [Q6 companion](Q6_LATER_LOCK_REVIEWED_01.md) remain controlling in their respective scopes. No original date, passage or rules text is changed.','',
        '## Relative sequence in the original','',
        'These entries describe the text’s relative order. They do not assign current campaign dates. The First Choir seam is explicitly unresolved.','']
    for x in events:lines += [f"### {x['id']} — {x['title']}",'',x['sourceFinding'],'',f"**Campaign boundary:** {x['currentCampaignLimit']}",'',f"Evidence: {', '.join(x['evidenceIds'])}.",'']
    lines += ['## Research-site placement','',
        'Use these as qualifications to the [existing library inventory](EQUATION_LIBRARY_SOURCE_INVENTORY_01.md), not a replacement set of sites. In particular, **Wax Library has both an original post-Infinite-Yield setting and explicit permission for adaptation**. Neither fact alone supplies its present floor or an Equation fragment.','']
    for x in sites:lines += [f"**{x['libraryRecordId']} — {x['name']}**",'',x['sourcePlacement'],'',x['remainingPlacementDecision'],'',f"Evidence: {', '.join(x['evidenceIds'])}.",'']
    lines += ['## Decisions still needed','']
    for x in gaps:lines += [f"### {x['id']} — {x['subject']}",'',x['finding'],'',f"**Next joint decision:** {x['nextDecision']}",'',f"Evidence: {', '.join(x['evidenceIds'])}.",'']
    lines += ['## Preserve the existing epilogue inventory','',
        'The [original seventeen-group inventory](../../../../../docs/audit/2026-10-08/full-game/ORIGINAL_COSMOLOGY_EPILOGUE_RULE_INVENTORY_01.json) and GPR-06 use matching IDs and titles. Reuse those records for subsequent operating proposals. This draft creates no competing EPI numbering and activates none of their effects.','',
        '| Existing ID | Source group |','|---|---|']
    for x in review_units:lines.append(f"| {x['id']} | {x['title']} |")
    lines += ['','## Eight review situations','',
        'These are authored discussion checks, not human playtests or software behavior tests.','']
    for x in cases:lines += [f"**{x['id']} — {x['situation']}**",'',x['expectedDiscussionBoundary'],'']
    lines += ['## Evidence and limits','',
        'The [structured source record](../../../data/director/cosmology/chronology_research_sites_draft_01.json) includes the selected original paragraphs, current owner/GPT scope records, timeline arrays and the actual source component excerpt. All locations are checked against current bytes. The 623-year/remainder-3 calculation is conditional on an uninterrupted shared ten-year cadence; it does not prove which date or rule should change.','',
        'The Main and ReviewBible source timeline arrays match. DungeonGuide source renders those records under Myth & Timeline; no browser rendering, shipping export or public-release behavior was tested in this pass. Future public qualification must inspect the real delivery path.','',
        'No current epoch, library relocation, crystal identity, Choir mapping, taint model or epilogue rule was adopted. The previously requested Part 3 choice remains pending; this draft has not been submitted to GPT.','']
    chapter.write_text('\n'.join(lines),encoding='utf-8',newline='\n')
    # Independently re-resolve each saved source location.
    jc={};lc={}
    for row in bindings.values():assert info(G/row['path'])==row
    for item in evidence.values():
        p=G/item['path']
        if 'paragraphIndexZeroBased' in item:
            v=docx_text[p][item['paragraphIndexZeroBased']];assert v==item['text'] and hashlib.sha256(v.encode()).hexdigest()==item['textSha256']
        elif 'jsonPointer' in item:
            if p not in jc:jc[p]=read(p)
            v=jc[p]
            for t in item['jsonPointer'].strip('/').split('/'):
                t=t.replace('~1','/').replace('~0','~');v=v[int(t)] if isinstance(v,list) else v[t]
            assert v==item['value']
        else:
            if p not in lc:lc[p]=p.read_text(encoding='utf-8-sig').splitlines()
            v='\n'.join(lc[p][item['firstLineOneBased']-1:item['lastLineOneBased']]);assert v==item['text'] and hashlib.sha256(v.encode()).hexdigest()==item['textSha256']
    for row in context:assert info(G/row['path'])==row
    assert len(events)==16 and len(sites)==9 and len(gaps)==8 and len(cases)==8
    check.write_bytes(encoded({'draft':info(target),'chapter':info(chapter),'sourceBindingsVerified':len(bindings),'exactEvidenceLocationsVerified':len(evidence),'docxParagraphs':sum('paragraphIndexZeroBased' in x for x in evidence.values()),'jsonObjects':sum('jsonPointer' in x for x in evidence.values()),'textSections':sum('firstLineOneBased' in x for x in evidence.values()),'relativeEvents':16,'siteQualifications':9,'openIssues':8,'reviewSituations':8,'existingEpiIdsAndTitlesMatched':17,'calendarArithmeticChecked':True,'newDatesOrRulesAdopted':False,'sourceInformationDeleted':0,'renderedRuntimeTest':False}))
    print(json.dumps(read(check)))


if __name__=='__main__':main()
