"""Assemble the LA candidate in new files; keep all original sources and runtime unchanged."""
from pathlib import Path
from datetime import datetime, timezone
from copy import deepcopy
from zipfile import ZipFile
import hashlib
import json

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'
V = A / 'language-source-reviewer-files'

def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p, data):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
def objects(value):
    if isinstance(value, dict):
        yield value
        for child in value.values(): yield from objects(child)
    elif isinstance(value, list):
        for child in value: yield from objects(child)

def main():
    target = R / 'data/director/language_communication_candidate_internal.json'
    assert not target.exists(), 'Preserve an existing candidate; review changes explicitly.'
    source_zip = A / 'DD_Language_Communication_Source_Prepared_v2.zip'
    assert sha(source_zip) == '736b0928dafcd1b0cd46045b4c2466ed780170dac8b5d907bd8fc67c8fc96c0c'
    with ZipFile(source_zip) as z:
        source_manifest = json.loads(z.read('FILE_MANIFEST.json'))
        for path, expected in source_manifest.items():
            assert len(z.read(path)) == expected['bytes'] and hashlib.sha256(z.read(path)).hexdigest() == expected['sha256']
            assert sha(G/path) == expected['sha256'], f'Changed current dependency: {path}'
    assert len(source_manifest) == 152
    reviewer_manifest = read(V/'REVIEWER_FILE_MANIFEST.json')
    for path, expected in reviewer_manifest.items():
        assert (V/path).stat().st_size == expected['bytes'] and sha(V/path) == expected['sha256']
    author = read(V/'LANGUAGE_AUTHORING_REGISTER.json')
    grants = read(V/'GRANT_IDENTITY_REGISTER.json')
    classes = read(V/'CLASS_LANGUAGE_INTERFACE_REGISTER.json')
    pending = read(V/'PENDING_LANGUAGE_INTERFACES.json')
    checklist = read(V/'LANGUAGE_EXACT_CANDIDATE_CHECKLIST.json')
    source_map = read(V/'LANGUAGE_SOURCE_MAP.json')
    prep = read(A/'LANGUAGE_COMMUNICATION_SOURCE_PREPARATION.json')
    advanced = read(A/'LANGUAGE_ADVANCED_INTERFACE_ADDENDUM.json')
    pubcraft = read(R/'data/crafting/advanced_craft_recipe_candidate_public.json')

    modes = ['spokenComprehension', 'speaking', 'reading', 'writing', 'scriptFamiliarity']
    rules = {
        'authority': 'LA-SOURCE-2026-10-11; candidate exact review pending',
        'permanentModeConvention': {'status': 'NEW', 'ordinaryModes': modes[:4], 'scriptFamiliarity': 'only actual established orthography', 'temporaryEffectsUseOwnModes': True, 'unknownSpokenModeNotFalse': True},
        'ordinaryLearning': {'status': 'NEW', 'languageSemanticsMinutes': 14400, 'scriptMinutes': 2400, 'languageLiteracyPracticeMinutes': 2400, 'fullLiteracyMinutes': 4800,
            'fullLanguageMinutes': 19200, 'fullLanguageWithSameScriptMinutes': 16800, 'phaseMinutes': 15,
            'shortFinalPhase': 'Only exact module completion after a real source-specific loss/adjustment',
            'referenceTuition': {'copperPerInstructionMinutes': {'numerator': 100, 'denominator': 480}, 'rounding': 'once upward per actual final purchase', 'actualInstructionIncludesUnproductiveTime': True},
            'watchMinutes': 480, 'maximumActiveWorkWatches': 2, 'teacherTimeOccupied': True, 'concurrentWork': 'Only explicit actual permission; otherwise forbidden',
            'prerequisites': ['actual modes and identified language/script', 'qualified teacher and mutually usable channel OR authentic usable complete curriculum', 'actual access/materials', 'actual production practice for speaking'],
            'completion': 'Deterministic exact required active credit and authentic final practice inside last phase; no additional roll/fee',
            'writtenOnlyCourse': '240 hours written semantics plus 80 literacy; same-script 40-hour credit only; no spoken mode inferred'},
        'ordinaryTranslation': {'status': 'NEW', 'wordsPerTenActiveMinutes': 250, 'minimumMinutes': 1, 'rounding': 'upward to whole minute', 'check': None, 'scope': 'accessible plain noncoded prose; actual source reading and destination writing'},
        'recognition': {'status': 'NEW', 'minutes': 1, 'defaultAbilitySkill': 'INT/History', 'difficulty': {'familiarAttested': 10, 'supportedRelated': 15, 'damagedDiagnostic': 20}, 'result': 'Supported identity/relationship only; no roll if obvious or evidence cannot support identification'},
        'decipherProject': {'status': 'NEW', 'activeMinutes': 480, 'maximumWords': 250, 'lead': 'one declared actual INT/History linguistic or INT/Investigation cipher task', 'dc': [15,20,25],
            'linguisticDifficulties': ['supported related dialect','unfamiliar adequately evidenced','damaged recoverable correspondence'],
            'cipherDifficulties': ['adequate known key','sufficiently constrained ordinary analysis','difficult genuinely solvable incomplete key'],
            'assistantMaximum': 1, 'assistantBonus': 1, 'assistantMinutes': 480, 'pbContributionsMaximum': 1,
            'prerequisites': ['preregister actual passage/output/missing sections','real finite supported meaning','relevant parallel/grammar/key evidence and access'],
            'degrees': 'Existing Core task degrees and natural shifts; success limited to passage; critical grants no extra passage/fluency/labor; failure no certified result; critical failure only separately predeclared lawful hazard',
            'retry': 'New evidence or concretely different supported method, with fresh required work; unchanged reader/date/copy changes do not qualify'},
        'communication': {'status': 'NEW', 'freeOrdinarySecondsPerCreaturePerNumberedRound': 6, 'extraTurnRefresh': False, 'additionalSixSecondSegmentCost': 'Action on actual available turn',
            'offTurnLongExchange': 'Requires applicable permission such as genuinely readied communication Action', 'spellWords': 'Own casting procedure, no added ordinary word cap',
            'interpretationOrder': ['actual reception','understanding','production','destination reception'], 'retroactiveQualification': False,
            'partySignalRehearsalMinutes': 10, 'maximumFixedCues': 6, 'cueRequirements': 'Actual participating learners, required hands/senses, perceptible path',
            'playerAccessibleExplanationIsFictionalSpeech': False},
        'scribingInsight': {'authority': 'KEEP completed SC-08', 'publicGainRecipeId': 'recipe-500', 'gainActiveMinutes': 60, 'gain': 1, 'maximumUnspent': 6,
            'ledgerOwner': ['researcherId','targetLanguageId'], 'oncePerReaderEvidenceIdentity': True, 'saturationBanksAward': False,
            'spend': 3, 'spendActiveMinutes': 480, 'maximumPassageWords': 250, 'extraCheck': False, 'unknownMeaningQualifies': False,
            'fluencyGranted': False, 'workCannotDoubleCount': True},
        'deviceControl': {'authority': 'KEEP actual TI-04', 'minimumControllerINT': 6, 'consentRequired': True, 'bindingActiveMinutes': 10, 'actualTinkersToolsRequired': True,
            'commandDistanceFeet': 60, 'commandAction': 'Bonus Action', 'configuredChannel': ['visible','audible'], 'telepathyIsHardwareAdapter': False,
            'sharedBudget': 'one command and one offensive output per owner per numbered round; actual source exclusions remain', 'serviceAndRepairHistoryPreserved': True},
        'silenceOathWindows': {'authority': 'KEEP different printed windows', 'silentSmiteSince': 'end of previous regular turn', 'vowUnbrokenSince': 'beginning of previous regular turn',
            'newVoluntarySpeechClarification': 'Deliberate speech/V/commands count even when reception fails; missing audibility still fails V. Signs/mental messages/player explanation do not count.'},
    }

    # Explicit record contracts. Required fields store facts and evidence; these are not a runtime engine.
    definitions = {
        'provenance': {'required': ['sourcePath','sourceSha256','recordId','fieldPresence','sourceSpelling','authority'],
            'fields': {'sourcePath':'string; original path','sourceSha256':'64 lowercase hex characters','recordId':'string; exact original ID','fieldPresence':'absent|null|value; preserve distinction','sourceSpelling':'original value only when present; no normalized replacement','authority':'exact grant/decision that permits the derived effect'}},
        'competency': {'required':['recordId','characterId','canonicalLanguageId','sourceSpellings','qualifier','modes','scripts','tenure','provenance'],
            'fields':{'recordId':'unique string','characterId':'actual recipient ID','canonicalLanguageId':'explicit known ID; no fuzzy aliases','sourceSpellings':'array of original strings','qualifier':'actual dialect/register/tradition or explicit null','modes':'object: each of five defined modes is granted|not-granted|unspecified; unknown is never permission','scripts':'array of actual script/orthography ID plus provenance','tenure':'permanent or temporary linked to effect ID','provenance':'nonempty array of actual provenance records'},
            'constraints':['A script-only grant cannot fabricate a speaking mode.','Physical channel suppression is recorded separately from competence.','Duplicate fixed grants union only genuinely granted modes and retain all sources.']},
        'choice': {'required':['slotId','characterId','grant','count','restriction','alternatives','priorCompetencyIds','state','resolution'],
            'fields':{'slotId':'unique source-linked string','characterId':'actual learner','grant':'provenance','count':'positive integer from actual grant','restriction':'verbatim source restriction and derived eligibility rule','alternatives':'closed IDs if specified; otherwise null with actual available options recorded at resolution','priorCompetencyIds':'array of existing actual competencies','state':'unresolved|resolved|invalid|exhausted','resolution':'null while unresolved; otherwise selected ID/modes or exhausted result, actual eligibility evidence, time and retained original choice'},
            'constraints':['Mycelian requires actual home-region evidence.','Elemental-Touched uses actual preselected affinity.','No secret future credit or free historical respec.']},
        'temporaryEffect': {'required':['effectId','source','casterId','recipientIds','allowedModesOrMeaning','consentEvidence','rangeAndChannel','start','expiration','suppression','costRecordIds'],
            'fields':{'effectId':'unique string','source':'exact card ID/path/hash and lawful access evidence','casterId':'actual source creature','recipientIds':'actual recipients','allowedModesOrMeaning':'bounded source modes/message/passage only','consentEvidence':'actual evidence when required; null only when source requires none','rangeAndChannel':'actual predicate and delivery evidence','start':'actual chronological event marker','expiration':'original exact marker plus elapsed-time mapping through initiative changes','suppression':'independent source-linked restriction records','costRecordIds':'links to actual resource histories'},
            'constraints':['Not a second resource ledger.','Expiration removes capabilities, preserves only actually learned particular information.','No shared language implied unless this exact interface provides it.']},
        'learning': {'required':['courseId','learnerId','languageId','modes','modules','instruction','access','intervals','losses','fees','completion'],
            'fields':{'courseId':'unique string','learnerId':'actual learner','languageId':'one actual competency','modes':'exact sought modes','modules':'required minutes, genuine prior same-script evidence, completed credit and remaining credit','instruction':'actual teacher modes plus usable channel OR identified authentic curriculum','access':'actual materials, legitimacy and production/correction method','intervals':'ordered start/end actual active intervals with complete phase credit, interruption reason and work-ledger references','losses':'actual source/effect, time and credited minutes lost; preserve history','fees':'actual quote, instruction minutes and invoice-rounded copper/payment record; no fabricated teacher','completion':'null or actual final practice, time and exact acquired modes'},
            'constraints':['No overlapping work without explicit source permission, including tutor.','A phase boundary is not an actual concentration interruption.','A shorter final phase only finishes a real adjusted balance.']},
        'textEvidence': {'required':['physicalTextId','contentVersionId','underlyingEvidenceId','languageAndScript','passage','representation','sourceMeaningEvidence','translationProvenance','parentCorrespondenceIds','audience'],
            'fields':{'physicalTextId':'unique inventory object','contentVersionId':'actual content/version identity','underlyingEvidenceId':'stable correspondence identity shared across copies and recreations','languageAndScript':'actual known identities, with unknown preserved','passage':'registered boundaries, words<=250 for bounded projects and explicit gaps','representation':'actual legibility/access/channel','sourceMeaningEvidence':'finite supported meaning/key/evidence; unavailable explicitly fails prerequisite','translationProvenance':'actual method, lead, work, checks if required and output extent','parentCorrespondenceIds':'source evidence lineage','audience':'public|director-only|restricted; unknown fails public export'},
            'constraints':['A new physical copy does not create new evidence.','No caller boolean certifies missing meaning.','Copying characters alone is not translation or magical encoding.']},
        'scribingLedger': {'required':['researcherId','targetLanguageId','unspent','evidenceReceipts','events'],
            'fields':{'researcherId':'one actual researcher','targetLanguageId':'one actual target language','unspent':'integer 0..6','evidenceReceipts':'all underlying correspondence IDs already studied by this reader, including saturated studies','events':'chronological actual gain/spend events, work references, evidence, amount, before/after, passage and prerequisite adjudication'},
            'constraints':['A saturated award is not banked.','Copies/holders/editions/magical recreations share anti-repeat identity.','Three points and eight separate hours yield one supported passage, not fluency.']},
        'communicationEvent': {'required':['eventId','senderId','intendedRecipientIds','channel','contentEvidence','capacityEvidence','delivery','interpretation','receipts','roundBudget'],
            'fields':{'eventId':'unique string','senderId':'actual actor','intendedRecipientIds':'actual addressed recipients','channel':'spoken|written|rehearsed-cue|actual-feature-channel, with feature ID if needed','contentEvidence':'specific content/meaning available to sender, recipient language/mode evidence','capacityEvidence':'actual hand/sense/voice/path/cost/consent state','delivery':'ordered actual start/end events','interpretation':'zero or more incoming receipt -> interpretation -> outgoing delivery links','receipts':'actual recipients and arrival events with supported comprehension; no arbitrary understood flag','roundBudget':'numbered round plus aggregate free ordinary seconds, Actions/readied permission and no refresh on extra turns'},
            'constraints':['No retroactive reception or reaction window.','Player explanations have no fictional communication event unless the character acts.','Hearing-only effects require actual hearing, not translated meaning by another channel.']},
    }
    schema = {'version':1, 'status':'Authored record contract; not an implemented companion schema migration', 'modeNames':modes,
              'presenceRule':'Preserve absent/null/empty/value separately in originalSource objects; derived fields explicitly state unresolved values', 'definitions':definitions}

    backgrounds = deepcopy(grants['backgrounds'])
    open_one = {'disgraced-noble-scion','guild-artisan-dropout','relic-hunter'}
    open_two = {'seeker-of-the-lost-pantheon','arcane-academy-dropout','planar-merchant','dimensional-refugee','prophecy-bearer'}
    for b in backgrounds:
        ident=b['backgroundId']; fixed=[]; choice=None
        if ident in open_one|open_two: choice={'count':2 if ident in open_two else 1,'kind':'open-admitted','alternatives':None,'restriction':b['originalLanguagesSource']}
        elif ident=='rift-scarred-survivor':choice={'count':1,'kind':'closed','alternatives':['abyssal','celestial','primordial','deep-cant'],'restriction':b['originalLanguagesSource']}
        elif ident=='wildling-herbalist':choice={'count':1,'kind':'closed','alternatives':['sylvan','primordial'],'restriction':b['originalLanguagesSource']}
        elif ident in {'marked-fugitive','cult-escapee','corruption-survivor'}:choice={'count':1,'kind':'restricted-open-examples-not-closed','alternatives':None,'restriction':b['originalLanguagesSource']}
        elif ident=='elemental-touched':choice={'count':1,'kind':'general-or-actual-affinity','alternatives':{'general':'primordial','byActualAffinity':grants['dialectPolicy']['affinityMap']},'restriction':b['originalLanguagesSource']}
        elif ident=='celestial-emissary':fixed=['celestial']
        else:assert not b['sourceLanguagesFieldPresent'],ident
        b['derivedGrant']={'fixed':fixed,'choice':choice,'modes':'LA-04 full ordinary modes except specifically narrower written competency','newGrantBeyondSource':False}

    current_cards={c['id']:c for group in prep['classComparisonRecords'] for c in group['cards']}
    extra=classes['additionalActuallyReadCalledCard']
    matches=[x for x in objects(read(G/extra['sourceFile'])) if x.get('id')==extra['id']]
    assert len(matches)==1
    current_cards[extra['id']]=matches[0]
    all_interfaces=deepcopy(classes['selectedCards'])+[dict(extra, name=matches[0]['name'], sourceFileSha256=sha(G/extra['sourceFile']), sourceStatus=matches[0].get('designStatus'), classCardPromoted=False)]
    for c in all_interfaces: c['originalSourceRecord']=deepcopy(current_cards[c['id']])
    spell_interfaces=[]
    routes={s['id']:s for s in pending['spells']}
    for s in prep['spellComparisonRecords']:
        spell_interfaces.append({'id':s['id'],'name':s['name'],'originalSourceRecord':s,'languageCase':'LA-11' if s['operational'] is None else 'LA-10',
            'disposition':routes[s['id']]['exactExistingQuestion'] if s['operational'] is None else 'KEEP complete actual operational object; apply LA-10 comprehension/channel boundaries without changing access/status',
            'operational':s['operational'],'status':s['status'],'promotedByLanguageCandidate':False,
            **({'pendingRoute':{'preparationFile':routes[s['id']]['preparationFile'],'questionId':routes[s['id']]['questionId']}} if s['id'] in routes else {})})
    original_grants={'ancestries':prep['ancestryGrants'],'backgrounds':prep['backgroundGrants'],'runtimeAlternatives':prep['runtimeLanguageAlternatives']}
    public_grants={'baseGrants':deepcopy(grants['baseGrants']),'variants':deepcopy(grants['variants']),'backgrounds':backgrounds,
                   'aliases':deepcopy(grants['aliases']),'explicitlyNotAliases':deepcopy(grants['explicitlyNotAliases']),
                   'dialectPolicy':deepcopy(grants['dialectPolicy']),'scripts':deepcopy(grants['scripts']),
                   'identities':deepcopy(grants['identityRegistry'])}
    # All identity labels above were individually inspected; comparison/deferred labels are NOT choice entries.
    for row in public_grants['identities']:
        row['automaticChoiceEntitlement']=False
        row['sourceNamesPreserved']=True
    public_classes=[{k:c[k] for k in ('id','name','disposition','sourceStatus','classCardPromoted') if k in c} for c in all_interfaces]
    public_spells=[{'id':s['id'],'name':s['name'],'status':s['status'],'classAccess':s['originalSourceRecord']['classAccess'],
                   'operational':s['operational'],'languageCase':s['languageCase'],'promotedByLanguageCandidate':False,
                   **({'pendingRoute':s['pendingRoute']} if 'pendingRoute' in s else {})} for s in spell_interfaces]
    public_scribing_ids={c['recipeId'] for c in advanced['completeScribingCards'] if c['visibility']=='public'}
    public_scribing=[deepcopy(c) for c in pubcraft['cards'] if c['recipeId'] in public_scribing_ids]
    assert len(public_scribing)==28
    status={'schemaVersion':1,'candidateVersion':'LA-CANDIDATE-v1','status':'authored-candidate-exact-review-pending','sourceReview':'LA-SOURCE-2026-10-11',
            'exactLanguageApproval':False,'classSpellFeatPromotion':False,'runtimeImplemented':False,'humanBalanceApproved':False,'wholeGameFlowApproved':False}
    public={**status,'audience':'public','guide':'docs/mechanics/LANGUAGE_COMMUNICATION_PLAYTEST.md','rules':rules,'grants':public_grants,'recordSchema':schema,
            'classInterfaces':public_classes,'spellInterfaces':public_spells,
            'pendingFeatInterfaces':[{'id':f['id'],'status':'pending-own-exact-review; no effect activated by this chapter'} for f in prep['pendingFeatSourceComparisons']],
            'publicScribingCards':public_scribing,
            'migration':{'performed':False,'rule':'Preserve old bytes; reconcile actual Human/Undead choice slots and Mycelian regional choice from evidence. No automatic Mycelic or retroactive tuition.'},
            'publicationMethod':'Explicit public fields and separately completed public recipe records; no projection of internal recipe records or private source dossiers.'}
    internal={**status,'audience':'director-only','guide':'docs/director-only/LANGUAGE_COMMUNICATION_INTERNAL_CANDIDATE.md','rules':rules,'recordSchema':schema,
              'decisionApplicationRegister':deepcopy(author['decisions']),'sourceMap':source_map,'originalGrantEvidence':original_grants,
              'derivedGrants':public_grants,'classInterfaces':all_interfaces,'classEngineContexts':prep['classComparisonRecords'],
              'spellInterfaces':spell_interfaces,'pendingInterfaces':pending,'completedAdvancedInterfaces':advanced,
              'deferredReceipt':deepcopy(author['decisions'][-1]),'originalSourceManifest':source_manifest,
              'sourceRuntimeArraysUnchanged':True,'publicProjectionPath':'data/playtest/language_communication_candidate_public.json'}

    guide_path=R/'docs/mechanics/LANGUAGE_COMMUNICATION_PLAYTEST.md'
    guide=guide_path.read_text(encoding='utf-8')
    assert '<!-- BASE_GRANT_TABLE -->' in guide and '<!-- BACKGROUND_GRANT_TABLE -->' in guide
    base_names={x['ancestryId']:x['fullCurrentAncestryRecord']['name'] for x in prep['ancestryGrants']}
    bg_names={x['backgroundId']:x['fullCurrentBackgroundRecord']['name'] for x in prep['backgroundGrants']}
    labels={r['canonicalId']:r['literalName'] for r in grants['identityRegistry']}
    base_table=['| Base ancestry | Starting languages |','|---|---|']
    for b in grants['baseGrants']:
        choices=b['derivedChoice']; desc=', '.join(labels[v] for v in b['derivedFixed'])
        if choices:desc+='; one choice'+(' common in its actual home region' if b['ancestryId']=='mycelian' else '')
        base_table.append(f"| {base_names[b['ancestryId']]} | {desc} |")
    bg_table=['| Background | Additional language grant |','|---|---|']
    for b in backgrounds:bg_table.append(f"| {bg_names[b['backgroundId']]} | {b.get('originalLanguagesSource','None; source has no Languages field')} |")
    guide=guide.replace('<!-- BASE_GRANT_TABLE -->','\n'.join(base_table)).replace('<!-- BACKGROUND_GRANT_TABLE -->','\n'.join(bg_table))
    guide_path.write_text(guide,encoding='utf-8')
    public['guideText']=guide
    save(R/'data/playtest/language_communication_candidate_public.json',public)
    save(target,internal)
    internal_guide=['# Language and communication: internal operating candidate','',
        '**LA-CANDIDATE-v1; authored candidate, exact joint review pending. Director-only.**',
        'The player procedure is [Languages, literacy and communication](../mechanics/LANGUAGE_COMMUNICATION_PLAYTEST.md). Use that chapter at the table. The following complete application register preserves every agreed source direction, including the private interfaces and deferred receipts. All NEW rules remain labeled; this document supplies no source-card promotion or companion implementation.',
        'The [internal data](../../data/director/language_communication_candidate_internal.json) contains the complete unchanged selected source records, all class engine contexts, 40 Scribing cards, 19 completed advanced sections, and the actual pending routes. Its public counterpart is independently selected from authorized public fields and public recipe records.',
        '## Procedure for the Director','',
        'Establish real language/access premises before resolving choices or study. Use supported meaning and an actual communication path before a roll or feature qualifies. Apply the public chapter for time, costs and outcomes; consult the exact card for exceptions. Record independent conditions, actual resource histories and original expiration markers. Preserve evidence identities across copies. Never solve a missing source by granting a language, teacher, protocol, spell, or private meaning.',
        '## Full decision application register','']
    for d in author['decisions']:
        internal_guide += [f"### {d['id']} — {d['title']}",'',f"**{d['disposition']}. Candidate implementation; exact review pending.**",'',d['authoringWording'],'', '**Worked boundary:** '+d['workedBoundaryOutcomes'],'']
    internal_guide += ['## All selected class interfaces','']
    for c in all_interfaces:internal_guide += [f"### {c['id']}",'',c['disposition'],'']
    internal_guide += ['## Source status and audience','',
        'All 152 original submitted payloads and their current dependencies matched before construction. The original source ZIP and the full reviewer ZIP are preserved in the audit directory. Public output contains only the 28 public Scribing records from the completed public envelope; private or restricted membership and dossiers remain here. Neither a source path containing public nor a legacy draft flag supplies a new review approval.',
        'The full 32-case checklist is the next exact-review gate. Worked examples are authored adjudications; reference calculations and static source-preservation checks are separate evidence. DD-01, runtime, human teaching/balance, full integration and final flow remain open. Final flow precedes the authorized GitHub push; verified remote commit precedes cosmology review.']
    ip=R/'docs/director-only/LANGUAGE_COMMUNICATION_INTERNAL_CANDIDATE.md'
    ip.write_text('\n\n'.join(internal_guide)+'\n',encoding='utf-8')
    save(A/'LANGUAGE_SOURCE_VERDICT_RECEIPT.json',{
        'reviewId':'LA-SOURCE-2026-10-11','requestId':'fb9c40f4-3f25-479a-954d-53b172ba08fd','replyId':'08f18635-6dea-4d41-8f11-19fafb1baf2c',
        'threadId':'6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b','receivedAtUtc':datetime.now(timezone.utc).isoformat(),
        'verdict':str(V/'LA_Language_Communication_Source_Verdict.md'),'verdictSha256':sha(V/'LA_Language_Communication_Source_Verdict.md'),
        'reviewerZip':str(A/'DD_Language_Communication_Source_Verdict_and_Evidence.zip'),'reviewerZipSha256':sha(A/'DD_Language_Communication_Source_Verdict_and_Evidence.zip'),
        'reviewerManifestVerified':len(reviewer_manifest),'reproducedChecks':460,'failures':len(read(A/'LANGUAGE_SOURCE_REPRODUCED_460_CHECKS.json')['failed']),
        'sourceArchiveSha256':sha(source_zip),'currentSourceDependenciesUnchanged':len(source_manifest),
        'status':'LA-01–15 authoring directions received and applied to first candidate; LA-16 receipt only; candidate exact review not yet submitted',
        'newApprovals':0,'sourceInformationDeleted':0,'runtimeChanged':False,'pushPerformed':False,'cosmologyReviewed':False})
    save(A/'LANGUAGE_CANDIDATE_V1_BUILD_RECEIPT.json',{'status':'First authored guide/data candidate; worked sequence adjudications and exact submission pending',
        'files':{str(p.relative_to(G).as_posix()):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in [guide_path,ip,target,R/'data/playtest/language_communication_candidate_public.json']},
        'counts':{'baseGrants':14,'variants':45,'backgrounds':20,'selectedClassCards':48,'calledClassCard':1,'spells':23,'pendingSpellRoutes':15,'pendingFeats':8,'scribingCards':40,'advancedSections':19,'publicScribingCards':28},
        'sourcePayloadsUnchanged':152,'exactReviewSubmitted':False,'candidateApproved':False})
    print(json.dumps({'created':4,'grantCounts':[len(grants['baseGrants']),len(grants['variants']),len(backgrounds)],'classInterfaces':len(all_interfaces),'spellInterfaces':len(spell_interfaces),'publicScribing':len(public_scribing),'exactApproval':False}))

if __name__=='__main__': main()
