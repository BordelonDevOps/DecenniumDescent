"""Index proposed higher-spell authoring without promoting catalog status."""
from pathlib import Path
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
import re
import zipfile

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
    previous = read(A / 'higher-spell-index-before-ac6/PRESERVATION_MANIFEST.json')
    for p in (out, doc, receipt):
        old = previous[p.relative_to(G).as_posix()]
        assert info(p) == {k: old[k] for k in ('bytes', 'sha256')}, 'Preserved prior index must still match before this one-use update'
    source_path = A / 'HIGHER_RANK_SPELL_FILE_HANDOFF_PREPARATION.json'
    catalog_path = R / 'data/public/spell_playtests/catalog.json'
    review_path = catalog_path.with_name('authored_review_index.json')
    source = read(source_path)
    catalog = {x['id']: x for x in read(catalog_path)['spells']}
    review = read(review_path)
    reviews = {x['id']: x for x in review['entries']}
    inputs = {p: info(p) for p in (source_path, catalog_path, review_path, Path(__file__).resolve())}
    feat_dispatch_path = A / 'FEAT_AUTHORED_V3_SUBMISSION.json'
    feat_dispatch = read(feat_dispatch_path)
    feat_archive = G / feat_dispatch['archive']['path']
    assert info(feat_archive)['sha256'] == feat_dispatch['archive']['sha256'] and feat_dispatch['sent'] is True
    with zipfile.ZipFile(feat_archive) as z:
        frozen_higher = json.loads(z.read(out.relative_to(G).as_posix()))
    shared_comparisons = {e['spellId'] for e in frozen_higher['entries'] if e['proposalFile']}
    assert len(shared_comparisons) == 71
    inputs[feat_dispatch_path] = info(feat_dispatch_path)
    checks = []
    def check(label, value):
        checks.append({'name': label, 'pass': bool(value)})
        assert value, label
    check('Current catalog is 848 with 412 reviewed and 436 pending', len(catalog) == 848 and review['authoredCounts'] == {'reviewed': 412, 'pending': 436})
    check('Exactly 435 distinct higher-rank source identities', len(source['selectedMembership']) == 435 and len({x['spellId'] for x in source['selectedMembership']}) == 435)
    proposals, proposal_locations, cohorts = {}, {}, []
    for stem, label in [('abjuration_conjuration_rank4', 'Rank-four Abjuration and Conjuration'), ('divination_enchantment_rank4', 'Rank-four Divination and Enchantment'), ('evocation_rank4', 'Rank-four Evocation'), ('illusion_necromancy_rank4', 'Rank-four Illusion and Necromancy'), ('transmutation_universal_rank4', 'Rank-four Transmutation and Universal'), ('evocation_rank5', 'Rank-five Evocation'), ('enchantment_illusion_rank5', 'Rank-five Enchantment and Illusion'), ('necromancy_transmutation_rank5', 'Rank-five Necromancy and Transmutation'), ('abjuration_conjuration_rank5', 'Rank-five Abjuration and Conjuration'), ('divination_universal_rank5', 'Rank-five Divination and Universal'), ('evocation_rank6', 'Rank-six Evocation'), ('enchantment_rank6', 'Rank-six Enchantment'), ('illusion_necromancy_rank6', 'Rank-six Illusion and Necromancy'), ('abjuration_conjuration_rank6', 'Rank-six Abjuration and Conjuration')]:
        proposal_path = R / 'data/director/spell_proposals' / (stem + '.json')
        proposal_doc = R / 'docs/spells/proposals' / (stem.upper() + '.md')
        proposal_check = A / (stem.upper() + '_OPERATING_PROPOSAL_CHECK.json')
        proposal = read(proposal_path)
        proposal_receipt = read(proposal_check)
        inputs.update({p: info(p) for p in (proposal_path, proposal_doc, proposal_check)})
        check(stem + ' all outputs match emitted receipt', all(info(G / rel) == expected for rel, expected in proposal_receipt['artifacts'].items()))
        check(stem + ' no runtime or cosmology completion claim', proposal['runtimeImplemented'] is False and proposal['cosmologyReviewed'] is False)
        for p in proposal['records']:
            sid = p['spellId']
            check(sid + ' no duplicate cohort procedure', sid not in proposals)
            proposals[sid] = p
            proposal_locations[sid] = (proposal_path, proposal_doc)
        cohorts.append({'label': label, 'document': proposal_doc.relative_to(G).as_posix(), 'records': len(proposal['records'])})
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
            'proposalState': 'post-push-literal-receipt-only' if deferred else 'complete-unadopted-proposal' if p else 'source-question-prepared-procedure-not-yet-proposed',
            'proposalFile': proposal_locations[sid][0].relative_to(G).as_posix() if p else None,
            'proposalDocument': proposal_locations[sid][1].relative_to(G).as_posix() if p else None,
            'authoredExamples': len(p['workedCases']) if p else 0,
            'jointReviewCompleted': False,
            'sharedAsFeatComparison': sid in shared_comparisons,
            'comparisonRequestId': feat_dispatch['requestId'] if sid in shared_comparisons else None,
            'dedicatedSpellReviewSubmitted': False,
        })
    check('162 proposed and226 remaining pre-push mechanical entries', sum(e['proposalState'] == 'complete-unadopted-proposal' for e in entries) == 162 and sum(e['proposalState'] == 'source-question-prepared-procedure-not-yet-proposed' for e in entries) == 226)
    check('71 previously shared comparisons and91 unshared drafts', shared_comparisons <= set(proposals) and len(set(proposals)-shared_comparisons)==91)
    check('324 complete authored examples',sum(e['authoredExamples'] for e in entries)==324)
    check('All 47 literal post-push source receipts preserved', sum(e['proposalState'] == 'post-push-literal-receipt-only' for e in entries) == 47)
    check('Blink is the only unreviewed ordinary identity outside higher-rank membership', {x['id'] for x in review['entries'] if x['authoredStatus'] != 'reviewed-authored-operational-playtest'} - {e['spellId'] for e in entries} == {'blink'})
    check('Blink retains its separate post-push receipt status', reviews['blink']['authoredStatus'] == 'receipt-only-post-push-cosmology')
    frozen = read(A / 'EXPEDITION_INTEGRATED_V3_PREPARATION.json')['manifest']
    for rel, expected in frozen.items():
        if rel != 'README_EXPEDITION_INTEGRATED_V3.md':
            check('Live expedition input unchanged: ' + rel, info(G / rel) == expected)
    now = datetime.now(timezone.utc).isoformat()
    counts = {'higherRankIdentities': 435, 'prePushMechanicalQuestions': 388, 'completeUnadoptedProcedures': 162, 'sharedOnlyAsFeatComparisons': 71, 'completeUnadoptedUnsentProcedures': 91, 'mechanicalProceduresStillToPropose': 226, 'literalPostPushReceipts': 47, 'authoredExamples': 324, 'ordinarySpellsReviewedUnchanged': 412, 'ordinarySpellsPendingUnchanged': 436}
    status = 'Navigation only. All162 procedures remain unadopted;71 were shared only as comparisons in the feat conference and91 remain unsent. No dedicated higher-spell review, ordinary spell status, class access, source or approval is changed.'
    save(out, {'status': status, 'createdAtUtc': now, 'counts': counts, 'entries': entries, 'pendingOutsideHigherRankScope': ['blink'], 'historicalPreparationNote': 'The source preparation freezes original membership/questions. Its older reviewed/pending totals are historical; current totals come from the live authored review index.', 'inputs': {p.relative_to(G).as_posix(): v for p, v in inputs.items()}, 'sourceInformationDeleted': 0, 'cosmologyReviewed': False, 'pushed': False})
    def link(p):
        return Path(os.path.relpath(p, doc.parent)).as_posix()
    lines = ['# Higher spell operating proposal index', '', '**Unadopted; dedicated joint spell review pending.** The earlier 71 drafts were shared as comparisons in the feat conference. Ninety-one new drafts have not yet been shared. This index grants no spell access or approval.', '',
             'Of 435 higher-rank identities, 388 have mechanical questions that can be resolved before the push. 162 now have complete proposed procedures and 324 authored examples; 226 still need procedures. The other 47 remain literal source receipts for the later cosmology review.', '',
             'The current ordinary catalog remains **412 reviewed / 436 pending**. Blink is the one unreviewed identity outside this higher-rank list and retains its separate post-push receipt status. Runtime implementation, human balance and the final joint whole-game flow review remain separate work.', '',
             '[Complete structured index](' + link(out) + ') · [Preservation checks](' + link(receipt) + ')', '',
             '## Proposed groups', '',
             *['- [' + c['label'] + '](' + link(G / c['document']) + '): ' + str(c['records']) + ' proposed procedures.' for c in cohorts], '',
             'Each group includes complete source/access records and current comparisons. The first preserves both Elemental Drain amounts and Alignment Anchor placements, with an explicitly new Faction Envoy. The second preserves Confusion and Phantasmal Killer school modes and flags eight decisions, including the already-reviewed cantrip’s exact RP readout. The third completes all eight rank-four Evocation procedures with sixteen examples and ten explicit issues, preserving source dice and defining field, terrain, control and delayed-damage timing. The fourth completes thirteen Illusion/Necromancy procedures with twenty-six examples and fourteen issues, including Soulburn Pact’s conflicting recovery amounts and retained seven-RP casting price. Its twenty-seven whole current counterparts include the seven lower-rank records completed since source preparation. The fifth adds twelve Transmutation/Universal procedures and twenty-four examples, with thirty whole counterpart records, thirteen class envelopes and fifteen explicit issues. Its time, reversal, spell-transfer and instant craft rules remain proposed. The sixth completes eight rank-five Evocation procedures and sixteen examples, retaining both school modes of Synaptic Static and explicit choices for area, repeat damage, hostile selection and control. It binds the completed EX58 descendant and legal example RP maxima. Banishment and Veiled Chest remain unchanged literal receipts. The seventh adds fourteen rank-five Enchantment/Illusion procedures and twenty-eight examples, including the Reaction trigger, long compulsion, finite illusion effects, real Creation output and local Dream. Its twenty-one current counterparts, six earlier proposals, current Group Illusion comparison and six full class envelopes remain distinct. The eighth adds sixteen rank-five Necromancy/Transmutation procedures and thirty-two examples, with twenty-two whole current counterparts, five complete prior draft counterparts and eight class envelopes. Its seventeen explicit review issues cover full dying recovery, finite disease and drain, five-body animation, actual terrain/mass conversion, localized stone anatomy, autonomous awakening, passage closure and instantaneous telekinesis. The ninth adds eleven rank-five Abjuration/Conjuration procedures and twenty-two examples, preserving five post-push receipts without interpretation. Its twenty-eight full current counterparts, four earlier drafts, current Resonance Barrier comparison and eight class envelopes support fourteen explicit issues, including local antimagic, mass dispelling, force-wall topology, genuine RP conversion, final pricing and institutional standing protection. The tenth adds eleven rank-five Divination/Universal procedures and twenty-two examples, preserving four post-push receipts. Its twenty-four whole current counterparts, seven earlier proposals and nine class envelopes support thirteen explicit review issues: premonition outcomes, source-range conflicts, memory and agency, institutional forecasts, temporary spell access, separate cast costs, dispel protection, atomic swaps, permanent circle operation, voluntary communication and established lore. The eleventh adds eight rank-six Evocation procedures and sixteen examples, with fifteen complete current counterparts, six earlier proposals and seven class envelopes. Its twelve joint issues cover visual blindness, actual time suspension, three-shot cannon operation, structural collapse, lightning arcs, disintegration and real ice. These remain proposed rules, with no temporal/device runtime integration approval. The twelfth adds seven rank-six Enchantment procedures and fourteen examples while preserving Soul Cage as an untouched post-push receipt. Its fifteen current counterparts, seven prior proposals and seven class envelopes support thirteen explicit issues: independent charm, recent episodic-memory loss and recovery, movement control, spell/item-use restriction, mental prison transitions, twelve-recipient24-hour suggestion and full-Action dance. The Haze/Woven recovery bridge and Mass Suggestion duration harmonization are expressly new proposals. The thirteenth adds thirteen rank-six Illusion/Necromancy procedures and twenty-six examples, with fifteen full current counterparts, eight prior proposals and seven class envelopes. Four explicitly new Ghoul/Ghast/Wight/Mummy profiles retain their unrated CR and remain separate from the current bestiary. Seventeen joint issues cover truth and illusion perception, finite detonations, real Prone, programmed triggers, incorporeal movement and lifetap, periodic fog damage, permanent binding/creation and three Eyebite modes. These are new proposals with no catalog or runtime promotion. The fourteenth adds eleven rank-six Abjuration/Conjuration procedures and twenty-two examples, sixteen current counterparts, eight earlier proposals and eight full class envelopes. Sixteen joint issues cover the incoming rank barrier, three constituent wards, alignment predicates, seven-day anchoring, stronger cleansing, projectile defense, elemental resistance, randomized arcs, two-attack commands, accelerated forge work and many-body army limits. The Forge conversion and cross-family Seal restriction are explicitly new decisions. Three cosmology-related identities remain literal receipts. The earlier71 drafts were shared only as comparisons with the feat conference; the new91 have not yet been shared. None has completed its dedicated higher-spell review.', '',
             '## All higher-rank identities', '',
             '| Source question | Spell | Treatment | Evidence |', '| --- | --- | --- | --- |']
    labels = {'post-push-literal-receipt-only': 'Literal receipt; post-push', 'complete-unadopted-proposal': 'Procedure proposed; joint review pending', 'source-question-prepared-procedure-not-yet-proposed': 'Source question prepared; procedure needed'}
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
