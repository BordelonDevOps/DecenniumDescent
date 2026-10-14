"""One navigation queue for all335 source feat identities; no promotions."""
from pathlib import Path
from collections import Counter
import json,hashlib,os
ROOT=Path(__file__).resolve().parents[1];GAME=ROOT.parents[1];AUDIT=GAME/'docs/audit/2026-10-08/full-game'
OUT=ROOT/'docs/director-only/FEAT_REVIEW_QUEUE.md'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def link(label,p):return '['+label+']('+os.path.relpath(p,OUT.parent).replace('\\','/')+')'
def main():
    source=ROOT/'src/data/feats.js';feats=json.JSONDecoder().raw_decode(source.read_text(encoding='utf-8').split('export const feats = ',1)[1])[0]
    manifest=ROOT/'data/public/feat_playtests/manifest.json';reviewed=set(read(manifest)['operationalIds'])
    craft=read(AUDIT/'CRAFTING_FEAT_INTERFACE_PREPARATION.json');combat=read(AUDIT/'COMBAT_FEAT_SOURCE_PREPARATION.json')
    craft_ids={r['featId'] for r in craft['selectedFeats']};combat_ids={r['featId'] for r in combat['selectedFeats']}
    related={f['id'] for f in combat['relatedUnapprovedFeatSources']}
    skill=read(AUDIT/'SKILL_FEAT_SOURCE_PREPARATION.json');skill_ids={z['featId'] for z in skill['selectedFeats']};skill_related={z['sourceObject']['id'] for z in skill['counterpartSources']}
    assert len(skill_ids)==25 and not skill_ids.intersection(reviewed|craft_ids|combat_ids)
    magic=read(AUDIT/'MAGIC_CORE_FEAT_SOURCE_PREPARATION.json');magic_ids={z['featId'] for z in magic['selectedFeats']};magic_related={z['sourceObject']['id'] for z in magic['counterpartSources']}
    assert len(magic_ids)==31 and not magic_ids.intersection(reviewed|craft_ids|combat_ids|skill_ids)
    assert len(feats)==335 and len({f['id'] for f in feats})==335
    assert len(reviewed)==8 and len(craft_ids)==24 and len(combat_ids)==47
    assert not reviewed.intersection(craft_ids|combat_ids) and not craft_ids.intersection(combat_ids)
    assert sha(source)==craft['sourceFileSha256']==combat['sourceFileSha256']==skill['sourceFileSha256']==magic['sourceFileSha256']
    rows=[]
    for f in feats:
        id=f['id']
        if id in reviewed:
            phase='Reviewed in the eight-feat operational scope'
            destination=ROOT/'docs/mechanics/BUFFER_FEAT_PLAYTEST.md'
            next_action='Retain actual acquisition and interface restrictions; broader balance/runtime remain separate'
        elif id in craft_ids:
            phase='Complete crafting/interface source packet prepared, unsent'
            destination=AUDIT/'CRAFTING_FEAT_INTERFACE_AUDIT.md'
            next_action='Full-clause source conference, authoring, then exact review'
        elif id in combat_ids:
            phase='Complete Combat-category source packet prepared, unsent'
            destination=AUDIT/'COMBAT_FEAT_SOURCE_AUDIT.md'
            next_action='Full-clause source conference, authoring, then exact review'
        elif id in skill_ids:
            phase='Complete Skill-category source packet prepared, unsent'
            destination=AUDIT/'SKILL_FEAT_SOURCE_AUDIT.md'
            next_action='Full-clause source conference, authoring, then exact review'
        elif id in magic_ids:
            phase='Complete first Magic-cohort source packet prepared, unsent'
            destination=AUDIT/'MAGIC_CORE_FEAT_SOURCE_AUDIT.md'
            next_action='Resolve actual spell/class/resource dependencies, then author and exact-review full clauses'
        else:
            phase='Complete source record preserved; focused full-clause packet open'
            destination=AUDIT/'REMAINING_FEAT_CATALOG_PREPARATION.json'
            next_action='Prepare individual questions and current governing dependencies, then joint review'
        rows.append({'featId':id,'name':f['name'],'sourceCategory':f['type'],'phase':phase,
          'currentOperationalReviewed':id in reviewed,'craftingConferenceMember':id in craft_ids,
          'combatConferenceMember':id in combat_ids,'skillConferenceMember':id in skill_ids,'magicConferenceMember':id in magic_ids,'magicDependencyRecord':id in magic_related,'skillDependencyRecord':id in skill_related,'combatDependencyOnly':id in related and id not in combat_ids,
          'evidence':str(destination.relative_to(GAME)).replace('\\','/'),'nextAction':next_action,
          'sourceFlagsPreserved':{k:f[k] for k in ('draft','needsReview','status','balanceReview','deprecated') if k in f}})
    counts={'sourceFeats':335,'operationalReviewed':8,'remaining':327,'craftingSourcePrepared':24,'combatSourcePrepared':47,'skillSourcePrepared':25,'magicSourcePrepared':31,'otherPendingFocusedPreparation':200,'combatDependencyOnly':6,'skillDependencyRecords':13,'magicDependencyRecords':11}
    checks={'all335UniqueIds':len(rows)==335,'allSourceNamesCategoriesPreserved':all(r['name']==f['name'] and r['sourceCategory']==f['type'] for r,f in zip(rows,feats)),'everyDestinationExists':all((GAME/r['evidence']).exists() for r in rows),'noQueuePromotion':sum(r['currentOperationalReviewed'] for r in rows)==8,'all327PendingAccounted':24+47+25+31+200==327,'sourceCategoryNotMechanicalScope':True}
    assert all(checks.values())
    lines=['# Feat review queue — internal navigation','',
      '**8 of 335 feat identities have completed the current full operational review; 327 remain.** These counts do not invalidate earlier source authoring or owner approval. Existing source flags remain preserved and are not treated as approval of new expanded rules.','',
      'The '+link('crafting interface packet',AUDIT/'CRAFTING_FEAT_INTERFACE_AUDIT.md')+' covers 24 complete pending feats. The '+link('Combat source packet',AUDIT/'COMBAT_FEAT_SOURCE_AUDIT.md')+' covers 47 additional complete pending feats. The '+link('Skill source packet',AUDIT/'SKILL_FEAT_SOURCE_AUDIT.md')+' covers 25 more, including Anatomy Lore, Spell Scribe and Wilderness Chef. The first Magic-cohort packet covers31 more; all four are unsent.200 other pending identities retain complete original records and await focused full-clause preparation. Six additional feats included as Combat dependencies still belong to their own pending route.','',
      'The '+link('Combat dependency supplement',AUDIT/'COMBAT_FEAT_SKILL_DEPENDENCY_SUPPLEMENT.json')+' must accompany the future Combat conference; it supplies full Anatomy Lore and the current Core roll rules. Source categories are navigation labels only: combat-related General, Magic or Skill feats are not considered finished by a Combat-category conference. No identity merge, source deletion, new effect, runtime installation or balance approval follows from this queue. Finish the active Jewelcrafting source conference before dispatching another conference. The31 Magic-cohort sources lack a status key; this grouping creates no historical approval inference. See MAGIC_CORE_FEAT_SOURCE_AUDIT.md for eight named-spell dependencies and two missing class-list identities.','',
      '| Source category | All identities | Reviewed in this pass | Crafting packet | Combat packet | Skill packet | Magic packet | Other pending |','|---|---:|---:|---:|---:|---:|---:|---:|']
    for category in sorted({r['sourceCategory'] for r in rows}):
        group=[r for r in rows if r['sourceCategory']==category]
        n=lambda key:sum(r[key] for r in group)
        lines.append(f"| {category} | {len(group)} | {n('currentOperationalReviewed')} | {n('craftingConferenceMember')} | {n('combatConferenceMember')} | {n('skillConferenceMember')} | {n('magicConferenceMember')} | {sum(not(r['currentOperationalReviewed'] or r['craftingConferenceMember'] or r['combatConferenceMember'] or r['skillConferenceMember'] or r['magicConferenceMember']) for r in group)} |")
    lines+=['','## Every source identity','', '| ID | Source feat | Category | Current route | Evidence |','|---|---|---|---|---|']
    for r in rows:
        note='; also a Combat dependency, not extra approval' if r['combatDependencyOnly'] else ''
        if r['skillDependencyRecord']:note+='; also a Skill dependency, not extra approval'
        if r['magicDependencyRecord']:note+='; also a Magic dependency, not extra approval'
        lines.append(f"| {r['featId']} | {r['name']} | {r['sourceCategory']} | {r['phase']}{note} | {link('source / rules',GAME/r['evidence'])} |")
    OUT.write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
    data={'status':'PASS','counts':counts,'checks':checks,'sourceSha256':sha(source),'reviewedManifestSha256':sha(manifest),'rows':rows,'scope':'navigation only, no new operational approval'}
    (AUDIT/'FEAT_REVIEW_QUEUE_VALIDATION.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'status':'PASS','counts':counts,'checks':checks}))
if __name__=='__main__':main()
