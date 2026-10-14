"""Preserve 22 heritage/mutation feats and actual ancestry/Warrior counterparts."""
import json,re
from prepare_magic_extended_feat_source_audit import ROOT,GAME,AUDIT,sha,digest,write,dump,section

QUESTIONS={
 'aberrant_mind':'Preserve telepathy with aberrations and psychic resistance under Intelligence15. Define actual creature-type eligibility,range,senses,language,directionality,consent/actions and informational limits. Source category does not by itself require Warrior or change creature type. No alien origin, universal cognition or cosmology decision is inferred.',
 'backlashEngine':'Reconcile standalone each hit while mutated with the full Warrior counterpart: Warrior8,Adrenal Backlash Core equipped/active,actual damage and once per round. Resolve source-defined BT cap/generation exceptions,hostile-threat rules,damage packets and zeroHP. Do not approve broader hit farming or grant this twice through class and feat catalogs.',
 'bioStabilizer':'Reconcile standalone+1 regeneration with Warrior4/Bloodthick equipped and the reviewed scheduling-only modifier. Require actual Bloodthick activation and two active mutations; define one added HP on the same pulse,shared Mutation Recovery Reserve,zeroHP/Wound gates and finite healing. No second pulse or free reserve refill.',
 'bornToHorrify':'Reconcile per-turn standalone wording with Warrior16 counterpart limiting failure rerolls to the owner regular turn while Apex active. Define optional declaration after die/result,advantage/disadvantage dice,new result,one ledger and off-turn saves; do not silently treat every enemy turn as another use.',
 'contraption_crafter':'Bind actual Gnome heritage eligibility and one/day recovery clock. Define a finite random-utility gadget table with creation/deployment actions,actual tools/materials,physical profile,duration,ownership,usage and end disposition. Compare Tinker Gnome ancestry and pending Tinker class/recipes without free permanent products,random undefined powers or automatic class access.',
 'crushing_advance':'Bind actual Ogre heritage,melee hit and precise moving requirement: own movement distance,straight path,timing,one hit versus every hit and cooldown. Define5ft push direction,target-size/save/space/collision,forced movement,reach and no source-implied bonus damage or extra attacks.',
 'cultural_legacy':'Bind Goblin heritage and identify an actual finite favored-skill list from supplied base/variant traits. Define10percent effectiveness against d20 check totals,task degrees or another explicit numerical result,including rounding/stacking. Do not invent culture/lore,apply a universal multiplier or silently replace the current percentage.',
 'distortedDominance':'Reconcile standalone loss of one action on failed saves versus provisional Warrior4 Aberrant-only Reaction denial. Preserve both texts and any already-reviewed component scope. Resolve target/range/duration/encounter ledger,actual mutation activation and hard-control guard; any retained Action denial requires an explicit bounded decision.',
 'elven_grace':'Define Elf heritage,once-per-real-combat ledger,voluntary declaration before/after attack/save,actual action/Reaction and eligible AoE or ranged event. Resolve multiple packets/ongoing zones/automatic damage,damage versus conditions/displacement and zeroHP permissions. No fabricated movement or broad immunity from evade.',
 'evisceratorProtocol':'Reconcile Echo Knuckles plus Talons with actual Warpgrip Talons counterpart and Warrior8 gate. Define equipped versus active requirements,one real offhand hit,choice of Bleed/Weakened,source ownership,pulse/expiry/cure/stacking. Preserve reviewed free-attack limits and no recursive on-hit/free-attack generation.',
 'evolutionUnderFire':'Reconcile single hit>15 versus counterpart actual damage event>15,Warrior16,one positive Warrior recharge counter and once-per-round shortening cap. Specify mitigation/tempHP/ward quantities,threshold exactness,which counter,active Apex requirement and no spent rest-use restoration.',
 'glamourborn':'Bind Feykin heritage,each enemy first attack timing and what resets that record. Define actual20percent miss roll,order versus attack/critical/advantage,ranged/melee/spell attacks,unseen enemies,multiple attacks and invalid declarations. No spell-save immunity,invisibility or Fey cosmology inference.',
 'hypermutationSpike':'Reconcile source stun/slow immunity with Warrior16 five-round Butcherform and the reviewed per-mode Speed-floor procedure. Define one activation,Long Rest expenditure,currentHP quarter-threshold ending,loss/suppression/return and Stunned scope. Keep existing physical restraint and root rules; no broad immunity created from slow wording.',
 'juggernautCore':'Reconcile critical immunity condition with actual Ossified Core suppression of extra critical dice and Warrior8 precision-damage halving. Define active mutation,actual Sneak Attack/other precision scope,only the extra component,rounding/order versus resistance and mixed types. Ordinary weapon damage and critical-trigger effects remain distinct.',
 'killChainAdaptation':'Reconcile melee kill with Warrior4 counterpart meaningful-hostile zeroHP,once per round,next-melee-attack+1 and Speed+10 until next regular-turn end. Define dying/dead distinction,ownership,refresh/stacking,actual mutation activation and movement already spent. Preserve anti-farming and no additional full Action.',
 'livingFortress':'Bind three actually active Vital mutations against real slot/active limits and temporary exceptions; resolve equipped-only prerequisite versus active benefit and Warrior8 gate. Identify actual flanking rule before denying its sole advantage. Do not erase other advantage sources,nearby allies or tactical positioning effects by an undefined blanket immunity.',
 'nightfang_training':'Bind Umbrin heritage,total darkness and actual senses without granting sight. Define10percent damage sources,packets/critical/rounding/resistance and+2 Stealth ability checks; require legal hiding. Preserve bright/dim versus total-dark boundaries and do not change ancestry/origin.',
 'orcish_warpath':'Bind Orc heritage and personally defeating a meaningful enemy,not arbitrary party kills. Define temporary+2 Strength score versus modifier,maximum3 stacks,duration/refresh/reset and ordinary or explicit score cap. Recompute actual attacks,checks,carrying/prerequisites consistently without permanently learning gated choices or creating repeated kill buffs.',
 'primal_recovery':'Bind Troll heritage and once-per-real-combat use with declaration/action timing,zeroHP/incapacity restrictions and an explicit eligible condition/debuff scope. Distinguish cure,suppression,ongoing sources,physical restraints,Wounds/disease/curses/death and ability availability. Do not reduce any-status source promise silently; decide necessary exceptions with evidence.',
 'synapticRot':'Reconcile nearby any enemy WIS/INT failure with Warrior8/15ft/your-feature/once-target-round counterpart and actual Silenced rules. Define verbal-only versus all-spell denial,save sources,active Wailing Eye Cluster/Viral Core Sacs binding and end-of-next-turn clock. Preserve nonspell abilities and source conflicts for explicit decision.',
 'terrorEngine':'Reconcile source two Shaken/Disoriented enemies+2DR with Warrior8 counterpart adding Frightened,30ft,your-feature attribution and first damage each round. Define actual active Carrion prerequisite,counting distinct hostiles,damage-reduction order/packet,expiry and changed counts. No universal armor,all-hit reduction or stacking inferred.',
 'versatile_mastery':'Bind Human heritage and once-per-rest clock. Define an explicit finite borrowing procedure for an actual party member class skill/ability,consent/availability,character/class-level gates,activation/RP/other resources,DC/scaling,duration and restrictions. No copied permanent progression,free resources/companions,signature identity or automatic full class access.'
}
MUTATION_MAP={
 'backlashEngine':'backlash-engine','bioStabilizer':'bio-stabilizer','bornToHorrify':'born-to-horrify','distortedDominance':'distorted-dominance',
 'evisceratorProtocol':'eviscerator-protocol','evolutionUnderFire':'evolution-under-fire','hypermutationSpike':'hypermutation-spike','juggernautCore':'juggernaut-s-core',
 'killChainAdaptation':'kill-chain-adaptation','livingFortress':'living-fortress','synapticRot':'synaptic-rot','terrorEngine':'terror-engine'}
