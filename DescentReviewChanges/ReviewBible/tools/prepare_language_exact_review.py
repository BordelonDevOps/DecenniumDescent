"""Freeze the complete first LA candidate with full source evidence for exact review."""
from pathlib import Path
from datetime import datetime, timezone
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib
import json

R=Path(__file__).resolve().parents[1]
G=R.parents[1]
A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha_bytes(b):return hashlib.sha256(b).hexdigest()
def main():
    zip_path=A/'DD_Language_Communication_Exact_Review_v1.zip'
    assert not zip_path.exists(), 'Preserve a frozen submission'
    validation=read(A/'LANGUAGE_CANDIDATE_VALIDATION.json')
    assert not validation['failed'] and validation['candidateChecks']==496
    for path,digest in validation['candidateHashes'].items():assert sha_bytes((G/path).read_bytes())==digest
    original=A/'DD_Language_Communication_Source_Prepared_v2.zip'
    payload={}
    with ZipFile(original) as z:
        original_manifest=json.loads(z.read('FILE_MANIFEST.json'))
        for path,e in original_manifest.items():
            b=z.read(path);assert sha_bytes(b)==e['sha256']==sha_bytes((G/path).read_bytes())
            payload[path]=b
        payload['ORIGINAL_SOURCE_V2_FILE_MANIFEST.json']=z.read('FILE_MANIFEST.json')
        payload['ORIGINAL_SOURCE_V2_README.md']=z.read('README_LANGUAGE_V2.md')
    extra=[G/path for path in validation['candidateHashes']]+[
        A/'LANGUAGE_SOURCE_VERDICT_RECEIPT.json',A/'LANGUAGE_SOURCE_REPRODUCED_460_CHECKS.json',
        A/'LANGUAGE_CANDIDATE_VALIDATION.json',A/'LANGUAGE_CANDIDATE_WORKED_ADJUDICATIONS.json',
        A/'ONBOARDING_CHARTER_EXACT_FULFILLMENT.json',original,
        R/'tools/build_language_candidate.py',R/'tools/complete_language_candidate_examples.py',R/'tools/validate_language_candidate.py',
    ]
    extra += list((A/'language-source-reviewer-files').rglob('*'))
    for p in extra:
        if p.is_file():
            key=p.relative_to(G).as_posix();b=p.read_bytes()
            if key in payload:assert payload[key]==b
            payload[key]=b
    readme='''# Complete language and communication candidate: exact review v1

Audience: INTERNAL joint review. This archive deliberately includes private source evidence. It is not a public distribution package.

Read these complete authored files first:
- DescentReviewChanges/ReviewBible/docs/mechanics/LANGUAGE_COMMUNICATION_PLAYTEST.md — full player chapter, 14 ancestry and20 background rows, new procedures labeled.
- DescentReviewChanges/ReviewBible/docs/mechanics/LANGUAGE_COMMUNICATION_WORKED_SEQUENCES.md — 32 concrete authored chronological adjudications.
- DescentReviewChanges/ReviewBible/docs/director-only/LANGUAGE_COMMUNICATION_INTERNAL_CANDIDATE.md — complete16-case application wording plus every selected class interface.
- DescentReviewChanges/ReviewBible/data/playtest/language_communication_candidate_public.json — full independent public envelope, 14/45/20 mappings, identity/mode/choice data, eight record contracts,49 class interfaces,23 spell comparisons,8 pending feat references and28 exact completed public Scribing cards.
- DescentReviewChanges/ReviewBible/data/director/language_communication_candidate_internal.json — complete source objects/engine contexts,15 spell routes,8 pending feat originals,40 Scribing cards and19 completed advanced sections, and the deferred LA16 receipt.

The original152 payloads are included at their original paths with identical bytes. ORIGINAL_SOURCE_V2_FILE_MANIFEST.json is their original manifest; the original source ZIP is also included so the reviewer read-only460-check script can run without reconstructing ZIP bytes. The full downloaded source verdict and all14 manifested reviewer files are under docs/audit/2026-10-08/full-game/language-source-reviewer-files. No live reasoning drafts were used as authority; only the final reply08f18635-6dea-4d41-8f11-19fafb1baf2c and its final package.

LANGUAGE_CANDIDATE_VALIDATION.json reports496 local checks, zero failures. These comprise static source/candidate/public parity plus20 finite reference arithmetic and18 finite reference boundary checks. The32 worked cases are authored semantic adjudications, NOT executed gameplay/runtime tests or human trials. The separate460 reviewer source checks reproduced with no failures. Record contracts are authored interfaces, not a deployed companion runtime or save migration.

The public envelope takes completed public recipe objects from the existing public artifact, never projects raw private recipe objects. Private or restricted Scribing membership/names are absent from that envelope. Published literal language names and restrictions remain, without new setting interpretation. Pending spells retain operational:null; feats and class review statuses are not promoted.

Please exact-review the actual complete candidate against all16 final source directions and all32 original expectations. Return bounded corrections with exact replacement wording and affected file/record paths where needed, or scoped authored-language approval. Do not reopen fulfilled NWX or687/433 recipe gates. No generic source conference is required. Whole-game flow, remaining catalogs, software runtime, human teaching/balance, push and post-push cosmology remain separate.

Builders in tools are one-time historical construction scripts and refuse an existing candidate. Do not run them over this frozen copy. validate_language_candidate.py is read-only on inputs and writes only its named validation report in a separately extracted workspace; the reviewer source validator reads the immutable source ZIP. Inspect any script before executing it.
'''
    payload['README_LANGUAGE_EXACT_V1.md']=readme.encode('utf-8')
    manifest={path:{'bytes':len(b),'sha256':sha_bytes(b)} for path,b in sorted(payload.items())}
    with ZipFile(zip_path,'w',ZIP_DEFLATED,compresslevel=9) as z:
        for path,b in sorted(payload.items()):z.writestr(path,b)
        z.writestr('FILE_MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    with ZipFile(zip_path) as z:
        assert len(z.namelist())==len(manifest)+1
        assert all(sha_bytes(z.read(p))==e['sha256'] for p,e in manifest.items())
    prep={'status':'Complete authored candidate frozen for exact review; not yet submitted','createdAtUtc':datetime.now(timezone.utc).isoformat(),
          'zip':str(zip_path),'bytes':zip_path.stat().st_size,'sha256':sha_bytes(zip_path.read_bytes()),'payloadFiles':len(payload),
          'original152PayloadsUnchanged':True,'manifest':manifest,'candidateHashes':validation['candidateHashes'],
          'localChecks':496,'localFailures':0,'reproducedSourceChecks':460,'authoredSemanticAdjudications':32,'executedReferenceArithmeticAndBoundaryChecks':38,
          'exactLanguageApproval':False,'runtimeImplemented':False,'newClassSpellFeatApproval':False,'sourceInformationDeleted':0,'pushPerformed':False,'cosmologyReviewed':False}
    (A/'LANGUAGE_EXACT_V1_PREPARATION.json').write_text(json.dumps(prep,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    prompt=f'''Your final LA-SOURCE-2026-10-11 reply08f18635-6dea-4d41-8f11-19fafb1baf2c and complete final evidence package are preserved. All14 packaged file hashes match; your460 read-only source/reference checks reproduce with zero failures. I used the final verdict, not the intermediate live drafts.

Here is the complete first language/communication candidate for exact review: DD_Language_Communication_Exact_Review_v1.zip, {prep['bytes']:,} bytes, SHA256 {prep['sha256']}, {len(payload)} complete payloads plus manifest. Read README_LANGUAGE_EXACT_V1.md and FILE_MANIFEST.json, then the actual full public chapter, worked-sequence chapter, internal guide and both complete data envelopes.

All16 directions are applied, with NEW policies labeled. The candidate has all14 base grants,45 variants,20 backgrounds, explicit aliases/dialect/script/mode/choice records and eight concrete record contracts. It includes all48 selected class interfaces plus the actually called Heaven's Decree, all23 spell comparisons with15 unchanged pending routes,8 pending feat originals,40 unchanged completed Scribing records and19 unchanged completed advanced sections. The separate public envelope carries only the28 completed public Scribing cards. Original class/spell/feat status and source absence/null/value distinctions remain; the152 original payloads and runtime arrays are unchanged.

There are32 concrete chronological authored adjudications mapped to your exact checklist. Local validation has496 passing checks: static preservation/public parity and38 executable reference arithmetic/boundary checks. These are not gameplay-runtime tests, human trials or actual campaign facts. The completed public chapter covers ordinary training and tuition, interruption/Tongues losses, known translation versus supported deciphering, six-second aggregate speech, ten-minute/six-cue rehearsal, timed interpretation, component restrictions, exact class/oath windows, SC08 Insight and actual TI04 channels and shared budgets.

Please inspect the complete exact candidate and decide all32 checklist cases and LA01–16 applications. Where a correction is needed, provide the precise affected file/record and replacement wording, with finite regression expectations and a scoped conditional fulfillment path. Where it meets the source decisions, say what authored-language scope is accepted. No generic preliminary source conference is needed; no unseen candidate, pending spell or feat should be promoted.

Carry fulfilled NWX and687/433 recipe gates forward without re-reviewing them. DD01, remaining catalogs, expedition/bestiary/Director integration, human teaching/balance, companion implementation and final whole-game flow remain open. LA16 remains receipt-only; no cosmology interpretation. Final joint whole-game flow precedes the authorized GitHub push, and verified remote commit precedes careful cosmology review. No deletion or push has occurred.'''
    (A/'CODEX_LANGUAGE_EXACT_V1_PROMPT.txt').write_text(prompt,encoding='utf-8')
    print(json.dumps({k:prep[k] for k in ('bytes','sha256','payloadFiles','localChecks','localFailures')},indent=2))

if __name__=='__main__':main()
