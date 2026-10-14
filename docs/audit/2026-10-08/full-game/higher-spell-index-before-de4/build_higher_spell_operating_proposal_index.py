"""Index proposed higher-spell authoring without promoting catalog status."""
from pathlib import Path
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
import re

G = Path(r'C:\Github\DecenniumDescent')
R = G / 'DescentReviewChanges/ReviewBible'
A = G / 'docs/audit/2026-10-08/full-game'

def read(p):
    return json.loads(p.read_text('utf-8-sig'))

def info(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': sha256(b).hexdigest()}

def digest_record(d):
    return sha256(json.dumps(d, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()

def save(p, d):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')

def main():
    out = R / 'data/director/higher_spell_operating_proposal_index.json'
    doc = R / 'docs/spells/proposals/HIGHER_SPELL_OPERATING_PROPOSAL_INDEX.md'
    receipt = A / 'HIGHER_SPELL_OPERATING_PROPOSAL_INDEX_CHECK.json'
    assert not any(p.exists() for p in (out, doc, receipt)), 'Preserve existing index artifacts before revision'
    source_path = A / 'HIGHER_RANK_SPELL_FILE_HANDOFF_PREPARATION.json'
    catalog_path = R / 'data/public/spell_playtests/catalog.json'
    review_path = catalog_path.with_name('authored_review_index.json')
    proposal_path = R / 'data/director/spell_proposals/abjuration_conjuration_rank4.json'
    proposal_doc = R / 'docs/spells/proposals/ABJURATION_CONJURATION_RANK4.md'
    proposal_check = A / 'ABJURATION_CONJURATION_RANK4_OPERATING_PROPOSAL_CHECK.json'
    source = read(source_path)
    catalog = {x['id']: x for x in read(catalog_path)['spells']}
    review = read(review_path)
    reviews = {x['id']: x for x in review['entries']}
    proposal = read(proposal_path)
    proposals = {x['spellId']: x for x in proposal['records']}
    proposal_receipt = read(proposal_check)
    inputs = {p: info(p) for p in (source_path, catalog_path, review_path, proposal_path, proposal_doc, proposal_check, Path(__file__).resolve())}
    checks = []
    def check(label, value):
        checks.append({'name': label, 'pass': bool(value)})
        assert value, label
    check('Current catalog is 848 with 412 reviewed and 436 pending', len(catalog) == 848 and review['authoredCounts'] == {'reviewed': 412, 'pending': 436})
    check('Exactly 435 distinct higher-rank source identities', len(source['selectedMembership']) == 435 and len({x['spellId'] for x in source['selectedMembership']}) == 435)
    check('All proposal outputs match their emitted receipt', all(info(G / rel) == expected for rel, expected in proposal_receipt['artifacts'].items()))
    check('Proposals do not claim runtime or cosmology completion', proposal['runtimeImplemented'] is False and proposal['cosmologyReviewed'] is False)
    entries = []
    for m in source['selectedMembership']:
        sid = m['spellId']
        current = catalog[sid]
        check(sid + ' complete original source record preserved', digest_record(current) == m['recordSha256'])
        check(sid + ' remains pending in actual authored index', reviews[sid]['authoredStatus'] == 'pending-authored-procedure')
        prep = G / m['preparationFile']
        check(sid + ' original question source exists', prep.is_file())
        if prep not in inputs:
            inputs[prep] = info(prep)
        deferred = sid in source['postPushReceiptOnlyIds']
        p = proposals.get(sid)
        check(sid + ' no mechanical proposal crosses the post-push boundary', not (deferred and p))
        entries.append({
            **m, 'name': current['name'], 'classAccess': current['classAccess'],
            'currentAuthoredStatus': reviews[sid]['authoredStatus'],
            'proposalState': 'post-push-literal-receipt-only' if deferred else 'complete-unadopted-unsent-proposal' if p else 'source-question-prepared-procedure-not-yet-proposed',
            'proposalFile': proposal_path.relative_to(G).as_posix() if p else None,
            'proposalDocument': proposal_doc.relative_to(G).as_posix() if p else None,
            'authoredExamples': len(p['workedCases']) if p else 0,
            'jointReviewCompleted': False,
        })
    check('Fifteen proposed and 373 remaining pre-push mechanical entries', sum(e['proposalState'] == 'complete-unadopted-unsent-proposal' for e in entries) == 15 and sum(e['proposalState'] == 'source-question-prepared-procedure-not-yet-proposed' for e in entries) == 373)
    check('All 47 literal post-push source receipts preserved', sum(e['proposalState'] == 'post-push-literal-receipt-only' for e in entries) == 47)
    check('Blink is the only unreviewed ordinary identity outside higher-rank membership', {x['id'] for x in review['entries'] if x['authoredStatus'] != 'reviewed-authored-operational-playtest'} - {e['spellId'] for e in entries} == {'blink'})
    check('Blink retains its separate post-push receipt status', reviews['blink']['authoredStatus'] == 'receipt-only-post-push-cosmology')
    frozen = read(A / 'EXPEDITION_INTEGRATED_V3_PREPARATION.json')['manifest']
    for rel, expected in frozen.items():
        if rel != 'README_EXPEDITION_INTEGRATED_V3.md':
            check('Live expedition input unchanged: ' + rel, info(G / rel) == expected)
    now = datetime.now(timezone.utc).isoformat()
    counts = {'higherRankIdentities': 435, 'prePushMechanicalQuestions': 388, 'completeUnadoptedUnsentProcedures': 15, 'mechanicalProceduresStillToPropose': 373, 'literalPostPushReceipts': 47, 'authoredExamples': 30, 'ordinarySpellsReviewedUnchanged': 412, 'ordinarySpellsPendingUnchanged': 436}
    status = 'Navigation only. Proposals are unadopted and unsent; no ordinary spell status, class access, source or approval is changed.'
    save(out, {'status': status, 'createdAtUtc': now, 'counts': counts, 'entries': entries, 'pendingOutsideHigherRankScope': ['blink'], 'historicalPreparationNote': 'The source preparation freezes original membership/questions. Its older reviewed/pending totals are historical; current totals come from the live authored review index.', 'inputs': {p.relative_to(G).as_posix(): v for p, v in inputs.items()}, 'sourceInformationDeleted': 0, 'cosmologyReviewed': False, 'pushed': False})
    def link(p):
        return Path(os.path.relpath(p, doc.parent)).as_posix()
    lines = ['# Higher spell operating proposal index', '', '**Unadopted and unsent.** This index separates proposed procedures from preserved source questions. It grants no new spell access or approval.', '',
             'Of 435 higher-rank identities, 388 have mechanical questions that can be resolved before the push. Fifteen now have complete proposed procedures and 30 authored examples; 373 still need procedures. The other 47 remain literal source receipts for the later cosmology review.', '',
             'The current ordinary catalog remains **412 reviewed / 436 pending**. Blink is the one unreviewed identity outside this higher-rank list and retains its separate post-push receipt status. Runtime implementation, human balance and the final joint whole-game flow review remain separate work.', '',
             '[Complete structured index](' + link(out) + ') · [Preservation checks](' + link(receipt) + ')', '',
             '## First proposed group', '',
             '[Rank-four Abjuration and Conjuration](' + link(proposal_doc) + ') includes every original source/access record, both printed Elemental Drain amounts, both Alignment Anchor placements, 37 complete current spell comparisons and an explicitly new Faction Envoy profile. Banishment remains unchanged. These proposals have not yet been sent to GPT.', '',
             '## All higher-rank identities', '',
             '| Source question | Spell | Treatment | Evidence |', '| --- | --- | --- | --- |']
    labels = {'post-push-literal-receipt-only': 'Literal receipt; post-push', 'complete-unadopted-unsent-proposal': 'Procedure proposed; joint review pending', 'source-question-prepared-procedure-not-yet-proposed': 'Source question prepared; procedure needed'}
    for e in entries:
        target = G / (e['proposalDocument'] or e['preparationFile'])
        lines.append('| ' + e['questionId'] + ' | ' + e['name'].replace('|', '\\|') + ' | ' + labels[e['proposalState']] + ' | [Read](' + link(target) + ') |')
    lines += ['', 'Original question identifiers and source hashes remain authoritative for scope. Older preparation snapshots and archives retain their historical counts. Refresh those packets against completed expedition and other intervening decisions before dispatch; an index is not a substitute for reading and discussing the actual procedures.', '']
    doc.parent.mkdir(parents=True, exist_ok=True)
    doc.write_text('\n'.join(lines), encoding='utf-8', newline='\n')
    for target in set(re.findall(r'\[[^\]]*\]\(([^)]+)\)', doc.read_text('utf-8'))):
        p = (doc.parent / target).resolve()
        check('Index link ' + target, p.is_file() or p == receipt)
    for p, expected in inputs.items():
        check('Index input unchanged: ' + p.relative_to(G).as_posix(), info(p) == expected)
    result = {'status': status, 'createdAtUtc': now, 'counts': counts, 'checks': len(checks), 'failures': 0, 'runtimeCases': 0, 'submittedCurrentPayloadsUnchanged': 303, 'artifacts': {p.relative_to(G).as_posix(): info(p) for p in (out, doc)}, 'details': checks}
    save(receipt, result)
    print(json.dumps({k: v for k, v in result.items() if k != 'details'}, ensure_ascii=False))

if __name__ == '__main__':
    main()
