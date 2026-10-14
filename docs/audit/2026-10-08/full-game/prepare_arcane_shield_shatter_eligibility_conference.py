from pathlib import Path
import json,hashlib
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
cat=read(R/'data/public/spell_playtests/catalog.json')['spells'];by={s['id']:s for s in cat}
ids=[s['id'] for s in read(A/'ARCANE_SHIELD_SHATTER_CANDIDATE_EFFECT_SCAN_249.json')['rows']]+['false-life','resistance']
rows=[]
for ident in ids:
 s=by[ident];assert s['operational']
 rows.append({'id':ident,'sourcePlacements':s['source']['original']['placements'],'actualClassRankSchool':{k:{'rank':v['rank'],'school':v['school']} for k,v in s['classAccess'].items()},'completeExistingOperationalCard':s['operational']})
intro='''CODEX — ARCANE SHIELD SHATTER ELIGIBILITY CONFERENCE BEFORE RANK-ONE EXACT AUTHORING.

The twelve Evocation rank-one sources and eight authoring clarifications are saved. Catalog remains249 reviewed/599 unfinished; no new rank-one card is selectable. The existing249 cards below are comparison evidence, not proposed rewrites. Cosmology remains deferred until after verified GitHub delivery.

One consequential definition remains ambiguous. Your first source conference required a spell expressly identified by its source as a shield/barrier/ward providing direct defensive protection, and excluded generic resistance buffs or ordinary temp HP merely feeling shield-like. The later clarification adds 'or equivalent defensive protective effect'. Please specify whether that phrase intentionally broadens eligibility, or only covers an expressly sourced shield/barrier/ward under another equivalent label. We need a finite source-qualified predicate, not a name-substring search and not a generic rank0–1 buff dispel.

I found ten currently reviewed low-rank identities matching source words shield/barrier/ward, plus False Life and Resistance as useful contrasts. Their COMPLETE current operational cards, original placements and actual class rank/school rows follow. This word scan does not grant eligibility. Please give a one-row explicit qualify/exclude/conditional disposition for EACH of the12, with the actual reason and the relevant condition. Keep rank0–1, current perception/LoE, both effect and creature within30, paid hidden eligibility, successful-ending-before1d8force, and actual parent callbacks intact.

Specific issues:
1. Arcane Ward, Shield and Alignment Shield grant defensive AC, but stronger same-stat flat bonuses can supersede their arithmetic without ending their source records. Does an established weaker ward remain an eligible protective effect? I propose yes while its otherwise-applicable defensive component exists, even if a stronger concurrent bonus wins. Do not confuse arithmetic arbitration with immunity/suppression. What if Alignment Shield has no currently attacking opposed-alignment creature? A still-active conditional defense can be eligible without revealing any hidden alignment. If an effect is actually wholly suppressed rather than merely superseded, choose whether it is eligible now or must wait until protection resumes; no diagnostic should leak the reason.

2. Resonance Shield: its source is explicitly a shield and its currently accepted tempHP absorb damage, but its own remaining points/source identity must still exist. Existing FORM_TEMP_HP_PLAYTEST.md says: a single active grant retains identity/source/owner/recipient/points/endpoint; a larger offer replaces it, an equal/smaller offer is discarded, discarded shields do not remain underneath, a zero offer creates no grant. Administrative expiry/replacement is not damage or paid absorption. Please confirm Shatter can remove ONLY a genuinely current accepted grant from this spell, never a later False Life/class shield pool or a discarded/depleted historical grant. Are spell-granted tempHP with a finite operational lifetime treated as an ongoing defensive effect despite raw Core Instantaneous metadata? If yes, make that explicit for this source, without treating every instantaneous historical spell consequence as dispellable.

3. Protective Sphere: this is a fixed area boundary rather than a creature-attached buff. The exact card says it blocks physical projectiles and Tiny/Small crossing, grants no cover, and rays/beams/non-projectile spells pass. Define what point represents the effect for30ft/LoE/perception (a perceived boundary point, center, or whole-area origin), which creature qualifies as currently protected, and whether ending the selected boundary ends the whole sphere application. I propose a perceived boundary point within30 and a perceived creature actually inside the sphere also within30/LoE; no requirement for a projectile to be mid-flight. It ends the actual single maintained sphere, not a custom hole. If the creature stands outside, the spell does not let the caster invent a protected-recipient relationship just because the sphere lies between them and a hypothetical attacker. Please approve/repair.

4. Corruption Ward and Minor Elemental Ward improve saves only. Are save bonuses/advantage an eligible direct defensive protection, or deliberately outside this specialist's shield scope? Source says 'such as' AC/prevention/absorption/interception/barrier, so the list alone does not settle this. Neither grants resistance or a physical shield. Choose explicitly for both and explain whether the same criterion excludes unbranded Resistance (+1d4 one save). Alarm Ward and Warning Ward only report events: I propose exclude despite names, because no actual defensive layer is ended.

5. False Life is an ongoing current spell-granted tempHP pool but lacks an expressly shield/barrier/ward source identity. The first conference appears to exclude it; the later 'equivalent defensive protective effect' could admit it. Choose explicitly. This will determine whether Shatter is a shield specialist or a broader tempHP remover. No class-created tempHP or Oracle False Life engine can qualify merely from similar wording.

6. Barrier Flicker has a very short next-projectile-attack lifetime. It may meet the predicate while actually active, but Shatter remains Action and gets no interrupt/timing exception. I propose eligibility does not invent an Action window during another attack; only an independently legal Action/Ready timing can act while its actual effect still exists. Its defenses still use the actual source timing. Confirm.

Please settle these twelve comparisons and the general predicate without changing their stored card texts or claiming all future defensive magic audited. New semantic/timing bridges belong in the Shatter exact card or a reviewed supplement. They remain provisional and still need exact manuscript review, runtime integration and human balance testing.

COMPLETE EXISTING COMPARISON EVIDENCE:
'''
p=A/'CODEX_ARCANE_SHIELD_SHATTER_ELIGIBILITY_CONFERENCE.txt';assert not p.exists();p.write_text(intro+json.dumps(rows,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
ledger={'status':'prepared; not yet submitted','scope':'Twelve unchanged operational comparison identities; no eligibility granted by name matching','ids':ids,'packetPath':str(p),'packetSha256':sha(p),'packetCharacters':len(p.read_text(encoding='utf-8')),'operationalBefore':249,'noPromotion':True}
f=A/'ARCANE_SHIELD_SHATTER_ELIGIBILITY_SUBMISSION.json';assert not f.exists();f.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(ledger,indent=2))
