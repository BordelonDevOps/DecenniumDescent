"""Preserve initial Vision evidence and tighten actual communicated-content scope."""
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded


def main():
    module = R / 'tools/di7_vision_transactions.py'
    prior_runner = R / 'tools/validate_di7_vision_transactions.py'
    runner = R / 'tools/validate_di7_vision_transactions_v2.py'
    delta = A / 'DI7_VISION_COMMUNICATION_DERIVED_OPERATIONS.json'
    preservation = A / 'source-before-di7-vision-communication'
    assert all(not p.exists() for p in [runner, delta, preservation])
    original = module.read_bytes(); text = original.decode('utf-8')
    old = """        if not source or not channel or channel.get('speaker') != speaker or channel.get('listener') != listener or channel.get('at') != self.now or not channel.get('actuallyReceivedUnderstood'):
            raise ValueError('Actual contemporaneous received/understood channel required')
        if channel.get('used'): raise ValueError('Communication event already delivered')
        channel['used'] = True
        self.memories.setdefault(listener, []).append({'learnedFrom': speaker, 'channelEvent': channel_event,
            'deliveredAt': self.now, 'answer': deepcopy(source['answer'])})
        return deepcopy(source['answer'])
"""
    new = """        if not source or not channel or not channel.get('sourceFact') or channel.get('speaker') != speaker or channel.get('listener') != listener or channel.get('at') != self.now or not channel.get('actuallyReceivedUnderstood'):
            raise ValueError('Actual contemporaneous source-qualified received/understood channel required')
        if channel.get('used'): raise ValueError('Communication event already delivered')
        delivered = channel.get('deliveredText')
        if not isinstance(delivered, str) or not delivered.strip() or delivered not in source['answer']['text']:
            raise ValueError('This bounded adapter requires the actual received literal excerpt of the remembered answer')
        # A paraphrase/lie can exist under its own communication adjudication;
        # this finite adapter neither authenticates it nor copies omitted facts,
        # step lists or the private answer metadata into the listener's knowledge.
        report = {'text': delivered}
        channel['used'] = True
        self.memories.setdefault(listener, []).append({'learnedFrom': speaker, 'channelEvent': channel_event,
            'deliveredAt': self.now, 'answer': report})
        return deepcopy(report)
"""
    assert text.count(old) == 1; updated = text.replace(old, new, 1)
    assert updated.replace(new, old, 1).encode() == original
    run = prior_runner.read_text(encoding='utf-8')
    swaps = [
        ("output = A / 'DI7_VISION_TRANSACTIONS_CHECK.json'", "output = A / 'DI7_VISION_TRANSACTIONS_V2_CHECK.json'"),
        ("'di7_vision_transactions.py', 'validate_di7_vision_transactions.py',", "'di7_vision_transactions.py', 'validate_di7_vision_transactions.py', 'validate_di7_vision_transactions_v2.py',"),
        ("m.learn('donor', 'fate-coin', 1, 'donor-actual-coin'); m.learn('donor', 'counterspell', 5, 'donor-actual-counter')", "m.learn('donor', 'fate-coin', 1, 'donor-actual-coin'); m.learn('donor', 'counterspell', 5, 'donor-actual-counter')\n        m.learn('donor', 'vision-quest', 13, 'donor-actual-selected-vision')"),
        ("'sourceFact': 'conditional-actual-audible-understood-spoken-message-after-trance'", "'sourceFact': 'conditional-actual-audible-understood-spoken-message-after-trance', 'deliveredText': 'Request an appointment with the keeper.'"),
        ("first.public_memory('donor')[0]['answer'] == answer(first)", "first.public_memory('donor')[0]['answer'] == {'text': 'Request an appointment with the keeper.'}"),
        ("'actual communication event.'", "'actual communicated literal excerpt.'")]
    # The final wording swap is optional because the existing scope is one long
    # sentence. All executable/data replacements below have an exact guard.
    for old_part, new_part in swaps[:-1]:
        assert run.count(old_part) == 1, old_part; run = run.replace(old_part, new_part, 1)
    marker = "    extra = [R / 'tools' / name for name in"
    assert run.count(marker) == 1
    additional = """    # Same hypothetical world, distinct actual caster IDs and paid cast histories.
    m = make(); m.advance(3660); owner_answer = deepcopy(answer(m))
    m.begin_turn('donor', 'donor/real-Vision-turn')
    m.declare('donor', 'vision-quest', 'donor-vision', {'target': 'target', 'question': alias}); m.resolve_vision('donor-vision'); m.advance(3720)
    check('same-world-distinct-paid-casters-consistent', m.public_memory('donor')[0]['answer'] == owner_answer and m.actors['owner']['rp'] == 31 and m.actors['donor']['rp'] == 31)
    record('same-world-distinct-caster-paid-equivalent-query', m)
    m = make(); m.advance(3660); original_answer = deepcopy(answer(m)); m.begin_turn('owner', 'owner/real-repeat-turn')
    m.declare('owner', 'vision-quest', 'repeat-vision', {'target': 'target', 'question': alias}); m.resolve_vision('repeat-vision'); m.advance(3720)
    check('same-caster-repeat-paid-with-real-Refrain', len(m.public_memory('owner')) == 2 and m.public_memory('owner')[1]['answer'] == original_answer and m.actors['owner']['rp'] == 14 and m.actors['owner']['refrain'] == 1 and m.actors['owner']['dissonance'] == 3)
    record('same-caster-second-paid-query', m)
    m = make(); m.world['communicationEvents']['attempt'] = {'speaker': 'owner', 'listener': 'donor', 'at': 3600, 'actuallyReceivedUnderstood': True, 'sourceFact': 'conditional-spoken-attempt', 'deliveredText': 'Request an appointment with the keeper.'}
    reject('cannot-communicate-during-maintained-trance', m, lambda: m.communicate('owner', 'donor', 'vision', 'attempt'))
    m.advance(3660)
    for label, patch in [('missing-source', {'sourceFact': ''}), ('missing-actual-content', {'deliveredText': None}), ('unreceived', {'actuallyReceivedUnderstood': False}), ('unverified-paraphrase', {'deliveredText': 'The keeper has already consented to entry.'})]:
        m.world['communicationEvents']['invalid'] = {'speaker': 'owner', 'listener': 'donor', 'at': 3660, 'actuallyReceivedUnderstood': True,
            'sourceFact': 'conditional-actual-message', 'deliveredText': 'Request an appointment with the keeper.', **patch}
        reject('channel-' + label, m, lambda: m.communicate('owner', 'donor', 'vision', 'invalid'))
    check('no-source-or-content-no-listener-memory', not m.public_memory('donor'))
    record('communication-preserves-private-content-boundary', m)

"""
    run = run.replace(marker, additional + marker, 1)
    compile(updated, str(module), 'exec'); compile(run, str(runner), 'exec')
    dest = preservation / module.relative_to(G); dest.parent.mkdir(parents=True, exist_ok=True); dest.write_bytes(original)
    before = {**info(module), 'preservedCopy': dest.relative_to(G).as_posix()}
    (preservation / 'PRESERVATION_MANIFEST.json').write_bytes(encoded([before]))
    module.write_text(updated, encoding='utf-8', newline='\n'); runner.write_text(run, encoding='utf-8', newline='\n')
    delta.write_bytes(encoded({'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'changes': [{'before': before, 'after': info(module),
        'operations': [{'old': old, 'replacement': new, 'textReplace': True}], 'exactInverseBytesVerified': True}],
        'priorReportPreserved': info(A / 'DI7_VISION_TRANSACTIONS_CHECK.json'), 'newRunner': info(runner),
        'newRuleAdoptions': 0, 'scope': 'Implement existing actual-channel/only-communicated-content boundary; no new game rule or source approval.'}))
    print(json.dumps({'delta': info(delta), 'newRunner': info(runner)}))


if __name__ == '__main__': main()
