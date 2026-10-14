"""Record two source-derived fixes without overwriting historical model evidence."""
from register_feat_reference_progress import register


CONFIG = {
    'id': 'FLORA-ACQUISITION-CORRECTION',
    'previousCheckpoint': 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_GADGET_USE.json',
    'checkpoint': 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_FEAT_FLORA_ACQUISITION.json',
    'delta': 'FEAT_EXACT_01_FLORA_ACQUISITION_COVERAGE_DELTA.json',
    'previousDelta': 'FEAT_EXACT_01_GADGET_USE_COVERAGE_DELTA.json',
    'preservationDirectory': 'navigation-and-coverage-before-feat-flora-acquisition',
    'report': 'FEAT_EXACT_01_FLORA_ACQUISITION_CHECK.json',
    'notes': 'FEAT_EXACT_01_FLORA_ACQUISITION_NOTES.md',
    'observation': 'FEAT_EXACT_01_FLORA_GPT_STATUS.json',
    'checks': 165, 'histories': 31, 'historyKey': 'histories',
    'expectedCounts': {'castingAbilities': 3, 'attainedLevelCasesPerAbility': 5, 'twoProviderChoiceHistories': 12},
    'navigationAnchor': '        ("Four heritage gadgets — source and physical-scope limits", "FEAT_EXACT_01_GADGET_USE_NOTES.md"),',
    'navigationLinks': [
        ('Conjure Flora — mandatory provider and current-level capacity evidence', 'FEAT_EXACT_01_FLORA_ACQUISITION_CHECK.json'),
        ('Conjure Flora — earlier model omission and correction scope', 'FEAT_EXACT_01_FLORA_ACQUISITION_NOTES.md')],
    'stateKey': 'featFloraAcquisitionCorrection',
    'previousClassification': 'progress: four-gadget construction/use evidence registered',
    'scope': ('Conjure Flora now has 165 passing acquisition/current-stat checks across 31 histories. '
        'The existing SUP07 rule requires a fixed actual casting route at acquisition; the earlier RemainingOwnedChains initialization omitted that field. '
        'A new FloraAcquisition override records the exact paid provider and uses current attained total level for plant capacity, including a level-8 opportunity spent at level10 or later. '
        'All three mental abilities, five attained levels, twelve choices between two separately paid providers, real later ASI changes, unavailable/spent opportunities and Nature/casting prerequisites are exercised. '
        'The initial grant has one use, zero plants and no pending second creation; it grants no spell or casting resource. '
        'Earlier reports/models remain preserved and are explicitly insufficient for complete Flora acquisition. No source rule changed. '
        'Actual plant creation, additional-creation entitlement, rest, command/trap/body interactions and final GPT review remain open; the all335 audit is still visibly running.'),
    'openIssue': ('Use FloraAcquisition for new Conjure Flora histories. The earlier RemainingOwnedChains report omitted SUP07 mandatory casting-route selection and used opportunity level for capacity; '
        'retain its limited ownership/predicate evidence but do not treat its Flora initialization as complete. Carry the correction and all 165-check evidence into the actual GPT audit follow-up. '
        'Full seedling/Trapcasting/Verdant Bond use and all335 acquisition closure remain separate.'),
    'ruleScope': 'No source rule changed; model now follows existing SUP07 route selection and current total-level capacity.',
    'nextAction': ('Carry the Conjure Flora correction into the next actual GPT exchange after its running acquisition audit finishes. '
        'Use the new FloraAcquisition override for all future Flora histories; preserve prior RemainingOwnedChains/report bytes and their explicit incompleteness. '
        'The 165 checks/31 histories cover mandatory actual provider selection and current total-level capacity, not real plant Actions, creation entitlements, rest, commands, traps or body conservation.')}


if __name__ == '__main__': register(CONFIG, __file__)
