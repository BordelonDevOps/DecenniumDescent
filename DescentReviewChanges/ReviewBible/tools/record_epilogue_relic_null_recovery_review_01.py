"""Record recovered GPT bytes and semantic review; adopt no proposed game rules."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import ast, difflib, hashlib, json, subprocess, sys
from apply_di7_ap_as_01 import G, R, A, info, encoded

def read(p): return json.loads(p.read_bytes())

def main():
    now = datetime.now(timezone.utc).isoformat()
    root = A / 'cosmology-epilogue-relic-null-01-return'
    packet = A / 'cosmology-epilogue-relic-null-01'
    archive = A / 'DD_Cosmology_Epilogue_Relic_Null_01_Return_01.zip'
    audit = A / 'COSMOLOGY_EPILOGUE_RELIC_NULL_01_SEMANTIC_REVIEW_01.json'
    report = A / 'COSMOLOGY_EPILOGUE_RELIC_NULL_01_SEMANTIC_REVIEW_01.md'
    request = A / 'COSMOLOGY_EPILOGUE_RELIC_NULL_02_REVISION_REQUEST.txt'
    target = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_RELIC_NULL_RECOVERY_01.json'
    delta = A / 'RELIC_NULL_RECOVERY_01_NAVIGATION_DELTA.json'
    preserved = A / 'navigation-before-relic-null-recovery-01'
    assert all(not p.exists() for p in [audit, report, request, target, delta, preserved])
    assert archive.stat().st_size == 70386
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == '24eeecec44d1ed248e96adf1d58b80b5c7f8434a3fdb487bdf7443c272de4699'
    checked = A / 'COSMOLOGY_EPILOGUE_RELIC_NULL_01_RETURN_SOURCE_CHECK_01.json'
    checks = read(checked)
    assert checks['checkCount'] == 234 and checks['failureCount'] == 0 and checks['sourceIntegrityOnly']
    model = read(root / 'RELIC_NULL_MODEL.json')
    cases = read(root / 'CASEBOOK.json')
    register = read(root / 'REGISTER.json')
    assert len(model['relics']) == 4 and len(model['chambers']) == 12 and len(model['flora']) == 4
    assert len(cases['cases']) == 47 and len({c['id'] for c in cases['cases']}) == 47
    return_files = [info(p) for p in sorted(root.iterdir()) if p.is_file()]
    frozen = read(packet / 'SOURCE_BINDINGS.json')
    current = [info(G / x['path']) for x in frozen]
    drift = []
    for old, new in zip(frozen, current):
        if old != new:
            before = (packet / 'sources' / old['path']).read_text(encoding='utf-8').splitlines()
            after = (G / old['path']).read_text(encoding='utf-8').splitlines()
            drift.append({'frozen': old, 'currentBeforeThisNavigationUpdate': new,
                          'diff': '\n'.join(difflib.unified_diff(before, after, fromfile='frozen', tofile='current'))})
    guide = R / 'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md'
    assert len(drift) == 1 and drift[0]['frozen']['path'] == guide.relative_to(G).as_posix()
    # The exact diff was read: additions are recovery status and later unadopted arc navigation.
    drift[0]['assessment'] = 'Navigation/status additions only; no original cosmology or adopted mechanic changed. Frozen and current guide are both preserved.'

    findings = []
    def add(n, title, pointers, problem, proposed, situations):
        ident = f'RNX-{n:02}'
        findings.append({'id': ident, 'title': title, 'status': 'OPEN; actual GPT correction required',
          'modelPointers': pointers, 'finding': problem, 'proposedRevisionForDiscussionOnly': proposed,
          'requiredSituations': [{'id': f'{ident}-{chr(65+i)}', 'scenario': v, 'status': 'requested; not executed or approved'} for i, v in enumerate(situations)]})

    add(1, 'The only flora visit is too short to harvest the antidote ingredients',
        ['/chambers/10/procedures', '/chambers/10/destinations/Veiled Expanse', '/flora', '/antidote'],
        'CH11 allows one Veiled Expanse card and exactly 10 minutes; return precedes same-timestamp local events. Bittersap recognition takes 10 minutes and harvesting takes another 20. Even preidentified Bittersap needs 20 minutes. Echo Lily recognition plus harvest takes 20 minutes; even a harvest begun immediately completes exactly when priority return removes the harvester. RN-F01 and RN-F02 assume 30/20 uninterrupted minutes without a lawful access route; RN-C11 does not demonstrate acquisition. This prevents the provided finite source from supplying its advertised antidote.',
        'Keep the brief one-use swap. Prefer an explicit NEW method to lift whole finite planting containers inside the visit, with actual Action, dimensions, mass, hands/carry and transport permissions, then identify and harvest the same depleted node identities outside. Alternatively propose a different finite access procedure and reconcile the original brief-swap premise. Do not silently extend time, grant another card, invent preexisting ingredients or add generic plane travel. Preserve every harvest/spoilage rule and write an end-to-end stock/time example.',
        ['Fresh party acquires two Bittersap parts and one Echo Lily through actual finite access, plus Bastion water, then completes a legal batch with all time, carrying and consumed stock shown.',
         'An unfinished harvest at the exact return time produces no ingredient unless the revised procedure explicitly authorizes it; failed/critical-failed harvests and lost containers cannot respawn nodes or adjacent plants.'])
    add(2, 'Null damage disagrees about an already-dying target and death counters',
        ['/null/veil/damageNonlethal/livingCreature', '/null/veil/damageNonlethal/preexisting'],
        'The model makes an already-dying recipient Stable, while also saying old death failures are not undone. Core says becoming Stable resets both counters. The player chapter says prior failures are not erased and does not tell the reader that an already-dying recipient becomes Stable. RN-N05 covers already-Stable, not already-dying. The same hit therefore has incompatible outcomes across the model, chapter and Core.',
        'Prefer no unsolicited stabilization of an already-dying recipient: the qualifying packet adds no damage-caused death failure and leaves its existing dying/counter/deadline state unchanged. Newly reduced living recipients may use the explicitly NEW Stable conversion and normal counter reset. If GPT instead recommends stabilizing already-dying targets, state that override honestly, clear counters under Core, and revise every view and case. Preserve old Wounds and actual death history in either choice.',
        ['Dying HP0 with two failures receives qualifying positive damage: print HP, dying/Stable, both counters and recovery deadline, identically in model and player/Director prose.',
         'Already-Stable HP0 receives qualifying damage with an existing absolute recovery time: no duplicate roll or later deadline; separately resolve newly-zero and fully-temp-absorbed damage.'])
    add(3, 'The broad Null override needs actual companion and zero-HP feature branches',
        ['/null/veil/damageNonlethal', '/actorProfiles'],
        'Living/nonliving prose does not settle every current source-specific zero lifecycle. Ranger beast immediate death, Mage asset destruction/token return, disappearance or duration expiry, and local projections are distinct. Declaring a generic Disabled state is not enough to tell whether a projection with no repair rule persists at zero or whether a separate timed expiry still removes it. Unconditional Unconscious language also needs an explicit interaction with Undying Spellform. Exact would-die protections must not spend a use when this override prevents the death trigger.',
        'Add an explicit recipient/lifecycle table bound to CREATURE_LIFECYCLE_PLAYTEST and HEALING_DEATH_PLAYTEST. Identify which damage-caused zero/death transitions are replaced, which independent expiry/sacrifice rules remain, and what restores each Disabled actor. Preserve actual class-specific zero-state permissions unless an expressly agreed NEW exception changes them. Do not derive nonliving anatomy from a name alone.',
        ['Resolve qualifying damage separately against a Ranger beast, a Mage asset and a local projection, including a later independent source expiry and actual legal recovery.',
         'Resolve a would-die ward and Undying Spellform on the same qualifying damage event; show whether any use is spent, remaining actions and concentration without replaying skipped death branches.'])
    add(4, 'Shrug durations lack a transition between initiative and elapsed time',
        ['/null/veil/shrug'],
        'Failure lasts through the end of the next regular turn in initiative but one minute outside it. Success uses next regular start versus six seconds. The draft never states what happens when initiative begins or ends during either effect. Switching modes can otherwise shorten, restart or leave the effect without a future marker.',
        'Choose one explicit clock conversion or absolute deadline rule, retaining the agreed source duration interpretation. Starting/ending initiative and extra turns cannot refresh, erase or duplicate the duration. This is a proposed clarification, not an adoption of the unrelated environment draft.',
        ['A failed shrug outside initiative has run for 59 seconds when combat starts: state its exact remaining duration and whether the first turn may act.',
         'A successful suppression starts during combat and combat ends before the next regular start: show the exact expiration and the flag of both an old delayed root and a newly created root.'])
    add(5, 'The Silence Wraith loses the manuscript heartbeat sense',
        ['/chambers/2', '/actorProfiles/ACT-SILENCE-WRAITH'],
        'Original P309 explicitly says the Wraith hunts by feeling heartbeat vibrations. The return substitutes floor movement pulses and a Stillness Action. A motionless living body still has its heartbeat; the source-to-procedure change is consequential and is not explained by the proposed counterplay. The seven 5-ft plates also lack a complete layout in the 35-by-35 room.',
        'Retain heartbeat as the actual signal and explicitly define range, intervening surfaces, moving/still bodies, floating bodies and genuinely heartbeat-free anatomy. Author finite counterplay without pretending that stillness ends a heartbeat. If movement-only sensing is a deliberate alternative, record it as a source departure for joint decision. Provide the numbered plate layout and a reachable sequence.',
        ['A motionless breathing character and an actually heartbeat-free creature stand on the same plate: establish detection from their real anatomy, without inventing universal type immunities.',
         'Walk the 1-3-5-7 solution using mapped plates, actual travel distances, Actions and active Wraith turns; show that the ten-minute investigation has a safe executable place or an actual risk.'])
    add(6, 'Acoustic silence needs the current spell and communication interfaces',
        ['/chambers/2', '/actorProfiles/ACT-SILENCE-WRAITH/actions'],
        'The chamber says sound does not carry/absolute acoustic silence, but does not specify verbal casting, audible Bard use, sound-dependent commands, spoken comfort or the boundary of silence. SPELL_INTEGRATION_RULES requires audible speech for V. The 47 cases do not resolve any of those interactions.',
        'Give the exact acoustic footprint and distinguish voice production, transmission, hearing and explicitly blocked verbal casting. Apply existing language/sign/writing and actual class cards. Do not turn the chamber into a general antimagic effect or grant comprehension without a language.',
        ['Try an actual V spell, an actual audible class feature and a signed/written communication inside the room; cite their real component/scope rules.',
         'One speaker is outside and one target is inside the threshold; resolve sound and legal communication at the boundary, plus Hush Claw speech loss independently.'])
    add(7, 'Tessellation has no fixed safe-path map or check cost',
        ['/chambers/3'],
        'Three rows of three paths are described, but the safe path per row, catch-net positions, height, return route and timing/action cost of reading are absent. The case assumes a failed read and an unsafe choice without a stored actual map. Fixed pattern persistence cannot be enforced until the pattern exists.',
        'Supply one finite scene map with coordinates, heights, safe choices and catch-net retrieval. Set the read action/time and check repetition rule. Keep the original creativity route and actual flight/rope/teleport permissions, without free generic traversal abilities.',
        ['Two characters read and traverse the same fixed row at different times; earlier observation remains correct unless an explicit mapped change occurs.',
         'A failed save lands on the actual net, then the character gets back to a legal path with explicit distance, action/time and any real support equipment.'])
    add(8, 'Ladder movement and safety-cable procedures are incomplete',
        ['/chambers/5'],
        'Each 15-ft segment costs an Action but does not state its movement cost or whether the Action moves the climber. Failure catches the climber five feet below segment start, including a first segment starting at the bottom ledge; attachment, width, support capacity and the route back from the catch are unspecified. The steadying Wisdom save also has no clear action or timing cost.',
        'Define shaft/ledge/cable coordinates and capacities, attachment and recovery, then reconcile the Action check with current climbing and the shared movement ledger. Make the fear-steadying opportunity finite and costed. Specify the bottom-segment catch without an invented below-floor space.',
        ['A burdened climber with known remaining movement tries a 15-ft segment; print both Action and movement expenditure, including ally assistance.',
         'Fail the first and third segments separately with actual cable attachment and capacity; show catch position, damage and return route without an extra free ascent.'])
    add(9, 'Shardpool emergency return can still target occupied or impossible space',
        ['/chambers/10/procedures', '/chambers/10/geometry'],
        'The final fallback sends travelers to a fixed 20-by-20 emergency pad regardless of obstruction, but the pad location/height and reservation are not authored. A blocked pad, enlarged traveler, separated traveler, carried creature or return of only some travelers has no outcome. Initial destination fit alone does not ensure return fit ten minutes later.',
        'Map and protect/reserve an actual return volume or define an explicit bounded waiting/recovery rule when every legal space is blocked. Recheck real footprints/heights and carried bodies, and state simultaneous/partial return ordering and attachment of eligible gear. Never silently overlap solid bodies, duplicate passengers or add an unlimited escape portal.',
        ['Block the original footprints, nearest legal alternatives and the emergency pad before both scheduled returns; print a legal nonduplicating terminal/waiting state.',
         'A traveler enlarges, loses carried gear or carries another creature during the visit; resolve actual return eligibility, fitting, custody and each consumed card once.'])
    add(10, 'Mirror repair names a Sentinel without supplying the side scene',
        ['/relics/2/reformation', '/chambers/11', '/actorProfiles'],
        'The relic requires a Glass-Mender Sentinel side scene attached to CH12. No such actor/scene is among the seven actor profiles or chamber procedures, and its location, access and discretion are undefined. Original P304 says reformation is at Sentinel discretion; the candidate promises automatic repair after two hours and three tabs. This needs a concrete bounded interpretation rather than a missing dependency.',
        'Author where and when the same Sentinel can be reached, its disposition and explicit grounds for accepting/refusing the finite repair. Preserve one mirror identity and finite three-tab stock; give tab mass/custody and an interrupted two-hour work rule. Label the narrowed one-repair limit and conditions as NEW, not recovered source text.',
        ['The mirror shatters after the party leaves CH12; demonstrate a real route back to the repair actor, the interaction and actual two-hour stock transaction.',
         'A tab is lost or the Sentinel refuses/interruption occurs; show remaining stock and a finite recovery/refusal outcome without creating a second mirror or resetting other Sentinel history.'])
    add(11, 'Twin Wind voting lacks token stock and one-vote identity rules',
        ['/chambers/8/procedures'],
        'The procedure refers to one finite decision token from the bowl, yet RN-C09 uses four votes. The token count, eligible voters, repeat placements, changing votes and retrieving tokens before/after commitment are unspecified. A finite majority cannot be determined consistently from the supplied inventory and identity rules.',
        'Use an explicit finite token stock or a recorded one-choice-per-eligible-traveler interface. Define eligibility and closing time, whether choices can change before closing, abstention, late arrivals and fixed tie order. Preserve the source-inspired local choice without creating another timeline or copied party.',
        ['Four eligible voters split two/two with sufficient real voting capacity: demonstrate the tie, fixed choice and single reward.',
         'One voter tries repeated deposits, a companion votes and a late arrival enters at the deadline: apply one stated eligibility/commitment rule with no ballot duplication.'])
    add(12, 'Local actor profiles leave combat and terminal states undefined',
        ['/actorProfiles', '/chambers/9/procedures'],
        'Several attacks omit reach, target count or attack kind; several fear effects say end of next turn without whose turn or outside-initiative duration. Feast Steward has HP40 but only cannot die/leaves when scene resolves, leaving its zero-HP outcome undefined. Crimson Arena does not settle simultaneous destruction of both projections; the favor mark grant condition appears in a case but not a clear success procedure. These are concrete gaps in the claimed self-contained profiles.',
        'Complete each local action/reaction envelope, exact fear source/end marker and zero/expiry lifecycle. Make source-specific senses and fixed passive scores explicit. Define duel simultaneous-zero terminal, favor grant/recipient and exit/reward timing. Do not promote the pending bestiary or copy player engines.',
        ['Run one complete initiative round with exact starts, positions, reach, targets, attack/save results, fear sources and end markers; resolve a zero-HP Feast Steward.',
         'One area packet reduces both duel projections to zero; state terminal result, gate opening, spear seal/availability and whether any Favor Mark is awarded.'])
    add(13, 'Pendant initial charge is not initialized',
        ['/relics/0/acquisition', '/relics/0/active', '/relics/0/transfer'],
        'The pendant has one charge and refresh/transfer rules, but discovery does not specify current charge. Every activation case simply assumes charge=1. A newly acquired physical item needs an actual initial state before its first use.',
        'Choose an explicit NEW initial charge for the unique reliquary item and state whether first bonding changes it. Preserve item-bound charge history, actual beneficial rest eligibility and no automatic refresh from transfer, loss or recovery. Add the initial state to scene stock and all relevant views.',
        ['Retrieve the actual unique pendant, finish its first bond and attempt its first consented cancellation before any beneficial Long Rest; derive readiness from the printed initial state.',
         'Spend the charge, transfer away and recover/rebond it: no new charge until the exact qualifying rest event, with both old and new bearer histories shown.'])
    add(14, 'The faint Null glow has no operational field boundary',
        ['/null/field', '/chambers/6', '/chambers/10/destinations/Veiled Expanse'],
        'The general rule requires an explicit boundary and stable field identity, while CH07 only names a faint/small Null glow. It never says whether that glow is an exposure field. The one-hour petition alcove might therefore cause an hourly check or be safe, depending on unstated geometry. The Veiled Expanse landing likewise does not explicitly distinguish its name from an active field. Generic Field A examples do not decide either actual scene.',
        'Declare each authored scene to contain a mapped field or no active field. If CH07 contains one, give exact radius/height, the alcove location, clock origin and overlap identity. Preserve field exposure versus Veil versus suppression/purge as distinct records. A realm name or visual glow alone must not add an unprinted field.',
        ['Carry out the actual CH07 consultation, meditation and petition through the real field map; process any due hourly save and blessing purge in one declared order.',
         'Enter, leave, rest and reenter that same field; track its partial exposure and Veil separately, and state explicitly whether the short Veiled Expanse visit adds exposure.'])

    accepted_boundaries = [
      'Original P302–316 statements and the after-Infinite-Yield heading are preserved as source evidence, separate from NEW operation.',
      'Campaign epoch, hidden identities and pending ordinary spells/bestiary remain unresolved; no catalog promotion is authorized by this audit.',
      'Finite item/card/ingredient identity and no-revisit-refill intent are useful; identified missing lifecycle details still need correction.',
      'Character-fiction/neutral-prompt consent routes are retained in the revision request; no real-player disclosure is needed.',
      'The special antidote remains separate from the 687 reviewed trade recipes.',
      'Creation-time delayed damage flags are explicitly labeled NEW in the return and covered by RN-N06; this audit does not silently replace that proposal.'
    ]
    record = {'id': 'COSMOLOGY-EPILOGUE-RELIC-NULL-SEMANTIC-REVIEW-01', 'recordedAtUtc': now,
      'status': 'Exact actual GPT return recovered; independent semantic review requires revision; NOT ADOPTED',
      'browserEvidence': {'browser': 'Chrome 3', 'tabId': '125746298', 'title': 'Calibration Review Continuation',
        'url': 'https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6ad1498d-f244-83ea-8ffe-63e75ff98073',
        'observedAlert': "You've hit your limit. Please try again later.",
        'download': 'Clicked the existing completed-return download button. Download-event watcher timed out, but the actual Downloads file was found and matched original size/hash exactly.',
        'latestTextRequestHasAssistantReply': False, 'newPromptSubmittedThisTurn': False,
        'interpretation': 'Browser reading and exact file recovery now work. The visible limit blocks the current review exchange; it is not evidence of source-file loss.'},
      'archive': info(archive), 'sourceIntegrityReceipt': info(checked), 'sourceIntegrityChecks': 234,
      'sourceIntegrityFailures': 0, 'returnedFiles': return_files, 'sourceCount': len(frozen),
      'currentSourceComparison': {'equal': 82, 'different': 1, 'differences': drift},
      'readScope': 'All model rules, all 47 authored cases, player chapter, register/source paragraphs, verdict and Director chapter model presentations/persistence/remaining boundaries. No gameplay execution.',
      'findings': findings, 'findingCount': len(findings), 'requiredSituationCount': sum(len(f['requiredSituations']) for f in findings),
      'preservedUsefulBoundaries': accepted_boundaries, 'nextReviewRequest': request.relative_to(G).as_posix(),
      'nextReviewRequestSubmitted': False, 'rulesApplied': False, 'newRulesAdopted': False,
      'sourceInformationDeleted': 0, 'runtimeTestsExecuted': 0, 'humanPlaytested': False,
      'numericalBalanceApproved': False, 'wholeGameFlowConfirmed': False, 'publicationApproved': False}
    assert len(findings) == 14 and record['requiredSituationCount'] == 28
    audit.write_bytes(encoded(record))
    lines = ['# EPI-08–14 recovered review: corrections required', '',
      'The exact completed GPT archive is now preserved locally: 70,386 bytes, SHA-256 `24eeecec44d1ed248e96adf1d58b80b5c7f8434a3fdb487bdf7443c272de4699`.', '',
      'All 234 file/source/citation checks pass. Of 83 frozen sources, 82 still match current files; the only changed file is the reader guide, whose added recovery status and unadopted arc links are preserved in the audit. These checks establish provenance, not playable correctness.', '',
      '**The returned module is not adopted.** Its four relics, twelve chambers, Null rules, four plants and 47 authored cases have 14 correction findings and 28 requested follow-up situations. Original source manuscripts and currently adopted mechanics remain unchanged.', '',
      'Chrome can read Part 3 and retrieve this archive. The chat currently displays “You\'ve hit your limit. Please try again later.” No duplicate prompt was sent. The correction request below is saved for the actual GPT discussion when replies resume.', '',
      '[Exact review data](COSMOLOGY_EPILOGUE_RELIC_NULL_01_SEMANTIC_REVIEW_01.json) · [Preserved archive](DD_Cosmology_Epilogue_Relic_Null_01_Return_01.zip) · [Source checks](COSMOLOGY_EPILOGUE_RELIC_NULL_01_RETURN_SOURCE_CHECK_01.json) · [Prepared revision request](COSMOLOGY_EPILOGUE_RELIC_NULL_02_REVISION_REQUEST.txt)', '']
    for f in findings:
        lines += [f"## {f['id']}: {f['title']}", '', f['finding'], '', '**Proposed correction for joint discussion:** '+f['proposedRevisionForDiscussionOnly'], '', '**Required follow-up situations:**', '']
        lines += [f"- {c['id']}: {c['scenario']}" for c in f['requiredSituations']]
        lines += ['']
    lines += ['## Boundaries to preserve', ''] + ['- '+v for v in accepted_boundaries]
    lines += ['', 'No runtime, human-playtest, balance, whole-game or publication gate is closed by this review. The later arc, consumable and environmental packets remain separate, unsubmitted proposals.', '']
    report.write_text('\n'.join(lines), encoding='utf-8', newline='\n')
    prompt = ['Decennium Descent — exact EPI-08–14 return recovered; semantic revision requested.',
      'This request is PREPARED ONLY until actually submitted. Codex retrieved your original 70,386-byte archive, SHA256 24eeecec44d1ed248e96adf1d58b80b5c7f8434a3fdb487bdf7443c272de4699. All 234 independent frozen source/output/citation checks pass. Your original eight files are preserved unchanged; no EPI08–14 rule has been applied.',
      'Please review these concrete findings against your existing exact return and its 83 frozen sources. 82 current sources match; only CURRENT_COSMOLOGY_READ_FIRST.md has later navigation/status additions, not rule changes. Do not regenerate the old archive or claim unseen environment/consumable/arcs drafts approved.',
      'For each RNX issue, explicitly agree, correct, or refute with exact source/rule evidence. Codex recommendations below are unadopted proposals. Return one complete corrected model, both complete playable chapters, REGISTER, all 47 earlier case IDs plus the 28 required scenarios (you may consolidate only with explicit ID mapping), SOURCE_HASHES, VERDICT and EVIDENCE_MANIFEST. Include precise changed-fields evidence and eight exact root files in DD_Cosmology_Epilogue_Relic_Null_02_Return.zip. Do not call it jointly approved until Codex has checked the revision and any further issues have been resolved.',
      'Keep source paragraphs, after-Infinite-Yield premise, owner epoch/identity holds, actual class/life rules, language access, finite inventory, one elapsed timeline and consent-safe character-fiction prompts. No human/runtime/balance/publication or general cosmology approval.', '']
    for f in findings:
        prompt += [f"{f['id']} — {f['title']}", f['finding'], 'Proposed discussion direction: '+f['proposedRevisionForDiscussionOnly']]
        prompt += [f"{c['id']}: {c['scenario']}" for c in f['requiredSituations']]
        prompt += ['']
    request.write_text('\n\n'.join(prompt), encoding='utf-8', newline='\n')

    previous = A / 'ACTIVE_AUTHORING_CHECKPOINT_AFTER_ENVIRONMENT_FOUNDATIONS_01.json'
    state = read(previous)
    start = G / 'START_HERE.md'; nav = R / 'tools/build_review_map.py'; ledger = R / 'data/playtest/game_development_coverage.json'
    originals = {}; saved = []
    for p in [start, guide, nav, ledger, G/'REVIEW_MAP.html', A/'REVIEW_MAP_BUILD.json']:
        raw = p.read_bytes(); out = preserved / p.relative_to(G); out.parent.mkdir(parents=True, exist_ok=True); out.write_bytes(raw)
        originals[p] = raw; saved.append({**info(p), 'preservedCopy': out.relative_to(G).as_posix()})
    (preserved/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    replacements = {}
    text = originals[start].decode()
    oldcheckpoint = previous.relative_to(G).as_posix(); newcheckpoint = target.relative_to(G).as_posix()
    assert text.count(oldcheckpoint) == 1
    text = text.replace(oldcheckpoint, newcheckpoint, 1)
    old = '**The archive is not yet retrieved or independently reviewed; those rules remain unadopted.** Chrome download access fails, and the native transfer attempt reports a system error.'
    new = '**The exact archive is now recovered and source-verified: 234 checks pass.** The [independent semantic review](docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_NULL_01_SEMANTIC_REVIEW_01.md) records14 correction findings and28 requested scenarios; those rules remain unadopted. Chrome reading/download works, while the chat currently displays a usage-limit alert. The [revision request](docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_NULL_02_REVISION_REQUEST.txt) is prepared, not submitted.'
    assert text.count(old) == 1; text = text.replace(old, new, 1)
    replacements[start] = [{'old':oldcheckpoint,'replacement':newcheckpoint},{'old':old,'replacement':new}]
    start.write_text(text, encoding='utf-8', newline='\n')
    text = originals[guide].decode()
    old = next(p for p in text.split('\n\n') if p.startswith('**Current recovery point:**'))
    new = '**Current recovery point:** The exact EPI-08–14 return is now [preserved locally](../../../../../docs/audit/2026-10-08/full-game/DD_Cosmology_Epilogue_Relic_Null_01_Return_01.zip), with the original 70,386-byte size and SHA256 verified. All234 [source/file/citation checks](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_NULL_01_RETURN_SOURCE_CHECK_01.json) pass. The [semantic audit](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_NULL_01_SEMANTIC_REVIEW_01.md) records14 correction findings and28 required follow-up situations, including flora acquisition time, Null stabilization conflicts and incomplete scene/lifecycle procedures. **No EPI-08–14 rule is adopted.** Chrome reading and download now work on actual Part3; the visible chat alert says the usage limit has been reached. The [saved revision request](../../../../../docs/audit/2026-10-08/full-game/COSMOLOGY_EPILOGUE_RELIC_NULL_02_REVISION_REQUEST.txt) has not been submitted. Preserve the existing source archive and all original return files.'
    assert text.count(old) == 1; text = text.replace(old, new, 1)
    replacements[guide] = [{'old':old,'replacement':new}]
    old2 = 'The live review is the same Part 3 conversation in Chrome 3/tab 125746268.'
    new2 = 'The review is the same Part3 conversation; the current readable Chrome3 tab is125746298 (Calibration Review Continuation), with a visible usage-limit alert.'
    assert text.count(old2) == 1; text = text.replace(old2,new2,1); replacements[guide].append({'old':old2,'replacement':new2})
    guide.write_text(text, encoding='utf-8', newline='\n')
    coverage = json.loads(originals[ledger]); before = deepcopy(coverage)
    row = next(x for x in coverage['aspects'] if x['id'] == 'DD-50'); oldrow = deepcopy(row)
    row['draftEvidence'].extend([audit.relative_to(G).as_posix(), checked.relative_to(G).as_posix(), request.relative_to(G).as_posix()])
    row.setdefault('currentEvidenceAddenda', []).append({'id':'epilogue-relic-null-recovery-review01','recordedAtUtc':now,
        'exactReturnRecovered':True,'sourceChecks':234,'sourceFailures':0,'semanticFindings':14,'requestedScenarios':28,
        'actualGptCorrectionPending':True,'revisionRequestSubmitted':False,'newRulesAdopted':False})
    for k in ['status','closure','humanEvidence','completionClass']: assert row[k] == oldrow[k]
    assert [x for x in coverage['aspects'] if x['id']!='DD-50'] == [x for x in before['aspects'] if x['id']!='DD-50']
    ledger.write_bytes(encoded(coverage))
    scope = 'EPI08–14 exact original return recovered:70,386bytes/hash verified;234 source/file/citation checks pass. Independent semantic audit:14 findings/28 requested situations, correction request prepared-not-submitted; module remains unadopted. Browser reading/download works; actual Part3 displays usage-limit alert, latest text request has no assistant reply. Environment7/59, consumables24/80 and arcs67 remain separate unsubmitted proposals. No original source, adopted rule or whole-game gate changed.'
    code = originals[nav].decode()
    tail = ' + read(A / "ENVIRONMENT_FOUNDATIONS_01_NAVIGATION_DELTA.json")["changes"]\n'
    assert code.count(tail) == 1
    code = code.replace(tail, tail.rstrip('\n')+' + read(A / "RELIC_NULL_RECOVERY_01_NAVIGATION_DELTA.json")["changes"]\n',1)
    nodes = [v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview']
    assert len(nodes)==1; code = code.replace(ast.get_source_segment(code,nodes[0]),repr(scope),1)
    items = [('EPI08–14 — recovered exact archive',archive.name),('EPI08–14 —234 source checks',checked.name),('EPI08–14 —semantic audit,14 correction findings',report.name),('EPI08–14 —prepared revision request, unsubmitted',request.name)]
    code = code.replace('    pending = [\n','    pending = [\n'+''.join('        '+repr(x)+',\n' for x in items),1)
    compile(code,str(nav),'exec'); nav.write_text(code,encoding='utf-8',newline='\n')
    changes = [{'before':next(x for x in saved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,guide,ledger,nav]]
    for change,p in zip(changes,[start,guide,ledger,nav]):
        if p in replacements: change['operations']=replacements[p]
        elif p==ledger:change['operations']=[{'aspectId':'DD-50','old':oldrow,'replacement':row}]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'newRulesAdopted':False,'fullDomainClosureChanged':False,'humanOrOwnerEvidenceChanged':False}))
    run = subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode: print(run.stdout[-1000:]); print(run.stderr[-2500:]); raise SystemExit(run.returncode)
    navigation = read(A/'REVIEW_MAP_BUILD.json'); assert not navigation['missingLinks']
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',
        previousGoalTurnClassification='progress',coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),
        newRuleAdoptions=0,newRuleAdoptionScope='Recovered original actual GPT bytes and recorded semantic corrections; no EPI08–14 rule adopted.',
        navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]})
    state['cosmologyEpilogueRelicNullRecoveryReview'] = {'audit':info(audit),'report':info(report),'sourceCheck':info(checked),'archive':info(archive),'revisionRequest':info(request),'semanticFindings':14,'requestedScenarios':28,'requestSubmitted':False,'moduleAdopted':False}
    state['latestActualGptBrowserEvidence'] = record['browserEvidence']
    state['activeGptReview'].update(recordedAtUtc=now,tabId='125746298',
        status='Exact return recovered and independently reviewed;14 correction findings remain. Saved revision request not submitted; visible GPT usage-limit alert.',
        verdictReceived=True,archiveRetrieved=True,independentReturnReviewComplete=True,
        semanticApproval=False,returnedArchive=info(archive),semanticReview=info(audit),
        consecutiveGoalTurnsWithObservationFailure=0,generationConfirmedLiveNow=False)
    state['cosmologyEpilogueRelicNullReview'].update(
        status='Actual original return recovered/source-verified; first semantic pass complete with14 findings; unadopted pending actual GPT correction.',
        returnedArchive=info(archive),sourceCheck=info(checked),semanticReview=info(audit),revisionRequest=info(request),revisionSubmitted=False)
    state['historicalNativeTransferEvidenceBeforeRecovery'] = state['latestActualGptTransferEvidence']
    state['latestActualGptTransferEvidence'] = info(audit)
    state['resumedBlockedAudit'] = {'resumedTurn':3,'previousConnectionBlockerChanged':True,
        'meaningfulProgress':'Fresh actual Chrome tab enabled exact archive recovery; all returned model rules and47 cases reviewed;14 revision findings recorded.',
        'currentExternalConstraint':'Visible GPT usage-limit alert prevents fresh replies; actual files and existing completed return are accessible.',
        'status':'active; meaningful source/semantic progress made, not a third consecutive no-progress turn'}
    state['historicalSafeNextActionsBeforeRecovery'] = state['safeNextActions']
    state['safeNextActions'] = ['Use the recovered exact EPI08–14 archive, not another export/recovery request. Its source check passes but the semantic audit requires14 corrections; do not adopt it yet.',
        'When actual GPT replies resume, send the saved RNX01–14 revision request in Part3 with the existing83 sources and exact original return. Do not claim it already submitted or duplicate the pending four-item text request.',
        'Keep environment/consumable/arc packets unadopted. Source/scene drafting may continue independently; final joint review remains necessary.']
    state.setdefault('preservationManifests',[]).append(info(preserved/'PRESERVATION_MANIFEST.json'))
    target.write_bytes(encoded(state))
    assert return_files == [info(p) for p in sorted(root.iterdir()) if p.is_file()]
    assert archive.stat().st_size == 70386
    for old in current:
        if old['path'] != guide.relative_to(G).as_posix():assert old == info(G/old['path'])
    print(json.dumps({'audit':info(audit),'report':info(report),'checkpoint':info(target),'findings':14,'requestedSituations':28,
        'sourceChecks':234,'sourceFailures':0,'navigationLinks':navigation['existingDistinctLinks'],'missingLinks':0,
        'allOriginalReturnFilesUnchanged':True,'newRulesAdopted':False,'requestSubmitted':False},ensure_ascii=False))

if __name__ == '__main__': main()
