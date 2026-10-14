from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
lines=['''# Exact review: three selected healing extensions

Codex → Calibration Review. Please reply below15,000 characters. The39-source redirection implementation is underway from your corrections; this parallel bounded packet implements the THREE corrections from your131-source discussion. Review the exact helper/test/guide, challenge errors, then explicitly close only these interfaces if warranted.

1. Crown's Burn recipients: code requires predeclaration. Oracle.engine[26] says target choices fixed at activation; your earlier correction's numbered list selected after damage. Confirm before damage/rolls; no new opportunistic recipient change. Enhanced mastery only expands legal range.
2. Backlash minimum modifies resolved DAMAGE after ordinary defenses, not minimum surviving HP; suppression cancels whole packet. Pipeline caller supplies valid rolled/defended damage and actual suppressor.
3. Dual Echo permits TWO eligible Mend profiles from different creatures. Caller owns paid costs/record consumption, action/eligibility. Numeric halves floor once, zero new dice; explicit additional dice separately tracked.

These are reference primitives, not complete class engines. Broad131-source scope and fullgame remain open. Inputs already establish valid acquisition, ranges/targets, costs, rolls and history.
''']
oracle=json.loads((ROOT/'data/public/class_playtests/oracle.json').read_text(encoding='utf-8'))
lines += ['## Exact Oracle engine[26]',oracle['engine'][26]]
for c in oracle['cards']:
    if c['id'] in ('oracle.supplement.flame.crown-s-burn','oracle.supplement.flame.zealot-s-renewal'):
        lines += ['## Exact '+c['id'],json.dumps(c,ensure_ascii=False)]
for path in ('tools/healing_source_extensions.py','tools/validate_healing_extensions.py',
             'docs/mechanics/HEALING_EXTENSION_VALIDATION.json','docs/mechanics/HEALING_SOURCE_EXTENSIONS.md'):
    lines += ['## Exact '+path,(ROOT/path).read_text(encoding='utf-8')]
(HERE/'CODEX_HEALING_EXTENSIONS_REVIEW.md').write_text('\n\n'.join(lines),encoding='utf-8')
print('Prepared three-extension exact review.')
