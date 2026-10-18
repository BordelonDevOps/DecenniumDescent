"""Preserve two systemic memory proposals and prepare explicit design forks.

This does not choose a new memory rule or promote the historical proposals.
"""
from copy import deepcopy
from datetime import datetime, timezone
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded
from prepare_ac5_current_interfaces_01 import at


def read(path):
    return json.loads(path.read_bytes())


def main():
    out = R / 'data/director/spell_review/memory_2_conference_01.json'
    checkpath = A / 'MEMORY_2_CONFERENCE_CHECK_01.json'
    assert not out.exists() and not checkpath.exists()
    auditpath = R / 'data/director/spell_review/control_memory_17_source_convergence_01.json'
    audit = read(auditpath)
    ids = ['woven-threads', 'haze-of-forgetting']
    records = [deepcopy(row) for row in audit['records'] if row['spellId'] in ids]
    history = [deepcopy(row) for row in audit['all34HistoricalScenarioTexts'] if row['spellId'] in ids]
    catalogpath = R / 'data/public/spell_playtests/catalog.json'
    catalog = read(catalogpath)
    indexpath = R / 'data/public/spell_playtests/authored_review_index.json'
    index = read(indexpath)
    regpath = R / 'data/director/spell_review/accepted_interface_registry_04.json'
    registry = read(regpath)
    checks, sources, counterparts = [], {}, []

    def ck(name, value):
        checks.append({'check': name, 'passed': bool(value)})
        assert value, name

    def bind(path):
        binding = info(path)
        sources[binding['path']] = binding
        return binding

    for path in [auditpath, catalogpath, indexpath, regpath,
                 R / 'data/director/spell_review/ordinary_spell_inventory_03.json',
                 R / 'data/public/class_playtests/wizard.json',
                 R / 'docs/mechanics/CHARACTER_FOUNDATION_TABLES.md',
                 R / 'docs/mechanics/CHARACTER_CREATION_PLAYTEST.md',
                 R / 'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md',
                 R / 'docs/mechanics/VIDEO_GAME_ONLY_DIRECTIVE.md']:
        bind(path)
    for row in records:
        ref = row['sourceReference']
        path = G / ref['path']
        bind(path)
        ck('Exact historical proposal ' + row['spellId'], at(read(path), ref['pointer']) == row['completeEarlierRecordUnchanged'])
        card = next(s for s in catalog['spells'] if s['id'] == row['spellId'])
        ck('Complete source/access preserved ' + row['spellId'], card == row['completeCurrentCatalogSourceAndAccess'])
        ck('Still pending ' + row['spellId'], next(e for e in index['entries'] if e['id'] == row['spellId'])['authoredStatus'] == 'pending-authored-procedure')
        for kind in ['catalog', 'core']:
            ck('Underlying source ' + row['spellId'] + ' ' + kind, bind(R / card['source'][kind + 'Path'])['sha256'] == card['source'][kind + 'Sha256'])
    for ident in ['disrupt-memory', 'minor-illusion', 'antimagic-field-lesser', 'greater-dispel']:
        matches = [e for e in index['entries'] if e['id'] == ident]
        if not matches and ident == 'antimagic-field-lesser':
            matches = [e for e in index['entries'] if e['name'] == 'Antimagic Field (Lesser)']
        ck('Actual accepted counterpart ' + ident, len(matches) == 1 and matches[0]['authoredStatus'] == 'reviewed-authored-operational-playtest')
        entry = matches[0]
        path = (indexpath.parent / entry['procedureFile']).resolve()
        whole = read(path)
        pointer = entry.get('wholeCardPointer', entry['procedurePointer'])
        counterparts.append({'spellId': entry['id'], 'source': bind(path), 'wholeCardPointer': pointer, 'completeCurrentCard': deepcopy(at(whole, pointer)), 'completeSharedRules': deepcopy(whole.get('sharedRules', {})), 'completeIndexEntry': deepcopy(entry)})
    interfaces = []
    for i in [0, 1, 3, 4, 7, 8, 11, 12, 36, 39, 40]:
        entry = registry['entries'][i]
        source = entry['currentAuthoritativeSource']
        b = bind(G / source['path'])
        ck('Exact current authority ' + entry['name'], b['sha256'] == source['sha256'] and b['bytes'] == source['bytes'])
        interfaces.append({'registryPointer': f'/entries/{i}', 'completeEntryUnchanged': deepcopy(entry), 'scopeLimit': 'Inherit only the exact existing scope. No new memory recovery, mental immunity, Fate presentation or dispellable record is inferred.'})
    shared = [deepcopy(s) for s in audit['completeOriginalSharedProposals'] if s['source']['path'] in {row['sourceReference']['path'] for row in records}]
    questions = []

    def question(ident, spells, promise, inherited, gap, a, b, recommendation):
        questions.append({'id': ident, 'spells': spells, 'classification': 'OPEN DESIGN QUESTION', 'risk': 'C', 'exactSourcePromise': promise, 'acceptedInterface': inherited, 'gap': gap, 'optionA': a, 'optionB': b, 'recommendedForActualConference': recommendation, 'scope': 'Only these two named sources and their expressly agreed recovery relationship. No global memory engine or cosmology adoption.', 'status': 'UNSENT; neither option is adopted'})

    question('MEM2-Q01', ids,
             'Woven: Alter a creature\'s recent memory (last 1 minute, WIS save resists). Haze: All targets in 30 ft forget last 1 minute (INT save resists). Both Core durations are Instantaneous.',
             'Disrupt Memory already distinguishes lasting firsthand loss from ongoing suppression and from real events. Ordinary dispel and antimagic act on actual eligible effects at their stated operation time.',
             'The historical two-spell proposals select instantaneous persistent recollection changes, but neither has received actual current concurrence. The word alteration alone does not establish a dispellable continuing application.',
             'Confirm the existing proposed instantaneous change. Preserve original event provenance and edits as history; later ordinary suppression/dispel does not reverse a completed change.',
             'Author a continuing magical-memory record that can be suppressed or dispelled, explicitly resolving source duration conflict and what suppression reveals/restores.',
             'A, as a local source interpretation consistent with Instantaneous. Confirm exact admission behavior in existing antimagic and no post-resolution eligible dispel record.')
    question('MEM2-Q02', ['woven-threads'],
             'Alter one creature\'s recent memory of the last minute; WIS resists; Action, 60 feet, V/S/F.',
             'Actual access, costs, perception, line of effect, saving throws and information protections are inherited. Disrupt Memory supplies no replacement narrative or readout.',
             'Erase/Replace modes, a 60-word narrative and the meaning of known ideas are earlier unadopted authorship. A fabricated remembered fact can affect belief without becoming a mechanical proficiency or true information.',
             'Confirm a selected real elapsed interval within the last 60 seconds, Erase or a coherent first-person sensory replacement of at most 60 ordinary words. Unknown actual memory is never read; familiar concepts may be combined into false events.',
             'Restrict Woven to deletion or editing only details already accurately known to the caster; replacement of unknown details fails without a diagnostic.',
             'A with an explicit distinction between new false episodic content and an actual skill, repertoire, formula grant or fact detector. Preserve the original 40-word example and no retroactive consent.')
    question('MEM2-Q03', ids,
             'Both sources select experiences in the genuinely preceding 60 elapsed seconds, not an arbitrarily dated recollection.',
             'Current Disrupt Memory uses actual resolution-relative time and cannot recursively reach older memories. Actual class knowledge and world-state history are distinct from episodic recall.',
             'Does an actually experienced but currently inaccessible episode remain eligible for a later Woven edit? Can thinking about an old event create a newly editable representation without rewriting the old event?',
             'Eligibility uses actual experienced event identity/time even when another edit masks recall. A current thought can itself be a recent experience, but altering it cannot rewrite its older referenced event or bypass another named source.',
             'Only currently accessible firsthand episodes qualify for Woven replacement; an independently erased episode cannot be targeted until restored.',
             'A preserves source-event provenance and supports overlap without reading the hidden original. Explicitly settle the distinction between an occurrence and a later recollection of it.')
    question('MEM2-Q04', ids,
             'Neither original spell prints a mundane memory-recovery procedure. Woven draft proposes ten minutes plus WIS/Insight against its original DC; Haze proposes a shared Haze/Woven highest-DC procedure.',
             'Core fixed-DC tasks use four degrees and natural shifts. Disrupt Memory allows learning new facts afterward, not ordinary restoration of its erased firsthand memory.',
             'The ten-minute evidence recovery is a substantive new source-family rule. Confirm its availability and time cost before it is written as operative authority.',
             'Approve the existing proposed evidence-based ten-minute WIS/Insight task for only these two sources; Success/Critical Success restores the selected actually experienced portion, with no bonus fact reward.',
             'Do not grant a mundane restoration task; only an independently reviewed effect expressly capable of restoring this memory can restore firsthand recall.',
             'A as an explicit local recovery permission with evidence and portion boundaries decided in Q05/Q06; no extension to Disrupt Memory.')
    question('MEM2-Q05', ids,
             'Earlier drafts require specific credible independent evidence and materially new evidence or method for a retry; wording refers to an episode or recovered portion without a fixed maximum scope.',
             'Task natural shifts and real elapsed time are already accepted. No current interface decides what evidence semantically proves a memory alteration.',
             'A deterministic game needs a bounded selected portion and a reproducible evidence predicate. One contradiction must not silently recover unrelated lifetime history or reveal information never experienced.',
             'For a local recovery attempt, select one real continuous interval no longer than 60 elapsed seconds. Record the concrete independently obtained evidence and affected event IDs; restore only the agreed selected experienced portion. Require a materially new evidence/method record before another failed attempt.',
             'Use an authored episode of variable duration; its source record defines the portion recoverable from specified evidence, including any larger permitted interval. No arbitrary 60-second recovery cap.',
             'A for a narrow finite task, unless actual narrative sources require B. GPT should specify whether credible evidence must address each restored event or whether one valid contradiction permits the whole selected interval; that consequence is not silently resolved here.')
    question('MEM2-Q06', ids,
             'Haze draft proposes highest original DC across current Haze/Woven alterations covering the episode and restoration of the true underlying original, not an older forged layer.',
             'Each actual source owner, original DC and event identity can be preserved without granting a new effect. Disrupt Memory retains its independent lost-firsthand-memory rule.',
             'Define operative versus merely masked edits, partial overlap, lower-DC recasts and what remains after partial recovery. Woven\'s separate original-DC wording conflicts with the proposed shared extension unless explicitly harmonized.',
             'Use the highest original DC among still-unrecovered Haze/Woven edits intersecting the selected portion, including an earlier edit hidden beneath a later one. On success clear only their intersection with the selected portion; retain all history and outside portions. Do not remove any independent Disrupt Memory loss.',
             'Recover layers independently against each layer\'s original DC; ordinary success removes one nominated layer and may expose the earlier forged layer instead of the genuine original.',
             'A, with complete harmonized text for both spells and exact interval endpoints; no rebase of a retained high DC by a weaker recast.')
    question('MEM2-Q07', ['haze-of-forgetting'],
             'All targets in 30 ft forget the last minute; Core range 30 feet, Action, V/S/F, INT resistance.',
             'An actual indiscriminate area can include unperceived recipients without revealing them; ordinary center-to-recipient line of effect and real body geometry apply.',
             'The earlier proposal chose a self-centered 30-foot-radius sphere including caster and allies. Exact source-center anchoring and snapshot ordering require explicit deterministic text, not a selective target list.',
             'Confirm a 30-foot-radius 3D sphere fixed to an expressly identified actual source point at resolution, with caster included and no individual perception requirement. GPT must state the point convention and any source-body exclusion needed for line of effect.',
             'Measure the 30-foot reach from the caster\'s actual body volume as a dilation, preserving all qualifying creatures including self; this yields a different area for large bodies.',
             'A, stating the actual point and inheriting relevant accepted volume-intersection rules. The reference case deliberately keeps every witness strictly inside under either convention; it does not pretend to settle boundary behavior.')
    question('MEM2-Q08', ids,
             'These spells alter memory; neither source prints compelled action, Charmed, concentration ending, skill loss or retroactive event reversal.',
             'Actual component defenses retain scope; Disrupt Memory has an express concentration-ending clause; ordinary control guards apply only to real qualifying hard-control components.',
             'Confirm that new memory authorship preserves actual skills, legitimately acquired repertoire, resource and Action ledgers, while a newly heard password may become inaccessible through erased episodic recall. Define no new player agency override.',
             'Confirm the historical distinctions: actual state and grants persist, no concentration ending or hard-control claim arises solely from memory change, independent older knowledge persists, and future decisions are not compelled.',
             'Author an explicit additional temporary incapacity, concentration loss or knowledge-grant removal with its own source conflict, guard and restoration rules.',
             'A. Do not add mechanical effects simply because forgetting would be inconvenient or narratively powerful.')

    for h in history:
        ck('Historical scenario exact ' + h['id'], at(read(G / h['sourceReference']['path']), h['sourceReference']['pointer']) == h['exactOriginalText'])
    narrative = 'At noon I met the courier beside the fountain. We discussed the weather then parted. I signed nothing, promised nothing, received nothing, learned nothing, and saw nobody enter the courtyard before I quietly walked back toward the old eastern gate.'
    ck('Original 40-word replacement obligation', len(narrative.split()) == 40)

    def actor(ident, level, intel, rp):
        row = next(r for r in records if r['spellId'] == ident)
        access = row['completeCurrentCatalogSourceAndAccess']['classAccess']['Wizard']
        pb = 4 if level <= 12 else 5
        ck('Actual access ' + ident + str(level), level >= access['minimumClassLevel'])
        return {'class': 'Wizard', 'firstClass': True, 'level': level, 'schoolSpecialization': 'Abjuration', 'actualPreparedMatrix': ident, 'actualSchool': access['school'], 'INT': intel, 'CON': 14, 'DEX': 14, 'PB': pb, 'spellDC': 8 + pb + (intel - 10) // 2, 'maximumHP': 8 + (level - 1) * 6, 'generatingRank': access['rank'], 'RPBefore': rp, 'quotedBaseAndFinalCost': access['baseRpCost'], 'RPAfter': rp - access['baseRpCost'], 'DissonanceBefore': 0, 'DissonanceAfter': 0, 'RefrainExtra': 0, 'cadence': 'First use of this actual prepared matrix; no optional class modifier activated.', 'actionAndComponents': 'One available ordinary Action, actual usable voice/hand/focus and V/S/F.'}

    def case(ident, spell, payload):
        old = next(h for h in history if h['id'] == ident)
        return {'id': ident, 'spellId': spell, 'originalTextUnchanged': old['exactOriginalText'], 'originalSourceReference': deepcopy(old['sourceReference']), 'status': 'CONDITIONAL design-conference trace, not an operative new rule or executed runtime test. New memory outcomes require actual GPT disposition.', **payload}

    target = {'class': 'Wizard', 'level': 1, 'firstClass': True, 'INT': 14, 'WIS': 14, 'CON': 14, 'PB': 2, 'maximumAndCurrentHP': 8, 'temporaryHP': 0, 'Wounds': 0, 'INTSaveModifier': 4, 'WISSaveModifier': 4, 'InsightModifier': 4, 'training': 'Actual Wizard first-class INT/WIS saves, chosen Insight and Arcana starting skills; +2 ability and +2 PB once. No applicable memory/mental protection.', 'agency': 'No inferred obedience, attitude change or hard-control admission.'}
    vectors = [case('DI5-04-A', 'woven-threads', {
        'sourceActor': actor('woven-threads', 9, 18, 32), 'recipient': deepcopy(target),
        'geometry': {'casterCenter': [0, 0, 1], 'targetCenter': [20, 0, 1], 'bothBodyHalfExtents': [1, 1, 1], 'actualPerceptionAndUnobstructedLine': True},
        'timeline': {'castResolves': 0, 'realEligibleWindow': [-60, 0], 'selectedMeetingInterval': [-30, -10], 'initialWISFace': 7, 'initialWISTotal': 11},
        'replacementNarrative': narrative,
        'actualEpisodeBeforeEdit': 'Recipient personally attended the meeting, signed a real paper and made a genuinely completed payment. These are explicit prior-event fixture facts, not new resource-generation or acquisition rules.',
        'conditionalResult': 'If Q01/Q02 are approved, failed WIS11 versus16 changes accessible recollection of that selected meeting. The 40-word false narrative is known authored content, not extracted from the target. The actual signed paper, transferred money, other witnesses, class knowledge, spells, injuries and consent history remain unchanged. RP32 becomes22; D0 remains0. No memory-readout, automatic success announcement, concentration loss or hard claim.',
        'originalObligation': 'Preserves the signed-paper, payment, formula and actual-consent distinctions in the original scenario.'}),
        case('DI5-04-B', 'woven-threads', {
            'recipient': deepcopy(target), 'earlierForger': actor('woven-threads', 13, 20, 48), 'laterEditor': actor('woven-threads', 9, 18, 32),
            'geometry': 'Each real source casts from center[0,0,1] to recipient[20,0,1], body halfextents[1,1,1], perceived with unobstructed line.',
            'timeline': {'actualEpisode': [-30, -10], 'earlierEditResolution': -5, 'earlierWindow': [-65, -5], 'earlierSaveFace': 5, 'earlierSaveTotal': 9, 'earlierDC': 18, 'laterEditResolution': 0, 'laterWindow': [-60, 0], 'laterSaveFace': 7, 'laterSaveTotal': 11, 'laterDC': 16, 'credibleEvidenceEncountered': 300, 'uninterruptedExamination': [300, 900], 'InsightFace': 14, 'InsightModifier': 4, 'InsightTotal': 18},
            'conditionalResult': 'Under Q04/Q06 optionA, preserved independent signed paper and witness evidence justify examining the actual selected20second meeting. Ten uninterrupted minutes and Insight18 meet the retained highestDC18. Restore the actually experienced meeting, not the earlier DC18 forgery; clear only those two selected-portion Woven edits and preserve both history records. If only the original Woven-alone DC rule is approved, GPT must state that alternate calculation explicitly rather than silently import Haze recovery.',
            'oldEventBranch': 'A later thought about an event yesterday does not move that event into the current60second window. The present thought may have its own event identity only if Q03 permits that distinction; no mechanical truth about yesterday is overwritten.'}),
        case('EN6-02-A', 'haze-of-forgetting', {
            'sourceActor': actor('haze-of-forgetting', 11, 18, 40),
            'geometry': {'declaredCasePoint': [0, 0, 1], 'casterBodyCenter': [0, 0, 1], 'witnessBodyCenters': [[10, 0, 1], [0, 20, 1], [0, 0, 21]], 'allHalfExtents': [1, 1, 1], 'allCenterToBodyLinesUnobstructed': True, 'boundaryStatus': 'All bodies are strictly within30ft under either Q07 point/body-distance option; this case does not choose that unresolved rule.'},
            'resolutionTime': 120, 'actualWindow': [60, 120],
            'recipients': [
                {'id': 'caster', 'INTSaveModifier': 8, 'd20': 5, 'total': 13, 'saveSucceeds': False, 'actualExperiencedPortion': [60, 120]},
                {'id': 'witnessA', 'profile': deepcopy(target), 'd20': 7, 'total': 11, 'saveSucceeds': False, 'actualExperiencedPortion': [90, 120], 'absenceOfExperience': 'Ordinary natural sleep with no actual experience during[60,90); no magical sleep source or waking ability is asserted.'},
                {'id': 'witnessB', 'profile': deepcopy(target), 'd20': 17, 'total': 21, 'saveSucceeds': True, 'actualExperiencedPortion': [60, 120]},
                {'id': 'witnessC', 'profile': 'Synthetic ordinary living creature,INT10,untrainedINTsave+0,actual episodic capacity; no protection or condition.', 'd20': 4, 'total': 4, 'saveSucceeds': False, 'actualExperiencedPortion': [60, 120]},
            ],
            'conditionalResult': 'Under Q01/Q07, caster and all three witnesses save against16. Caster,A,C lose only actual experience in the specified window; B retains it. There is no replacement story, visual fog, continuing area or entrant effect. RP40 becomes27; the caster forgetting the expenditure does not refund it. Original spilled ink, Wounds and written receipt remain real. No roster of failed or hidden recipients is disclosed.',
            'sourceQualifiedConcentrationBranch': 'A completed prior Minor Illusion is an available actual counterpart; its existing concentration would not end solely from Haze. No prior such cast is required for the four-recipient case.'}),
        case('EN6-02-B', 'haze-of-forgetting', {
            'recipient': deepcopy(target), 'hazeCaster': actor('haze-of-forgetting', 11, 18, 40), 'wovenCaster': actor('woven-threads', 13, 20, 48),
            'geometry': 'Each named cast uses source center[0,0,1], recipient center[20,0,1], halfextents[1,1,1], actual perception where required, no obstruction; recipient lies strictly in Haze sphere.',
            'timeline': [
                'Haze resolves120 atDC16,recipientINT7+4=11fails,affecting[60,120).',
                'Woven resolves126 atDC18,recipientWIS5+4=9fails,selecting personally experienced[115,125)inside its actual[66,126)window; both sources overlap[115,120). The replacement is the same40-word authored narrative, not a readout.',
                'An independent actual Wizard1 with INT18/PB2 and prepared Disrupt Memory resolves130 from20ft away,Action/V/S,rank0,cost0RP4→4,firstmatrixD0,DC14. RecipientWIS5+4=9fails,so accepted Disrupt Memory independently removes firsthand recall of[124,130)and ends actual maintained concentration if any. No concentration application is assumed merely to satisfy that clause.',
                'At300 receive credible independent evidence of the selected[115,125)portion; examine it without interruption through900; trained Insight14+4=18.',
            ],
            'conditionalResult': 'If the proposed family recovery inQ04/Q06 is approved, highest retained familyDC is18. Success clears Haze/Woven restrictions only over selected[115,125),restoring actual original firsthand content over[115,124). Disrupt Memory still independently prevents restored firsthand recall of[124,125),and still covers[125,130)outside the selected portion. External evidence may supply new learned facts there but not undo Disrupt Memory. Haze outside[115,120)remains in place,all original provenance persists,and no never-observed fact is granted.',
            'weakerRecastBoundary': 'A later successful lower-DC edit that genuinely overlaps an eligible recent event cannot lower a still-unrecoveredDC18 restriction underQ06A. This is a conditional rule comparison, not an invented free or out-of-window cast.',
            'endpointQuestion': 'Half-open intervals here are explicit proposed test notation. GPT must confirm exact event ordering at resolution; no current pointer is silently rewritten.'})]

    ck('Four IDs in original order', [v['id'] for v in vectors] == [h['id'] for h in history])
    ck('Real costs and DCs', 32 - 10 == 22 and 48 - 10 == 38 and 40 - 13 == 27 and 8 + 4 + 4 == 16 and 8 + 5 + 5 == 18)
    ck('Actual Wizard HP', 8 + 8 * 6 == 56 and 8 + 10 * 6 == 68 and 8 + 12 * 6 == 80)
    ck('Meeting windows', -60 <= -30 < -10 <= 0 and -65 <= -30 < -10 <= -5)
    ck('Recovery duration and threshold', 900 - 300 == 600 and 14 + 4 == max(16, 18))
    ck('Haze60seconds and actual30second portion', 120 - 60 == 60 and 120 - 90 == 30)
    ck('All witness bodies strictly inside30 undercasepoint', all(sum((max(0, abs(v[i] - [0, 0, 1][i]) - 1)) ** 2 for i in range(3)) < 30 ** 2 for v in [[10, 0, 1], [0, 20, 1], [0, 0, 21]]))
    ck('Haze four exact save outcomes', [5 + 8 >= 16, 7 + 4 >= 16, 17 + 4 >= 16, 4 >= 16] == [False, False, True, False])
    ck('Woven and Disrupt overlap arithmetic', 126 - 60 == 66 and 130 - 6 == 124 and 66 <= 115 < 125 <= 126)
    ck('No successful save invented', 7 + 4 < 16 and 5 + 4 < 18 and 5 + 4 < 14)
    ck('Counts remain480368', index['authoredCounts'] == {'reviewed': 480, 'pending': 368})
    for binding in sources.values():
        ck('Full source unchanged ' + binding['path'], info(G / binding['path']) == binding)
    result = {'id': 'MEMORY-2-DESIGN-CONFERENCE-01', 'recordedAtUtc': datetime.now(timezone.utc).isoformat(), 'status': 'UNSENT / UNADOPTED systemic design conference. Two earlier complete procedures and all four original scenarios preserved. Eight design forks and four conditional traces prepared; no new systemic rule chosen.', 'developmentDirection': 'video-game-only', 'sourceAudit': info(auditpath), 'records': records, 'originalExamplesUnchanged': history, 'conditionalConferenceVectors': vectors, 'completeOriginalSharedProposalsUnchanged': shared, 'currentAcceptedInterfaceComparisons': interfaces, 'completeCurrentCounterparts': counterparts, 'semanticDelta': [deepcopy(s) for s in audit['semanticDelta'] if s['spellId'] in ids], 'questions': questions, 'sourceBindings': list(sources.values()), 'noNewGlobalRule': True, 'historyPolicy': 'Original procedures/source text/access/placements and prior shared proposals are complete historical proposals, not acceptance. Stale historical exampleD+1 does not override current prepared-WizardD0. The new vectors are conditional design comparisons only.', 'nextRequiredWork': 'Actual GPT conference and explicit question dispositions before building the new operative memory procedures, final cases or exact acceptance files.', 'newRuleAdoptions': 0, 'runtimeTestsExecuted': 0, 'sourceInformationDeleted': 0}
    out.write_bytes(encoded(result))
    checkpath.write_bytes(encoded({'candidate': info(out), 'checks': checks, 'checkCount': len(checks), 'failureCount': 0, 'sourceCount': len(sources), 'completeOriginalProcedures': 2, 'originalCases': 4, 'conditionalTraces': 4, 'designQuestions': len(questions), 'newRuleAdoptions': 0, 'runtimeTestsExecuted': 0}))
    print(json.dumps({'candidate': info(out), 'checks': len(checks), 'fullSources': len(sources), 'conditionalTraces': len(vectors), 'unresolvedDesignQuestions': len(questions)}))


if __name__ == '__main__':
    main()
