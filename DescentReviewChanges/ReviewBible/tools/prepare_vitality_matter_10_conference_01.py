"""Freeze source decisions for ten native rank-seven spells; adopt no rules."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json, zipfile
from apply_di7_ap_as_01 import G, R, A, info, encoded
from prepare_ac5_current_interfaces_01 import at
from vitality_matter_10_questions_01 import IDS, TIERS, Q

def read(p): return json.loads(p.read_bytes())

def main():
    root=A/'vitality-matter10-source-conference-01'
    out=R/'data/director/spell_review/vitality_matter_10_source_conference_01.json'
    check=A/'VITALITY_MATTER_10_SOURCE_CONFERENCE_01_CHECK.json'
    prep=A/'VITALITY_MATTER_10_SOURCE_CONFERENCE_01_PREPARATION.json'
    request=A/'VITALITY_MATTER_10_SOURCE_CONFERENCE_01_REQUEST.txt'
    archive=A/'DD_Vitality_Matter_10_Source_Conference_01.zip'
    assert not any(p.exists() for p in [root,out,check,prep,request,archive])
    sources={};checks=[]
    def ck(n,v):
        checks.append({'check':n,'passed':bool(v)});assert v,n
    def bind(p):
        b=info(p);sources[b['path']]=b;return b
    cp=R/'data/public/spell_playtests/catalog.json';ip=cp.parent/'authored_review_index.json'
    qp=R/'data/director/spell_review/remaining_work_queue_12.json'
    rp=R/'data/director/spell_review/accepted_interface_registry_06.json'
    dp=A/'ENVIRONMENT_DISEASE_INTERFACE_AUDIT_01.json'
    pushp=G/'docs/audit/2026-10-18/github-snapshot-persistent20/PUSH_RECEIPT.json'
    catalog,index,queue,registry,disease,push=map(read,[cp,ip,qp,rp,dp,pushp])
    ck('Current525 reviewed323 pending',index['authoredCounts']=={'reviewed':525,'pending':323})
    ck('173 exact scoped interfaces',len(registry['entries'])==173)
    ck('Latest preservation push verified',push['commit']==push['remoteMain']=='032bc7e33d941d7e635efa8b9a8b060f9f1742f8' and push['trackedEntriesDeleted']==0)
    for p in [cp,ip,qp,rp,dp,pushp,Path(__file__),Path(__file__).with_name('vitality_matter_10_questions_01.py'),R/'rulebook_output.txt']:bind(p)
    originals={i:('ILLUSION_NECROMANCY_RANK7_SOURCE_PREPARATION.json' if n<5 else 'TRANSMUTATION_UNIVERSAL_RANK7_SOURCE_PREPARATION.json') for n,i in enumerate(IDS)}
    lines=(R/'rulebook_output.txt').read_text('utf-16').splitlines();records=[]
    for ident in IDS:
        oldp=A/originals[ident];old=read(oldp);bind(oldp)
        n=next(n for n,s in enumerate(old['selectedSpells']) if s['spellId']==ident);s=old['selectedSpells'][n]
        card=next(s for s in catalog['spells'] if s['id']==ident);row=next(s for s in queue['rows'] if s['id']==ident);entry=next(e for e in index['entries'] if e['id']==ident)
        ck('Complete current source equality '+ident,s['fullSourceAndCurrentAccessRecord']==card==row['completeCurrentSourceAndAccess'])
        ck('No earlier operational procedure '+ident,row['currentGroup'] is None and not row['previousAuthoringMapRowUnchanged']['completeEarlierProposalRecords'])
        ck('Pending identity '+ident,entry['authoredStatus']=='pending-authored-procedure')
        ck('Actual rank7 price/access '+ident,all(v['rank']==7 and v['baseRpCost']==17 for v in card['classAccess'].values()))
        bb=[deepcopy(b) for b in old['currentBookBindings'] if b['spellId']==ident]
        ck('Every original school placement '+ident,len(bb)==len(card['source']['original']['placements']))
        for b in bb:ck('Exact current book line '+ident,lines[b['currentBookRow']['line']-1]==b['currentBookRow']['exactText'])
        for key in ['catalog','core']:ck('Full underlying source '+ident+key,bind(R/card['source'][key+'Path'])['sha256']==card['source'][key+'Sha256'])
        for class_name in card['classAccess']:
            bind(R/('data/public/Decennium_Descent_Bard_Playtest_v0_1.json' if class_name=='Bard' else 'data/public/class_playtests/'+class_name.lower().replace(' ','-')+'.json'))
        records.append({'spellId':ident,'riskTier':TIERS[ident][0],'riskReason':TIERS[ident][1],'completeCurrentCatalogSourceAndAccess':deepcopy(card),'currentIndexEntry':deepcopy(entry),'originalQuestionSource':info(oldp),'originalQuestionPointer':f'/selectedSpells/{n}','completeOriginalSourceQuestionUnchanged':deepcopy(s),'completeHistoricalCommonQuestionUnchanged':old['commonOperationalQuestion'],'completeHistoricalScopeExceptionUnchanged':old['commonQuestionException'],'completeCurrentBookBindings':bb,'earlierCompleteProcedures':[],'earlierOperationalWorkedCases':[],'status':'Source conference prepared UNSENT; no operational procedure or case adoption.'})
    # The disease audit is useful source evidence, not a generic adopted disease engine.
    disease_comparison=[]
    for previous in disease['sourceBindings']:
        current=bind(G/previous['path'])
        disease_comparison.append({'historicalAuditBinding':deepcopy(previous),'currentBinding':current,'byteIdentical':all(previous[k]==current[k] for k in ['bytes','sha256']),'authority':'Historical source-only audit preserved. Current exact sources control; changed bytes are explicitly shown, never relabeled as the old snapshot.'})
    ck('Disease audit still source-only',disease['newRulesAdopted']==0 and disease['submitted'] is False)
    for p in [R/'data/public/Decennium_Descent_Bard_Playtest_v0_1.json',R/'data/playtest/equipment_acquisition_candidate.json',R/'data/playtest/spell_form_profiles.json',R/'data/director/spell_proposals/companion_life_10_current_04.json',A/'COMPANION_LIFE_10_CURRENT_04_ACTUAL_SUBMISSION.json',A/'PERSISTENT_DAMAGE_20_EXACT07_APPLICATION_RECEIPT.json',A/'DAMAGE_CONTROL_25_EXACT10_APPLICATION_RECEIPT.json']:
        bind(p)
    for name in ['VIDEO_GAME_ONLY_DIRECTIVE.md','CLASS_PLAYTEST_RULES.md','SPELL_INTEGRATION_RULES.md','COMBAT_ACTION_PLAYTEST.md','CORE_RESOLUTION_PLAYTEST.md','CONDITIONS_PLAYTEST.md','CONTROL_STATES_PLAYTEST.md','BODY_EQUIPMENT_PLAYTEST.md','CREATURE_LIFECYCLE_PLAYTEST.md','DEVICE_LIFECYCLE_PLAYTEST.md','HEALING_DEATH_PLAYTEST.md','CHARACTER_CREATION_PLAYTEST.md','MAXIMUM_HP_PLAYTEST.md','DAMAGE_SHARING_PLAYTEST.md','TRANSFORMATION_SPELL_PLAYTEST.md','CRAFTING_HARVEST_PLAYTEST.md']:
        bind(R/'docs/mechanics'/name)
    inherited=[]
    ns=list(range(0,15))+[22,31,36,39,40,50,51,61]+list(range(108,117))+list(range(143,152))
    for n in ns:
        e=registry['entries'][n];b=e['currentAuthoritativeSource'];actual=bind(G/b['path'])
        ck('Current accepted interface source '+str(n),all(actual[k]==b[k] for k in ['bytes','sha256']))
        inherited.append({'registryPointer':f'/entries/{n}','completeEntryUnchanged':deepcopy(e),'scopeLimit':'Exact named scope only; new source-specific exceptions require an explicit decision. No companion draft, class profile or damage-funding policy transfers automatically.'})
    counterparts=[]
    for ident in ['animate-dead','enlarge-reduce','polymorph','true-polymorph','vampiric-touch','leeching-plague','enervation','blight','frozen-tomb','dimensional-anchor','antimagic-field-lesser','greater-dispel','purify-food-and-drink','detect-poison']:
        e=next(e for e in index['entries'] if e['id']==ident);ck('Actually reviewed counterpart '+ident,e['authoredStatus']=='reviewed-authored-operational-playtest')
        path=(ip.parent/e['procedureFile']).resolve();doc=read(path);ptr=e.get('wholeCardPointer',e['procedurePointer'])
        counterparts.append({'spellId':ident,'source':bind(path),'pointer':ptr,'completeCurrentCard':deepcopy(at(doc,ptr)),'completeSharedRules':deepcopy(doc.get('sharedRules',{})),'indexEntry':deepcopy(e)})
    questions=[{'id':i,'spellIds':ids,'exactSourceOrConflict':src,'options':opts,'recommendationAndConsequences':rec,'decisionSelected':False} for i,ids,src,opts,rec in Q]
    ck('25 distinct unselected questions',len(questions)==len({q['id'] for q in questions})==25)
    ck('Every identity has exact questions',set().union(*(set(q['spellIds']) for q in questions))==set(IDS))
    risk=dict(Counter(r['riskTier'] for r in records));ck('Per-spell assessment fiveB fiveC',risk=={'C':5,'B':5})
    ck('Ten original identities and placements',len(records)==10 and sum(len(r['completeCurrentBookBindings']) for r in records)==10)
    candidate={'id':'VITALITY-MATTER-10-SOURCE-CONFERENCE-01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'SOURCE_CONFERENCE_PREPARED_UNSENT','developmentDirection':'video-game-only','records':records,'currentAcceptedInterfaceComparisons':inherited,'completeAcceptedCounterparts':counterparts,'questions':questions,'riskCounts':risk,'semanticDelta':[{'spellId':r['spellId'],'riskTier':r['riskTier'],'riskReason':r['riskReason'],'startingPoint':'Full original source and preserved earlier questions; no earlier operational procedures/cases exist for this identity.','genuineQuestionIds':[q['id'] for q in questions if r['spellId'] in q['spellIds']]} for r in records],'diseaseEvidence':{'historicalAudit':info(dp),'completeFindingsUnchanged':deepcopy(disease['findings']),'currentSourceComparisons':disease_comparison,'qualification':'The audit is source-only UNSENT, and establishes no generic disease engine. Its historical counts/statuses are not current authority. Current source bindings and actual exact accepted rules control.'},'companionDependency':{'current04':info(R/'data/director/spell_proposals/companion_life_10_current_04.json'),'actualSubmission':info(A/'COMPANION_LIFE_10_CURRENT_04_ACTUAL_SUBMISSION.json'),'qualification':'Actual GPT semantic review active when this packet was frozen. Full04 is included for proposed comparison only. No acceptance, profile entitlement, CR rating or healing extension is inferred.'},'earlierOperationalWorkedCases':[],'currentVectors':[],'futureCaseRequirements':['Preserve original source questions and all explicit decisions. Author at least two full current cases per spell plus every genuinely different profile/branch after the conference decisions.','Actual eligible caster/class/level/repertoire/costs/components/real regular-turn and companion markers; complete bodies, gear, occupied volumes, allegiance and recipient life states.','Colossus two-hit versus cleave, actual maximumHP/controller provenance, birth-round command and suppression; Finger actual death replacement and one-corpse competing claim.','Black Reaping complete multi-recipient damage, transferred/protected branches and one exact aggregate heal with actual healing modifiers.','Plague Wind separate damage/disease immunity, exact finite future events, actual cure and suspended/expired disease with no replay.','Metal to Glass successful drop-save still converts; real held/worn/composite object properties, damage and surviving constituent histories.','Titanic growth fit/strength precedence/attack cadence; Flash Freeze damage/restraint separation and any adopted shell/escape.','All three Transmute Being profiles and real one-body gear/life transitions; Regenerate independent heal/limb outcomes with actual original/removed-part lineage.','Conditional fixtures must identify missing actual upstream profile/branch; synthetic numerical inputs are not complete actual-class casts. No runtime, balance or human playtest claim.'],'countsUnchanged':deepcopy(index['authoredCounts']),'sourceBindings':list(sources.values()),'newRuleAdoptions':0,'runtimeTestsExecuted':0,'humanPlaytests':0,'sourceInformationDeleted':0,'cosmologyDecisions':0}
    root.mkdir();frozen=[]
    for b in sources.values():
        p=G/b['path'];ck('Source unchanged '+b['path'],info(p)==b);dst=root/'sources'/b['path'];dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(p.read_bytes())
        ck('Frozen source exact '+b['path'],dst.read_bytes()==p.read_bytes());frozen.append({**b,'frozenCopy':dst.relative_to(G).as_posix()})
    out.write_bytes(encoded(candidate))
    check.write_bytes(encoded({'candidate':info(out),'checks':checks,'checkCount':len(checks),'sourceCount':len(sources),'sourceIdentities':10,'placements':10,'earlierCompleteProcedures':0,'earlierOperationalWorkedCases':0,'newCurrentVectors':0,'questions':25,'riskCounts':risk,'failures':0,'validationScope':'Exact source, authority/access comparison and preservation only; no semantic approval or gameplay execution.'}))
    (root/'MANIFEST.json').write_bytes(encoded({'candidate':info(out),'check':info(check),'files':list(sources.values()),'frozenSources':frozen,'sourceCount':len(sources),'newRuleAdoptions':0}))
    (root/'README.md').write_text('# Ten rank-seven vitality and matter spells\n\nRead ten complete original source records, all ten placements,25 explicit unselected questions,14 full accepted counterparts and exact inherited interfaces. Five individually justified tierB and five tierC records. No earlier complete operational procedures/cases exist; none are invented by this packet. The full current Companion04 is proposed comparison evidence under actual GPT review, not adopted authority. The historical disease audit is also source-only; its changed live-source bindings are listed explicitly.\n\nReturn complete source-linked proposed procedures, every question disposition and genuine remaining-content holds. Preserve printed benefits and actual class access; label all new profiles, timing, limits and conflict decisions. Develop full actual cases only after choices are settled.525reviewed/323pending stay unchanged. No source deletion, runtime/human/balance/cosmology or75-domain closure.\n',encoding='utf8',newline='\n')
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in ['README.md','MANIFEST.json']:z.write(root/name,name)
        z.write(out,'CANDIDATE.json');z.write(check,'PREFLIGHT.json')
        for b in frozen:z.write(G/b['frozenCopy'],'sources/'+b['path'])
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and z.read('CANDIDATE.json')==out.read_bytes()
        for b in frozen:assert z.read('sources/'+b['path'])==(G/b['frozenCopy']).read_bytes()
    b=info(archive)
    request.write_text(f'Please conduct the ten-spell rank7 vitality/matter source conference using {archive.name}, {b["bytes"]}bytes SHA256{b["sha256"]}. Read all ten full sources,25 explicit questions,14 accepted counterpart cards and scoped interfaces. Five tierB/five tierC per actual risk. Return complete proposed procedures, exact question dispositions and remaining true content holds. Companion04 and the disease audit are qualified pending comparison evidence, not accepted new authority. Preserve all printed benefits, actual classes, source/gear/body histories; no external monster stats or generic disease engine.525/323membership stays unchanged.\n',encoding='utf8',newline='\n')
    prep.write_bytes(encoded({'archive':b,'candidate':info(out),'manifest':info(root/'MANIFEST.json'),'check':info(check),'request':info(request),'sourceCount':len(sources),'allArchiveSourcesVerified':True,'riskCounts':risk,'status':'Prepared UNSENT; no actual GPT decision on this packet yet.','newRuleAdoptions':0}))
    print(json.dumps({'archive':b,'candidate':info(out),'sources':len(sources),'checks':len(checks),'questions':25,'riskCounts':risk,'operationalCases':0}))

if __name__=='__main__':main()