CONTEXT={
 'ANCESTRY_BACKGROUND_PLAYTEST.md':['Selecting and recording a character','Recharge, recovery and action clocks','Trait procedures and source-specific exceptions'],
 'CHARACTER_CREATION_PLAYTEST.md':['Abilities and training','Gain a level','Multiclass entry and class features'],
 'CORE_RESOLUTION_PLAYTEST.md':['Which rule applies','Rolls','Resolve a damage event','Zero HP and recovery'],
 'COMBAT_ACTION_PLAYTEST.md':['Encounter and action resources','Time and event ordering — NEW','Maneuvers and ordinary attacks','Movement and geometry','Cover, sight, Hide and Search'],
 'CONTROL_STATES_PLAYTEST.md':['Records, clocks and precedence','Speed arbitration','Root, physical restraints and suppression','Compulsion, action denial and initiative','Hypermutation and systemic penalties'],
 'HEALING_PULSE_PLAYTEST.md':['Keep the original clock','Targets, payments and separate budgets','Native recurrence and device limits'],
 'HEALING_DEATH_PLAYTEST.md':['Damage quantities and resolution','ZeroHP permissions and start timing','Recovery gates, triggers and loops','Removing suppressed Bleed and fire'],
 'MAXIMUM_HP_PLAYTEST.md':['Exact thresholds and recorded events','Percentage recovery and damage'],
 'CONDITIONS_PLAYTEST.md':['Bleeding','Silenced','Stunned'],
 'BODY_EQUIPMENT_PLAYTEST.md':['Entering and changing forms','Using equipment in a form','Carrying and Load']}

