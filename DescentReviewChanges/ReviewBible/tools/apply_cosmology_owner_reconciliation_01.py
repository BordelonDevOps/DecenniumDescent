"""Apply bounded owner reconciliation; preserve originals, receipts and prior companions."""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib, json, re
from apply_di7_ap_as_01 import G, R, A, info, encoded


def read(p):return json.loads(p.read_bytes())


def walk(o):
    if isinstance(o,dict):
        yield o
        for v in o.values():yield from walk(v)
    elif isinstance(o,list):
        for v in o:yield from walk(v)


def plain(s):return ' '.join(s.replace('**','').split())


def main():
    root=A/'cosmology-owner-reconciliation-01-received'
    candidate=R/'data/director/cosmology/owner_reconciliation_reviewed_01.json'
    companion=R/'docs/director-only/cosmology/OWNER_RECONCILIATION_REVIEWED_01.md'
    current=R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md'
    core=R/'docs/canon/CANON_CORE.md'
    preserved=A/'canon-core-before-owner-reconciliation-01'
    check=A/'COSMOLOGY_OWNER_RECONCILIATION_01_ADOPTION_CHECK.json'
    assert all(not p.exists() for p in [candidate,companion,current,preserved,check])
    previous_check=read(A/'COSMOLOGY_OWNER_RECONCILIATION_01_APPLICATION_CHECK.json')
    assert previous_check['exactOwnerQuotesVerified']==11 and previous_check['docxCitationOccurrences']==34
    assert all(x['hashMatches'] and x['excerptMatches'] for x in previous_check['docxChecks'])
    bindings=read(A/'cosmology-owner-reconciliation-01/CURRENT_SOURCE_BINDINGS.json')
    assert all(info(G/r['path'])==r for r in bindings)
    original=read(root/'REGISTER.json');register=deepcopy(original)
    probe=read(A/'cosmology-owner-reconciliation-01/LOCAL_SOURCE_PROBE.json')
    enc=read(A/'COSMOLOGY_OWNER_RECONCILIATION_01_ENCODING_ADDENDUM.json')
    formula=read(A/'COSMOLOGY_MATRIX_FORMULA_SOURCE_CHECK_01.json')
    harmony=read(A/'cosmology-owner-reconciliation-01/EXTERNAL_HARMONY_REFERENCE.json')
    context=A/'COSMOLOGY_OWNER_CORRECTIONS_2026_10_15_CONVERSATION_DOM.txt'
    locks=R/'docs/director-only/continuity/OWNER_COSMOLOGY_LOCKS_2026-07-30.md'
    source_aliases={name:A/'cosmology-owner-reconciliation-01'/name for name in ['LOCAL_SOURCE_PROBE.json','EXTERNAL_HARMONY_REFERENCE.json']}
    source_aliases['COSMOLOGY_OWNER_RECONCILIATION_01_ENCODING_ADDENDUM.json']=A/'COSMOLOGY_OWNER_RECONCILIATION_01_ENCODING_ADDENDUM.json'
    edits=[]; resolved_checks=[]
    for item in register['items']:
        for evidence in item['evidence']:
            if 'file' in evidence:
                evidence['evidenceKind']='exact-docx-paragraph-with-verified-hash-and-excerpt';continue
            source=evidence['sourcePath']; quote=evidence['excerpt']
            if item['id']=='OC-04' and evidence.get('locator','').startswith('context-bound'):
                assert quote in context.read_text(encoding='utf-8')
                edits.append({'itemId':item['id'],'kind':'source-path-correction','before':source,'after':context.relative_to(G).as_posix(),'textUnchanged':True})
                evidence['sourcePath']=context.relative_to(G).as_posix();evidence['evidenceKind']='exact-gpt-referent; owner-assent-is-separate-agreed-quote';evidence['sourceBinding']=info(context);resolved_checks.append({'itemId':item['id'],'kind':'correct-context-path','passed':True});continue
            path=source_aliases.get(source,G/source); evidence['resolvedSourcePath']=path.relative_to(G).as_posix();evidence['sourceBinding']=info(path)
            if source=='LOCAL_SOURCE_PROBE.json':
                if item['id']=='OC-05':
                    matches=[x for x in probe['matches'] if x['query']=='twenty_cycles'];assert matches
                    assert any(any(m.get('paragraphIndexZeroBased')==27 and 'The Sundering lasted twenty cycles.' in m['text'] for m in x['matches']) for x in matches)
                    actual={'matchedSources':len(matches),'exactOriginalPhrase':'The Sundering lasted twenty cycles.','definedUnitInProbe':False}
                elif item['id']=='OC-06':
                    hits=[x for x in probe['matches'] if x['query']=='harmony_reference'];assert hits==[]
                    actual={'counts':probe['counts'],'harmonyReferenceMatches':[],'scope':probe['scope']}
                elif item['id']=='OC-10':
                    docs=[x for x in probe['worldAethelNamedFiles'] if x['path'].endswith('.docx')];assert len(docs)==4 and len({x['sha256'] for x in docs})==1
                    actual={'namedDocxCopies':docs,'originalPlaceholder':'[...Existing Sections I–VI remain unchanged...]'}
                else:raise AssertionError(item['id'])
                evidence['evidenceKind']='reviewer-summary-of-verified-structured-evidence';evidence['verifiedSourceValues']=actual
            elif source=='EXTERNAL_HARMONY_REFERENCE.json':
                assert harmony['principleLabels']==['Diversity','Cycle','Interdependence','Adaptation','Health','Geometry','Oneness']
                evidence['evidenceKind']='reviewer-summary-of-external-research-reference';evidence['verifiedSourceValues']=harmony
            elif source=='COSMOLOGY_OWNER_RECONCILIATION_01_ENCODING_ADDENDUM.json':
                assert enc['uniqueEncodedSources']==15 and not enc['unresolvedPriorDecodeErrors']
                assert all(x['roundTripExact'] and not x['matches']['harmony_reference'] and not x['matches']['twenty_cycles'] for x in enc['sources'])
                evidence['evidenceKind']='reviewer-summary-of-verified-structured-evidence';evidence['verifiedSourceValues']={'uniqueEncodedSources':15,'unresolvedErrors':[],'harmonyMatches':0,'twentyCyclesMatches':0,'roundTripExactAll':True}
            elif path.name=='COSMOLOGY_MATRIX_FORMULA_SOURCE_CHECK_01.json':
                assert formula['paragraphsChecked']==23 and formula['oMathObjectsInMainDocument']==0 and not formula['embeddedMediaOrObjects']
                evidence['evidenceKind']='reviewer-summary-of-verified-structured-evidence';evidence['verifiedSourceValues']={k:formula[k] for k in ['paragraphsChecked','oMathObjectsInMainDocument','embeddedMediaOrObjects','result','remainingLimitation']}
            elif path==locks:
                s=plain(path.read_text(encoding='utf-8'))
                if evidence['locator']=='Q2':assert plain(quote) in s
                elif evidence['locator']=='Q5':
                    for fragment in ['Keep, but as mortal folk religion — not objective canon.','Lumina/Umbra as theological abstractions']:assert fragment in s
                elif evidence['locator']=='Q6':
                    for fragment in ['Not answered by the owner in this round. Left open.','Do not infer an answer.']:assert fragment in s
                else:assert plain(quote) in s
                evidence['evidenceKind']='normalized-markdown-quote' if evidence['locator']=='Q2' else 'reviewer-summary-or-joined-excerpts-with-markup-removed'
            else:
                evidence['evidenceKind']='exact-owner-message-or-capture-excerpt'
                assert any(x['sourcePath']==source and x['excerpt']==quote and x['excerptMatchesDecodedSource'] for x in previous_check['nonDocxChecks'])
            resolved_checks.append({'itemId':item['id'],'sourcePath':evidence['sourcePath'],'kind':evidence['evidenceKind'],'passed':True})
    # The returned prose corrected a typo inside quotes. Restore the exact submitted sentence.
    manuscript=(root/'DIRECTOR_COMPANION.md').read_text(encoding='utf-8')
    bad='“The heartcell was a desperate attempt to find something that silence them, the Pact manifested the prison.”'
    good='“'+register['items'][7]['ownerQuote']+'”';assert manuscript.count(bad)==1
    manuscript=manuscript.replace(bad,good,1)
    edits.append({'kind':'exact-owner-quotation-restored','before':bad,'after':good,'substantiveDecisionChanged':False})
    # Original companion labels summarized facts as OWNER CURRENT. Exact item quote source is provided below.
    manuscript+='\n## Traceable review record\n\nThe exact eleven owner statements, reviewed dispositions and citation checks are retained in [the structured companion](../../../data/director/cosmology/owner_reconciliation_reviewed_01.json). The returned GPT archive is preserved unchanged. Local editorial verification corrected one context-file pointer, classified source summaries separately from quotations, and restored the owner’s exact “desperte” wording inside the quoted sentence. No new lore was added.\n\nThe later archive-index search is separate local evidence: twelve non-audit ZIP indexes and six relevant source payloads were checked without recovering World I–VI. It does not establish universal absence.\n'
    assert len(register['remainingDependencies'])==13
    now=datetime.now(timezone.utc).isoformat()
    data={'reviewId':register['reviewId'],'recordedAtUtc':now,'status':'Reviewed Director-only owner-correction successor; authorship/source-priority branch remains conditional','register':register,'adoptionMatrix':read(root/'ADOPTION_MATRIX.json'),'sourceReceipt':info(A/'COSMOLOGY_OWNER_RECONCILIATION_01_RECEIVED_DECISION.json'),'sourceCheck':info(A/'COSMOLOGY_OWNER_RECONCILIATION_01_APPLICATION_CHECK.json'),'localEditorialCorrections':edits,'localEvidenceClassificationChecks':resolved_checks,'laterArchiveProbe':info(A/'COSMOLOGY_OWNER_RECONCILIATION_01_ARCHIVE_INDEX_CHECK.json'),'publicExportEnabled':False,'dependentAuthorshipAdopted':False,'fullCosmologyApproved':False,'sourceInformationDeleted':0}
    candidate.write_bytes(encoded(data));companion.write_text(manuscript,encoding='utf-8',newline='\n')
    current.write_text('''# Current cosmology reading order

Start with [the reviewed owner-correction companion](OWNER_RECONCILIATION_REVIEWED_01.md). It incorporates the eleven statements captured on 15 October and keeps the later source-priority ambiguity visible. Underlying Heartcell authorship remains conditional until the owner answers the clarification.

Then read [creation and origins](CREATION_ORIGINS_REVIEWED_01.md) and [gods and pantheons](GODS_PANTHEONS_REVIEWED_01.md) as earlier reviewed records, subject to that successor. Their files and receipts are preserved unchanged. In particular, Mephistopheles is now Cania only; the devouring-to-one correction supersedes conflicting mechanism explanations; no essence tether is valid; and the owner's limited Sundering assent replaces the earlier unresolved term scope. Maladomini's replacement ruler, the survivor's exact identity, the missing formulas/chapters and the Harmony-to-Choir mapping remain unresolved.

The original Cosmology, Matrix and World manuscripts remain source evidence. Original-source claims, mortal religion, owner statements and reviewer proposals retain separate authority. No missing chronology, named builder, cycle unit, Shardspire origin or Floor-97 merger has been supplied by inference.

This is Director/reviewer material. Planes, souls/death/resurrection, history, divine/class powers and campaign revelations still require their remaining reviews. Class/spell mechanics, runtime, human playtesting and publication have not been certified by these cosmology records.
''',encoding='utf-8',newline='\n')
    old=core.read_bytes();text=old.decode('utf-8');section=text[text.index('## Director Truth'):text.index('## Why the Dungeon Exists')]
    replacement='''## Director Truth — current owner corrections

The **Silent Ones are the Old Ones**. The owner’s current account says many attacked, were imprisoned, and then devoured one another until one primal one remained. Aethel gradually appeared around the prison after their confinement. The exact identity of that survivor in relation to Ul’nak, the Floor-97 Old God and the Interstice remains unresolved.

The **Pact manifested the prison**. The owner describes the Heartcell as a desperate attempt to find something that would silence the Old Ones: its changing rooms provide chaotic noises that keep them lulled. Calan’thir and Asmodeus have **not tied their essences**; the Pact itself became sentient.

**Underlying Heartcell authorship remains conditional.** The July account says the Silent Ones built the older machinery and the custodians found and modified it. The latest corrections and the later “Use the original version” message leave the controlling authorship account awaiting the owner’s clarification. Do not turn either account into an unqualified builder thesis, or invent a machinery/prison distinction to resolve it.

Use the [current reviewed companion](../director-only/cosmology/OWNER_RECONCILIATION_REVIEWED_01.md) for the exact owner statements, historical conflicts and retained dependencies. Earlier manuscripts, July locks and review receipts remain preserved evidence.

'''
    text=text.replace(section,replacement,1)
    before_sentence='Reality remains alive only while meaningful difference continues to produce possibility, choice, motion, history, memory, identity, and will. The Heartcell harvests and preserves the resonance created by consequential mortal action.'
    after_sentence=before_sentence+' This operating description does not settle the original builder or replace the owner’s containment purpose above. The Matrix distinguishes the dangerous ontological stillness from ordinary political peace, treaties and reconciliation.'
    assert text.count(before_sentence)==1;text=text.replace(before_sentence,after_sentence,1)
    preserved.mkdir();(preserved/'CANON_CORE.md').write_bytes(old);assert (preserved/'CANON_CORE.md').read_bytes()==old
    before_info=info(core);core.write_text(text,encoding='utf-8',newline='\n')
    unaffected=[row for row in bindings if row['path']!=before_info['path']];assert all(info(G/r['path'])==r for r in unaffected)
    inverse=text.replace(after_sentence,before_sentence,1).replace(replacement,section,1)
    # read_text normalizes CRLF; compare reconstructed logical text and preserved exact bytes independently.
    assert inverse==old.decode('utf-8')
    check.write_bytes(encoded({'reviewId':register['reviewId'],'recordedAtUtc':now,'candidate':info(candidate),'manuscript':info(companion),'readingOrder':info(current),'sourceReceipt':info(A/'COSMOLOGY_OWNER_RECONCILIATION_01_RECEIVED_DECISION.json'),'priorSourceCheck':info(A/'COSMOLOGY_OWNER_RECONCILIATION_01_APPLICATION_CHECK.json'),'exactOwnerQuotesVerified':11,'docxCitationOccurrencesVerified':34,'nonDocxEvidenceClassifiedAndVerified':len(resolved_checks),'localEditorialCorrections':edits,'remainingDependencies':13,'canonCoreChange':{'before':before_info,'preserved':info(preserved/'CANON_CORE.md'),'after':info(core),'inverseReconstructsOriginalText':True},'originalSourceAndHistoricalFilesUnchanged':len(unaffected),'dependentAuthorshipAdopted':False,'spellFlagsChanged':False,'publicExportEnabled':False,'sourceInformationDeleted':0,'fullCosmologyApproved':False}))
    print(json.dumps({'check':info(check),'candidate':info(candidate),'companion':info(companion),'originalBindingsUnchanged':len(unaffected),'currentDerivedFilesChanged':1,'dependentAuthorshipAdopted':False}))


if __name__=='__main__':main()
