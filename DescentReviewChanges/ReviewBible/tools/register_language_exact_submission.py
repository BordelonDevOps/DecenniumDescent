"""Record the verified once-only submission and navigation, preserving prior checkpoints."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess
import sys

R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    receipt=A/'LANGUAGE_EXACT_V1_SUBMISSION.json'
    assert not receipt.exists()
    p=read(A/'LANGUAGE_EXACT_V1_PREPARATION.json')
    assert sha(Path(p['zip']))==p['sha256']
    receipt_data={'status':'Submitted once; exact verdict pending; browser visibly responding',
        'requestId':'b152ba58-ee3a-4a1b-bcbe-4d7cc27e55cb','submittedAtUtc':datetime.fromtimestamp(1791701812.817,timezone.utc).isoformat(),
        'observedAtUtc':datetime.now(timezone.utc).isoformat(),'threadId':'6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b',
        'threadTitle':'Calibration Review Part 2','url':'https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b',
        'attachment':{'path':p['zip'],'bytes':p['bytes'],'sha256':p['sha256'],'payloadFiles':p['payloadFiles']},
        'prompt':str(A/'CODEX_LANGUAGE_EXACT_V1_PROMPT.txt'),'promptSha256':sha(A/'CODEX_LANGUAGE_EXACT_V1_PROMPT.txt'),
        'browserProof':str(A/'LANGUAGE_EXACT_V1_SUBMISSION_BROWSER.png'),
        'observedResponse':'Verifying Review Package Archive Contents. I’ll verify the archive and complete candidate, inspect the public envelope, then assess all 32 cases against the final source directions.',
        'candidateExactApproval':False,'sourceDirectionsReceived':True,'newClassSpellFeatApprovals':0,'sourceInformationDeleted':0,'runtimeChanged':False,'pushPerformed':False,'cosmologyReviewed':False}
    save(receipt,receipt_data)
    paths=[R/'data/playtest/game_development_coverage.json',R/'docs/mechanics/GAME_DEVELOPMENT_COVERAGE.md',G/'START_HERE.md',A/'GPT_REVIEW_CONTINUATION_HANDOFF.md',A/'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json']
    backup=A/'navigation-before-language-exact-submission';backup.mkdir()
    before={}
    for path in paths:
        rel=path.relative_to(G);dest=backup/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,dest);before[rel.as_posix()]=sha(path)
    save(backup/'MANIFEST.json',before)
    data=read(paths[0]);gates={r['id']:{k:r[k] for k in ('acceptanceGate','closure','humanEvidence')} for r in data['aspects']}
    row=next(r for r in data['aspects'] if r['id']=='DD-46')
    row['status']='authored-candidate-submitted-exact-review-pending'
    def add(field,values):
        for value in values:
            if value not in row[field]:row[field].append(value)
    add('reviewEvidence',['docs/audit/2026-10-08/full-game/LANGUAGE_SOURCE_VERDICT_RECEIPT.json','docs/audit/2026-10-08/full-game/language-source-reviewer-files/LA_Language_Communication_Source_Verdict.md','docs/audit/2026-10-08/full-game/LANGUAGE_EXACT_V1_SUBMISSION.json'])
    add('draftEvidence',['DescentReviewChanges/ReviewBible/docs/mechanics/LANGUAGE_COMMUNICATION_PLAYTEST.md','DescentReviewChanges/ReviewBible/docs/mechanics/LANGUAGE_COMMUNICATION_WORKED_SEQUENCES.md','DescentReviewChanges/ReviewBible/docs/director-only/LANGUAGE_COMMUNICATION_INTERNAL_CANDIDATE.md','DescentReviewChanges/ReviewBible/data/playtest/language_communication_candidate_public.json','DescentReviewChanges/ReviewBible/data/director/language_communication_candidate_internal.json'])
    add('validationEvidence',['docs/audit/2026-10-08/full-game/LANGUAGE_SOURCE_REPRODUCED_460_CHECKS.json','docs/audit/2026-10-08/full-game/LANGUAGE_CANDIDATE_VALIDATION.json','docs/audit/2026-10-08/full-game/LANGUAGE_CANDIDATE_WORKED_ADJUDICATIONS.json'])
    row['openIssues'][0]='LA-01–15 source directions are received; LA-16 remains receipt-only. The complete authored language candidate was submitted once for exact review in Calibration Review Part 2 (request b152ba58-ee3a-4a1b-bcbe-4d7cc27e55cb): all14/45/20 grants,49 class interfaces,23 spells,8 pending feats,40 Scribing records,19 advanced sections and32 authored adjudications. Await the exact verdict and fulfill bounded corrections; source460 and local496 checks are not runtime/human certification. Character-record integration and this acceptance gate remain open.'
    assert gates=={r['id']:{k:r[k] for k in ('acceptanceGate','closure','humanEvidence')} for r in data['aspects']}
    save(paths[0],data)
    start=paths[2].read_text(encoding='utf-8')
    old=next(line for line in start.splitlines() if line.startswith('| Languages and communication |'))
    new='| Languages and communication | [Complete player candidate](DescentReviewChanges/ReviewBible/docs/mechanics/LANGUAGE_COMMUNICATION_PLAYTEST.md) and [32 worked sequences](DescentReviewChanges/ReviewBible/docs/mechanics/LANGUAGE_COMMUNICATION_WORKED_SEQUENCES.md). All16 source decisions received; the complete184-file [exact-review submission](docs/audit/2026-10-08/full-game/LANGUAGE_EXACT_V1_SUBMISSION.json) is with GPT. All152 original source payloads remain unchanged;460 source and496 local checks pass within their stated scopes. Exact candidate approval remains pending. |'
    start=start.replace(old,new)
    old=next(line for line in start.splitlines() if line.startswith('| Final delivery |'))
    new=old[:-1]+'; [size screening](docs/audit/2026-10-08/full-game/GITHUB_DELIVERY_SIZE_SCREENING_2026-10-11.json) and [Windows long-path correction](docs/audit/2026-10-08/full-game/GITHUB_DELIVERY_LONG_PATH_RECONCILIATION_2026-10-11.json). The clean delivery checkout matches the recorded remote; no authoring files copied or pushed. All68 files above100MiB are in the separate asset experiment; final packaging remains open. |'
    start=start.replace(old,new);paths[2].write_text(start,encoding='utf-8')
    prefix='''## Current checkpoint — language candidate submitted for exact review, 11 October

The complete LA-01–16 source verdict is received and preserved in [its receipt](LANGUAGE_SOURCE_VERDICT_RECEIPT.json). All460 original reviewer source/reference checks reproduce. The complete authored language candidate is now [submitted once for exact review](LANGUAGE_EXACT_V1_SUBMISSION.json), request `b152ba58-ee3a-4a1b-bcbe-4d7cc27e55cb`. Its184-payload ZIP has SHA256 `788e1210d28120b5e94a6ddc4d1dcc69e48a2aeb7cfd60f434c9680b30fa2ec1` and12,859,675 bytes. Browser shows GPT verifying the package. Do not resend, restart or treat a connector user-message completion as the final verdict.

Full player/internal guides and data plus32 worked adjudications are authored. All14 ancestries,45 variants,20 backgrounds,48 selected class cards plus Heaven's Decree,23 spells,15 pending routes,8 pending feat originals,40 Scribing cards and19 advanced sections are represented. The independent public envelope includes only the28 completed public Scribing records. All152 original payloads/current dependencies remain unchanged. Local496 checks include38 finite reference calculations/boundaries; the32 semantic adjudications are authored expectations, not runtime/human tests. Candidate approval, broader character-record integration and DD46 closure remain pending.

The original source-verdict package is `DD_Language_Communication_Source_Verdict_and_Evidence.zip`, SHA256 `c373c824b10879f334dbbb3074c18f7fb84a4e88442b890babf2a25703b042a0`; its final manuscript is `language-source-reviewer-files/LA_Language_Communication_Source_Verdict.md`. Use the final artifacts, not intermediate live reasoning drafts, which differed.

Delivery preparation: the existing remote snapshot has been materialized in the isolated checkout and is clean at `57bb6d86e0e06d5e4f1e24a6e39a6a7ddb26a2cc`. The [size screen](GITHUB_DELIVERY_SIZE_SCREENING_2026-10-11.json) plus [long-path correction](GITHUB_DELIVERY_LONG_PATH_RECONCILIATION_2026-10-11.json) count164,507 files/27,300,572,657 bytes within the stated exclusions; all259 initial stat failures were accessible long paths, not missing files. All68 >100MiB files are in the separate imported asset experiment. Preserve that local material and reconcile actual distribution/dependency/rights evidence before final public packaging. No move/deletion, authoring copy, new commit, push or cosmology review occurred.

After the language exact gate, update the queued spell/feat/expedition/bestiary/Director source handoffs with completed language authority. Their earlier preparations remain preserved and unsent. Final joint whole-game flow still precedes the authorized GitHub push; verified remote commit precedes careful cosmology review. All75 acceptance gates, closures and human evidence remain unchanged.

The checkpoints below are preserved history. Earlier “source verdict pending” and “capture before authoring” statements are superseded by this current checkpoint.

'''
    paths[3].write_text(prefix+paths[3].read_text(encoding='utf-8'),encoding='utf-8')
    save(paths[4],{'atUtc':datetime.now(timezone.utc).isoformat(),'currentReview':'language exact candidate v1','requestId':receipt_data['requestId'],
        'status':'once-submitted; browser actively verifying package','sourceVerdictReceived':True,'candidateSubmitted':True,'candidateExactVerdictReceived':False,
        'next':'Capture full final exact verdict and evidence; do not resend or promote on progress text. Continue independent preparation.',
        'submissionReceipt':str(receipt),'sourceReceipt':str(A/'LANGUAGE_SOURCE_VERDICT_RECEIPT.json'),'allSourceInformationPreserved':True,'pushPerformed':False,'cosmologyReviewed':False})
    subprocess.run([sys.executable,'-X','utf8',str(R/'tools/build_game_coverage.py')],check=True)
    save(A/'LANGUAGE_EXACT_COVERAGE_REGISTRATION.json',{'status':'Source verdict and submitted exact candidate registered; no new closure',
        'before':before,'after':{str(p.relative_to(G).as_posix()):sha(p) for p in paths},'all75AcceptanceGatesClosuresHumanEvidenceUnchanged':True,
        'sourceInformationDeleted':0,'newApprovals':0,'submissionRequestId':receipt_data['requestId']})
    print('Registered actual language submission, source evidence, candidate navigation and corrected delivery inventory. No new closure or push.')

if __name__=='__main__':main()
