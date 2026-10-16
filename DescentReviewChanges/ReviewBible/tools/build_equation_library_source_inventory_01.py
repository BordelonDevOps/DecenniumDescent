"""Inventory existing research settings without assigning Equation fragments or adopting rules."""
from datetime import datetime, timezone
from zipfile import ZipFile
from xml.etree import ElementTree as E
import hashlib, json
from apply_di7_ap_as_01 import G, R, A, info, encoded


def main():
    target = R/'data/director/cosmology/equation_library_source_inventory_01.json'
    chapter = R/'docs/director-only/cosmology/EQUATION_LIBRARY_SOURCE_INVENTORY_01.md'
    check = A/'COSMOLOGY_EQUATION_LIBRARY_SOURCE_INVENTORY_01_CHECK.json'
    assert all(not p.exists() for p in [target, chapter, check])
    bindings = {}; evidence = {}; discovery = []
    ns = {'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    def bind(p):
        row = info(p); bindings[row['path']] = row; return row['path']
    def add(key, row):
        assert key not in evidence
        evidence[key] = {'id': key, **row}
    originals = [63,65,67,69,71,105,106,107,128,129,130,165,166,183,184,185,196,197,198,228,229,230,231,236,237,238,252,253,254,255,256,257,258,259,273,274,275,308,309]
    selections = [
        ('O', 'The Cosmology of Decennium Descent.docx', originals),
        ('M', 'The Decennium Descent and the Matrix of Oblivion.docx', []),
        ('W', 'The_World_of_Aethel_Lore.docx', [23,24,25,26,27,28]),
        ('P', 'books/player/Decennium_Descent_Player_Rulebook_v6.docx', [223,228,231,5375,5376,5377,5378]+list(range(10367,10376))+list(range(10432,10442))),
        ('D', 'docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx', list(range(120,127))+list(range(2149,2158))+list(range(2353,2360))),
        ('C', 'books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx', list(range(1299,1306))+list(range(8760,8770))),
    ]
    for prefix, name, indices in selections:
        p = G/name; path = bind(p)
        with ZipFile(p) as z: root = E.fromstring(z.read('word/document.xml'))
        ps = [''.join(t.text or '' for t in x.findall('.//w:t', ns)) for x in root.findall('.//w:p',ns)]
        hits = [i for i, t in enumerate(ps) if __import__('re').search(r'\blibrar\w*\b|\barchive\w*\b|\bscriptor\w*\b',t,__import__('re').I)]
        discovery.append({'path':path,'query':'library/libraries/archive/archives/scriptor* word stems, case-insensitive','paragraphCount':len(ps),'hitParagraphs':hits,'semanticCoverage':'Only the complete paragraphs in evidenceLocations are claimed read; hits alone are discovery.'})
        for i in indices:
            add(f'{prefix}{i}', {'path':path,'part':'word/document.xml','paragraphIndexZeroBased':i,'text':ps[i],'textSha256':hashlib.sha256(ps[i].encode()).hexdigest()})
    def obj(key, name, ptr):
        p = G/name; path = bind(p); value = json.loads(p.read_text(encoding='utf-8-sig'))
        for token in ptr.strip('/').split('/'):
            token = token.replace('~1','/').replace('~0','~')
            value = value[int(token)] if isinstance(value,list) else value[token]
        add(key, {'path':path,'jsonPointer':ptr,'value':value})
    obj('F47','src/data/floor-encounters.json','/tiers/4/safeHavens/1')
    obj('TK-META','src/data/t1-5-encounter-toolkit.json','/meta')
    obj('TK47','src/data/t1-5-encounter-toolkit.json','/tiers/4/encounterCards/5')
    obj('TK44','src/data/t1-5-encounter-toolkit.json','/tiers/4/sampleRosters/1')
    owner = (R/'data/director/cosmology/heartcell_owner_update_02.json').relative_to(G).as_posix()
    for i in range(6): obj(f'HC02-{i+1:02d}',owner,f'/decisions/{i}')
    p = G/'docs/manuals/Chronicle_of_the_Decennial_Opening.md'; path = bind(p)
    lines = p.read_text(encoding='utf-8-sig').splitlines()
    for key, lo, hi in [('GZ-INTRO',1,26),('GZ-HAVENS',195,214),('GZ-LANG',279,290),('GZ-T5',442,465)]:
        text = '\n'.join(lines[lo-1:hi])
        add(key, {'path':path,'firstLineOneBased':lo,'lastLineOneBased':hi,'text':text,'textSha256':hashlib.sha256(text.encode()).hexdigest()})

    records = []
    def site(n, name, kind, sources, fact, location, clue, gap, caution):
        records.append({'id':f'LIB{n:02d}','name':name,'recordKind':kind,'evidenceIds':sources,'sourceFinding':fact,'locationEvidence':location,'candidateResearchUseNotAdopted':clue,'unresolved':gap,'doNotInfer':caution,'containsAssignedEquationFragment':False,'jointlyReviewed':False})
    site(1,'Boundless Void — library analogy','original cosmic realm, not a named building',['O67','O69','O274'],
         'The fourth realm is compared to a library without walls; reasoning evolves under Pattern, Law and Contradiction.',
         'A pillar realm. Mirroring of cosmic exchanges in dungeon chambers is described separately.',
         'A source of themes for competing interpretations, if a later agreed research site uses them.',
         'No literal shelf, local entrance, floor or Equation clue is assigned.',
         'A metaphor is not a mapped Descent library; mirroring does not identify a particular room or passage.')
    site(2,'Whispering Archive','original tributary realm',['O71'],
         'An endless shelf of sealed memories questioning their own veracity, between Shadow and Thought, with lesser-spirit custodians.',
         'A tributary realm; no numbered Descent floor.',
         'A possible source of conflicting testimony or provenance questions.',
         'No access route, clue inventory or local counterpart is established.',
         'Do not equate it with the Void Archives or turn it into a dungeon room by name alone.')
    site(3,'Mirrorsage monastery library','original unnamed gate site',['O105','O106','O107'],
         'One of the seven aspirant gates appears in a monastery library; its gate admits seekers who embrace uncertainty.',
         'The gate leads toward the deep Dungeon throne hall. The monastery itself is not located by floor.',
         'A possible teaching or interpretive tradition.',
         'The monastery name, location, current availability and any relevant records are absent.',
         'The narrative gate criterion is not a complete present-day travel ability or proof the monastery lies inside the Descent.')
    site(4,'Mephistopheles’s decaying libraries','original infernal collections',['O128','O166'],
         'Parchment blossoms rewrite into apologies; Asmodeus obtains information about the Pact directive from these libraries, and the dukes debate exploiting it.',
         'Infernal context; these passages do not fix the library address or a Descent floor.',
         'A possible biased comparative source about Pact theory.',
         'The actual stolen document, access terms, knowledge reliability and present holdings are unspecified.',
         'Pact information is not automatically the Equation of Oblivion; dialogue about formulas is not the recovered playable formula.')
    site(5,'Ellide’s ancestral archive','original unnamed mortal library',['O129','O130'],
         'Ellide sees herself restoring the archive she shattered and returns home to rebuild it with community help.',
         'Her unnamed home; the vision occurs at Hearth Embers. Those locations must not be silently merged.',
         'A model for repairing damaged evidence with witnesses.',
         'No archive name, holdings, Descent location or Equation connection.',
         'A restoration story does not supply an accessible puzzle library.')
    site(6,'Oath Archive','original named archon site',['O184'],
         'Valcendyr creates living contracts that revise with underlying intention; commitments are visible in gemstone veins.',
         'Inside Crystal Bastion, as expressly named in the passage.',
         'A possible comparator for changing intention and written records.',
         'No Equation manuscript or numbered-floor placement.',
         'Do not silently equate Crystal Bastion with Bastion of Flame or convert oath records into a universal truth oracle.')
    site(7,'Library of Shifting Sigils','original named archon site',['O185'],
         'Quorilith establishes pages that rewrite as the reader learns; tactical manuals change when motive shifts from defense to conquest.',
         'No exact location is stated in the passage.',
         'A possible inspiration for version-sensitive evidence and meaning that depends on the reader.',
         'No fixed location, exact text, Equation holding or access procedure.',
         'Not proven identical to Sigil Navigators Library. Rewriting is not permission to hide arbitrary clue changes from players.')
    site(8,'Sixth Archive','original named affiliation',['O198'],
         'Cartographers of the Sixth Archive gather at Sigil Navigators Library to compare resonance maps.',
         'No separate archive address is given.',
         'A possible provenance or cartographic witness network.',
         'It is unclear whether the name identifies an institution, collection or physical site.',
         'Do not read Sixth as Floor 6, Tier 6, the Sixth Gate or a prescribed sixth puzzle stage.')
    site(9,'Sigil Navigators Library','original named meeting site',['O198'],
         'Cartographers compare emotional barometrics and leylines after Shardfall, identifying new lattice nodes.',
         'Unlocated named library in the Silver Prism narrative.',
         'A possible comparative map source if chronology and availability are resolved.',
         'Its relationship to Library of Shifting Sigils and its current availability remain unproven.',
         'The square root of nowhere is narrative cosmological language, not an adopted computable rule or Equation fragment.')
    site(10,'Unbound Academy library','original library within named institution',['O228','O229','O230','O231'],
         'After the Sunrise of Chosen Threads, the Academy grows seventeen wings near the Yieldheart narrative; a dispute over library silence leads to collaborative muffled-radiance research.',
         'Academy context at Yieldheart; these passages do not provide a Descent floor.',
         'A possible research community and source of contrasting methods.',
         'No specific library holdings, access terms or relationship to the campaign start is established.',
         'Do not equate every Yieldheart reference with the Floor 3 haven, or treat the Academy as automatically available at campaign start.')
    site(11,'Citadel of Many Echoes','original named archive complex',['O236','O237','O238','O275'],
         'The Academy and Yieldheart guilds establish the Citadel at Crystalfall Summit; galleries preserve songs, concord-steel prototypes and oath-accessed crimson chronicles. Selene’s voyage journal is embedded at the foundation; a final chamber holds the Mirror of Potential Silence.',
         'Crystalfall Summit. A cosmological diagram places its symbol between coils two and three as a bridge between shadow and dream.',
         'A possible source of layered historical evidence with documented access distinctions.',
         'The text supplies no campaign-date accessibility, extractable journal, current catalogue or Equation fragment.',
         'Diagram coils are not dungeon floors. A sealed foundation journal is not automatically a loanable book; the diagnostic Mirror does not grant a universal cure.')
    site(12,'Silent Library and Final Ledger','original Matrix encounter',['O253','O254','O255','O256','O257','O258','O259'],
         'The fellowship ascends toward the High Chancel and enters the Matrix through a portal. The Library tries to reduce transient thoughts to zero; memory-rope and sung stories stabilize books. The Final Ledger’s accusation is answered and its display blanks.',
         'Within the Matrix during the Proof War ascent; not assigned to a numbered Descent floor.',
         'An original example of knowledge, memory and Oblivion interacting.',
         'Its chronology, continuing state and relationship to present campaign access need joint resolution.',
         'Do not relocate it into the Descent, erase its narrated transformation, or treat the already-answered encounter as an untouched ordinary library or a recovered Equation manuscript.')
    site(13,'Wax Library','original Dungeon chamber seed',['O308','O309'],
         'The Chamber Seed Table for undocumented dungeon floors includes a Wax Library: books melt when read aloud; silent reading is the preservation challenge.',
         'Explicitly a Dungeon chamber seed; no particular floor or repeat frequency is fixed.',
         'Potential material-handling obstacle for an agreed research clue.',
         'No holdings, language, clue, custodian, placement or Research procedure is supplied.',
         'Silent reading preserves books in this seed; it is not immunity to owner-defined knowledge taint. Selection from a d12 table is not twelve mandatory research stages.')
    site(14,'Cantor’s Archive','secondary mapped Descent haven',['F47','TK-META','TK47','TK44','GZ-HAVENS','GZ-T5'],
         'The Floor 47 haven contains rune-etched lecterns, harmonic drones, harmony-infused elixirs and tone-stones. The draft toolkit gives it a Revealing scene about tone-stones versus dissonance.',
         'Floor 47, Tier 5 / Sanctum of Echoing Choirs. This is an explicit floor placement in the surveyed records.',
         'Potential tonal comparison setting, if an Equation clue and Research method are separately authored and reviewed.',
         'No Equation fragment, translation, exact protective mechanics or taint interaction is present.',
         'Dissonance relief is not automatically knowledge-taint removal. Floor 47 / Tier 5 does not redefine the owner’s separate level-5-onward proximity statement.')
    site(15,'Grand Library of Aethel','secondary named NPC institution',['P5375','P5377','P5378'],
         'Archmage Thorne Vellum, a human Spellbinder, heads a centuries-spanning collection of preserved spellbooks and is sought for ancient-magic guidance.',
         'Aethel; no city, Descent floor or access route in the entry.',
         'Possible surface scholarship or book-provenance support.',
         'Current class terminology, precise location, access and relevant holdings need reconciliation.',
         'Claims that his protection is impenetrable are reported reputation, not a validated mechanical immunity or proof of omniscience.')
    site(16,'Void Archives','secondary mortal cosmology site',['P10367','P10369','P10370','P10371','P10372','P10373','P10375'],
         'The Player appendix lists it among Astral dominions as a repository of knowledge from across the multiverse.',
         'Astral dominion in the secondary account; no Descent floor.',
         'A possible mortal belief or lead for comparison with original cosmology.',
         'Original-source reconciliation, existence as stated, access and holdings remain unconfirmed.',
         'Do not merge it with the Boundless Void or Whispering Archive, promote the secondary list over original cosmology, or guarantee that it knows every answer.')
    site(17,'Grand Libraries of the Age of Wonders','secondary historical collective',['P10432','P10434','P10436','P10437','P10438','P10439','P10440','P10441'],
         'The Player appendix lists Grand Libraries among the developments of an Age of Wonders.',
         'Historical civilization context; individual sites and surviving locations are unspecified.',
         'Possible provenance for later recovered documents.',
         'No named surviving collection, owner, access route or current manuscript.',
         'The claim to all known knowledge is not a guarantee of the Equation. Secondary dates do not set fixed durations for owner-defined primordial ages.')
    site(18,'Luminalis archives','secondary surface collection reference',['W26','GZ-LANG','GZ-T5'],
         'The gazetteer associates Elvish with Luminalis archives and Tier 5 echo samples with Luminalis; the World extract names Queen-Librarian Syphra as ruler of Luminalis.',
         'Luminalis surface-setting context; no individual archive address.',
         'A possible external sponsor, language witness or comparative echo collection.',
         'No identified collection, access conditions or Equation-bearing item.',
         'A librarian title does not prove possession of a specific clue or establish her named deity as primordial cosmological authority.')
    site(19,'Haven library notes','secondary downtime example',['D120','D121','D122','D123','D124'],
         'A Research work row has a cleric translate forge-glyphs, continue translation, then cross-reference haven library notes.',
         'An unnamed haven in an example schedule.',
         'A model for document comparison over meaningful work periods.',
         'No actual library, floor, glyph text or research completion rule is identified.',
         'A scheduling example does not automatically add a library to every haven or establish Equation progress per period.')
    site(20,'Tier 6 civic archive treaty','secondary suggested revelation scene',['D2353','D2354','D2355','D2356','D2357','D2358','D2359'],
         'Director guidance suggests a civic archive containing a treaty where a Pact Signatory assumes control of preexisting crossings; maps depend on who, direction, cargo, agreements and events.',
         'Tier 6 example, no named settlement or particular floor.',
         'A candidate scene for conditional-map research after original-source reconciliation.',
         'The treaty, archive, authorship claim and placement need review against original cosmology.',
         'The word may makes this a proposed example. It does not settle the Heartcell builder or override owner-required source priority.')
    site(21,'Surface archive — Custodian of Weight hook','secondary suggested campaign hook',['D2149','D2150','D2151','D2152','D2153','D2154','D2155'],
         'A continuing-campaign hook places the title Custodian of Weight in a surface archive where it supposedly should not appear.',
         'Unnamed surface archive.',
         'A possible document anomaly to investigate.',
         'No document, custodian identity, reliable interpretation or Equation relationship is supplied.',
         'A hook is not proof of who built the Heartcell or an existing complete puzzle encounter.')
    site(22,'Inherited expedition archive','secondary player legacy asset, not a named site',['C1301','C1302','C8760','C8761','C8762','C8763','C8767','C8768','C8769','P223','P228','P231'],
         'Core describes an archive earned by extracting books, maps and research, offering recipes, clues and appraisal benefits. Matrix research distinguishes inherited records from personal cognitive continuity. Ancestry passages describe rival written, living and oral histories.',
         'An expedition or community record, not a fixed Descent library.',
         'A container for the actual provenance and unresolved interpretations of recovered evidence.',
         'Exact benefits, successor understanding and taint transmission need the current research procedure.',
         'Possession of records does not itself establish functional understanding, independent corroboration, taint amount or completed prerequisites.')

    findings = [
        {'id':'LR01','finding':'The owner requires Research across multiple libraries within the Descent. Within this bounded inventory, Cantor’s Archive is explicitly mapped to Floor 47; Wax Library is an original Dungeon chamber seed without a fixed floor. Other entries do not by themselves supply an additional mapped Descent library.'},
        {'id':'LR02','finding':'None of the selected site passages assigns a recoverable Equation fragment or a complete multi-library progression. Original narrative mathematics and the later expressive notebook drafts remain separate from a chosen playable solution.'},
        {'id':'LR03','finding':'Do not collapse Library of Shifting Sigils and Sigil Navigators Library into one site, or conflate Whispering Archive, Void Archives and the Boundless Void. Sixth Archive has no established floor-number meaning.'},
        {'id':'LR04','finding':'Original site availability depends on narrative chronology. Silent Library is reached within the Matrix through the High Chancel ascent and is changed by the fellowship. Citadel and Academy are founded in later narrated events. Current campaign placement cannot be inferred from the mere existence of these passages.'},
        {'id':'LR05','finding':'Owner Research requirements and the Core’s personal Arcana/History/Religion/Nature/Engineering requirement must be reconciled in the eventual procedure; this inventory supplies neither numeric ranks nor substitute team pooling.'},
        {'id':'LR06','finding':'Physical preservation, translation, functional understanding, knowledge taint, proximity taint and initiation of a Hunt are distinct questions. Silent reading, tone-stones, copied maps or inherited books do not answer the other questions automatically.'},
        {'id':'LR07','finding':'Secondary Director civic-archive and Custodian hooks are suggestions and remain subordinate to original cosmology plus explicit owner corrections. They cannot settle the builder or allow guaranteed public knowledge beyond the agreed revelation ceiling.'},
    ]
    questions = [
        {'id':'LQ01','question':'Which additional libraries actually exist inside the Descent for the Equation route? Can reviewed new sites be authored where original sources leave gaps, and should the Wax Library be placed on a specific floor?','preparedChoice':'Use Cantor and Wax only as candidate settings; keep every additional location and each new holding explicitly proposed until joint review.'},
        {'id':'LQ02','question':'Are Library of Shifting Sigils and Sigil Navigators Library separate institutions, a renamed site, or related collections? Which original narrative era is available to the present campaign?','preparedChoice':'Retain separate records and chronology notes until supported; do not decide by similar names.'},
        {'id':'LQ03','question':'How do Research skill, the researcher’s personal disciplines, source diversity and demonstration of functional understanding interact?','preparedChoice':'Record evidence provenance, interpretation and demonstrated understanding separately; leave numeric prerequisites and pooling unresolved.'},
        {'id':'LQ04','question':'What does each selected library actually contribute: a symbol reading, conflicting interpretation, provenance, contextual constraint or independent test?','preparedChoice':'Author actual examinable evidence and a dependency map before choosing a fragment count; do not import seven stages or the example six-tick clock as an owner decision.'},
        {'id':'LQ05','question':'What warnings, symptoms and meaningful choices precede functional understanding, exposure and Hunt initiation, including silent reading and protected research?','preparedChoice':'Use the existing souls/Hunt draft to resolve consequences without silently nullifying real preservation, ward, cure or resurrection effects.'},
        {'id':'LQ06','question':'How are copied, mistranslated, stolen, altered, destroyed and inherited clues handled so the puzzle remains difficult but reviewable?','preparedChoice':'Keep a source/version/witness record and distinguish independent evidence from a copied claim; replacement leads and recovery costs require explicit scene design.'},
    ]
    cases = [
        {'id':'LRT01','situation':'A Director labels Sigil Navigators Library Floor 6 because Sixth Archive cartographers meet there.','expected':'Reject the unsupported placement; institution naming and floor numbering are separate.'},
        {'id':'LRT02','situation':'A party reads the Wax Library silently and argues it cannot be tainted.','expected':'Silent reading addresses book preservation only; the actual knowledge/proximity rules remain a separate, currently unresolved procedure.'},
        {'id':'LRT03','situation':'A character uses a Cantor tone-stone and claims all forbidden understanding is erased.','expected':'The haven prose supplies no such cure. Apply only a separately defined reviewed item effect.'},
        {'id':'LRT04','situation':'A Director supplies the whole Equation from Grand Libraries because they contain all known knowledge.','expected':'A secondary historical description supplies neither present access nor an actual complete Equation text.'},
        {'id':'LRT05','situation':'A recovered copy and its original are counted as two independent library discoveries.','expected':'Under the proposed evidence protocol, record their shared provenance; whether and how either yields progress must be explicit.'},
        {'id':'LRT06','situation':'The Silent Library is inserted as an ordinary untouched Floor 97 room.','expected':'Flag the unsupported relocation and chronology change; preserve original High Chancel/Matrix context and the separately reviewed Q6 boundaries.'},
        {'id':'LRT07','situation':'A successor inherits the archive and is treated as personally qualified in every discipline.','expected':'Source possession does not prove personal qualification or cognitive continuity. Resolve Research and inheritance explicitly.'},
        {'id':'LRT08','situation':'A Tier 6 civic treaty is cited as settled proof of the Heartcell builder.','expected':'The suggested scene does not establish that identity; original-source priority and unresolved authorship remain in force.'},
    ]
    for record in records:
        assert all(x in evidence for x in record['evidenceIds'])
    result = {
        'reviewId':'COSMOLOGY-EQUATION-LIBRARY-SOURCE-INVENTORY-01',
        'recordedAtUtc':datetime.now(timezone.utc).isoformat(),
        'status':'Bounded source inventory and proposed conference agenda; unsubmitted, no new canon or procedures adopted',
        'authority':'Explicit owner corrections; original cosmology first. Secondary documents are qualified as such. New research uses and questions are proposals, not recovered source facts.',
        'sourceBindings':list(bindings.values()),'discovery':discovery,'evidenceLocations':list(evidence.values()),
        'records':records,'findings':findings,'questions':questions,'reviewSituations':cases,
        'coverage':{'records':len(records),'notAllPhysicalSites':True,'sourceFiles':len(bindings),'completeDocxParagraphs':sum('paragraphIndexZeroBased' in x for x in evidence.values()),'completeJsonObjects':sum('jsonPointer' in x for x in evidence.values()),'completeMarkdownSections':sum('firstLineOneBased' in x for x in evidence.values()),'limitations':'Bounded reading of listed passages and objects, not an exhaustive semantic review of the folder. Website text mirrors and audit copies are not independent manuscript witnesses. Search results not saved as complete evidence are not claimed semantically reviewed.'},
        'gptReview':'No joint review yet. Part 2 reached its length limit; the existing owner choice about Part 3 remains pending. This inventory does not modify the frozen planes packet or prepared handoff.',
        'equationFragmentsAssigned':0,'additionalLibrariesInvented':0,'newRulesAdopted':False,'runtimeApproved':False,'publicExportEnabled':False,'fullCosmologyApproved':False,'sourceInformationDeleted':0,
    }
    target.write_bytes(encoded(result))
    md = ['# Equation research: existing libraries and archives','',
          'Director preparation only · source inventory and discussion draft · not jointly reviewed or adopted','',
          'The owner requires Research across multiple libraries **inside the Descent**. This inventory contains 22 records, including institutions, examples and metaphors; it does not claim 22 usable dungeon libraries. Cantor’s Archive is explicitly placed on Floor 47. The original Wax Library is a dungeon chamber seed without a fixed floor. No selected site passage supplies an assigned Equation fragment or a complete research route.','',
          'Use original cosmology first, with the explicit [Heartcell owner corrections](HEARTCELL_OWNER_UPDATE_02.md). This companion does not relocate cosmic sites, choose numeric taint stages, or replace the [souls and Hunt discussion draft](SOULS_DEATH_HUNT_CONFERENCE_DRAFT_01.md). All candidate uses below are proposals.','',
          '## Existing settings and their limits','']
    for record in records:
        md += [f"### {record['id']} — {record['name']}",'',f"**Source category:** {record['recordKind']}.",'',record['sourceFinding'],'',f"**Location:** {record['locationEvidence']}",'',f"**Possible research use, unadopted:** {record['candidateResearchUseNotAdopted']}",'',f"**Still missing:** {record['unresolved']}",'',f"**Reading limit:** {record['doNotInfer']}",'',f"Evidence: {', '.join(record['evidenceIds'])} in the [source inventory](../../../data/director/cosmology/equation_library_source_inventory_01.json).",'']
    md += ['## What the sources establish','']
    for f in findings: md += [f"- **{f['id']}:** {f['finding']}"]
    md += ['','## Decisions prepared for GPT','']
    for q in questions: md += [f"**{q['id']} — {q['question']}**",'',q['preparedChoice'],'']
    md += ['## Eight review situations','']
    for c in cases: md += [f"**{c['id']} — {c['situation']}**",'',c['expected'],'']
    md += ['## Coverage and status','',f"The machine-readable inventory embeds {result['coverage']['completeDocxParagraphs']} complete DOCX paragraphs, {result['coverage']['completeJsonObjects']} complete JSON objects and {result['coverage']['completeMarkdownSections']} Markdown sections, bound to {len(bindings)} exact source files. Paragraph indices count all document paragraphs, including blanks and table paragraphs. A search hit is discovery, not semantic approval. The original Matrix manuscript was included in the bounded word-stem search and yielded no matching paragraph; that is not a claim that it has no relevant research lore.",'',
           'ChatGPT Part 2 reached its conversation-length limit. The existing Part 3 choice remains pending, so this inventory has not been submitted. The frozen planes packet and all original source files are unchanged. No Equation fragments, additional libraries, numerical mechanics or public/runtime content have been adopted.','']
    chapter.write_text('\n'.join(md),encoding='utf-8',newline='\n')
    # Re-read each exact evidence location against source bytes, independently of generation arrays.
    for row in bindings.values(): assert info(G/row['path']) == row
    verified = 0
    for item in evidence.values():
        p = G/item['path']
        if 'paragraphIndexZeroBased' in item:
            with ZipFile(p) as z: root=E.fromstring(z.read(item['part']))
            ps=[''.join(t.text or '' for t in q.findall('.//w:t',ns)) for q in root.findall('.//w:p',ns)]
            actual=ps[item['paragraphIndexZeroBased']]; assert actual == item['text']
            assert hashlib.sha256(actual.encode()).hexdigest() == item['textSha256']
        elif 'jsonPointer' in item:
            actual=json.loads(p.read_text(encoding='utf-8-sig'))
            for token in item['jsonPointer'].strip('/').split('/'):
                token=token.replace('~1','/').replace('~0','~'); actual=actual[int(token)] if isinstance(actual,list) else actual[token]
            assert actual == item['value']
        else:
            actual='\n'.join(p.read_text(encoding='utf-8-sig').splitlines()[item['firstLineOneBased']-1:item['lastLineOneBased']])
            assert actual == item['text'] and hashlib.sha256(actual.encode()).hexdigest() == item['textSha256']
        verified += 1
    assert len(records)==22 and len(questions)==6 and len(cases)==8
    check.write_bytes(encoded({'inventory':info(target),'chapter':info(chapter),'sourceBindingsVerified':len(bindings),'exactEvidenceLocationsVerified':verified,'records':22,'questions':6,'reviewSituations':8,'sourceInformationDeleted':0,'newRulesAdopted':False,'gptJointReview':False}))
    print(json.dumps(json.loads(check.read_bytes())))


if __name__=='__main__': main()
