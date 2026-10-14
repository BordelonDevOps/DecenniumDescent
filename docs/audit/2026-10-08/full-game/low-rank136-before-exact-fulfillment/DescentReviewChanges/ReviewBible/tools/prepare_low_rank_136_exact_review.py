"""Freeze a complete internal review packet; never overwrite a frozen submission."""
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import ast
import hashlib
import json

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'
P = A / 'low-rank137-source-reviewer-files'


def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    target = A / 'DD_Low_Rank_136_Exact_Review_v1.zip'
    assert not target.exists(), 'Never overwrite an immutable review submission'
    validation = read(A / 'LOW_RANK_136_CANDIDATE_LOCAL_VALIDATION.json')
    assert all(c['pass'] for c in validation['checks']) and len(validation['checks']) == 49
    authored = read(A / 'LOW_RANK_136_CANDIDATE_AUTHORING_RECEIPT.json')
    payload = {}
    def add(p):
        key = p.relative_to(G).as_posix()
        data = p.read_bytes()
        if key in payload:
            assert payload[key] == data, key
        payload[key] = data
    original = A / 'DD_Low_Rank_Spells_137_Source_Prepared_v3.zip'
    with ZipFile(original) as z:
        manifest = json.loads(z.read('FILE_MANIFEST.json'))
        for path, e in manifest.items():
            data = z.read(path)
            assert sha(data) == e['sha256']
            if (G/path).is_file():
                assert data == (G/path).read_bytes(), path
            payload[path] = data
        payload['ORIGINAL_SOURCE_V3_FILE_MANIFEST.json'] = z.read('FILE_MANIFEST.json')
    protected = read(A / 'LOW_RANK_SPELL_FILE_HANDOFF_V3_PREPARATION.json')['currentFileHashes']
    assert len(protected) == 342
    assert all(sha(payload[path]) == expected == sha((G/path).read_bytes()) for path,expected in protected.items())
    for path, info in authored['artifacts'].items():
        assert sha((G/path).read_bytes()) == info['sha256']
        add(G/path)
    extra = [original, A/'LOW_RANK_136_CANDIDATE_AUTHORING_RECEIPT.json',
             A/'LOW_RANK_136_CANDIDATE_LOCAL_VALIDATION.json',
             A/'LOW_RANK_137_SOURCE_VERDICT_RECEIPT.json',
             A/'LOW_RANK_137_FINAL_BROWSER_REPLY.txt',
             A/'LANGUAGE_EXACT_FULFILLMENT.json',
             A/'ONBOARDING_CHARTER_EXACT_FULFILLMENT.json',
             A/'ADVANCED_167_EXACT_PROMOTION_RECEIPT.json',
             R/'docs/mechanics/LANGUAGE_REVIEW_STATUS.json',
             R/'docs/playtest/ONBOARDING_REVIEW_STATUS.json',
             R/'docs/mechanics/ADVANCED_CRAFT_REVIEW_STATUS.json']
    for p in extra:
        add(p)
    for p in P.rglob('*'):
        if p.is_file():
            add(p)
    # Include every local Python dependency needed by the candidate scripts.
    pending = [Path(__file__), R/'tools/build_low_rank_136_candidates.py', R/'tools/validate_low_rank_136_candidates.py']
    visited = set()
    while pending:
        p = pending.pop()
        if p in visited:
            continue
        visited.add(p); add(p)
        tree = ast.parse(p.read_text(encoding='utf-8-sig'))
        for node in ast.walk(tree):
            names = [a.name.split('.')[0] for a in node.names] if isinstance(node, ast.Import) else [node.module.split('.')[0]] if isinstance(node, ast.ImportFrom) and node.module else []
            for name in names:
                local = R/'tools'/f'{name}.py'
                if local.is_file() and local not in visited:
                    pending.append(local)
    readme = '''# Complete low-rank spell candidate — exact review v1

INTERNAL joint-review packet. Contains complete private comparison/source evidence. This archive is not a public distribution package; its separately identified public candidate contains only the selected public spell originals and their new authored procedures.

Start with these actual full artifacts under DescentReviewChanges/ReviewBible:

- docs/playtest/LOW_RANK_136_CANDIDATE.md: every full card and all 20 shared rules, including the nonoperative Blink receipt.
- data/playtest/spell_drafts/candidate_low_rank_136.json: complete internal 137-identity envelope, every original source-authoring record, full current public source receipts, exact class access, 141 book bindings, mode/alias decisions and 136 operationalCandidate objects.
- data/public/spell_playtests/candidate_low_rank_136.json and matching .md: complete actual public envelope and manuscript. No internalSourceAuthoringRecord or private comparison catalogs are projected into it. All 137 sourceReceipt objects are exactly equal to the existing public catalog. No catalog promotion has occurred.
- docs/playtest/LOW_RANK_137_AUTHORED_BOUNDARIES.md and data/playtest/spell_drafts/low_rank_137_authored_boundaries.json: all 187 complete authored boundary records. Matching public JSON and manuscript are in data/public/spell_playtests.

Audit artifacts under docs/audit/2026-10-08/full-game:

- LOW_RANK_136_CANDIDATE_QUESTION_MAP.json: every original question mapped to the actual full candidate paragraph, preserved modes and book bindings.
- LOW_RANK_136_CANDIDATE_AUTHORING_RECEIPT.json: all authored artifact hashes, 136 procedures, Blink receipt, 141 bindings and preserved inputs.
- LOW_RANK_136_CANDIDATE_LOCAL_VALIDATION.json: 49 passing checks covering exact source preservation, whole public parity, manuscript paragraphs, all 187 boundaries, seven deliberate corruption cases, existing helper cases and four transparent arithmetic cases. The access/pricing sweeps comprise 18,840 real class/level gates and 2,808 ordinary pricing calculations. Quotation fixtures temporarily assume approved status ONLY in local memory; no such fixture is written to any source/catalog file.
- low-rank137-source-reviewer-files/: all 28 final source-verdict package files, with original manifest and evidence; final source review LR-SOURCE-2026-10-11/reply 6ecc2e79-e637-4c69-ac48-61069296008c.

All 342 submitted original payloads remain identical at their original paths. ORIGINAL_SOURCE_V3_FILE_MANIFEST.json preserves the original manifest. The original v3 source ZIP is also included intact so the reviewer source reproduction scripts have the exact input archive. Their reported 3,476/3,726 checks have NOT been rerun locally; do not confuse those reviewer reports with the new 49 local checks. No reviewer script has been executed locally. Inspect scripts before running them in a fresh extracted workspace.

The new builder copies all final operative directions into complete candidate fields, with only five explicit editorial introduction removals. NEW clauses remain labeled. Complete source-authoring records and original source fields remain intact. Candidates are authored tabletop procedures, not deployed engine implementations. They use operationalCandidate rather than the live operational catalog slot, which remains null for every selected identity. Components/mode/range prose is intentionally retained in full rather than reduced to a lossy scalar model; any later runtime adapter is a separate task.

The 187 examples are authored expectations, NOT 187 executed gameplay tests. Existing helpers validate only their stated access/cost/roll/HP/clock scope. No complete new spell controller, sensing, trigger, wrapper, summons, class-specific hook execution, world premise authentication, human teaching trial or numerical balance approval is claimed. In particular, the original class/spell/feat comparison statuses are unchanged.

Please exact-review all LRE-01 through LRE-13 groups against the ACTUAL full artifacts and the final source directions. Return precise bounded corrections by spell ID/JSON path/manuscript paragraph with replacement wording and finite acceptance cases, or scoped authored-candidate acceptance. Do not reopen a generic preliminary source conference. One tiny editorial point to assess: TR-28 Enhance Ability is explicitly concentration up to TEN minutes; its preserved source boundary uses the shorthand “minute window.” The duration is not reduced to one minute by that example.

Carry fulfilled LAX language, NWX teaching and 687 internal/433 public recipe gates forward. Current ordinary spell totals are still 276 operational / 572 pending. Blink stays receipt-only, as do unassigned higher-rank alternatives. Literal setting terms receive no new interpretation. Final actual joint whole-game flow review must precede the already authorized GitHub push; verified remote commit must precede careful cosmology review. Source preservation/deletion constraints remain in force. There is no newly inferred owner-approval gate from notebook wording.

The validator writes only its named local report when deliberately run in a fresh extracted workspace. The builder writes its explicitly named candidate artifacts; the packaging script refuses to overwrite its existing frozen ZIP. All protected source hashes are checked before writing.
'''
    payload['README_LOW_RANK_EXACT_V1.md'] = readme.encode('utf-8')
    manifest = {name:{'bytes':len(data),'sha256':sha(data)} for name,data in sorted(payload.items())}
    with ZipFile(target,'w',ZIP_DEFLATED,compresslevel=9) as z:
        for name,data in sorted(payload.items()):
            z.writestr(name,data)
        z.writestr('FILE_MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    with ZipFile(target) as z:
        assert len(z.namelist()) == len(manifest)+1
        assert all(sha(z.read(name)) == e['sha256'] for name,e in manifest.items())
    receipt = {'status':'prepared-not-yet-submitted','createdAtUtc':datetime.now(timezone.utc).isoformat(),
               'zip':str(target),'bytes':target.stat().st_size,'sha256':sha(target.read_bytes()),
               'payloadFiles':len(manifest),'manifest':manifest,'originalSubmittedPayloadsUnchanged':342,
               'mechanicalCandidates':136,'receiptOnly':['blink'],'sharedRules':20,'bookBindings':141,
               'authoredBoundaryRecords':187,'localChecks':49,'localFailures':0,
               'accessBoundaryTrials':18840,'ordinaryPriceTrials':2808,'sourceRecordsPromoted':0,
               'runtimeVerified':False,'exactCandidateApproval':False,'sourceDeleted':0,'pushPerformed':False}
    (A/'LOW_RANK_136_EXACT_V1_PREPARATION.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    prompt = f'''Your final LR-SOURCE-2026-10-11 verdict/reply 6ecc2e79-e637-4c69-ac48-61069296008c is preserved with all 28 packaged files and verified hashes. Here is the actual complete candidate requested for separate exact review: DD_Low_Rank_136_Exact_Review_v1.zip, {receipt['bytes']:,} bytes, SHA256 {receipt['sha256']}, {len(manifest)} full payloads plus manifest.

Please read README_LOW_RANK_EXACT_V1.md, FILE_MANIFEST.json, the full LOW_RANK_136_CANDIDATE.md manuscript and both actual candidate_low_rank_136.json envelopes, then the full boundary casebook and question map. All 136 procedures are present, with 20 full shared rules, all original 137 records, 141 book bindings, exact current class access and all assigned/unassigned modes. Blink stays operationally null and unavailable. No catalog selection or promotion has changed.

Local verification: 49 passing bounded checks, including 18,840 class/level gates, 2,808 ordinary price quotations, full public/source equality, manuscript content, 187 full authored boundary records, seven deliberate-corruption rejection cases and existing Core/clock/HP reference cases. Those do not execute the entire spell procedures or class hooks and do not establish human balance. Reviewer source scripts have not been locally rerun; their reported totals are preserved as your evidence, not misrepresented as my local result. All 342 original submitted files remain byte-identical; the full original v3 ZIP and all final source-verdict files are included.

Please inspect the exact full candidate against every LRE-01 through LRE-13 group, all original questions and the 187 authored examples. Give either precise bounded corrections with affected file/record, exact replacement wording and acceptance cases, or scoped authored-candidate acceptance. Source questions are already resolved; no new generic preliminary conference is needed. The separate candidate representation retains full mode/components/range prose and does not pretend to be an implemented runtime adapter. TR-28's duration is explicitly ten minutes; please clarify its inherited boundary shorthand “minute window” if useful.

Carry fulfilled LAX/NWX and 687/433 recipe gates without reopening them. Actual ordinary totals remain 276 operational / 572 pending, and comparison class/feat/spell statuses remain unchanged. No source deletion, push, full-game-flow, human/runtime or cosmology approval is asserted. The human already authorized pushing after actual final joint Codex/GPT whole-game flow agreement; careful cosmology review follows that push and verified remote commit. Please preserve that order without introducing an additional owner confirmation requirement.'''
    (A/'CODEX_LOW_RANK_136_EXACT_V1_PROMPT.txt').write_text(prompt,encoding='utf-8')
    print(json.dumps({k:receipt[k] for k in ['bytes','sha256','payloadFiles','mechanicalCandidates','localChecks']},indent=2))


if __name__ == '__main__':
    main()
