"""Preserve new owner corrections and prepare a source-bound actual-notebook review.

One-use preparation only. Does not overwrite original lore or adopt GPT proposals.
"""
from datetime import datetime, timezone
from pathlib import Path
import hashlib, json, re, subprocess, zipfile
from xml.etree import ElementTree as ET
from apply_di7_ap_as_01 import G, R, A, info, encoded

ID = 'COSMOLOGY-OWNER-RECONCILIATION-01'
CAPTURE = 'COSMOLOGY_OWNER_CORRECTIONS_2026_10_15_MESSAGE_CAPTURE.json'
CONTEXT = 'COSMOLOGY_OWNER_CORRECTIONS_2026_10_15_CONVERSATION_DOM.txt'

READINGS = [
 ('Aethel formation', 'Explicit owner correction', 'After confinement, Aethel gradually appeared around the prison. The planetary comparison is the owner\'s analogy, not a literal orbital model.', ['U-01','U-02'], 'Matrix P39 places the prison beneath a material world; original Cosmology P72 mentions souls coalescing near the prison. Preserve both and flag ordering conflict; do not fabricate a mechanism or date.'),
 ('Quiet and chaotic rooms', 'Explicit owner correction; wording preserved', 'Heartcell was designed to be as quiet as possible; ever-changing rooms supply chaotic noises that keep the prisoners lulled; peace is the trigger.', ['U-02','U-07'], 'Do not silently turn quiet into complete acoustic silence. Matrix P4–7 and P41–50 distinguish ontological peace from ordinary treaties and require activity. Cosmology P17–19, P24–26, P83 and P154–159 supply related but not identical accounts. No new threshold.'),
 ('Pact sentience; no essence tether', 'Explicit owner correction', 'Calanthir and Asmodeus have not tied their essence; the Pact itself became sentient.', ['U-03'], 'July Q3 says bound themselves, without specifying essence. Cosmology P53 describes expenditure of essence during resealing, not a perpetual essence tether. P160–174 contains actual Pact sentience. Do not erase all covenant obligations or treat sentience as simultaneous with manifestation unless sourced.'),
 ('Scope of Sundering', 'Context-bound owner agreement', 'The owner said agreed to GPT\'s U-04 row; retain the exact referent below. This is assent to that row, not the rest of the proposed package.', ['U-04'], 'July Q5 still treats Lumina/Umbra as theological abstractions and Appendix B as mortal religion. Matrix P22–34 and original Cosmology P59 use Sundering for conflict. Identify the precise contradiction without silently literalizing the entire folk creation story.'),
 ('Twenty cycles', 'Skepticism; no adopted definition', 'The owner questions whether the cycle explanation was invented; GPT later admits its internal convergence-cycle model was invented.', ['U-05'], 'Matrix P27 actually says twenty cycles. Do not delete the attested phrase or adopt GPT\'s accumulation/convergence/reset unit. Unit, duration and sequence remain unestablished.'),
 ('Harmony principles', 'Explicit thematic authority; mapping unresolved', 'The owner identifies seven principles of harmony in nature associated with Harmony by Charles, Tony Juniper and Ian Skelly as governing the celestial side.', ['U-06'], 'The message does not enumerate principles, replace seven Choir names/virtues, or define emergence timing. The external primary-source list is research context, not a game mapping or proof of exact book wording. No invented aliases or schedule.'),
 ('Equation of Oblivion', 'Explicit source-recovery direction', 'Remember the equation of oblivion.', ['U-07'], 'Retrieve exact surviving Matrix text and retain the checked source gap: 23 incomplete plain-text formula paragraphs, no OMML or embedded formula recovery. Do not invent missing math or a numeric stillness threshold.'),
 ('Prison manifestation and desperate containment', 'Explicit owner correction; builder not identified', 'Heartcell was a desperate attempt to find something that silences them; the Pact manifested the prison.', ['U-01','U-02','U-03','U-08'], 'This directly challenges the July Q3 prison-builder formulation. The passive sentence does not name a new Heartcell builder or settle every machinery layer. It does not answer Shardspire origin, despite its position as item 8. No inverted convergence-engine repair.'),
 ('Many Old Ones become one', 'Explicit owner correction; Floor 97 link absent', 'Many Old Ones attacked; after imprisonment they devoured each other until one primal one remained, silent and hungry for oblivion.', ['U-09'], 'Cosmology P49 describes converged dreaming and P154 fused one mind; preserve the different earlier account. The owner does not explicitly name the survivor Ul\'nak or identify it with the Floor-97 Old God/Interstice. July Q6, World P7 and current Director chapter 34 remain distinct evidence.'),
 ('Missing World sections', 'Direction to address source gap', 'Lets address it refers to the missing World of Aethel I–VI issue.', ['U-10'], 'Search for recoverable originals. Do not pass GPT\'s proposed six replacement headings off as the original missing outline. Any later authored replacement must be marked NEW.'),
 ('Mephistopheles', 'Explicit owner placement lock', 'Mephistopheles has one canonical placement: Cania.', ['U-11','GP-04','GPR-04'], 'This closes the Mephistopheles placement question and rejects dual placement. Original Cosmology P56 is retained as a historical error. The owner did not name a replacement ruler of Maladomini.'),
]

