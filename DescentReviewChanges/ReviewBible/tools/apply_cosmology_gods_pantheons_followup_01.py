"""Verify corrected evidence and assemble an exact, scoped Director companion."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib, json, os, re, zipfile, xml.etree.ElementTree as ET
from apply_di7_ap_as_01 import G, R, A, info, encoded


def walk_citations(value):
    if isinstance(value,dict):
        if {'path','part','paragraphIndexZeroBased','paragraphTextSha256'} <= value.keys(): yield value
        for child in value.values(): yield from walk_citations(child)
    elif isinstance(value,list):
        for child in value: yield from walk_citations(child)


def main():
    download = Path('C:/Users/cbord/Downloads/COSMOLOGY_GODS_PANTHEONS_FOLLOWUP_01_Addendum_and_Evidence.zip')
    archive = A/download.name
    root = A/'cosmology-gods-pantheons-followup-01-received'
    receipt = A/'COSMOLOGY_GODS_PANTHEONS_FOLLOWUP_01_RECEIVED_DECISION.json'
    application = A/'COSMOLOGY_GODS_PANTHEONS_FOLLOWUP_01_APPLICATION_CHECK.json'
    candidate = R/'data/director/cosmology/gods_pantheons_reviewed_01.json'
    manuscript = R/'docs/director-only/cosmology/GODS_PANTHEONS_REVIEWED_01.md'
    assert all(not p.exists() for p in [archive,root,receipt,application,candidate,manuscript])
    raw = download.read_bytes()
    assert len(raw)==58279 and hashlib.sha256(raw).hexdigest()=='f099da70e910b586f36db22d36e21459dce563a36c3f5ec35637520e784a94a7'
    names = {'COSMOLOGY_GODS_PANTHEONS_01_REGISTER_CORRECTED.json','FOLLOWUP_DISPOSITIONS.json','VERDICT.md','SOURCE_HASHES.json','SEMANTIC_COVERAGE.json','EVIDENCE_MANIFEST.json'}
    with zipfile.ZipFile(download) as z:
        assert set(z.namelist())==names and len(z.namelist())==len(names)
        payloads = {name:z.read(name) for name in names}
    manifest = json.loads(payloads['EVIDENCE_MANIFEST.json'])
    assert len(manifest['files'])==5
    for row in manifest['files']:
        b=payloads[row['filename']]
        assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
    submitted = A/'DD_Cosmology_Gods_Pantheons_Followup_01.zip'
    assert manifest['submission']['sha256']==info(submitted)['sha256']
    assert manifest['submission']['bytes']==submitted.stat().st_size
    register = json.loads(payloads['COSMOLOGY_GODS_PANTHEONS_01_REGISTER_CORRECTED.json'])
    followup = json.loads(payloads['FOLLOWUP_DISPOSITIONS.json'])
    prior = json.loads((A/'cosmology-gods-pantheons-01-received/COSMOLOGY_GODS_PANTHEONS_01_REGISTER.json').read_bytes())
    hashes = json.loads(payloads['SOURCE_HASHES.json'])
    assert hashes==json.loads((A/'cosmology-gods-pantheons-01/SOURCE_HASHES.json').read_bytes()) and len(hashes)==71
    for name,sha in hashes.items():
        assert hashlib.sha256((G/name).read_bytes()).hexdigest()==sha,name
        assert hashlib.sha256((A/'cosmology-gods-pantheons-01/sources'/name).read_bytes()).hexdigest()==sha,name
    assert len(register['rows'])==9 and len(register['reviewedSummaries'])==4 and len(register['unresolvedDependencies'])==17
    assert len(followup['gprDispositions'])==8
    assert register['reviewedSummaries']==prior['reviewedSummaries']
    assert register['unresolvedDependencies'][:9]==prior['unresolvedDependencies']
    assert register['generalCosmologyAuthorityPromoted'] is False and register['wholeGameApproved'] is False
    citations = list(walk_citations(register))+list(walk_citations(followup))
    cache={}; verified=[]
    n='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    for citation in citations:
        path=G/citation['path'];assert path.resolve().is_relative_to(G.resolve())
        key=(citation['path'],citation['part'])
        if key not in cache:
            with zipfile.ZipFile(path) as z: xml=ET.fromstring(z.read(citation['part']))
            cache[key]=[''.join(t.text or '' for t in p.iter(n+'t')) for p in xml.iter(n+'p')]
        actual=cache[key][citation['paragraphIndexZeroBased']]
        assert hashlib.sha256(actual.encode()).hexdigest()==citation['paragraphTextSha256'],citation
        excerpt=citation.get('excerpt','')
        normalized=' '.join(actual.split())
        assert ' '.join(excerpt.rstrip('…').split()) in normalized,citation
        verified.append({'path':citation['path'],'part':citation['part'],'paragraphIndexZeroBased':citation['paragraphIndexZeroBased'],'paragraphTextSha256':citation['paragraphTextSha256']})
    assert len(citations)==316
    unique={(x['path'],x['part'],x['paragraphIndexZeroBased']) for x in verified}
    assert len(unique)==157
    dom=A/'COSMOLOGY_GODS_PANTHEONS_FOLLOWUP_01_RETURNED_DOM.txt'
    assert 'Response complete' in dom.read_text(encoding='utf-8') and download.name in dom.read_text(encoding='utf-8')
    now=datetime.now(timezone.utc).isoformat()
    archive.write_bytes(raw);root.mkdir()
    for name,b in payloads.items():(root/name).write_bytes(b)
    decision={
        'reviewId':register['reviewId'],'recordedAtUtc':now,'status':'corrected successor received; exact source citations verified; eight follow-up findings retained',
        'archive':info(archive),'files':[info(root/name) for name in sorted(names)],
        'submission':info(A/'COSMOLOGY_GODS_PANTHEONS_FOLLOWUP_01_SUBMISSION.json'),
        'receivedDOM':info(dom),'visibleProof':info(A/'COSMOLOGY_GODS_PANTHEONS_FOLLOWUP_01_RETURNED.png'),
        'manifestPayloadsVerified':5,'currentAndFrozenSourceHashesVerified':71,
        'paragraphCitationOccurrencesVerified':len(verified),'uniqueParagraphCitationsVerified':len(unique),
        'citationValidationScope':'Exact source paragraph text hashes and normalized excerpts; semantic decisions are separately bounded by the nine GP and eight GPR reviews. This is not a full cosmology approval.',
        'fourSummariesUnchanged':True,'priorNineDependenciesRetained':True,'totalDependencies':17,
        'returnedBackupMetadataCorrection':{'returnedField':register['currentProgressBackupCommit'],'actualLatestVerifiedBackup':'18c6e3ae8b3c1d391dd91121693931657ae9c98f','treatment':'Returned metadata names the older review baseline. Preserve it as historical reviewer metadata; use the current local push receipt for actual GitHub status.'},
        'earlierDirectorCoverageCaution':'The earlier return listed Director paragraph positions that do not generally identify the claimed hierarchy material under the exact XML indexing. Those positions are not used as support in this companion. The corrected successor has narrower coverage; no full Director rereview is claimed.',
        'sourceDoctrineChanges':0,'sourceInformationDeleted':0,'fullCosmologyApproved':False,'wholeGameApproved':False,
    }
    receipt.write_bytes(encoded(decision))
    summaries={k:v['text'] for k,v in register['reviewedSummaries'].items()}
    doc={
        'schemaVersion':'1.0','reviewId':register['reviewId'],
        'status':'reviewed scoped editorial companion; no general cosmology authority promotion',
        'audience':'Director/reviewer; contains hidden cosmology and an embedded public wording example, not a player export',
        'authority':info(root/'COSMOLOGY_GODS_PANTHEONS_01_REGISTER_CORRECTED.json'),'receivedDecision':info(receipt),
        'summaries':summaries,'issues':register['rows'],'identityInventory':register['reviewedIdentityInventory'],
        'factBeliefRevelation':register['factBeliefRevelation'],'unresolvedDependencies':register['unresolvedDependencies'],
        'followupDispositions':followup['gprDispositions'],'matrixFormulaSourceGap':followup['matrixFormulaSourceGap'],
        'sourceHashes':hashes,'semanticCoverage':json.loads(payloads['SEMANTIC_COVERAGE.json']),
        'originalSourcesChanged':False,'generalCosmologyAuthorityCreated':False,'runtimeEnabled':False,'fullCosmologyApproved':False,
    }
    candidate.parent.mkdir(parents=True,exist_ok=True);candidate.write_bytes(encoded(doc))
    def link(path):return os.path.relpath(path,manuscript.parent).replace('\\','/')
    lines=['# Gods and pantheons — reviewed reading companion','',
        '**Director and reviewer material.** This companion preserves the reviewed distinctions among the Choir, worship masks, archons, Thrones, aspirants and class patrons. It includes hidden setting material. The public paragraph is a wording example, not a player export. Original books remain unchanged; no general cosmology domain or class mechanic is promoted.','',
        f'Authority: [corrected register]({link(root/"COSMOLOGY_GODS_PANTHEONS_01_REGISTER_CORRECTED.json")}); [eight follow-up dispositions]({link(root/"FOLLOWUP_DISPOSITIONS.json")}); [verification receipt]({link(receipt)}); [structured companion]({link(candidate)}). The earlier return remains preserved with its citation errors.','']
    for key,title in [('publicFaith','Public faith wording example'),('directorIdentityBoundary','Director identity boundary'),('umbrinWording','Umbrin lore and interpretation'),('infernalRosterPolicy','Infernal roster and public terms')]:
        lines.extend(['## '+title,'',summaries[key],''])
    lines.extend(['## Reviewed source decisions','','These decisions retain their original authority limits. Paragraph numbers below refer to zero-based paragraphs in word/document.xml, including blanks and tables. The corrected register supplies exact hashes and excerpts.',''])
    for row in register['rows']:
        lines.extend(['### '+row['id']+' — '+row['topic'],'',row['decision'],''])
        grouped={}
        for citation in row['support'].get('docx',[]):grouped.setdefault(citation['path'],set()).add(citation['paragraphIndexZeroBased'])
        for path,paragraphs in grouped.items():lines.append('- ['+Path(path).name+']('+link(G/path)+'): P'+', P'.join(map(str,sorted(paragraphs)))+'.')
        lines.append('')
    lines.extend(['## Follow-up findings','','These are recorded consequences and open seams, not permission to invent missing history.',''])
    for row in followup['gprDispositions']:lines.extend(['### '+row['id'],'',row['ruling'],''])
    lines.extend(['## Remaining dependencies','','The nine earlier dependencies remain, with eight additional items made explicit. Their presence does not expand the First Choir or promote a source narrative into current mechanics.',''])
    for row in register['unresolvedDependencies']:
        lines.append('- **'+row['id']+':** '+row['issue']+' '+row.get('status',row.get('whenNeeded','')))
    lines.extend(['','## Next comparisons','',
        'Proceed through planes; souls, death and resurrection; history; divine and class powers; then campaign revelations. The original forward saga and epilogue do not by themselves establish the present campaign epoch.',
        f'The [preliminary plane concordance]({link(A/"COSMOLOGY_PLANES_SOURCE_CONCORDANCE_01.json")}) identifies map and travel dependencies. It has not yet received its own GPT conference.',
        f'The [Matrix formula source check]({link(A/"COSMOLOGY_MATRIX_FORMULA_SOURCE_CHECK_01.json")}) records gaps already present in the original Word XML. No replacement equations are invented.',
        'New owner decisions must come from actual owner direction. GPT recommendations labeled as owner locks do not establish approval. Existing original-source words and earlier receipts remain available for comparison.',''])
    manuscript.parent.mkdir(parents=True,exist_ok=True);manuscript.write_bytes(('\n'.join(lines)).encode())
    saved=json.loads(candidate.read_bytes());text=manuscript.read_text(encoding='utf-8')
    assert saved['summaries']==summaries and all(text.count(s)==1 for s in summaries.values())
    assert saved['issues']==register['rows'] and saved['unresolvedDependencies']==register['unresolvedDependencies']
    assert saved['followupDispositions']==followup['gprDispositions']
    links=re.findall(r'\]\(([^)]+)\)',text)
    for target in links:assert (manuscript.parent/target).resolve().is_file(),target
    for name,sha in hashes.items():assert hashlib.sha256((G/name).read_bytes()).hexdigest()==sha
    application.write_bytes(encoded({'recordedAtUtc':now,'reviewId':register['reviewId'],'status':'exact corrected editorial companion assembled',
        'authority':info(root/'COSMOLOGY_GODS_PANTHEONS_01_REGISTER_CORRECTED.json'),'candidate':info(candidate),'manuscript':info(manuscript),
        'exactSummariesVerified':4,'unchangedPriorSummaryTexts':4,'issueDispositions':9,'followupDispositions':8,'unresolvedDependenciesRetained':17,
        'paragraphCitationOccurrencesVerified':len(verified),'uniqueParagraphCitationsVerified':len(unique),'verifiedCitations':verified,
        'manuscriptLinksVerified':len(links),'originalSourceHashesUnchanged':71,'sourceInformationDeleted':0,
        'classMechanicsChanged':False,'generalCosmologyAuthorityCreated':False,'publicExportCreated':False,'fullCosmologyApproved':False}))
    print(json.dumps({'receipt':info(receipt),'application':info(application),'candidate':info(candidate),'manuscript':info(manuscript),'citationOccurrencesVerified':len(verified),'originalSourcesUnchanged':71}))


if __name__=='__main__':main()
