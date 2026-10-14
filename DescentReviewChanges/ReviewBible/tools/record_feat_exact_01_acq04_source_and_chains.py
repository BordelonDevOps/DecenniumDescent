"""Preserve and record source adoption, paid-chain progress and owner direction."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import sys
from record_feat_exact_01_acq03_fulfillment import read, info, write_new

R = Path(__file__).resolve().parents[1]; G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'


def main():
    now = datetime.now(timezone.utc).isoformat()
    previous_path = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_EXACT_01_COMPOSITE_CASTING.json'
    target = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT327_ACQ04_SOURCE_AND_CHAINS.json'
    delta_path = A / 'FEAT327_ACQ_04_SOURCE_AND_CHAINS_COVERAGE_DELTA.json'
    preservation = A / 'navigation-and-coverage-before-feat327-acq04-source-and-chains'
    assert all(not p.exists() for p in [target, delta_path, preservation])
    tinker_path = A / 'FEAT_EXACT_01_TINKERING_PROGRESSION_CHECK.json'
    chain_path = A / 'FEAT_EXACT_01_REMAINING_OWNED_CHAINS_CHECK.json'
    source_path = A / 'FEAT327_ACQ_04_INDEPENDENT_DESCENDANT_CHECK.json'
    owner_path = A / 'OWNER_CRPG_DIRECTION_VISIBLE_CAPTURE_2026-10-13.json'
    tinker, chains, source, owner = [read(p) for p in [tinker_path, chain_path, source_path, owner_path]]
    operations = read(A / 'FEAT327_ACQ_04_DERIVED_OPERATIONS.json')
    altered = {x['after']['path']: x for x in operations['changes']}
    for report, count in [(tinker, 149), (chains, 141), (source, 161)]:
        assert report['checks'] == count and not report['failures'] and all(x['passed'] for x in report['results'])
        for bound in report.get('sourceBindings', []):
            current = info(G / bound['path'])
            if current != bound:
                change = altered[bound['path']]
                assert {k: change['before'][k] for k in bound} == bound and current == change['after']
                assert info(G / change['before']['preservedCopy'])['sha256'] == bound['sha256']
    assert chains['counts']['cumulativePartialPrerequisiteIdentities'] == 330 and len(chains['remaining']) == 5
    assert len(owner['ownerMessages']) == 2
    owner_ids = []
    for message in owner['ownerMessages']:
        for ancestor in message['ancestorDataAttributes']:
            for key, value in ancestor['attrs']:
                if key == 'data-chatgpt-search-message-ids':
                    owner_ids.append(value)
    assert owner_ids == ['6a5d3234-1622-44e5-9162-c6a4de7fe687', '3a66c8c1-5216-4d1c-b3a8-e5216e18b3d5']
    ledger_path = R / 'data/playtest/game_development_coverage.json'
    before = read(ledger_path); ledger = deepcopy(before)
    changed = {'DD-06', 'DD-14', 'DD-69'}
    scope = ('Tinker Adept has149 passing checks over conditional source-qualified trade progression and actual paid selection. '
        'A further141 checks across21 captured histories cover Dark Binding, Trapcasting and Voltyros Pact with actual paid parents, '
        'fixed Stormcaller route and Voltyros ability choices, finite initial uses and no created bodies/events. '
        'These add4 disjoint partial prerequisite identities to the326 checkpoint:330 covered,5 remaining. '
        'The Animal Handling branch of Companion Training and the CON15 Berserker parent are also checked but their target identities are not counted complete. '
        'Full335 acquisitions, use procedures, exact-candidate approval and software implementation remain open.')
    acq_scope = ('Actual GPT ACQ-04 reply a469c764-37b9-4beb-9a8c-f485a071eb8d retains all four operative procedures and resolves their external-source dispositions. '
        'The new ACQ04-EC1 evidence contract distinguishes conditional fixtures from actual-world credentials. '
        'Five existing files receive only the exact shared append/four reference annotations/reader mirrors; one policy file is added. '
        'All prior bytes are preserved,101 reviewer source checks reproduce locally and161 independent descendant checks pass. '
        'The sixteen behavioral acceptance groups remain outstanding; this source adoption adds zero covered prerequisite identities and is not full feat approval.')
    for row in ledger['aspects']:
        if row['id'] not in changed:
            continue
        row.setdefault('completedScopes', []).extend([scope, acq_scope])
        row.setdefault('validationEvidence', []).extend(p.relative_to(G).as_posix() for p in [tinker_path, chain_path, source_path])
        row.setdefault('reviewEvidence', []).append((A / 'FEAT327_ACQ_04_RECEIVED_DECISION.json').relative_to(G).as_posix())
        row.setdefault('currentEvidenceAddenda', []).append({'id': 'FEAT327-ACQ04-SOURCE-AND-PAID-CHAINS',
            'recordedAtUtc': now, 'partialPrerequisiteIdentities': 330, 'remainingIdentities': 5,
            'sourceApplicationComplete': True, 'acq04BehavioralAcceptanceComplete': False,
            'all335CompleteAcquisitionsValidated': False, 'fullFeatCandidateApproved': False})
        if row['id'] == 'DD-14':
            row.setdefault('historicalOpenIssueSnapshots', []).append({'recordedAtUtc': now,
                'reason': 'Preserve326/9 checkpoint before Tinkering, three paid chains and actual ACQ-04 source adoption.',
                'status': row['status'], 'openIssues': deepcopy(row['openIssues'])})
            row['openIssues'][1] = ('FXC-05 partial prerequisite count is330/335, not330 complete acquisitions. '
                'The latest disjoint additions are Tinker Adept, Dark Binding, Trapcasting and Voltyros Pact. '
                'Remaining identities: ' + ', '.join(x['id'] for x in chains['remaining']) + '. '
                'ACQ-04 source directions are received and applied; execute all16 acceptance groups before finite fulfillment. '
                'Complete Animal Companion paid acquisition/body/bond evidence and Companion Training ownership branch. '
                'Prodigy still needs its ordered skill/tool/language/Expertise selections. All broader selections, resource/use procedures and exact review remain open. '
                'Earlier GPT KEEP applies to its stated evidence scopes; newer local counts are not broad GPT approval.')
    for old, new in zip(before['aspects'], ledger['aspects']):
        assert old['id'] == new['id'] and old.get('closure') == new.get('closure') and old.get('humanEvidence') == new.get('humanEvidence')
        if old['id'] not in changed:
            assert old == new
    directive = {'id': 'owner-crpg-system-specification-2026-10-13-capture',
        'evidence': owner_path.relative_to(G).as_posix(), 'messageIds': owner_ids,
        'currentWork': 'Complete and reconcile every game system as an unambiguous authored specification; manual tabletop bookkeeping is not an acceptance gate.',
        'expeditionInvariants': ['Twelve characters in any rule/alignment-compatible combination, Good through Neutral through Bad.',
            'Up to four human players may perform different concurrent activities such as delving, supply gathering and research.',
            'Host configures permissions and any human/AI distribution, including all twelve AI. Players act independently within those permissions.'],
        'laterWork': 'Detailed control interface, AI and multiplayer design and CRPG software conversion remain later work. No software architecture or engine-version choice is adopted by this record.',
        'deliveryOrder': ['Finish system specifications and actual joint whole-game flow review', 'Authorized GitHub commit/push',
            'Verify remote commit', 'Careful cosmology review and preservation-based repository cleanup in their agreed post-delivery phase', 'CRPG conversion'],
        'preservation': 'Delete historical material only after both file audit and GPT confirm it obsolete; preserve unique code, assets and history.',
        'completedScopes': 'Carry forward reviewed crafting, language, onboarding/teaching and EX58 scopes; reopen only a concrete newly evidenced conflict.'}
    ledger.setdefault('ownerDirectedSequencing', []).append(directive)
    ledger['objective'] = 'Complete every game system as a coherent, source-linked authored specification for the later CRPG, with actual joint review and preserved history'
    ledger['completionPolicy'] += (' Owner CRPG clarification: manual tabletop administerability and manual bookkeeping are not acceptance gates. '
        'Current authored rules must be complete and unambiguous, preserve meaningful player decisions and resolve cross-system conflicts. '
        'Historical runtime/parity/implementation and human-session requirements remain documented as separate later evidence gates; source or finite model checks do not claim software completion or balance.')
    ledger['workingMethod'] += ' Carry forward the owner CRPG and unchanged twelve-character expedition direction captured13October; actual software conversion follows system completion and verified delivery.'
    nav = R / 'tools/build_review_map.py'; nav_text = nav.read_text(encoding='utf-8')
    anchor = '        "FEAT_EXACT_01_COMPOSITE_CASTING_COVERAGE_DELTA.json",'
    assert nav_text.count(anchor) == 1
    nav_text = nav_text.replace(anchor, anchor + '\n        "FEAT327_ACQ_04_SOURCE_AND_CHAINS_COVERAGE_DELTA.json",')
    anchor = '    chain = list(entries.values()) + acq03["changes"] + coverage_deltas'
    assert nav_text.count(anchor) == 1
    nav_text = nav_text.replace(anchor, '    acq04 = read(A / "FEAT327_ACQ_04_DERIVED_OPERATIONS.json")\n    chain = list(entries.values()) + acq03["changes"] + acq04["changes"] + coverage_deltas')
    anchor = '        ("Combined feat prerequisites — scope and remaining work", "FEAT_EXACT_01_COMPOSITE_CASTING_PREREQUISITE_NOTES.md"),'
    links = [
        ('Owner CRPG and expedition direction', owner_path.name),
        ('Tinker Adept — actual trade progression', 'FEAT_EXACT_01_TINKERING_PROGRESSION_NOTES.md'),
        ('Tinker Adept — recorded conditional history', tinker_path.name),
        ('Remaining paid feat chains — scope', 'FEAT_EXACT_01_REMAINING_OWNED_CHAINS_NOTES.md'),
        ('Remaining paid feat chains — source-qualified histories', chain_path.name),
        ('External credentials — actual GPT reply', 'FEAT327_ACQ_04_GPT_RESPONSE.json'),
        ('External credentials — controlling evidence policy', 'FEAT327_ACQ_04_EXTERNAL_CREDENTIAL_POLICY.json'),
        ('External credentials — preservation and source changes', 'FEAT327_ACQ_04_DERIVED_OPERATIONS.json'),
        ('External credentials — independent source check', source_path.name),
        ('External credentials — sixteen acceptance groups to execute', 'feat327-acq04-source/ACQ04_ACCEPTANCE_CASES.json')]
    assert nav_text.count(anchor) == 1
    nav_text = nav_text.replace(anchor, anchor + ''.join('\n        (' + json.dumps(label, ensure_ascii=False) + ', ' + json.dumps(path) + '),' for label, path in links))
    anchor = 'The old numeric/history/Warrior reports retain their original input bindings;'
    assert nav_text.count(anchor) == 1
    nav_text = nav_text.replace(anchor, scope + ' ' + acq_scope + ' Owner direction is now CRPG system specification with twelve characters, parallel activities and host-configured human/AI control; manual tabletop bookkeeping is not a completion gate. Implementation remains later. ' + anchor)
    compile(nav_text, str(nav), 'exec')
    template = R / 'tools/review_map_template.html'; template_text = template.read_text(encoding='utf-8')
    old_sequence = '<div class="sequence"><p><strong>Delivery order:</strong> finish the authored game and joint flow review → push to GitHub → verify the remote commit → carefully review cosmology. Human teaching, balance and campaign playtests remain separate.</p></div>'
    assert template_text.count(old_sequence) == 1
    template_text = template_text.replace(old_sequence,
        '<div class="sequence"><p><strong>Delivery order:</strong> finish the system specification and joint flow review → commit/push to GitHub → verify the remote commit → carefully review cosmology and complete preservation-based cleanup → later CRPG conversion. Software implementation and human balance testing remain separate.</p>'
        '<p><strong>Owner direction:</strong> preserve the twelve-character expedition, alignment compatibility, up to four humans performing parallel activities, and host-configured human/AI permissions. Manual tabletop bookkeeping is not an acceptance gate.</p></div>')
    saved = []
    for path in [ledger_path, nav, template, G / 'REVIEW_MAP.html', A / 'REVIEW_MAP_BUILD.json']:
        bound = info(path); dest = preservation / path.relative_to(G)
        dest.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(path, dest)
        assert dest.read_bytes() == path.read_bytes()
        saved.append({**bound, 'preservedCopy': dest.relative_to(G).as_posix()})
    manifest_path = preservation / 'PRESERVATION_MANIFEST.json'; write_new(manifest_path, saved)
    ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    write_new(delta_path, {'recordedAtUtc': now, 'status': 'verified-scoped-progress-and-owner-direction',
        'before': next(x for x in saved if x['path'] == ledger_path.relative_to(G).as_posix()), 'after': info(ledger_path),
        'aspectsChanged': sorted(changed), 'allOtherAspectsUnchanged': True, 'allClosuresAndHumanEvidenceUnchanged': True,
        'topLevelFieldsChanged': ['objective', 'completionPolicy', 'ownerDirectedSequencing', 'workingMethod'],
        'ownerEvidence': info(owner_path), 'validation': [info(p) for p in [tinker_path, chain_path, source_path]],
        'previousCoverageDelta': info(A / 'FEAT_EXACT_01_COMPOSITE_CASTING_COVERAGE_DELTA.json'),
        'partialPrerequisiteIdentities': 330, 'remainingIdentities': 5, 'fullFeatCandidateApproved': False})
    nav.write_text(nav_text, encoding='utf-8', newline='\n'); template.write_text(template_text, encoding='utf-8', newline='\n')
    completed = subprocess.run([sys.executable, '-X', 'utf8', str(nav)], capture_output=True, text=True, encoding='utf-8')
    if completed.returncode:
        print(completed.stderr); raise SystemExit(completed.returncode)
    navigation = read(A / 'REVIEW_MAP_BUILD.json')
    assert not navigation['missingLinks'] and info(G / 'REVIEW_MAP.html')['sha256'] == navigation['sha256']
    decision = read(A / 'FEAT327_ACQ_04_RECEIVED_DECISION.json')
    state = read(previous_path)
    state.update({'recordedAtUtc': now, 'goalTurnClassification': 'progress',
        'previousGoalTurnClassification': 'no progress: answered owner roadmap question without an authoritative state change',
        'previousCheckpoint': info(previous_path), 'status': scope + ' ' + acq_scope,
        'ownerDirection': directive,
        'activeGptReview': {'id': 'FEAT327-ACQ-04', 'status': 'reply-received-source-applied-sixteen-behavioral-groups-outstanding',
            'replyReceived': True, 'replyMessageId': decision['replyMessageId'], 'chatUrl': decision['chatUrl'],
            'browserId': decision['browserId'], 'tabId': decision['tabId'], 'decision': info(A / 'FEAT327_ACQ_04_RECEIVED_DECISION.json'),
            'pendingResponse': False, 'noUnchangedResubmissionRequired': True, 'wholeExactCandidateApproved': False},
        'featTinkeringProgression': {'report': info(tinker_path), 'checks': 149, 'newPartialIdentities': 1},
        'featRemainingOwnedChains': {'report': info(chain_path), 'checks': 141, 'histories': 21, 'newPartialIdentities': 3},
        'featACQ04SourceApplication': {'operations': info(A / 'FEAT327_ACQ_04_DERIVED_OPERATIONS.json'),
            'independentVerification': info(source_path), 'checks': 161, 'reviewerChecksReproduced': 101,
            'behavioralAcceptanceComplete': False, 'sourceInformationDeleted': False},
        'partialPrerequisiteIdentitiesCurrent': 330, 'remainingCredentialIdentitiesCurrent': chains['remaining'],
        'navigation': {'map': info(G / 'REVIEW_MAP.html'), 'receipt': info(A / 'REVIEW_MAP_BUILD.json'),
            'links': navigation['existingDistinctLinks'], 'missingLinks': []},
        'coverageLedger': info(ledger_path), 'coverageDelta': info(delta_path),
        'navigationBindingPolicy': 'Explicit preserved coverage delta plus measured ACQ-01/02/03/04 source changes; no blanket hash exceptions.'})
    state['safeNextActions'] = [
        'ACQ-04 has a terminal actual GPT reply; do not resend. Source additions and161 independent checks are complete. Execute all16 named acceptance groups using the exact policy and bound conditional fixtures, then record finite fulfillment. Do not infer actual campaign credentials, class rage, legacy aliases or cosmology from tests.',
        'Five partial prerequisite identities remain: ' + ', '.join(x['id'] for x in chains['remaining']) + '. Complete the Animal Companion paid acquisition/body/bond history and Companion Training ownership branch alongside ACQ-04 fulfillment.',
        'Tinker149 and paid-chain141 evidence predate the five-file ACQ-04 addition. Preserve their bindings; use FEAT327_ACQ_04_DERIVED_OPERATIONS.json to resolve exact current descendants. Do not rerun immutable evidence blindly.',
        'Prodigy mandatory ordered skill, profiled tool, eligible language/mode and skill Expertise choices still need completion; the partial lineage count never established these selections.',
        'After prerequisites and mandatory choices, complete all named feat resource/use, command, casting/copy, original660-case and exact-review requirements. Full335 acquisition or gameplay validation is not established by330 partial identities.',
        'Carry forward all owner CRPG/expedition direction and reviewed crafting/language/teaching/EX58 scopes. Complete unambiguous system specifications; software product controls, AI, multiplayer implementation and human balance remain later. Final actual joint flow precedes authorized push, remote verification and careful cosmology review.',
    ] + state['safeNextActions'][1:]
    state.setdefault('preservationManifests', []).extend([info(manifest_path), operations['preservationManifest']])
    write_new(target, state)
    print(json.dumps({'checkpoint': info(target), 'coverage': info(ledger_path),
        'navigationLinks': navigation['existingDistinctLinks'], 'missingLinks': 0,
        'partialIdentities': 330, 'remaining': 5, 'pushed': False, 'cosmologyReviewed': False}, indent=2))


if __name__ == '__main__':
    main()
