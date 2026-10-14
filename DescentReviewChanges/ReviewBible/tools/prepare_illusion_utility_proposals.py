"""Concrete unapproved utility-illusion proposals, with complete original source records."""
from pathlib import Path
from datetime import datetime, timezone
from copy import deepcopy
import hashlib
import json

R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

DRAFTS={
'blurred-visage':{
 'kept':'Action,V/S, caster-only benefit, half cover versus ranged attacks, one-round duration and all actual class/rank0 access. Core range30ft remains in the full source record.',
 'sourceConflictDisposition':'PROPOSED: the explicit caster target controls recipient identity. Retain30ft in source metadata; it creates no selectable ally target or ranged aura. The card explicitly says Self without silently editing the source range.',
 'activation':'Action','rangeFeet':0,'targets':'Self; the actual caster only','components':['V','S'],'concentration':False,
 'duration':'One round: NEW until the start of your next regular turn, with an absolute six-elapsed-second endpoint outside initiative; keep the original marker if initiative changes.',
 'resolution':'Automatic effect on the caster. NEW visual scope: the benefit applies to an incoming ranged attack whose targeting actually relies on ordinary sight of the caster. A source that actually sees through this illusion or targets wholly through an unaffected alternate sense receives no benefit-imposed obstruction.',
 'effect':'Blur the caster\'s visible outline. For an eligible ranged attack, treat the caster as having half cover (+2 AC). Use the strongest applicable cover category, never add this to other half/three-quarters cover. It is not a physical barrier or total cover and does not change legal line of effect. NEW source-limited scope: no DEX-save benefit, because the printed benefit is versus ranged attacks; other independently actual cover keeps its own save benefit.',
 'scaling':'None. No ally targets, larger area or duration increase from level.',
 'limitations':'No protection against melee attacks, automatic Hidden/Invisible condition, miss chance, retaliation or forced aiming. The caster remains at the same actual position. A new successful casting replaces the caster\'s earlier Blurred Visage; overlapping copies never add cover or bank durations. Casting has its actual Refrain/component cost even when an existing stronger cover makes the effect numerically irrelevant. Actual interaction/examination follows the existing visual-illusion evidence rules; recognizing this particular visual distortion defeats only this source\'s proposed visual cover, not real cover or another condition.',
 'newDecisions':['Explicit self recipient resolves unused Core30ft target ambiguity','Exact ordinary-turn/elapsed expiry','Sight-dependent illusory half-cover eligibility and recognition','Ranged-attack-only AC benefit, with no added DEX-save bonus','Replace prior same spell; no duration banking'],
 'boundaries':[
  ['Caster has real three-quarters cover and Blurred Visage against a ranged attack.','Use +5 real cover, not +7; the real cover still gives its own lawful DEX-save benefit.'],
  ['An ally stands within30ft when this is cast.','The explicit caster-only source does not grant that ally cover.'],
  ['An incoming attack uses an actual unaffected alternate sense rather than ordinary sight.','This proposed visual effect adds no half cover to that attack; actual independent cover still applies.'],
  ['Initiative ends before the next regular turn marker.','Retain the original expiry mapping; leaving initiative does not renew or freeze the one-round protection.']]
},
'disguise-self-minor':{
 'kept':'Core Action,Self,V/S,one minute; minor aspects of own appearance, distinct from the reviewed rank1 Disguise Self.',
 'sourceConflictDisposition':'No numerical conflict. Complete the undefined word minor as the explicitly bounded NEW menu below, without borrowing the rank1 spell\'s full visual-form scope.',
 'activation':'Action','rangeFeet':0,'targets':'Self; own visible body surface and actually worn clothing surfaces only','components':['V','S'],'concentration':False,
 'duration':'One minute; NEW ends earlier on your Action dismissal or actual lawful effect-ending. Record original elapsed expiry through initiative changes.',
 'resolution':'No initial save. NEW reuse of the existing local visual-illusion evidence procedure: physical interaction revealing a mismatch requires no check to recognize that evidence; an observer can spend an Action for INT/Investigation against the actual spell DC to recognize the minor illusion. Knowing the illusion reveals the actual affected appearance to that observer.',
 'effect':'Choose up to three visible surface changes at cast start: one hair/eye/skin coloration; one superficial blemish/freckle/scar appearance; one hair or beard texture/style within the actual hair\'s present volume; or one coloration/pattern on an actually worn clothing surface. Each selection is one actual localized feature/surface. The visual pattern follows the real body/clothing movements. This NEW minor menu changes no face proportions, silhouette, size, height, apparent ancestry, number of limbs, item shape, insignia provenance or actual anatomy. A pictured ordinary symbol is only that visible design, not authenticated authority or a magical glyph.',
 'scaling':'None. Three selected minor details, one minute and Self remain fixed.',
 'limitations':'No voice, scent, heat, tactile texture, mind, records, statistics, ability, clothing protection, new equipment, missing limb, age-dependent body change or concealment condition. An actual item leaving the caster\'s worn possession loses its surface illusion; returning it does not create a new timer. An observer\'s response uses ordinary evidence and social procedures; there is no automatic identity success or bonus. Recasting replaces this caster\'s previous minor disguise. With another independently lawful appearance effect, do not combine surface edits into permissions neither card grants; keep each source and its own expiry, and resolve any actual incompatible visual claim before play through the governing illusion procedure.',
 'newDecisions':['Finite three-detail visual surface menu','Explicit difference from the existing full rank1 visual disguise','Existing investigation/physical-evidence procedure applied to this minor spell','Actual worn-item exit and source-separated overlap histories'],
 'boundaries':[
  ['Caster changes hair color and adds a visible cheek scar.','The colors and scar image change; a touched cheek has its actual texture and no wound/HP change.'],
  ['Caster requests another ancestry\'s anatomy or a taller silhouette.','Outside the proposed minor menu; knowing this cantrip supplies no transformation or full disguise.'],
  ['A cloak with a recolored pattern is removed and passed to an ally.','Its own surface illusion ends on leaving worn possession; no new disguised cloak is manufactured.'],
  ['An observer successfully investigates the minor disguise.','That observer recognizes/sees the actual affected surface, without automatically revealing unrelated magic or secret identity records.']]
},
'phantom-footsteps':{
 'kept':'Core Action,30ft,V/S,Instantaneous; audible footsteps moving in one direction.',
 'sourceConflictDisposition':'PROPOSED transient delivery completes Instantaneous without installing an ongoing movable or repeating source: one sequence is delivered over at most six actual seconds and then ceases.',
 'activation':'Action','rangeFeet':30,'targets':'One perceived unobstructed starting point and one declared straight direction/path entirely within30ft','components':['V','S'],'concentration':False,
 'duration':'Instantaneous finite sequence, NEW up to six seconds of actual delivery; no waiting or repeated playback.',
 'resolution':'Automatic creation of the specified sound sequence. Actual recipients require hearing and an available acoustic path. No save, attack or compulsory search/turn is generated. An observer may use the actual ordinary investigation/perception action and evidence to question it; the NEW explicit illusion scrutiny procedure is one Action INT/Investigation against spell DC, with no requirement to roll against directly conclusive physical evidence.',
 'effect':'Produce one succession of ordinary walking or running footstep sounds along a straight path of at most30ft chosen at casting; both endpoints and every point remain within30ft of the caster at resolution and unobstructed by total cover for placement. Choose an actual plausible step cadence and audible surface character the caster knows. At most six seconds of sound plays at ordinary footstep volume, from successive points along the path; it stops at an impassable placement obstruction rather than turning or passing through it. No path adjustment, branching, second direction, automatic repeat or sound after the recorded endpoint.',
 'scaling':'None. Fixed30ft placement range and maximum path, one direction and one finite sequence.',
 'limitations':'The sound creates no physical feet, creature, tracks, mass, tremor, displaced dust, trap pressure, attack or occupied space. It does not certify a real walker, hide the caster\'s V, grant a Stealth success, force targeting or require a sentry to search. A convincing distraction uses actual circumstances and ordinary checks, without a bonus from this card. Recognizing the illusion provides its actual evidential result; it does not physically silence sound for every other creature. Actual sound suppression blocks the affected delivery; missed sounds are not queued after suppression. Repeated casts have their own costs/Refrain and cannot extend a prior one-shot path.',
 'newDecisions':['Six-second,30ft straight-path finite delivery','Real placement/cover and heard-sound boundaries','Source volume/cadence/surface knowledge','Voluntary scrutiny versus direct evidence; no compelled distraction'],
 'boundaries':[
  ['Start20ft east of the caster and run30ft farther east.','Illegal proposed path: portions lie beyond30ft casting placement range. Choose a fully in-range path.'],
  ['Footstep sounds approach a closed solid door.','The placed moving source stops at the obstruction rather than emerging beyond it. Sound that normally reaches a listener still uses actual acoustics.'],
  ['A pressure plate lies on the chosen apparent route.','No physical walker or weight exists, so footsteps alone do not press it.'],
  ['A guard hears the sequence and suspects an illusion.','No automatic forced search, target switch or failed defense; use actual chosen actions and supported investigation.']]
},
'shadow-mark':{
 'kept':'Core Action,30ft,V/S; an invisible mark visible only to its caster. Complete delayed persistence without editing the retained Instantaneous source field.',
 'sourceConflictDisposition':'PROPOSED NEW one-hour mark, no concentration, rather than treating Instantaneous as either no usable mark or permanent unbounded tracking. The exact source duration stays in the original record.',
 'activation':'Action','rangeFeet':30,'targets':'One perceived noncreature object or fixed surface point with line of effect within30ft; consenting holder if worn/carried','components':['V','S'],'concentration':False,
 'duration':'NEW one hour from actual resolution; earlier destruction of the marked surface, Action dismissal by caster, or actual applicable effect-ending. Movement/suppression does not pause or reset it.',
 'resolution':'Automatic legal placement; no save/attack. Choose one simple visible-to-caster shape or short literal symbol the caster can actually specify, fitting a palm-sized area. A creature\'s body is not an eligible target in this proposed ordinary-object profile; a worn object still requires actual holder consent.',
 'effect':'Place the mark on the actual chosen surface. Only this caster can ordinarily see the mark when they have actual sight/line of sight and sufficient visual access to that surface. It is an identity cue for that actual marked surface, not a map beacon, sensing ability, telepathic ping or proof about the object\'s nature. The mark does not emit light, reveal a hidden object, defeat darkness/blindness/invisibility, or allow seeing through cover. Moving the object moves its actual mark; a fixed surface mark stays there.',
 'scaling':'None. NEW maximum three active marks per caster and one per caster on an exact marked surface; a fourth successful mark ends that caster\'s oldest at resolution.',
 'limitations':'A new successful same-caster placement on the same surface replaces its old mark and has its own paid cast/history. Different actual casters\' marks remain separate, individually invisible to other casters, within each owner\'s own cap; no shared ownership grants another reader. Copying, painting, repairing or substituting an object does not reproduce, transfer or recharge the magic. Actual casting/component observation remains possible, even though the resulting mark is not ordinarily visible to others. This spell does not cancel a specific lawful detection/dispel effect that explicitly applies; generic sight alone does not reveal the mark to another creature. The spell grants no forgery authentication, protected meaning, remote location updates or privileged targeting. Surface destruction ends that mark; no storage of its remaining lifetime.',
 'newDecisions':['One-hour persistence and three-mark owner cap','Palm-sized ordinary-object/surface targeting, consent and no creature profile','Actual-sight-only caster visibility rather than remote tracking','Separate owners, physical identity, replacement and destruction lifecycle'],
 'boundaries':[
  ['A marked crate is carried behind a wall.','The caster cannot see the mark or infer the crate\'s present location through that wall.'],
  ['A creature carries a marked cloak through darkness.','The mark supplies no light or extraordinary sight; normal actual visibility remains necessary.'],
  ['A second caster marks the same actual surface.','Each has their own record/cap/expiry and sees only their own mark normally; neither acquires the other\'s ownership or remote knowledge.'],
  ['The marked piece is destroyed and replaced by an identical repair.','Its magic does not transfer to the replacement surface or reset the old clock.']]
}
}

