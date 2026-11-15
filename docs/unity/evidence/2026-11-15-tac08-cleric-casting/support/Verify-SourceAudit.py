"""Verify the initial TAC08 source audit only; this does not approve a contract or qualify gameplay."""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess

PACKET = Path(__file__).resolve().parents[1]
ROOT = PACKET.parents[3]

def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def sha(data):
    return hashlib.sha256(data).hexdigest()

def canonical(value):
    return sha(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8'))

def require(value, message):
    if not value:
        raise ValueError(message)

def main():
    bindings = load(PACKET / 'SOURCE_BINDINGS.json')
    selected = load(PACKET / 'SPELL_CANDIDATES.json')
    source_bytes = {}
    require(len(bindings['sources']) == 52, 'Initial source inventory changed')
    for row in bindings['sources']:
        ref = row['revision'] + ':' + row['path']
        data = subprocess.check_output(['git', 'show', ref], cwd=ROOT)
        blob = subprocess.check_output(['git', 'rev-parse', ref], cwd=ROOT, text=True).strip()
        require(blob == row['gitBlob'] and len(data) == row['bytes'] and sha(data) == row['sha256'], 'Pinned source differs: ' + ref)
        working = (ROOT / row['path']).read_bytes()
        require(len(working) == row['workingBytes'] and sha(working) == row['workingSha256'], 'Inspected checkout differs: ' + row['path'])
        comparison = 'EXACT' if data == working else 'CRLF_ONLY'
        require(comparison == row['workingTreeComparison']
                and data.replace(b'\r\n', b'\n') == working.replace(b'\r\n', b'\n'), 'Source content differs beyond recorded line endings')
        source_bytes[row['path']] = data
    catalog_bytes = source_bytes[selected['catalogPath']]
    require(sha(catalog_bytes) == selected['catalogSha256'], 'Selected catalog binding differs')
    catalog = json.loads(catalog_bytes.decode('utf-8-sig'))
    authored = json.loads(source_bytes['DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'].decode('utf-8-sig'))
    entries = {row['id']: row for row in authored['entries']}
    ids = {'arcane-ward', 'guidance', 'spare-the-dying', 'sanctuary', 'purify-food-and-drink', 'detect-magic'}
    require(len(selected['candidates']) == 6 and {x['id'] for x in selected['candidates']} == ids, 'Candidate identity inventory differs')
    for row in selected['candidates']:
        card = catalog['spells'][int(row['wholeCardPointer'].split('/')[-1])]
        require(card['id'] == row['id'] and canonical(card) == row['wholeCardSha256']
                and canonical(card['operational']) == row['procedureSha256']
                and card['operational'] == row['operationalEvidence']
                and card['classAccess']['Cleric'] == row['clericAccess'], 'Selected source procedure changed: ' + row['id'])
        require(canonical(entries[row['id']]) == row['authoredReviewEntrySha256']
                and entries[row['id']]['authoredStatus'] == 'reviewed-authored-operational-playtest', 'Authored review binding differs')
        require(row['castingStatusAtBaseline'] == 'UNSUPPORTED', 'Audit promoted runtime authority')
    repertoire = source_bytes['engine/com.decennium.foundation/Runtime/Core/SpellRepertoireRecords.cs']
    conditions = source_bytes['engine/com.decennium.foundation/Laboratory/Model/ConditionCombatPolicy.cs']
    require(b'public bool CastingSupported => false;' in repertoire
            and b'OrdinarySpellcastingUnsupported' in repertoire, 'Initial unsupported-casting baseline differs')
    require(b'This explicitly selected fixture admits no concentration.' in conditions, 'Concentration audit baseline differs')
    require(not subprocess.check_output(['git', 'diff', bindings['baseline'], '--', 'engine'], cwd=ROOT), 'Engine changed during source-only audit')
    result = {
        'status': 'PASS_SOURCE_BINDINGS_ONLY',
        'atUtc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'baseline': bindings['baseline'],
        'engineSource': bindings['engineSource'],
        'precedingAcceptance': bindings['precedingAcceptance'],
        'sourceFiles': len(bindings['sources']),
        'selectedProcedures': len(selected['candidates']),
        'recordedCrLfOnlyCheckoutDifferences': [x['path'] for x in bindings['sources'] if x['workingTreeComparison'] == 'CRLF_ONLY'],
        'contractStatus': 'INCOMPLETE_NOT_SUBMITTED',
        'runtimeChanges': False,
        'notExecuted': ['compilation', 'runtime tests', 'connected casting', 'Unity'],
        'sourceBindingsSha256': sha((PACKET / 'SOURCE_BINDINGS.json').read_bytes()),
        'spellCandidatesSha256': sha((PACKET / 'SPELL_CANDIDATES.json').read_bytes()),
        'verifierSha256': sha(Path(__file__).read_bytes()),
        'wholeEngineCompletion': 'NOT COMPLETE'
    }
    (PACKET / 'SOURCE_AUDIT.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print('PASS SOURCE BINDINGS ONLY: 52 pinned files, six complete source procedures and unchanged accepted engine; contract incomplete, no runtime qualification.')

if __name__ == '__main__':
    main()
