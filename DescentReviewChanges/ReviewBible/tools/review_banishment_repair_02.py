"""Audit Repair02 and request source-coherent mandatory ending and closure rules."""
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded, digest


def read(p):
    return json.loads(p.read_bytes())


def at(d, pointer):
    for part in pointer.strip('/').split('/'):
        part = part.replace('~1', '/').replace('~0', '~')
        d = d[int(part)] if isinstance(d, list) else d[part]
    return d


def main():
    out = A / 'banishment-repair-02-return'
    target = A / 'BANISHMENT_REPAIR_02_LOCAL_AUDIT.json'
    request = A / 'BANISHMENT_REPAIR_03_REQUEST.txt'
    assert not target.exists() and not request.exists()
    inputs = read(A / 'banishment-current-review-01-input/CURRENT_REVIEW_INPUT.json')
    model = read(out / 'SPELL_MODEL.json')
    casebook = read(out / 'CASEBOOK.json')
    sources = read(out / 'SOURCE_HASHES.json')
    manifest = read(out / 'EVIDENCE_MANIFEST.json')
    checks = []

    def check(label, ok):
        checks.append({'check': label, 'pass': bool(ok)})

    check('original49source bindings exact', sources['bindings'] == inputs['sourceBindings'])
    for b in sources['bindings']:
        raw = (G / b['path']).read_bytes()
        check('current source: ' + b['path'], len(raw) == b['bytes'] and digest(raw) == b['sha256'])
    for b in manifest['files']:
        raw = (out / b['name']).read_bytes()
        check('output: ' + b['name'], len(raw) == b['bytes'] and digest(raw) == b['sha256'])
    check('ordinary source/access object exact', model['sourceAndAccess'] == inputs['sourceCard'])
    cases = casebook['cases']
    check('thirty original cases and four repair cases', [c['id'] for c in cases] == [f'BAN-C{i:02}' for i in range(1,31)] + [f'BAN-X{i:02}' for i in range(1,5)])
    for original in inputs['originalAuthoredExamples'] + inputs['additionalReviewScenarios']:
        check('historical evidence: ' + original['id'], next(c for c in cases if c['id'] == original['id'])['historicalSourceScenario'] == original)
    check('ten original review IDs', [q['id'] for q in model['questionDispositions']] == [f'BAN-{i:02}' for i in range(1,11)])
    check('five repair dispositions', [q['id'] for q in model['repairDispositions']] == [f'BAN-R02-{i:02}' for i in range(1,6)])
    refs = 0
    sections = []
    for c in cases:
        check(c['id'] + ' nonempty sourceRefs', bool(c['sourceRefs']))
        for ref in c['sourceRefs']:
            refs += 1
            path = out / ref['path'] if ref['path'] == 'SPELL_MODEL.json' else G / ref['path']
            if ref['pointer'].startswith('section:'):
                sections.append({'caseId': c['id'], **ref})
                continue
            try:
                value = at(read(path), ref['pointer'])
                ok = value is not None
            except (KeyError, IndexError, ValueError, FileNotFoundError):
                ok = False
            check(c['id'] + ' JSON reference ' + ref['path'] + ref['pointer'], ok)
    findings = [
        {
            'id': 'BAN-R03-01', 'severity': 'adoption-blocking',
            'location': 'SPELL_MODEL.json /procedure/closure/geometryChangeGate, /primaryReservation, /protectedSilhouette; BODY_EQUIPMENT_PLAYTEST.md Placement and involuntary endings; catalog /spells/735/operational',
            'finding': 'The new berth invariant fails against an existing mandatory anatomy ending. A Medium root creature can already be in a legal Tiny form before Banishment. It enters a narrow place, is banished in that small anatomy, and receives only the small exact-vacated berth. Its prior Polymorph then expires, is dispelled or ends at actual0HP. If no root-sized replacement berth fits, Repair02 says an indivisible involuntary geometry-changing event fails as a whole. The accepted body rule instead says a mandatory ending still occurs when root anatomy does not fit; Polymorph source expiry/0HP ending cannot be vetoed to preserve a Banishment invariant. Released melded gear and corpse/body lifecycle pose the same required preservation issue.',
            'requiredCorrection': 'Never fail, delay or negate an actual death, summon expiry, concentration ending, mandatory reversion, damage event or cargo release just to preserve a reserved shape. Reconcile the exact current body rule. Consider replacing berth reservation with a finite mandatory return to the origin plane followed by the EXISTING same-anchor/squeeze/nearest-adjacent/same-unobstructed-region placement-conflict procedure. The Banishment cell/application can end while a canonical physical placement conflict remains on the origin plane. If used, explicitly define plane, anchor, body/cargo identity, remaining legal interactions and clock state; the conflict is not continued extraplanar imprisonment, body deletion, overlap permission or a hidden future rule. The narrow terminal endpoint-blocker exception still needs an explicit scoped ruling. If retaining berths, prove mandatory reversion and every real ending remain valid and disclose the added terrain-ward power, including forced movement and collapse rather than silently canceling a whole external event.'
        },
        {
            'id': 'BAN-R03-02', 'severity': 'operative-contradiction',
            'location': 'SPELL_MODEL.json /procedure/currentInterfaces/dimensionalAnchor, /procedure/admission/effect, /questionDispositions/8/reason; REGISTER.json /questionDispositions/8/reason',
            'finding': 'Active text still invokes BAN-CLOSE-01. The Dimensional Anchor interface still requires searching for an unblocked return first, while BAN-CLOSE-02 directly uses a reserved berth with a blocker exception. The old and new operating procedures disagree.',
            'requiredCorrection': 'Reconcile every active rule ID and outcome in model, register, chapter, Director and cases to the final chosen closure design. Preserve old wording only in explicitly historical evidence, not as simultaneous current authority.'
        },
        {
            'id': 'BAN-R03-03', 'severity': 'invalid-or-incomplete-example-geometry',
            'location': 'CASEBOOK.json BAN-C24 and BAN-C30; SPELL_MODEL.json /procedure/cell/coordinates, /initialGeometry, /boundaries',
            'finding': 'With a5ft-wide primary centered at local0 and5ft clearance per side, the initial cell is15ft wide (nominal x/y -7.5..+7.5). C24 declares a perceived Water Pet creation space x10..15 before any expansion, outside the opaque boundary. Expansion after successful legal admission cannot itself supply prior target perception/LoE for an otherwise illegal cast. C30 likewise needs an actual initial floor layout and legal movement/space sequence for a Large Steed.',
            'requiredCorrection': 'Give actual initial cell bounds, owner/body positions, legal movement costs and fitting currently perceived in-cell summon footprints before casting. Use an already visible adjacent pet square, and move the owner lawfully if required to fit a Large Steed. Do not use prior expansion to authorize a source whose legal preflight has not yet succeeded.'
        },
        {
            'id': 'BAN-R03-04', 'severity': 'incomplete-concentration-example',
            'location': 'CASEBOOK.json BAN-X04',
            'finding': 'The primary Wizard escapes through its own Faction Portal while a Water Pet is said still to exist, but no different actual owner/concentration arrangement is supplied. If the Wizard created the Pet, Portal concentration ends it before the crossing. Thus this does not yet establish the requested real escape with another body remaining.',
            'requiredCorrection': 'Use an actual nonconcentration companion source or prove a separate legal owner. A supplied concrete candidate is Mage /cards/21 Conjure Elemental Familiar: Mage5 selection, Action4RP, rank3 class spell,10minutes, no printed concentration, common familiar profile. A banished entitled Mage7 can create that familiar, then use its known ordinary Faction Portal with real positive faction standing/knownHQ and actual source prices to escape while the familiar and a genuine loose object remain. Apply the shared exact familiar/source rules rather than inventing an outside visitor or keeping two incompatible concentrations.'
        }
    ]
    result = {
        'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
        'status': 'Further repair required; correct Paladin distinction and ledger fixes retained as candidate improvements, but Banishment not accepted/adopted.',
        'archive': info(A / 'DD_Banishment_Repair_02_Return.zip'),
        'actualBrowserResponse': info(A / 'BANISHMENT_REPAIR_02_RETURN_ACTUAL_DOM.txt'),
        'checks': checks, 'checkCount': len(checks), 'failureCount': sum(not c['pass'] for c in checks),
        'sourceReferenceCount': refs, 'resolvedJsonReferenceCount': refs-len(sections),
        'descriptiveSectionReferences': sections,
        'semanticFindings': findings, 'semanticFindingCount': len(findings),
        'independentSemanticReadScope': 'Complete Player/Director chapters and operative model; selected current case actions and exact named class/spell/body authorities. Pointer resolution is not proof of semantic correctness or runtime execution.',
        'sourceInformationDeleted': 0, 'newRulesAdopted': False, 'runtimeTestsExecuted': 0, 'humanPlaytested': False,
        'countsUnchanged': {'reviewed': 434, 'pending': 414, 'total': 848},
    }
    assert result['failureCount'] == 0
    target.write_bytes(encoded(result))
    body = (R / 'docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md').read_text(encoding='utf8')
    section = body.split('## Placement and involuntary endings\n',1)[1].split('\n## Body weight and conditions',1)[0]
    familiar = read(R / 'data/public/class_playtests/mage.json')['cards'][21]
    text = [
        'Continue ordinary Banishment Repair03 in this same chat. Your Repair02 archive is preserved exactly: DD_Banishment_Repair_02_Return.zip,40,775bytes,SHA256 f38520b8abda2f9ed4699e77d6a273f049c06a8ba3dd185ddec35a20e302d84f. No Banishment rule has been adopted.',
        f'Local structural verification: {len(checks)}checks,0failures; all49frozen sources unchanged; complete original source/access unchanged; all28 historical scenario objects preserved;34case IDs present;98nonempty references, of which77JSON pointers resolve and21are descriptive section references. Those checks do not prove semantic coherence.',
        'Keep your corrected exact Paladin distinction, admissionIntent and corrected cost/clock ledgers. Four issues remain; the first is a direct conflict with an already accepted mandatory-ending rule, not a speculative future plane-erasure case.',
    ]
    for f in findings:
        text += [f['id'] + ' — ' + f['location'], f['finding'], 'Required resolution: ' + f['requiredCorrection']]
    text += [
        'The authoritative BODY_EQUIPMENT_PLAYTEST.md is ALREADY among the49 frozen sources. Here is its exact complete Placement and involuntary endings section for the closure redesign:',
        section,
        'The current catalog /spells/735/operational also expressly ends Polymorph at its deadline, actual0HP, death or Incapacitated and refers mandatory blocked reversion to canonical geometry. Do not relabel that mandatory ending as a voluntary preflight failure. Test a root Medium creature admitted while legitimately Tiny, followed by source expiry and no root-sized berth; preserve all original clocks and actual state.',
        'The Mage card suggested for the real secondary-body escape example is also already in the49-source input. Exact operative card:',
        json.dumps({k:v for k,v in familiar.items() if k!='source'},ensure_ascii=False,indent=2),
        'Please critically evaluate the simpler canonical placement-conflict alternative. Existing physical conflict on the origin plane is different from maintaining the Banishment cell past60seconds. A finite ending need not invent a safe open square, negate death/reversion, freeze a falling body or create a new terrain exclusion. Define the resulting actual state and available lawful resolution using the real body rules; do not merely say Director decides. If you choose another design, justify its exact source preservation and fully resolve the concrete counterexample.',
        'Return DD_Banishment_Repair_03_Return.zip with exactly the same8root files. Preserve original source/access and all28 historicalSourceScenario objects; retain BAN-C01..30 and BAN-X01..04 IDs, revising current adjudications explicitly. Add concrete mandatory-reversion and actual nonconcentration-secondary escape examples if needed. Include dispositions BAN-R03-01..04, update all active closure references consistently, and verify49source/output hashes. No runtime/human/balance/canon/soul/origin/era/whole-game/publication approval. Cleric Banish Unholy stays separate.'
    ]
    request.write_text('\n\n'.join(text)+'\n',encoding='utf8',newline='\n')
    print(json.dumps({'audit': info(target), 'request': info(request), 'structuralChecks': len(checks), 'failures': 0, 'semanticFindings': len(findings)}))


if __name__ == '__main__':
    main()
