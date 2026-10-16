"""Resolve four local semantic ambiguities before the proposed item conference."""
from copy import deepcopy
from datetime import datetime,timezone
import hashlib,json
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())
def digest(b):return hashlib.sha256(b).hexdigest()
def render(m):
    out=['# Core brews and substances — individual discussion draft','',
        '**Local, unsubmitted and unadopted.** Twenty item procedure proposals and four explicit source-decision holds. All24 original records remain preserved; no source item or active rule is promoted.','',
        '[Exact model and source evidence](ITEMS_MODEL.json) · [52 authored situations](CASEBOOK.json) · [Shared use proposal](../core-consumable-use-local-draft-01/DISCUSSION.md)','',
        '## Common proposals','']
    for k,v in m['commonProposals'].items():
        if k!='status':out.extend([f'**{k}:** {v}',''])
    for p in m['items']:
        out.extend([f"## {p['id']} — {p['name']}",'','**Source:** '+p['original']['effect']])
        if 'crash' in p['original']:out.append('**Source crash:** '+p['original']['crash'])
        fields={k:v for k,v in p['original'].items() if k not in ['name','effect','crash','description']}
        out.extend(['','**Preserved source fields:** '+json.dumps(fields,ensure_ascii=False),''])
        if p['reviewReadiness']=='specific-source-decision-required':
            out.extend(['**Specific decision required:** '+p['reason'],''])
            for option in p['concreteAlternativesForJointDiscussion']:out.extend(['- '+option,''])
            out.extend(['**Next:** '+p['requiredEvidenceOrDecision'],''])
        else:
            if p['unitOverride']:out.extend(['**Serving:** '+p['unitOverride'],''])
            for k,label in [('benefit','Proposed benefit'),('endingOrCrash','Ending and crash'),('repetitionAndTolerance','Repeat use'),('limitsAndInterfaces','Limits and interfaces'),('overdose','Overdose')]:out.extend([f'**{label}:** '+p[k],''])
    table=m['newWyrmspiceComplicationProposal'];out.extend(['## Proposed Wyrmspice complication table','',table['status'],'','| d6 | Result | Actual consequence |','|---|---|---|'])
    for r in table['rows']:out.append(f"| {r['roll']} | {r['name']} | {r['effect']} |")
    out.extend(['','These are authored proposals and situations, not runtime executions, human playtests or balance approval. Actual GPT must review all original-to-proposal changes and resolve the four held sources before complete-catalog approval.',''])
    return '\n'.join(out)

