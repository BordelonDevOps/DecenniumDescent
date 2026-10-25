from pathlib import Path
import copy, hashlib, json, zipfile

G = Path(r'C:\Github\DecenniumDescent')
A = G / 'docs/audit/2026-10-08/full-game'
D = A / 'director-spell-review-128'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def enc(x): return (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode()
def sha(b): return hashlib.sha256(b).hexdigest()
q = read(A / 'spell-review-resume-116/CURRENT_SPELL_QUEUE_128.json')
g = next(x for x in q['groups'] if x['group'] == 'rank7-gate-glyph3')
assert g['currentPhase'] == 'prepared-awaiting-review'
c = read(G / g['candidate']['path'])
orig = G / g['archive']['path']
assert sha(orig.read_bytes()) == g['archive']['sha256']
index = read(G / 'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json')
for sid in g['identities']:
    assert next(e for e in index['entries'] if e['id'] == sid)['authoredStatus'] == 'pending-authored-procedure'
checks = []
with zipfile.ZipFile(orig) as z:
    assert z.testzip() is None and len(z.namelist()) == len(set(z.namelist()))
    for b in c['sourceBindings']:
        v = z.read('sources/' + b['path'])
        assert len(v) == b['bytes'] and sha(v) == b['sha256']
        checks.append({'path': b['path'], 'originalExact': True, 'currentExact': sha((G / b['path']).read_bytes()) == b['sha256']})
extra = [
    ('GG128-ADD01', ['chain-gate'], 'Three portals require three independently qualified sites and one explicit directed graph.', 'Choose the complete three-aperture topology and entry/exit faces. For actual planar travel use original qualified geographic/cosmological evidence; do not infer a remote-site entitlement, plane identity, time conversion or current acceptance from pending Planar6. Include exact local poses, rotations, carried-body sets, finite placement candidates and whole-group arrival. A missing site/profile stays a whole positive-case hold.'),
    ('GG128-ADD02', ['chain-gate'], 'Applied Transport6 is comparison authority, not automatic Chain Gate authorship.', 'Inspect the complete current MysticGate and Circle procedures, proper rotation/aperture fit rules, disjoint object groups, genuine movement/vehicle prerequisites and source-qualified Anchor/Antimagic. Explicitly adopt only the selected relevant clauses. Circle identity/study permissions do not grant ChainGate destinations. Show partial suppression of B preserving only original usable edges, no automatic A-to-C bypass, and one real crossing at the exact closing boundary.'),
    ('GG128-ADD03', ['symbol', 'symbol-of-death'], 'An inscription trigger is a finite local observation, not a hidden fact query.', 'Bind an actual support face, orientation, custody and sensor path. Decide whether carrier motion, newly unhidden face, an existing occupant, a forced mover or an ordinary real entry triggers. A glyph cannot detect unseen HP, allegiance, identity, plane or caster intent without a separately selected explicit source permission. Inscription range does not expand sensing or payload range. No expensive material is invented where the focus alternative is permitted.'),
    ('GG128-ADD04', ['symbol-of-death'], 'Direct death uses actual source-qualified lifecycle and separate event identity.', 'Provide full cases at60 and61 operativeHP with temporaryHP and actual Body8 form endpoints. DeathWard and Null damage routing cannot manufacture immunity to nondamage death. The real acquired, unspent Ritual of Undeath or other would-die replacement resolves once; each later distinct rune reevaluates the then-current body/HP. Do not rescan a survivor within the same rune event or treat zero-only triggers as death replacements.'),
    ('GG128-ADD05', ['symbol', 'symbol-of-death'], 'Current Time5 and accepted Symbol of Stunning are limited comparisons.', 'Preserve paid commitment, concentration/Ready chronology and absolute clocks. If selecting a finite stasis or stopped-time interaction, name the exact current source and real affected glyph anchor/recipient; no inferred general timer freeze. Countered inscription creates no trap, suppression banks no missed trigger and dispel uses its captured source set. Symbol of Stunning is a separate already-applied identity; do not borrow its payload or reopen it.'),
    ('GG128-ADD06', ['symbol', 'symbol-of-death'], 'Every harmful branch and any disarm procedure must be authored in full.', 'If Symbol has a menu, provide complete numbers, save, geometry, limits and native-source cases for every option. For disarming choose actual Action/tool/skill/DC/retry and failure effect, or clearly state the existing available removal route. Glyph Trace reveals only its real supplied information; it supplies no decoder, hidden target knowledge or automatic disarm. Preserve spent charges, unrelated inscriptions, remains, inventory and witnessed knowledge through destruction and source ending.')
]
qs = copy.deepcopy(c['questions'])
for qid, ids, issue, request in extra:
    qs.append({'id': qid, 'spellIds': ids, 'exactSourceOrConflict': issue, 'request': request, 'decisionSelected': False})
specs = {
    'chain-gate': [
        'One actual paid cast establishes exactly3 source-qualified apertures in selected order; actual qualified traveler/body/cargo traverses each permitted directed edge using real movement.',
        'Known illegal versus hidden/late invalid endpoint, actual Anchor/Antimagic where applicable, suppressed middle node and exact closing boundary; no bypass, split body, free recall or refunded casting.'
    ],
    'symbol': [
        'Every selected harmful option with full acquired caster, genuine surface/trigger sensor and initial/entering recipients, actual save/damage/condition results and consumed charge.',
        'Moving/covered carrier and actual physical disarm or qualified removal; suppression, countered creation, same-owner replacement/cap and successive distinct glyph triggers with full custody/clocks.'
    ],
    'symbol-of-death': [
        'One genuine local discharge with operativeHP60 versus61 and real temporaryHP; exact living/active nonliving source-defined terminal lifecycle and no damage-root or Wound fabrication.',
        'Actual acquired unspent would-die replacement, a second distinct rune and newly currentHP/body state, real form endpoint/remains/inventory, exact expiry and no repeated same-event kill.'
    ]
}
cases = [{'id': 'GG128-' + sid.upper() + '-' + chr(65+i), 'spellId': sid, 'requiredEvidence': text, 'status': 'REQUIRED_NEW_CASE_NOT_AUTHORED'} for sid, rows in specs.items() for i, text in enumerate(rows)]
notes = {'id': 'GATE-GLYPH3-INDEPENDENT-CONFERENCE-128', 'status': 'PREPARED_UNSENT_NOT_ACCEPTED', 'identities': g['identities'], 'currentAppliedCounts': {'reviewed':616,'pending':232,'standalone':340,'interfaces':173,'acceptedUnapplied':0}, 'completeOriginalQuestionsUnchanged': copy.deepcopy(c['questions']), 'focusedAdditionalQuestions': qs[len(c['questions']):], 'allQuestions': qs, 'requiredNewCases': cases, 'additionalBranchRequirement': 'At least6main cases plus each materially distinct selected harmful menu, actual form/death replacement, admitted channel/forced-transit and disarm branch.', 'originalFutureCaseRequirementsUnchanged': c['futureCaseRequirements'], 'sourceChecks': checks, 'runtimeExecuted':False, 'sourceProgramsExecuted':False, 'scope':'Current accepted receipts supersede only their exact historical pending labels. All three identities remain pending. No cosmological, runtime, human or release acceptance.'}
(D / 'GATE_GLYPH3_NEXT_CONFERENCE_NOTES_128.json').write_bytes(enc(notes))
files = {}
with zipfile.ZipFile(A / 'DD_VitalityMatter10_Director_Conference_128.zip') as z:
    for n in z.namelist():
        if n.startswith(('accepted-context/', 'accepted/', 'current/')): files[n] = z.read(n)
files['original/' + orig.name] = orig.read_bytes()
files['INDEPENDENT_QUESTIONS_128.json'] = enc(notes)
files['README.md'] = b'Gate/Glyph3 director conference128. All3 identities remain pending. Read complete original source and all21questions; author6main cases plus each materially distinct branch. Retain full source, value operations, exact receipts and content holds. Applied baseline616/232. Transport6 is accepted current scoped comparison; pending Planar6 and Magic7 confer no acceptance. No supplied/historical program may execute. No runtime/human/balance/cosmology/release claim.\n'
manifest = {'id':'GATE-GLYPH3-CONFERENCE-128-MANIFEST', 'files':[{'path':n,'bytes':len(v),'sha256':sha(v)} for n,v in files.items()]}
files['MANIFEST.json'] = enc(manifest)
out = A / 'DD_GateGlyph3_Director_Conference_128.zip'
assert not out.exists()
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for n,v in files.items(): z.writestr(n,v)
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
    for b in manifest['files']:
        v=z.read(b['path']); assert len(v)==b['bytes'] and sha(v)==b['sha256']
receipt={'id':'GATEGLYPH3-DIRECTOR-CONFERENCE-128','status':'PREPARED_NOT_SENT','archive':{'path':str(out),'bytes':out.stat().st_size,'sha256':sha(out.read_bytes())},'members':len(files),'bindings':len(manifest['files']),'questions':len(qs),'requiredMainCases':len(cases),'sourceChecks':len(checks),'canonicalChanges':False,'runtimeExecuted':False}
(D/'GATEGLYPH3_PACKET_128.json').write_bytes(enc(receipt))
print(json.dumps(receipt,indent=2))