U04_REFERENT = "RESOLVED. The Sundering is only the primordial Lumina/Umbra separation and the first great division of reality. It does not include the Silent Ones' imprisonment, First Seal, Divine Pact, Crucible construction, or later activation. Those happen afterward. This preserves the published definition instead of stretching “Sundering” across unrelated epochs."

REQUEST = '''COSMOLOGY-OWNER-RECONCILIATION-01 — source excavation and precise incorporation of actual owner corrections.

Before proceeding to planes, review the eleven actual owner statements captured from the separate Resolve Heartcell Origins conversation. The user rebuked the notebook for inventing connective lore. We must not repeat that. The capture is a submitted human message, not a draft; its HTML has an ordered list starting at 2. The owner guardrail is: Review my sources of lore. I think you are inventing things. The full role-labelled conversation context is supplied only to bind each reply; GPT's tables labelled NEW OWNER LOCK are GPT proposals, not human authority. GPT later expressly retracted its invented convergence-engine purpose, inversion, essence tether, internal-cycle model, Choir schedule, Shardspire hardware story, invented replacement headings, and unsupported Floor-97 merger/separation claims.

Use the actual original full DOCX sources and exact paragraph index, July owner locks, current Director/Player and separate reviewed companions. Original sources and historical receipts must stay intact. Our local register provides eleven exact quotes and conservative provisional readings. Challenge those readings if the exact evidence differs. Every returned statement must distinguish owner text, earlier owner lock, original-source assertion, reviewer interpretation, unresolved conflict, and newly authored proposal (none requested here).

Required work:
1. Return one disposition for each OC-01 through OC-11. Show precisely what the new owner text establishes, which older statements are superseded, what is still unresolved, and source citations with exact file, XML part, zero-based paragraph index, textSha256 and excerpt. Do not infer a named Heartcell builder from passive wording. Distinguish prison manifestation from underlying machinery without inventing a reconciliation.
2. Sundering: item 4 is agreed to the exact U-04 row copied in the register. Preserve this limited assent and confront Matrix P22–34 / Cosmology P59's conflicting use. Do not treat Appendix B wholesale as objective lore or abolish Q5's abstraction boundary.
3. Cycles and Choir: Matrix P27 attests twenty cycles but no unit. Owner item 5 is skeptical, not approval of your invented model. Item 6 establishes Harmony inspiration/celestial governance but not a one-to-one mapping to the existing seven named Choir virtues or a chronology. The external Harmony Project list is a verified research reference, not the missing game source or an owner-approved mapping.
4. Pact/Old Ones: read actual Cosmology P16–19, P49–59, P154–174 and Matrix P0–55. No essence tether; Pact sentience is genuine source content. Owner's devouring-to-one replaces a conflicting mechanism where relevant but does not automatically identify the survivor with every Ul'nak spelling, World P7 Floor-97 Old God or Interstice. Track the exact remaining identity question instead of either forced identity or forced disjointness. Quiet/noise/peace must preserve owner wording and Matrix's explicit political-vs-ontological distinction; no invented acoustic or numeric rule.
5. Mephistopheles: incorporate Cania as the explicit current owner lock. Maladomini's replacement remains unassigned. Missing World I–VI and incomplete formula source: retain exact gaps and search findings. No reconstructed math, six invented chapters, or fictitious recoveries.
6. Supply current coherent Director-only reconciliation prose and a precise adoption matrix for existing creation_origins_reviewed_01, gods_pantheons_reviewed_01, CANON_CORE, July historical locks and current Director text. Label unresolved seams visibly. Prior completed reviews remain historical evidence, not current authority over the later owner's words. Do not edit/reinterpret old receipts, promote class/spell mechanics, change audience boundaries, certify deployment or claim full cosmology/game approval.

Return COSMOLOGY_OWNER_RECONCILIATION_01_Addendum_and_Evidence.zip with REGISTER.json (all 11 dispositions, exact owner quotes, evidence and remaining dependencies), DIRECTOR_COMPANION.md, ADOPTION_MATRIX.json, VERDICT.md, SOURCE_HASHES.json matching all entries in CURRENT_SOURCE_BINDINGS.json, and EVIDENCE_MANIFEST.json with payload bytes/SHA-256. Make the register structured with fields id, ownerQuote, disposition, established, superseded, retained, unresolved, evidence for each item. DOCX evidence fields: file, part, paragraphIndexZeroBased, textSha256, excerpt. Non-DOCX evidence uses exact source path and excerpt. Do not label GPT interpretations owner locks. Scope: careful source reconciliation, not expansion of lore.
'''


