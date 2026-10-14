"""Generate a readable, source-linked working reference from reviewed bindings."""
from pathlib import Path
import json
import os

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]
OUT=ROOT/'docs/mechanics/CUSTOM_CONDITION_BINDINGS.md'

def link(path,label,base=ROOT):
    relative=os.path.relpath(base/path,OUT.parent).replace('\\','/')
    return f'[{label}]({relative})'

def source_line(s):
    if s['kind']=='card':
        return link(s['path'],s['cardId'])
    if s['kind']=='engine':
        return link(s['path'],f"{Path(s['path']).stem} engine[{s['engineIndex']}]")
    if s['kind']=='core-condition':
        return link(s['path'],f"Core condition: {s['conditionId']}")
    return link(s['path'],f"ordinary spell: {s['spellId']}")

def main():
    p=json.loads((ROOT/'data/playtest/custom_condition_bindings.json').read_text(encoding='utf-8'))
    lines=['# Custom condition and rider bindings — working playtest reference','',
        '**Status: IN PROGRESS.** These source-qualified rules are provisional integration decisions. They preserve the original class and spell cards; they do not establish that all 1,223 class cards, all spells, or all game systems have completed semantic review.','',
        f"This reference currently contains **{len(p['definitions'])} definitions and {len(p['hooks'])} feature interfaces**. Machine checks verify source references and selected interactions, not encounter balance or human table readiness.",'',
        'Use the [generic conditions](CONDITIONS_PLAYTEST.md) and [recovery procedures](CONDITION_RECOVERY_PLAYTEST.md) alongside this reference. Source text, timing, costs, targets and concentration remain applicable. A family tag supplies only its explicitly documented recognition/cure/immunity interface. It never imports every member\'s effects.','',
        '## Bounded reviewed scopes','']
    for scope in p.get('completedScopes', []):
        lines += [f"**{scope['name']}: {scope['status']}.** {scope['scope']}", '',
                  'Review: '+link(scope['reviewEvidence'],'GPT disposition',GAME)+'.','']
    if p.get('pendingScopes'):
        lines += ['## Candidate corrections under implementation review','']
        for scope in p['pendingScopes']:
            lines += [f"**{scope['name']}: {scope['status']}.** {scope['scope']}",'',
                      'Source conference: '+link(scope['reviewEvidence'],'GPT proposal',GAME)+'.','']
    lines += ['## Shared interpretation','']
    for rule in p['familyRules']:
        lines += [f"**{rule['id']}.** {rule['rule']}",'']
    lines += ['**Application records.** Preserve application ID, owner character, source class/engine, target, DC, damage type, start, remaining ticks or expiry, source stack group, and cure exceptions. “Immune” in an active-effect eligibility check means immunity to the condition/application, not merely immunity to its damage type. Damage immunity does not by itself erase an effect.','',
        '**Timing.** Explicit start/end timing wins. An omitted next-turn periodic marker is provisionally end of the next regular target turn. Extra turns add no periodic ticks or ending saves. Outside initiative preserve the clock and consume one due step per complete six seconds; initiative transitions do not duplicate events.','',
        '**Bleed treatment.** A WIS (Medicine) Action by self or an adjacent helper selects one ordinary Bleed record before rolling: printed cure DC, otherwise recorded applying effect/class/spell DC, otherwise 10. Success ends that record. One legal magical-healing event with positive pre-cap/pre-prohibition potential ends every eligible automatic-healing-cure record; each Blood Curse instead receives its own CON save. An explicit remover keeps its stated one/all/owner scope.','',
        '**Cure presence.** Treatment, magical-healing cure and permitted per-record ending saves can remove a still-present suppressed or condition-immune Bleed/fire record. Cure scope and special prerequisites remain unchanged. Effect eligibility and damage arbitration still exclude suppressed records. Successful removal ends the record permanently; immunity ending cannot restore it.','',
        '**Kit exceptions.** A Crimson kit Action consumes one use and ends that source owner\'s Crimson Bleeds on the victim. A Dragoon kit Action consumes one use and ends the selected Dragoon Bleed. Other records do not silently acquire these kit endpoints.','',
        '**Attached fire treatment.** One self/helper extinguish Action or full immersion ends all ordinary-extinguishable attached fires on that creature. Explicit protected-fire exceptions survive. At the end of each regular target turn, after due ticks are consumed, each still-active fire record with future ticks remaining receives its own ending DEX save at its source DC or 10. An indefinite generic fire has future ticks. No ending save is needed after a record\'s final tick expires.','',
        '**Duration changes.** Printed base duration is distinct from an express hard cap. A qualifying refresh never shortens remaining duration. Persistent Bleed normally supplies two turns; Prolonged Suffering changes application/refresh to four only for owned profiles whose printed base is exactly two. Use the greatest legal replacement, not a sum; obey actual hard caps. No source trigger means no refresh, and expired records cannot be refreshed.','',
        '## Periodic effect lookup','',
        '| Mechanical identity | Damage | Regular target marker | Base ticks | Source stack group |',
        '|---|---|---|---:|---|']
    for d in p['definitions']:
        if 'periodic' in d:
            t=d['periodic']
            ticks='indefinite' if t['ticks'] is None else t['ticks']
            lines.append(f"| `{d['mechanicalId']}` | {t['dice']} {t['damageType']} | {t['marker'].split('.')[-1]} | {ticks} | `{t['stackGroupTemplate']}` |")
    lines += ['', 'The table gives base profiles. Printed eligibility, saves, instance exceptions and reviewed duration upgrades still apply. Ashblood is deliberately outside the ongoing-fire family. The ordinary spell named Elemental Bolt is separate from the Mage class card and gains no class-card rider merely from a matching name.','', '## Feature interfaces','']
    for h in p['hooks']:
        lines += [f"### {h['id']}",'',h['rule'],'', 'Sources: '+', '.join(source_line(s) for s in h['sourceReferences'])+'.','']
    lines += ['## Bound definitions','']
    for d in p['definitions']:
        lines += [f"### {d['displayName']} — `{d['mechanicalId']}`",'',
            d['effect'],'',f"**Ending:** {d['ending']}",'',f"**Stacking:** {d['stacking']}",'',
            f"**Immunity:** {d['immunityRule']}",'',
            '**Tags:** '+(', '.join(f'`{t}`' for t in d['familyTags']) or 'No shared family tag.') ,'']
        if d.get('integrationDecisions'):
            lines += [str(n) for n in d['integrationDecisions']]+['']
        if 'cure' in d:
            lines += ['**Exact cure metadata:**','', '```json',json.dumps(d['cure'],ensure_ascii=False,indent=2),'```','']
        lines += ['Sources: '+', '.join(source_line(s) for s in d['applicationSources'])+'.','',
                  'Review: '+', '.join(link(e,Path(e).stem,GAME) for e in d['reviewEvidence'])+'.','']
    lines += ['## Open integration work','']+[f'- {x}' for x in p['openIssues']]+['',
        'The [machine report](CUSTOM_CONDITION_BINDING_VALIDATION.json) explicitly separates source integrity from selected interface checks and preserves this unfinished registry status.','']
    OUT.write_text('\n'.join(lines),encoding='utf-8')
    print(f'Generated working reference: {len(p["definitions"])} definitions, {len(p["hooks"])} hooks.')

if __name__=='__main__':
    main()
