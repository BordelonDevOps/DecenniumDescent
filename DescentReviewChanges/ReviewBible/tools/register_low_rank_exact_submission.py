"""Record the observed exact-review request and preserve earlier navigation states."""
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import re
import subprocess
import sys
from urllib.parse import unquote

R=Path(__file__).resolve().parents[1]
G=R.parents[1]
A=G/'docs/audit/2026-10-08/full-game'


def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return sha256(p.read_bytes()).hexdigest()
def save(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def main():
    receipt_path=A/'LOW_RANK_136_EXACT_V1_SUBMISSION.json'
    assert not (A/'LOW_RANK_136_EXACT_V1_NAVIGATION_REGISTRATION.json').exists(), 'Preserve completed registration'
    if receipt_path.exists():
        assert read(receipt_path)['requestId']=='c18136bc-5efc-4989-a31b-613c448e9546', 'Unrelated existing receipt'
    prep=read(A/'LOW_RANK_136_EXACT_V1_PREPARATION.json')
    upload=Path(r'C:\Users\cbord\AppData\Local\Temp\codex-file-preview-TKwuqb\DD_Low_Rank_136_Exact_Review_v1.zip')
    assert sha(Path(prep['zip']))==sha(upload)==prep['sha256']
    submitted=datetime.fromtimestamp(1791711829.951,timezone.utc).isoformat()
    receipt={'status':'submitted-once-awaiting-final-exact-review','submittedAtUtc':submitted,
             'threadId':'6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b','threadTitle':'Calibration Review Part 2',
             'requestId':'c18136bc-5efc-4989-a31b-613c448e9546',
             'browserTabId':'125745464','archive':prep['zip'],'bytes':prep['bytes'],'sha256':prep['sha256'],
             'payloadFiles':prep['payloadFiles'],'connectorVerifiedRequestAndOneAttachment':True,
             'attachedFileMatchesLocalArchive':True,'browserShowsRespondingAndStop':True,
             'sendClickTimedOutButSubmissionIndependentlyVerified':True,'resubmitted':False,
             'mechanicalCandidates':136,'blinkReceiptOnly':True,'sharedRules':20,'bookBindings':141,
             'authoredBoundaryRecords':187,'localChecks':49,'localFailures':0,
             'sourceRecordsPromoted':0,'exactCandidateApproval':False,'runtimeVerified':False,
             'pushPerformed':False,'cosmologyReviewed':False}
    protected=read(A/'LOW_RANK_SPELL_FILE_HANDOFF_V3_PREPARATION.json')['currentFileHashes']
    assert all(sha(G/p)==h for p,h in protected.items())
    data_path=R/'data/playtest/game_development_coverage.json'
    doc_path=R/'docs/mechanics/GAME_DEVELOPMENT_COVERAGE.md'
    nav=[G/'START_HERE.md',A/'PREPARED_SPELL_SOURCE_INDEX.md',A/'GPT_REVIEW_CONTINUATION_HANDOFF.md',data_path,doc_path]
    backup=A/'navigation-before-low136-exact-submission'
    if backup.exists():
        # Recovery after a guard failed before any navigation write. Never replace
        # the original snapshot or resume over changed user files.
        prior_hashes=read(backup/'MANIFEST.json')
        assert all(sha(p)==prior_hashes[str(p.relative_to(G))]==sha(backup/p.name) for p in nav)
    else:
        backup.mkdir()
        for p in nav: (backup/p.name).write_bytes(p.read_bytes())
        save(backup/'MANIFEST.json',{str(p.relative_to(G)):sha(p) for p in nav})
    save(receipt_path,receipt)
    d=read(data_path); prior=deepcopy(d)
    d['activeLowRankSpellReview'].update(phase='136-complete-candidates-authored; exact-review-submitted-awaiting-final',
        exactRequestId=receipt['requestId'],exactSubmittedAtUtc=submitted,
        candidateSubmissionReceipt=receipt_path.relative_to(G).as_posix(),mechanicalCandidates=136,
        fullPublicEnvelope=True,authoredBoundaryRecords=187,localChecks=49,exactApproval=False)
    changed=[]
    old_clause='Read each full source/conflict/operating row, author its complete candidate with actual access, costs, clocks and boundaries, and obtain separate exact review.'
    new_clause='Complete candidates with actual access, costs, clocks and boundaries are authored and submitted in the full 136-card exact-review packet; await the final exact verdict and fulfill its bounded corrections.'
    for row in d['aspects']:
        for i,old in enumerate(row['openIssues']):
            new=old
            if old_clause in old:
                new=old.replace(old_clause,new_clause)
            elif old.startswith('LR-SOURCE-2026-10-11 final directions received'):
                new='All136 full low-rank mechanical candidates plus Blink receipt are authored and submitted for exact review in Calibration Review Part 2, request '+receipt['requestId']+'. Full internal/public envelopes and manuscripts preserve137 originals,141 book bindings,20 shared policies and187 authored boundaries.49 bounded local checks pass; all342 original inputs unchanged. Await the final exact verdict; no operational promotion. Totals remain276 operational drafts/572 pending.'
            elif old.startswith('All572 pending ordinary identities'):
                new=old.replace('awaiting complete candidates and exact review','complete candidates now authored and submitted for exact review')
            elif old.startswith('276 ordinary spell drafts are operational;572'):
                new=old.replace('Complete candidate authoring and exact review, plus remaining aliases, rituals and class-specific repertoire interfaces','The136 candidates are now authored and submitted for exact review; complete the verdict corrections and remaining aliases, rituals and class-specific repertoire interfaces')
            if new!=old:
                row.setdefault('historicalIssueNotes',[]).append({'id':f"{row['id']}-LR-EXACT-V1-{i:02}",
                    'originalText':old,'replacement':new,'reason':'Actual complete candidate authored and exact request independently verified; no acceptance gate advanced.',
                    'evidence':[receipt_path.relative_to(G).as_posix()],'recordedAtUtc':datetime.now(timezone.utc).isoformat()})
                row['openIssues'][i]=new;changed.append({'area':row['id'],'issueIndex':i})
        if any(x['area']==row['id'] for x in changed):
            for key,path in [('draftEvidence',R/'docs/playtest/LOW_RANK_136_CANDIDATE.md'),('validationEvidence',A/'LOW_RANK_136_CANDIDATE_LOCAL_VALIDATION.json'),('reviewEvidence',receipt_path)]:
                relative=path.relative_to(G).as_posix()
                if relative not in row[key]: row[key].append(relative)
    for before,after in zip(prior['aspects'],d['aspects']):
        for key in ['acceptanceGate','status','closure','humanEvidence','completedScopes','completionClass']:
            assert (key in before)==(key in after) and before.get(key)==after.get(key),(before['id'],key)
    save(data_path,d)
    start=(G/'START_HERE.md').read_text(encoding='utf-8')
    current='**Current joint review:** The [136 complete low-rank spell candidates](DescentReviewChanges/ReviewBible/docs/playtest/LOW_RANK_136_CANDIDATE.md), full internal/public envelopes,20 shared rules and187 authored examples are [submitted for exact GPT review](docs/audit/2026-10-08/full-game/LOW_RANK_136_EXACT_V1_SUBMISSION.json) in Calibration Review Part 2. All137 originals/141 book bindings are preserved; Blink remains receipt-only.49 bounded local checks pass. Await the final exact verdict; ordinary totals remain276 operational drafts/572 pending. Fulfilled language, onboarding and crafting gates carry forward.'
    start=re.sub(r'^\*\*Current joint review:\*\*.*$',lambda m:current,start,flags=re.M)
    start=start.replace('Complete candidates and separate exact review are next.','The136 complete candidates and full public envelope are now submitted for separate exact review; await the final verdict.')
    (G/'START_HERE.md').write_text(start,encoding='utf-8')
    index=A/'PREPARED_SPELL_SOURCE_INDEX.md'
    text=index.read_text(encoding='utf-8').replace('136 mechanical directions await complete candidate authoring/exact review','136 complete mechanical candidates are authored and submitted for exact review')
    text=text.replace('full candidate authoring and exact review are next.','the [136 complete candidates and Blink receipt are now submitted for exact review](LOW_RANK_136_EXACT_V1_SUBMISSION.json), with full internal/public manuscripts and187 authored examples; await the final verdict.')
    index.write_text(text,encoding='utf-8')
    handoff=A/'GPT_REVIEW_CONTINUATION_HANDOFF.md'
    old=handoff.read_text(encoding='utf-8')
    new=f'''**CURRENT PHASE — full low-rank candidates under exact review:** All136 complete cards plus Blink receipt are authored and [submitted once](LOW_RANK_136_EXACT_V1_SUBMISSION.json) to Calibration Review Part 2 at{submitted}, request `{receipt['requestId']}`. The60,244,248-byte393-payload archive SHA256 is `{prep['sha256']}`; its actual attached file has the same hash. The Send click timed out, but connector request/attachment and browser responding state independently confirm success: **do not resend**. [Complete manuscript](../../../../DescentReviewChanges/ReviewBible/docs/playtest/LOW_RANK_136_CANDIDATE.md), whole internal/public JSON,20 shared rules,141 book bindings and187 complete authored examples are included. [Local validation](LOW_RANK_136_CANDIDATE_LOCAL_VALIDATION.json) has49 passing bounded checks including18,840 access gates and2,808 hypothetical in-memory ordinary quotations; no full spell runtime or human balance claim. All342 submitted sources and current276/572 catalog totals remain unchanged. Await the final exact verdict, inspect its complete files, and fulfill bounded corrections before any promotion. Preserve prior completed LAX/NWX/recipe gates. Independent worksheet/glossary/three teaching examples remain unsent; remaining435 spells,327 feats and other system conferences still need current-interface review. Final actual joint whole-game flow precedes authorized GitHub push; remote verification precedes cosmology.

**Historical checkpoints below are retained; earlier authoring/live-source phases are superseded by the exact submission above.**

'''
    handoff.write_text(new+old,encoding='utf-8')
    subprocess.run([sys.executable,str(R/'tools/build_game_coverage.py')],check=True,capture_output=True,text=True)
    links=0
    for p in [x for x in nav if x.suffix=='.md']:
        for raw in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
            target=unquote(raw.split('#',1)[0].strip('<>'))
            if not target or re.match(r'^[a-zA-Z]+:',target): continue
            assert (p.parent/target).exists(),(p,target)
            links+=1
    assert all(sha(G/p)==h for p,h in protected.items())
    save(A/'LOW_RANK_136_EXACT_V1_NAVIGATION_REGISTRATION.json',{
        'status':'exact-submission-recorded-no-gates-advanced','changedIssueNotes':changed,
        'originalIssueNotesPreserved':True,'all75AcceptanceStatusClosureHumanScopesUnchanged':True,
        'protectedSubmittedInputsUnchanged':342,'validNavigationLinks':links,
        'newNavigationHashes':{p.relative_to(G).as_posix():sha(p) for p in nav}})
    print(json.dumps({'updatedIssueNotes':len(changed),'validNavigationLinks':links,'sourceInputsUnchanged':342,'acceptanceGatesAdvanced':0}))


if __name__=='__main__': main()
