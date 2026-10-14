"""Preserve ordinary alignment evidence and correct copied-source lookup only."""
from datetime import datetime, timezone
from apply_di7_ap_as_01 import G, R, A, info, encoded, digest


def main():
    path = R/'tools/di7_alignment_transactions.py'
    delta = A/'DI7_ALIGNMENT_COPY_SOURCE_DERIVED_OPERATIONS.json'
    preserved = A/'source-before-di7-alignment-copy-source'/path.relative_to(G)
    assert not delta.exists() and not preserved.exists()
    old = path.read_bytes()
    before = info(path)
    old_text = "            op = self.sources.spell(cast['spellId'], cast['provider'])[1]\n"
    new_text = ("            source_provider = self.casts[cast['copyLineage']['original']]['provider'] if cast.get('route') == 'fate-echo-copy' else cast['provider']\n"
                "            _, op, source_binding, _ = self.sources.spell(cast['spellId'], source_provider)\n"
                "            if source_binding != cast['sourceBinding']:\n"
                "                raise ValueError('Exact generating source binding must survive to resolution')\n")
    text = old.decode('utf-8'); assert text.count(old_text) == 1
    changed = text.replace(old_text, new_text)
    compile(changed, str(path), 'exec')
    assert changed.replace(new_text, old_text).encode('utf-8') == old
    preserved.parent.mkdir(parents=True, exist_ok=True); preserved.write_bytes(old)
    path.write_bytes(changed.encode('utf-8'))
    delta.write_bytes(encoded({'id': 'DI7-alignment-copied-generating-source-lookup', 'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
        'classification': 'Evaluator correction; existing Fate source identity rule unchanged.',
        'changes': [{'before': {**before, 'preservedCopy': preserved.relative_to(G).as_posix()}, 'after': info(path),
            'operation': {'old': old_text, 'replacement': new_text}, 'exactInverseBytesVerified': digest(changed.replace(new_text, old_text).encode('utf-8')) == before['sha256']}],
        'reason': 'A Fate child uses its original generating spell source, while its actual Fate caster supplies ability/PB/class-level stats. Looking up ordinary access through the echoer wrongly rejects Cleric/Shaman copying a Wizard Alignment Suggestion.',
        'ordinarySourceRecordsChanged': False, 'sourceInformationDeleted': 0, 'newRules': 0}))
    print(encoded({'delta': info(delta), 'changed': info(path)}).decode())


if __name__ == '__main__': main()
