"""Verify Q6's frozen return, classify its citations, and apply a current Director successor."""
from copy import deepcopy
from datetime import datetime,timezone
from zipfile import ZipFile
from xml.etree import ElementTree as E
import hashlib,json
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())
def digest(b):return hashlib.sha256(b).hexdigest()

def main():
    review='COSMOLOGY-Q6-LATER-LOCK-01';now=datetime.now(timezone.utc).isoformat()
    root=A/'cosmology-q6-later-lock-01-received';submitted=A/'cosmology-q6-later-lock-01'
    archive=A/'COSMOLOGY_Q6_LATER_LOCK_01_Addendum_and_Evidence.zip'
    candidate=R/'data/director/cosmology/q6_later_lock_reviewed_01.json'
    companion=R/'docs/director-only/cosmology/Q6_LATER_LOCK_REVIEWED_01.md'
    receipt=A/'COSMOLOGY_Q6_LATER_LOCK_01_RECEIVED_DECISION.json'
    check=A/'COSMOLOGY_Q6_LATER_LOCK_01_APPLICATION_CHECK.json'
    current=R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md'
    preserved=A/'before-q6-later-lock-01'
    assert all(not p.exists() for p in [candidate,companion,receipt,check,preserved])
    assert info(archive)['bytes']==15130 and info(archive)['sha256']=='f72ec4b82e5c73934352df25cde796a2001d947824952ec3c6788509737bf168'
    manifest=read(root/'EVIDENCE_MANIFEST.json')
    packet=A/'DD_Cosmology_Q6_Later_Lock_01.zip'
    assert info(packet)['bytes']==manifest['submission']['bytes'] and info(packet)['sha256']==manifest['submission']['sha256']
    with ZipFile(archive) as z:
        assert len(z.namelist())==6 and z.testzip() is None
        for p in root.iterdir():assert p.read_bytes()==z.read(p.name)
    for row in manifest['payloads']:
        p=root/row['filename'];assert p.stat().st_size==row['bytes'] and digest(p.read_bytes())==row['sha256']
    bindings=read(submitted/'SOURCE_BINDINGS.json')
    returned=read(root/'SOURCE_HASHES.json')
    assert returned['sources']==bindings and len(bindings)==28
    hc_preserved=read(A/'before-heartcell-owner-update-02/PRESERVATION_MANIFEST.json')
    source_checks=[]
    for row in bindings:
        frozen=submitted/'sources'/row['path'];b=frozen.read_bytes()
        assert len(b)==row['bytes'] and digest(b)==row['sha256']
        cur=info(G/row['path']);same=cur==row
        if not same:
            prior=next(x for x in hc_preserved if x['path']==row['path'])
            assert prior['sha256']==row['sha256']
            assert digest((G/prior['preservedCopy']).read_bytes())==row['sha256']
        source_checks.append({'submitted':row,'frozenCopyVerified':True,'current':cur,'currentUnchanged':same,
            'changedSinceSubmissionReason':None if same else 'Preserved current pointer/derived core updated by HEARTCELL-OWNER-UPDATE-02; verified against its preservation manifest.'})
    assert sum(not x['currentUnchanged'] for x in source_checks)==2
    original=read(root/'REGISTER.json');reg=deepcopy(original)
    assert len(reg['issues'])==8
    citations=[]
    for issue,e in [('authority',x) for x in reg['authorityFinding']['evidence']]+[(i['id'],x) for i in reg['issues'] for x in i['evidence']]:
        p=submitted/e['path'];rel=e['path'].removeprefix('sources/')
        bound=next(x for x in bindings if x['path']==rel)
        if 'jsonPointer' in e:
            value=read(p)
            for part in e['jsonPointer'].strip('/').split('/'):
                part=part.replace('~1','/').replace('~0','~');value=value[int(part)] if isinstance(value,list) else value[part]
            actual=value if isinstance(value,str) else json.dumps(value,ensure_ascii=False)
        else:
            lines=p.read_text(encoding='utf-8').splitlines()
            assert 1<=e['firstLineOneBased']<=e['lastLineOneBased']<=len(lines)
            value='\n'.join(lines[e['firstLineOneBased']-1:e['lastLineOneBased']]);actual=value
        exact=e['excerpt'] in actual
        e['evidenceKind']='verbatim-contained-source-excerpt' if exact else 'reviewer-summary-or-joined-excerpts; not a verbatim quotation'
        e['submittedSourceBinding']=bound
        e['actualBoundSourceValue']=value
        citations.append({'issue':issue,'path':rel,'locator':e.get('jsonPointer') or [e['firstLineOneBased'],e['lastLineOneBased']],
            'evidenceKind':e['evidenceKind'],'locatorResolved':True,'sourceHashVerified':True,
            'semanticAssessment':'Supports disposition within the bounded source scope; historical pending-source-preference text is superseded by Heartcell owner update02.'})
    docx=submitted/'sources/docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx'
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    with ZipFile(docx) as z:xml=E.fromstring(z.read('word/document.xml'))
    paragraphs=[''.join(t.text or '' for t in p.findall('.//w:t',ns)) for p in xml.findall('.//w:p',ns)]
    paragraphs_checked=[]
    for e in reg['issues'][6]['evidence'][:3]:
        value=e['actualBoundSourceValue'];assert isinstance(value,dict)
        assert paragraphs[value['paragraphIndexZeroBased']]==value['text']
        assert digest(value['text'].encode())==value['textSha256']
        paragraphs_checked.append({'paragraphIndexZeroBased':value['paragraphIndexZeroBased'],'exactDocxTextVerified':True})
    hc=R/'data/director/cosmology/heartcell_owner_update_02.json'
    assert read(hc)['sourcePreferenceAmbiguityClosed']
    qualifier='Later owner update HEARTCELL-OWNER-UPDATE-02 settles source preference: original cosmology manuscripts first, with explicit owner corrections. Underlying Heartcell authorship remains unresolved, but no longer awaits the old source-preference clarification. The Q6 domain is a specific owner-locked endgame rule; it does not become general cosmology authority or settle entity identity. The new Research/taint/Hunt rules do not by themselves identify the Old God.'
    derived={'reviewId':review,'recordedAtUtc':now,'register':reg,'registerStatus':'Historical reviewed findings with current qualification below',
        'currentQualification':qualifier,'currentOwnerUpdate':info(hc),
        'archive':info(archive),'semanticCoverage':read(root/'SEMANTIC_COVERAGE.json'),
        'sourceInformationDeleted':0,'newMechanicsAdopted':False,'identityMerged':False,'publicExportEnabled':False,
        'fullCosmologyApproved':False,'humanPlaytestApproved':False}
    candidate.write_bytes(encoded(derived))
    text=(root/'DIRECTOR_COMPANION.md').read_text(encoding='utf-8')
    tick=chr(96)
    old=f"Underlying Heartcell machinery authorship remains **conditional** pending the owner's already-requested clarification of the later {tick}Use the original version ...{tick} message. Nothing in Q6 resolves that question."
    new='The later [Heartcell owner update](HEARTCELL_OWNER_UPDATE_02.md) settles source preference: original cosmology manuscripts first, with explicit owner corrections. Underlying Heartcell authorship remains unresolved, but no longer awaits the old source-preference clarification. The Q6 owner lock governs the specific endgame path; it supplies no general cosmology authority or entity identification.'
    assert text.count(old)==1
    text=text.replace('## Pending Heartcell authorship','## Current Heartcell scope',1).replace(old,new,1)
    text=text.replace('- pending Heartcell-builder clarification.','- unresolved underlying Heartcell authorship, using the settled original-source preference.',1)
    text+='\n## Traceable evidence\n\nThe returned GPT archive is preserved unchanged. [The structured successor](../../../data/director/cosmology/q6_later_lock_reviewed_01.json) distinguishes reviewer paraphrases from verbatim excerpts and includes the actual bound source values. All 28 submitted source hashes were verified against the frozen packet; the current reading pointer and derived Canon Core had subsequently changed under the preserved Heartcell owner update. Three Interstice paragraphs were also checked against the actual Director DOCX. No historical manuscript or review receipt was rewritten.\n'
    companion.write_text(text,encoding='utf-8',newline='\n')
    receipt.write_bytes(encoded({'reviewId':review,'recordedAtUtc':now,'archive':info(archive),'inputArchive':info(packet),
        'payloadsVerified':6,'boundSourcesVerified':28,'issues':8,'terminalCapture':info(A/'COSMOLOGY_Q6_LATER_LOCK_01_TERMINAL_THREAD_CAPTURE.json'),
        'downloadObservation':'Browser download-event/snapshot timed out, but Downloads held exact15130byte archive with expected SHA256; no second download requested.',
        'sourcePreferenceSuccessor':info(hc),'candidate':info(candidate),'companion':info(companion),
        'scope':'Director clarification and current owner qualification only; no identity merger, combat math or full-domain closure'}))
    before=info(current);prior=current.read_bytes();preserved.mkdir();(preserved/current.name).write_bytes(prior)
    old_current=current.read_text(encoding='utf-8')
    sentence='Q6 has a captured terminal verdict awaiting its evidence-archive verification.'
    replacement='The [Q6 endgame companion](Q6_LATER_LOCK_REVIEWED_01.md) is verified and applied: it distinguishes the registered crystal path and public ceiling from open identity and full encounter mechanics.'
    assert old_current.count(sentence)==1
    new_current=old_current.replace(sentence,replacement,1);assert new_current.replace(replacement,sentence,1)==old_current
    current.write_text(new_current,encoding='utf-8',newline='\n')
    check.write_bytes(encoded({'reviewId':review,'recordedAtUtc':now,'archive':info(archive),'receipt':info(receipt),
        'sourceChecks':source_checks,'boundSourcesVerified':28,'currentUnchangedBeforeAdoption':26,
        'citationOccurrences':len(citations),'citationChecks':citations,'exactDirectorParagraphs':paragraphs_checked,
        'candidate':info(candidate),'companion':info(companion),
        'readingOrderChange':{'before':before,'preserved':info(preserved/current.name),'after':info(current),
            'operations':[{'old':sentence,'replacement':replacement}],'inverseReconstructsOriginalText':True},
        'sourcePreferenceQualification':qualifier,'originalManuscriptsChanged':False,'sourceInformationDeleted':0,
        'runtimeApproved':False,'publicExportEnabled':False,'identityMerged':False}))
    print(json.dumps({'check':info(check),'receipt':info(receipt),'citations':len(citations),'boundSources':28,'currentUnchangedAtReview':26,'companion':info(companion)}))

if __name__=='__main__':main()