def source_probe():
    """Literal phrase recovery across source text and all non-audit DOCX; no web lore import."""
    names = subprocess.run(['rg','--files','--hidden',str(G),'-g','!.git/**','-g','!**/node_modules/**'], capture_output=True, text=True, encoding='utf-8', check=True).stdout.splitlines()
    paths = []
    for n in names:
        p=Path(n); rel=p.relative_to(G).as_posix()
        if '/audit/' in '/'+rel or any(x in p.parts for x in ['.git','node_modules','.next','dist','build']): continue
        if p.suffix.lower() in ['.docx','.txt','.md','.json']: paths.append(p)
    patterns = {'harmony_reference':re.compile(r'King Charles|Tony Juniper|Ian Skelly|seven principles of harmony|harmony in nature',re.I), 'twenty_cycles':re.compile(r'twenty\s+(?:\w+\s+){0,2}cycles',re.I)}
    seen={}; matches=[]; worlds=[]; errors=[]
    counts={'paths':len(paths),'uniqueContents':0,'docxPaths':0,'uniqueDocx':0}
    for p in paths:
        rel=p.relative_to(G).as_posix()
        long_path=Path('\\\\?\\'+str(p))
        try: b=long_path.read_bytes()
        except OSError as e:
            errors.append({'path':rel,'error':str(e)}); continue
        h=hashlib.sha256(b).hexdigest()
        if 'world' in p.name.lower() and 'aethel' in p.name.lower(): worlds.append({'path':rel,'bytes':len(b),'sha256':h})
        if p.suffix.lower()=='.docx': counts['docxPaths']+=1
        if h in seen:
            seen[h]['aliases'].append(rel); continue
        entry={'sha256':h,'path':rel,'bytes':len(b),'aliases':[]}; seen[h]=entry
        counts['uniqueContents']+=1
        try:
            if p.suffix.lower()=='.docx':
                counts['uniqueDocx']+=1
                with zipfile.ZipFile(long_path) as z:
                    rows=[]
                    for part in z.namelist():
                        if part=='word/document.xml' or re.fullmatch(r'word/(header|footer)\d+\.xml',part):
                            xml=ET.fromstring(z.read(part)); ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                            rows.extend({'part':part,'paragraphIndexZeroBased':i,'text':''.join(t.text or '' for t in q.findall('.//w:t',ns))} for i,q in enumerate(xml.findall('.//w:p',ns)))
            else:
                encoding='utf-16' if b[:2] in [b'\xff\xfe',b'\xfe\xff'] else 'utf-8-sig'
                rows=[{'lineOneBased':i,'text':s} for i,s in enumerate(b.decode(encoding).splitlines(),1)]
            for key,pat in patterns.items():
                hit=[v for v in rows if pat.search(v['text'])]
                if hit: matches.append({'query':key,'source':entry,'matches':hit})
        except Exception as e: errors.append({'path':rel,'error':str(e)})
    return {'scope':'All rg-enumerated non-audit .docx/.txt/.md/.json under G, including preserved history; byte-identical files deduplicated with aliases. DOCX main/header/footer paragraphs only. Archives/PDF/images not searched; absence is bounded to this corpus. Later authored review material is not an original lore source.', 'queries':{k:v.pattern for k,v in patterns.items()},'counts':counts,'matches':matches,'worldAethelNamedFiles':worlds,'errors':errors}


