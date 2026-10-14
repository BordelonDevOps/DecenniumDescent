#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
component=(ROOT/'src/components/ExpeditionTracker.tsx').read_text(encoding='utf-8')
lib=(ROOT/'src/lib/gameplay-loop.ts').read_text(encoding='utf-8')
errors=[]
checks={
 'roster hard cap':'state.members.length >= 12',
 'imported roster truncation':'slice(0, 12)',
 'Rest Debt countdown':'restDebtDueIn',
 'Additional Action guard':'additionalActionAllowed',
 'linear party multiplier':'1 + 0.2 * difference',
 'Extraction Class in DC':'highestExtractionClass',
 'reputation access helper':'reputationAccess',
 'Heat-zero bribe guard':'if (current === 0) return 0',
 'insurance payout helper':'insurancePayout',
}
for label,token in checks.items():
    if token not in component and token not in lib: errors.append(f'Missing state invariant: {label}')
if 'Math.pow(1.2, difference)' in lib: errors.append('Encounter party-size scaling still compounds exponentially')
if 'Rest debt {member.watchesWithoutRest}/3' in component: errors.append('Obsolete Rest Debt /3 UI remains in component')
if errors:
    print('Gameplay state validation: FAIL'); [print(f'- {e}') for e in errors]; sys.exit(1)
print('Gameplay state validation: PASS - roster, Rest Debt, action, extraction, Haven guards present')
