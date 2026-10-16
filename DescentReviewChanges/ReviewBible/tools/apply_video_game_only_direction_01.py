"""Apply the owner's video-game-only direction to active navigation, preserving sources."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import ast, hashlib, json, re, subprocess, sys
from apply_di7_ap_as_01 import G, R, A, info, encoded

def read(p): return json.loads(p.read_bytes())

def main():
    now=datetime.now(timezone.utc).isoformat()
    attachment=Path(r'C:\Users\cbord\.codex\attachments\648011ef-dacb-416d-914d-45e18bcc1793\Pasted text.txt')
    directive=R/'docs/mechanics/VIDEO_GAME_ONLY_DIRECTIVE.md'
    guide=R/'docs/DEVELOPMENT_DIRECTION.md'
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_AC6_SEMANTIC_CURRENT_06_SUBMITTED.json'
    checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_VIDEO_GAME_ONLY_01.json'
    delta=A/'VIDEO_GAME_ONLY_01_NAVIGATION_DELTA.json'
    check=A/'VIDEO_GAME_ONLY_01_APPLICATION_CHECK.json'
    keep=A/'navigation-before-video-game-only-01'
    start=G/'START_HERE.md';ledger=R/'data/playtest/game_development_coverage.json'
    builder=R/'tools/build_review_map.py';template=R/'tools/review_map_template.html'
    registry=R/'data/director/spell_review/accepted_interface_registry_02.json'
    inventory=R/'data/director/spell_review/ordinary_spell_inventory_01.json'
    semantic=R/'data/director/spell_review/damage_control_25_semantic_delta_01.json'
    protocol=R/'docs/mechanics/SPELL_REVIEW_PROTOCOL.md'
    index=R/'data/public/spell_playtests/authored_review_index.json'
    observed=A/'VIDEO_GAME_ONLY_GPT_DIRECTION_BROWSER.txt'
    assert all(not p.exists() for p in [directive,guide,checkpoint,delta,check,keep])
    assert 'drop tabletop/TTRPG development as a project goal' in attachment.read_text(encoding='utf8')
    assert 'Decennium Descent should be treated as a video game ruleset only.' in observed.read_text(encoding='utf8')
    raw={};saved=[]
    for p in [start,ledger,builder,template,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        raw[p]=p.read_bytes();q=keep/p.relative_to(G);q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(raw[p])
        saved.append({**info(p),'preservedCopy':q.relative_to(G).as_posix()})
    manifest=keep/'PRESERVATION_MANIFEST.json';manifest.write_bytes(encoded(saved))
    protected=[protocol,registry,inventory,semantic,index,A/'AC5_EXACT_ACCEPTANCE_05_RECEIPT.json',A/'DD_AC6_Semantic_Current_06.zip',R/'data/director/spell_proposals/divination_enchantment_rank4_current_03.json',A/'DE4_FATE_GUARD_AMENDMENT_DRAFT_02.json']
    protected_before=[info(p) for p in protected]
    directive.write_bytes(attachment.read_bytes())
    objective='Build Decennium Descent into a deep, deterministic computer RPG whose complexity is handled by software rather than imposed on a tabletop group.'
    direction={
        'id':'owner-video-game-only-2026-10-16','effectiveDate':'2026-10-16','recordedAtUtc':now,
        'product':'video-game-only','objective':objective,'directive':info(directive),
        'actualGptAcknowledgment':info(observed),'activeGuide':guide.relative_to(G).as_posix(),
        'precedence':'Supersedes tabletop/TTRPG goals, manual adjudication deliverables, tabletop publication and campaign-playtest acceptance wording in older plans, the accelerated protocol and historical checkpoints. Compatible source-fidelity, review, preservation and scope requirements remain active.',
        'authoredAcceptance':'authored-video-game-rules-candidate',
        'retiredRequirements':['manual-tabletop-administerability','physical-dice-administration','GM-adjudication-teaching','paper-character-sheet-polish','tabletop-session-zero-production','tabletop-book-layout-and-publication'],
        'documentationPriority':['canonical-source','operative-engine-specification','data-schema','state-transitions','validation-cases','player-presentation'],
        'caseRequirements':['initialState','operation','deterministicInputsOrSeededRng','expectedIntermediateStates','expectedFinalState'],
        'separateUnclosedGates':['implementation','automated-runtime-tests','numerical-balance','human-gameplay-testing','cosmology-canon','whole-game-flow','release-approval'],
        'interfaceRegistry':info(registry),'interfacePolicy':'Reuse the exact accepted scope as an engine contract. Historical acceptance strings and authoritative files remain unchanged. Provisional and pending interfaces retain their status; no runtime, canon or wider-scope approval inferred.',
        'rngPolicy':'Dice notation denotes engine RNG. Preserve gameplay-relevant information visibility, selection probabilities and eligibility. Do not retain physical-die administration. Any missing digital decision is narrow NEW scoped authorship; substantial systemic changes require owner conference.',
        'timingAndGeometry':'Use exact engine events, snapshots, bodies, traces and intersections. Preserve accepted intentional turn/round or geometry abstractions; the direction change alone does not replace Ready, Falling, timing or targeting rules.',
        'preservation':'All existing tabletop documents, sources, identities, access/rank/school records, prior versions and frozen acceptance hashes remain evidence. No deletion or retroactive acceptance.',
        'scope':'All 75 tracked domains remain inventoried, with tabletop-only work retired and relevant content carried into digital development. This is a direction change, not completion of any domain.'
    }
    guide_text='''# Decennium Descent — active development direction

Effective 16 October 2026, Decennium Descent is a **video game only**. Tabletop/TTRPG development is retired by the owner. The [verbatim directive](mechanics/VIDEO_GAME_ONLY_DIRECTIVE.md) takes precedence over conflicting tabletop requirements in older plans and the [original accelerated review protocol](mechanics/SPELL_REVIEW_PROTOCOL.md). Both originals remain preserved.

Build a deep, deterministic computer RPG. The engine handles the bookkeeping; the player interface presents understandable choices and results. Retain complexity when it earns its place in gameplay.

## What work continues

Develop source-faithful engine specifications, data schemas, state transitions, deterministic test vectors and useful player descriptions. Preserve spell/class identity, access, rank, school, lore and source provenance. Each operation needs precise eligibility, geometry, timing, resource commitments, ownership, lifecycle and cleanup.

The [49-entry interface registry](../data/director/spell_review/accepted_interface_registry_02.json) is the current reuse index. Its exact source scopes and provisional/pending distinctions still govern. Existing accepted contracts remain usable; a tabletop heading or historical acceptance label does not invalidate their mechanics. Do not reopen them without a genuine contradiction or required narrow digital decision. This registry is documentation, not implemented engine code.

Dice notation denotes engine RNG. Preserve actual probabilities, eligibility and gameplay-relevant hidden information. Physical rolling and manual adjudication are no longer deliverables. Existing intentional turn/round abstractions remain rules until an explicit design decision changes them.

## What leaves the active backlog

Stop tabletop chapter polishing, physical-dice procedures, paper character-sheet production, manual GM teaching, table-contract publication and print-book layout. Preserve their current files as source/history. Reuse relevant material for digital onboarding, host permissions, encounter/content authoring, information visibility and gameplay testing.

The coverage ledger retains all 75 identities. Updated digital scope governs older issue text. Historical source work and review evidence remain valid within their original scope; no area becomes complete merely because its tabletop requirements are retired.

## Review workflow

1. Freeze source bindings and identify exact class/rank/access requirements.
2. Reuse accepted interfaces and assign risk tiers: routine 25–40, interaction-heavy 15–25, systemic 5–10 where safe.
3. Run source/hash and structure validation; identify genuine semantic differences.
4. Resolve only missing engine decisions. Label narrow additions **NEW scoped authorship** and confer before substantial new systemic rules.
5. Author complete engine behavior and test vectors with initial state, operation, deterministic inputs or seeded RNG, expected intermediate states and final state. Validate arithmetic and geometry where applicable.
6. Confer with the actual GPT notebook on exceptions and exact acceptance. Freeze accepted outputs and register their precise scopes.

Future acceptance means **authored video-game rules candidate**. It does not establish implementation, automated runtime tests, numerical balance, human gameplay testing, cosmology canon, whole-game completion or release approval.

## Current continuation

- Recorded ordinary-spell coverage remains **451 reviewed / 397 pending**, across 848 identities. The [inventory](../data/director/spell_review/ordinary_spell_inventory_01.json) preserves every pending identity. No spell is promoted by this direction change.
- AC6 Current06 was submitted once to the actual GPT notebook. Later notebook discussion describes AC6 as completed, but its exact Current06 acceptance artifact still needs recovery and verification before local adoption. Do not resend the package or count the 14 as adopted prematurely.
- The next [25-spell semantic delta](../data/director/spell_review/damage_control_25_semantic_delta_01.json) is prepared: 10 routine and 15 interaction-heavy spells. Its 1,349-check preflight verifies source/structure/accounting; it does not validate unwritten procedures, arithmetic, geometry or runtime behavior.
- DE4 current03 remains unadopted. Two identified test-fixture issues need correction: Phantasmal Killer uses an impossible same-class school combination, and Field Repair omits touch/recharge prerequisites. The separate Fate Reversal guard proposal remains pending; this directive does not approve its systemic extension.
- Continue the other digital game domains and final joint whole-game flow review. Cosmology retains its careful source/canon boundaries. Latest verified GitHub backup is `18c6e3a`; newer local work is not represented by that backup.

The [coverage ledger](../data/playtest/game_development_coverage.json), [owner start page](../../../START_HERE.md) and [current checkpoint](../../../docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_VIDEO_GAME_ONLY_01.json) carry this direction. Older checkpoints are historical where they conflict.
'''
    guide.write_text(guide_text,encoding='utf8',newline='\n')
    cov=json.loads(raw[ledger]);oldcov=deepcopy(cov)
    cov['objective']=objective
    cov['developmentDirection']=direction
    cov['completionPolicy']='All active work targets authored video-game rules candidates. Source audit, exact scoped semantic review and appropriate validation remain required. Manual tabletop operation, GM teaching and tabletop publication are retired requirements. Implementation, automated runtime tests, numerical balance, human digital gameplay testing, cosmology canon, whole-game flow and release approval are separate unclosed gates. No source, finite model check or direction change proves those gates complete.'
    cov['workingMethod']='Source → engine specification → data/schema → state transitions → deterministic test vectors → player presentation. Reuse accepted engine contracts, automate preflight and arithmetic/geometry checks, review semantic differences in risk-tiered cohorts, and confer with actual GPT over exceptions. Preserve all originals and histories.'
    cov['ownerDirectedSequencing'].append({'id':direction['id'],'evidence':directive.relative_to(G).as_posix(),'currentWork':'Video-game-only authored system development; retire tabletop-only deliverables immediately.','supersedes':'Conflicting tabletop goals and manual publication requirements in all previous directions.','retained':'Existing source-preservation, twelve-character expedition and host-permission direction; careful cosmology boundaries; actual GPT conference and verified delivery requirements.'})
    cov.setdefault('historyReferences',[]).append(manifest.relative_to(G).as_posix())
    cov['activeOrdinarySpellReview']={**cov['activeOrdinarySpellReview'],'recordedAtUtc':now,'ordinaryOperational':451,'ordinaryPending':397,'authoredIndex':info(index),'latestAcceptance':info(A/'AC5_EXACT_ACCEPTANCE_05_RECEIPT.json'),'scope':'Current authored counts verified from the 848-entry index; historical status strings preserved. Future acceptance is authored-video-game-rules-candidate. AC6 exact receipt remains unrecovered/unadopted.','runtimeVerified':False}
    maps={
      'DD-05':('Character state and data model','Source-faithful digital character state, choices, derived fields and persistence; existing paper records remain references.','Validate required state fields and transitions against sources; complete digital entry/update flows without losing choices or history.'),
      'DD-53':('Engine authority and content-author controls','Deterministic rule precedence, explicit uncertainty, hidden-information boundaries and permitted host/content-author controls.','No runtime outcome depends on unspecified GM fiat; any configurable decision has explicit authority, allowed values and transition behavior.'),
      'DD-54':('Hidden game data and player visibility','Separate internal world/creature/quest state from information the player is entitled to see.','Verify actual gameplay information boundaries in data, client/server behavior as applicable and player presentation; historical Director labels alone are not an implementation.'),
      'DD-55':('Adventure content and encounter authoring','Source-faithful adventure content, encounter inputs, triggers, objectives, rewards and state transitions.','Specify deterministic content progression and failure/recovery behavior; preserve narrative and source obligations without manual GM teaching deliverables.'),
      'DD-56':('Campaign progression and content orchestration','Source-faithful campaign sequencing, persistent consequences, branching, world clocks and completion states.','Resolve progression dependencies and state transitions; human GM campaign-planning instruction is retired.'),
      'DD-58':('Digital game setup and host permissions','Carry forward source-backed tone/content settings, character compatibility, PvP and host-configured human/AI permissions where relevant to digital play.','Specify digital setup choices and their permitted effects. Table attendance rules and physical session-zero publication are retired; new settings require source or explicit scoped authorship.'),
      'DD-60':('Digital onboarding and first-play flow','First character, first turn, first encounter, casting, rest, advancement and relevant player-facing explanations in the computer game.','Validate digital onboarding against operative rules; later human gameplay tests must demonstrate usable first-play flow. Paper worksheets and tabletop teaching package polish are retired.'),
      'DD-61':('In-game references and indexes','Searchable source-linked game data, tooltips, condition/rule references and accessible player presentation.','Resolve references and information visibility against current rules; printable reference-sheet production is retired.'),
      'DD-62':('Deterministic scenarios and test vectors','Initial state, operation, deterministic inputs or seeded RNG, expected intermediate states and final state for important interactions.','Machine-check meaningful arithmetic/geometry/state expectations where possible and distinguish authored vectors from executed engine tests.'),
      'DD-63':('Game-state persistence and rule parity','Persist characters, companions, resources, clocks, ownership, provenance and world state consistently with operative rules.','Verify save/load, interruption/resumption and state parity in actual implementation; authored checks alone do not close runtime coverage.'),
      'DD-65':('Digital build packaging and information boundaries','Game data, internal content tools, player assets, references, manifests and release packaging.','Verify selected digital build contents, valid references and gameplay information boundaries; no separate tabletop book release required.'),
      'DD-67':('Digital presentation and release structure','Useful in-game presentation, documentation and digital distribution structure.','Verify accessible player presentation and coherent digital delivery. Tabletop book layout, print pagination and manual publishing are retired.'),
      'DD-71':('Human digital gameplay testing','Base, Arch and Hero progression, mixed parties, new and experienced players and actual human/AI control combinations.','Record human computer-game sessions and resolve observed friction/ambiguity. Tabletop test sessions are no longer required.'),
      'DD-72':('Numerical balance and gameplay testing','Damage, survivability, healing, control, resource pacing, encounter difficulty and build diversity in the digital game.','Use relevant simulation and actual gameplay evidence for balance claims, separately from structural correctness; manual table evidence is not required.'),
      'DD-73':('Long-duration digital gameplay testing','Advancement, recovery, economy, crafting, Decennial cycle and persistent state over sustained computer-game play.','Validate the sustained digital progression loop and persistence, beyond isolated combats; no physical tabletop campaign requirement.')
    }
    for row in cov['aspects']:
        row['activeDirection']=direction['id']
        if row['id'] in maps:
            row['priorDirectionScope']={k:deepcopy(row[k]) for k in ['domain','requiredCoverage','acceptanceGate','openIssues']}
            row['domain'],row['requiredCoverage'],row['acceptanceGate']=maps[row['id']]
            row['openIssues']=['Complete the digital coverage and acceptance requirement above. Preserve and reuse applicable source findings and reviewed rules from the prior scope; tabletop-only production is retired.', 'Distinguish authored specification, software implementation, automated execution and human gameplay evidence. No gate is closed by this scope change.']
            if row['id']=='DD-54' or row['id']=='DD-65':
                row['openIssues'].append('Resolve the existing sealed-bestiary/client-data exposure and public-route findings using actual digital information policy; inventory alone is not proof of a deployed leak or a repaired boundary.')
            if row['id']=='DD-60':
                row['openIssues'].append('Reuse reviewed onboarding and the existing language/crafting/injury/companion source cases for digital flow. Retain the separately identified Recycling conflict; do not spend further effort polishing the nine-paper-artifact packet.')
        old=next(x for x in oldcov['aspects'] if x['id']==row['id'])
        assert all(row[k]==old[k] for k in ['status','closure','humanEvidence','completionClass','reviewEvidence','sourceEvidence','validationEvidence','draftEvidence'])
    ledger.write_bytes(encoded(cov))
    text=raw[start].decode('utf8')
    text=text.replace(previous.relative_to(G).as_posix(),checkpoint.relative_to(G).as_posix())
    banner='**Active direction — video game only (16 October 2026):** Tabletop/TTRPG development is retired. Read the [current development plan](DescentReviewChanges/ReviewBible/docs/DEVELOPMENT_DIRECTION.md) and [verbatim owner directive](DescentReviewChanges/ReviewBible/docs/mechanics/VIDEO_GAME_ONLY_DIRECTIVE.md). Future work targets engine specifications, data, state transitions and deterministic test vectors. Existing tabletop files remain source/history. This direction overrides conflicting tabletop requirements below and in older checkpoints. Actual GPT has already acknowledged the same direction.\n\n'
    text=text.replace('# Decennium Descent — start here\n\n','# Decennium Descent — start here\n\n'+banner,1)
    text=text.replace('All game acceptance gates remain unchanged.','The video-game-only direction below supersedes tabletop requirements; substantive review evidence and separate implementation, gameplay, balance and release gates remain.')
    text=text.replace('The finish line remains a coherent campaign-playtest candidate; final joint flow, human balance, publication approval and full companion implementation remain open.','The authored finish line is a coherent video-game rules candidate; final joint flow, implementation, automated runtime tests, human gameplay, balance and release approval remain separate open gates.')
    text=text.replace('GPT is reviewing it; exact acceptance and adoption remain open. No AC6 spell is adopted.','Later GPT notebook discussion describes AC6 as completed, but the exact Current06 acceptance artifact still needs recovery and verification before local adoption. No AC6 spell is adopted.')
    text=text.replace('**Next fifteen-spell group:**','**Preserved fifteen-spell proposal:**')
    text=text.replace('## Start reading or building a character','## Existing rules and source references')
    text=text.replace('**Player/Director delivery is still open.**','**Digital packaging and information boundaries remain open.** Tabletop publication is retired; the following audience inventory is preserved evidence.')
    oldrow='| Director procedures and adventure design |'
    text=text.replace(oldrow,'| Engine/content-author rules from Director sources |')
    insertion='**Accelerated digital spell review:** Reuse the [49-entry interface registry](DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_02.json). The [pending inventory](DescentReviewChanges/ReviewBible/data/director/spell_review/ordinary_spell_inventory_01.json) and [next 25-spell semantic delta](DescentReviewChanges/ReviewBible/data/director/spell_review/damage_control_25_semantic_delta_01.json) are prepared. The [1,349-check preflight](docs/audit/2026-10-08/full-game/accelerated-review-01/PREFLIGHT.json) has zero failures within its source/structure scope; new cohort procedures and test vectors are still to author.\n\n'
    text=text.replace('**Preserved fifteen-spell proposal:**',insertion+'**Preserved fifteen-spell proposal:**',1)
    start.write_text(text,encoding='utf8',newline='\n')
    code=raw[builder].decode('utf8')
    tail=' + read(A / "AC6_SEMANTIC_CURRENT_06_NAVIGATION_DELTA.json")["changes"]\n'
    assert code.count(tail)==1
    code=code.replace(tail,tail.rstrip('\n')+' + read(A / "VIDEO_GAME_ONLY_01_NAVIGATION_DELTA.json")["changes"]\n',1)
    code=code.replace('return "Director procedures"','return "Engine and content authoring"').replace('return "Teaching and reference"','return "Onboarding and reference"')
    code=code.replace('    featured = [\n','    featured = [\n'+''.join('        '+repr(x)+',\n' for x in [('Active video-game-only plan',guide.relative_to(G).as_posix()),('Owner directive — preserved verbatim',directive.relative_to(G).as_posix()),('Accepted interface registry',registry.relative_to(G).as_posix()),('Next 25-spell semantic delta',semantic.relative_to(G).as_posix())]),1)
    scope='Video-game-only development. All75 domains remain inventoried with digital scopes and retired tabletop-only requirements. 451 reviewed/397 pending ordinary spells;49 scoped interface records. AC6 exact Current06 acceptance artifact still needs recovery before adoption; DE4 and next25 remain pending. No implementation, runtime-test, balance, gameplay, canon, whole-game or release gate is closed by this change.'
    vals=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];assert len(vals)==1
    code=code.replace(ast.get_source_segment(code,vals[0]),repr(scope),1)
    compile(code,str(builder),'exec');builder.write_text(code,encoding='utf8',newline='\n')
    html=raw[template].decode('utf8')
    html=html.replace('Owner and Director workspace','Owner and development workspace')
    html=html.replace('This map includes Director material.','This map includes internal and historically Director-only material.')
    html=html.replace('<p id="position"></p>','<p class="sequence"><strong>Video game only:</strong> tabletop development is retired. Engine rules, data, state transitions, deterministic test vectors and player presentation are the active deliverables. Historical source files and acceptance records remain preserved.</p>\n<p id="position"></p>')
    html=re.sub(r'<p>Seventeen domain entries.*?</p>','<p>The ledger retains all 75 domain identities and prior review evidence. Current counts above come from the authored index. Historical proposals and completed scopes remain scoped evidence; tabletop-only production is retired. AC6 exact acceptance still needs recovery and verification before local adoption.</p>',html,count=1,flags=re.S)
    html=re.sub(r'<div class="sequence"><p><strong>Delivery order:</strong>.*?</div>','<div class="sequence"><p><strong>Active direction:</strong> source → engine specification → data/schema → state transitions → validation cases → player presentation. Reuse accepted interfaces and confer over genuine new decisions.</p><p><strong>Preserved owner direction:</strong> twelve-character expedition, alignment compatibility, up to four humans performing concurrent activities, and host-configured human/AI permissions. Verified progress backups already satisfy the prerequisite for careful cosmology review. Final whole-game flow, implementation, gameplay tests, balance and release remain separate gates.</p></div>',html,count=1,flags=re.S)
    template.write_text(html,encoding='utf8',newline='\n')
    delta.write_bytes(encoded({'recordedAtUtc':now,'direction':direction,'changes':[{'before':next(x for x in saved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,ledger,builder,template]],'ruleChanges':0,'newSpellAdoptions':0,'domainClosuresChanged':False,'sourceInformationDeleted':0}))
    run=subprocess.run([sys.executable,'-X','utf8',str(builder)],capture_output=True,text=True,encoding='utf8')
    assert run.returncode==0,(run.stdout[-2000:],run.stderr[-2000:])
    build=read(A/'REVIEW_MAP_BUILD.json');assert not build['missingLinks']
    assert [info(p) for p in protected]==protected_before
    assert directive.read_bytes()==attachment.read_bytes()
    for item in saved:
        assert hashlib.sha256((G/item['preservedCopy']).read_bytes()).hexdigest()==item['sha256']
    assert len(cov['aspects'])==75 and read(index)['authoredCounts']=={'reviewed':451,'pending':397}
    assert len(read(registry)['entries'])==49
    # Validate local markdown links in the new active guide and the start page.
    checked_links=0
    for p in [guide,start]:
        for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf8')):
            if '://' in target or target.startswith('#'):continue
            assert (p.parent/target.split('#')[0]).exists(),(p.name,target)
            checked_links+=1
    application={'recordedAtUtc':now,'direction':direction,'attachmentBytes':attachment.stat().st_size,'attachmentSha256':hashlib.sha256(attachment.read_bytes()).hexdigest(),'directive':info(directive),'verbatimCopy':True,'navigationFilesPreserved':len(saved),'protectedFilesUnchanged':protected_before,'areasRetained':75,'digitalScopesUpdated':list(maps),'domainClosureAndEvidenceUnchanged':True,'ordinarySpellCounts':read(index)['authoredCounts'],'registryEntries':49,'guideAndStartPageLocalLinksVerified':checked_links,'reviewMapExistingLinks':build['existingDistinctLinks'],'reviewMapMissingLinks':[],'newRuleAdoptions':0,'sourceInformationDeleted':0,'runtimeTestsRun':False,'scope':'Direction/navigation/preservation checks only; no mechanic implementation or gameplay validation.'}
    check.write_bytes(encoded(application))
    state=read(previous)
    state.update(recordedAtUtc=now,previousCheckpoint=info(previous),status=scope,goalTurnClassification='progress',developmentDirection=direction,coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),applicationCheck=info(check),newRuleAdoptions=0,newRuleAdoptionScope='Owner direction and navigation only; no source mechanic, accepted cohort, cosmology canon or domain closure changed.',navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':build['existingDistinctLinks'],'missingLinks':[]})
    state['activeGptReview'].update(userTurnId='b5b34710-2b90-4e7a-b644-a27f19a0fec8',status='Current06 was submitted once. Later notebook discussion describes AC6 as completed; exact acceptance artifact remains unrecovered and unverified. Do not resend or adopt from a later summary.',generationConfirmedLiveAtObservation=False,returnReceived=False,newRulesAdopted=False)
    state['acceleratedReview']={'protocol':info(protocol),'registry':info(registry),'inventory':info(inventory),'next25SemanticDelta':info(semantic),'preflight':info(A/'accelerated-review-01/PREFLIGHT.json'),'supersession':'Video-game-only directive controls conflicting tabletop requirements and future acceptance wording.'}
    state['safeNextActions']=['Follow the video-game-only directive and active guide; do not resume tabletop chapter/worksheet/GM publication work from historical checkpoint prose.','Recover and verify AC6 exact Current06 acceptance artifact before local adoption; no resubmission merely because older browser messages are unavailable.','Correct DE4 two identified fixture errors as deterministic digital test vectors while preserving originals. Do not adopt the pending Fate guard amendment without substantive conference.','Continue the prepared25-spell semantic delta with accepted-interface inheritance, actual automated preflight and narrowly authored engine decisions; no repeated review of settled scopes.','Preserve all75 domain identities; pursue their digital scope, final actual-GPT whole-game flow and verified delivery. Source/canon and implementation/gameplay/balance/release gates remain separate.']
    state.setdefault('preservationManifests',[]).append(info(manifest))
    checkpoint.write_bytes(encoded(state))
    print(json.dumps({'directive':info(directive),'guide':info(guide),'checkpoint':info(checkpoint),'check':info(check),'areas':75,'updatedDigitalScopes':len(maps),'preservedFiles':len(saved),'protectedFilesUnchanged':len(protected),'links':build['existingDistinctLinks'],'missingLinks':0,'ruleChanges':0,'newSpellAdoptions':0}))

if __name__=='__main__':main()