def main():
    root=A/'core-consumable-items-local-draft-01';history=root/'history/before-refinement-01a'
    receipt=A/'CORE_CONSUMABLE_ITEMS_DRAFT_01A_REFINEMENT.json'
    assert not history.exists() and not receipt.exists()
    m=read(root/'ITEMS_MODEL.json');cb=read(root/'CASEBOOK.json');before=deepcopy(m);oldcb=deepcopy(cb)
    assert cb['count']==48;items={x['id']:x for x in m['items']};changes=[]
    def setfield(i,k,new,reason):
        p=items[i];changes.append({'itemId':i,'field':k,'reason':reason,'before':p[k],'after':new});p[k]=new
    setfield('CB-04','benefit',
        'For eight elapsed hours, gain advantage on actual ability checks to resist or recover from seasickness. NEW bounded waterborne-motion procedure: track cumulative seconds of actual rough motion in one motion episode. First CON ability check DC12 occurs at600rough-motion seconds, then at4200,7800 and each further3600rough-motion seconds. Failure applies/retains local Seasick: disadvantage on STR/DEX ability checks, with no automatic attack/save/damage penalty. Success ends that penalty. Quiet intervals pause accumulation and create no check; a short quiet interval does not backdate or reset an already processed marker. An episode ends after600continuous seconds without rough motion, clearing Seasick and the counter. A later new episode begins at0. Seat/heading/initiative/session changes never create extra checks.',
        'The first draft mixed continuous exposure with retained clocks across short pauses; an explicit cumulative-within-episode clock resolves that contradiction.')
    setfield('CB-04','endingOrCrash',
        'Grog advantage expires atT0+28800; it does not itself cure Seasick. The separate motion episode ends after600uninterrupted seconds without rough motion. Re-entry earlier than that retains its accumulated rough seconds and penalty; steady time is not added to the rough-motion counter. At an exact600second steady completion, end the prior episode before any genuinely new motion begins.',
        'Define pause, recovery and exact boundary independently of the brew timer.')
    setfield('CS-03','endingOrCrash',
        'At this dose’s ten-minute/tolerant or actual early benefit end, remove its unspent temporary HP and chosen CON-penalty exception, then take1d6NEW necrotic crash damage. A benefit lock begins at dose completion and clears only after this dose has ended/crashed AND a genuinely qualifying Long Rest completes at or after that actual crash timestamp. A rest completed earlier cannot prepay the post-crash lock. If crash and rest completion share a timestamp, resolve the actual dose end/damage/life state first, then award only a rest that still qualifies under the normal rules. A corpse receives no rest benefit. Every deliberately consumed locked dose retains its own ending/lock record; all operative Redwake locks must clear before another benefit.',
        'The prior after-dose rest wording could let a rest completed before the crash satisfy a consequence described as following the effect. This is an explicit NEW post-crash choice for GPT review.')
    setfield('CS-10','benefit',
        'For ten elapsed minutes gain fire resistance and add+1 to one existing damage component of each actual melee attack that hits. Choose that component at declaration and retain its type. Apply the point in the attack’s ordinary flat-damage formula before the final nonnegative floor and defenses, once per attack rather than per die/component. A real zero damage formula can become1; a sufficiently negative formula can still floor to0. This supplies no damage component for an attack that has none. Legal melee weapon, unarmed, natural and melee spell attacks qualify; a melee-range save effect, miss, damaging aura or separately triggered secondary packet does not.',
        'The initial positive-base prerequisite unnecessarily narrowed the source bonus and hid the zero/negative damage boundary.')
    setfield('CS-12','repetitionAndTolerance',items['CS-12']['repetitionAndTolerance']+
        ' If overlapping unspent doses chose different elements, declare one currently unexpired dose record as the source of the breath before choosing cone orientation or rolling. Its already selected type controls that breath; no new type is chosen. Spending the one breath marks every overlapping unspent same-item entitlement consumed, and each such dose resolves its own once-only recoil in actual dose-application order, using that dose’s own selected type. An earlier individually expired dose is not consumed or recoiled again. Expiry of one unused dose ends/recoils that dose alone; it grants no new use and does not erase a still-live independent record.',
        'Different stored elemental choices require an explicit source selection and per-dose recoil order; same-item entitlement policy must not create extra breaths or recolor earlier recoil.')
    newcases=[
        {'id':'CB-04-I01-C3','itemId':'CB-04','title':'Pause preserves only rough seconds','given':'An episode has540rough seconds. Then540steady seconds, then60rough seconds. Grog active.','expected':'No check during steady time. Totalrough reaches600 atelapsed1140, producing the one firstcheck. Ten full steady minutes would instead reset the episode. Next marker remains4200roughseconds, not4200wallseconds.','kind':'proposed-item-adjudication','runtimeExecuted':False},
        {'id':'CS-03-I01-C3','itemId':'CS-03','title':'No prepaid post-crash rest','given':'DoseT0; actual qualifying Long Rest completesT0+300; dosebenefit ends/crashesT0+600.','expected':'The earlier rest cannot clear this dose’s post-crash lock. Actual crash at600 applies; a later genuinely qualifying Long Rest is required. A coincident rest at600 would be evaluated only after actual crash/life state and its ordinary eligibility.','kind':'proposed-item-adjudication','runtimeExecuted':False},
        {'id':'CS-10-I01-C3','itemId':'CS-10','title':'Zero and negative attack formulas','given':'Legal melee hit with one actual damage component; its ordinary flat formula is0 in one history and−2 in another, before the nonnegative floor.','expected':'EmberResin+1 yields1 in the first history andmax(0,−2+1)=0 in the second. A grapple/attack with no damage component gains none. No positive-base prerequisite is invented.','kind':'proposed-item-adjudication','runtimeExecuted':False},
        {'id':'CS-12-I01-C3','itemId':'CS-12','title':'Two stored elements, one actual breath','given':'Unexpired fire doseA then cold doseB; both unspent. User declaresA asbreathsource beforeorientation.','expected':'One3d6fire cone, no cold cone. Mark both entitlements consumed; resolveA1d6fire recoil thenB1d6cold recoil in actualapplication order, eachwithitsdefenses/life. No latersecondbreath orduplicateexpiryrecoil.','kind':'proposed-item-adjudication','runtimeExecuted':False}
    ]
    cb['cases'].extend(newcases);cb.update(count=52,proposedItemAdjudications=44)
    checks=[
        {'name':'48prior case IDs preserved plus four distinct new cases','pass':set(x['id'] for x in oldcb['cases'])<=set(x['id'] for x in cb['cases']) and len({x['id'] for x in cb['cases']})==52},
        {'name':'every original source object unchanged','pass':all(x['original']==next(y['original'] for y in before['items'] if y['id']==x['id']) for x in m['items'])},
        {'name':'rough-only clock example','pass':540+60==600 and 540+540+60==1140 and 540<600},
        {'name':'zero and negative flat-damage boundaries','pass':max(0,0+1)==1 and max(0,-2+1)==0},
        {'name':'all source binding bytes remain exact','pass':all(info(G/x['path'])==x for x in m['sourceBindings'])},
        {'name':'four held items unchanged','pass':[x for x in m['items'] if x['reviewReadiness']=='specific-source-decision-required']==[x for x in before['items'] if x['reviewReadiness']=='specific-source-decision-required']},
        {'name':'no actual approval or promotion','pass':not any(x['approved'] or x['activeOperational'] for x in m['items'])}
    ];assert all(x['pass'] for x in checks)
    history.mkdir(parents=True)
    for n in ['ITEMS_MODEL.json','CASEBOOK.json','DIRECTOR_DISCUSSION.md','LOCAL_CHECKS.json','MANIFEST.json']:(history/n).write_bytes((root/n).read_bytes())
    m['reviewGates']=[x.replace('all48 authored dispositions','all52 authored dispositions') for x in m['reviewGates']]
    (root/'ITEMS_MODEL.json').write_bytes(encoded(m));(root/'CASEBOOK.json').write_bytes(encoded(cb));(root/'DIRECTOR_DISCUSSION.md').write_text(render(m),encoding='utf-8',newline='\n')
    oldcheck=read(history/'LOCAL_CHECKS.json')
    (root/'LOCAL_CHECKS.json').write_bytes(encoded({'initialChecksPreserved':info(history/'LOCAL_CHECKS.json'),'initialCheckCount':oldcheck['count'],'refinementChecks':checks,'refinementCheckCount':len(checks),'failures':0,'scope':'Source preservation and selected clock/damage boundaries; counts overlap and are not execution of all52 situations.'}))
    entries=[{'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())} for p in sorted(root.rglob('*')) if p.is_file() and p!=root/'MANIFEST.json']
    (root/'MANIFEST.json').write_bytes(encoded({'files':entries}))
    receipt.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'Local unadopted refinement; four source holds remain.','previousModel':info(history/'ITEMS_MODEL.json'),'previousCases':info(history/'CASEBOOK.json'),'model':info(root/'ITEMS_MODEL.json'),'casebook':info(root/'CASEBOOK.json'),'discussion':info(root/'DIRECTOR_DISCUSSION.md'),'changes':changes,'newCases':newcases,'authoredSituations':52,'checks':checks,'checkCount':len(checks),'failureCount':0,'newRulesAdopted':False,'sourceInformationDeleted':0,'runtimeSituationsExecuted':0}))
    print(json.dumps({'refinement':info(receipt),'model':info(root/'ITEMS_MODEL.json'),'casebook':info(root/'CASEBOOK.json'),'situations':52,'checks':len(checks),'failures':0}))

if __name__=='__main__':main()
