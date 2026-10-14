from pathlib import Path
import json
GAME=Path(__file__).resolve().parents[4]
ROOT=GAME/'DescentReviewChanges/ReviewBible'
AUDIT=Path(__file__).resolve().parent
report=json.loads((ROOT/'docs/mechanics/COMBAT_PLAYTEST_VALIDATION.json').read_text(encoding='utf-8'))
header='''# Exact combat candidate review

The candidate below implements your first proposal as corrected by our counterexample exchange. Original books and class cards remain unchanged. Source integrity: two unchanged books, 217 exact paragraphs. Reference validation is bounded, not a complete event engine or balance claim. Whole DD03/17/18/19/20/21 remain open.

Please adversarially review the exact guide and helper code below. Identify material contradictions, missing costs, unlimited loops or misleading scope. These specific final interpretations need your disposition:

1. An explicit END OF NEXT target turn applied DURING its current turn excludes that current end. Your earlier next-end wording said strictly-after application (which alone would incorrectly include current end). I implemented skip_current_end for both bare future rounds and explicit next-turn ends. Confirm.
2. Bare N-round ALLY-targeted buffs lacking endpoint: source-start convention unless their text clearly makes a target clock? Confirm or give a different default.
3. Pin/Silence once-per-regular-turn cap: do you mean use only on OWN regular turn, or one attempt between OWN regular starts even when a legal attack occurs off-turn/extra turn? Your reply says extra turns do not replenish but doesn't expressly forbid use. I recommend interval budget usable on any legal qualifying attack, reset own regular start; no new uses from extra turns. Press and stance selection remain explicitly own-regular-turn-only. Need exact text before closing.
4. Ready casting occurs at preparation; I recommend ordinary spell effect duration begins at release, while held concentration and Ready expiry run during preparation. Concentration and RP/Dissonance/Refrain/cast triggers happen once at setup. Confirm no expired duration before effect first exists. Source expressly tied to CAST time can override only its explicit clock. Focused forbids ordinary Ready release; no free Reaction exception.
5. Source Secure Cargo says 'attach, lift, transfer, or protect up to one Extraction Load class'. It does NOT itself mean reduce a handling class. Existing Gameplay guide separates Load (approx10lb/unit; capacity STR with size modifiers) and Extraction Class0–6 (handling danger). I have explicitly left this term/interface open for the cargo audit; no broad cargo closure.
6. Simultaneous effects order is timestamp then stable creation sequence encoding printed same-source internal order. Caller arbitrates periodic families first, then dispatches actual winner packet at its sequence; no extra loser damage. Helper is scoped selected HP events, not all timer/cure/trigger dispatch. Is that sufficient reference scope?

Please give exact fixes for material findings; if this bounded source/action/timing pass can close after these clarifications, say so without closing the larger ledger rows. Then we continue Strain namespacing and remaining conditions/control, and source movement/extraction dependencies.\n\n'''
body=header+f"Current tests: {report['status']}; {report['checks']} checks; {report['movementInvariantStates']} movement-cost states.\n\n"
for rel in ['docs/mechanics/COMBAT_ACTION_PLAYTEST.md','tools/combat_playtest_rules.py','tools/validate_combat_playtests.py']:
    body+=f'\n# EXACT FILE: {rel}\n\n'+(ROOT/rel).read_text(encoding='utf-8')+'\n'
(AUDIT/'CODEX_COMBAT_EXACT_REVIEW.md').write_text(body,encoding='utf-8')
print(f'Built exact combat review packet: {len(body)} characters')
