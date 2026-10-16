"""Prepare a source-bound research worksheet; do not adopt Equation mechanics."""
from datetime import datetime, timezone
from zipfile import ZipFile
from xml.etree import ElementTree as E
import hashlib, json
from apply_di7_ap_as_01 import G, R, A, info, encoded


def read(p): return json.loads(p.read_bytes())


def main():
    target=R/'data/director/cosmology/equation_research_interface_draft_01.json'
    chapter=R/'docs/director-only/cosmology/EQUATION_RESEARCH_INTERFACE_DRAFT_01.md'
    check=A/'COSMOLOGY_EQUATION_RESEARCH_INTERFACE_DRAFT_01_CHECK.json'
    assert all(not p.exists() for p in [target,chapter,check])
    bindings={}; evidence={}
    def bind(p):
        row=info(p); bindings[row['path']]=row; return row['path']
    def obj(key,p,ptr):
        path=bind(p); value=read(p)
        for token in ptr.strip('/').split('/'):
            token=token.replace('~1','/').replace('~0','~');value=value[int(token)] if isinstance(value,list) else value[token]
        evidence[key]={'id':key,'path':path,'jsonPointer':ptr,'value':value}
    def md(key,p,lo,hi):
        path=bind(p); lines=p.read_text(encoding='utf-8-sig').splitlines();assert hi<=len(lines)
        text='\n'.join(lines[lo-1:hi]); evidence[key]={'id':key,'path':path,'firstLineOneBased':lo,'lastLineOneBased':hi,'text':text,'textSha256':hashlib.sha256(text.encode()).hexdigest()}
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    for prefix,p,inds in [
        ('C',G/'books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx',[1301,1302]+list(range(8338,8355))),
        ('P',G/'books/player/Decennium_Descent_Player_Rulebook_v6.docx',list(range(5539,5544))),
        ('D',G/'docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx',list(range(1753,1761))+[1769,1770]),
    ]:
        path=bind(p)
        with ZipFile(p) as z:root=E.fromstring(z.read('word/document.xml'))
        ps=[''.join(t.text or '' for t in x.findall('.//w:t',ns)) for x in root.findall('.//w:p',ns)]
        for i in inds:evidence[f'{prefix}{i}']={'id':f'{prefix}{i}','path':path,'part':'word/document.xml','paragraphIndexZeroBased':i,'text':ps[i],'textSha256':hashlib.sha256(ps[i].encode()).hexdigest()}
    guide=R/'docs/mechanics/LANGUAGE_COMMUNICATION_PLAYTEST.md'
    for key,lo,hi in [('L-MODES',59,75),('L-LEARN',77,99),('L-DECIPHER',101,123),('L-MAGIC',148,165),('L-ORACLE',169,177),('L-SCRIBING',190,202)]:md(key,guide,lo,hi)
    md('SKILLS',R/'docs/mechanics/CHARACTER_FOUNDATION_TABLES.md',111,121)
    md('TRAINING',R/'docs/mechanics/CHARACTER_CREATION_PLAYTEST.md',20,34)
    md('TASK',R/'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md',23,33)
    language=R/'data/playtest/language_communication_candidate_public.json'
    for key,ptr in [('L-TRANSLATE','/rules/ordinaryTranslation'),('L-RECOGNIZE','/rules/recognition'),('L-PROJECT','/rules/decipherProject'),('L-INSIGHT','/rules/scribingInsight'),('L-COMPREHEND','/spellInterfaces/1'),('L-TONGUES','/classInterfaces/13'),('L-TONGUES-I','/classInterfaces/14'),('L-TRANSFER','/classInterfaces/46')]:obj(key,language,ptr)
    obj('KT',R/'data/public/class_playtests/wizard.json','/cards/31')
    obj('COMPREHEND-STATUS',R/'data/public/spell_playtests/authored_review_index.json','/entries/223')
    assert evidence['COMPREHEND-STATUS']['value']['authoredStatus']=='reviewed-authored-operational-playtest'
    for key,part,ptr in [('TEAM',1,'/publicEnvelope/sections/1'),('CLOCK',1,'/publicEnvelope/sections/2'),('CLOCK-D',1,'/directorModule/sections/2'),('HAVEN',3,'/publicEnvelope/sections/5'),('HAVEN-D',3,'/directorModule/sections/5')]:
        obj(key,R/f'data/director/expedition_candidate/part{part:02d}.json',ptr)
    for i in [0,4,5]:obj(f'HC02-{i+1:02d}',R/'data/director/cosmology/heartcell_owner_update_02.json',f'/decisions/{i}')
    status_path=R/'docs/mechanics/LANGUAGE_REVIEW_STATUS.json';receipt_path=A/'LANGUAGE_EXACT_FULFILLMENT.json'
    bind(status_path);bind(receipt_path);status=read(status_path);receipt=read(receipt_path)
    assert hashlib.sha256(receipt_path.read_bytes()).hexdigest()==status['fulfillmentSha256']
    assert status['exactLanguageApproval'] and receipt['exactLanguageApproval']
    language_hashes=[]
    for name,sha in status['finalHashes'].items():
        p=G/name;assert info(p)['sha256']==sha;language_hashes.append(info(p))
    library=R/'data/director/cosmology/equation_library_source_inventory_01.json'
    souls=R/'data/director/cosmology/souls_death_hunt_conference_draft_01.json'
    context=[info(library),info(souls)]
    sections=[]
    def section(n,title,refs,existing,proposal,gaps):
        sections.append({'id':f'ER{n:02d}','title':title,'evidenceIds':refs,'existingSourceBoundary':existing,'proposalNotAdopted':proposal,'requiresJointDecision':gaps})
    section(1,'Research is an activity; its Equation qualification is still missing',['SKILLS','TRAINING','P5539','P5540','P5541','P5542','P5543','C1301','C1302','TEAM','HC02-05'],
        'The reviewed character foundation has 20 basic skills, including the five Core disciplines, but no separate Research skill. Research is an Expedition team. Core requires the primary Matrix researcher personally to possess high ranks in Arcana, History, Religion, Nature and Engineering; no numerical interpretation is supplied by the selected passage.',
        'Use Research as the project heading and record each actual subject skill independently. Preserve the owner’s wording and the personal multidisciplinary requirement as an explicit unresolved interface. Ordinary translation remains usable under its own rules while overall Equation eligibility is unresolved.',
        'Choose the exact mapping of owner Research skill to current character mechanics, what high ranks means, and which stage requires it. Do not silently add a twenty-first skill, equate craft ranks to basic skills, or replace personal qualification with five different specialists.')
    section(2,'Register the actual evidence before adjudication',['L-DECIPHER','L-PROJECT','D1756','D1757','D1758','C1302'],
        'Reviewed deciphering requires an accessible finite passage, genuine supporting evidence, declared output and missing sections. Original Director guidance proposes multiple source types; Core also names rare drops, libraries, mechanisms and seasonal change.',
        'Give every physical source and underlying evidence identity separate IDs. Record its site, custody, version, raw visible symbols, actual source meaning, missing material, languages/scripts, cipher or protection, corroborating sources and provenance. Preserve observations, quotations, translations and interpretations as different fields. A genuinely changed living text gets a version entry and the observed change, without pretending every copy is independent.',
        'Author real clues and their supported meanings, a dependency graph and recovery leads. Determine which nonlibrary evidence is needed in addition to the owner-required multiple Descent libraries; no number of fragments is selected here.')
    section(3,'Let language tools complete their real work',['L-MODES','L-TRANSLATE','L-RECOGNIZE','L-PROJECT','L-COMPREHEND','COMPREHEND-STATUS','L-LEARN'],
        'Known plain prose translates at ten active minutes per 250 words, proportionately rounded up to a whole minute, minimum one. Recognition identifies a supported language/style, not meaning. The separate supported decipher project allows at most 250 words, eight active hours, INT/History for language or INT/Investigation for a mundane cipher, with its actual DC and retry requirements. Comprehend Languages grants literal eligible understanding within its real perception/concentration limits and excludes ciphers, protected meanings and glyph functions.',
        'Declare the task layer: copying, recognizing, plain translation, linguistic reconstruction, mundane cipher, technical interpretation, theorem synthesis, or actual magical execution. Use the existing procedure only for the layer it covers. Put a real ordinary-language sentence in a clue when an ordinary language effect should reveal it; do not retroactively relabel every difficult passage a secret cipher after a player uses a valid ability.',
        'Choose actual clue language, protection and technical structure before play. The eight-hour language project is not automatically the time required to understand the whole Equation, and an unsupported interpretation cannot be recovered by a high roll.')
    section(4,'Assistance and bonuses keep their actual scope',['TEAM','L-PROJECT','TRAINING','L-ORACLE','L-TONGUES-I','KT','L-TRANSFER'],
        'Generic expedition tasks allow up to three trained meaningful assistants at +1 each; the specific language decipher project allows one qualified assistant at +1 after the full eight hours. PB contributes once, with actual Expertise modifying that contribution only. Oracle Tongues I has a related-check interpretation bonus and actual hearing/range requirements. Knowledge Transfer can loan one actual skill proficiency for an hour, never Expertise, memories or secrets.',
        'Record who provides which benefit, its real duration and why its trigger is met. Apply a borrowed skill to eligible ordinary checks while actually in effect. Do not claim it transfers an Equation secret, permanent study or every prerequisite. Do not add generic expedition assistant bonuses on top of the specific language project allowance.',
        'Decide whether and when borrowed proficiency qualifies toward the Core personal high-rank requirement, and whether that requirement must be maintained during work or only at a declared test. The inventory does not erase a lawful skill loan or assume that a one-hour loan lasts an eight-hour project.')
    section(5,'Copying, comprehension and functional understanding are different records',['HC02-05','L-MODES','L-DECIPHER','L-SCRIBING','L-TRANSFER','KT','C1302'],
        'The owner ties knowledge taint to functional Equation understanding and separately allows proximity/voices to taint. The reviewed language chapter preserves particular information learned through temporary magic after general competence expires. Knowledge Transfer does not convey memories or secrets. Core distinguishes inherited archives from cognitive continuity.',
        'For each person, record what they actually perceived, which literal meaning they learned, which interpretation they can justify, when they first demonstrated any agreed functional understanding, and the supporting evidence. Knowledge delivery needs a real channel and time. Language comprehension does not by itself certify a complete theorem. Do not erase remembered information when a spell expires.',
        'Define the functional-understanding threshold and its observable demonstration, whether particular literal statements can themselves cross it, what assistance or explanation transmits, and the exact taint consequences. Do not default to either automatic contamination from any copied symbol or blanket safety from an unread-looking page.')
    section(6,'Resolve real work on one clock',['CLOCK','CLOCK-D','HAVEN','HAVEN-D','L-LEARN','L-SCRIBING','L-INSIGHT'],
        'The Expedition uses one elapsed clock, eight-hour Watches, two productive-work Watches and a scheduled Rest Watch. Parallel teams do not add elapsed time twice. Exact language phases and decipher work retain their own interruption rules. A Haven supplies no teacher, stock, access or safe berth by name. Language Insight uses its own researcher/language ledger, one point per qualifying evidence hour, cap six, and three points plus eight separate hours for one supported passage.',
        'Log start/end, active credited work, elapsed interruption, assistants, payments and source access. Keep guarding, interpreting, casting and study separate when incompatible. Record Language Insight separately from the Insight skill, Equation understanding and taint. Use real facility/provider records rather than assuming a newly named library supplies everything.',
        'Specify Equation-specific work durations, interruptions, exposure while working, applicable materials and any unusual facility requirement. Existing course, spell, clock and reference-item rules remain intact; this draft supplies no new universal research discount or bonus.')
    section(7,'Failure preserves information honestly',['L-PROJECT','TASK','D1769','D1770','D1758','D1760','HC02-05','HC02-06'],
        'Reviewed language project failure spends real work and leaves notes without a certified translation. Critical failure adds only an independently lawful predeclared hazard. No failure fabricates authoritative lore. Earlier generic Director guidance suggests partial answers, false confidence, damage, attention or new sources; those suggestions do not override the specific reviewed language result.',
        'Predeclare the actual result scope and any independent material/exposure hazard. If characters hold a mistaken hypothesis, label its evidential basis and preserve the distinction from the Director’s source truth. A failed roll may leave a concrete new lead only if the scene actually supplies one; no automatic fabricated translation. Keep a route back to missing evidence without promising completion of forbidden research.',
        'Agree any new Equation failure consequences and how discoveries can be recovered after material loss. Attention, taint and an active Hunt need their own triggers; they are not interchangeable critical-failure labels.')
    section(8,'Functional demonstration must be playable',['C1302','HC02-05','L-PROJECT','D1759'],
        'Existing language outcomes establish bounded meaning, while the owner requires difficult research culminating in functional knowledge. No complete proof or progression algorithm is supplied by the selected sources.',
        'Prepare a Director rubric containing the actual relation to establish, relevant evidence, a finite prediction or interpretation that distinguishes competing hypotheses, and what feedback can be observed. Let character competence and declared choices resolve the attempt under the eventual procedure. The player need not personally know advanced mathematics, perform a voice or read the fictional script. Keep asking which claim the character is testing and what evidence supports it.',
        'Write the real rubric, exact character prerequisites, costs and resolution. A proposed demonstration is not automatically harmless, a cast, a complete Equation or permission to alter the Matrix. Each needs a separate definition.')
    section(9,'Keep study distinct from execution and enforcement',['HC02-05','HC02-06','C1302','L-SCRIBING','L-MAGIC'],
        'Reading functional instructions is not itself casting access or device control. Actual class/rank/school, repertoire, RP, components and use rules remain applicable. Owner Hunt/death direction retains extremely rare Divine or Abyssal exceptions rather than an absolute intervention ban.',
        'End each study entry with separate outcomes: document changes, information learned, interpretation supported, functional-understanding status, actual taint event if defined, external attention, and whether a separately recorded Hunt has begun. Link these to the souls/Hunt draft. Keep original public knowledge boundaries in all player-facing notes.',
        'Complete the taint model, Hunt initiation criteria, pursuer knowledge/authority and exceptional intervention route through joint review before applying them to play. This worksheet changes none of those rules.')

    fields=[
        ('projectIdAndQuestion','Stable project ID; one specific question; requested output layer and completion condition.'),
        ('sourceIdentity','Physical object ID and underlying evidence ID; source file/paragraph or newly authored scene record; version and custody.'),
        ('accessAndContent','Real site and permission; observed symbols and damage; language/script/cipher/protection; actual Director meaning or explicitly missing meaning.'),
        ('provenanceAndComparison','Other documents, witnesses, mechanisms or samples; shared-copy provenance; disagreements and how they were detected.'),
        ('leadAndQualifications','Named researcher; actual ability/skill/PB/Expertise; grant source and expiration; unresolved Equation qualification clearly marked.'),
        ('helpersAndEffects','Named actual assistants; procedure-specific limit; real work; exact card effects, costs, range, hearing/access and duration.'),
        ('workAndClock','Start/end seconds; actual active work; retained/lost credit under the exact procedure; interruption; money/materials; no incompatible duplicate assignment.'),
        ('resolution','Procedure and exact source; preregistered DC and output where applicable; actual die/modifiers/result; no invented extra critical benefit.'),
        ('informationPerPerson','What was perceived and understood, when and via which channel; retained facts; interpretation, evidence and uncertainty.'),
        ('understandingAndConsequences','Separate functional-understanding determination, actual taint cause/effect, attention, Hunt record and aftermath; mark undefined rules unresolved rather than zero.'),
        ('followUpAndAudience','Remaining evidence or lawful new method; original and copied item locations; Director-only truths versus facts the characters actually learned.'),
    ]
    situations=[
        ('ERP01','A researcher knows both written languages and translates 375 words of accessible plain noncoded prose.','15 active minutes, no translation roll. The 250-word cap applies to the separate decipher/Insight projects, not to ordinary prose translation. The result does not automatically authenticate the text or solve its theorem.',['L-TRANSLATE','L-DECIPHER']),
        ('ERP02','A supported 200-word unfamiliar-language project has DC20. Lead INT+3, PB+3, one qualified assistant works all eight hours, and the d20 is13.','Total20: Success, one registered passage. Eight elapsed hours contain eight lead-hours and eight helper-hours, not sixteen world-hours. No fluency, Equation stage or taint amount is inferred.',['L-PROJECT','TASK','CLOCK']),
        ('ERP03','The same project rolls a natural20, total27.','The unshifted total is Success; natural20 shifts to Critical Success. It still supplies only the registered passage, without a second passage, bonus labor or general fluency.',['L-PROJECT','TASK']),
        ('ERP04','The same project rolls a natural1, total8, and no separate lawful hazard was predeclared.','Critical Failure after the bounded shift: real work is spent and no certified translation results. Do not invent a true-sounding false Equation, damage, automatic taint or a Hunt.',['L-PROJECT','TASK','D1770']),
        ('ERP05','Three trained helpers join that language decipher project.','Only one eligible full-work assistant supplies its +1. The generic Expedition allowance does not add two more bonuses to this specific procedure. Other people need their own actual tasks.',['L-PROJECT','TEAM']),
        ('ERP06','Comprehend Languages reads a perceivable ordinary sentence beside an encrypted technical glyph.','Apply literal eligible understanding to the sentence under the actual spell. Do not decode the cipher or glyph function. Particular information actually learned survives expiry, without granting general literacy. Whether that sentence crosses an eventual understanding threshold remains a separate question.',['L-COMPREHEND','L-DECIPHER']),
        ('ERP07','A level-eligible Spellbinder lawfully lends Engineering proficiency for one hour.','The ally can use that real skill proficiency for eligible checks while it lasts. It conveys no Expertise, memories or Equation secret, and does not last an eight-hour project by assumption. Its role in personal high-rank eligibility requires an explicit joint decision.',['KT','L-TRANSFER','C1302']),
        ('ERP08','A researcher has two Language Insight and one new authenticated useful parallel correspondence.','One qualifying active hour gives the third point; spending three plus eight separate active hours completes one supported passage: nine active hours total, zero remaining Insight. No course hours or Equation progress are automatically added.',['L-INSIGHT','L-SCRIBING']),
        ('ERP09','Two libraries hold copies of the same underlying correspondence.','Retain both objects and custody histories. The reviewed Language Insight award occurs only once per reader/evidence identity. The copies are not automatically two independent Equation discoveries; actual research progression is still to be defined.',['L-INSIGHT','L-SCRIBING']),
        ('ERP10','The character recognizes Runic letters on a damaged page but its decisive lines are absent.','Recognition or copying supplies only the actual evidence. A missing unsupported meaning makes the decipher task unqualified before work/spending; a high roll does not recover destroyed facts. Seek a real source or recoverable evidence.',['L-MODES','L-RECOGNIZE','L-PROJECT']),
        ('ERP11','A guard claims the same eight hours as full alert guard duty and full decipher assistance.','Reject incompatible double credit; schedule distinct real workers or intervals. The clock remains one shared world clock, with actual rest and work limits.',['CLOCK','TEAM','L-PROJECT']),
        ('ERP12','Five specialists each know one Core discipline, but no named lead personally satisfies the eventual full requirement.','They can perform their legal ordinary tasks, but the group does not automatically establish the Core primary-researcher qualification by pooling. The exact high-rank threshold remains unresolved, not failed or satisfied by invented arithmetic.',['C1302','TEAM','SKILLS']),
        ('ERP13','An Oracle interprets for an ally outside the actual hearing/range requirements.','No interpretation bonus reaches that check through the class interface. Real conveyed information may help only after actual delivery; source qualifications and costs remain independent.',['L-TONGUES-I','L-ORACLE']),
        ('ERP14','A translated record is inherited after a researcher dies during a Hunt.','Preserve the actual document and learned facts of surviving people. Inheritance does not transfer the deceased’s memories, qualifications or a free exception to Hunt death. Determine a successor’s own understanding and consequences under the eventual agreed rules.',['C1302','HC02-05','HC02-06','KT']),
    ]
    cases=[{'id':i,'situation':s,'expectedAuthoredAdjudication':o,'evidenceIds':refs,'isRuntimeOrHumanTest':False} for i,s,o,refs in situations]
    for row in sections+cases: assert all(x in evidence for x in row['evidenceIds'])
    # Check the finite arithmetic used in the examples, not a claim of game-runtime validation.
    assert (375*10+249)//250==15
    assert 13+3+3+1==20 and 20+3+3+1==27 and 1+3+3+1==8
    assert 60+480==540 and 2+1-3==0
    result={'reviewId':'COSMOLOGY-EQUATION-RESEARCH-INTERFACE-DRAFT-01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
        'status':'Source-bound proposed Equation interface and Director worksheet; unsubmitted and unadopted',
        'sourceBindings':list(bindings.values()),'evidenceLocations':list(evidence.values()),'contextArtifacts':context,
        'languageExactApprovalVerification':{'statusFile':info(status_path),'fulfillmentReceipt':info(receipt_path),'exactReceiptHashMatched':True,'currentFinalArtifactsMatched':language_hashes,'limitation':'This verifies the existing LAX scope only; it grants no Equation, class, spell, feat, runtime or full-game approval.'},
        'sections':sections,'worksheetFields':[{'field':k,'instruction':v} for k,v in fields],'reviewSituations':cases,
        'ordinaryLanguageRulesChanged':False,'newSkillAdded':False,'numericMatrixQualificationChosen':False,'functionalUnderstandingThresholdChosen':False,'equationFragmentsAssigned':0,'taintMechanicsAdopted':False,'newRulesAdopted':False,'sourceInformationDeleted':0,'publicExportEnabled':False,'runtimeApproved':False,'humanPlaytestConfirmed':False,'fullCosmologyApproved':False,
        'jointReviewStatus':'No new GPT verdict. Part2 terminal conversation-length limit; existing Part3 choice pending. Frozen planes packet unchanged.',
        'coverageLimit':'Only the cited exact sections/objects/paragraphs are semantically covered. Reviewed language text is not authority to activate pending effects or invent undiscovered meanings. Source directions and earlier Director suggestions remain distinct from current operational procedures.'}
    target.write_bytes(encoded(result))
    lines=['# Equation Research: language, qualifications and work','',
        'Director discussion draft · not jointly reviewed or adopted','',
        'The ordinary language and Expedition procedures already cover much of the work. The remaining Equation-specific gap is substantial: Research is a team activity rather than one of the current 20 basic skills, and the Core requirement for a primary researcher’s personal “high ranks” in five disciplines has no selected numeric interpretation here. This draft does not add a skill or silently choose that threshold.','',
        'Use the [library inventory](EQUATION_LIBRARY_SOURCE_INVENTORY_01.md), [owner decisions](HEARTCELL_OWNER_UPDATE_02.md) and [souls/Hunt draft](SOULS_DEATH_HUNT_CONFERENCE_DRAFT_01.md) together. Existing language rules remain in force within their scope; every proposed Equation extension below still needs GPT discussion.','']
    for s in sections:
        lines += [f"## {s['id']} — {s['title']}",'',f"**Existing sources:** {s['existingSourceBoundary']}",'',f"**Proposal for joint review:** {s['proposalNotAdopted']}",'',f"**Decision still required:** {s['requiresJointDecision']}",'',f"Evidence: {', '.join(s['evidenceIds'])} in the [bound source record](../../../data/director/cosmology/equation_research_interface_draft_01.json).",'']
    lines += ['## Director project worksheet','',
        'Use this to record a concrete study attempt. A blank or unresolved field is not permission to invent a result. Keep hidden source truth and character knowledge distinct.','',
        '| Record | Required information |','|---|---|']
    for k,v in fields:lines.append(f'| {k} | {v} |')
    lines += ['','## Fourteen review situations','',
        'These are hypothetical authored adjudications. They are not recovered Equation clues, runtime tests or human playtest results.','']
    for c in cases:lines += [f"### {c['id']} — {c['situation']}",'',c['expectedAuthoredAdjudication'],'',f"Evidence: {', '.join(c['evidenceIds'])}.",'']
    lines += ['## Validation and review status','',
        'The saved LAX exact-approval receipt and all seven listed final artifacts still match their recorded hashes. That proves the cited language candidate has not drifted from its exact-reviewed version; it does not approve these new cosmology interfaces. Every embedded source location is checked against its current file. Arithmetic checks cover only the stated example calculations.','',
        'No source text, ordinary rule, selected spell, class card or runtime data was changed. The existing Part 3 continuation choice remains pending. This draft is prepared for the next appropriate joint conference after the planes review.','']
    chapter.write_text('\n'.join(lines),encoding='utf-8',newline='\n')
    # Verify actual saved locations against current sources.
    docx_cache={};json_cache={};line_cache={}
    for row in bindings.values():assert info(G/row['path'])==row
    for item in evidence.values():
        p=G/item['path']
        if 'paragraphIndexZeroBased' in item:
            if p not in docx_cache:
                with ZipFile(p) as z:root=E.fromstring(z.read(item['part']))
                docx_cache[p]=[''.join(t.text or '' for t in q.findall('.//w:t',ns)) for q in root.findall('.//w:p',ns)]
            actual=docx_cache[p][item['paragraphIndexZeroBased']];assert actual==item['text'] and hashlib.sha256(actual.encode()).hexdigest()==item['textSha256']
        elif 'jsonPointer' in item:
            if p not in json_cache:json_cache[p]=read(p)
            actual=json_cache[p]
            for token in item['jsonPointer'].strip('/').split('/'):
                token=token.replace('~1','/').replace('~0','~');actual=actual[int(token)] if isinstance(actual,list) else actual[token]
            assert actual==item['value']
        else:
            if p not in line_cache:line_cache[p]=p.read_text(encoding='utf-8-sig').splitlines()
            actual='\n'.join(line_cache[p][item['firstLineOneBased']-1:item['lastLineOneBased']]);assert actual==item['text'] and hashlib.sha256(actual.encode()).hexdigest()==item['textSha256']
    for row in context:assert info(G/row['path'])==row
    assert len(sections)==9 and len(cases)==14 and len(fields)==11
    check.write_bytes(encoded({'draft':info(target),'chapter':info(chapter),'sourceBindingsVerified':len(bindings),'exactEvidenceLocationsVerified':len(evidence),'docxParagraphs':sum('paragraphIndexZeroBased' in x for x in evidence.values()),'jsonObjects':sum('jsonPointer' in x for x in evidence.values()),'markdownSections':sum('firstLineOneBased' in x for x in evidence.values()),'existingLanguageReceiptVerified':True,'existingLanguageFinalHashesVerified':7,'sections':9,'worksheetFields':11,'reviewSituations':14,'exampleArithmeticChecked':True,'runtimeTest':False,'newRulesAdopted':False,'sourceInformationDeleted':0}))
    print(json.dumps(read(check)))


if __name__=='__main__':main()
