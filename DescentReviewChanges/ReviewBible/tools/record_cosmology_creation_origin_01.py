"""Preserve origin review and assemble its exact scoped Director reading companion."""
from datetime import datetime,timezone
from pathlib import Path
import hashlib,json,os,zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded

def main():
    downloaded=Path('C:/Users/cbord/Downloads/COSMOLOGY_CREATION_ORIGIN_01_Addendum_and_Evidence.zip')
    archive=A/downloaded.name;root=A/'cosmology-creation-origin-01-received'
    receipt=A/'COSMOLOGY_CREATION_ORIGIN_01_RECEIVED_DECISION.json'
    application=A/'COSMOLOGY_CREATION_ORIGIN_01_APPLICATION_CHECK.json'
    candidate=R/'data/director/cosmology/creation_origins_reviewed_01.json'
    manuscript=R/'docs/director-only/cosmology/CREATION_ORIGINS_REVIEWED_01.md'
    assert all(not p.exists() for p in [archive,root,receipt,application,candidate,manuscript])
    raw=downloaded.read_bytes()
    assert len(raw)==16458 and hashlib.sha256(raw).hexdigest()=='684c90b962d21d04b43e2a924b68443455fa3cb59807a2e7bfdd2057ac7f29f8'
    with zipfile.ZipFile(downloaded) as z:
        names={'COSMOLOGY_CREATION_ORIGIN_01_REGISTER.json','COSMOLOGY_CREATION_ORIGIN_01_VERDICT.md','SOURCE_HASHES.json','SEMANTIC_COVERAGE.json','EVIDENCE_MANIFEST.json'}
        assert set(z.namelist())==names and len(z.namelist())==len(names)
        payloads={n:z.read(n) for n in names}
    manifest=json.loads(payloads['EVIDENCE_MANIFEST.json'])
    for row in manifest['payloads']:
        b=payloads[row['name']];assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
    prep=json.loads((A/'COSMOLOGY_CREATION_ORIGIN_01_PREPARATION.json').read_bytes())
    assert manifest['submission']['sha256']==prep['archive']['sha256']
    register=json.loads(payloads['COSMOLOGY_CREATION_ORIGIN_01_REGISTER.json'])
    hashes=json.loads(payloads['SOURCE_HASHES.json'])
    for name,sha in hashes.items():
        assert hashlib.sha256((G/name).read_bytes()).hexdigest()==sha
        assert hashlib.sha256((A/'cosmology-creation-origin-01/sources'/name).read_bytes()).hexdigest()==sha
    assert len(register['issues'])==9 and len(register['unresolvedDependencies'])==11
    assert register['baseline']['outsidePacketDirectorsCrucibleReliedUpon'] is False
    proposal=json.loads((A/'cosmology-creation-origin-01/PROPOSED_COMPARISON.json').read_bytes())['proposedSummaries']
    reviews=register['summaryReview']
    for key in ['public','originScope']:assert reviews[key]['verdict']=='ACCEPT' and reviews[key]['text']==proposal[key]
    assert reviews['director']['verdict']=='CORRECT'
    assert reviews['peaceScope']['verdict']=='ACCEPT WITH CLARIFICATION'
    summaries={key:row.get('replacement',row.get('text')) for key,row in reviews.items()}
    assert all(isinstance(s,str) and s for s in summaries.values())
    dom=A/'COSMOLOGY_CREATION_ORIGIN_01_RECEIVED_DOM.txt'
    assert 'Response complete' in dom.read_text(encoding='utf-8') and downloaded.name in dom.read_text(encoding='utf-8')
    now=datetime.now(timezone.utc).isoformat()
    archive.write_bytes(raw);root.mkdir()
    for name,b in payloads.items():(root/name).write_bytes(b)
    decision={'reviewId':register['reviewId'],'recordedAtUtc':now,'status':'creation-origin-conference-received; nine dispositions; eleven unresolved dependencies retained','submission':info(A/'COSMOLOGY_CREATION_ORIGIN_01_SUBMISSION.json'),'archive':info(archive),'files':[info(root/n) for n in sorted(names)],'receivedDOM':info(dom),'visibleProof':info(A/'COSMOLOGY_CREATION_ORIGIN_01_RECEIVED.png'),'manifestPayloadsVerified':4,'currentAndFrozenSourceHashesVerified':len(hashes),'issues':[{'id':x['id'],'disposition':x['disposition']} for x in register['issues']],'summaryDispositions':{k:v['verdict'] for k,v in reviews.items()},'unresolvedDependencies':register['unresolvedDependencies'],'nextGodsPantheonsSourceNeeds':register['nextGodsPantheonsSourceNeeds'],'semanticCoverage':register['semanticCoverage'],'outsidePacketNotebookSourceReliedUpon':False,'sourceDoctrineChanges':0,'sourceInformationDeleted':0,'fullCosmologyApproved':False,'wholeGameApproved':False}
    receipt.write_bytes(encoded(decision))
    doc={'schemaVersion':'1.0','reviewId':register['reviewId'],'status':'reviewed-scoped-editorial-companion; no general cosmology authority promotion','audience':'Director/reviewer only; includes secret material and an embedded public wording example, not a public export','authority':info(root/'COSMOLOGY_CREATION_ORIGIN_01_REGISTER.json'),'receivedDecision':info(receipt),'summaries':summaries,'factBeliefRevelationTable':register['factBeliefRevelationTable'],'issues':register['issues'],'unresolvedDependencies':register['unresolvedDependencies'],'sourceHashes':hashes,'semanticCoverage':register['semanticCoverage'],'originalSourcesChanged':False,'generalCosmologyAuthorityCreated':False,'runtimeEnabled':False,'fullCosmologyApproved':False}
    candidate.parent.mkdir(parents=True,exist_ok=True);candidate.write_bytes(encoded(doc))
    def link(path):return os.path.relpath(path,manuscript.parent).replace('\\','/')
    lines=['# Creation and origins — reviewed reading companion','',
        '**Director and reviewer material.** This document contains secret setting facts. The public paragraph below is an embedded wording example, not a player export. This is a scoped synthesis of existing owner decisions and reviewed source distinctions; it does not create a general cosmology authority or finish the cosmology review.','',
        f'Review: [nine source dispositions]({link(root/"COSMOLOGY_CREATION_ORIGIN_01_REGISTER.json")}); [received evidence]({link(receipt)}); [complete structured companion]({link(candidate)}). Original books and their differing accounts remain unchanged.','']
    for key,title in [('public','Public wording example'),('director','Director account and unresolved provenance'),('originScope','How to read the original origin accounts'),('peaceScope','Peace and meaningful difference')]:lines.extend(['## '+title,'',summaries[key],''])
    lines.extend(['## Fact, belief and revelation','','Read each statement with its listed authority. An original source account is not automatically an owner-locked fact.','','| Subject | Director account | Public belief | Revelation or open boundary | Authority |','|---|---|---|---|---|'])
    for row in register['factBeliefRevelationTable']:
        lines.append('| '+' | '.join(row[k].replace('|','\\|') for k in ['subject','factDirector','publicBelief','revelation','authority'])+' |')
    lines.extend(['','## Unresolved dependencies','','These are retained questions, not prompts to improvise an answer. No immediate owner choice about a numeric stillness threshold is required.',''])
    for row in register['unresolvedDependencies']:lines.append(f'- **{row["id"]}:** {row["question"]} {row["status"]}')
    lines.extend(['','## Source boundaries','',f'- [Owner decisions Q1–Q5]({link(G/"docs/mechanics/OWNER_COSMOLOGY_LOCKS_2026-07-30.md")}) control the questions they actually answer.',f'- [Player/Director boundary]({link(R/"docs/canon/PLAYER_DIRECTOR_BOUNDARY.md")}) controls the staged revelation distinction.',f'- [Exact semantic coverage]({link(root/"SEMANTIC_COVERAGE.json")}) records which passages were read and what remains outside this conference.','- Gods/pantheons, planes, souls/death/resurrection, full history, divine/class powers and campaign revelation implementation remain later comparisons.','- The original Heartcell motive, transformation into a prison, precise Sundering/Pact chronology, and unresolved endgame identities have not been supplied by this synthesis.',''])
    manuscript.parent.mkdir(parents=True,exist_ok=True);manuscript.write_bytes(('\n'.join(lines)).encode())
    current=json.loads(candidate.read_bytes());text=manuscript.read_text(encoding='utf-8')
    assert current['summaries']==summaries and all(text.count(s)==1 for s in summaries.values())
    assert current['issues']==register['issues'] and current['unresolvedDependencies']==register['unresolvedDependencies']
    for name,sha in hashes.items():assert hashlib.sha256((G/name).read_bytes()).hexdigest()==sha
    application.write_bytes(encoded({'recordedAtUtc':now,'reviewId':register['reviewId'],'status':'exact-reviewed-editorial-wording-assembled','authority':info(root/'COSMOLOGY_CREATION_ORIGIN_01_REGISTER.json'),'candidate':info(candidate),'manuscript':info(manuscript),'exactSummariesVerified':4,'unchangedAcceptedSummaries':2,'reviewedReplacementSummaries':2,'factBeliefRevelationRows':7,'issueDispositions':9,'unresolvedDependenciesRetained':11,'originalSourceHashesUnchanged':len(hashes),'sourceInformationDeleted':0,'generalCosmologyAuthorityCreated':False,'publicExportCreated':False,'fullCosmologyApproved':False}))
    print(json.dumps({'receipt':info(receipt),'application':info(application),'manuscript':info(manuscript),'unresolvedDependenciesRetained':11,'originalsUnchanged':len(hashes)}))

if __name__=='__main__':main()
