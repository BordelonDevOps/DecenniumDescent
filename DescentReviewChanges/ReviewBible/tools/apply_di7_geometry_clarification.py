"""Apply the terminal geometry source addendum, with exact reversible edits."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded, node


def read(p): return json.loads(p.read_bytes())


def main():
    receipt = A / 'DI7_GEOMETRY_3D_RECEIVED.json'
    delta = A / 'DI7_GEOMETRY_DERIVED_OPERATIONS.json'
    preservation = A / 'source-before-di7-geometry'
    assert all(not p.exists() for p in [receipt, delta, preservation])
    now = datetime.now(timezone.utc).isoformat()
    dom = (A / 'DI7_GEOMETRY_3D_RECEIVED_DOM.txt').read_text(encoding='utf-8')
    assert 'DI7-GEOMETRY-3D-01 — controlling source addendum' in dom and 'Response complete' in dom
    assert 'button "Stop"' not in dom
    replacements = {sid: (A / filename).read_text(encoding='utf-8') for sid, filename in [
        ('mass-revelation', 'DI7_GEOMETRY_MASS_REPLACEMENT.txt'),
        ('resonance-sight-supreme', 'DI7_GEOMETRY_SUPREME_REPLACEMENT.txt')]}
    for replacement in replacements.values():
        assert len(replacement.split('\n\n')) == 4
        for paragraph in replacement.split('\n\n'): assert paragraph in dom
    receipt.write_bytes(encoded({'id': 'DI7-GEOMETRY-3D-01', 'recordedAtUtc': now,
        'status': 'terminal-source-addendum-received', 'question': info(A / 'DI7_GEOMETRY_3D_QUESTION.txt'),
        'sentProof': info(A / 'DI7_GEOMETRY_3D_SENT.png'), 'responseDom': info(A / 'DI7_GEOMETRY_3D_RECEIVED_DOM.txt'),
        'visibleProof': info(A / 'DI7_GEOMETRY_3D_RECEIVED.png'),
        'exactReplacements': [info(A / 'DI7_GEOMETRY_MASS_REPLACEMENT.txt'), info(A / 'DI7_GEOMETRY_SUPREME_REPLACEMENT.txt')],
        'classification': 'KEEP horizontal grid metric and axial/circular cone. NEW scoped vertical Supreme metric, Supreme fixed-center resolution revalidation and Mass fixed-origin resolution check.',
        'newRuleAdoptions': 3, 'scope': 'These two DI7 procedures only; no general movement/3D/targeting rule.',
        'reviewerDidNotRerunTests': True, 'exactCardsApproved': False, 'full49Fulfilled': False,
        'replyReceived': True, 'pendingResponse': False, 'pushed': False, 'cosmologyReviewed': False}))
    public_path = R / 'data/public/spell_candidates/divination_rank7_exact_01.json'
    internal_path = R / 'data/director/spell_candidates/divination_rank7_exact_01.json'
    manuscript_path = R / 'docs/spells/candidates/DIVINATION_RANK7_EXACT_01.md'
    expectations_path = R / 'data/playtest/spell_candidates/divination_rank7_exact_01_expectations.json'
    paths = [public_path, internal_path, manuscript_path, expectations_path]
    original_bytes = {p: p.read_bytes() for p in paths}
    public = read(public_path); internal = read(internal_path); expectations = read(expectations_path)
    original_groups = deepcopy(expectations['groups'])
    assert internal['completePublicEnvelope'] == public and internal['publicEnvelopeBinding'] == info(public_path)
    assert internal['finiteExpectations'] == expectations and not public['selectionEnabled'] and not public['exactReviewReceived']
    changed_procedures = []
    for sid, index, prefix in [('mass-revelation', 1, 'NEW exact fallback template'), ('resonance-sight-supreme', 0, 'KEEP Action/V/S/F/base 17 RP')]:
        card_index = next(i for i, c in enumerate(public['cards']) if c['id'] == sid)
        old = public['cards'][card_index]['operationalCandidate']['completeProcedure']
        paragraphs = old.split('\n\n'); assert paragraphs[index].startswith(prefix)
        paragraphs[index] = replacements[sid]; new = '\n\n'.join(paragraphs)
        changed_procedures.append((sid, card_index, old, new))
    addenda_before = deepcopy(public['sourceDirectionAddenda'])
    addenda_after = addenda_before + [{'id': 'DI7-GEOMETRY-3D-01', 'affectedSpellIds': list(replacements),
        'authority': info(receipt), 'scope': 'Scoped 3D area definitions and fixed committed geometry resolution checkpoints.', 'exactApproval': False}]
    variants = []
    for n, (point, inside) in enumerate([([20,20,0], True), ([20,20,20], True), ([0,0,20], True), ([20,0,5], True), ([25,0,0], False)], 1):
        variants.append({'id': 'DI7-GEO-S'+str(n), 'kind': 'supreme-cell-membership', 'offset': point,
            'expectedInside': inside, 'qualification': 'Membership only; actual current clipping and information protections remain.'})
    for n, (point, legal) in enumerate([([120,120,120], True), ([125,0,0], False)], 1):
        variants.append({'id': 'DI7-GEO-R'+str(n), 'kind': 'supreme-caster-center-range', 'offset': point,
            'expectedWithinRange': legal, 'qualification': 'Actual perception and line of effect separately required.'})
    for n, (point, inside) in enumerate([([60,30,0], True), ([60,0,30], True), ([60,25,25], False), ([60,35,0], False), ([65,0,0], False)], 1):
        variants.append({'id': 'DI7-GEO-M'+str(n), 'kind': 'mass-cell-membership', 'origin': [0,0,0], 'facing': [1,0,0],
            'cellCenter': point, 'expectedInside': inside, 'qualification': 'Actual occupied non-origin cell and current clipping separately required; no extra radial cap.'})
    variants.append({'id': 'DI7-GEO-M6', 'kind': 'mass-cell-membership', 'origin': [0,0,0], 'facing': [12,5,0],
        'cellCenter': [65,0,0], 'expectedInside': True, 'expectedAxial': 60, 'expectedPerpendicular': 25,
        'qualification': 'Normalize facing to (12/13,5/13,0); no radial rejection at65.'})
    for n, expected in enumerate([
        'Supreme committed from(0,0,0) to C=(120,0,0); legal displacement to(0,5,0) keeps fixed C at grid distance120. Resolve if perception and line of effect survive.',
        'Same Supreme commitment; displacement to(-5,0,0) makes range125. No information, refund or substitute center.',
        'Supreme fixed C in range but perception or caster-to-center line of effect fails at resolution: no information. Only center-to-portion obstruction clips its own portions.',
        'Mass O at source-cell center; displacement to nonoverlapping cell no longer containing O: no effect, remote old-position cone, translated new-position cone or refund.',
        'Mass caster changes position while O remains legal in actual occupied space, or genuinely returns before resolution: unchanged O/F cone if other requirements survive; no new direction.',
        'Illegal geometry before commitment rejects activation rather than producing a paid post-interruption failure.'
    ], 1): variants.append({'id': 'DI7-GEO-I'+str(n), 'kind': 'resolution-interruption', 'expected': expected})
    assert len(variants) == 19
    supplements_before = deepcopy(expectations['supplementalSourceExpectations'])
    supplements_after = supplements_before + [{'id': 'DI7-GEOMETRY-3D-01', 'authority': info(receipt),
        'evidenceKind': 'Authored source expectations only; execution evidence separate.', 'original49Unchanged': True, 'variants': variants}]
    changes = []
    def change_json(path, original, operations):
        after = deepcopy(original)
        for op in operations:
            obj, key = node(after, op['pointer']); assert obj[key] == op['old']; obj[key] = deepcopy(op['replacement'])
        inverse = deepcopy(after)
        for op in reversed(operations):
            obj, key = node(inverse, op['pointer']); assert obj[key] == op['replacement']; obj[key] = deepcopy(op['old'])
        assert inverse == original and encoded(inverse) == original_bytes[path]
        changes.append((path, encoded(after), operations)); return after
    pub_ops = [{'pointer': '/cards/'+str(i)+'/operationalCandidate/completeProcedure', 'spellIdGuard': sid, 'old': old, 'replacement': new} for sid,i,old,new in changed_procedures]
    pub_ops.append({'pointer': '/sourceDirectionAddenda', 'old': addenda_before, 'replacement': addenda_after})
    public = change_json(public_path, public, pub_ops)
    expectations = change_json(expectations_path, expectations, [{'pointer': '/supplementalSourceExpectations', 'old': supplements_before, 'replacement': supplements_after}])
    internal = change_json(internal_path, internal, [
        *[{**op, 'pointer': '/completePublicEnvelope'+op['pointer']} for op in pub_ops],
        {'pointer': '/publicEnvelopeBinding', 'old': internal['publicEnvelopeBinding'], 'replacement': info(public_path, encoded(public))},
        {'pointer': '/finiteExpectations/supplementalSourceExpectations', 'old': supplements_before, 'replacement': supplements_after}])
    assert internal['completePublicEnvelope'] == public and internal['finiteExpectations'] == expectations
    assert expectations['groups'] == original_groups and len(original_groups) == 16 and sum(len(g['variants']) for g in original_groups) == 49
    manuscript = manuscript_path.read_text(encoding='utf-8'); inverse = manuscript; text_ops = []
    for sid,i,old,new in changed_procedures:
        assert manuscript.count(old) == 1; manuscript = manuscript.replace(old,new,1)
        text_ops.append({'textReplace': True, 'spellIdGuard': sid, 'old': old, 'replacement': new})
    inverse = manuscript
    for op in reversed(text_ops): inverse = inverse.replace(op['replacement'],op['old'],1)
    assert inverse.encode() == original_bytes[manuscript_path]
    changes.append((manuscript_path, manuscript.encode(), text_ops))
    preserved = []
    for path in paths:
        dest = preservation / path.relative_to(G); dest.parent.mkdir(parents=True, exist_ok=True); dest.write_bytes(original_bytes[path])
        assert dest.read_bytes() == original_bytes[path]
        preserved.append({**info(path), 'preservedCopy': dest.relative_to(G).as_posix()})
    (preservation / 'PRESERVATION_MANIFEST.json').write_bytes(encoded(preserved))
    operations = []
    for path,data,ops in changes:
        path.write_bytes(data); assert path.read_bytes() == data
        operations.append({'before': next(x for x in preserved if x['path'] == path.relative_to(G).as_posix()),
            'after': info(path), 'operations': ops, 'exactInverseBytesVerified': True})
    delta.write_bytes(encoded({'id': 'DI7-GEOMETRY-3D-01', 'recordedAtUtc': now, 'authority': info(receipt), 'changes': operations,
        'newRuleAdoptions': 3, 'original49ExpectationsAndFourShieldSupplementUnchanged': True, 'newSupplementalExpectations': 19,
        'allOtherCandidateContentUnchanged': True, 'allCostAccessApprovalSelectionFieldsUnchanged': True,
        'sourceInformationDeleted': 0, 'spellPromotions': 0}))
    print(json.dumps({'received': info(receipt), 'delta': info(delta), 'changedActiveFiles': len(operations), 'newExpectations': 19}))


if __name__ == '__main__': main()
