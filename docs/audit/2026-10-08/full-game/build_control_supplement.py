"""Preserve an explicitly selected semantic follow-up; do not alter original packet."""
from pathlib import Path
import json, hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
selected={
 'crimson-agent':['veinjammer'],
 'dragoon':['drakestorm-dive','elemental-lance'],
 'mage':['elemental-bolt','cold','elemental-mastery','elemental-surge','elemental-fusion','cascade-storm','undying-spellform'],
 'monk':['echoing-guard','pressure-point-strike'],
 'oracle':['ledger-s-command','bones-revelation-mastery','tremor-sense','shardburst','gale-of-unmaking','seal-s-fracture','slumber-glimpse','resonant-seed','moment-s-pause','the-spiral-opens'],
 'paladin':['black-manifestation','law-s-weight','decree-of-submission','echo-of-ages','standing-stone','iron-leash-aura','reign-of-ashes','royal-decree'],
 'shaman':['elemental-affinity','elemental-chorus','balanced-elements'],
 'thief':['vein-cutter','crippling-lash'],
 'warrior':['brutal-strike','hypermutation-spike','stonecore','mutation-overload'],
}
rows=[]
for owner,suffixes in selected.items():
 p=ROOT/f'data/public/class_playtests/{owner}.json'
 d=json.loads(p.read_text(encoding='utf-8'))
 for c in d['cards']:
  if c['id'].split('.')[-1] in suffixes:
   rows.append({'kind':'class-card','owner':owner,'path':str(p.relative_to(ROOT)).replace('\\','/'),'card':c,
    'sourceObjectSha256':hashlib.sha256(json.dumps(c,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()})
packet={'status':'SOURCE_CANDIDATES_ONLY','scope':'Explicitly selected omitted Speed/control sources and relevant self-penalty/immunity boundaries; supplements original 179 without claiming game-wide completeness.','recordCount':len(rows),'records':rows}
(HERE/'CONTROL_STATE_SUPPLEMENT_SOURCE_PACKET.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
header='''# Control-state counterexamples and exact missing sources

The first 179-source response is preserved. I agree with the bounded namespaces, strongest hostile soft-control arbitration, distinct system penalties, ownership, component suppression, and regular expiry/save clocks. Before implementing, resolve these actual edges against the exact objects below. These are a semantic supplement, not a completeness claim.

1. Mage Cold now supplied: exact Cold Focus, Bolt, Surge, Arch Mastery, Hero Mastery, Fusion and Cascade. Confirm the NEW Glacier half-then-5 formula only for Arch Mastery, not Hero Mastery. Cold passive requires actual positive damage; Bolt's cold rider is on a hit even if cold damage becomes zero; Surge says on hit applies Focus reduction. On successful Glacier save with actual damage, passive -10/-15 applies; on failure both passive and Glacier profiles can apply but choose strongest independent result within one owner Focus group, never add. At preSpeed10, ordinary -15 ->0 beats Glacier half-5 ->0; at preSpeed5 unmastered passive-10->0 beats half->2. Do not let replacement by a weaker same-group profile make someone faster while a stronger unexpired application exists. Keep independent candidate expiries (or equivalent magnitude-specific subrecords) within one effective group. At expiry of stronger profile, weaker remaining profile resumes. Does passive Cold also trigger on the Cold damage component of non-Focus-tagged Fusion/Cascade while their printed secondary riders remain separate non-Mastery profiles? Clarify current selected Cold Focus prerequisite and off-Focus finisher permission versus granting other Focus passives.

2. NEW hostile-soft arbitration is across actual adverse control records regardless of allied/self inflictor; voluntary serum side effects, Oracle backlash, Strain, cargo, and form mobility limits stay separately governed systemic modifiers. Iron Leash Aura says minimum5; use min(preControlSpeed,max(5,preControlSpeed-10)) so it never raises Speed3 to5. Hypermutation Spike half-normal floor must be defined against these and Speed0/Grappled/Restrained/Exhaustion. Define normal Speed baseline without recursive bonus calculation, which restrictions it beats, and what it does not bypass. If unresolved, explicitly defer only that binding, not silently ignore it.

3. Exact Monk Echoing Guard and Warrior Brutal Strike both explicitly define Staggered as -1 attacks/-5Speed. Core Staggered is Guard removal and one forced-move extension. They were not in the current 57 custom records. Propose distinct monk.echoing-guard.stagger and warrior.brutal-strike.stagger IDs (same display, independent sources), neither silently adds Core Staggered. Same-name/source repeated applications refresh; -1 attack nonstack across those two unless expressly otherwise; Speed follows arbitration. Confirm a shared eligibility hook only if an actual reader requires it. Do not alter original cards.

4. First response Divine Judgment said regular-turn damage reflection, but only repeat-save/expiry clocks have established regular-only behavior. Card says first damage on each of target's turns. Decide explicitly if an extra turn can trigger reflection once on that turn; off-turn damage triggers none. Do NOT broaden regular-only convention to all own-turn attack/passive triggers globally. Zero actual damage triggers none despite minimum1. Multiple victims in one simultaneous attack: is first event stable application order/target declaration order, or summed? Provide one deterministic bounded rule.

5. Guiding Bolt mark: your proposal spends +2 on first qualifying ally attack, even miss. If that attack misses, does a later ally hit still add S and consume mark, or is inert mark all that remains? Recommend two riders: next ally ATTACK gets +2 once; next ally HIT before expiry adds S once and consumes mark. This is NEW clarification; no bonus backfill, repeated attacks don't regain+2. Reapplication refreshes/reset new paid opportunity without stacking. Wrathful Brand: ally heal explicitly once/Brand; clarify whether WIS/-1 rider is also once or every ally damage. Recommend one shared ally-trigger entitlement once/Brand (existing first response), eligible with positive damage; heal prohibition doesn't refund it. Owner's 'next damaging attack you hit' requires positive actual total attack damage before bonus, not hypothetical dice from fully immune hit. Drake Mark says first subsequent direct polearm HIT so consumes even if damage zero. Soldier first HIT damage reducer likewise spent on that hit. Tinker scanner next ATTACK consumes on roll. Please accept or correct.

6. Corpse reuse: Carrion Conductor new corpse lock is independent of mark expiry/suppression; record source-specific corpse used history, not all corpse mechanics. Disease immunity classification never cures, duration/progression clocks continue; confirm suppressed lethal endpoint needs individual source rule (do not resurrect or universally prevent endpoint death by hiding penalty). Detection does not infer classification from name/flavor.

7. Physical restraint fallback eligibility: a fixed endpoint alone excludes it under your proposal; that's an explicit NEW restriction, preserve it. No generic helper/cutting bypass for magical-only restraints. Distinguish magical earth anchored to surface (Earthen Grip ends when source surface relation broken?) from unspecified attached magic; do not invent teleport escape without relation rule. For suppressed Grapple/Restrained whose source requires reach, if target then moves out of required reach, source ends rather than coming back after immunity ends. Physical net retained when suppression ends before printed expiry if still attached.

8. Control composites/hard guard: confirm a consumed guard prevents only future hard component while still allowing printed soft fallback, not substituting one when absent. Address new omitted command/denial sources (Oracle Ledger, Moment's Pause, Slumber, Spiral; Paladin Decree, Echo of Ages, ash teleport ban). 'Until end next turn' without specified creature remains source next regular turn per combat convention; printed 'target/its' uses target. Distinguish per-round entry pulses from repeating saves. Generic source registry is not full spell/command automation.

Please give explicit dispositions for all attached IDs, with source-qualified IDs/clock/stacking/escape where relevant, then focused answers to eight issues. No source deletion or broad DD16 closure.

## Exact normalized source cards
'''
brief=[{'kind':r['kind'],'owner':r['owner'],**{k:r['card'].get(k) for k in ('id','name','activation','cost','rangeAndTarget','duration','frequency','effect','prerequisite')},'sourceObjectSha256':r['sourceObjectSha256']} for r in rows]
(HERE/'CODEX_CONTROL_COUNTEREXAMPLES.md').write_text(header+'\n```json\n'+json.dumps(brief,ensure_ascii=False,indent=2)+'\n```\n',encoding='utf-8')
print(f'{len(rows)} exact supplemental cards')

