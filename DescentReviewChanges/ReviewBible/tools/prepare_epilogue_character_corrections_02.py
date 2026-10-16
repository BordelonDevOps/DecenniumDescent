"""Preserve revised EPI semantic review and prepare a bounded second conference."""
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded

ISSUES = [
  {
    'id': 'ER01', 'title': 'One motif transaction and explicit denial integration',
    'locations': ['/EPI02/access', '/EPI02/motifs/2', '/EPI02/motifs/3', '/EPI04/wearing/sharedDenialLedger', 'CASEBOOK:EPI04-C06'],
    'finding': 'Ordinary activation fixes listeners at commitment and requires them through completion, but interruption says before commitment/completion means no spend, while payment says interruption after commitment spends. The commitment instant is still undefined. Split groups inherit one state only until 24h has elapsed. Law never explicitly joins the shared denial ledger; the mask guard and case still say if/where the guard applies. Law also does not say whether the performer is protected or whether the target can choose a hostile area effect over protected listeners.',
    'proposedResolution': [
      'For an ordinary motif, preflight and fix candidates/work order at start; perform for 60 uninterrupted seconds outside an encounter; recheck at completion. Commitment occurs only at successful completion, deducting the shared allowance immediately before effects. An interruption before completion spends elapsed time but no allowance. Remove candidates who did not hear throughout; an invalid effect at completion means no commitment. Law instead commits during its Action after legal preflight and before its save.',
      'All descendants of an Expedition split retain the same motifLedgerId and shared transaction record indefinitely. A merge links contributing ledgers to one state using the latest refresh timestamp and lowest allowance; no split, rename, new member, or later split of a merge unlinks these histories. One registered member cannot supply refresh to two ledger pools in the same 24h. State how actual separate Expeditions formed independently at module adoption differ from a renamed existing party.',
      'NEW explicit integration proposal: both Law control and mask Stunned use the current successful hard-denial mark keyed by source character, target, actual encounter. A legal activation always pays its own cost before immunity/guard/save; if the mark already exists, these two EPI effects have no control effect and no replacement rider. An unsuccessful save blocked by immunity/guard does not create a new mark. A successful first Law/Mask application sets the mark, which existing class features then honor with only their own printed fallback. Use the same current encounter definition; initiative changes are not a reset.',
      'Law may include the performer among its fixed willing protected listeners. The controlled target cannot deliberately include a protected listener in a hostile area effect, as well as the stated hostile targeted effects. Keep nonprotected third-party/environment damage break rules as written. Sorrow has at most one pending grant per listener; another grant does not stack or extend its existing expiry.'
    ],
    'requiredCases': ['A 40-second interrupted ordinary performance costs no allowance, and a completed immune Law costs one.', 'Monk Stunning Strike really succeeds first (2 Ki, hit, failed CON save), then the same Monk pays mask charge but cannot apply another Stunned; reverse order uses the real Monk Reaction-loss fallback.', 'Law first then mask, and mask first then Law; separate source character remains separately eligible.', 'Split groups spend/refill one ledger after 24h rather than acquiring two pools.']
  },
  {
    'id': 'ER02', 'title': 'Close Transition and Balance integration rather than defer it',
    'locations': ['/EPI02/motifs/1', '/EPI02/motifs/6', '/EPI02/transitionClockPolicy'],
    'finding': 'Transition no longer nerfs source halving, but final-target selection contradicts fixed preflight, work orders have no start/expiry rule, and ceil-minute/minimum-one-minute can increase a positive sub-minute remainder. Balance still says matrix modifications end/pause as the source requires although the new Balance substitution is not a source-defined preparation event. Mixed active work/assistant participation can still make a shortened qualified task impossible without deciding the actual participant intervals.',
    'proposedResolution': [
      'Fix an existing workOrderId, exact task, materials/prerequisites, worker roles and up to four beneficiaries at preflight. Commit only if these still exist at completion. Start affected active work within 24h of grant; otherwise the unused reduction expires. Once begun, the reduction persists only for that same work order under its original interruption/deadline rules. It cannot be carried into a new attempt/project or reassigned to a new worker.',
      'For positive remaining minutes r use min(r, max(1, ceil(r/2))); zero stays zero. Thus 5m becomes3m, 30s stays30s, and no task becomes longer. Existing exact time adjustments apply first. Preparation active study may qualify; an effect duration never does. Include actual Matrix Efficiency full preparation 60→45→23m and exact Forge Dwarf artisan-tool craft 480→360→180m. For Fervent Ritualist establish a legal Ritual casting-work clock, not merely a duration field; if its base active time is10m it becomes9m then5m. Do not invent a missing casting time.',
      'Required simultaneous participation remains simultaneous. Complete a joint phase only after every mandatory worker has satisfied their independently adjusted clock; each must remain present and qualified for the full actual common phase, even if their own credited minimum was reached earlier. Optional assistance applies only when that assistant qualifies throughout the actual check-producing work. Personal mask projects remain single-worker. Never use shortened hours to avoid a real minimum duration or borrowed-proficiency expiry.',
      'NEW explicit Balance rule: remove all Matrix Mastery modification and pair assignments on the removed matrix; replacement is unmodified until a later legal full preparation assigns one. A linked-pair record containing the removed matrix becomes inactive, with its already-spent per-round history retained. No new link is formed by Balance. End a preparation-bound benefit tied to the removed matrix but do not silently end an already-cast spell unless its own rule or the new stated adaptation requires it. State ongoing Stability Reinforcement precisely. Preserve all family history and limited-use counters.',
      'Use actual Druid form names/cards already checked: Dire Wolf /cards/11, Earth Warden (Dire Bear) /cards/12, Sky Serpent /cards/13. State that selecting a new Arch attunement does not itself activate a form or clear Refrain. Apply Warrior max-HP clamp explicitly when Flesh Warden is removed; no heal on a capacity increase.'
    ],
    'requiredCases': ['Sub-minute remainder, partially completed task, actual Matrix Efficiency and Fervent Ritualist qualification.', 'Wizard removes a linked/modified matrix while a spell is ongoing; actual state and modification/history after swap.', 'Three required qualified assistants with Knowledge Transfer expiring during the actual shared phase.', 'Warrior Flesh Warden removal clamps HP; replacement capacity does not heal.']
  },
  {
    'id': 'ER03', 'title': 'One operative-mask rule and source-faithful examples',
    'locations': ['/EPI04/identity/operativeLimit', '/EPI04/identity/operativeDesignation', '/EPI04/project', 'CASEBOOK:EPI04-C01', 'CASEBOOK:EPI02-C03', 'CASEBOOK:EPI02-C07', 'CASEBOOK:EPI02-C08'],
    'finding': 'operativeLimit says completing a new mask makes all older masks dormant immediately; operativeDesignation says keep current and choose after beneficial rest. They disagree. Vow change during an unfinished project is unspecified. C01 still says Warrior chooses STR/DEX at project start. Courage C03 still restores from ambiguous 0/2 without a spent slot. Sorrow C07 still treats the pending reroll as an unspent motif activation. C08 implies a personal mask requires borrowed proficiency despite its bare ability check.',
    'proposedResolution': [
      'Use operativeDesignation as the single rule: if no operative mask exists, completion/rebind may designate that mask immediately; otherwise completing another does not deactivate the existing one. Choose one replacement operative mask at completion of a beneficial rest. Retiring/superseding/fulfilling the bound vow immediately dormants it and removes its operative designation. Never refresh wearer charge from any such transition.',
      'A project binds the active vow and class at its start. If that vow changes before the crafting check, pause rather than silently transfer secrets/DC: the wearer may cancel (committed blank becomes spoiled) or finish a cosmetic dormant mask under the original fixed project record; a completed dormant mask can later undergo the existing one-hour rebind. No new crafting check or deadline reset. Disclose before revision.',
      'Clarify finite reserve is keyed to the actual class selected at adoption; no free change of blank material for later multiclass projects. Give a concrete worn/carried gear weight and storage/durability reference as NEW if source lacks one. Repairs require actually available workshop/materials; workshop label or price alone is not stock. Do not invent punitive breakage rolls.',
      'Correct C01 Warrior wording to the already-recorded level-one permanent choice. C03 begins ready0/spent1 and ends ready1/spent0; add ready0/spent0 gives nothing. C07 begins with an already-granted pending Sorrow and says committed consequences cannot be rewound, pending charge remains subject to original expiry. C08 should use mask as bare-key work and put borrowed proficiency on a separate qualified research example.'
    ],
    'requiredCases': ['Two completed masks while one is operative; rest switches designation without extra charge.', 'Vow superseded mid-project with original deadline preserved.', 'Transition applied with less than60m shaping remaining locks secrets at that instant; interrupted final short block earns no credit.']
  },
  {
    'id': 'ER04', 'title': 'Complete all challenge terminal states and clocks',
    'locations': ['/EPI06/test/scenes', 'DIRECTOR_CHAPTER.md#Seven Test scenes'],
    'finding': 'Sorrow and Contradiction still have no result for passive timeout without a false assertion. Balance says pour twice into either basin although the5-unit basin overflows at6. Its critical failure increments a reset but only third spill triggers failure. Law at-most-one allows a state with no claimant served, contrary to its own posted allocation rule. Transition jump lacks gap widths. Courage failure says no real items consumed, while materialReturn retains real expended resources. General critical degree/timing at exact deadline/participant count remain unstated.',
    'proposedResolution': [
      'Add shared test procedure: one petitioner acts, one Action per6s in round scenes; helpers cannot supply extra challenge turns. Actual external features work only when their exact targeting permits it. For these task checks collapse Critical Success/Success to listed success and Failure/Critical Failure to listed failure unless expressly stated otherwise. Resolve an action/check completing exactly at the deadline before timeout. End immediately upon success/failure; no same-petition restart. Real resources voluntarily spent remain spent; projected props vanish and projected hazards inflict no real injury.',
      'Courage: place courier at the near end of the30ft crossing; state Coach/Brace range/hearing, escorted character movement, and end-round resolution before the anchor release so three Brace successes work. Remove contradictory no-real-items-consumed sentence.',
      'Balance: safe solution pours both cupfuls into the7-unit basin, or divides them with neither capacity exceeded. Every spill and stated critical-failure reset increments one common reset counter; third reset fails. Failed study spends time; repeat only if enough clock remains for study and the physical pours. Exactly20m check completion resolves first, then there is no time for later pours.',
      'Law: without an openly agreed prospective amendment, success requires A/B/C each exactly one token and fourth in tray. State what constitutes agreement to an amendment (petitioner plus all three projected claimants), its allowed scope and time, and claimant consent responses. Token handling one Action each; ordinary speech/declared amendment uses actual stated scene time. Two failed persuasion attempts do not stop legal nonpunitive redistribution.',
      'Sorrow: projection briefing explicitly establishes Daro returned alive at the recorded event, with no evidence identifying the missing deceased. A genuine explicit choice to preserve uncertainty succeeds; doing nothing/unfinished response at timeout fails.10m analysis completes at deadline, followed by a single immediate no-time answer before timeout; no extra work.',
      'Contradiction: unanswered/unresolved at timeout fails, including repeated failed analyses without a stated reconciliation. Define5m attempts and immediate final answer at deadline.',
      'Transition: specify adjacent5ft platform footprints, actual gap width/exit step distance and crystal handling. Ride stays the no-check solution. Actual zero Speed prevents normal step; do not invent motion beyond actual abilities. Put alternate jump movement, DC and failure landing in the printed scene rather than defer an unknown gap.'
    ],
    'requiredCases': ['Sorrow passive timeout, Contradiction two failed analyses, Balance third non-spill reset, Law empty-allocation rejection, three Brace successes at exact18s, real resource spent during a projected failure.']
  },
  {
    'id': 'ER05', 'title': 'Give Concord Step a finite playable destination and exact return boundary',
    'locations': ['/EPI06/revelation/sigil', 'CASEBOOK:EPI06-C08', 'DIRECTOR_CHAPTER.md#Concord Step'],
    'finding': 'Four identical empty alcoves with an unauthored exterior still supply no meaningful visit; availability permits result12 to become inert because no scene was authored. Their environment is safe only for8h, after which stranded characters have no defined environment or route. Return at7h50 is permitted to start, but completion must be before8h and flags expire at exactly8h; Director instead says finish by8h. Return has no completion recheck for death/unconsciousness/presence. Origin circles are unnamed; default origin need not be physically on Aethel. It is unclear whether opening the next real session cancels already-issued returns.',
    'proposedResolution': [
      'NEW finite default module: enable all four primary-realm visitor alcoves at adoption, without asserting recovered/public geography. The origin must be an existing accessible hub physically on Aethel. If none is currently reachable, retain the unspent sigil; do not silently replace response12 with an inert prize. Its outbound session window still applies, so disclose access before the petition roll.',
      'Author four actual named20x20 visitor-room scenes, each with six nonoverlapping5ft arrival spaces, a specific local mortal custodian, props, finite stock, one meaningful10–30m activity with at least two choices and explicit outcomes, and a limited truthful answer menu. Use the source-described principles only as theme; do not disclose Equation text, hidden identities, new cosmological history or universal facts. Rewards can be local mundane drawings/records with concrete access/story consequences, not new unlimited resources or recovered lore.',
      'Define a closed finite visitor area: room and, if desired, one bounded vestibule with an ordinary door, exact geometry and light/air/temperature continuing after8h. No newly asserted route beyond it. Supply finite food/water and exact custodian conduct, with no automatically beneficial rest/Haven. Disclose before outbound: missing return can strand a traveler in this defined site; the default module contains no free onward/return route. A separately actually available approved travel effect or concrete campaign rescue is required, not a promise that unspecified ordinary travel exists. No automatic lethal environmental change at expiry.',
      'Keep up to5 total travelers. Specify origin15ft square/legal landing cells and ordinary carried gear/capacity. Outbound and return recheck living/conscious/willing/present, legal spaces and stronger denials at completion. If a companion becomes invalid omit them; if a solo returner becomes invalid the return fails with no flag spent. Mark flags only for actual outbound travelers.',
      'At equality, a valid return completing exactly outboundAt+8h resolves first, then expire remaining flags. Thus7h50 start is valid;7h50m01s is not. The next scheduled session opening prevents uncommitted outbound, but personal return rights already issued continue through their actual8h deadline during play. Session UI changes advance no campaign time.',
      'The current C08 says two occupied origin circles leave room for only two of three, but origin geometry and capacity do not demonstrate that. Replace with exact blocked/occupied cells and actual remaining legal spaces, preserving partial return order and no-refund/deadline rules.'
    ],
    'requiredCases': ['One fully worked visit with meaningful local activity and no invented canon.', 'Return19:50→20:00 succeeds;19:50:01 is refused.', 'Opening next scheduled session while companions remain does not erase valid returns.', 'Unconscious/dead returner at completion stays, original flag expires normally.', 'A stranded traveler after8h has an explicit physical state, supplies and known unavailable escape, rather than an undefined plane hazard.']
  },
  {
    'id': 'ER06', 'title': 'Make the two prose chapters usable without decoding the JSON',
    'locations': ['PLAYER_CHAPTER.md', 'DIRECTOR_CHAPTER.md'],
    'finding': 'The Player chapter omits home principles, motif30ft/hearing and Motif DC, exact guidance menu, virtue/class pairings, duplicate blessing/acquisition/scaling limits, mask bare-ability/PB restriction, some Conflict immunity rule and usable step actions. Director still omits all seven symbolic acts and refers to model for return-space rules. Important rules cannot be discovered from the prose alone.',
    'proposedResolution': [
      'Print concise complete player-facing procedures for all of those items; keep optional details and actual class IDs as provenance links, not substitutes for rules. Do not print secret challenge/puzzle answers in the player chapter.',
      'Print all seven symbolic acts and the complete challenge/destination/return procedure in Director prose. Make model and both chapters mechanically identical after this patch; remove contradicted earlier paragraphs instead of adding a competing addendum.',
      'For checks: include range/hearing/qualification/cost/commitment, duration/expiry, all material exceptions and actual choice menus. Present this as playable rules, without audit jargon in the actual player flow.'
    ],
    'requiredCases': ['Cross-check each printed table and numeric boundary against the final model; report concrete corrected sections, not a blanket claim.']
  },
  {
    'id': 'ER07', 'title': 'Repair overclaimed correction dispositions and preserve every draft',
    'locations': ['REGISTER.json#correctionDispositions', 'VERDICT.md', 'CASEBOOK.json'],
    'finding': 'EC03 claims exact transaction despite undefined ordinary commitment. EC04 never resolves motif/class shared denial. EC07 cites EPI01-C01/C02 for mixed conduct but neither exercises it. EC09 claims all terminal branches executable despite timeout holes. EC12 says old cases corrected despite the lingering Warrior/Courage/Sorrow cases. Counts and valid citations do not establish semantic completion.',
    'proposedResolution': [
      'Preserve both prior ZIPs and every original75case ID. Correct current versions of defective cases; retain historical wording only in clearly nonoperative provenance. Add actual numerical new cases for ER01–ER05 and mixed conduct (one qualifying aligned choice plus one contrary choice gives neither).',
      'Return the same eight filenames, unchanged60source bindings, refreshed seven-file output hashes and a new filename ending Integrated. Record each ER01–ER07 disposition with actual final paths and case IDs. Source-check success and authored examples are not runtime execution or human/balance/whole-game approval.',
      'If a proposed rule has a substantive better alternative, state and resolve the exact issue explicitly rather than defer it to a future source or generic Director choice. Source original50% Transition, every-PC starting vow,17classes and exact existing card gates remain fixed.'
    ],
    'requiredCases': ['All75IDs retained uniquely, source hashes unchanged, operative/prose/case contradictions removed.']
  }
]

