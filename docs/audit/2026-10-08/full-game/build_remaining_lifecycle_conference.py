from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
data=read(HERE/'REMAINING_LIFECYCLE_CONFERENCE_SOURCES.json')
supports=read(HERE/'CREATURE_LIFECYCLE_SOURCE_CANDIDATES.json')['supportingSources']+read(HERE/'CREATURE_LIFECYCLE_SUPPORTING_SOURCES.json')['supportingSources']
header='''# Remaining class lifecycle source conference — prepared, not yet sent

Codex → Calibration Review. This is the next80-source slice:74 remaining original lexical candidates plus6 explicit semantic supplements. Please classify every supplied ID, resolve the listed source-specific questions, preserve all source text, and label NEW integration decisions. Do not infer full-card closure from incidental mention. TemporaryHP and full forms remain a dedicated later corpus review; this packet focuses remaining summons, controlled creatures, spirit manifestations and Soldier structures.

The exact earlier source-qualified healing/control decisions are included at the end so those pieces are not silently reopened. No earlier redirection transfer binding was found for Oracle Ledger interception; that interface needs its own precise incoming-attack contract. Five frozen shared paragraphs are supplied. No invented named powers/spells and no material deletion.

Please reply below18,000 characters. Give a grouped source-ID classification table, clear operational boundaries for actual lifecycle cards, and genuine evidence gaps. This is discussion before code, not approval of a complete runtime or all nine families.

'''
parts=[header,(HERE/'REMAINING_LIFECYCLE_QUESTIONS.md').read_text(encoding='utf-8'),'']
for r in data['classRecords']:
    if r['kind']=='class-card':
        c=r['card'];ident=c['id'];proc={k:c.get(k) for k in ('name','activation','cost','rangeAndTarget','duration','frequency','effect','prerequisite')}
    else:ident=f"{r['owner']}.engine[{r['engineIndex']}]";proc={'text':r['text']}
    parts+=['## '+ident,json.dumps(proc,ensure_ascii=False),'']
parts+=['## Frozen shared support',json.dumps(supports,ensure_ascii=False),'']
wanted={'oracle.supplement.bones.ledger-s-command','cleric.hero.cultist.rite-of-the-crimson-choir',
        'cleric.hero.cultist.ritual-of-undeath','paladin.supplement.oath-of-grief.echo-of-the-fallen'}
for name in ('control_state_bindings.json','healing_death_bindings.json'):
    rows=[r for r in read(ROOT/'data/playtest'/name)['bindings'] if r.get('sourceId') in wanted]
    parts+=['## Prior component dispositions: '+name,json.dumps(rows,ensure_ascii=False),'']
out='\n'.join(parts)
(HERE/'CODEX_REMAINING_LIFECYCLE_CONFERENCE_PREPARED.md').write_text(out,encoding='utf-8')
print(f'Prepared80+5 discussion packet:{len(out)} characters; not sent.')
