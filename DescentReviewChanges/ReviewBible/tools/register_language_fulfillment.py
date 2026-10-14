"""Register the fulfilled LAX scope without closing broader game gates."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil,subprocess,sys
R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    receipt=read(A/'LANGUAGE_EXACT_FULFILLMENT.json');assert receipt['exactLanguageApproval']
    assert all(sha(G/p)==h for p,h in receipt['finalHashes'].items())
    paths=[G/'START_HERE.md',A/'GPT_REVIEW_CONTINUATION_HANDOFF.md',A/'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json',R/'data/playtest/game_development_coverage.json',R/'docs/mechanics/GAME_DEVELOPMENT_COVERAGE.md']
    backup=A/'navigation-before-language-fulfillment';assert not backup.exists();backup.mkdir()
    before={p.relative_to(G).as_posix():sha(p) for p in paths}
    for p in paths:
        target=backup/p.relative_to(G);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
    write(backup/'FILE_MANIFEST.json',before)
    start=paths[0].read_text(encoding='utf-8')
    old="The [language and communication source review](docs/audit/2026-10-08/full-game/LANGUAGE_COMMUNICATION_V2_SUBMISSION.json) is now submitted with 16 bounded cases and 152 complete source files; its verdict is pending."
    assert old in start
    start=start.replace(old,"The [language and communication exact review](docs/audit/2026-10-08/full-game/LANGUAGE_EXACT_FULFILLMENT.json) is also fulfilled under LAX-01–03. Its authored chapter, records and32 worked sequences are reviewed; remaining catalog and character-record integration stay open.",1)
    start=start.replace('Next: language and communication, then remaining systems.','Next: the remaining spell, feat, expedition, bestiary and Director procedures.',1)
    old=next(x for x in start.splitlines() if x.startswith('| Languages and communication |'))
    start=start.replace(old,'| Languages and communication | [Reviewed player chapter](DescentReviewChanges/ReviewBible/docs/mechanics/LANGUAGE_COMMUNICATION_PLAYTEST.md) and [32 worked sequences](DescentReviewChanges/ReviewBible/docs/mechanics/LANGUAGE_COMMUNICATION_WORKED_SEQUENCES.md). [LAX-01–03 fulfilled](docs/audit/2026-10-08/full-game/LANGUAGE_EXACT_FULFILLMENT.json):460 source,496 candidate and44 focused checks; standalone496 also passes. Original152 payloads and frozen v1 preserved. Pending class/spell/feat statuses, runtime, human balance and wider integration remain unchanged. |')
    paths[0].write_text(start,encoding='utf-8')
    prefix='''## Current checkpoint — language exact review fulfilled, 11 October

**LAX-01–03 are fulfilled.** Final GPT reply `12106bf1-18cf-41ee-b0df-8e5a8714d143` conditionally accepted the authored language layer. The [owner fulfillment receipt](LANGUAGE_EXACT_FULFILLMENT.json) records actual repository applications, source460/candidate496/focused44 checks, a standalone496 reproduction, pre-label and final hashes, and a label-only proof. The [final verdict](language-exact-reviewer-files/LAX_Language_Communication_Exact_Verdict.md) is preserved with its full15-file manifest and evidence package.

The completed candidate is LA-CANDIDATE-v1.1, reviewed authored language/communication playtest. LAX-01 uses the exact links to already-supplied public collections; the prepared four-file reference addendum remains preserved and unsent, and is unnecessary. LAX-02 correctly distinguishes absent/null/value provenance. LAX-03 limits TI-04 control to its actual automata, keeps manual/trap/operator procedures, restores noncombat Action start and preserves TD-08. All32 full cases remain aligned; LA-T30 is the named replacement. All152 original payloads, complete class/spell/feat/recipe source objects and LA-16 receipt remain unchanged. Historical reports and frozen v1 are preserved.

The source/candidate/focused counts overlap and are not gameplay tests. DD-46's wider character-record integration and acceptance gate remain open. All75 closures, acceptance gates and human-evidence fields remain unchanged. The next conference is the full137 remaining low-rank spell source set, with completed language/NWX/crafting authority and the eight explicitly unapproved proposals. No source deletion, push or cosmology interpretation has occurred. Final joint whole-game flow precedes the authorized push; verified remote commit precedes careful cosmology review.

The earlier checkpoints below are preserved history; their live-review and unfulfilled-language statements are superseded by this checkpoint.

'''
    paths[1].write_text(prefix+paths[1].read_text(encoding='utf-8'),encoding='utf-8')
    write(paths[2],{'atUtc':datetime.now(timezone.utc).isoformat(),'currentReview':'language exact review fulfilled','status':'LAX-01–03 applied and verified; preparing full137-spell source conference','requestId':receipt['requestId'],'replyId':receipt['replyId'],'candidateExactVerdictReceived':True,'exactLanguageApproval':True,'fulfillmentReceipt':str(A/'LANGUAGE_EXACT_FULFILLMENT.json'),'next':'Refresh and send complete low-rank137 source packet with completed language authority and eight unapproved proposals.','allSourceInformationPreserved':True,'pushPerformed':False,'cosmologyReviewed':False})
    ledger=read(paths[3]);gates={x['id']:{k:x[k] for k in ('acceptanceGate','closure','humanEvidence')} for x in ledger['aspects']}
    row=next(x for x in ledger['aspects'] if x['id']=='DD-46');row['status']='reviewed-authored-language-layer-integration-open'
    for field,values in {'reviewEvidence':['docs/audit/2026-10-08/full-game/LANGUAGE_EXACT_VERDICT_RECEIPT.json','docs/audit/2026-10-08/full-game/language-exact-reviewer-files/LAX_Language_Communication_Exact_Verdict.md','docs/audit/2026-10-08/full-game/LANGUAGE_EXACT_FULFILLMENT.json'],
                         'validationEvidence':['docs/audit/2026-10-08/full-game/LANGUAGE_EXACT_FULFILLMENT_SOURCE_460.json','docs/audit/2026-10-08/full-game/LANGUAGE_EXACT_FULFILLMENT_CANDIDATE_496.json','docs/audit/2026-10-08/full-game/LANGUAGE_EXACT_FULFILLMENT_FOCUSED_44.json','docs/audit/2026-10-08/full-game/LANGUAGE_EXACT_FULFILLMENT_PORTABLE_496.json','DescentReviewChanges/ReviewBible/docs/mechanics/LANGUAGE_REVIEW_STATUS.json']}.items():
        for value in values:
            if value not in row[field]:row[field].append(value)
    row['openIssues'][0]='LAX-01–03 exact language corrections are fulfilled. The complete ordinary language chapter, grant/record contracts,49 language-only class interfaces,23 spell comparisons,8 pending feat comparisons and32 authored sequences are reviewed under the version-bound receipt. All152 original payloads remain unchanged; source460/candidate496/focused44 checks and standalone496 pass. These are static/reference checks, not runtime/human certification. Character-record integration, remaining spell/feat procedures and this broader acceptance gate remain open.'
    assert gates=={x['id']:{k:x[k] for k in ('acceptanceGate','closure','humanEvidence')} for x in ledger['aspects']}
    write(paths[3],ledger)
    subprocess.run([sys.executable,'-X','utf8',str(R/'tools/build_game_coverage.py')],check=True)
    assert all(sha(G/p)==h for p,h in receipt['finalHashes'].items())
    write(A/'LANGUAGE_FULFILLMENT_COVERAGE_REGISTRATION.json',{'before':before,'after':{p.relative_to(G).as_posix():sha(p) for p in paths},'all75AcceptanceGatesClosuresHumanEvidenceUnchanged':True,'scope':'Language authored review registered; wider integration open','sourceInformationDeleted':0,'pushPerformed':False})
    print('Registered fulfilled language review; preserved all broader closure/human gates.')
if __name__=='__main__':main()
