"""Preserve all pending source-category Combat feats and finite review questions.

Preparation only. Never promotes source flags to operational approval.
"""
from pathlib import Path
from collections import Counter
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1];AUDIT=GAME/'docs/audit/2026-10-08/full-game'
QUESTIONS={
'armor_crusher':"Define damage-packet eligibility, target/armor requirements, zero damage, application after the triggering damage, once-per-turn cadence and nonstacking across multiple owners. Does it alter an AC formula or a separate debuff layer, and what expires at the next regular start?",
'battlefield_commander':"Bind Action, hearing/willingness, three unique allies, Reaction expenditure, half-current-Speed separate budget, terrain costs, sequential placement, interruption and opportunity immunity. Define short-rest recovery and no movement at Speed0.",
'berserker_rage':"Define activation and exact two-round clock, weapon-die selection for multi-die/versatile/natural attacks, critical doubling and AC penalty arbitration. Establish whether this counts as the separate Berserker feat's rage for Frenzied Rage, without aliasing their sources.",
'bleeding_edge':"Assign an explicit periodic identity/family, damage type, three-round/tick clock, repeated applications and multiple owners. Resolve bleedable-body permission, Medicine action/range/hands and whether stopping this rider also affects unrelated Bleeding families.",
'brace_for_impact':"Define moved-since-start across forced movement, teleport and extra turns; reaction timing before/after mitigation; PB+CON minimum; one packet versus area or split damage; actual damaged recipient; and interaction with transfer/prevention rules.",
'break_line':"Define ordinary movement cost, occupied-space entry/exit and size limit; when the special opportunity attack occurs, who can make it, Reaction cost, declined/unavailable attack, hit consequence and legal stopping space. Do not leave passage dependent on an attack that cannot occur.",
'bull_rush':"Bind qualifying melee attack types, straight continuous ten-foot movement, actual hit versus damage, cadence and save timing. Decide push and Prone independently where displacement is blocked, and any size/anchor limits not supplied by the feat.",
'cleaving_momentum':"Bind the 2H Weapon prerequisite and whether the triggering/bonus attack must use it. Define hostile drop event, ordinary Bonus Action cost, same-turn window, another target, reach, death versus0HP and prevention of chained extra bonus actions.",
'close_quarters_combat':"Resolve ranged weapon versus spell attacks and which disadvantage sources are removed. Identify any actual attack-generated opportunity trigger in current combat rules; do not invent a universal ranged-attack opportunity penalty just to remove it.",
'combat_intuition':"Bind consciousness, surprise handling, first-round identity for late entrants/extra turns and the+1 AC layer. Resolve changing consciousness and already-existing surprise without granting extra turns or reactions.",
'combat_slide':"Decide whether5ft is a separate budget or uses ordinary remaining movement; bind before/after one weapon attack, declared target, misses/cancellation, terrain, Speed0 and immunity from only that target. Define own-turn cadence across extra turns.",
'crippling_strike':"Resolve the printed finesse OR melee-weapon scope, including thrown finesse weapons. Define speed modes/floor, repeated/multiple-owner applications, once-per-turn cadence and expiry; do not silently replace with the Thief class's source-specific Slow.",
'defensive_stance':"Supply activation, duration, frequency and legal timing for the retained+15% AC and cannot-move-this-turn clause. Define percentage base, rounding and AC-family interaction, plus forced movement/teleport and stance competition. Any numeric conversion must be explicitly NEW.",
'disarming_blow':"Specify legal attack types, declaration/payment of one actual damage die, critical/multi-die/rider eligibility and inability to pay. Bind save/DC ability, held reachable object, selection/drop placement, non-droppable bonds and damage resolution order.",
'double_tap':"Bind Attack-action qualification, one Bonus Action attack, weapon/ammunition/loading/hands and target choice. Resolve negative ability modifiers, an explicit modifier-restoring feature, off-turn/extra-turn timing and coexistence with other bonus-attack feats.",
'draw_cut':"Define the once-per-encounter boundary, lawful drawing interaction within an attack, sheathed weapon eligibility and hit/miss spending. Select one base weapon die and critical interaction without multiplying riders or laundering repeated sheath/draw events.",
'exploit_weakness':"Define when actual target HP below half maximum is checked, temporary HP/temporary maxima and unknown information handling. Resolve nineteen-to-twenty critical range against other range modifiers and automatic-critical effects without unsupported stacking.",
'feint':"Complete the absent Action/Bonus Action, target/range, check/save, AC amount/layer, next-attack beneficiary, deadline, use frequency and replacement behavior. Preserve the original short clause separately; do not adopt an external game's Feint by name.",
'grappler':"Bind+4 to actual initiating/maintaining/escape contests and whose roll receives the-4. Resolve multiple grapplers, size/reach/hands limits, four-degree checks, magical escape and stacking with proficiency/expertise without granting new grapple actions.",
'lunge':"Bind one selected melee weapon attack, declaration before targeting, own-turn cadence, current weapon reach and reversion. Explicitly distinguish attack reach from persistent control/opportunity reach and grapple reach.",
'overrun':"Complete Dash-linked movement budget, per-creature encounter limits, ally/enemy scope, save/DC and success/failure passage. Resolve no legal five-foot side destination, blocked endpoints, opportunity attacks and size/anatomy restrictions.",
'power_attack':"Complete declaration, eligible attacks, frequency, exact-2 attack penalty and+20% damage base/rounding/order. Resolve multi-type packets, criticals, resistance and combination with Precision Strike/Giant Slayer without silently substituting a flat damage bonus.",
'precise_shot':"The supplied current combat guide imposes nearby-hostile disadvantage, not a general ally-adjacent-to-target disadvantage. Locate source authority for the assumed penalty or choose an explicit finite new overlay; do not invent that penalty globally or silently turn this into Sharpshooter.",
'precision_throw':"Define thrown-property melee/ranged weapon use, actual attack qualifier, normal versus long range caps and legal cases where doubled normal exceeds long. Resolve+1 bonus-family stacking and improvised thrown objects.",
'punishing_blow':"Define eligible damage events/attacks, hostile versus any target, actual Stunned/Prone timing, once-per-turn cadence and damage type. Avoid copying the PB rider through each damage component or transfer operation.",
'reckless_swing':"Bind declaration and eligible melee weapon, advantage cancellation, selection of one weapon die and critical doubling. Resolve repeated use, missed attacks, extra turns, expiry and all attacks against the user without replacing source with a class Rage rule.",
'riposte':"Resolve Agility15+ against the actual ability taxonomy and Melee Proficiency against existing credentials. Define dodge/parry success, trigger timing, legal target/reach, Action/Reaction cost, frequency and recursive counterattack prevention. 'Free attack' is not a completed action rule.",
'savage_momentum':"Define consecutive hit chain scope, turns/encounters/off-turn attacks, target changes, misses and nonattack interruptions. Resolve when the once-per-turn bonus is chosen and prior hits counted, PB cap and chain state through target death/transformation.",
'shattering_smash':"Complete missing save DC and attack scope. Define actual physical block, one damage-die cost, declaration, save timing and suppression of ordinary shield AC versus magical enhancement/other block benefits. Do not damage/destroy equipment by implication.",
'shield_bash':"Supply attack ability/proficiency/weapon classification, range, shield-hand use and missing stun DC. Bind Attack-action prerequisite, Bonus Action, one-short-rest use declaration/payment and Stunned expiry; distinguish the shield from a new priced weapon.",
'shield_expert':"Bind the+1 AC as a separate actual eligible modifier and worn/wielded shield requirements. Define interposition, Reaction timing on a successful Dexterity half-damage save, area/cover geometry, rerolls and no change to failed saves.",
'sure_shot':"Define attribution of up to2 AC to armor or cover across suit formulas, natural/unarmored defenses, shields, negative grades and magical enhancement. Identify what counts as a magical barrier and preserve total-cover targeting limits.",
'tactical_flanker':"Supply or locate the exact current flanking geometry. Define which owner's once-per-turn budget funds which ally attack, designation timing, same-hit collisions across owners, damage type and no duplicated1d6 from one triggering application.",
'target_mark':"Define weapon range as normal/long and the actual selected weapon; target legality, sight/cover and mark ending/replacement. Resolve first attack by each ally per mark versus per turn, whether self qualifies, application after misses, alliance changes and short-rest recovery.",
'unstoppable_force':"Define push/knock scope including mundane/spell/class effects, whether pulls qualify, bonus displacement limits and blocked movement. Resolve prone on fail-by5 where the original effect uses a contest or no save, cadence and interaction with Bull Rush.",
'volley':"Complete weapon/ammunition requirements, Action and frequency, area shape/size/origin/range/line, attacks versus saves/DC, target selection, damage, miss outcomes and ammunition expenditure. The retained 'small area' is not an operational template.",
'weapon_finesse':"Bind eligible melee attack types, actual weapon/natural/unarmed distinctions and attack-only versus damage ability. Preserve Strength-dependent prerequisites and weapon properties unless an explicit completion changes them.",
'weapon_mastery':"Define chosen weapon type, actual proficiency, character-level prerequisite and whether repeatable. Specify+1 critical range semantics, floor/limit and arbitration with Exploit Weakness and other critical features; no imported external Weapon Mastery system.",
'whip_control':"Bind actual Whip proficiency/use, one attack replacement or on-hit trigger, disarm versus trip choice, checks/saves/DC, reach, target size, damage/payment, frequency and legal dropped-object/push placement.",
'whirlwind_striker':"Complete surrounded geometry, meaning of evasion and cleave, exact percentage bases/rounding, triggers, targets, costs, frequency and ending. Preserve the+5%/+10% originals and label any conversion as NEW.",
'eldritch_combat':"Resolve legacy1st-level against this game's rank system; actual repertoire/casting-class access, RP/components/concentration/Dissonance and independent casting-time eligibility. Define ordering with Attack action, hit prerequisite, touch/self target clauses, reaction-triggered free casts, cadence and separate short-rest use without granting free costs.",
'favored_enemy_dragon':"Bind current bestiary dragon/dragonkin tags without cosmology or ancestry retcons; damage event scope, Survival/Lore skill mapping and genuine information checks. Define ally+1 breath-save radius/timing/duration, Frightened one-round limit, difficult-terrain use/duration and continuing lair hazard damage.",
'frenzied_rage':"Preserve all three clauses: replacement+3 instead of+2, drop-trigger extra attack OR one-round extension, and once-per-rage charge with Dazed. Bind valid rage sources and acquisition prerequisites, action/cadence/caps, movement/save/DC/targets/duration, avoiding unlimited kill/extension loops or name-only class eligibility.",
'giant_slayer':"Bind Size thresholds and the+20% damage base/order, successful melee-hit speed-halving timing/recovery and short-rest use. Complete miss-trigger Reaction movement budget/reach, direct1d6 versus an attack, type, geometry and disadvantage deadline. Preserve all three effects.",
'life_drinker':"Bind actual Dark Affinity/Hemocraft prerequisite IDs without approving them. Resolve critical-hit healing from final paid HP damage versus tempHP/overkill/copied damage, hostile0HP healing identity/cadence and simultaneous triggers; define below-half/creatures-with-blood rider using reviewed healing ledgers.",
'precision_strike':"Bind the explicit Dexterity OR Weapon Focus prerequisite, once-per-turn choice and-2/+50% arithmetic. Resolve whether automatic-critical mode replaces both penalty and percent bonus, restrained/grappled/Anatomy Lore qualification, timing, short-rest charge and immunity/critical-range interfaces.",
'slayer_s_resolve':"Bind Favored Enemy OR level prerequisite, actual dragon source tags, Frightful Presence versus broader fear immunity, conscious ally aura/line and+2 AC eligibility. Resolve Reaction declaration for attack disadvantage or personal breath-save reroll, information window, mandatory reroll choice and short-rest payment."
}
RELATED=['berserker','greatWeaponMaster','sharpshooter','weaponFocus','dark_affinity','hemocraft']
CONTEXT={
 'COMBAT_ACTION_PLAYTEST.md':None,
 'DAMAGE_SHARING_PLAYTEST.md':['Resolve the kind of protection first','One transfer operation and exact amounts','Hit identity and final damage accounting'],
 'CONDITIONS_PLAYTEST.md':['Shared handling','Bleeding','Dazed','Frightened','Grappled','Prone','Restrained','Stunned'],
 'CHARACTER_CREATION_PLAYTEST.md':['Abilities and training','Gain a level','One shared RP pool','Shared strain, recovery and concentration'],
 'CHARACTER_FOUNDATION_TABLES.md':['Ability-check skills'],
 'EQUIPMENT_ACQUISITION_PLAYTEST.md':['Armor and shields','Hands and focuses','Weapons and ammunition','Equipment grade'],
 'BUFFER_FEAT_PLAYTEST.md':['Shared rules','Lifeleech — Magic; actual spellcasting ability','Soul Cage feat — Magic; level8+ and (Lifeleech **or** actual spellcasting ability)'],
 'CLASS_PLAYTEST_RULES.md':None}
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(o):return hashlib.sha256(json.dumps(o,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def write(p,t):p.write_text(t,encoding='utf-8',newline='\n')
def dump(p,o):write(p,json.dumps(o,ensure_ascii=False,indent=2)+'\n')
def section(text,heading):
    start=text.index('## '+heading+'\n');end=text.find('\n## ',start+1)
    return text[start:end+1 if end>=0 else len(text)]
def main():
    p=ROOT/'src/data/feats.js';raw=json.JSONDecoder().raw_decode(p.read_text(encoding='utf-8').split('export const feats = ',1)[1])[0];by={f['id']:f for f in raw}
    pending=read(AUDIT/'REMAINING_FEAT_CATALOG_PREPARATION.json')
    craft=read(AUDIT/'CRAFTING_FEAT_INTERFACE_PREPARATION.json');excluded={f['featId'] for f in craft['selectedFeats']}
    reviewed=set(read(ROOT/'data/public/feat_playtests/manifest.json')['operationalIds'])
    selected=[f for f in raw if f['type']=='Combat' and f['id'] not in reviewed|excluded]
    assert len(selected)==47 and set(QUESTIONS)=={f['id'] for f in selected}
    full_pending=[f for f in raw if f['id'] not in reviewed]
    boundaries=[]
    protected=dict(craft['protectedFiles'])
    def protect(path):protected[str(path.relative_to(GAME)).replace('\\','/')]=sha(path)
    for name,heads in CONTEXT.items():
        path=ROOT/'docs/mechanics'/name;text=path.read_text(encoding='utf-8');protect(path)
        for h in heads or [None]:
            exact=section(text,h) if h else text
            boundaries.append({'file':str(path.relative_to(GAME)).replace('\\','/'),'fileSha256':sha(path),'heading':h,'exactText':exact,'statusClaim':'current saved manuscript; retain its own stated review scope, not a new approval'})
    class_dependencies=[]
    for name in ('druid','warrior'):
        path=ROOT/f'data/public/class_playtests/{name}.json';d=read(path);protect(path)
        for c in d['cards']:
            if re.search(r'\brage\b|\bberserker\b',json.dumps(c),re.I):
                class_dependencies.append({'file':str(path.relative_to(GAME)).replace('\\','/'),'fileSha256':sha(path),'card':c,'interpretation':'literal source/card match only; not proof that this qualifies as a rage for any feat'})
    rows=[]
    for f in selected:
        spans=[]
        for field in ('description','effect','prerequisite','legacyEffect'):
            for m in re.finditer(r'\b\d+(?:\.\d+)?%|\b(?:free attack|free action|small area|Agility|Anatomy Lore|physical damage|crit range)\b',f.get(field,''),re.I):
                spans.append({'field':field,'span':[m.start(),m.end()],'exactText':m.group()})
        rows.append({'featId':f['id'],'sourceObject':f,'sourceObjectSha256':digest(f),'questionId':f'CF-{len(rows)+1:02}','fullClauseQuestion':QUESTIONS[f['id']],'literalReviewSignals':spans,'currentOperationalStatus':'full-feat-review-pending'})
    for f in ['REMAINING_FEAT_CATALOG_PREPARATION.json','FEAT_IDENTITY_CANDIDATES.json','CRAFTING_FEAT_INTERFACE_PREPARATION.json']:protect(AUDIT/f)
    protect(ROOT/'data/public/feat_playtests/manifest.json')
    tests=[
      ('335 complete source registries still byte-identical',len(raw)==335 and p.read_bytes()==(GAME/'src/data/feats.js').read_bytes()),
      ('327 pending complete source records unchanged',full_pending==[z['sourceObject'] for z in pending['records']]),
      ('eight reviewed IDs separate',len(reviewed)==8 and not reviewed.intersection(QUESTIONS)),
      ('47 Combat IDs exact,24 crafting overlaps excluded',len(selected)==47 and len(excluded)==24 and not excluded.intersection(QUESTIONS) and sum(f['type']=='Combat' for f in full_pending)==48),
      ('each full selected object and hash exact',all(z['sourceObject']==by[z['featId']] and z['sourceObjectSha256']==digest(by[z['featId']]) for z in rows)),
      ('every selected feat has its own full-clause question',len(QUESTIONS)==len(rows)==47 and all(len(z['fullClauseQuestion'])>100 for z in rows)),
      ('literal signals reconstruct their exact source spans',all(z['sourceObject'][s['field']][s['span'][0]:s['span'][1]]==s['exactText'] for z in rows for s in z['literalReviewSignals'])),
      ('six complete prerequisite/counterpart objects preserved',len(RELATED)==6 and all(x in by for x in RELATED)),
      ('two literal class dependencies preserved',len(class_dependencies)==2),
      ('all governing excerpts occur exactly in saved manuscripts',all(z['exactText'] in (GAME/z['file']).read_text(encoding='utf-8') for z in boundaries)),
      ('all prior and current protected files unchanged',all(sha(GAME/path)==h for path,h in protected.items()))]
    assert all(v for _,v in tests),[n for n,v in tests if not v]
    data={'status':'PREPARED, NOT SENT; complete source/category audit and questions, no operational approval','sourceFile':str(p.relative_to(GAME)).replace('\\','/'),'sourceFileSha256':sha(p),'selection':'all pending source type Combat except the one member already routed through the24-feat crafting interface; no semantic reclassification','selectedFeats':rows,'relatedUnapprovedFeatSources':[by[x] for x in RELATED],'classDependencies':class_dependencies,'currentGoverningExcerpts':boundaries,'identityAudit':read(AUDIT/'FEAT_IDENTITY_CANDIDATES.json'),'counts':{'allSourceFeats':335,'reviewed':8,'pending':327,'selectedCombat':47,'separatelyPreparedCrafting':24,'otherPending':256,'sourceCombatTotalPending':48,'relatedCounterparts':6,'classDependencies':2,'contextExcerpts':len(boundaries),'currentPercentEffects':sum('%' in f['effect'] for f in selected),'reviewFlagFalse':sum(not f.get('needsReview',False) for f in selected),'declaredProvisionalComplete':sum(f.get('status')=='provisional-complete' for f in selected)},'checks':[{'name':n,'pass':v} for n,v in tests],'protectedFiles':protected,'featsApproved':0,'originalRulesChanged':False,'cosmology':'post-push only; no ontology/ancestry retcons authorized by feat terminology'}
    dump(AUDIT/'COMBAT_FEAT_SOURCE_PREPARATION.json',data)
    lines=['# Combat feat source review preparation','',data['status'],'',f"47 pending Combat feats; 6 complete unapproved counterpart records; 2 literal class-card dependencies; {len(boundaries)} exact current-guide excerpts. All 335 original feats remain intact and the operational count remains 8 reviewed / 327 pending. The 24 crafting-interface feats are separately routed, leaving 256 other pending identities outside these two focused packets.",'','Source flags are not an operational verdict. Preserve the current effect, description, prerequisite and inactive legacy effect separately. Percentage rules, short action clauses and ambiguous prerequisite names need explicit decisions; no source is deleted or automatically aliased.','', '| Case | Full feat | Source prerequisite | Exact-review question |','|---|---|---|---|']
    for z in rows:
        f=z['sourceObject'];lines.append(f"| {z['questionId']} | {f['name']} ({f['id']}) | {f['prerequisite']} | {z['fullClauseQuestion']} |")
    lines+=['','## Shared conference requirements','',
      'Resolve actual character-level/ability/proficiency prerequisites, selection and repeated acquisition; timing, Action/Bonus Action/Reaction, legal targets/range/geometry, payment, cadence, expiry and recovery; ordinary versus extra turns; actual damage types and percentage/critical arithmetic; critical range, weapon dice, hit identity, temporary HP and overkill; source-specific conditions, slot/armor modifiers and named bonus families. Resolve every full effect clause, including prestige feats with several clauses. Preserve legacy wording and mark every completion NEW.','',
      'Precise Shot assumes ally-adjacent disadvantage absent from the supplied current combat guide; current nearby-hostile disadvantage and ordinary cover are distinct. Riposte says Agility and free attack; Volley supplies no area size; several effects retain percentages. Locate authority or make explicit finite decisions rather than substituting another game’s similarly named option.','',
      'Berserker, Berserker Rage, Frenzied Rage and the two literally matched class cards are separate source identities. Matching a word is not evidence of a common rage engine. Dark Affinity and Hemocraft remain unreviewed counterparts; Life Drinker is not the reviewed Lifeleech feat. Do not expand dragon/dragonkin labels into a cosmology review.','',
      'This audit covers the source Combat category only. Combat-related General/Magic/Skill entries remain in the full pending catalog; source categories are navigation metadata, not mechanical scope. Six included counterparts are dependency evidence, not six extra approvals.','',
      'Before dispatch, attach current applicable reviewed revisions and confirm no other conference is active. Finish Tailoring exact review first. Any later authored cards require their own exact review; human balance, runtime and whole-game flow remain separate.','']
    audit='\n'.join(lines);write(AUDIT/'COMBAT_FEAT_SOURCE_AUDIT.md',audit)
    packet='\n\n'.join(['PREPARED COMBAT FEAT SOURCE CONFERENCE — NOT SENT.\n\nThis is the complete47-feat source-category packet, not operational cards. Please return finite numbered decisions for every CF case and full clause, preserving originals and distinguishing existing authority from NEW completions. The source classification does not exclude combat-related feats in other categories from later review. The six counterpart feats are dependency evidence and remain pending. Do not infer a missing feature from a similar name. No cosmology review: labels identify only current mechanical prerequisites/targets. Source flags, local checks and filenames are not your independent approval.\n\nUpdate this cover with current reviewed dependencies before dispatch. The active Tailoring exact review must complete first. Nothing here changes current rules or authorizes promotions.',audit,'COMPLETE47 SOURCE OBJECTS, EXACT FIELD SPANS AND FULL-CLAUSE QUESTIONS',json.dumps(rows,ensure_ascii=False,separators=(',',':')),'SIX COMPLETE UNAPPROVED COUNTERPART SOURCES',json.dumps(data['relatedUnapprovedFeatSources'],ensure_ascii=False,separators=(',',':')),'TWO COMPLETE LITERAL CLASS DEPENDENCIES',json.dumps(class_dependencies,ensure_ascii=False,separators=(',',':')),'CURRENT SAVED GUIDE EXCERPTS, WITH THEIR OWN BOUNDED STATUS',json.dumps(boundaries,ensure_ascii=False,separators=(',',':')),'HISTORICAL IDENTITY CANDIDATES, NOT ALIAS APPROVAL',json.dumps(data['identityAudit'],ensure_ascii=False,separators=(',',':')),'LOCAL PRESERVATION EVIDENCE',json.dumps({'counts':data['counts'],'checks':data['checks'],'protectedFiles':protected},ensure_ascii=False,separators=(',',':'))])
    path=AUDIT/'CODEX_COMBAT_FEAT_SOURCE_PREPARED.txt';write(path,packet)
    status={'status':'prepared-not-sent; no operational feat approval','packetFile':path.name,'characters':len(packet),'sha256':sha(path),'counts':data['counts'],'checks':len(tests),'protectedFiles':len(protected),'featsApproved':0,'reviewedFeatsUnchanged':8,'remainingFeats':327}
    dump(AUDIT/'COMBAT_FEAT_SOURCE_STATUS.json',status)
    print(json.dumps(status,ensure_ascii=True))
if __name__=='__main__':main()

