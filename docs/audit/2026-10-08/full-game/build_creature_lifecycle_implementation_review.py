from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
path=ROOT/'data/playtest/creature_lifecycle_bindings.json'
data=json.loads(path.read_text(encoding='utf-8'))
data['status']='IMPLEMENTED CANDIDATE; exact selected-interface review pending; incidental form/tempHP effects deferred'
data['scope']='100 exact five-family candidates:83 original passages plus17 semantic supplements;5 frozen supporting paragraphs (3 original plus2 targeting/hard-denial supplements). Only supplied lifecycle/command/guard roles, not complete classes.'
for row in data['bindings']:
    cls=row['classification'];ident=row['bindingId']
    row['status']='DISCUSSED / deferred full-effect work' if cls.startswith(('FORM','THP')) else 'SOURCE-AUDITED / implemented role candidate; review pending'
    row['reviewEvidence']=list(dict.fromkeys(row['reviewEvidence']+['GPT_CREATURE_LIFECYCLE_BOUNDARIES.md','GPT_CREATURE_LIFECYCLE_EVENT_BOUNDARIES.md']))
    row['operationalOverrides']=[
        'CREATURE_LIFECYCLE_PLAYTEST.md defines this source role. Later boundary and event replies supersede the initial conference. Exact original text remains preserved.',
        'Incidental form/tempHP, damage riders, acquisition guards and earlier-reviewed interfaces are classifications/dependencies, not newly complete card execution.']
    row['openIssues']=['Exact implementation review pending. Remaining card effects, full forms/tempHP and broader catalogs are outside this supplied role.']
    if ident in ('mirrorsage.base.charm-creature','mirrorsage.engine[4]'):
        row['classification']='LC / NEW Reflective hard-denial and future Action reservation; not part of earlier219 control closure'
        row['operationalOverrides'].append('At most one forced Action under shared character-target-encounter guard; current-round BA, future-round offense reservation; no fallback compelled Actions.')
    if ident in ('wizard.engine[21]','wizard.engine[22]','wizard.engine[23]'):
        row['openIssues'].append('Wizard elite acquisition/binding/return source is genuinely absent; no public create/bind/return operation.')
    if cls.startswith(('FORM','THP')):
        row['openIssues'].append('Full form/Buffer Reserve/tempHP work remains deferred; only its stated dependency/guard is discussed here.')
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
header='''# Exact creature lifecycle implementation review

Codex → Calibration Review. All100+5 source roles and your three conference replies are preserved. Please review the actual implementation below; reply below15,000 characters with specific counterexamples before disposition. Original cards/books/frozen class guide unchanged.

105 targeted checks and2,800 Ranger wounded-conversion/capacity states pass. Existing device132/1,200 suite also passes after extending the SAME CommandLedger with control offense and Reflective reservations. This is a bounded tabletop/engine reference, not a complete runtime or whole-class certification.

Implemented: source-owner provenance and snapshots/dynamic HP; finite summons/dependencies; Ranger real bond/death/HP-only state; Mage same-asset Lich return; Wizard standard body/cap/Auto-Raise checkpoint; shared attached commands/Ghoul Lash; Reflective future reservations/hard guard; atomic immediate Mirror-origin Echo. Wizard elites expose a schema/cap check only; no binding/create/return. Full forms/tempHP and complete on-hit damage/control effects are explicitly deferred.

Canonical integration boundaries: caller certifies actual source access, correct legal range/space/LOE/perception/conditions, rolls/saves, existing consent/quest/acquisition, real Form Surge payment, exact absolute/virtual endpoints, concentration, source recharge/use keys, actual completed rests, current eligible modifier records and one shared wallet/command/hard-denial/Echo ledger across ALL features. The helper validates its supplied state/cost/cap/identity transitions; caller must not mint new wallets/use scopes per feature. Effects persist if their own source predicates allow; expired effects still require canonical expiry processing.

Please focus on:
1. CommandLedger compatibility across devices/control/damage and reserved future offense. Reflective cancels unused offense on concentration/capability/legality/hard-guard changes while keeping issued BA. Actual regular Action slot only; no second whole-Action compulsion/fallback.
2. Auto-Raise's non-turn attached checkpoint, automatic first qualifying trigger, reservation cap, real body ownership, failed-spent opportunity, dead-killer survival and absolute creation-round action bar. Invalid modifier preflight is atomic; no Conjuration bonus on Auto-Raise.
3. Same-asset Mage return/current stats/clock preservation versus real Ranger death/bond/rest distinction. One preserved real body identity presently avoids fragment/repeated-death material records; full corpse/resurrection cleanup remains later-source work. Flag if this bounded choice itself conflicts with exact supplied source.
4. Guide distinguishes implemented lifecycle APIs from caller-owned rolls/condition riders/zone ticks. Miasma finite ticks reuse the prior periodic model without new commands; Wraith attack/control events must notify original marker state. No blanket full-card claim from classification.
5. Finite snapshot stats/current original source owner, dynamic Ranger and elite maxima, maxHP ledger integration, actual controller exception solely for eligible Flesh Ascendant records.
6. Mirror-origin immediate owner Action+BA/cap/record/RP preflight, local Beast option, no automatic senses/movement and no offensive-companion debit. Actual extra own turn legal only with genuine Action/BA/caps.

If correct, explicitly dispose of the SELECTED100+5 lifecycle/command/guard classifications with form/tempHP/full-card and named evidence gaps remaining open. If defects exist, provide the smallest concrete correction. Do not equate source integrity with semantic approval.

'''
parts=[header]
for name in ('docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST.md','tools/creature_lifecycle_playtest_rules.py',
             'tools/validate_creature_lifecycle_playtests.py','docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST_VALIDATION.json',
             'docs/mechanics/CREATURE_LIFECYCLE_SOURCE_VALIDATION.json','tools/device_lifecycle_playtest_rules.py'):
    parts+=['## '+name,'',(ROOT/name).read_text(encoding='utf-8'),'']
parts+=['## All100 source roles','',json.dumps(data,ensure_ascii=False,indent=2),'']
source=json.loads((HERE/'CREATURE_LIFECYCLE_SOURCE_CANDIDATES.json').read_text(encoding='utf-8'))
supports=source['supportingSources']+json.loads((HERE/'CREATURE_LIFECYCLE_SUPPORTING_SOURCES.json').read_text(encoding='utf-8'))['supportingSources']
parts+=['## Five exact frozen supports','',json.dumps(supports,ensure_ascii=False,indent=2),'']
(HERE/'CODEX_CREATURE_LIFECYCLE_IMPLEMENTATION_REVIEW.md').write_text('\n'.join(parts),encoding='utf-8')
print('Built exact100+5 creature implementation review, retaining deferred scope.')
