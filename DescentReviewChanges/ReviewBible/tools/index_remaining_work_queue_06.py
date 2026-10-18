"""Reconcile current pending identities with actual reviews, packets and source audits."""
from copy import deepcopy
from datetime import datetime, timezone
from collections import Counter
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded


def read(p):
    return json.loads(p.read_bytes())


def main():
    out = R / 'data/director/spell_review/remaining_work_queue_06.json'
    report = A / 'REMAINING_WORK_QUEUE_06_CHECK.json'
    assert not out.exists() and not report.exists()
    indexp = R / 'data/public/spell_playtests/authored_review_index.json'
    catalogp = R / 'data/public/spell_playtests/catalog.json'
    priorp = R / 'data/director/spell_review/remaining_spell_authoring_map_03.json'
    index, catalog, prior = read(indexp), read(catalogp), read(priorp)
    byindex = {e['id']: e for e in index['entries']}
    bycard = {s['id']: s for s in catalog['spells']}
    byold = {r['id']: r for r in prior['rows']}
    reviewed = {i for i, e in byindex.items() if e['authoredStatus'] == 'reviewed-authored-operational-playtest'}
    pending = set(byindex) - reviewed
    assert len(byindex) == len(bycard) == 848 and len(reviewed) == 480 and len(pending) == 368
    groups, membership, bindings = [], {}, {}

    def bind(p):
        b = info(p)
        bindings[b['path']] = b
        return b

    for p in [indexp, catalogp, priorp]:
        bind(p)
    specifications = [
        ('damage-control25', 'exact-rebound-prepared-unsent', R / 'data/director/spell_proposals/damage_control_25_current_09.json', A / 'DAMAGE_CONTROL_25_EXACT_REBOUND_10_PREPARATION.json', A / 'DD_Damage_Control_25_Exact_Rebound_10.zip', 25),
        ('persistent-damage20', 'exact-rebound-prepared-unsent', R / 'data/director/spell_proposals/persistent_damage_20_current_07.json', A / 'PERSISTENT_DAMAGE_20_EXACT_REBOUND_07_PREPARATION.json', A / 'DD_Persistent_Damage_20_Exact_Rebound_07.zip', 20),
        ('illusion-perception14', 'semantic-conference-prepared-unsent', R / 'data/director/spell_proposals/illusion_perception_14_current_12.json', A / 'ILLUSION_PERCEPTION_14_CONFERENCE_12_PREPARATION.json', A / 'DD_Illusion_Perception_14_Conference_12.zip', 14),
        ('control15', 'semantic-conference-prepared-unsent', R / 'data/director/spell_proposals/control_15_current_12.json', A / 'CONTROL_15_CONFERENCE_12_PREPARATION.json', A / 'DD_Control_15_Conference_12.zip', 15),
        ('memory2', 'systemic-design-conference-prepared-unsent', R / 'data/director/spell_review/memory_2_conference_02.json', A / 'MEMORY_2_CONFERENCE_02_PREPARATION.json', A / 'DD_Memory_2_Conference_02.zip', 2),
        ('creation1', 'systemic-design-conference-prepared-unsent', R / 'data/director/spell_review/creation_conference_02.json', A / 'CREATION_CONFERENCE_02_PREPARATION.json', A / 'DD_Creation_Conference_02.zip', 1),
        ('material-terrain8', 'systemic-design-conference-prepared-unsent', R/'data/director/spell_review/material_terrain_8_conference_02.json', A/'MATERIAL_TERRAIN_8_CONFERENCE_02_PREPARATION.json', A/'DD_Material_Terrain_8_Conference_02.zip', 8),
        ('companion-life10', 'actual-gpt-semantic-review-in-progress', R/'data/director/spell_review/companion_life_10_conference_01.json', A/'COMPANION_LIFE_10_CONFERENCE_01_PREPARATION.json', A/'DD_Companion_Life_10_Conference_01.zip', 10),
        ('body-defense8', 'systemic-design-conference-prepared-unsent', R/'data/director/spell_review/body_defense_8_conference_01.json', A/'BODY_DEFENSE_8_CONFERENCE_01_PREPARATION.json', A/'DD_Body_Defense_8_Conference_01.zip', 8),
    ]
    for group, phase, candidatepath, prep, archive, count in specifications:
        candidate = read(candidatepath)
        if 'spells' in candidate:
            identities = [s.get('id', s.get('spellId')) for s in candidate['spells']]
        elif 'records' in candidate:
            identities = [s['spellId'] for s in candidate['records']]
        else:
            identities = [candidate['completeEarlierRecordUnchanged']['spellId']]
        assert len(identities) == len(set(identities)) == count
        assert set(identities) <= pending and not set(identities) & set(membership)
        record = {'group': group, 'phase': phase, 'identities': identities, 'identityCount': count, 'candidate': bind(candidatepath), 'preparation': bind(prep), 'archive': bind(archive), 'adopted': False}
        if group == 'persistent-damage20':
            record['actualReturnedReview'] = bind(A/'PERSISTENT_DAMAGE_20_CONFERENCE_06_RECEIPT.json')
            record['actualAssistantTurn'] = '0d6f943a-dd04-4129-9af8-cab561c62fc8'
            record['nineCorrectionsReplayed'] = bind(A/'PERSISTENT_DAMAGE_20_CURRENT_07_REPLAY_CHECK.json')
            record['exactReboundSubmitted'] = False
        if group == 'companion-life10':
            record['actualSubmission'] = bind(A/'COMPANION_LIFE_10_CONFERENCE_01_ACTUAL_SUBMISSION.json')
            record['actualUserTurn'] = 'e064c030-16dc-47a0-85d0-e361fdef35b1'
            record['actualGptThread'] = '6ad1acef-455c-83ea-bc33-56e4adaec9c8'
            record['latestObservedStatus'] = 'Visible Stop while actual conference is ongoing; native idle is not final-review evidence.'
            record['newCurrentVectorsSubmitted'] = 0
        groups.append(record)
        membership.update({ident: (group, phase) for ident in identities})
    assert len(membership) == 103
    bind(R/'data/director/spell_review/remaining_work_queue_05.json')
    rows = []
    for ident in sorted(pending):
        original = byold[ident]
        group, phase = membership.get(ident, (None, original['authoringState']))
        rows.append({'id': ident, 'name': bycard[ident]['name'], 'currentIndexEntryUnchanged': deepcopy(byindex[ident]), 'completeCurrentSourceAndAccess': deepcopy(bycard[ident]), 'previousAuthoringMapRowUnchanged': deepcopy(original), 'currentGroup': group, 'currentPhase': phase, 'semanticAcceptanceClaimed': False, 'nextAction': ('Wait for and verify actual final GPT review; preserve before applying corrections.' if phase == 'actual-gpt-semantic-review-in-progress' else 'Send the complete prepared packet to actual GPT when the current review finishes.' if 'prepared-unsent' in phase else 'Prepare source-specific forks and current cases before substantial new authorship.' if phase.startswith('source-audit') else 'Read exact original sources and accepted interfaces, classify actual new decisions and preserve existing history before authoring.')})
    counts = dict(Counter(row['currentPhase'] for row in rows))
    assert sum(counts.values()) == 368 and len({r['id'] for r in rows}) == 368
    assert counts['earlier-complete-proposal-awaiting-current-reconciliation'] == 32
    assert counts['no-complete-procedure-found-in-current-proposal-directory'] == 232
    assert counts['receipt-only-pending'] == 1
    for b in bindings.values():
        assert info(G / b['path']) == b
    result = {'id': 'REMAINING-WORK-QUEUE-06', 'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'developmentDirection': 'video-game-only', 'source': 'Current848-identitycatalogandmembershipindex,witholder03mapretainedperrow;preparedarchivesareboundexactly.', 'ordinarySpellCounts': {'total': 848, 'reviewed': 480, 'pending': 368}, 'pendingDistribution': counts, 'preparedOrActualReviewIdentityCount': 103, 'additionalSourceAuditIdentityCount': 0, 'otherEarlierCompleteProposalCount': 32, 'originalSourceOrReceiptWorkCount': 233, 'groups': groups, 'rows': rows, 'sourceBindings': list(bindings.values()), 'limitations': 'This is an inventory/navigation reconciliation,not a new semantic review. Earlier completeproposalstatuses remain historical; DE4 currentmembership is alreadyreviewed and absentfrompending. A preparedpacket is not acceptance. No percent-complete estimate for the fullgame follows from spellcounts.', 'newRuleAdoptions': 0, 'runtimeTestsExecuted': 0, 'sourceInformationDeleted': 0}
    out.write_bytes(encoded(result))
    report.write_bytes(encoded({'queue': info(out), 'currentIdentities': 848, 'reviewed': 480, 'pending': 368, 'uniquePendingRows': 368, 'groupOverlapCount': 0, 'allBoundSourcesUnchanged': True, 'exactBindingsChecked': len(bindings), 'preparedOrSubmitted': 103, 'sourceAuditOnly': 0, 'otherEarlierComplete': 32, 'originalSourceOrReceiptWork': 233, 'newRuleAdoptions': 0, 'runtimeTestsExecuted': 0}))
    print(json.dumps(read(report)))


if __name__ == '__main__':
    main()
