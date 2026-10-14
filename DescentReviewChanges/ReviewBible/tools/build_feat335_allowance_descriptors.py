"""One-use FW08 assembly from exact audited identities and current full sources."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
from validate_feat_exact_01_composite_casting import read, info

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G/'docs/audit/2026-10-08/full-game'
V = A/'feat335-acquisition-audit-01-verdict'

LR = '''acrobatic_mastery arcane_recall arcaneResonance arcane_transfusion divine_favor
echo_spell ether_anchor flash_cast hypermutationSpike mental_buffer mirror_cast
overchannel rogue_s_escape spell_deflection spell_echo_chamber spell_reservoir
stubborn_resolve twin_cast wilderness_chef blood_ritual cursebound_flesh undying_flesh'''.split()
SR = '''battlefield_commander berserker_rage fast_talker mental_fortress orcish_fury
shield_bash target_mark volley anatomy_lore beast_lore combat_engineering core_infusion
dark_fortitude eldritch_combat favored_enemy_dragon giant_slayer hardened_grip
precision_strike primal_instinct siege_savant slayer_s_resolve'''.split()
BOTH = '''blood_magic channeled_flow mystic_recoil versatile_mastery arcane_adaptation
arcane_calculus conjure_flora eldritch_echo mimicry quickened_thought spell_reflection'''.split()
NO_POOL = 'aberrant_mind brawler climber combat_reflexes forge mobile'.split()

# These are later-event entitlement keys, not new consumable pools or invented
# turn/recipient records at purchase. Full controlling text is included below.
CADENCE = {}
def cadence(ids, family, scope, epoch, detail):
    for sid in ids.split():
        CADENCE.setdefault(sid, []).append(dict(family=(family or sid), maximum=1,
            scope=scope, epoch=epoch, initialization='No event/epoch claim at acquisition; retain existing clock and history.', detail=detail))

cadence('bladedancer break_line bull_rush crippling_strike crusher piercer punishing_blow savage_attacker slasher tactical_flanker unstoppable_force precision_strike',
    None, ['owner'], 'actual regular creature-turn interval under FS06', 'An eligible off-turn event can use a distinct regular creature-turn interval; linked extra turns do not reset it. Exact own-movement/attack prerequisites remain in the full procedure.')
cadence('cleave combat_slide crushing_advance whirlwind_striker combatExpertise',
    None, ['owner'], 'owner regular-turn interval', 'Only the exact own-turn event qualifies; no extra-turn refresh.')
cadence('efficient_caster', None, ['owner'], 'numbered global round', 'Both the LR charge and this round claim commit with the genuine reduction.')
cadence('spell_reflection', 'spell_reflection.passiveRetaliation', ['owner'], 'numbered global round', 'Separate from the one SR/LR redirect use; first qualifying damage packet consumes the claim even if half rounds to zero.')
cadence('combat_reflexes', 'combat_reflexes.extraReaction', ['owner'], 'numbered global round / governed six-second interval', 'One extra token begins at genuine encounter entry; ordinary Reaction has its separate regular-start clock. Preserve identity across entry/reentry/outside transitions and prohibit two Reactions on one event.')
cadence('mana_burn', 'mana_burn', ['recipient'], 'numbered global round', 'One recipient-wide allowance across every caster/owner, consumed even when an actual RP pool currently has zero.')
cadence('curse_weaving', 'curse_weaving', ['owner', 'recipient'], 'numbered global round', 'One initial-save curse per owner/target/round, no per-tick or per-stage renewal.')
cadence('wilderness_chef', 'wilderness_chef.recipient', ['recipient'], 'recipient beneficial Long-Rest epoch', 'One eater entitlement across every cook; additional portions do not refresh it. No eater or portion exists at acquisition.')
cadence('arcane_adaptation eldritch_echo mimicry', 'copyRelease', ['owner'], 'numbered global round', 'One shared copy-release allowance; recharge of a feat does not reset this independent round history.')
cadence('arcane_calculus quickened_thought', 'freeStoredRelease', ['owner'], 'numbered global round', 'One shared free stored release; both retain the existing one Ready/concentration slot and distinct legal release windows.')
cadence('quickened_thought', 'quickened_thought.firstInitiative', ['owner'], 'real encounter', 'No cantrip at purchase. Only first legitimate initiative allows an actually payable bank; reroll/reentry cannot bank again.')
cadence('eldritch_combat', 'eldritch_combat.embeddedCast', ['owner'], 'actual regular creature-turn interval', 'Both append modes share this cap. Ordinary Attack-Action append additionally has an owner regular-turn cap; SR mode may occur off-turn.')
cadence('eldritch_combat', 'eldritch_combat.ordinaryAppend', ['owner'], 'owner regular-turn interval', 'No extra Action, repertoire or RP; shared embeddedCast cap also applies.')
cadence('energy_sink', 'energy_sink.hostileCast', ['owner', 'hostileCastRoot'], 'whole actual hostile cast lifetime', 'One recovery from a cast across all its later ticks, not one per LR epoch.')
cadence('lucky', 'lucky.intervention', ['owner', 'underlyingRoll'], 'whole underlying roll lifetime', 'One Lucky point intervention even if another feature later rerolls the same event.')
cadence('overrun', 'overrun.challenge', ['owner', 'recipient'], 'owner regular-turn interval', 'No repeated challenge against the same creature from extra Dashes.')
cadence('target_mark', 'target_mark.firstAttack', ['mark', 'attacker'], 'whole actual mark lifetime', 'At most one mark per owner. On the first eligible attack consume all applicable owners\' mark entitlements; award at most one +1. Alliance/custody changes never reset identity.')
cadence('primal_instinct', 'primal_instinct.howl', ['actual howl', 'recipient'], 'original howl deadline', 'Fixed eligible recipients including owner, one family entitlement each, consumed on first eligible attack even on miss/cancellation.')
cadence('fast_talker trapsetter', 'hardDenial', ['sourceCharacter', 'recipient'], 'real encounter', 'Use the existing cross-class/spell/companion/feat denial family; no new denial allowance on new trap/feat/rest identity.')
cadence('shield_bash', 'hardDenial', ['sourceCharacter', 'recipient'], 'real encounter', 'Stun also requires the shared denial ledger; rest replenishes stun use but cannot reset encounter denial history.')
cadence('conjure_flora', 'offensiveCompanion', ['owner'], 'numbered global round', 'The shared companion allowance already exists; acquiring plants or command permissions does not create another. See prior exact Flora/Trapcasting evidence.')

SHARING = {
    'blood_magic': 'Damage/DC choices spend the same use; no permanent mode selection.',
    'slayer_s_resolve': 'Melee/breath attack-disadvantage and breath-save-reroll branches spend the same use.',
    'trapsetter': 'Three separate type uses: snare, caltrop, charge. Physical armed-body slots and stock are separate, initially empty.',
    'mimicry': 'One capture and its one release chain per rest epoch; no second spend at release and no replacement loop. Rest expires an existing capture but never creates one.',
    'conjure_flora': 'One rest creation use; total10 capacity permits its one additional paid Action inside that same committed use, not a second rest charge or initial plant.',
    'eldritch_echo': 'Capture use is separate from the shared Forbidden Pact/Echo single cantrip grant identity; acquisition preserves the existing grant and casting histories.',
    'versatile_mastery': 'One borrowed activation; prepared-choice changes do not refill. Already-known donor card shares actual personal card recharge history; unknown borrowed card retains its one activation history.',
    'core_infusion': 'SR reroll is distinct from later beneficial-LR infusion creation; owner/body slot identities and actual crafted-item receipts stay separate.',
    'anatomy_lore': 'SR use limits only advantage-mode slow rider; later marking has its actual BA cost and one active mark, no new rest limit.',
    'precision_strike': 'Critical mode spends SR use and turn allowance; ordinary mode spends only turn allowance. Both exclude Power Attack on the same attack.',
    'spell_reservoir': 'LR charge needs a later genuine beneficial SR trigger; LR alone never supplies that trigger, and declining cannot bank its past trigger.',
    'arcane_recall': 'Existing paid-expense/refund receipts are shared across refund sources, never initialized by this feat.',
    'arcaneResonance': 'Eligible paid rank1 expense must be in the same owner LR epoch; shared refund ledger bounds all recovery of that expense.',
    'dark_fortitude': 'Separate live +2 per total-level maximumHP component preserves current HP; necrotic SR Reaction and strict-below-half poison threshold remain separate.',
    'blood_ritual': 'One owner LR start-use; self plus PB OTHER allies fixed at later ritual start. Exact tied-rest completion ordering remains in the unchanged reviewed procedure.',
    'wilderness_chef': 'Owner LR preparation use is separate from the recipient-wide LR entitlement across all chefs.',
    'elven_grace': 'One actual encounter evasion; changing initiative labels or reentering the same encounter cannot refill it.',
    'contraption_crafter': 'One construction start per24 elapsed hours, not per SR/LR/calendar date; object transfer retains body expiry and uses, no owner allowance transfer.'
}

def assemble():
    paths = [V/'ACQUISITION_ROWS.json', V/'FINITE_REMAINING_WORK.json',
        A/'FEAT_EXACT_01_ACQUISITION_CONTRACTS.json',
        R/'data/public/feat_candidates/exact_01/candidate.json',
        R/'data/director/feat_candidates/exact_01/candidate.json',
        R/'data/public/feat_candidates/exact_01/shared_rules.json',
        A/'FEAT335_CURRENT_ACQUISITION_FOLLOWTHROUGH_AFTER_CONDITIONAL_PRESERVATION.json',
        R/'tools/feat335_allowance_bindings.py', Path(__file__)]
    rows = {r['id']:r for r in read(paths[0])['rows']}
    fw = next(g for g in read(paths[1])['groups'] if g['id']=='FW-08')
    contracts = {r['id']:r for r in read(paths[2])['records']}
    current = {r['id']:r for r in read(paths[6])['rows']}
    specific = set(LR + SR + BOTH + NO_POOL + ['lucky','efficient_caster','energy_sink','contraption_crafter','elven_grace','trapsetter'])
    assert len(specific)==66
    assert specific=={sid for sid in fw['exactMembers'] if not rows[sid]['e_evidence']['ordinaryNoNewStateBranch']}
    assert set(CADENCE).issubset(set(fw['exactMembers']))
    entries=[]
    for sid in fw['exactMembers']:
        r=rows[sid]; allowances=[]
        def add(identity, maximum, recovery):
            allowances.append({'identity':identity,'owner':'paid feat owner', 'recipient':'owner holds the allowance; actual effect recipients are selected only at a later source-qualified event',
                'maximum':maximum,'initialCurrent':'maximum at first legitimate paid acquisition only',
                'recovery':recovery,'mechanism':'BoundAllowance + existing FiniteFeatUse',
                'noAliasReinitialization':True,'growth':'capacity only; never current refill',
                'unrelatedState':'Preserve current HP/RP, ordinary actions/Reactions, real bodies, stock, prior casts, use roots and actual clocks.'})
        if sid in LR: add(sid,1,'LR')
        if sid in SR or sid in BOTH: add(sid,1,'SR_OR_LR')
        if sid in ['efficient_caster','energy_sink']:add(sid,'currentPB','LR')
        if sid=='lucky':add(sid,3,'LR')
        if sid=='contraption_crafter':add(sid,1,'elapsed24h')
        if sid=='elven_grace':add(sid,1,'realEncounter')
        if sid=='trapsetter':
            for mode in ['snare','caltrop','charge']:add(sid+'.'+mode,1,'SR_OR_LR')
        entries.append({'id':sid, 'name':r['name'],
            'auditedBranch':'noNewConsumableOrActiveEffect' if r['e_evidence']['ordinaryNoNewStateBranch'] else 'specificInitialState',
            'exactAcquisitionDescriptor':deepcopy(r['a_acquisition']),
            'exactMandatorySelectionAndSnapshotDescriptor':deepcopy(r['b_mandatorySelectionsAndSnapshots']),
            'exactInitialStateDescriptor':deepcopy(r['c_initialState']),
            'exactConditionalOrDeferredDescriptor':deepcopy(r['d_externalOrDeferred']),
            'currentCompleteContract':deepcopy(contracts[sid]),
            'finiteAllowances':allowances, 'laterEventCadences':deepcopy(CADENCE.get(sid,[])),
            'sharedOrSeparateIdentity':SHARING.get(sid,'Each explicit feat identity is separate except the exact shared families in its full operative procedure and FS01–08. No catalog alias grants a second acquisition.'),
            'preservedExistingSpecializedEvidence':{k:deepcopy(v) for k,v in current[sid].items() if k.endswith('Evidence')},
            'initializationScope':'Finite entitlement/data binding only. No attack, healing, cast, active effect, body, inventory or new external qualification is inferred from purchase.',
            'fullUseRuntimeExecuted':False})
    return {'recordedAtUtc':datetime.now(timezone.utc).isoformat(), 'finiteWorkGroup':'FW-08',
        'status':'assembled; validation recorded separately', 'sourceBindings':[info(p) for p in paths],
        'counts':{'members':177,'noNewConsumableOrActiveEffect':111,'specificInitialState':66},
        'countClarification':'The111 no-new-consumable/active-effect rows are INSIDE the177 FW08 members. Some still have later-event cadence limits; no additional111 characters or new resource pools are requested.',
        'authority':'Complete current operative procedure and unchanged supplements control. Structured fields bind acquisition allowances and explicit identity/epoch exceptions only, not a full executable rules translation.',
        'entries':entries, 'newRules':0, 'exactApproval':False, 'fullAcquisitionRuntime':False, 'cosmologyReviewed':False}


if __name__=='__main__':
    out=A/'FEAT335_ALLOWANCE_DESCRIPTORS.json'
    assert not out.exists()
    data=assemble()
    out.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'report':info(out),'counts':data['counts']}))