def main():
    now = datetime.now(timezone.utc).isoformat()
    folder = A/'cosmology-epilogue-character-01-corrections-02'
    audit = A/'COSMOLOGY_EPILOGUE_CHARACTER_01_SEMANTIC_AUDIT_02.json'
    archive = A/'DD_Cosmology_Epilogue_Character_01_Corrections_02.zip'
    assert not any(p.exists() for p in [folder,audit,archive])
    revised = A/'cosmology-epilogue-character-01-return-revised'
    first = A/'cosmology-epilogue-character-01-return'
    source_check = A/'COSMOLOGY_EPILOGUE_CHARACTER_01_RETURN_SOURCE_CHECK_revised.json'
    cases = json.loads((revised/'CASEBOOK.json').read_text('utf-8'))['cases']
    old = json.loads((first/'CASEBOOK.json').read_text('utf-8'))['cases']
    assert len(cases)==75 and len({c['id'] for c in cases})==75
    assert {c['id'] for c in old} <= {c['id'] for c in cases}
    check = json.loads(source_check.read_text('utf-8'))
    assert check['checkCount']==444 and check['failureCount']==0
    report = {'recordedAtUtc':now,'reviewId':'COSMOLOGY-EPILOGUE-CHARACTER-01-ER','status':'revised return source integrity passes; seven remaining semantic correction groups; NOT adopted',
      'reviewedArchive':info(A/'DD_Cosmology_Epilogue_Character_01_Return_revised.zip'),
      'sourceCheck':info(source_check),'sourceChecks':444,'sourceFailures':0,
      'semanticReviewScope':'Read full revised model, player and Director chapters, all75authored cases, all12EC dispositions and verdict. Checked actual Druid forms, Monk Stunning Strike/Stun Guard, Wizard Matrix Mastery/Efficiency, Cleric Fervent Ritualist and crafting Master Craftsman source text. No runtime tests executed.',
      'readFiles':[info(revised/name) for name in ['EPILOGUE_CHARACTER_MODEL.json','PLAYER_CHAPTER.md','DIRECTOR_CHAPTER.md','CASEBOOK.json','REGISTER.json','VERDICT.md']],
      'preservedFirstCaseIds':len(old),'revisedUniqueCaseIds':len(cases),
      'improvementsVerified':['Bard citation corrected','Transition50% restored','seven exact blessing card envelopes copied including Soldier During combat','wearer-owned reveal charge and permanent Warrior ability in model','source-required starting vow and no forced belief rewrite','Sorrow future save window','valid unique Three Lamps truth table','petition arithmetic and Exhaustion5 disadvantage fixed'],
      'issues':ISSUES,'newRulesAdopted':False,'sourceInformationDeleted':0,
      'approvalGates':{'runtime':False,'humanPlaytest':False,'balance':False,'wholeGame':False,'publication':False}}
    audit.write_bytes(encoded(report));folder.mkdir()
    (folder/'SEMANTIC_AUDIT_02.json').write_bytes(encoded(report))
    (folder/'SOURCE_CHECK_REVISED.json').write_bytes(source_check.read_bytes())
    request = '''Joint EPI-01–07 revised-return review, ER01–ER07.
The revised archive b1b0e6a6275b7208d385b611038eadfa9c1c39dad1e9aea8dee3d09333c8f241 is preserved.444 source/file/location checks pass. I read the full model, both chapters, all75cases,12dispositions and verdict. The corrections substantially improve it, but seven precise groups remain. The attached audit gives actual defects, concrete proposed resolutions and required adversarial examples. This is a bounded integration request, not a request to restart the design.
Resolve ER01–ER07 in the existing eight files. Preserve all75case IDs and unchanged60source bindings. Use proposed rules or explicitly resolve a substantive better alternative. Add a finite playable default Concord visit, exact mask/motif/denial state transitions, completed challenge timeout branches, and complete prose. Do not claim closure from counts or citations alone. Return DD_Cosmology_Epilogue_Character_01_Return_Integrated.zip with refreshed EVIDENCE_MANIFEST.json and ER dispositions.
All new completion is NEW provisional Director/playtest authorship, never recovered cosmological canon. No epoch/hidden-identity decision, pending-spell promotion, EPI08–17 adoption, source deletion, runtime/human/balance/whole-game/publication approval. The user asked us to keep conferring and fully develop the game; no new permission is needed for this bounded work.
'''
    (folder/'REQUEST.txt').write_text(request,encoding='utf-8')
    manifest={'recordedAtUtc':now,'files':[info(p) for p in sorted(folder.iterdir()) if p.is_file()], 'newRulesAdopted':False}
    (folder/'MANIFEST.json').write_bytes(encoded(manifest))
    with ZipFile(archive,'w',ZIP_DEFLATED) as z:
        for p in sorted(folder.iterdir()):z.write(p,p.name)
    print(json.dumps({'audit':info(audit),'packet':info(archive),'groups':len(ISSUES),'sourceChecks':444,'sourceFailures':0,'reviewedCases':75,'newRulesAdopted':False}))

if __name__=='__main__':main()
