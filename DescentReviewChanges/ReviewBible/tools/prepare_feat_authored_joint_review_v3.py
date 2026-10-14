"""Freeze the complete pending-feat proposal conference against current EX58.

Creates a new review packet only. No source/proposal/status overwrite, no dispatch,
no promotion, and no public projection of Director material.
"""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json, zipfile

G = Path(r'C:\Github\DecenniumDescent')
R = G / 'DescentReviewChanges/ReviewBible'
A = G / 'docs/audit/2026-10-08/full-game'
ARCHIVE = A / 'DD_Feats_327_Complete_Proposals_EX58_v3.zip'
RECEIPT = A / 'FEAT_AUTHORED_V3_PACKAGE.json'
REPORT = A / 'FEAT_AUTHORED_V3_PRESERVATION.json'
INTERFACES = A / 'FEAT_EX58_JOINT_INTERFACE_REGISTER.json'
GUIDE = A / 'FEAT_AUTHORED_V3_REVIEW_GUIDE.md'
PROMPT = A / 'CODEX_FEAT_AUTHORED_V3_REVIEW_REQUEST.txt'
README = 'README_FEAT_AUTHORED_V3.md'


def read(p):
    return json.loads(p.read_text('utf-8-sig'))


def info(b):
    return {'bytes': len(b), 'sha256': sha256(b).hexdigest()}


def rel(p):
    return p.relative_to(G).as_posix()