def main():
    protected={}
    def read(p):
        protected[p.relative_to(GAME).as_posix()]=sha(p);return json.loads(p.read_text(encoding='utf-8-sig'))
    p=ROOT/'src/data/feats.js';f=json.JSONDecoder().raw_decode(p.read_text(encoding='utf-8-sig').split('export const feats = ',1)[1])[0];protected[p.relative_to(GAME).as_posix()]=sha(p);by={x['id']:x for x in f}
    reviewed=set(read(ROOT/'data/public/feat_playtests/manifest.json')['operationalIds'])
    routed={z['featId'] for n in ['CRAFTING_FEAT_INTERFACE_PREPARATION.json','COMBAT_FEAT_SOURCE_PREPARATION.json','SKILL_FEAT_SOURCE_PREPARATION.json','MAGIC_CORE_FEAT_SOURCE_PREPARATION.json','MAGIC_EXTENDED_FEAT_SOURCE_PREPARATION.json'] for z in read(AUDIT/n)['selectedFeats']}
    pending=read(AUDIT/'REMAINING_FEAT_CATALOG_PREPARATION.json')
    selected=[x for x in f if x['id'] not in reviewed|routed and x['type']!='General'];assert len(selected)==22 and {x['id'] for x in selected}==set(QUESTIONS)
    warrior=read(ROOT/'data/public/class_playtests/warrior.json');wc={c['id']:c for c in warrior['cards']}
    pairs=[{'featId':id,'sourceObject':by[id],'completeClassCounterpart':wc['warrior.supplement.'+suffix],'relationship':'same named source-row subject; identity/acquisition and effect reconciliation pending; not two automatic grants'} for id,suffix in MUTATION_MAP.items()]
    mutations=[c for c in warrior['cards'] if c['sourceKind']=='mutation']
    ancestry=read(ROOT/'data/playtest/ancestry_background_candidate.json')
    heritage=[]
    for x in selected:
        if x['type']!='Racial':continue
        name=x['prerequisite'].removesuffix(' heritage');matches=[a for a in ancestry['ancestries'] if a['name']==name];assert len(matches)==1
        heritage.append({'featId':x['id'],'sourcePrerequisite':x['prerequisite'],'matchingCurrentAncestryRecord':matches[0],'scope':'name match plus complete base/variant data; full feat eligibility still requires joint decision'})
    excerpts=[]
    for name,heads in CONTEXT.items():
        p=ROOT/'docs/mechanics'/name;t=p.read_text(encoding='utf-8');protected[p.relative_to(GAME).as_posix()]=sha(p)
        for h in heads:excerpts.append({'file':p.relative_to(GAME).as_posix(),'heading':h,'sha256':sha(p),'exactText':section(t,h)})
    # Carry selected historical bindings with their own explicit narrow scopes.
    bindings=[];ids=set(c['id'] for c in mutations)|{z['completeClassCounterpart']['id'] for z in pairs}
    for name in ['CONTROL_SOURCE_BINDINGS.md','HEALING_PULSE_SOURCE_BINDINGS.md','HEALING_DEATH_SOURCE_BINDINGS.md','FORM_TEMP_HP_SOURCE_BINDINGS.md','MAXIMUM_HP_SOURCE_BINDINGS.md']:
        p=ROOT/'docs/mechanics'/name;t=p.read_text(encoding='utf-8');protected[p.relative_to(GAME).as_posix()]=sha(p)
        for m in re.finditer(r'^## (.+)$',t,re.M):
            if not any(id in m[1] for id in ids):continue
            end=re.search(r'^## ',t[m.end():],re.M);part=t[m.start():m.end()+end.start() if end else len(t)]
            bindings.append({'file':p.relative_to(GAME).as_posix(),'heading':m[1],'exactText':part,'scope':'literal existing binding and its own recorded review limit; no full-feat approval inferred'})
    rows=[{'featId':x['id'],'questionId':f'HM-{i+1:02}','sourceObject':x,'sourceObjectSha256':digest(x),'fullClauseQuestion':QUESTIONS[x['id']],'currentOperationalStatus':'full-feat-review-pending'} for i,x in enumerate(selected)]
    checks=[
      ('335 source registry byte equality',len(f)==335 and (ROOT/'src/data/feats.js').read_bytes()==(GAME/'src/data/feats.js').read_bytes()),
      ('All327 pending source objects retained',[x for x in f if x['id'] not in reviewed]==[z['sourceObject'] for z in pending['records']]),
      ('Exact22 remaining nongeneral source identities',len(selected)==22 and {x['id'] for x in selected}==set(QUESTIONS)),
      ('No overlap with185 prepared or8 reviewed',len(routed)==185 and len(reviewed)==8 and not set(QUESTIONS).intersection(routed|reviewed)),
      ('All22 complete original objects and full-clause questions',all(z['sourceObject']==by[z['featId']] and z['sourceObjectSha256']==digest(z['sourceObject']) and len(z['fullClauseQuestion'])>150 for z in rows)),
      ('Nine full ancestry base-and-variant matches',len(heritage)==9 and len({z['matchingCurrentAncestryRecord']['id'] for z in heritage})==9),
      ('Twelve complete Warrior mutation-feat counterparts',len(pairs)==12 and {z['completeClassCounterpart']['id'] for z in pairs}=={c['id'] for c in warrior['cards'] if c['sourceKind']=='mutationFeat'}),
      ('All actual Warrior mutation profiles supplied',len(mutations)>20 and all(c==wc[c['id']] for c in mutations)),
      ('Existing narrow review-binding excerpts exact',all(z['exactText'] in (GAME/z['file']).read_text(encoding='utf-8') for z in bindings)),
      ('All governing excerpts exact',all(z['exactText'] in (GAME/z['file']).read_text(encoding='utf-8') for z in excerpts)),
      ('Only120 General pending after source routing',len([x for x in f if x['id'] not in reviewed|routed|set(QUESTIONS)])==120 and all(x['type']=='General' for x in f if x['id'] not in reviewed|routed|set(QUESTIONS))),
      ('All protected source/rule files unchanged',all(sha(GAME/q)==h for q,h in protected.items()))]
    assert all(v for _,v in checks),[n for n,v in checks if not v]
    counts={'sourceFeats':335,'operationalReviewed':8,'pending':327,'selectedHeritageMutation':22,'racial':9,'mutationCategories':13,'warriorCounterpartPairs':12,'completeWarriorMutationCards':len(mutations),'completeAncestryRecords':9,'ancestryVariants':sum(len(z['matchingCurrentAncestryRecord']['variants']) for z in heritage),'scopedReviewBindings':len(bindings),'currentGuideExcerpts':len(excerpts),'otherPendingFocusedPreparation':120}
    data={'status':'prepared-not-sent; source and counterpart evidence only','sourceFileSha256':sha(ROOT/'src/data/feats.js'),'selectedFeats':rows,'warriorCounterpartPairs':pairs,'warriorMutationCards':mutations,'warriorEngine':warrior['engine'],'warriorCatalogStatus':warrior['status'],'heritageSourceMatches':heritage,'ancestrySourcePolicy':ancestry['sourcePolicy'],'scopedReviewBindingExcerpts':bindings,'currentGoverningExcerpts':excerpts,'counts':counts,'checks':[{'name':n,'pass':v} for n,v in checks],'protectedFiles':protected,'featsApproved':0,'newRules':False,'cosmology':'post-push only; names and eligibility evidence do not establish origins or creature ontology'}
    dump(AUDIT/'HERITAGE_MUTATION_FEAT_SOURCE_PREPARATION.json',data)
    lines=['# Heritage and mutation feat source review','',data['status'],'',
      'This preserves all22 pending source identities outside General after the five earlier packets: nine Racial, five Aberrant_mutation, four Combat_mutation and four Vital_mutation. Aberrant Mind has no matching Warrior mutation-feat card in the supplied twelve-card subset; its category alone does not impose Warrior class access.','',
      'Twelve standalone mutation feats have corresponding provisional Warrior cards with additional class-level gates and more specific effects. Both complete versions are supplied side by side. Reconcile their identity, acquisition and every clause before publishing one playable choice; no duplicate grant or automatic adoption of either version is approved here. Existing control/healing bindings retain their narrow reviewed roles.','',
      'All nine heritage names match complete current ancestry records, including their27 variants. This is source evidence, not a new ancestry rule. Full Warrior engine, mutation profiles and selected review bindings accompany the questions.','',
      '| Case | Source feat | Prerequisite | Full-clause decision |','|---|---|---|---|']
    for z in rows:
        x=z['sourceObject'];lines.append(f"| {z['questionId']} | {x['name']} ({x['id']}) | {x['prerequisite']} | {z['fullClauseQuestion']} |")
    lines+=['','Prepared only; finish active Jewelcrafting before sending another conference. Current full-feat approval remains8/335. The remaining120 pending source identities are General-category entries requiring focused preparation. Preserve all original flags and labels. Do not review cosmology, invent ancestral origins or map a creature type from flavor; post-push review remains separate.','']
    audit='\n'.join(lines);write(AUDIT/'HERITAGE_MUTATION_FEAT_SOURCE_AUDIT.md',audit)
    packet='\n\n'.join(['PREPARED HERITAGE/MUTATION FEAT CONFERENCE — NOT SENT.\n22 complete sources and22 individual questions;12 complete Warrior counterparts;9 ancestry records including variants;actual mutation engine/profiles and scoped review bindings. Reconcile full clauses and identity/acquisition explicitly. No duplicate grants,hidden source deletion,full-feat promotion or cosmology decision.',audit,'COMPLETE SOURCE AND DEPENDENCY EVIDENCE',json.dumps(data,ensure_ascii=False,separators=(',',':'))])
    p=AUDIT/'CODEX_HERITAGE_MUTATION_FEAT_SOURCE_PREPARED.txt';write(p,packet)
    status={'status':'prepared-not-sent','packetFile':p.name,'characters':len(packet),'packetSha256':sha(p),'counts':counts,'checkCount':len(checks),'protectedFilesUnchanged':len(protected),'featsApproved':0,'sourceInformationDeleted':0,'cosmology':'post-push only'}
    dump(AUDIT/'HERITAGE_MUTATION_FEAT_SOURCE_STATUS.json',status);print(json.dumps(status))
if __name__=='__main__':main()