def main():
    root=A/'cosmology-owner-reconciliation-01'; archive=A/'DD_Cosmology_Owner_Reconciliation_01.zip'
    receipt=A/'COSMOLOGY_OWNER_RECONCILIATION_01_PREPARATION.json'
    assert all(not p.exists() for p in [root,archive,receipt])
    capture=json.loads((A/CAPTURE).read_bytes()); context=(A/CONTEXT).read_text(encoding='utf-8')
    assert len(capture['ownerMessage']['listItems'])==10
    quotes=capture['ownerMessage']['paragraphs']+[x['text'] for x in capture['ownerMessage']['listItems']]
    assert U04_REFERENT in context
    now=datetime.now(timezone.utc).isoformat()
    items=[]
    for i,((topic,status,reading,refs,caution),quote) in enumerate(zip(READINGS,quotes),1):
        item={'id':f'OC-{i:02d}','ownerItemNumber':i,'ownerQuote':quote,'topic':topic,'authorityClassification':status,'codexProvisionalReading':reading,'affectedIssues':refs,'cautionAndSourceConflict':caution}
        if i==4: item['exactGptReferentAcceptedByAgreed']=U04_REFERENT
        items.append(item)
    register={'reviewId':ID,'recordedAtUtc':now,'status':'Exact owner text captured; Codex interpretations pending actual GPT source reconciliation','ownerCapture':info(A/CAPTURE),'contextCapture':info(A/CONTEXT),'ownerGuardrail':capture['ownerGuardrail'],'items':items,'informationDeleted':0}
    probe=source_probe()
    external={'title':'What are Nature’s principles of Harmony?','url':'https://www.theharmonyproject.org.uk/faq/what-are-nature-principles-of-harmony','accessedDate':'2026-10-15','verifiedVia':'web open primary Harmony Project FAQ, lines 59–62','principleLabels':['Diversity','Cycle','Interdependence','Adaptation','Health','Geometry','Oneness'],'authority':'External research context only; not an in-game owner-approved Choir mapping. The exact cited book edition/text was not inspected. No full webpage reproduced.'}
    payloads={}
    # Preserve full previously reviewed packet, not merely selective quotations.
    with zipfile.ZipFile(A/'DD_Cosmology_Gods_Pantheons_01.zip') as z:
        for name in z.namelist():
            assert not name.startswith('/') and '..' not in Path(name).parts
            payloads['previous-source-packet/'+name]=z.read(name)
    bindings=json.loads((A/'cosmology-gods-pantheons-01/SOURCE_BINDINGS.json').read_bytes())
    for row in bindings: assert info(G/row['path'])==row
    extra=[
      A/CAPTURE,A/CONTEXT,A/'COSMOLOGY_MATRIX_FORMULA_SOURCE_CHECK_01.json',A/'COSMOLOGY_DIRECTOR_INTERSTICE_SOURCE_CHECK_01.json',
      A/'COSMOLOGY_OWNER_SOURCE_PRIORITY_2026_10_15_CAPTURE.json',A/'COSMOLOGY_OWNER_SOURCE_PRIORITY_2026_10_15_CONTEXT_DOM.txt',
      A/'COSMOLOGY_CREATION_ORIGIN_01_RECEIVED_DECISION.json',A/'COSMOLOGY_GODS_PANTHEONS_FOLLOWUP_01_RECEIVED_DECISION.json',
      R/'data/director/cosmology/creation_origins_reviewed_01.json',R/'docs/director-only/cosmology/CREATION_ORIGINS_REVIEWED_01.md',
      R/'data/director/cosmology/gods_pantheons_reviewed_01.json',R/'docs/director-only/cosmology/GODS_PANTHEONS_REVIEWED_01.md',
      R/'docs/canon/CANON_CORE.md',R/'docs/canon/PLAYER_DIRECTOR_BOUNDARY.md',
      R/'docs/director-only/continuity/OWNER_COSMOLOGY_LOCKS_2026-07-30.md',R/'docs/mechanics/WORLD_DUNGEON_LOOP.md',
    ]
    for p in extra:
        row=info(p); payloads['current-sources/'+row['path']]=p.read_bytes()
        if row['path'] not in {x['path'] for x in bindings}: bindings.append(row)
    for p in sorted((A/'cosmology-gods-pantheons-followup-01-received').iterdir()):
        if p.is_file(): payloads['corrected-gods-review/'+p.name]=p.read_bytes()
    payloads['OWNER_CORRECTION_REGISTER_PROPOSED.json']=encoded(register)
    payloads['LOCAL_SOURCE_PROBE.json']=encoded(probe)
    payloads['EXTERNAL_HARMONY_REFERENCE.json']=encoded(external)
    payloads['CURRENT_SOURCE_BINDINGS.json']=encoded(bindings)
    pending_priority='''\nLater source-priority message: the owner subsequently wrote Use the original version followed by a quotation of the Director Silent-Ones-builder account. GPT interpreted this as original manuscripts controlling, but the referent is ambiguous. Exact capture and later role-labelled context are included. Codex has asked the human which meaning they intend. Do not treat GPT\'s interpretation as confirmation, do not settle that choice by a second GPT vote, and keep dependent authorship adoption conditional until the human clarifies. Continue the non-dependent source comparison and unambiguous Cania/no-essence-tether corrections.\n'''
    payloads['REQUEST.txt']=(REQUEST+pending_priority).encode('utf-8')
    payloads['prepare_cosmology_owner_reconciliation_01.py']=Path(__file__).read_bytes()
    manifest={'reviewId':ID,'recordedAtUtc':now,'ownerItems':11,'currentSourceCount':len(bindings),'informationDeleted':0,'payloads':[{'path':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for n,b in sorted(payloads.items())]}
    payloads['PACKAGE_MANIFEST.json']=encoded(manifest)
    root.mkdir()
    for n in ['OWNER_CORRECTION_REGISTER_PROPOSED.json','LOCAL_SOURCE_PROBE.json','EXTERNAL_HARMONY_REFERENCE.json','CURRENT_SOURCE_BINDINGS.json','REQUEST.txt','PACKAGE_MANIFEST.json']: (root/n).write_bytes(payloads[n])
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED) as z:
        for n,b in sorted(payloads.items()): z.writestr(n,b)
    with zipfile.ZipFile(archive) as z:
        assert len(z.namelist())==len(payloads)
        for row in manifest['payloads']:
            b=z.read(row['path']); assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
    receipt.write_bytes(encoded({'reviewId':ID,'recordedAtUtc':now,'status':'prepared; not submitted','archive':info(archive),'manifest':info(root/'PACKAGE_MANIFEST.json'),'register':info(root/'OWNER_CORRECTION_REGISTER_PROPOSED.json'),'probe':info(root/'LOCAL_SOURCE_PROBE.json'),'sourceCount':len(bindings),'payloadsVerified':len(manifest['payloads']),'sourceInformationDeleted':0}))
    print(json.dumps({'archive':info(archive),'receipt':info(receipt),'probeCounts':probe['counts'],'probeErrors':len(probe['errors']),'harmonyMatchedUniqueFiles':sum(x['query']=='harmony_reference' for x in probe['matches']),'worldNamedFiles':len(probe['worldAethelNamedFiles'])}))

if __name__=='__main__': main()
