"""Prepare next exact-source conference; no catalog promotion or adoption."""
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
ids=['harmonic-bulwark','polymorph','shapechange','true-polymorph','mass-polymorph']
catalog=json.loads((ROOT/'data/public/spell_playtests/catalog.json').read_text(encoding='utf-8'))
current={r['id']:r for r in catalog['spells']}
rows=[]
for ident in ids:
    r=current[ident]
    assert r['status']=='blocked-pending-operational-review' and r['operational'] is None
    rows.append({'id':ident,'catalogSource':r['source']['original'],
                 'coreEntries':r['source']['coreEntries'],'possibleHistoricalAliases':r['source']['possibleHistoricalAliases'],
                 'classAccess':r['classAccess'],'currentStatus':r['status'],
                 'wholeOverlaySnapshot':r,
                 'overlaySha256':hashlib.sha256(json.dumps(r,ensure_ascii=False,sort_keys=True).encode()).hexdigest()})
data={'status':'PREPARED / UNDISCUSSED: next named five-spell completion batch',
      'spellIds':ids,'spells':rows,'costByRank':catalog['costByRank'],
      'originalCatalogPreserved':True,'overlayPromotionAuthorizedByDiscussion':False}
(HERE/'TRANSFORMATION_SPELL_SOURCE_CANDIDATES.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
questions='''# Five named spell completion conference

Codex → Calibration Review. The user wants the entire game developed, so named blocked components now need actual operational completion. This batch is Harmonic Bulwark, Polymorph, Shapechange, True Polymorph and Mass Polymorph. All five original catalog identities, school placements, access gates and Core fields are supplied below. No source is to be deleted, aliased automatically or imported from another game's rules.

The preceding form/shield reference is a same-body, one-HP, one-buffer chassis. Its26 Druid profiles, class gates and finite reserves are Druid-specific; spell transformations may share state machinery but never silently grant those class features. Complete five individual operational drafts; label every new specification. Preserve the original names and all class-specific ranks/learn levels/baseRP. Do not let the global lowest rank replace class access. Keep each source's explicit scope, notably Mass Polymorph's up to10 creatures and True Polymorph's permanent creature/object transformation.

Please discuss and decide every numbered issue before presenting source-qualified drafts:

1. Harmonic Bulwark's catalog says5 tempHP per RP. Possible historical Mana Shield says2 perRP, Action/60ft/instant/V,S,F/base5RP. The alias is not proven. Choose exact operational target, Action, components, duration, what RP is counted, additional-payment bounds, and discount/Refrain interaction. Preserve5-perRP source identity rather than silently replace it with the alias. Explicitly distinguish base spell cost from discretionary extra conversion and prevent discounts/free copies from producing shields based on unspent RP. If copying any alias metadata, label it NEW, not recovered fact.
2. Polymorph's Core gives Action/60ft/V,S,F/7RP but “instantaneous” contradicts an undefined ongoing form. Shapechange givesAction/120ft/V,S,F/26RP/instantaneous yet saysdifferent creature eachround. MassPolymorph givesAction/120ft/V,S,F/26RP/instantaneous/up to10. Choose actual durations/concentration/target rules as explicit NEW reconciliation. TruePolymorph alone explicitly saysuntil dispelled: preserve that meaningful permanence in the playable draft, not an unexplained3round downgrade.
3. Which modes require willing targets and which allow hostile targets? Specify saves, repeat saves, damage breaks, dispelling, immunities, legendary exceptions and payment timing. A forced form needs an explicit agency/control procedure and must respect the reviewed hard-denial limit if it actually denies an Action. Consider how anatomy and speech restrictions affect the subject's available actions. Keep the player in control of their decisions.
4. Define a finite spell-form list with complete size, movement, senses, speech/hands, operative AC, natural attacks, damage types and qualified passive defenses. Prefer clearly labeled spell profiles over copying unreviewed bestiary statblocks. Distinguish Polymorph/Mass's available forms from Shapechange/True's rank9 capability. Do not import multiattack, class spells, legendary powers, arbitrary CR, new RP, healing or rest resources. The repository has a large separate bestiary; it has not yet passed this full-game mechanics conference, so presence of a creature name is not an approved combat profile.
5. State retained HP, maximum HP, temporary HP, Wounds, conditions, attributes, proficiency and identity. Does a supplied attack or DC use the subject's or original caster's current attributes? Define the calculation for NPCs without player class levels/S/M. Changing form must not duplicate bodies, gear, corpses, souls, resources, buffs, initiative entries or condition clocks.
6. Specify spellcasting and equipment. What class/passive abilities can the subject still use, what anatomy or components block them, and how does anatomy-compatible melded-item AC apply? Ordinary natural attacks remain separate from unresolved weapon-only proc taxonomy. No silent hand/material access. State whether subject can end a willing effect, caster can end it, and exact Action cost/timing.
7. Form defenses apply to the one triggering damage packet, without a second beast-HP pool. When does a spell form revert relative to a valid would-drop-to-zero/instead-remain-at-one effect? What happens to permanent True Polymorph at zero HP or death, and to transformed objects on damage, destruction or dispelling? Close healing-on-reversion and missing-vital-body ambiguities.
8. Shapechange's switch each round needs an exact action, frequency clock, space requirement, subtype identity and concentration rule. Specify its target and treatment of existing effects. If narrowing the printed 120-foot range, preserve that source metadata and label the change. Switching grants no Druid reserves, repeated entry shields or per-rest resets.
9. True Polymorph's creature-to-object, object-to-creature and object-to-object modes need exact eligibility, mass/size/material bounds, targeting of carried/worn objects, agency, commands, combat profiles, permanent identity and dispel/antimagic transitions. Is an object made into a creature independent or a controlled companion? Apply the shared command budget if controlled. Prevent fabrication of valuable materials, consumables, usable corpses, souls, XP and loot while giving permanent transformation meaningful uses. “Permanent” does not automatically mean irrevocable or erase original identity.
10. For Mass Polymorph, specify preselected targets/forms, legal space at commitment, individual saves and independent outcomes within one casting. Use one concentration record with target-specific endings. Preserve the explicit up-to-ten target count instead of importing a generic three-target cap. Distinguish casting range/line of sight from any ongoing tether.
11. Resolve competing transformations: recasts, different casters, a Druid form plus a spell form, simultaneous endings and creature/object chains. Define one active anatomy without hidden forms or resource refreshes. Ordinary transformation spells follow spell Dissonance/Refrain rules; casting one is not automatically a Druid Shapeshift reset.
12. Present complete individual objects with fields id, activation, rangeFeet, targets, duration, concentration, components, resolution, effect, scaling, limitations and designNotes. Add exact profile/state tables as needed. Identify preserved clauses, new decisions and future dependencies. Do not leave all missing rules to Director discretion or claim human balance/the whole project complete.

The integration should remain reviewable: source-specific drafts first, then executable boundedreference checks and independent implementationreview before activating catalog entries.
'''
parts=[questions,'\n## Core RP by rank\n```json\n'+json.dumps(catalog['costByRank'],indent=2)+'\n```\n']
for r in rows:
    trimmed={k:v for k,v in r.items() if k!='wholeOverlaySnapshot'}
    parts+=['\n## '+r['id']+'\n```json\n'+json.dumps(trimmed,ensure_ascii=False,indent=2)+'\n```\n']
for ident in ('resonance-shield','heroism','false-life'):
    r=current[ident]
    parts+=['\n## Existing separate operational buffer comparison: '+ident+'\n```json\n'+json.dumps({k:r[k] for k in ('id','classAccess','additionalRpCost','operational')},ensure_ascii=False,indent=2)+'\n```\n']
path=HERE/'CODEX_TRANSFORMATION_SPELL_CONFERENCE_PREPARED.md';path.write_text(''.join(parts),encoding='utf-8')
print('Prepared5 source-qualified spell conference, not sent/adopted:',path.stat().st_size,'bytes')
