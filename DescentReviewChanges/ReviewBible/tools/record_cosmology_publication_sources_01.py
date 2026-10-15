"""Bind current publication evidence for COS-A05 and the next pantheon comparison."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib,json,zipfile,xml.etree.ElementTree as ET
from apply_di7_ap_as_01 import G,A,info,encoded

def main():
    root=A/'cosmology-publication-source-check-01'
    receipt=A/'COSMOLOGY_PUBLICATION_SOURCE_CHECK_01.json'
    assert not root.exists() and not receipt.exists()
    names=['books/player/Decennium_Descent_Player_Rulebook_v6.docx','docs/manuals/Decennium_Descent_Player_Rulebook_v6.docx','DescentReviewChanges/ReviewBible/books/player/Decennium_Descent_Player_Rulebook_v6.docx','rulebook_output.txt','DescentReviewChanges/ReviewBible/rulebook_output.txt','docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx','DescentReviewChanges/ReviewBible/docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx']
    originals={n:(G/n).read_bytes() for n in names}
    assert originals[names[0]]==originals[names[1]]==originals[names[2]]
    assert originals[names[3]]==originals[names[4]]
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    def paragraphs(name):
        with zipfile.ZipFile(G/name) as z:
            doc=ET.fromstring(z.read('word/document.xml'))
        return [''.join(n.text or '' for n in p.findall('.//w:t',ns)) for p in doc.findall('.//w:p',ns)]
    player=paragraphs(names[0]); director=paragraphs(names[5])
    checks={
        'renamedAppendix':(9976,'Appendix B: Faiths and Cosmologies of Aethel'),
        'mortalTheologyDisclaimer':(9977,'mortal theology, not objective cosmic history'),
        'luminaUmbraAbstractions':(9983,'twin abstractions of creation'),
        'worshipMasks':(10018,'worship masks mortals place on real cosmic forces'),
        'fifteenfoldFolkScope':(10041,'this appendix records that faith'),
        'mortalPlanarDiagram':(10113,'This Wheel of Testimony is a teaching tool'),
        'folkInfernalConflict':(10319,'Temple historians call the War of Chains and Teeth'),
        'infernalConflictPactConsequence':(10319,'Every escalation strains the Divine Pact')}
    anchors=[]
    for label,(i,phrase) in checks.items():
        assert phrase in player[i],label
        anchors.append({'id':label,'path':names[0],'part':'word/document.xml','paragraphIndexZeroBased':i,'fullText':player[i],'textSha256':hashlib.sha256(player[i].encode()).hexdigest(),'observedPhrase':phrase})
    extracts=[]
    for name in names[3:5]:
        raw=originals[name];assert raw[:2]==b'\xff\xfe'
        text=raw.decode('utf-16')
        for label,(_,phrase) in checks.items():assert phrase in text,(name,label)
        extracts.append({'path':name,'encoding':'UTF-16LE with BOM','allEightPatchAnchorPhrasesPresent':True})
    assert 'a truce, not an ending' in director[913]
    def rows(pars,indices):return [{'part':'word/document.xml','paragraphIndexZeroBased':i,'text':pars[i],'textSha256':hashlib.sha256(pars[i].encode()).hexdigest()} for i in indices]
    passages={'scope':'Exact text-run paragraphs, not a rendered layout review. Full originals are preserved separately.','playerAppendixB':{'source':names[0],'paragraphs':rows(player,range(9976,len(player)))},'directorPeaceContext':{'source':names[5],'paragraphs':rows(director,range(911,919))}}
    root.mkdir();preserved=[]
    for name,raw in originals.items():
        p=root/'sources'/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
        assert p.read_bytes()==raw
        preserved.append({**info(G/name),'preservedCopy':p.relative_to(G).as_posix()})
    (root/'PRESERVATION_MANIFEST.json').write_bytes(encoded(preserved))
    (root/'EXACT_PUBLICATION_PASSAGES.json').write_bytes(encoded(passages))
    report={'reviewId':'COSMOLOGY-PUBLICATION-SOURCE-CHECK-01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'previousAuthoringCheckpoint':info(A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_COPY_SOURCE_AND_COSMOLOGY_REVIEW.json'),'authorityConference':info(A/'COSMOLOGY_SOURCE_AUTHORITY_01_RECEIVED_DECISION.json'),'status':'current publication patch anchors located and verified; full publication/cosmology review remains open','sourceBindings':preserved,'preservationManifest':info(root/'PRESERVATION_MANIFEST.json'),'passages':info(root/'EXACT_PUBLICATION_PASSAGES.json'),'byteIdenticalGroups':[names[:3],names[3:5]],'directorMainAndReviewBibleIdentical':originals[names[5]]==originals[names[6]],'patchAnchors':anchors,'livingExtractChecks':extracts,'COS_A05_Disposition':'Actual current Player Rulebook bytes and both living extracts contain the eight specified patch anchors. This independently supports the reviewer’s stale-status disposition for the old TODO row. It does not certify every remaining paragraph, rendering or player-information boundary. No original status row was overwritten here.','directorNotebookSourceLimit':'Local Complete Director Edition P913 independently contains the truce-not-ending wording. This is not proof that the reviewer’s differently titled notebook document is byte-identical; that exact notebook source binding is still requested in the active creation review.','semanticReadingCompleted':{'player':[[9976,10119],[10318,10326]],'director':[[894,918]],'remainingAppendixParagraphs':'Extracted and indexed, not all semantically reviewed.'},'observationsForNextConference':['Player P9983 contains a folk-attributed consciousness narrative and P9985 repeats much of that narrative. Preserve both; any editing requires separate exact comparison, not automatic duplicate deletion.','Player P10319–10325 uses War of Chains and Teeth and Nine Infernal Courts. Do not automatically replace these current publication names with older source labels.','The canon registry references the Player Rulebook for class-identity, paths and racial domains; these references do not create general cosmology authority.'],'activeGptReview':{'reviewId':'COSMOLOGY-CREATION-ORIGIN-01','submission':info(A/'COSMOLOGY_CREATION_ORIGIN_01_SUBMISSION.json'),'browserId':'3','tabId':'125745968','latestObservation':'Tab remains listed as Calibration Review Part 2. DOM and screenshot observation timed out; completion state is unknown. Do not resend or restart from an observation timeout.'},'latestUsageUsedPercent':17,'ownerStopAtUsedPercent':50,'sourceInformationDeleted':0,'sourceDoctrineChanges':0,'publicProjectionCertified':False,'cosmologyCompleted':False,'fullFeatCopyBehaviorValidated':False,'nextActions':['Reobserve the same GPT creation review, preserving terminal evidence if available.','Use these exact current publication bytes in the gods/pantheons comparison and COS-A05 status follow-up.','Continue the thirteen unexecuted copy-release behaviors and remaining game development; the publication check does not close those gates.']}
    receipt.write_bytes(encoded(report))
    print(json.dumps({'receipt':info(receipt),'sourcesPreserved':len(preserved),'patchAnchorsVerified':len(anchors),'livingExtractsVerified':len(extracts),'sourceChanges':0,'fullPublicationReviewed':False}))

if __name__=='__main__':main()