def main():
    out=A/'ILLUSION_UTILITY_CANTRIP_AUTHORING_PROPOSALS.json';assert not out.exists()
    sources=[A/'LOW_ILLUSION_SPELL_SOURCE_PREPARATION.json',R/'data/public/spell_playtests/catalog.json',R/'docs/mechanics/SPELL_INTEGRATION_RULES.md',R/'docs/mechanics/COMBAT_ACTION_PLAYTEST.md',R/'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md']
    hashes={str(p.relative_to(G).as_posix()):sha(p) for p in sources}
    prep=read(sources[0]);selected={s['spellId']:s for s in prep['selectedSpells']}
    catalog={s['id']:s for s in read(sources[1])['spells']}
    proposals=[]
    for sid,draft in DRAFTS.items():
        row=selected[sid];original=row['fullSourceAndCurrentAccessRecord'];assert original==catalog[sid] and original['operational'] is None
        proposals.append({'spellId':sid,'questionId':row['questionId'],'status':'Unapproved Codex proposal for the existing low-rank137 source conference; UNSENT',
            'existingPreparation':sources[0].relative_to(G).as_posix(),'existingQuestion':row['individualQuestion'],
            'completeOriginalSourceAndAccess':deepcopy(original),'sourceRecordSha256':row['recordSha256'],
            'proposedOperational':{k:v for k,v in draft.items() if k not in ('kept','sourceConflictDisposition','newDecisions','boundaries')},
            'preserved':draft['kept'],'sourceConflictDisposition':draft['sourceConflictDisposition'],'newDecisions':draft['newDecisions'],
            'authoredBoundaryCases':[{'setup':a,'proposedOutcome':b,'runtimeExecuted':False} for a,b in draft['boundaries']],
            'catalogChanged':False,'promoted':False})
    counterparts=[deepcopy(catalog[x]) for x in ('minor-illusion','silent-image','disguise-self')]
    report={'status':'Four finite utility-cantrip proposals; source conference not yet dispatched','preparedAtUtc':datetime.now(timezone.utc).isoformat(),
        'scope':'Supports IL05,IL07,IL08,IL09 within the complete low-rank137 conference; not approval or a substitute for the other pending spells.',
        'commonCastRule':'Retain actual class-specific school/rank/repertoire and RP/extra-cost gates, components, cast-start payment/concentration/Refrain, legal interruption and original source objects. Same-stat flat bonuses use strongest; cover uses strongest category; no implicit spell scaling.',
        'proposals':proposals,'unchangedReviewedCounterparts':counterparts,'protectedInputs':hashes,
        'sourceFactsVersusNewRules':'Source numbers and effects are explicitly separated from proposed modes, targeting, sense dependence, duration reconciliation and lifecycle. GPT must consider/amend these concrete proposals in the dedicated source review before any catalog promotion.',
        'allProtectedInputsUnchanged':hashes=={str(p.relative_to(G).as_posix()):sha(p) for p in sources},'newApprovals':0,'sourceInformationDeleted':0,'runtimeChanged':False,'cosmologyReviewed':False,'submitted':False}
    assert report['allProtectedInputsUnchanged']
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Four utility illusion cantrip proposals','', '**UNSENT and unapproved.** Full original records, exact current access and reviewed comparison cards are preserved in the [structured proposal](ILLUSION_UTILITY_CANTRIP_AUTHORING_PROPOSALS.json). These NEW choices await the existing complete low-rank source conference; the catalog remains unchanged.','',report['commonCastRule'],'']
    for p in proposals:
        lines += [f"## {p['questionId']} — {catalog[p['spellId']]['name']}",'', '**Preserved:** '+p['preserved'],'','**Source disposition:** '+p['sourceConflictDisposition'],'']
        lines += [f'**{k}:** {v}' for k,v in p['proposedOperational'].items()]
        lines += ['','**Explicit NEW choices:** '+ '; '.join(p['newDecisions']),'','**Authored boundary cases; no runtime result claimed:**','']
        lines += [f"- {x['setup']} {x['proposedOutcome']}" for x in p['authoredBoundaryCases']]
        lines += ['']
    (A/'ILLUSION_UTILITY_CANTRIP_AUTHORING_PROPOSALS.md').write_text('\n\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'proposals':len(proposals),'accessBindings':sum(len(p['completeOriginalSourceAndAccess']['classAccess']) for p in proposals),'reviewedCounterpartsPreserved':len(counterparts),'authoredBoundaryCases':16,'catalogChanges':0,'approvals':0,'submitted':False},indent=2))

if __name__=='__main__':main()
