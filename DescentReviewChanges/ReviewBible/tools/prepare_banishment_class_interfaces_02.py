"""Preserve additional current class interfaces for the separate Banishment conference."""
from datetime import datetime,timezone
import json,re
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p): return json.loads(p.read_bytes())

def main():
    out=A/'BANISHMENT_CLASS_INTERFACE_ADDENDUM_02.json'
    assert not out.exists()
    original=read(A/'ac4-current-review-01-input/CURRENT_REVIEW_INPUT.json')
    pattern=re.compile(r'banish|exile|cross[- ]plan|interplan|another plane|other plane|planar|teleport|extradimensional',re.I)
    rows=[];bindings=[]
    for cls in original['currentClasses']:
        p=G/cls['file']['path'];assert info(p)==cls['file'];bindings.append(info(p))
        def walk(n,ptr=''):
            if isinstance(n,dict):
                if all(k in n for k in ['id','name','effect']):
                    searchable={k:v for k,v in n.items() if k not in ['source','sourceEvidence','originalSource','sourceFiles']}
                    if pattern.search(json.dumps(searchable,ensure_ascii=False)):
                        rows.append({'class':cls['class'],'file':info(p),'pointer':ptr,'id':n['id'],'completeCard':n})
                for k,v in n.items():
                    if k not in ['source','sourceEvidence','originalSource','sourceFiles']:
                        walk(v,ptr+'/'+k.replace('~','~0').replace('/','~1'))
            elif isinstance(n,list):
                for i,v in enumerate(n):walk(v,ptr+'/'+str(i))
        walk(read(p))
    manual={
      'cleric.arch.banish-unholy':'Distinct class technique. WIS, radiant damage/push and next-turn rider are not the ordinary spell CHA/60-second proposal. Its nearest-legal return is comparison evidence, not a complete finite-cell termination rule.',
      'oracle.supplement.fate-bound.fate-bound-boon-iv':'Actual acquired Fate-Bound Oracle15 grants +2 versus banishment. The 1/LR death-save reroll does not become a banishment reroll.',
      'paladin.supplement.oath-of-vengeance.no-escape':'Voluntary teleport/extradimensional prohibition must be distinguished from hostile forced exile and mandatory source-ending return. Willing election of save failure needs an explicit decision. Do not infer immunity from the feature name.',
      'paladin.supplement.oath-of-vengeance.verdict-absolute':'The actual brand clause prevents voluntary teleport/invisibility. It is not a general banishment immunity or an automatic counterspell.',
      'paladin.supplement.oathbreaker-oath-of-chains-broken.reign-of-ashes':'Cannot benefit from teleportation requires explicit reconciliation with the new Banishment transport classification, willing rescue versus hostile exile, and required return. Preserve exact source wording; do not silently universalize No Escape voluntary scope.',
      'paladin.supplement.oath-of-the-chain.chain-of-duty':'Its actual0-HP rescue requires same plane and60 feet. A target in a distinct cell does not qualify merely because its origin anchor is near the Paladin.',
      'paladin.supplement.oath-of-chains-broken.liberty-s-step':'Supplies movement permissions only; no teleport or passage through occupied solid boundaries.',
      'soldier.arch.hold-the-line':'Speed0 soft control expressly permits teleport and forced movement. Banishment is not blocked by Speed0 alone.',
      'soldier.hero.champion.divine-lockdown':'Physical suppression expressly leaves teleport available. Reaction loss can matter separately but does not become planar anchoring.',
      'soldier.hero.tyrant.execution-zone':'The exact source permits teleport/forced movement and is not an impassable magical wall.',
      'thief.arch.crippling-strike':'Its slow expressly does not deny teleport. Preserve ordinary agency/actions separately.',
      'wizard.arch.dimensional-pocket':'This stores unattended nonliving material, excludes living creatures and is not a generic doorway to any selected plane. An active nonliving Construct creature cannot be assumed to be unattended material. The actual overflow return is comparison evidence only.',
      'mage.hero.lich.corpse-gateway':'Requires an actual visible eligible corpse and adjacent destination. It grants no remote view, arbitrary cross-plane knowledge or invented corpse inside the cell. Source corpse identity and eligibility remain real.',
      'mage.base.blink':'Perceived legal space within30 feet and actual planar wards apply. A local teleport supplies no unprinted external view or cross-plane exit.',
      'oracle.supplement.dream.unreality':'An attack-triggered miss/teleport cannot trigger from Banishment own CHA save; a separately eligible incoming attack retains its actual trigger. No arbitrary dodge against all spell casts.'
    }
    ids={r['id'] for r in rows};assert set(manual)<=ids
    for row in rows:
        row['independentDisposition']=manual.get(row['id'],'Navigation evidence only; no claim of independent complete semantic review from keyword matching.')
        row['independentlyReadForThisAddendum']=row['id'] in manual
    scenarios=[
      ('BAN-C19','An actual No Escape mark is active on target T. T is unwilling and fails a legal Banishment save; compare T voluntarily electing failure to accept rescue.','Decide exact voluntary/forced transport predicate for these two branches; do not label all banishment voluntary or all willing transport forced.'),
      ('BAN-C20','T was exiled before a No Escape or Reign of Ashes restriction could lawfully become active on it. The60-second deadline now arrives.','Resolve actual application legality first, then mandatory return versus the exact active transport restriction. No indefinite cell from a blanket blocker; no silently invented source exception.'),
      ('BAN-C21','A Chain of Duty ally reaches0 inside the separate cell; its old origin anchor is20 feet from the Paladin.','Same-plane rescue condition is false. Anchor distance does not replace actual target plane/location; no free Paladin entry.'),
      ('BAN-C22','A cell occupant with Wizard Dimensional Pocket attempts to create storage and enter it. Compare an active nonliving Construct occupant.','Living entry is expressly barred; a creature is not unattended material merely because nonliving. Do not confer a new cell escape through an inventory ability.'),
      ('BAN-C23','A visitor has an independently legal interplanar route to the cell, actual knowledge and enough fitting space; arrival would occur before t60.','The existing draft has no complete terminal state for that visitor. Review a finite entry/collapse protocol explicitly; neither absence of free return nor source expiry permits stranding/deletion.'),
      ('BAN-C24','T uses an otherwise legal creature-creation ability inside the cell; a distinct creature would remain when t60 arrives.','Treat internally created bodies as well as visitors. A no-visitor rule alone does not close this case. Preserve real source costs and creature identity; specify finite terminal placement.'),
      ('BAN-C25','Origin footprint is aboard a moving vehicle, or the origin surface becomes unsupported during exile.','Choose fixed-world anchor versus support-attached coordinates explicitly. The local draft proposes fixed origin and pre-change early return; evaluate real event boundaries and Falling, not a hidden force-wall reservation.'),
      ('BAN-C26','One atomic source event changes T geometry and another body occupancy so the preserved anchor no longer fits. No intermediate state is exposed by that source.','Complete the draft unresolved atomic-change branch. Preemptive return cannot depend on retrospectively splitting an indivisible resolved event.'),
      ('BAN-C27','T dies in the cell with genuine worn gear; separately a finite Null Disabled summon expires there.','Return actual surviving corpse/objects under their source identities; no resurrection, Hunt reset, recreated summon body, free loot or repeated corpse use.'),
      ('BAN-C28','Before the endpoint, T lawfully escapes elsewhere with some original gear and leaves other objects in the cell.','Do not drag escaped T back. Settle every remaining real object once and close the cell by a finite rule, preserving consumed/moved object history; no duplicated cargo or new permanent plane.')
    ]
    doc={'id':'BANISHMENT-CLASS-INTERFACES-02','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'Unsubmitted independent comparison addendum; unresolved scenarios are requirements for complete authorship, not operative rules',
      'priorDraft':info(A/'banishment-local-draft-01/PROPOSAL.json'),'sourceBindings':bindings,'classEnvelopesScanned':len(bindings),'navigationMethod':pattern.pattern,
      'nonExhaustiveWarning':'Lexical navigation is not proof of all semantic class coverage. All17 full envelopes should accompany the actual conference; only explicitly marked cards were independently read here.',
      'exactComparisonCards':rows,'independentlyReadCards':len(manual),'newAuthoredReviewScenarios':[{'id':ident,'initialState':state,'requiredResolution':resolution,'runtimeTest':False,'adopted':False} for ident,state,resolution in scenarios],
      'sourceChecks':len(bindings),'failureCount':0,'newRulesAdopted':False,'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'humanPlaytested':False}
    out.write_bytes(encoded(doc));print(json.dumps({'artifact':info(out),'classEnvelopes':len(bindings),'exactNavigationCards':len(rows),'independentlyReadCards':len(manual),'newScenarios':len(scenarios),'failureCount':0}))

if __name__=='__main__':main()
