"""Exact fractional cone boundaries and actual cross-provider copied alignment."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded, digest
from di7_cast_transactions import DI7Sources
from di7_area_fixtures import make as area_fixture
from di7_alignment_transactions import AlignmentTransactions


def main():
    output = A/'DI7_BOUNDARY_AND_COPY_SOURCE_CHECK.json'
    assert not output.exists()
    sources = DI7Sources(); checks, histories = [], []
    def check(label, value): assert value, label; checks.append(label)
    for provider in ['Wizard', 'Cleric', 'Mirrorsage', 'Shaman']:
        for label, point, inside, blocked in [
                ('60-30-inclusive', [60,30,0], True, False), ('30.1-outside', [60,30.1,0], False, False),
                ('60.1-outside', [60.1,0,0], False, False), ('actual-total-cover', [60,30,0], False, True)]:
            m, request = area_fixture(sources, provider=provider, points=[point])
            if blocked:
                line = m.world['geometry']['portions']['portion-0']['clippingByOrigin']['0,0,0']
                line.update(lineOfEffect=False, totalCover=True, authorityEvent='conditional-real-total-cover')
            m.declare('owner', 'mass-revelation', 'mass', request)
            gate = m.resolve_area_geometry('mass')
            check(provider+'/'+label+'/paid-Action', m.actors['owner']['rp'] == m.actors['owner']['maxRP']-17 and m.actors['owner']['actions'] == 0)
            check(provider+'/'+label+'/exact-membership', bool(gate['readableSpatialPortions']) == inside)
            check(provider+'/'+label+'/geometry-only-qualified', not gate['informationPayloadExecuted'] and not gate['publicInformationDelivered'])
            histories.append({'id': 'D7T-03-01/'+provider+'/'+label, 'final': m.snapshot()})
    for provider in ['Wizard', 'Cleric', 'Mirrorsage', 'Shaman']:
        for invalidated in [False, True]:
            base, _ = area_fixture(sources, provider=provider)
            world = deepcopy(base.world)
            world['entities']['target'] = {'kind':'creature','positionFeet':25,'willing':True,'alliedTo':{},'relatedQuestions':[]}
            world['alignmentActors']['target'] = {'underlying':{'order':'Chaotic','ethics':'Evil'},'immunities':[], 'permanentIdentity':{'id':'target'},'acquisitionSnapshots':[],'usedAllowances':{}}
            for aid in base.actors:
                world['relations'][aid+'>target'] = {'sourceFact':'conditional-perceived-open-local-target','perceived':True,'visible':True,'lineOfEffect':True}
            m = AlignmentTransactions(sources, base.actors, world)
            m.learn('owner', 'fate-echo', m.actors['owner']['classLevel'], 'actual-Fate-acquisition')
            m.learn('counter', 'alignment-suggestion', 1, 'actual-Wizard-original-acquisition')
            for aid, actor in m.actors.items():
                if actor['provider'] == 'Wizard':
                    m.prepare_wizard(aid, list(actor['learned']), aid+'/study', {'actor':aid,'completedAt':0,'sourceEvent':'conditional-completed-own-rest'})
            m.begin_turn('counter', 'conditional-counter-regular-turn')
            m.declare('counter', 'alignment-suggestion', 'original', {'target':'target'})
            m.world['identificationFacts']['direct'] = {'observer':'owner','castId':'original','kind':'conditional-actual-direct-identification'}
            m.observe_cast('owner', 'original', 'direct')
            m.resolve_alignment('original', face=1, modifier=0)
            m.advance(3601); m.begin_turn('owner', 'conditional-owner-regular-turn')
            m.begin_fate('owner', 'echo', 'original', {'target':'target'}); child = m.finish_fate_outer('echo')
            if invalidated:
                m.world['entities']['target']['positionFeet'] = 140
                m.events.append({'kind':'conditional-legal-target-movement','sourceEvent':'actual-before-child-resolution','at':m.now})
            m.resolve_alignment(child['id'], face=1, modifier=0)
            label = provider+'/'+('invalidated' if invalidated else 'legal')
            check(label+'/own-payment-and-original-payment', m.actors['counter']['rp'] == 46 and m.actors['owner']['rp'] == m.actors['owner']['maxRP']-19)
            check(label+'/exact-original-source-own-stats', child['sourceBinding'] == m.casts['original']['sourceBinding'] and child['provider'] == provider and child['dc'] == 8+4+2+(m.actors['owner']['totalLevel']-1)//4)
            check(label+'/no-ordinary-Suggestion-acquisition', 'alignment-suggestion' not in m.actors['owner']['learned'])
            if invalidated:
                check(label+'/no-replacement-no-refund', child['id'] not in m.alignment.effects and m.alignment.effects['original']['state'] == 'live' and m.actors['owner']['concentration'] is None)
            else:
                check(label+'/actual-cross-provider-copy-payload', m.alignment.effects[child['id']]['state'] == 'live' and m.alignment.effects['original']['state'] == 'ended' and m.actors['counter']['concentration'] is None)
            histories.append({'id':'copy-generating-source/'+label, 'final':m.snapshot()})
    delta_path = A/'DI7_ALIGNMENT_COPY_SOURCE_DERIVED_OPERATIONS.json'
    delta = json.loads(delta_path.read_bytes())
    for change in delta['changes']:
        check('source-correction-current-binding', info(G/change['after']['path']) == change['after'])
        check('source-correction-preserved-byte-inverse', digest((G/change['before']['preservedCopy']).read_bytes()) == change['before']['sha256'] and change['exactInverseBytesVerified'])
    report = {'status':'pass','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'checks':len(checks),'historyCount':len(histories),
        'sourceBindings':sources.bindings+[info(p) for p in [R/'tools/validate_di7_boundary_and_copy_source.py',R/'tools/di7_alignment_transactions.py',R/'tools/di7_area_fixtures.py',R/'tools/di7_area_geometry.py',R/'tools/di7_fate_transactions.py',R/'tools/di7_alignment_clock.py',delta_path]],
        'checkLabels':checks,'histories':histories,'failures':[],
        'sourceExpectationCoverage':{'D7T-03-01':[h['id'] for h in histories if h['id'].startswith('D7T-03-01/')]},
        'closedInventoryGap':'D7T-03-01','priorInventory':info(A/'DI7_FINITE_93_EVIDENCE_INVENTORY.json'),
        'remainingInventoryGaps':['D7T-08-02','D7T-10-01'],
        'scope':'Exact paid60/30,30.1,60.1 cone geometry and real total cover; actual Wizard original copied by all four Fate providers with own stats/payment and current target revalidation.',
        'conditionalPremises':['Occupied test-cell centers and clipping are explicitly supplied world geometry, including the source-requested fractional center coordinates; no generic grid/map engine is certified.',
            'Character attainment/body/rest/turn chronology and intervening target movement are conditional upstream premises.',
            'No totem is supplied to these Shaman actors; no vent is inferred. Copied Suggestion is not ordinary repertoire and requires the original Wizard source.'],
        'full49Fulfilled':False,'exactApproved':False,'newRuleAdoptions':0,'sourceInformationDeleted':0,'spellPromotions':0}
    output.write_bytes(encoded(report))
    print(json.dumps({'report':info(output),'checks':len(checks),'histories':len(histories),'closedGap':'D7T-03-01'}))


if __name__ == '__main__': main()
