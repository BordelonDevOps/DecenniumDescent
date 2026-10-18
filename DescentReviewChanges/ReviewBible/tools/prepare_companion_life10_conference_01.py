"""Package ten preserved life/companion proposals for decisions before new rules."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import hashlib, json, zipfile
from apply_di7_ap_as_01 import G, R, A, info, encoded
from prepare_ac5_current_interfaces_01 import at


def read(p):
    return json.loads(p.read_bytes())


def main():
    ap = R / 'data/director/spell_review/companion_life_10_source_convergence_01.json'
    out = R / 'data/director/spell_review/companion_life_10_conference_01.json'
    root = A / 'companion-life10-conference-01'
    archive = A / 'DD_Companion_Life_10_Conference_01.zip'
    prep = A / 'COMPANION_LIFE_10_CONFERENCE_01_PREPARATION.json'
    requestp = A / 'COMPANION_LIFE_10_CONFERENCE_01_REQUEST.txt'
    assert not any(p.exists() for p in [out, root, archive, prep, requestp])
    audit = read(ap)
    sources = {b['path']: b for b in audit['sourceBindings']}
    checks, questions, vectors = [], [], []

    def ck(name, value):
        checks.append({'check': name, 'passed': bool(value)})
        assert value, name

    def bind(p):
        b = info(p)
        sources[b['path']] = b
        return b

    for p in [ap, A / 'COMPANION_LIFE_10_SOURCE_CHECK_01.json', Path(__file__)]:
        bind(p)
    by_id = {r['spellId']: r for r in audit['records']}
    wp = R / 'data/public/class_playtests/wizard.json'
    clp = R / 'data/public/class_playtests/cleric.json'
    wizard, cleric = read(wp), read(clp)
    catalogp = R / 'data/public/spell_playtests/catalog.json'
    catalog = read(catalogp)
    indexp = R / 'data/public/spell_playtests/authored_review_index.json'
    index = read(indexp)
    additional = []
    for ident in ['arcane-ward', 'death-ward']:
        entry = next(e for e in index['entries'] if e['id'] == ident)
        ck('Actually reviewed counterpart: ' + ident, entry['authoredStatus'] == 'reviewed-authored-operational-playtest')
        p = (indexp.parent / entry['procedureFile']).resolve()
        doc = read(p)
        ptr = entry.get('wholeCardPointer', entry['procedurePointer'])
        additional.append({'spellId': ident, 'source': bind(p), 'pointer': ptr, 'completeCurrentCard': deepcopy(at(doc, ptr)), 'completeSharedRules': deepcopy(doc.get('sharedRules', {})), 'currentIndexEntry': deepcopy(entry)})

    def q(n, ids, promise, gap, a, b, recommendation, inherited):
        questions.append({'id': f'CL10-Q{n:02}', 'spells': ids, 'classification': 'OPEN DESIGN QUESTION',
                          'sourcePromise': promise, 'newDecision': gap, 'optionA': a, 'optionB': b,
                          'recommendedForConference': recommendation, 'inheritedAcceptedInterface': inherited,
                          'sourcePointers': [by_id[ident]['sourceReference'] for ident in ids],
                          'scope': 'Only named sources. No universal lifecycle, resource, bestiary, soul or cosmology rule.',
                          'status': 'UNSENT; no option adopted'})

    q(1, ['summon-corpse-golem'], 'Summon a Corpse Golem, HP60 and2d10 attack; complete original Core/source retained.',
      'Confirm complete Construct profile without a physical corpse input and Slow Aura as an alternative commanded offense.',
      'Retain proposed HP60/AC15/600lb/Speed20 finite body, one Slam or one10ft Slow Aura per shared offense; aura CON, half-Speed only while in field, one save per activation and original-owner-next-START endpoint.',
      'Keep the printed body/attack but require a real corpse or remove/rework the aura through an explicit source-conflict choice with full revised examples.',
      'A preserves the prior source-compatible proposal without inferring souls or consumed corpse material; confirm complete profile and command channel.',
      'Existing owner command/offense and actual damage/save/condition rules are inherited.')
    q(2, ['summon-corpse-golem', 'summon-death-knight', 'summon-soul-wraith', 'create-homunculus'],
      'Distinct sources summon/create distinct bodies; uniform suppression behavior is not printed.',
      'Disposition each original source-specific lifecycle, including source-sustaining classification and current body/cargo location.',
      'Retain Golem/Wraith/Homunculus full-source-suppression ending and Knight temporary absent-body suspension, with real cargo drop and original HP/clock/history. Supply exact local Knight placement/reappearance and Wraith cargo position rules.',
      'Change one or more explicitly identified sources to a different finite suppression state machine, preserving full source promise and all affected cases.',
      'A preserves the original differences unless an actual source contradiction is shown. No accepted pet behavior becomes a universal rule.',
      'Actual Lesser Antimagic and Greater Dispel eligibility/loci remain unchanged; current sources determine their effects.')
    q(3, ['soulburn-pact'], 'Sacrifice20HP; catalog grants up-to3RP while Core prints5RP. Rank4 remains7RP.',
      'Choose recovery amount and intended resource utility without hiding the negative net return.',
      'Retain3RP self recovery, pay7RP then20 real normal HP before countering, requireHP≥21 and sufficient quotedRP. Successful undiscounted cast is net−4RP.',
      'Select Core5RP or a separately explicit source amendment, retaining actual cast payment and documenting the resulting net value and every changed scenario.',
      'Ask GPT to choose explicitly; neither3 nor5 yields net recovery at an unmodified7RP cost. No free discount or renamed technique may be invented to conceal that problem.',
      'Ordinary quoted cost, no credit from future recovery, directHP payment and no failed-cast refund are inherited.')
    q(4, ['soulburn-pact'], 'No beneficial-rest frequency limit is printed in the source promise.',
      'Decide the proposed one successful-attempt use between beneficial long rests, including countered casts and genuine price waivers.',
      'Retain one use spent at legal commitment, even if countered; real beneficial-rest rules reset it. Actual scoped RP waivers do not waive20HP or generate extra uses.',
      'Remove the new use cap; each otherwise legal paid cast may occur under actual action, RP, HP and cadence constraints.',
      'B is more source-faithful unless a specific free-cost exploit justifies the proposed new limit. Request the exact exploit and scope rather than a blanket resource fear.',
      'Current true cost modifiers and beneficial-rest limits are unchanged; ordinary idle turns do not reset Refrain.')
    q(5, ['summon-death-knight'], 'Summon a Death Knight with HP80/AC18 and2d10necrotic attack.',
      'Confirm new complete ability/sense/movement profile, owner-derived attack/saves, one-body cap and nonloot intrinsic equipment.',
      'Retain the complete proposed Medium Undead profile, one owner-commanded attack, one-body cap and fixed baseHP80 before genuinely eligible source modifiers; keep distinct temporary suspension underQ02.',
      'Use a different explicitly authored complete profile with exact source rationale and full affected example replacements.',
      'A preserves the printed80/18/2d10 and complete pending procedure. Its name grants no fear aura, immunity, Multiattack or transferable sword.',
      'Current maximumHP source qualifications, original source owner and companion action budget are inherited.')
    q(6, ['grave-gift'], 'Sacrifice half HP to fully restore an ally from Dying; the source does not settle Critical or broad prohibition.',
      'Choose direct full-effective-maximum state recovery versus ordinary healing, and exact eligible living0 recipient.',
      'Retain another willing living Dying/Stable0 ally, floor(current normalHP/2) donor cost with≥1HP retained, and direct assignment to effective max, preserving all Wounds/Critical while bypassing only ordinary-healing ceiling/modifiers.',
      'Treat as ordinary healing up to the actual effective maximum, retaining Critical ceiling and applicable healing modifiers; define the source-consistent meaning of fully restore.',
      'A matches the former proposal but is material new authorship requiring explicit concurrence. Keep resurrection, Wound removal and resource restoration separate.',
      'Accepted distinction between HP payment, ordinary healing and direct state recovery remains unchanged; this spell must choose its own operation.')
    q(7, ['grave-gift'], 'Full recovery can be blocked by an actual cannot-regain-HP rule.',
      'Decide independent stabilization and actual-gain triggers when recovery is blocked.',
      'Retain blocked recovery→Stable0, clear counters and establish exactly one real d4-hour deadline for a formerly Dying target; an already Stable target keeps its original deadline. Costs remain spent; no ordinary healing modifier/copy trigger.',
      'Blocked recovery leaves the prior Dying/Stable state unchanged because the source prints no independent stabilize component.',
      'A preserves the prior proposal, but request a complete trigger/disclosure statement and lawful actual blocker fixture before claiming a fully sourced case.',
      'Stable clocks and broadHP prohibition remain inherited; a proposed stabilization exception does not change other blocked recovery sources.')
    q(8, ['negative-energy-flood', 'danse-macabre'], 'Flood creates a zombie on qualifying Humanoid death; Danse animates up to five corpses.',
      'Confirm the complete new zombie profile, separate caps, hour lifetime and suppression of real consumed bodies.',
      'Retain shared HP20/AC10/STR12/DEX6/CON14/INT3/WIS6/CHA3 profile, actual missing anatomy, one1d6bludgeoning attack, one hour, no creation-round acts; one Flood slot and five Danse bodies, both outside actual Wizard standard-minion slots.',
      'Use another explicitly named existing or new complete profile/cap/lifetime, with the actual source access and all changes recorded; never silently borrow a Wizard class asset.',
      'A preserves the prior proposals and meaningful separate spell identities; explicitly disposition each cap and suppression choice.',
      'One owner command/offense, actual body allocation, real gear and no duplicate corpse fuel are inherited.')
    q(9, ['negative-energy-flood'], 'Only actual death caused by this damage creates its zombie.',
      'Choose exact qualifying original recipient, post-response claim timing and interactions with actual competing corpse consumers.',
      'Retain original-target actual Humanoid death from this packet, after real immediate survival/resurrection responses and before a genuinely existing later Auto-Raise checkpoint; actual eligible corpse and original space rechecked once.',
      'Queue this source alongside ordinary later corpse claims at their real shared checkpoint, with complete deterministic priority and no guaranteed earlier claim.',
      'A preserves the prior promise. Require an actually qualifying Auto-Raise event before showing a competing reservation: Flood by itself is not a standard minion personal killing blow.',
      'Accepted damage/life responses, body identity and Auto-Raise triggers remain unchanged; no extra reservation is invented.')
    q(10, ['danse-macabre', 'create-undead'], 'Animate actual corpses, with distinct spells and named outcomes.',
      'Confirm Danse24-hour limit versus Create Undead no arbitrary age limit, body completeness and successful replacement rules.',
      'Retain each original admission: Danse≤24hours, torso/head and actual retained anatomy; Create Undead actual surviving usable matter without a generic age cap. Paid hidden failure grants no replacement body selection. Keep each separate source cap.',
      'Choose a different explicit local corpse age/anatomy policy, preserving both source promises and explaining every rejected original case.',
      'A keeps source-compatible differences; do not use this to decide global corpse decay or soul reconstruction.',
      'One actual consumed body, missing anatomy and independent resurrection prerequisites remain unchanged.')
    q(11, ['summon-soul-wraith'], 'HP100/AC18 incorporeal creature,2d10necrotic plus lifetap.',
      'Choose lifetap recipient and eligible donor provenance without changing Vampiric Touch.',
      'Retain self-only Wraith healing=floor(eligible numeric actualDamageDealt/2), temporaryHP included, original/terminal branches counted once, excluding temporary summons/copies/no-resource creations and consumed animated bodies.',
      'Use accepted Vampiric Touch numeric funding without these new provenance exclusions, or another explicit source-local recipient/funding choice with full consequences.',
      'A preserves the prior proposal but must be accepted as a new restriction. Type alone is not a funding exclusion; do not silently ban all Undead/Construct donors.',
      'Actual numeric damage, transfer exclusions, healing caps/prohibitions and destroyed-recipient timing are inherited.')
    q(12, ['summon-soul-wraith'], 'Incorporeal movement, not sight through walls or arbitrary cargo transport.',
      'Complete difficult-terrain passage, whole-body exit, finite expulsion and real cargo drop.',
      'Retain2ft budget per1ft ordinary solid traversal, Fly40/Hover, no real cargo through solids, actual last-entry-side escape path and once-at-phase-END1d10force if trapped; finite nearest-space fallback only where explicitly allowed, otherwise end manifestation.',
      'Permit passage only when the entire declared route and final open whole-body space are legal; if a later external event traps it, use only accepted adjacent placement/ending without a new force-damage rescue.',
      'Ask for complete source-local text choosingA orB. Cargo must use its actual current/entry-side position and never teleport to an unrelated historical point.',
      'Actual perception/LoE, whole-body geometry, real carrying and existing source-scoped placement remain unchanged.')
    q(13, ['command-undeath'], 'Up to two existing Undead, printed CR2, permanently bound until dispelled.',
      'Choose literal exactCR2 versus an upper bound and define permanent non-Charmed control admission.',
      'Retain exactlyCR2, failedWIS plus one actual hard-control admission, two bindings per caster/one per target, no invented repeat saves or concentration.',
      'Interpret CR2 as≤2 with explicit source reasoning, retaining the other individually chosen control components and requiring actual documented creature eligibility.',
      'A preserves the prior literal interpretation; no current public source candidate supplies an exactCR2 Undead row. Keep examples conditional rather than invent a monster.',
      'Accepted actual saves/immunities and source-character/target hard guard remain unchanged.')
    q(14, ['command-undeath'], 'Permanent binding redirects an actual existing creature.',
      'Confirm schedule transition, defensive-only uncommanded agency, source-owner/binder caps and absence/death/suppression behavior.',
      'Retain the complete proposed independent-to-attached transition with no duplicated regular opportunity; existing companion keeps its actual original-owner phase/stats/slots and dual-owner reservation constraints. Suppression restores only actual ordinary agency; an absent binder grants no invented phase.',
      'Keep every independent creature on its original schedule, with one explicitly queued future forced action under an amended permanent control rule; supply full restriction and command timing.',
      'A retains the prior procedure, but require exact deterministic pending-opportunity mapping and permanent dormant relation behavior. No command grants resources, secrets, oath breach or a new soul claim.',
      'Current compelled-budget arbitration and accepted Dominate Beast/Person source-qualified bridges remain intact.')
    q(15, ['create-undead'], 'Create Ghoul, Ghast, Wight or Mummy; all four alternatives must survive.',
      'Confirm four complete new profiles, permanent conversion, separate dispellable two-slot command authority and released agency.',
      'Retain all four full explicit profiles and permanent real bodies. Slot replacement releases authority without destroying the old body; released/suppressed bodies have actual independent agency and no duplicate turn. Repeated paid casts with fresh eligible corpses can accumulate independent bodies.',
      'Retain all four profiles but bound body persistence to creator authority or an explicit finite body cap, changing the former permanence proposal and all affected cases openly.',
      'Ask GPT to explicitly accept or rejectA’s accumulating permanent-body consequence. Keep CR unrated, original-owner scaling and actual physical needs explicit; no automatic loyalty/hostility or harvest entitlement.',
      'Existing body provenance, shared companion budget and no source-resource refresh remain unchanged; four new stats require actual authorship concurrence.')
    q(16, ['create-homunculus'], 'Create a servant that carries out commands; no named consumed material is printed.',
      'Confirm persistent Tiny physical servant, supervised chores, no-resource ending and paid nonspell maintenance.',
      'Retain the complete8lb/HP20/AC14/STR6/Fly30/Hover profile,45lb and3Load simultaneous cargo limits, spoken supervised60ft chores, actual BA attached task in combat, and original-caster Action/touch/2RP/2d6 repair of a surviving body.',
      'Use a narrower nonphysical task servant or ordinary repair-source-only physical servant, with exact source conflict, body/cargo and usefulness consequences stated.',
      'A preserves the prior physical servant; confirm which actual work roles it cannot replace and whether the new repair operation is intended. No invisible skill, crew slot, shop income or free salvage.',
      'Actual carrying/Load, real task timing, crafting/EX58 credentials and source-qualified maximumHP remain inherited.')

    # The actual persistent20 conference identified a footprint error in named
    # class fixtures. Do not submit the unfinished vectors below as current.
    # This packet asks the required design questions BEFORE new systemic rules.
    geometry_notice = {
        'finding': 'Named Small/Medium creatures use accepted5x5ft occupied space unless an actual exception applies; half-extents[1,1,1] cannot certify those class-based fixtures.',
        'source': bind(R / 'docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md'),
        'actualGPTResponse': bind(A / 'PERSISTENT_DAMAGE_20_CONFERENCE_06_ACTUAL_GPT_FINAL.json'),
        'currentAction': 'Hold new concrete geometry vectors for exact occupancy/range/LoE revalidation. Original20 case texts are preserved as scenario obligations, not complete proved integrations.',
        'WraithObligation': 'A15ft-thick wall and a body with nonzero extent require entry/exit distances. The old30spent/10remaining arithmetic describes only a15ft contacted path segment; it does not by itself prove a whole-body crossing. Q12 must specify actual contact metric and complete path.'}
    ck('Sixteen distinct questions', len(questions)==len({q['id'] for q in questions})==16)
    ck('Twenty original scenarios intact', len(audit['all20HistoricalScenarioTexts'])==20)
    for row in audit['records']:
        ref=row['sourceReference']
        ck('Exact original procedure: '+row['spellId'], at(read(G/ref['source']['path']),ref['pointer'])==row['completeEarlierRecordUnchanged'])
    result={'id':'COMPANION-LIFE-10-CONFERENCE-01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
            'status':'UNSENT / UNADOPTED pre-authorship design conference; not a complete current operating-candidate review.',
            'developmentDirection':'video-game-only','sourceAudit':info(ap),
            'records':deepcopy(audit['records']),'all20HistoricalScenarioTexts':deepcopy(audit['all20HistoricalScenarioTexts']),
            'completeOriginalSharedProposalsUnchanged':deepcopy(audit['completeOriginalSharedProposalsUnchanged']),
            'inheritedAcceptedInterfaces':deepcopy(audit['currentAcceptedInterfaceComparisons']),
            'completeAcceptedCounterparts':deepcopy(audit['completeAcceptedCounterparts'])+additional,
            'completePendingCounterparts':deepcopy(audit['completePendingCounterparts']),
            'semanticDelta':deepcopy(audit['semanticDelta']),'findings':deepcopy(audit['findings']),
            'bestiarySourceSearch':deepcopy(audit['bestiarySourceSearch']),'conferenceQuestions':questions,
            'geometryPreflightHold':geometry_notice,'newCurrentVectorsSubmitted':0,
            'sourceBindings':list(sources.values()),'riskCounts':audit['riskCounts'],
            'countsUnchanged':{'reviewed':480,'pending':368},'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0,'cosmologyDecisions':0}
    out.write_bytes(encoded(result))
    bind(out)
    root.mkdir()
    frozen=[]
    for b in sources.values():
        ck('Current source: '+b['path'],info(G/b['path'])==b)
        p=root/'sources'/b['path']
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes((G/b['path']).read_bytes())
        ck('Exact preserved source: '+b['path'],info(p)['sha256']==b['sha256'])
        frozen.append({**b,'archivePath':'sources/'+b['path']})
    (root/'MANIFEST.json').write_bytes(encoded({'id':'COMPANION-LIFE-10-CONFERENCE-01-MANIFEST','candidate':info(out),'sources':frozen,'sourceCount':len(frozen),'completeOriginalProcedures':10,'originalCases':20,'designQuestions':16,'newCurrentVectorsSubmitted':0}))
    (root/'LOCAL_PREFLIGHT.json').write_bytes(encoded({'checks':checks,'checkCount':len(checks),'failureCount':0,'runtimeTestsExecuted':0,'scope':'Source, full original-record and exact frozen-file checks. New current cases intentionally withheld for accepted occupied-space validation.'}))
    (root/'README.md').write_text('''# Ten companion and life sources: decisions before new systemic authorship

This is the source-conference stage required before creating substantial new rules. Read all ten complete earlier proposals, all original shared context and twenty exact original scenario obligations. Resolve sixteen genuine design forks using the preserved sources and current accepted interfaces. No new current vector is submitted or claimed proved. The source-generating script retains unfinished case work after an unconditional return; it is not part of the submitted candidate or evidence of execution.

The actual persistent20 review exposed insufficient occupied spaces in named class fixtures. Accepted Small/Medium5x5ft spaces remain authoritative. New case development is held for complete geometry/attack/timing reconciliation; historical examples remain exact. Source promises, original access, distinct companion lifecycles, physical corpse identity, real gear and all four Create Undead alternatives must remain intact. A source-only bestiary record is not an operative creature profile or a made-up CR.

Return source-linked dispositions for each question and each original proposal, complete replacement rule text where needed, and a precise case-development checklist. Classify example defects separately from genuine procedure changes. Discuss Soulburn3-versus5RP and negative undiscounted yield, Grave Gift direct recovery, each suppression lifecycle, death/body claims, Wraith lifetap/path geometry, permanent Command Undeath, accumulating permanent Create Undead bodies, and the physical Homunculus task/repair profile. Do not reopen accepted pricing, command budgets, Ready, Null, death, healing, crafting or antimagic interfaces without an actual contradiction.

Provide input/output hashes and actual review scope in a downloadable archive. This is not exact operating-candidate acceptance, promotion, runtime, numerical balance, cosmology, whole-game or release approval. No new soul or world-history inference is permitted. Current480 reviewed/368 pending and all75 domain gates remain distinct.
''',encoding='utf-8')
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(root.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(root).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert len(z.namelist())==len(set(z.namelist()))==len(frozen)+3
        for b in frozen:
            raw=z.read(b['archivePath'])
            assert len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256']
    b=info(archive)
    requestp.write_text(f"Please conduct a pre-authorship design conference for ten companion/life sources using DD_Companion_Life_10_Conference_01.zip ({b['bytes']} bytes; SHA-256 {b['sha256']}). All {len(frozen)} full source files are frozen and verified. Read the10 complete original procedures and20 preserved scenario obligations, then resolve all16 genuine questions. This stage asks for actual choices before substantial new systemic authorship, not exact acceptance of a finished current candidate. New current vectors are intentionally withheld while I repair the accepted5x5ft occupied-space issue you found; the original scenarios remain preserved and their missing source/geometry prerequisites explicit. Return complete source-linked rule corrections, dispositions and case-development requirements in a downloadable archive. Preserve actual source access, all four Create Undead alternatives, distinct suppression/lifecycle rules, real body/gear histories and video-game-only development. Do not infer cosmology or reopen accepted interfaces by analogy. Counts480/368 and75 distinct domain gates stay unchanged.\n",encoding='utf-8')
    prep.write_bytes(encoded({'archive':b,'candidate':info(out),'manifest':info(root/'MANIFEST.json'),'localPreflight':info(root/'LOCAL_PREFLIGHT.json'),'request':info(requestp),'sources':len(frozen),'checkCount':len(checks),'allArchiveSourceHashesVerified':True,'newCurrentVectorsSubmitted':0,'submitted':False,'newRuleAdoptions':0,'runtimeTestsExecuted':0}))
    print(json.dumps({'archive':b,'candidate':info(out),'sources':len(frozen),'checks':len(checks),'originalProcedures':10,'originalCases':20,'questions':16,'newCurrentVectorsSubmitted':0}))
    return

    # Unsubmitted partial vector work remains below as preserved development
    # history. It must be reconstructed with accepted occupied spaces before use.
    def v(case_id, qids, initial, operation, expected, gaps, actor_class='Wizard', rp=None, hp=None):
        old = next(h for h in audit['all20HistoricalScenarioTexts'] if h['id'] == case_id)
        ident = old['spellId']
        access = by_id[ident]['completeCurrentCatalogSourceAndAccess']['classAccess'][actor_class]
        level, rank, cost = access['minimumClassLevel'], access['rank'], access['baseRpCost']
        classdoc = wizard if actor_class == 'Wizard' else cleric
        maximum = classdoc['rpByClassLevel'][level - 1]
        before = maximum if rp is None else rp
        pb = 2 + (level - 1)//4
        actor = {'class': actor_class, 'level': level, 'classSource': info(wp if actor_class == 'Wizard' else clp),
                 'castingAbility': 'INT' if actor_class == 'Wizard' else 'WIS', 'castingAbilityScore': 18,
                 'CON': 14, 'DEX': 14, 'PB': pb, 'spellDC': 8+pb+4, 'spellAttack': pb+4,
                 'actualAccess': deepcopy(access), 'knownOrPreparedSpell': ident,
                 'generatingRank': rank, 'RPMaximum': maximum, 'RPBefore': before,
                 'baseAndFinalCost': cost, 'RPAfterCommitIfEligible': before-cost,
                 'DissonanceBefore': 0, 'DissonanceAfterCommitIfEligible': 0 if actor_class=='Wizard' else (2 if rank>=6 else 1),
                 'RefrainExtra': 0, 'actualRequirements': 'Genuinely acquired at a legal source level, prepared where required; first distinct spell/matrix, actual owned usable focus and voice/hands, available Action, no cost modification, no nonproficient armor. This vector grants no missing target or profile.'}
        if actor_class == 'Wizard':
            actor.update({'specialization':'Abjuration','HPMaximum':8+6*(level-1),'normalHPBefore':8+6*(level-1) if hp is None else hp})
        vectors.append({'id':case_id,'spellId':ident,'originalTextUnchanged':old['exactOriginalText'],
                        'originalSource':{'source':old['source'],'pointer':old['pointer']},'sourceActor':actor,
                        'questionIds':qids,'initialState':initial,'operation':operation,
                        'expectedIfProposalAgreed':expected,'unresolvedPremises':gaps,
                        'status':'Conditional design comparison; complete original scenario preserved, no operative adoption or runtime execution.'})
        ck('Actual class rank/RP bounds: '+case_id, classdoc['maxSpellRankByClassLevel'][level-1]>=rank and 0<=before<=maximum)
        ck('Actual DC and quote: '+case_id, actor['spellDC']==8+pb+4 and actor['RPAfterCommitIfEligible']==before-cost)

    v('IN4-07-A',['CL10-Q01','CL10-Q02'],
      {'casterCenter':[0,0,1],'golemCreationCenter':[10,0,5],'golemHalfExtents':[2,2,5],
       'recipient':{'class':'Wizard','level':9,'DEX':14,'CON':14,'HP':56,'AC':12,'center':[18,0,1],'halfExtents':[1,1,1],'Wounds':0,'tempHP':0},
       'attackFace':12,'attackModifier':7,'damageD10Faces':[6,7]},
      'At t0 cast; during the same actual regular turn use its genuinely available BA command. Attached phase t2 moves the Golem center to[12,0,5], then resolves one Slam if this proposed creation-round command is agreed.',
      {'commandSpent':1,'offenseSpent':1,'movementFt':2,'nearestBodyGapFt':3,'attackTotal':19,'damage':13,'recipientHPAfter':43,'WoundCheck':False,'sameRoundSlowAuraOrOtherDeviceOffense':False,'concentrationDeadline':60},
      'The Golem profile/creation-round permission are pending. This target/body geometry is a declared class-based fixture, not an actual runtime execution; no extra device attack exists merely to be denied.')
    v('IN4-07-B',['CL10-Q01'],
      {'golemCenter':[12,0,5],'recipientCenter':[18,0,1],'recipientHalfExtents':[1,1,1],
       'recipient':'Same actual Wizard9 from A, ordinary Speed30, CON14 untrained save+2, no other Speed/control effects.',
       'CONSave':{'face':10,'modifier':2,'total':12,'DC':15},'auraCreatedAt':7,'nextOriginalOwnerStart':12},
      'On the next actual owner turn t6 spend one BA/offense for Slow Aura, operative in attached phase t7. During recipient turn t8 move center18→23→18 along X, with actual Speed budget and clear ground.',
      {'failedCON':True,'insideSpeed':15,'outsideSpeed':30,'totalPathFt':10,'outsideNearestDistanceSquared':109,'radiusSquared':100,'sameActivationReentrySaveCount':0,'reentrySpeed':15,'hardDenialClaimed':False,'endsAt':12},
      'The old application must still exist and concentration remain legal. Only this proposed field effect is toggled by exit/reentry; the spell grants no movement refund or automatic known-enemy classification.')
    v('IN4-10-A',['CL10-Q03','CL10-Q04'],
      {'normalHP':31,'RP':12,'unusedProposedLongRestUse':True,
       'counterAlternative':{'class':'Wizard','level':2,'INT':16,'PB':2,'RPBefore':6,'cost':3,'RPAfter':3,'automaticSource':'wizard.base.counterspell','rangeFt':30,'checkFace':13,'checkModifier':5,'total':18,'DC':18,'firstDistinctClassMatrixDissonance':0}},
      'Commit actual7RP and proposed20 normalHP payment, plus the proposed use. In the separate countered branch, an actual capable Wizard2 perceives the cast within60ft, spends its real Reaction and automatic Counterspell cost; recharge2 becomes spent.',
      {'RPAtCommit':5,'HPAtCommit':11,'successful3RPRecoveryFinalRP':8,'netRPChange':-4,'counteredRP':5,'counteredHP':11,'costRefund':False},
      '3RP versus5RP and frequency are not yet chosen. The alternative Counterspell event is sourced, not presumed to occur in the successful branch; no genuine discount/waiver is present.',rp=12,hp=31)
    v('IN4-10-B',['CL10-Q03','CL10-Q04'],
      {'alternativeInitialStates':[{'RP':6,'normalHP':31},{'RP':12,'normalHP':20}], 'tempHP':'Any actual buffer cannot pay a normalHP cost.'},
      'Preflight each separate starting state against actual quoted7RP and proposed20 normalHP with positive remainingHP.',
      {'eitherStateCanCommit':False,'ActionSpentByRejectedPreflight':False,'useSpentByRejectedPreflight':False,'tempHPUsedAsPayment':False,'actualPriceWaiverWouldRemoveHPCost':False},
      'No price-waiver source is granted. The waiver statement remains a conditional scope comparison, not a demonstrated free cast.',rp=6,hp=31)
    v('NE5-01-A',['CL10-Q05','CL10-Q02'],
      {'casterCenter':[0,0,1],'knightCenter':[20,0,1],'knightHalfExtents':[1,1,1],
       'target':{'class':'Wizard','level':9,'DEX':14,'CON':14,'AC':12,'HP':56,'center':[24,0,1],'halfExtents':[1,1,1]},
       'attackFace':11,'spellAttack':8,'damageD10Faces':[6,7]},
      'Create the proposed Knight; during a real eligible later owner turn pay one BA command and resolve its single attack only in the actual attached phase.',
      {'startingKnightHP':80,'attackTotal':19,'damageNecrotic':13,'targetHPAfter':43,'otherSkeletonOffenseAllowed':False,'extraSlashingOrFear':False},
      'No Conjuration specialization is present, so the fixed proposed base80 is not silently boosted. Exact later cast-to-command clock is within the original60sec and must be retained; the attack/profile itself remains pending.')
    v('NE5-01-B',['CL10-Q02','CL10-Q05'],
      {'knightCurrentHP':50,'knightMaximumHP':80,'priorActualDamageLoss':30,'knightCenter':[20,0,1],'spellCreatedAt':0,'originalDeadline':60,
       'suppressor':{'class':'Wizard','level':9,'INT':18,'specialization':'Divination','RPBefore':32,'actualPreparedSpell':'antimagic-field-lesser','cost':10,'RPAfter':22,'DissonanceAfter':0,'center':[20,-8,1],'fieldCenter':[20,0,1],'fieldRadiusFt':10,'castTime':2,'voluntaryConcentrationEndTime':3}},
      'At t2 a separately lawful Lesser Antimagic cast targets its perceived center8ft away, intersecting the Knight body while its original caster at0 lies outside the field. At t3 that suppressor actually ends concentration.',
      {'knightBodyTemporarilyAbsentIfProposed':True,'borrowedLanternDropsAtActualKnightPosition':True,'intrinsicShadowSwordBecomesLoot':False,'HPOnLawfulResumption':50,'deadlineUnchanged':60,'corpseOnExpiry':False},
      'The30HP loss is declared existing state, not an invented attack. A real lantern/gear position and full local resumption/conflict rule still need the new lifecycle decision. This is an actual suppression-source comparison conditional on the Knight proposal.')
    v('NE5-04-A',['CL10-Q06','CL10-Q07'],
      {'donorHP':31,'recipient':{'class':'Wizard','level':7,'CON':14,'level1BaseDie':6,'laterD6HPRolls':[4,4,3,3,3,3],'maximumHP':40,'normalHP':0,'Wounds':3,'state':'Dying','deathSuccesses':0,'deathFailures':1,'willing':True,'center':[20,0,1]},'casterCenter':[0,0,1]},
      'Commit actual10RP and proposed floor(31/2)=15 normalHP payment. If direct recovery is adopted and unblocked, assign actual effective maximum once.',
      {'donorHPAfter':16,'recipientHPAfter':40,'recipientWoundsAfter':3,'CriticalRetained':True,'deathCountersAfter':[0,0],'ordinaryHealingCeiling39Applied':False,'RPRefundOrRefill':False},
      'The recipient maximum40 is now a lawful rolled-HP Wizard build rather than an unnamed maximum. Actual alive/willing state and no independent gain prohibition are starting facts; the bypass remains a new rule awaiting concurrence.',hp=31)
    v('NE5-04-B',['CL10-Q06','CL10-Q07'],
      {'donorHP':2,'recipient':'Same legal living0HP recipient as A; separate branch assumes a genuinely operative broad cannot-regain-HP source.',
       'proposedStabilizationRNG':{'die':'d4','face':2},'applicationTime':100,'alreadyStableAlternativeDeadline':4000},
      'Commit10RP and1 normalHP. Under the proposed independent stabilization, a Dying recipient gets one deadline; an already Stable recipient keeps its old deadline.',
      {'donorHPAfter':1,'recipientHPAfter':0,'DyingBranchBecomesStable':True,'DyingBranchRecoveryTime':7300,'alreadyStableDeadlineRetained':4000,'costRefund':False,'donorHP1Eligible':False,'deadRecipientResurrected':False},
      'Broad prohibition is conditional until an actual eligible source and full timing are bound; no invented condition is granted. The d4 is the ordinary Stable deadline RNG, not an added public Fate presentation.',hp=2)
    v('NE5-07-A',['CL10-Q08','CL10-Q09'],
      {'casterCenter':[0,0,1],'target':{'class':'Wizard','level':1,'actualType':'Humanoid','size':'Medium','CON':14,'HP':8,'maximumHP':8,'tempHP':0,'Wounds':0,'center':[20,0,1],'halfExtents':[1,1,1]},
       'CONSave':{'face':8,'modifier':2,'total':10,'DC':16},'damageD12Faces':[8,8,7,7,7],'bodyProvenance':'Actual previously living non-summoned/non-copied/not-previously-raised Humanoid; surviving whole corpse, real belt pouch and legal original space; no actual survival/resurrection response.'},
      'Resolve proposed one CON full/half Flood packet, then actual life state and only its qualifying original-body claim.',
      {'damage':37,'instantDeathComparison':{'postTempMinusPreHP':29,'maximumHP':8},'actuallyDead':True,'WoundSaves':0,'zombiesCreatedIfProposalAgreed':1,'zombieBaseHP':20,'creationRoundActs':0,'sameBeltPouchAndConsumedBody':True,'AutoRaiseAutomaticallyGranted':False},
      'The Humanoid classification/body completeness are explicit actual starting facts, not inferred solely from Wizard. The source-specific zombie profile and claim timing await concurrence.')
    v('NE5-07-B',['CL10-Q09'],
      {'recipient':{'class':'Wizard','level':9,'CON':14,'HPBefore':20,'maximumHP':56,'tempHP':0,'WoundsBefore':0},'damageAfterFailedSave':37,
       'WoundSave':{'face':18,'modifier':2,'total':20,'DC':18}},
      'Use the same actual Flood source and dice from A against this distinct legal starting recipient; finalize surviving positive-to-zero state before any corpse claim.',
      {'instantDeath':False,'postTempMinusPreHP':17,'WoundSaveSuccess':True,'WoundsAfter':0,'HPAfter':0,'stateAfter':'Dying','deathCounters':[0,0],'zombiesCreated':0,
       'conditionalOtherBranches':'An actual eligible survival/resurrection response preventing or undoing final death before this claim supplies no corpse; later death-save death does not retroactively qualify. A genuinely competing reserved body cannot be consumed twice.'},
      'No generic immediate resurrection, Ward or Auto-Raise ability is fabricated. Those preserved original alternative obligations still require their actual source trigger/cost/checkpoint; Flood alone does not create a standard-minion Auto-Raise reservation.')

    # Remaining ten scenario comparisons and frozen package are added below.


if __name__ == '__main__':
    main()
