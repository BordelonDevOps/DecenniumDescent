import json,hashlib
from pathlib import Path
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game';D=R/'data/playtest/spell_drafts'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
src=read(D/'candidate_enchantment_rank2_sources.json'); rows=src['spells'];cat=read(R/'data/public/spell_playtests/catalog.json')['spells'];by={s['id']:s for s in cat}
assert len(rows)==7 and sum(len(s['sourcePlacements']) for s in rows)==8
for s in rows:
 c=by[s['id']]
 assert not c['operational']
 assert s['sourcePlacements']==c['source']['original']['placements']
 assert s['sourceCoreEntries']==c['source']['coreEntries']
 assert s['classAccess']==c['classAccess']
 assert s['possibleHistoricalAliases']==c['source']['possibleHistoricalAliases']
common=rows[1]['classAccess']
compact=[]
for s in rows:
 x=dict(s)
 if x['classAccess']==common:x['classAccess']='SHARED_ENCHANTMENT_ACCESS'
 compact.append(x)
questions="""# Seven rank-two Enchantment identities — source conference preparation

This packet is source evidence and questions, not an authored or selectable batch. Return complete draftable rulings for all seven, marking NEW completions explicitly. Exact cards will return separately before promotion. All eight placements/Core blocks and actual access are retained. Do not infer familiar spell rules from another game.

1. Deep Mesmerize: preserve real Stunned for two rounds OR until damaged. Action30/V,S,F/base3RP; raw duration Instantaneous conflicts with explicit continuing effect. Need NEW save or express no-save decision, target count, concentration decision, exact damage trigger (positive post-defense packet versus numeric HP loss) and immunity/guard handling. Unlike Mesmerize, no separate unaware rider is printed. Two target-round deadline means second future regular END, excluding entire current target turn; twelve elapsed seconds outside initiative unless a different explicit decision. Do not retroactively undo the attack that wakes it, restore ended concentration, replay dropped-item/Prone events or grant unprinted condition components.

2. Dire Charm: target becomes loyal servant for one minute, WIS save at each turn END. Preserve actual service/control rather than dilute it to a social-check bonus. Define initial save, concentration (not printed), legal targets and actual command procedure: hearing/language/range at application or each order, command action cost, target timing, default behavior when no order, voluntary details and whether it can be ordered to attack/protect. Specify limits on self-harm, secrets, property, optional limited resources, binding oath/duty and PvP; do not silently import Command's distinct source constraints. Does this apply actual Charmed, a separate service compulsion, or both? Define exact narrow-immunity components and the shared hard-control record for ongoing commanded Actions, repeat saves including current regular turn, harm ending if NEW, multiple casters and no permission to invent actions. A label 'loyal servant' creates no permanent faction/membership/ownership transfer.

3. Group Pacify: all enemies in15ft cone cannot initiate combat unless provoked. Range15,Action,V/S/F,base3, no save/duration supplied. Need NEW save, duration/concentration and exact cone/LoE, ordinary enemy identification and affected-set snapshot. Can it halt an existing fight or only prevent a new one? Define 'initiate combat': attacks only, damaging casts, knowingly harmful control/indirect acts, movement/defense, existing paid commitments and actual provocation (caster/allies vs any attacker, recognized target allies, damage vs commitment). Compare Pacify and Voice of Peace explicitly; no automatic alliance/initiative cancellation, mere insults ending, or invented whole-Action denial if other acts remain. Does effect persist after leaving cone and must targets hear/understand? Source has no hearing gate.

4. Illusive Commands: force simple action, examples drop item/walk away/kneel. Action30,V/S/F,base3, no save/duration supplied. Preserve actual compelled action and distinguish from rank-one one-word Command. Does it permit a short instruction rather than one word, choose one of three finite options, or supply another clear bounded procedure? Need NEW save, target, timing, hearing/language, action/movement/interaction costs, posture duration, legal later item recovery, repeat/expiry, safe-route constraints and competing applications. Spell name does not create an Illusion school mode or new sensory images. Exact hard whole-Action component consumes/reserves the existing allowance; harmless forced movement isn't automatically hard denial.

5. Calm Emotions: suppress strong emotions in20ft sphere; source range20,Action,V/S/F,base3. Need explicit radius/diameter and sphere-center placement, targets including allies/hidden creatures, LoE, NEW save/willingness/duration/concentration, initial vs persistent zone/entry timing. Operationally distinguish ordinary emotional intensity, actual Core Charmed/Frightened and named class emotion/fury/rage mechanics. If suppression of actual conditions is added, expressly authorize which components; do not remove every mental effect by theme. Do clocks/saves continue and resume when calm ends? Does harm end or merely break hostility indifference, if that mode is deliberately added? Preserve existing beliefs/knowledge/agency and no unprinted healing of Strain/Corrupted/Dissonance, permanent personality change, oath recovery or memory erasure.

6. Crown of Madness: control a Humanoid's actions, WIS save ends; concentration up to1minute,Action30,V/S/F,base3. Preserve actual Humanoid predicate, evaluated after paid casting without free classification disclosure; decide application-only or maintained classification explicitly. Need initial/repeat-save timing, whether actual Charmed applies, source-specific commanded behavior and how much of Action/BA/Reaction/movement is controlled, caster order cost/communication, victim choice, attacks/resources/secrets/oaths/self-harm, no-order default, no valid action, concentration loss and multiple control sources. Do not silently replace broad printed control with another game's one-melee-attack/maintaining-Action version. Shared hard-control allowance applies to actual whole-Action/turn commandeering, records once on establishment and never refunds/refreshes; no extra Action from coercion.

7. Zone of Truth: keep both actual modes/access — Enchantment2/base3/Core350 says 15ft RADIUS cannot lie, CHA negates; Divination4/base7/Core256 says 15ft zone creatures must save to lie, unspecified appropriate save. Both raw range15,Action,V/S/F,Instantaneous. Are these unified geometry/duration/procedure with explicit actual class rank/school price, or meaningfully different modes? Need NEW placement/radius/height/LoE, duration/concentration, application/entry/end/start saves, immunity after successful save or repeat attempts, leaving/reentering, target awareness and whether caster knows save result. Preserve freedom to stay silent, evade, state mistaken beliefs, quote/fiction/intentionally misleading truths and private knowledge; no forced disclosure/objective truth engine. Define a deliberate lie according to actual belief/intent, not secretly omniscient facts. Avoid importing save-result knowledge or speech/language restrictions absent decision. If a Divination source interacts with Protection from Scrying, distinguish prohibited magical information generation from action restriction; Enchantment placement does not inherit Divination classification. Actual class access is fixed below and never selectable interchangeably just by paying another price.

Shared existing rules: actual class repertoire/rank, legal action/components/RP preflight then commitment/concentration transition/Dissonance/Refrain/beginning hooks, then counters LIFO and surviving effect. No refunds or restoration. V audible/S normal usable hand/F ordinary focus. Save DC8+PB+actual casting modifier, binary saves. Hidden eligibility after payment; no automatic diagnostic. One combined source-character/target/encounter hard-denial allowance across spells/classes/companions; establishes once, no later refund/refresh. Creature type alone supplies no immunity; Charmed immunity only has actual scope. Exact conditions and independent causes retain their callbacks; clocks and guards survive suppression/reordering/extra turns/absence/planes. No automatic scaling or generic upcast.

Report numerical balance concerns separately from source fidelity. Authored rules are provisional, not runtime validation or whole-game/publication approval.
"""
parts=[questions,'## Exact shared access\n'+json.dumps(common,ensure_ascii=False),'## Full exact source records\n'+json.dumps(compact,ensure_ascii=False,indent=1)]
for rel,ranges in [('docs/mechanics/CONDITIONS_PLAYTEST.md',[(161,175),(697,713)]),('docs/mechanics/CONTROL_STATES_PLAYTEST.md',[(129,143)])]:
 p=R/rel;lines=p.read_text(encoding='utf-8').splitlines()
 parts.append('## Existing authority '+rel+'\nSHA256 '+sha(p))
 for lo,hi in ranges:parts.append('\n'.join(f'{i+1}: {lines[i]}' for i in range(lo-1,min(hi,len(lines)))))
packet='\n\n'.join(parts)+'\n';p=A/'CODEX_ENCHANTMENT_RANK2_SOURCE_CONFERENCE_PREPARED.md';assert not p.exists();p.write_text(packet,encoding='utf-8')
meta={'status':'source conference prepared; NOT SENT; awaiting rank-one exact review','ids':[s['id'] for s in rows],'count':7,'sourcePlacements':8,'sourceCoreBlocks':8,'packetPath':str(p),'packetSha256':sha(p),'sourceCandidateSha256':sha(D/'candidate_enchantment_rank2_sources.json'),'operationalAtPreparation':sum(bool(s['operational']) for s in cat),'scope':'All source evidence checked against current catalog; questions are not authored mechanics or approval. Rank2 Enthrall remains a separately preserved unassigned variant on the rank1 identity.'}
(A/'ENCHANTMENT_RANK2_CONFERENCE_PREPARATION.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'characters':len(packet),'status':meta['status'],'sha256':sha(p)},indent=2))

