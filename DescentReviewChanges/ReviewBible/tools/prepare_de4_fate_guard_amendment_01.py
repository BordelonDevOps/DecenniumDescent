"""Prepare, but do not apply, the explicit three-spell reroll-guard amendment."""
from copy import deepcopy
from datetime import datetime,timezone
import json
from apply_di7_ap_as_01 import G,R,A,info,encoded
from prepare_ac5_current_interfaces_01 import at

def read(p):return json.loads(p.read_bytes())

def parent(d,p):
    bits=p.split('/')[1:];v=d
    for raw in bits[:-1]:
        key=raw.replace('~1','/').replace('~0','~');v=v[int(key)] if isinstance(v,list) else v[key]
    key=bits[-1].replace('~1','/').replace('~0','~');return v,int(key) if isinstance(v,list) else key

def main():
    out=A/'DE4_FATE_GUARD_AMENDMENT_DRAFT_01.json';checkfile=A/'DE4_FATE_GUARD_AMENDMENT_CHECK_01.json'
    assert not out.exists() and not checkfile.exists()
    catalogp=R/'data/public/spell_playtests/catalog.json';catalog=read(catalogp)
    mark=catalog['spells'][220];coin=catalog['spells'][222];assert mark['id']=='mark-omen' and coin['id']=='fate-coin'
    opening='Mark Omen and Fate Coin share one guard:';end='No new Action, roll event, cast, payment or duplicated outcome hook is created by replacing dice.'
    lim=mark['operational']['limitations'];before=lim[lim.index(opening):lim.index(end)+len(end)]
    assert before in coin['operational']['limitations']
    after=before.replace('Mark Omen and Fate Coin share one guard:','NEW scoped DE4-GUARD-01 amendment: Mark Omen, Fate Coin and Fate Reversal share one guard:',1).replace('either of these two spells','any of these three spells').replace('across all casters, coins, marks and recasts','across all casters, coins, marks, Fate Reversal permissions and recasts').replace('for these two spells','for these three spells').replace('Only the first legal commitment spends a mark/coin;','Only the first legal commitment spends its own actual mark, coin or Fate Reversal permission and any Reaction required by that source;')
    after+=' This extension changes only the common lineage guard. Mark Omen still replaces the caster\'s own marked-target attack d20 procedure with no additional Action or Reaction; Fate Coin still changes exactly one eligible physical die through its holder\'s actual Reaction and30-foot perceived-event interface; Fate Reversal still requires its own Reaction, pending permission, eligible complete attack/save/check d20 procedure and60-foot perceived-event interface. No class feature is added to this family merely because it changes a roll, and this amendment grants no new access to hidden dice or any source\'s otherwise ineligible roll.'
    checks=[]
    def ck(label,ok):checks.append({'name':label,'passed':bool(ok)});assert ok,label
    ck('Distinct proposed guard text',before!=after and 'two spells' not in after)
    json_paths=['data/public/spell_playtests/catalog.json','data/public/feat_candidates/exact_01/spell_dependencies.json','data/playtest/spell_drafts/candidate_divination_rank1.json','data/playtest/spell_drafts/batch_divination_rank1.json']
    prose_paths=['docs/mechanics/SPELL_PLAYTEST_STARTER.md','docs/mechanics/SPELL_INTEGRATION_RULES.md','docs/feats/exact-candidate-01/SPELL_PAYLOADS.md']
    planned=[];historical=[];bindings=[]
    for rel in json_paths:
        p=R/rel;doc=read(p);copy=deepcopy(doc);edits=[]
        def walk(v,path=''):
            if isinstance(v,dict):
                for k,x in v.items():walk(x,path+'/'+k.replace('~','~0').replace('/','~1'))
            elif isinstance(v,list):
                for i,x in enumerate(v):walk(x,path+'/'+str(i))
            elif isinstance(v,str) and opening in v:
                if '/originalCatalogRecord/' in path:
                    historical.append({'path':p.relative_to(G).as_posix(),'pointer':path,'retainedOriginal':v});return
                ck('One complete guard at '+rel+path,v.count(before)==1)
                replacement=v.replace(before,after,1);pv,key=parent(copy,path);pv[key]=replacement
                edits.append({'pointer':path,'before':v,'after':replacement})
        walk(doc)
        reverse=deepcopy(copy)
        for op in reversed(edits):pv,key=parent(reverse,op['pointer']);ck('Expected replacement at '+rel+op['pointer'],pv[key]==op['after']);pv[key]=op['before']
        ck('Exact reversible JSON values '+rel,reverse==doc)
        ck('Expected two active records '+rel,len(edits)==2)
        if rel.endswith('spell_dependencies.json'):
            for ident in ['fate-coin','mark-omen']:ck('Preserve immutable original dependency '+ident,copy['spells'][ident]['originalCatalogRecord']==doc['spells'][ident]['originalCatalogRecord'])
        planned.append({'source':info(p),'kind':'proposed-json-field-replacements','operations':edits});bindings.append(info(p))
    for rel in prose_paths:
        p=R/rel;text=p.read_text(encoding='utf8');count=text.count(before)
        ck('Complete literal guard in '+rel,count>0)
        new=text.replace(before,after)
        ck('Exact reversible prose '+rel,new.replace(after,before)==text)
        planned.append({'source':info(p),'kind':'proposed-exact-prose-replacement','before':before,'after':after,'expectedOccurrences':count});bindings.append(info(p))
    ck('Only two frozen original dependency records excluded',len(historical)==2)
    # The actual apply step must recompute all current catalog/index dependency bindings, not only these words.
    indexp=R/'data/public/spell_playtests/authored_review_index.json';dep=read(R/'data/public/feat_candidates/exact_01/spell_dependencies.json')
    catalog_bound=[{'id':ident,'binding':row['binding']} for ident,row in dep['spells'].items() if row['binding']['file']==catalogp.relative_to(G).as_posix()]
    for row in catalog_bound:ck('Current feat dependency binding '+row['id'],all(row['binding'][k]==info(catalogp)[k] for k in ['bytes','sha256']))
    result={'id':'DE4-FATE-GUARD-AMENDMENT-DRAFT-01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'UNSENT and UNADOPTED. Concrete reviewable proposed amendment only; no current rules/files modified.','scope':'Explicitly extend only the current Mark Omen/Fate Coin common original-roll-lineage guard to Fate Reversal, subject to actual joint DE4 acceptance.','existingGuardVerbatim':before,'proposedGuardVerbatim':after,'plannedActiveRepresentationChanges':planned,'immutableHistoricalRecordsRetained':historical,'sourceBindings':bindings,'additionalApplicationRequirements':['Obtain actual GPT acceptance of exact complete DE4 procedures, shared amendment and worked cases before applying any change.','Preserve exact before bytes for all current mutation targets. Apply only active representations; retained historical originalCatalogRecord and sealed review returns stay exact.','Refresh current catalog whole-file hash in the authored index and all actual completeCurrentProcedureCard dependency bindings; recompute derived candidate metadata using existing accepted procedures. No blanket rewrite of historical source hashes.', 'Append the explicit extension to Mark Omen and Fate Coin design notes/current interpretation while retaining original pre-extension evidence; do not quietly imply the original two-spell acceptance already covered Fate Reversal.', 'Reconcile current AC5/AC6 references through preserved frozen-source aliases or explicit accepted extension, without altering their sealed historical acceptance artifacts.','Preserve actual per-source payment, one-die versus full-d20-set replacement, physical-die restrictions, perception/LoE, range, reaction availability, no hidden-information permission, natural-result and shared-roll outcomes.'], 'currentAuthoredIndex':info(indexp),'currentCatalogBoundFeatDependencies':catalog_bound,'requiredFocusedExamples':['Mark Omen reserves the lineage for an advantage attack; later legal-looking Fate Reversal is barred with no permission/Reaction spend.','Fate Reversal reserves an eligible complete save/check d20 lineage; later Coin cannot reroll one of its replacement dice.','Coin replaces one physical die in a shared damage pool; the same changed total applies to every recipient; Fate Reversal cannot target damage at all.','A genuinely separate later damage event remains distinct from its attack event; the guard does not merge separate actual rolls.','An exact class reroll keeps its source timing/permission but never erases a previously spent three-spell guard; no free repeated lineage is created.','Unavailable Reaction or prohibited/perception-blocked candidate cannot reserve the guard before preflight; first actual legal declaration wins under existing initiative/neutral order.'],'newSpellAdoptions':0,'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'currentFilesModified':0}
    out.write_bytes(encoded(result));checkfile.write_bytes(encoded({'id':'DE4-FATE-GUARD-AMENDMENT-CHECK-01','draft':info(out),'checks':checks,'checkCount':len(checks),'failureCount':0,'activeFiles':len(planned),'activeJsonFieldReplacements':sum(len(x.get('operations',[])) for x in planned),'proseGuardOccurrences':sum(x.get('expectedOccurrences',0) for x in planned),'historicalRecordsPreserved':len(historical),'dependentCatalogBindings':len(catalog_bound),'status':'Reversible proposal and current-binding checks only. No source modification or joint acceptance.'}))
    print(json.dumps({'draft':info(out),'check':info(checkfile),'checks':len(checks),'activeFiles':len(planned),'currentFilesModified':0}))

if __name__=='__main__':main()
