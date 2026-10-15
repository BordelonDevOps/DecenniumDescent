"""Record completed local source reading and preserve original epilogue rules as pending work."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

G=Path('C:/Github/DecenniumDescent')
A=G/'docs/audit/2026-10-08/full-game'

def sha(raw): return hashlib.sha256(raw).hexdigest()
def read(path): return json.loads(path.read_bytes())
def bind(path):
    raw=path.read_bytes()
    return {'path':path.relative_to(G).as_posix(),'bytes':len(raw),'sha256':sha(raw)}
def write(path,value):
    with path.open('x',encoding='utf-8') as f:
        json.dump(value,f,ensure_ascii=False,indent=2)
        f.write('\n')

def main():
    out=A/'COSMOLOGY_GODS_PANTHEONS_01_LOCAL_FOLLOWUP_READING.json'
    inv=A/'ORIGINAL_COSMOLOGY_EPILOGUE_RULE_INVENTORY_01.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_GODS_PANTHEONS_SUBMISSION.json'
    assert all(not p.exists() for p in [out,inv,checkpoint])
    packet=A/'cosmology-gods-pantheons-01'
    originals=read(packet/'SOURCE_BINDINGS.json')
    for row in originals: assert bind(G/row['path'])==row
    doc='The Cosmology of Decennium Descent.docx'
    source=read(packet/'DOCX_PASSAGE_INDEX.json')['documents'][doc]
    def refs(indices):
        return [{'source':doc,**next(x for x in source if x['part']=='word/document.xml' and x['paragraphIndexZeroBased']==i)} for i in indices]
    findings=[
        {'id':'GPR-01','topic':'Serit death and later living teacher','evidence':refs([116,129,132,166]),'finding':'P116 narrates Serit\'s death and the Verdant bloom. P129 then presents traveling Mirrorsage Serit settling in Hearth Embers; P166 calls him Lantern Master Serit. No resurrection, reincarnation, second namesake or flashback explanation is supplied by these paragraphs.','disposition':'Unresolved continuity/ascension dependency. Do not invent a bridge; compare with actual GP-03 verdict.'},
        {'id':'GPR-02','topic':'First Choir count wording drift','evidence':refs([163,279,280,292]),'finding':'P163 uses Passion in a Choir-deliberation sequence. P279 says nine verses, one for each virtue plus Omega, whereas P280 and P292 list seven virtues and Q5 locks seven Choir members. This is not evidence of a newly authorized eighth/ninth member.','disposition':'Preserve exact wording; qualify as unresolved label/arithmetic issue, not a pantheon expansion. Check GPT disposition before any editorial repair.'},
        {'id':'GPR-03','topic':'Ul\'nak collective identity is explicitly asserted in the original','evidence':refs([154,202,242]),'finding':'P154 calls Ulnak the one mind of Old Ones fused after the Sundering; spelling variants occur. This is an exact original-source identity/chronology assertion, not merely a name-search inference. It still does not establish that the separate imprisoned Old God is the same being.','disposition':'Ask for/compare the bounded source classification. Preserve the explicit assertion; do not erase it with a blanket no-identity statement or elevate it into a new owner ruling.'},
        {'id':'GPR-04','topic':'Infernal association and repeated role names','evidence':refs([56,79,111,128,163,176,187,247,248,322]),'finding':'Cania/Mephistopheles is repeatedly explicit through later chapters. The duplicated Maladomini claim is not repaired. P187 also repeats Mephistopheles in the same council as Lord of Lies. These passages provide no independently named replacement ruler.','disposition':'Keep the roster dispute open. Later evidence strengthens Cania association, not a guessed replacement or dual-rule explanation.'},
        {'id':'GPR-05','topic':'Pact-driven changes to class performance','evidence':refs([178,179,180,181,182,183,204,220,221]),'finding':'Narrative chapters describe spell failure, altered class performance, honesty/intent variables and class-wide vocational change. These are source assertions with mechanical consequences; they have not been reconciled with current class candidates or registered combat/spellcasting sources.','disposition':'Carry to divine/class powers and history reviews. Do not silently implement moral-stat modifiers or pretend the original contains only flavor.'},
        {'id':'GPR-06','topic':'Epilogue rule layer and campaign epoch','evidence':refs([262,264,276,280,283,287,288,293,298,309,314,316,319,324]),'finding':'The original explicitly offers a post-Proof-War workbook with playable rules and campaign arcs. P276 even proposes the cosmograph at session zero. Those instructions are content within the original, not a decision that the current campaign begins after those events or that the newer authored mechanics are superseded.','disposition':'Finite original-rule inventory recorded separately; campaign epoch, revelation placement, mechanics and balance remain open.'},
        {'id':'GPR-07','topic':'Remaining player publication terminology','evidenceSource':'books/player/Decennium_Descent_Player_Rulebook_v6.docx','paragraphs':[10383,10387,10538,10552],'finding':'The current Appendix B still contains Sigil, Far Realm, Khazad-Dûr and Al-Qadim in named setting passages, despite other terminology migrations.','disposition':'Record for the naming/publication pass with exact passages; no automatic substitution or legal conclusion. Preserve originals.'},
        {'id':'GPR-08','topic':'Source chronology versus current public knowledge','evidence':refs([154,191,214,226,239,242,261,262,267,276]),'finding':'The original has a full forward saga, including public cosmic events and a successful Proof War. Its relation to the campaign\'s current epoch and owner-locked discovery limits is not established merely by preserving the book.','disposition':'Keep historical/campaign placement open. No current public reveal or global aftermath presumed.'},
    ]
    units=[
        ('EPI-01','Spiral Map and home-plane rest rewards',[270,271,272,273,274,275,276]),
        ('EPI-02','Seven Choir motif benefits',[279,280]),
        ('EPI-03','Unfinished starting vow',[282,283]),
        ('EPI-04','Living and Cracked Mask crafting, use and removal',[284,285,286,287,288]),
        ('EPI-05','Virtue/class pairings and Conflict Die',[290,291,292,293]),
        ('EPI-06','Archon petition and d12 response benefits',[295,296,297,298]),
        ('EPI-07','Sentinel encounter information boons',[299]),
        ('EPI-08','Shard Pendant of Xi',[302]),
        ('EPI-09','Concord Spear Fragment',[303]),
        ('EPI-10','Mirror of Potential Silence',[304]),
        ('EPI-11','Glove of Null Ink',[305]),
        ('EPI-12','Twelve dungeon chamber seeds',[307,308,309]),
        ('EPI-13','Residual Null exposure and Null Veil',[311,312,313,314,315]),
        ('EPI-14','Four Null flora and antidote formula',[315,316]),
        ('EPI-15','Rekindling Stars campaign arc',[319,320]),
        ('EPI-16','Conclave of Untitled Songs campaign arc',[319,321]),
        ('EPI-17','Devil\'s Signature campaign arc',[319,322]),
    ]
    inventory={'inventoryId':'ORIGINAL-COSMOLOGY-EPILOGUE-01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'source-inventory-complete; domain-reconciliation-and-behavior-review-pending','source':bind(G/doc),'scope':'All discrete rules/toolbox groups in original Chapter XII P269-P324, grouped into seventeen units; narratives before this chapter remain separately relevant.','units':[{'id':ident,'title':title,'evidence':refs(indices),'status':'preserved-source-not-promoted','implementedByThisPass':False,'requires':'Relevant current system source comparison and actual GPT conference before candidate implementation.'} for ident,title,indices in units],'count':len(units),'groupCounts':{'choirMotifs':7,'listedVirtuePairings':7,'relics':4,'chamberSeeds':12,'flora':4,'campaignArcs':3},'sourceInformationDeleted':0,'fullCosmologyApproved':False,'runtimeApproved':False}
    write(inv,inventory)
    reading={'reviewId':'COSMOLOGY-GODS-PANTHEONS-01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'local-full-original-and-appendix-prose-read; actual-GPT-response-still-pending-at-last-observation','submittedPacketCoverageIsHistorical':True,'newReadAfterSubmission':{'originalCosmologyMainDocumentParagraphs':[125,337],'playerAppendixBAdditionalRanges':[[10120,10284],[10417,10603],[10628,10678]]},'cumulativeRead':{'originalCosmologyMainDocumentParagraphs':[0,337],'matrixMainDocumentParagraphs':[0,363],'survivingWorldMainDocumentParagraphs':[0,93],'currentPlayerAppendixBParagraphs':[9976,10678]},'readingLimits':['Text-run semantic reading, not page rendering.','Matrix equation symbols are incompletely represented in the prior extractor; original DOCX is preserved and no mathematical correctness is certified.','Class candidates were screened for exact named references and relevant metadata, not fully rereviewed.','Full-source reading does not grant unregistered authority or approve every contained rule.'],'sourceFilesStillUnchanged':len(originals),'findings':findings,'epilogueInventory':bind(inv),'sourceInformationDeleted':0,'ruleChanges':0,'nextAction':'Retrieve and verify the same live GPT request. Compare the verdict against these later-source findings and submit a bounded follow-up if any consequential item is missed.'}
    write(out,reading)
    state=read(A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_CREATION_ORIGIN_REVIEW.json')
    previous=bind(A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_CREATION_ORIGIN_REVIEW.json')
    state.update({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'previousCheckpoint':previous,'goalTurnClassification':'progress','previousGoalTurnClassification':'progress: saved backup pushed and verified','status':'Gods/pantheons source comparison submitted to actual GPT; local full original cosmology and current Appendix B prose reading complete.','activeGptReview':{'reviewId':'COSMOLOGY-GODS-PANTHEONS-01','status':'response observed running on existing Chrome tab','tabId':'125745968','conversationTitle':'Calibration Review Part 2','submission':bind(A/'COSMOLOGY_GODS_PANTHEONS_01_SUBMISSION.json'),'lastObservation':'Same tab displayed active analysis and Stop during this goal turn; do not infer completion or resend from this checkpoint.'},'cosmologyGodsPantheonsReview':{'preparation':bind(A/'COSMOLOGY_GODS_PANTHEONS_01_PREPARATION.json'),'localFollowupReading':bind(out),'epilogueRuleInventory':bind(inv),'proposalRows':9,'newLocalFindings':len(findings),'acceptedByGpt':False,'originalSourcesUnchanged':71,'fullCosmologyApproved':False},'latestProgressBackup':bind(G/'docs/audit/2026-10-15/github-snapshot-cosmology/PUSH_RECEIPT.json'),'usageAtLatestCheck':{'usedPercent':20,'window':'weekly','ownerStopAtUsedPercent':50},'safeNextActions':['Read the actual COSMOLOGY-GODS-PANTHEONS-01 response on the same Chrome tab and preserve/verify its downloaded evidence.','Compare exact verdict to GPR-01 through GPR-08; confer about any missed consequential source question before implementation.','After the gods identity comparison, continue ordered planes, souls/death/resurrection, history, divine/class powers and campaign revelations.','Keep the original Chapter XII rule inventory pending against registered source systems; preserve all seventeen units.','Continue the thirteen copy-release behavior examples and the wider unfinished game work recorded in prior checkpoint.'],'sourceInformationDeleted':0,'wholeGameFlowConfirmed':False,'cosmologyReviewed':False})
    write(checkpoint,state)
    print(json.dumps({'reading':bind(out),'inventory':bind(inv),'checkpoint':bind(checkpoint),'sourceFilesVerifiedUnchanged':len(originals),'newLocalFindings':len(findings),'epilogueUnits':len(units)}))

if __name__=='__main__':main()
