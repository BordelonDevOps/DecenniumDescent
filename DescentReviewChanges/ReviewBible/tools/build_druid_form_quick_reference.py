"""Readable projection of existing profiles; adds no mechanics."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def main():
    data=json.loads((ROOT/'data/playtest/druid_form_profiles.json').read_text(encoding='utf-8'))
    lines=['# Druid form quick reference','',
           'Use this alongside [Forms and temporary HP](FORM_TEMP_HP_PLAYTEST.md). This table is a view of the 26 existing source profiles, not a grant of every form or a substitute for their complete riders. The linked guide records the current review status.','',
           'Keep your own HP, abilities, saves, proficiency and conditions. One Action makes one listed natural attack; use PB + actual WIS to hit and the current Druid DC for saves. The table shows the basic attack before conditional riders. No separate beast HP or imported monster stat block.','',
           '**Entry:** Bonus Action + one shift use below level 20; ten minutes. At the natural endpoint, same-form renewal costs another shift use below 20 but no Bonus Action, preserving the instance and its limits. Early reversion costs a Bonus Action. Natural attacks never reset Refrain.','',
           '**Reserves:** record Buffer Reserve = 2 × Druid level + M and Form Surges = PB at a completed long rest. Form changes do not refill either. Bear/Earth entry offers spend Reserve even if a larger existing shield wins.','',
           '**AC:** N means legal AC from components still operative while transformed. Melded armor/shield calculations and unclassified item bonuses are excluded. Apply the exact formula below without adding armor again.','',
           '**Access:** all five Base forms at level 1. Circle forms require the named chosen Circle and printed gate. The five Arch forms require level 11 and attunement to at most two at a completed long rest. Base forms cannot speak; Arch/Hero forms can. Gear melds.','',
           '| Form | Access | Size | Movement (feet) | AC | Basic natural attack | Entry shield |',
           '|---|---|---|---|---|---|---|']
    for ident,p in data['profiles'].items():
        src=p['sourceProcedure'];name=src['name'];access=f"Level {p['minimumLevel']}"
        if p['circle']:access+='; '+p['circle']
        if p['archAttunement']:access+='; attuned'
        size=p['size']+('/Large if space permits' if p['mayLarge'] else '')
        movement=', '.join(k+' '+str(v) for k,v in p['movement'].items())
        if p['hover']:movement+='; hover'
        if ident.endswith('elemental-shapeshifting'):movement+='; Air fly 60 / Earth burrow 20 loose soil / Water swim 60'
        if ident.endswith('master-of-vermin'):movement+='; bat subtype fly 30 instead of physical resistance'
        a=p['ac'];mode=a['mode'];n=a['amount']
        ac=f'max(N, {n})' if mode=='floor' else f'N + {n}' if mode=='add' else str(n) if mode=='fixed' else 'N'
        attack=p['attack']['damage']
        if p['attack']['damageType']!='mixed':attack+=' '+p['attack']['damageType']
        if ident.endswith('elemental-shapeshifting'):attack='2d8 + WIS; Air lightning / Earth bludgeoning / Fire fire / Water cold'
        shield=f"Up to {p['entryBuffer']} from Reserve; ends with form" if p['entryBuffer'] else '—'
        lines.append('| '+' | '.join((name,access,size,movement,ac,attack,shield))+' |')
    lines+=['','## Specials retain their own costs','',
            '| Form | Named special | Payment and limit |',
            '|---|---|---|']
    for ident,p in data['profiles'].items():
        for special,q in p['specials'].items():
            action=q['action'] or 'Attached rider or entry event'
            payment={'surge':'1 Form Surge; once per instance for this special',
                     'recharge2':'Recharge 2; owner/source clock across all forms',
                     'short-rest':'1 per short/long rest, shared across all instances',
                     'long-rest':'1 per long rest, shared across all instances'}[q['payment']]
            lines.append('| '+p['sourceProcedure']['name']+' | '+special.replace('-',' ')+' | '+action+'; '+payment+' |')
    lines+=['',
            'Elemental Shapeshifting additionally spends one of two long-rest entry uses. Same-subtype natural renewal spends no additional elemental entry use. Changing subtype is a new form entry.','',
            'Broodmother spawning is optional and only available during entry; declining or failing its preflight does not leave a later spawn window. Its critical-negation is separate. Frost resistance bypass must attach to an actual legal Breath; the wet bonuses attach to actual qualifying attacks. These riders do not grant another Action or attack.','',
            'Mooncursed ally and enemy Howls share one opportunity. For allies, choose/order up to three before the shared 2d8 roll; spend Reserve sequentially for each entire offer. Accepted ally shields survive reversion and use the recipient long-rest default.','',
            'The complete source effects include senses, defenses, saves, charge/first-hit bonuses, auras and movement restrictions omitted from these compact tables. Apply their exact wording in [all form profiles](../../data/playtest/druid_form_profiles.json) and the [source register](FORM_TEMP_HP_SOURCE_BINDINGS.md). Natural/form attacks do not automatically qualify for unrelated weapon-only effects.','']
    path=ROOT/'docs/mechanics/DRUID_FORM_QUICK_REFERENCE.md';path.write_text('\n'.join(lines),encoding='utf-8')
    print('Rendered26 Druid forms and their source-special cost table; no new rules.')
if __name__=='__main__':main()
