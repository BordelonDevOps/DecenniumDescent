from pathlib import Path
import json
GAME=Path(__file__).resolve().parents[4]
ROOT=GAME/'DescentReviewChanges/ReviewBible'
AUDIT=Path(__file__).resolve().parent
report=json.loads((ROOT/'docs/mechanics/STRAIN_PLAYTEST_VALIDATION.json').read_text(encoding='utf-8'))
text='''# Exact Strain candidate review

The source-qualified Strain guide and helpers below implement our conference and corrections. Status IN_REVIEW. No source book or normalized class card changed. Namespacing correction is also made in the generic condition/recovery references: neither Strain track is global Exhaustion.

Please adversarially review for source drift, boundary bugs, recovery replay, maxHP/damage confusion, accidental class grants or changing the wrong track. Material points to confirm:

1. Level2 retains -1 attack/save exactly; your earlier level3 summary is corrected in the guide and tests. The actual ending-gain profile is Sanguine Surge; my earlier 'Regenerator' example was not a canonical source name and is not used in the implementation.
2. Dash during its own regular turn excludes the current end and locks through the NEXT future turn's end; I reused the corrected combat marker helper with explicit excluded_current_marker. Dash at1 during current turn ending3→lock through9. Off-turn Dash at4 with own end phase3→9. Outside Dash4→10; crossing initiative preserves original deadline. Please confirm this fixes the imprecise 'strictly after Dash' wording without letting same-turn end clear the lock.
3. RestHistory validates COMPLETED activity intervals and reward histories, not active project management/inventory. Caller owns real care/supplies, legal activities, ongoing interruptions and other rest rewards. It forbids overlapping ordinary activity intervals and overlapping Haven windows; a Haven care window may contain distinct sleep/recreation. Processing order must be chronological, completed IDs cannot replay. Ineligible activity isn't a RestWatch just because it lasts8h and therefore cannot clear Rest Debt. A legal but reward-capped safe RestWatch DOES clear Debt without changing long-rest/short-rest benefit clocks.
4. Ordinary point recovery requires chosen eligible point (or all for Haven). It never alters LifeState, so cannot revive/restoreHP; actual corpse rest/treatment legality is caller-owned. MaxHP projection preserves death counters/dead state and clamps without damage. True expedition death gain calls existing kill(). Collapse retains independently dying0HP state, and later lethal gain at collapsed6 kills despite storage cap.
5. The 30 bindings are NAMESPACE REFERENCES, not triggers: mapping Serum Tolerance to serum Strain does not apply gain or grant immunity. Unknown source IDs are rejected. All30 exact references/track contexts are checked. Broad source integrity separately verifies8engine references,17cards,3campaign sections,12Core paragraphs against unchanged files.
6. Helper track_penalties supplies selected numeric/flag projection, not every Exhaustion/condition/life/collapse effect. Caller adds independently applicable condition effects and derives actual walking/travel pace. No duplicate global Exhaustion immunity or auto-cure by similar name.

Return exact fixes for material findings. If this supplied namespace/recovery package can close after review, say so at bounded scope only; broader condition/all-source, travel/Expedition, rest reward, class grant and human balance gates remain open.

'''
text+=f"Validation: {report['status']}; {report['checks']} total checks ({report.get('transitionChecks',71)} transition checks plus30 source checks); {report['maximumHpInvariantStates']} maximumHP scenarios.\n\n"
for rel in ['docs/mechanics/STRAIN_PLAYTEST.md','tools/strain_playtest_rules.py','tools/validate_strain_playtests.py']:
    text+=f'\n# EXACT FILE {rel}\n\n'+(ROOT/rel).read_text(encoding='utf-8')+'\n'
(AUDIT/'CODEX_STRAIN_EXACT_REVIEW.md').write_text(text,encoding='utf-8')
print(f'Built exact Strain review packet: {len(text)} characters')