def encoded(d):
    return (json.dumps(d, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def main():
    for p in [ARCHIVE, RECEIPT, REPORT, INTERFACES, GUIDE, PROMPT]:
        assert not p.exists(), 'Preserve existing revision: ' + str(p)
    checks = []

    def check(name, value):
        checks.append({'name': name, 'pass': bool(value)})
        assert value, name

    files, live = {}, {}
    archive_path_remaps = {}

    def add_bytes(name, b):
        check('Safe archive path ' + name,
              not name.startswith(('/', '\\')) and ':' not in name and '..' not in Path(name).parts)
        if name in files:
            check('Overlapping full payload agrees ' + name, files[name] == b)
        files[name] = b

    def add(p):
        name = rel(p)
        b = p.read_bytes()
        add_bytes(name, b)
        live[name] = info(b)

    status_path = R / 'docs/mechanics/expedition/EXPEDITION_REVIEW_STATUS.json'
    status = read(status_path)
    current_eight = status['currentArtifactBindings']
    check('EX58 current authored approval', status['exactCandidateAuthoredApproval'] is True)
    check('EX58 does not enable runtime or selection', not status['runtimeImplemented'] and not status['selectionEnabled'])
    check('Eight exact current EX58 descendants', len(current_eight) == 8)
    for name, expected in current_eight.items():
        check('EX58 current binding ' + name, info((G / name).read_bytes()) == expected)

    exact_report_path = A / 'EX58_EXACT_CANDIDATE_PACKAGE.json'
    exact_manifest = read(exact_report_path)['manifest']
    exact_archive = A / 'DD_EX58_Complete_Exact_Candidate_01.zip'
    check('Original EX58 archive hash', info(exact_archive.read_bytes())['sha256'] ==
          'ab16fff6b7e80d755a6b4d1971c9d7e8fbe20442a1876178073b7f546edd946a')
    exact_changes = []
    archive_only = []
    with zipfile.ZipFile(exact_archive) as z:
        check('EX58 original payload count', len(exact_manifest) == 419)
        for name, expected in exact_manifest.items():
            original = z.read(name)
            check('EX58 frozen payload ' + name, info(original) == expected)
            p = G / name
            if p.is_file():
                current = p.read_bytes()
                if current != original:
                    check('Only approved EX58 descendant differs ' + name,
                          name in current_eight and info(current) == current_eight[name])
                    history = 'HISTORICAL_EX58_SUBMISSION/' + name
                    add_bytes(history, original)
                    exact_changes.append({'file': name, 'original': expected,
                                          'current': info(current), 'originalPreservedAt': history})
                add(p)
            else:
                archive_only.append(name)
                # Keep the submitted root manifest as evidence, but reserve the
                # new root manifest for this complete combined packet.
                destination = 'HISTORICAL_EX58_SUBMISSION/FILE_MANIFEST.json' if name == 'FILE_MANIFEST.json' else name
                if destination != name:
                    archive_path_remaps[name] = destination
                add_bytes(destination, original)
    check('EX58 preservation accounting', len(exact_changes) == 8 and len(archive_only) == 3)

    v2_path = A / 'FEAT_COMPLETE_FILE_HANDOFF_V2_PREPARATION.json'
    v2 = read(v2_path)
    v2_archive = A / v2['bundleFile']
    check('Frozen source-only v2 hash', info(v2_archive.read_bytes())['sha256'] == v2['bundleSha256'])
    v2_changes = []
    with zipfile.ZipFile(v2_archive) as z:
        check('V2 original dependencies', len(v2['currentFileHashes']) == 268)
        for name, h in v2['currentFileHashes'].items():
            original = z.read(name)
            check('V2 frozen payload ' + name, info(original)['sha256'] == h)
            p = G / name
            if p.is_file():
                current = p.read_bytes()
                if current != original:
                    # These revisions were already carried in the completed EX58 source packet.
                    check('V2 intervening revision carried by EX58 ' + name,
                          name in exact_manifest and info(current) == exact_manifest[name])
                    history = 'HISTORICAL_FEAT_SOURCE_V2/' + name
                    add_bytes(history, original)
                    v2_changes.append({'file': name, 'old': info(original),
                                       'current': info(current), 'oldPreservedAt': history,
                                       'currentEvidence': rel(exact_report_path)})
                add(p)
            else:
                add_bytes(name, original)
    check('Six known V2 intervening revisions preserved', len(v2_changes) == 6)

    registry_path = R / 'src/data/feats.js'
    source = json.JSONDecoder().raw_decode(registry_path.read_text('utf-8').split('export const feats = ', 1)[1])[0]
    by = {x['id']: x for x in source}
    operational = read(R / 'data/public/feat_playtests/manifest.json')['operationalIds']
    index_path = R / 'data/director/feat_operating_proposal_index.json'
    index = read(index_path)
    check('335 original identities, eight reviewed', len(source) == len(by) == 335 and len(operational) == 8)
    check('Both full registries identical', registry_path.read_bytes() == (G / 'src/data/feats.js').read_bytes())
    check('Index count 327', len(index['records']) == 327)
    record_paths = sorted({x['proposalData'] for x in index['records']})
    check('Nine complete cohorts', len(record_paths) == 9)
    proposals, proposal_sources, historical_index_refs = {}, {}, []
    history_candidates = list(A.glob('feat-index-*/feat_operating_proposal_index.json'))
    for name in record_paths:
        p = G / name
        d = read(p)
        add(p)
        deps = d.get('sourceFiles', d.get('currentSourceFiles', {}))
        for path, expected in deps.items():
            expected_hash = expected if isinstance(expected, str) else expected['sha256']
            now = (G / path).read_bytes()
            if info(now)['sha256'] != expected_hash:
                check('Only historical navigation reference differs', path == rel(index_path))
                matches = [q for q in history_candidates if info(q.read_bytes())['sha256'] == expected_hash]
                check('Whole old index retained ' + expected_hash, bool(matches))
                add(matches[0])
                historical_index_refs.append({'proposal': name, 'reference': path,
                                              'oldSha256': expected_hash,
                                              'oldPreservedAt': rel(matches[0]),
                                              'currentSha256': info(now)['sha256'],
                                              'meaning': 'Historical navigation only; no rule procedure changed.'})
            add(G / path)
        for x in d['records']:
            fid = x['featId']
            check('Unique pending proposal ' + fid, fid not in proposals and fid not in operational)
            check('Whole original feat object ' + fid, x['sourceObject'] == by[fid])
            check('Full procedure and examples ' + fid, bool(x['procedure'].strip()) and len(x['workedCases']) >= 2)
            proposals[fid] = x
            proposal_sources[fid] = {'path': name, 'recordSelector': {'featId': fid},
                                    'questionId': x.get('questionId')}
    check('Exact pending partition', set(proposals) == set(by) - set(operational))
    check('660 authored examples', sum(len(x['workedCases']) for x in proposals.values()) == 660)
    deferred = sorted(fid for fid, x in proposals.items() if x.get('procedureScope') == 'grant-interface-only-deferred-spell')
    check('Only two declared deferred payloads', deferred == ['astral_projection', 'planar_binding'])
    check('Two historical index references', len(historical_index_refs) == 2)
    for x in index['records']:
        add(G / x['proposalManuscript'])
        add(G / x['sourcePreparation'])
        add(G / x['sourceAudit'])
    add(index_path)
    add(R / 'docs/feats/FEAT_OPERATING_PROPOSAL_INDEX.md')
    add(A / 'FEAT_OPERATING_PROPOSAL_INDEX_CHECK.json')
    for p in (R / 'tools').glob('build_*feat*proposal*.py'):
        add(p)
    for pattern in ['*_OPERATING_PROPOSALS.json', '*_OPERATING_PROPOSAL_CHECK.json', '*_PROPOSAL_ARITHMETIC_REVIEW.json']:
        for p in A.glob(pattern):
            # The six higher-spell cohorts are comparative only, identified below.
            add(p)
    add(R / 'data/director/training_feat_operating_proposal_internal.json')
    add(R / 'docs/feats/TRAINING_FEAT_OPERATING_PROPOSAL.md')

    higher_path = R / 'data/director/higher_spell_operating_proposal_index.json'
    higher = read(higher_path)
    add(higher_path)
    add(R / 'docs/spells/proposals/HIGHER_SPELL_OPERATING_PROPOSAL_INDEX.md')
    for name, expected in higher['inputs'].items():
        check('Current higher-spell comparison input ' + name, info((G / name).read_bytes()) == expected)
        add(G / name)
    for p in (R / 'tools').glob('build_*rank*_operating_proposal.py'):
        add(p)

    authorities = [status_path, exact_report_path, v2_path,
        A / 'EX58_X01_FULFILLMENT.json', A / 'EX58_REVIEW_LABEL_NORMALIZATION.json',
        A / 'GPT_EX58_X01_FULFILLMENT_CONFIRMED.md', A / 'CODEX_EX58_X01_FULFILLMENT_RECEIPT.txt',
        A / 'EX58_COVERAGE_ADDENDUM.json', A / 'TEACHING_TEX_EXACT_FULFILLMENT.json',
        A / 'TEACHING_TEX_ADDENDUM_FULFILLMENT.json', A / 'TC_RECYCLING_01_CONTROLLING_ERRATUM.md',
        A / 'TEX_CONTROLLING_ADDENDUM_2026_10_11.md', Path(__file__)]
    for p in authorities:
        add(p)
    for p in (A / 'ex58-exact-gpt-verdict').iterdir():
        if p.is_file():
            add(p)

    book = R / 'docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md'
    book_text = book.read_text('utf-8')

    def section(anchor):
        marker = f'<a id="{anchor.lower()}"></a>'
        start = book_text.index(marker)
        stop = book_text.find('<a id="', start + len(marker))
        return book_text[start:stop if stop >= 0 else None].strip()

    issues = [
        ('FEX-01', ['endurance', 'survivalist', 'hardy'], ['fl-03', 'fl-04'],
         'Endurance requires a real reconciliation: its generic deprivation timers do not yet define an exception to canonical daily shortfall Strain and scheduled Rest Debt. Supply an explicit finite clock and combined food/water/sleep example; retain existing debt, no free provisions, no extra work Watch or rest rewards. Survivalist should reduce the personal 2-lb/8-pint quantities to 1-lb/4-pint without reducing oil or other logistics. Do not equate environmental Strain, serum Strain, Exhaustion and Dissonance by name.'),
        ('FEX-02', ['forager', 'wilderness_chef', 'naturalist', 'scavenger'], ['fl-04', 'fl-06'],
         'Forager proposes 480 active minutes and a finite guaranteed yield replacing only the ordinary yield roll. Seven standard person-days are 14 lb edible food and 56 pints potable water, not seven whole Supply baskets. Confirm the source guarantee, scarcity/depletion, containers, unrelated food/water availability, ordinary hazard gates, and actual work allocation. Cooking and scavenging cannot multiply that stock or reset its age.'),
        ('FEX-03', ['appraise', 'merchant_s_guile', 'negotiator'], ['fl-19', 'fl-20', 'fl-21', 'fl-25', 'so-01', 'so-02', 'so-06'],
         'Resolve ten-minute feat appraisal versus the thirty-minute Haven appraisal operation, and ten-minute bargaining versus the thirty-minute disposition operation. Recommend treating the feat task as only its exact subtask/exception, with provenance, claims and real transfer work retained. Decide the source-powerful property-identification promise against full Identify and hidden-source protections. Distinguish reference value, sale offer, real settlement and lawful assay/remint costs; predeclare attainable concessions and do not double the same discount.'),
        ('FEX-04', ['cavalry', 'mounted_combatant', 'pathfinder', 'wilderness_walker'], ['tr-01', 'tr-02', 'tr-03', 'tr-04', 'tr-05', 'tr-06', 'tr-13'],
         'Replace future-verdict placeholders by exact current mounting, control, custody, capacities, footprint, action ownership and route procedures. Resolve Cavalry +10 actual mount Speed through burden/terrain and strategic pace using the real mode/profile rather than inventing a mode or second movement budget. Carriage is not rider self-movement, Momentum or free dismount distance. Pathfinder changes only coordinated travel terrain/normal tracking; Wilderness Walker does not confer its personal benefit on the mount.'),
        ('FEX-05', ['animal_companion', 'companion_training', 'leadership', 'beast_whisperer'], ['fl-02', 'tr-02', 'tr-03', 'tr-10'],
         'Compare full proposed companion templates/commands with current class companions and actual mounts. A physical animal cannot gain two independent turns by overlapping companion/mount labels. Resolve whether an eligible bonded body can be ridden and which single phase/control contract applies. Leadership supplies no thirteenth member, free employee or combat body; noncharacter animals and hired independent characters use their actual roster categories.'),
        ('FEX-06', ['tinker_adept', 'combat_engineering', 'siege_savant', 'forge'], ['fl-03', 'fl-18', 'tr-11', 'tr-14'],
         'Decide Tinker Adept\'s explicitly NEW at-most-30-active-minute repair exception inside a beneficial Short Rest; no generic concurrent work permission. Use actual repair cost, target eligibility, current HP, service/fuel counters and duration. An eight-hour or six-hour repair cannot become a short-rest repair. Resolve manufactured barricade/kill-zone and siege source claims without duplicate crafting output/quality/XP or unsupported free object targeting.'),
        ('FEX-07', ['quick_recovery', 'field_surgeon', 'wilderness_chef', 'arcaneResonance'], ['fl-03', 'fl-24'],
         'Apply one real beneficial-rest epoch to refresh/recipient/paid-cost receipts, with at most two beneficial Short Rests between beneficial Long Rests and one beneficial Long Rest per 24 elapsed hours. Debt-clearing safe rest alone gives no second reward. Initial feat uses cannot refill unrelated resources; zero-HP/critical/capacity and blocked-offer rules remain. Inspect all 327 feats for the same invariant, not only these examples.'),
        ('FEX-08', ['craftsman', 'quick_learner', 'diligent_researcher', 'skill_expert', 'skilled'], ['fl-03'],
         'Resolve actual credential/acquisition choices with reviewed character creation and TEX training. Work-time reductions and the proposed strongest-factor families cannot reduce fixed calendar requirements, create a third work Watch or permit simultaneous incompatible lead/helper jobs. Supplies, assistant minutes and completed time remain physical; no generic XP or proficiency from mere item ownership.'),
        ('FEX-09', ['leadership', 'gossip', 'courtly_manners', 'charismatic', 'fast_talker', 'commanding_presence'], ['so-01', 'so-02', 'so-03', 'so-07', 'so-08', 'so-09', 'rp-a01', 'rp-a06'],
         'Fit each feat to a concrete predeclared uncertain social outcome and real channel/time, preserving ordinary agency and exact magical exceptions. Standing is the reviewed -3..+3 event record, with signed per-scene change capped +/-2; persuasion does not grant another reputation award, automatic consent or a loyalty compulsion. Alias/background initialization never resets earned history.'),
        ('FEX-10', ['cartographer', 'dungeon_cartographer', 'master_tracker', 'tracker', 'keen_mind'], ['fl-03', 'fl-10', 'tr-13'],
         'Keep actual observation, route and map evidence distinct from powerful proposed exceptional senses. Decide the explicit new water/air trail sense and source absolute never-lost language; no teleport bridge, unknown geography or cosmology truth follows. Mapping/tracking concurrency changes only its named activity, never every Watch job.'),
        ('FEX-11', [], [],
         'Resolve cross-cohort stacking explicitly. Skill/Crafting/Combat/General drafts propose additive distinct flat feat bonuses, while Extended Magic retains current strongest eligible same-stat bonuses. Define precise families/scopes and precedence for feats versus class, spell, item, cover, resistance, advantage, critical chance, cost reductions and percentages. Preserve eight already reviewed full feats and maximum-HP component contracts. Return numerical mixed-source examples.'),
        ('FEX-12', [], [],
         'Resolve common acquisition, permanent skill-modifier prerequisites, missing ancestry credentials, initial uses, aliases, repeatability and later suppression across all nine cohorts. Preserve every current description/effect/legacy disagreement and full Warrior mutation counterpart. One earned feat choice must not grant duplicate mutation/feat benefits or a second class engine.'),
        ('FEX-13', ['greater_spell_focus', 'spell_sniper', 'magicInitiate', 'familiar_bond', 'feyTouched'], [],
         'Review the explicitly NEW Spell Focus supplement outside 335 identities, feat-only Eldritch Blast outside 848 ordinary spells, finite named curricula, chosen school/rank and feat-casting route. Named feat grants give no RP pool, class rank progression or ordinary access. Current reviewed spell cards govern their payloads; higher-spell proposals remain unadopted comparisons. Validate all resource examples against actual class level, maximum pool and acquisition.'),
        ('FEX-14', ['astral_projection', 'planar_binding'], [],
         'These are the only two grant-interface-only deferred entries. Preserve full source and finite grant proposals, but do not author or approve cosmology payloads before verified GitHub delivery. Other feats with plane/soul/heritage language need bounded mechanical identity receipts without cosmology interpretation. Identify exact affected clauses rather than deferring unrelated whole cohorts.'),
        ('FEX-15', [], [],
         'Review all 660 authored examples and each full proposed procedure, supplement, animal/gadget/maneuver/curriculum table and actual class/spell/recipe counterpart. Structural/arithmetic checks are not runtime or human balance testing. Return an individual disposition for every one of 327 source IDs, every original question, all shared conventions and the separate new supplements; preserve exact sources and label every NEW completion. Any required changes must state full finite replacement text and affected examples, not merely request generic further review.'),
    ]
    interface_records = []
    for issue_id, ids, anchors, question in issues:
        check(issue_id + ' all exact feat identities', set(ids) <= set(proposals))
        interface_records.append({'id': issue_id, 'status': 'OPEN joint authoring decision',
            'questionAndLocalRecommendation': question,
            'featProposals': [{'featId': fid, **proposal_sources[fid],
                               'completePreservedProposalRecord': proposals[fid]} for fid in ids],
            'currentExpeditionSections': [{'file': rel(book), 'anchor': anchor,
                                           'fullSection': section(anchor)} for anchor in anchors]})
    register = {'createdAtUtc': datetime.now(timezone.utc).isoformat(),
        'status': 'New conference interface register; no proposal or reviewed rule changed.',
        'reviewBaseline': status, 'issues': interface_records,
        'allPendingProposalSources': proposal_sources,
        'sourceFeats': 335, 'reviewedFullFeats': 8, 'pendingFullFeats': 327,
        'completeLocalDraftsBeforeCurrentInterfaceReview': 325, 'deferredGrantInterfaces': deferred,
        'authoredExamples': 660, 'currentIntegratedFeatApproval': False,
        'sourceInformationDeleted': 0, 'runtimeImplemented': False, 'cosmologyReviewed': False}
    INTERFACES.write_bytes(encoded(register))
    add(INTERFACES)

    guide = '''# Full feat conference after the reviewed expedition candidate

This is the first dedicated joint review of all 327 pending feats **with their full locally authored procedures**. The source-only v1/v2 packets remain history. There are 335 original identities, eight unchanged reviewed full feats, 325 complete local procedure drafts and two deferred grant-interface drafts, with 660 authored examples across nine cohorts. “Complete draft” does not mean integrated, adopted or balanced.

Start with `FEAT_EX58_JOINT_INTERFACE_REGISTER.json`, then `DescentReviewChanges/ReviewBible/docs/feats/FEAT_OPERATING_PROPOSAL_INDEX.md`. Its nine cohort manuscripts and full internal JSON records preserve every original object, source question, procedure and example. The six training entries are already among the 31 exploration entries, not six more feats. Read all shared conventions and the embedded full counterpart/supplement tables, not just the first record in each cohort.

The interface register identifies 15 specific review matters. In particular Endurance's deprivation-clock draft needs reconciliation with the now-reviewed daily shortfall and Rest Debt procedures. Old statements that the expedition verdict is pending are historical; current EX58 status and the complete current Player/Director books control. The proposed ten-minute appraisal, Cavalry Speed bonus and Tinker Adept repair-during-rest exception need express resolution against these complete current rules. No proposal has been silently rewritten to look approved.

Use actual sources and current contracts for prerequisites, stacking, resource capacity/cadence, action ownership, damage/healing, component exceptions, class access, recipes, institutions, real work, cargo, supplies and prices. The Skill/Combat/etc. additive-feat proposal versus Extended Magic's strongest-bonus rule is an explicit cross-cohort issue. Preserve eight reviewed feat identities and reviewed maximum-HP components without inferring whole-feat approval for other entries.

The new Spell Focus feat and feat-only Eldritch Blast are separately identified supplements outside the 335 feat and 848 ordinary spell totals. Astral Projection and Planar Binding have deferred spell payloads. Literal cosmology sources are retained without interpretation; careful cosmology review remains after verified GitHub delivery. All 71 proposed higher spells and their 142 cases are comparative, unadopted context, not an additional ordinary-spell approval request through this feat conference.

Return one coherent source/proposal authoring verdict with a machine-readable 327-ID disposition register, individual original-question coverage, all shared-rule and new-supplement decisions, and exact replacement text/cases for any amendments. Distinguish retained-as-written, amended, rejected with a usable replacement, and bounded genuine deferrals. A later exact assembled candidate can be checked against that finite verdict; avoid serial generic preliminary conferences or marking unread material accepted. If the entire packet cannot be inspected in one response, accurately retain the inspected/pending identity register and continue from the same attached source.

The package preserves all 419 frozen EX58 payloads (current approved descendants occupy their real paths; eight originals have additional historical paths; the submitted root manifest is preserved at HISTORICAL_EX58_SUBMISSION/FILE_MANIFEST.json), all 268 old v2 dependency bytes (six changed versions have additional historical paths), complete proposed feat source inputs, original books, all 17 class catalogs/guides and current spell/recipe/teaching rules. Two old proposal references to earlier navigation indexes are preserved as complete files. The older embedded manifests and unsent/status strings remain historical. Only the new root FILE_MANIFEST.json describes this package; FEAT_AUTHORED_V3_PRESERVATION.json records the refresh.

This is a private Director-inclusive review archive. It is not a public player bundle. No source deletion, runtime implementation, human playtest/balance approval, final whole-game approval or GitHub push has occurred through packaging. Final joint whole-game flow agreement still precedes the already-authorized GitHub push; the verified remote commit precedes cosmology review.
'''
    GUIDE.write_text(guide, encoding='utf-8', newline='\n')
    add(GUIDE)
    prompt = '''EX58 is fulfilled as confirmed. Please now undertake the dedicated, complete pending-feat joint conference using the attached DD_Feats_327_Complete_Proposals_EX58_v3.zip. This is a new full-procedure packet, not the older source-only v2.

Read README_FEAT_AUTHORED_V3.md and docs/audit/2026-10-08/full-game/FEAT_AUTHORED_V3_REVIEW_GUIDE.md, verify the root manifest, then inspect all nine full cohort manuscripts/data plus complete originals, questions and governing counterparts. There are 335 original feats: eight reviewed unchanged, 327 pending (325 complete local drafts, two deferred spell-grant outlines), 660 authored examples. The six training entries are already included in exploration. New Spell Focus and feat-only Eldritch Blast remain separate proposals outside the original catalogs.

Resolve every original question and procedure, all shared conventions, and all 15 FEX interface issues against the included current reviewed EX58 books, class rules, ordinary spell cards, Core/combat/condition/healing/body/equipment/ancestry/recipe/teaching contracts. Endurance's generic deprivation timing specifically needs an exact bridge to canonical daily shortages and Rest Debt. Also resolve additive-versus-strongest feat bonuses, appraisal/settlement time, real mounting and Cavalry Speed, companion phase ownership, finite foraging, rest repair, acquisition/legacy credentials and actual resource-capacity examples. Full source and legacy alternatives are retained; label NEW decisions explicitly. The 71 higher-spell drafts are comparisons only, still unadopted.

Please produce one complete source/proposal-authoring verdict and downloadable evidence package: individual dispositions for all327 exact IDs and all original questions; shared convention/supplement dispositions; full finite correction/replacement text and corrected examples wherever needed; and a precise finite acceptance contract for the subsequent assembled exact candidate. Do not treat unread records, check counts or stale draft labels as approvals. Preserve the two deferred cosmology-dependent payloads without interpreting cosmology. No runtime/human balance/whole-game approval is being requested by this packet. No source deletion or push. Existing reviewed scopes remain carried forward, and final joint whole-game flow -> authorized push -> verified remote commit -> careful cosmology review remains the delivery order.
'''
    PROMPT.write_text(prompt, encoding='utf-8', newline='\n')
    add(PROMPT)
    add_bytes(README, ('# DD feat authored review v3\n\n' + guide.split('\n', 1)[1]).encode('utf-8'))
    for name, expected in live.items():
        check('Full current input unchanged during packaging ' + name, info((G / name).read_bytes()) == expected)
    report = {'createdAtUtc': datetime.now(timezone.utc).isoformat(),
        'status': 'Prepared; awaiting actual browser dispatch and GPT review.',
        'originalSourceFeats': 335, 'reviewedFullFeatsUnchanged': 8, 'pendingIdentities': 327,
        'completeLocalDraftsBeforeCurrentInterfaceReview': 325, 'deferredGrantInterfaces': deferred,
        'authoredExamples': 660, 'cohorts': 9, 'jointInterfaceQuestions': 15,
        'exactSourcePayloadsPreserved': 419, 'exactChangedReviewedDescendants': exact_changes,
        'exactArchiveOnlyOriginals': archive_only,
        'historicalArchivePathRemaps': archive_path_remaps,
        'v2OriginalDependencyBytesPreserved': 268, 'v2CurrentChanges': v2_changes,
        'historicalIndexReferences': historical_index_refs,
        'higherSpellComparisonCounts': higher['counts'],
        'currentInputBindings': live, 'checks': checks, 'checkCount': len(checks), 'failures': 0,
        'newRuleAdoptions': 0, 'sourceInformationDeleted': 0, 'runtimeImplemented': False,
        'humanBalanceApproved': False, 'wholeGameFlowApproved': False, 'pushed': False,
        'cosmologyReviewed': False, 'sent': False}
    REPORT.write_bytes(encoded(report))
    add(REPORT)
    manifest = {name: info(b) for name, b in sorted(files.items())}
    assert 'FILE_MANIFEST.json' not in manifest, 'Root manifest name is reserved'
    with zipfile.ZipFile(ARCHIVE, 'x', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for name, b in sorted(files.items()):
            z.writestr(name, b)
        z.writestr('FILE_MANIFEST.json', encoded(manifest))
    with zipfile.ZipFile(ARCHIVE) as z:
        assert len(z.namelist()) == len(set(z.namelist())) == len(manifest) + 1
        assert z.testzip() is None
        assert json.loads(z.read('FILE_MANIFEST.json')) == manifest
        for name, expected in manifest.items():
            assert info(z.read(name)) == expected, name
    receipt = {'createdAtUtc': datetime.now(timezone.utc).isoformat(),
        'status': 'Complete full-proposal packet prepared and ZIP roundtrip verified; UNSENT.',
        'archive': rel(ARCHIVE), **info(ARCHIVE.read_bytes()), 'payloadFiles': len(manifest),
        'uncompressedPayloadBytes': sum(x['bytes'] for x in manifest.values()),
        'checksBeforeArchive': report['checkCount'], 'zipRoundtripPayloadChecks': len(manifest),
        'failures': 0, 'preservationReport': rel(REPORT), 'reviewGuide': rel(GUIDE),
        'interfaceRegister': rel(INTERFACES), 'prompt': rel(PROMPT),
        'manifest': manifest, 'sent': False, 'sourceInformationDeleted': 0,
        'newRuleAdoptions': 0, 'runtimeImplemented': False, 'cosmologyReviewed': False}
    RECEIPT.write_bytes(encoded(receipt))
    print(json.dumps({k: v for k, v in receipt.items() if k != 'manifest'}, indent=2))


if __name__ == '__main__':
    main()
