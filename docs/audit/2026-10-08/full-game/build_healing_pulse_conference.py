"""Build exact source conference without changing original class records."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
data=json.loads((HERE/'HEALING_PULSE_SOURCE_CANDIDATES.json').read_text(encoding='utf-8'))
header="""# Healing pulses, zones and upkeep conference

Codex → Calibration Review. Maximum-HP exact review closure is recorded (58 sources;60 checks/909 states); Rewind historical damage predicate and Flesh Ascendant runtime alias caveat retained. No original sources changed.

Next bounded discussion:100 lexical class candidates below. Many are guards, earlier-reviewed regeneration/flat bonuses, or non-healing zones. Please classify EVERY supplied ID in a compact table, distinguish native passive recurrence, action-paid pulses, target-start funded windows, finite installments, already-reviewed guards and excluded single-use/repair effects. Do not invent a uniform three-pulse limit for passives. This is source discussion before implementation. Keep reply under18,000 characters; concise per-ID table plus shared rulings is best.

Resolve these source-sensitive questions with explicit NEW labels where needed:

1. Exact initial and later payments/actions: Lifewell's FIRST pulse already costs BA+1RP beyond activation; Renewal/Briar/Harmony/Restoration first included then BA+1RP. Oracle engine26 vs Garden/Song/Finals and Paladin engine11 need precise distinct schedules.
2. Funded window versus per-target cost: Garden target-start healing uses activation window1, source-next-regular-start1RC for windows2/3? Crown Restored target-start maximum3 and Final included payments? Song exactlyactivation+nextregularstart, nottargetstart? Eternal Bloom fixed3 reserve installments.
3. Define source regular-turn/target-start windows, missed upkeep endpoint (Lifewell source-end explicit), extra turns, source incapacity/unconsciousness/concentration loss, suppression, and clocks outside initiative. Do paid BA zones end immediately if skipped, or at own end and cannot resume? Does max3 count scheduled opportunities regardless actual gain?
4. Target identities: fixed at activation for Oracleengine26/Lifewell explicitchosenallies; other pulses repick≤3 when no fixed wording? How do chosen targets leaving/re-entering, death, enemy classification, zone movement and per-creature/round ledgers work? A blocked heal/zero actualgain still spends its paid opportunity; no replacement after dice/blocked outcome?
5. Renewal upgrade4thpulse, Echo Totem half arithmetic/shared parent upkeep/lifetime and same-name nonstack. Are parent and Echo same pulse for once/round and target cap, how choose strongest coverage without double healing, and what happens if parent destroyed? Totem movement/other BAs compete; cannot create entry healing. Keep non-Renewal Totem Pulse distinct.
6. Eternal Bloom reserve snapshot: three integer installments/remainders, missing/outside/dead targets lose scheduled share rather than bank? Suppression does not extend clocks; source-independent target clocks? One floor perally distinct from installments. Garden first-entry/start cure is independent of HP gain and differs from healing pulses.
7. Cleric passive Aura of Grace and Mutation regen retain source cadence/cost rather than genericthreecap. EfficientPowerCells/MechOverdrive extend duration only where allowed, never RestorationField3pulses or free recharges; disabled devices do not pause clocks.
8. Propose coherent per-instance record and eligibility/budget commit ordering for source/target/round/pulse IDs; retain previous healing graph, strongest flat modifiers, blocked-gain cure independence and exact clocks. No broad copy/companion/control runtime closure.

Please expose missing supporting source evidence rather than guessing; candidate extraction is lexical, not proof every zone in all game catalogs was supplied.

## Exact source procedures
"""
lines=[header]
for r in data['classRecords']:
    if r['kind']=='class-card':
        c=r['card'];ident=c['id'];proc={k:c.get(k) for k in ('name','activation','cost','rangeAndTarget','duration','frequency','effect')}
    else:
        ident=f"{r['owner']}.engine[{r['engineIndex']}]";proc={'text':r['text']}
    lines += ['### '+ident,'',r['path'],'',json.dumps(proc,ensure_ascii=False,indent=2),'']
(HERE/'CODEX_HEALING_PULSE_CONFERENCE.md').write_text('\n'.join(lines),encoding='utf-8')
print('Prepared',len(data['classRecords']),'exact candidate source passages.')
