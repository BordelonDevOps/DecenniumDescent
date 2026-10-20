"""Freeze complete impact/exile sources and explicit unselected review questions."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json, zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded
from prepare_ac5_current_interfaces_01 import at
from rank9_impact_exile_4_questions_01 import IDS,TIERS,Q,FINDINGS,CASES

def read(p):return json.loads(p.read_bytes())

def frozen_io(p):return Path('\\\\?\\'+str(p.resolve()))

def main():
    stem='RANK9_IMPACT_EXILE_4_SOURCE_CONFERENCE_01'
    root=A/'rank9-impact-exile4-source-conference-01'
    out=R/'data/director/spell_review/rank9_impact_exile_4_source_conference_01.json'
    check,prep,request=[A/(stem+s) for s in ['_CHECK.json','_PREPARATION.json','_REQUEST.txt']]
    archive=A/'DD_Rank9_Impact_Exile_4_Source_Conference_01.zip'
    assert not any(p.exists() for p in [root,out,check,prep,request,archive])
    sources={};checks=[]
    def ck(label,ok):
        checks.append({'check':label,'passed':bool(ok)});assert ok,label
    def bind(p):
        b=info(p);sources[b['path']]=b;return b
    catp=R/'data/public/spell_playtests/catalog.json';ip=catp.parent/'authored_review_index.json'
    qp=R/'data/director/spell_review/remaining_work_queue_51.json'
    regp=R/'data/director/spell_review/accepted_interface_registry_06.json'
    cov=R/'data/playtest/game_development_coverage.json'
    protected={p:p.read_bytes() for p in [catp,ip,qp,regp,cov]}
    catalog,index,queue,registry=map(read,[catp,ip,qp,regp])
    olds=[A/(name+'_RANK9_SOURCE_PREPARATION.json') for name in ['TRANSMUTATION_UNIVERSAL']]
    histories=[read(p) for p in olds]
    ck('Actual membership unchanged',index['authoredCounts']=={'reviewed':525,'pending':323} and index['representationCounts']['completeReviewedStandaloneProcedures']==249)
    ck('173 scoped interfaces',len(registry['entries'])==173)
    for p in [catp,ip,qp,regp,cov,*olds,Path(__file__),Path(__file__).with_name('rank9_impact_exile_4_questions_01.py'),
              A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_SUMMON_HOSTS_63.json',
              A/'PERTINENT_GPT_DECISIONS_2026_10_20_02.json',
              A/'GPT_PART5_PERTINENT_OWNER_CHOICES_2026_10_20_NATIVE.json',
              A/'GPT_UNITY_DEVELOPMENT_SETUP_2026_10_20_NATIVE.json',
              G/'docs/audit/2026-10-20/github-snapshot-planar-gates61/PUSH_RECEIPT.json',
              G/'docs/mechanics/LEVEL_97_OLD_GOD_Q6_OPEN.md',
              R/'rulebook_output.txt',G/'docs/reference/Player_Rulebook_v6_source_text.txt',
              R/'books/player/Decennium_Descent_Player_Rulebook_v6.docx']:
        bind(p)
    lines=(R/'rulebook_output.txt').read_text('utf-16').splitlines()
    reference=(G/'docs/reference/Player_Rulebook_v6_source_text.txt').read_text('utf8').splitlines()
    records=[]
    for ident in IDS:
        j=next(j for j,h in enumerate(histories) if any(s['spellId']==ident for s in h['selectedSpells']))
        prior=histories[j];n=next(n for n,s in enumerate(prior['selectedSpells']) if s['spellId']==ident)
        historical=prior['selectedSpells'][n]
        card=next(s for s in catalog['spells'] if s['id']==ident)
        row=next(s for s in queue['rows'] if s['id']==ident)
        entry=next(e for e in index['entries'] if e['id']==ident)
        ck('Full current/historical/queue card '+ident,historical['fullSourceAndCurrentAccessRecord']==card==row['completeCurrentSourceAndAccess'])
        ck('Previously ungrouped without complete procedure '+ident,row['currentGroup'] is None and not row['previousAuthoringMapRowUnchanged']['completeEarlierProposalRecords'])
        ck('Pending authored procedure '+ident,entry['authoredStatus']=='pending-authored-procedure')
        ck('Exact rank9 actual class access '+ident,all(a['rank']==9 and a['minimumClassLevel']==17 and a['baseRpCost']==26 for a in card['classAccess'].values()))
        books=[deepcopy(b) for b in prior['currentBookBindings'] if b['spellId']==ident]
        ck('Every full native placement '+ident,len(books)==len(card['source']['original']['placements']))
        for b in books:
            line=b['currentBookRow']['line']-1
            ck('Both full manuscript extractions exact '+ident+':'+str(line),lines[line]==b['currentBookRow']['exactText']==reference[line])
        for key in ['catalog','core']:
            ck('Underlying full source bound '+ident+':'+key,bind(R/card['source'][key+'Path'])['sha256']==card['source'][key+'Sha256'])
        for cls in card['classAccess']:bind(R/('data/public/class_playtests/'+cls.lower()+'.json'))
        records.append({'spellId':ident,'riskTier':TIERS[ident][0],'riskReason':TIERS[ident][1],
            'completeCurrentCatalogSourceAndAccess':deepcopy(card),'currentIndexEntry':deepcopy(entry),
            'originalQuestionSource':info(olds[j]),'originalQuestionPointer':'/selectedSpells/'+str(n),
            'completeOriginalSourceQuestionUnchanged':deepcopy(historical),
            'completeHistoricalCommonQuestionUnchanged':prior['commonOperationalQuestion'],
            'completeHistoricalScopeExceptionUnchanged':prior['commonQuestionException'],
            'completeCurrentBookBindings':books,'earlierCompleteProcedures':[],'earlierOperationalWorkedCases':[],
            'status':'Prepared full source conference; no selected procedure or current vectors.'})
    expected_access={
        'eternal-anvil':{c:'Transmutation' for c in ['Druid','Mage','Wizard']},
        'reverse-gravity-field':{c:'Transmutation' for c in ['Druid','Mage','Wizard']},
        'transmute-flesh-to-energy':{c:'Transmutation' for c in ['Druid','Mage','Wizard']},
        'planar-collapse':{c:'Universal' for c in ['Cleric','Mage','Wizard']}}
    for record in records:
        sid=record['spellId'];card=record['completeCurrentCatalogSourceAndAccess']
        ck('Exact actual class and school routes '+sid,card['classAccess']=={c:{'rank':9,'minimumClassLevel':17,'school':school,'baseRpCost':26} for c,school in expected_access[sid].items()})
        ck('Exact cast/range/duration '+sid,all(e['original']['casting_time']=='1 action' and e['original']['range']==('60 feet' if sid=='reverse-gravity-field' else '120 feet') and e['original']['duration']==('1 round' if sid=='eternal-anvil' else 'Instantaneous') for e in card['source']['coreEntries']))
    for name in ['VIDEO_GAME_ONLY_DIRECTIVE.md','CLASS_PLAYTEST_RULES.md','SPELL_INTEGRATION_RULES.md',
                 'COMBAT_ACTION_PLAYTEST.md','CORE_RESOLUTION_PLAYTEST.md','CONDITIONS_PLAYTEST.md',
                 'CONTROL_STATES_PLAYTEST.md','BODY_EQUIPMENT_PLAYTEST.md','CREATURE_LIFECYCLE_PLAYTEST.md','HEALING_DEATH_PLAYTEST.md',
                 'DAMAGE_SHARING_PLAYTEST.md','TRANSFORMATION_SPELL_PLAYTEST.md','FORM_TEMP_HP_PLAYTEST.md',
                 'MAXIMUM_HP_PLAYTEST.md','RESONANCE_CANON.md','COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md',
                 'ENCHANTMENT_CONTROL_INTEGRATION_PLAYTEST.md','ENCHANTMENT_RANK3_INTEGRATION_PLAYTEST.md',
                 'REPUTATION.md','CUSTOM_CONDITION_BINDINGS.md','CONTROL_SOURCE_BINDINGS.md',
                 'CHARACTER_CREATION_PLAYTEST.md','CHARACTER_FOUNDATION_TABLES.md','CHARACTER_FOUNDATION_REVIEW_STATUS.json',
                 'XP_ADVANCEMENT_CANON.md','STRAIN_PLAYTEST.md']:
        bind(R/'docs/mechanics'/name)
    for name in ['healing_playtest_rules.py','form_temphp_playtest_rules.py']:bind(R/'tools'/name)
    bind(R/'data/playtest/control_state_bindings.json')
    for name in ['WORLD_DUNGEON_LOOP.md','CRAFTING_HARVEST_PLAYTEST.md','EQUIPMENT_ITEM_PROCEDURES.md','EXPEDITION_STRUCTURE_CANON.md']:
        bind(R/'docs/mechanics'/name)
    for name in ['EXPEDITION_PLAYER_BOOK.md','EXPEDITION_DIRECTOR_BOOK.md','EXPEDITION_REVIEW_STATUS.json']:
        bind(R/'docs/mechanics/expedition'/name)
    for name in ['COSMOLOGY_PLANES_SOURCE_CONCORDANCE_01.json','COSMOLOGY_SAVED_WEBSITE_SOURCE_CHECK_01.json']:
        bind(A/name)
    class_files=[R/('data/public/class_playtests/'+n+'.json') for n in ['wizard','cleric','mage','druid','paladin','oracle','monk','warrior','manifest']]
    ck('Four actual casters and four defensive/body class payloads plus manifest',len(class_files)==9 and sum('cards' in read(p) for p in class_files)==8)
    for p in class_files:bind(p)
    for name in ['candidate.json','shared_rules.json','supplements.json']:bind(R/'data/public/feat_candidates/exact_01'/name)
    inherited=[]
    for n in list(range(20))+[20,22,23,24,26,27,28,32,33,36,37,39,40,43,44,45,46,47,48,49,50,63,68]+list(range(108,117))+[142]+list(range(143,152))+[172]:
        e=registry['entries'][n];b=e['currentAuthoritativeSource'];actual=bind(G/b['path'])
        ck('Exact accepted interface '+str(n),all(actual[k]==b[k] for k in ['bytes','sha256']))
        inherited.append({'registryPointer':'/entries/'+str(n),'completeEntryUnchanged':deepcopy(e),
            'scopeLimit':'Only exact accepted scope. Hammer manifestation/use,60ft broad lift,chosen-energy bodily conversion and area damage/Prone/exile require source-local choices. Damage,body,clock,control and Falling rules already settled remain inherited; private-cell/return exceptions need explicit named extension.'})
    counterparts=[]
    for ident in ['conjure-skybrand-weapon','summon-minor-weapon','catapult','thunderwave','force-spike','crystalline-flash','orb-of-annihilation','banishment','banish-elemental','elemental-banishment','dimensional-anchor','planar-barrier','rift-spiral']:
        e=next(e for e in index['entries'] if e['id']==ident)
        ck('Actually applied counterpart '+ident,e['authoredStatus']=='reviewed-authored-operational-playtest')
        p=(ip.parent/e['procedureFile']).resolve();d=read(p);ptr=e.get('wholeCardPointer') or e['procedurePointer'];b=bind(p)
        if e.get('completeEnvelopeBinding'):ck('Exact applied envelope '+ident,b==e['completeEnvelopeBinding'])
        if e.get('authoredAcceptanceReceipt'):ck('Exact acceptance receipt '+ident,bind(G/e['authoredAcceptanceReceipt']['path'])==e['authoredAcceptanceReceipt'])
        for path in e.get('caseSourceReferenceAliases',{}).values():bind(G/path)
        card=deepcopy(at(d,ptr))
        for key in ['operational','operationalCandidate']:
            op=card.get(key)
            if isinstance(op,dict):
                for path in op.get('sourceReview',[])+op.get('reviewEvidence',[]):bind(G/path)
                if op.get('authoringFile'):bind(R/op['authoringFile'])
        counterparts.append({'spellId':ident,'source':b,'pointer':ptr,'completeCurrentCard':card,
            'completeSharedRules':deepcopy(at(d,e['sharedRulesPointer']) if e.get('sharedRulesPointer') else d.get('sharedRules',{})),
            'indexEntry':deepcopy(e),'qualification':'Actual applied source and acceptance govern historical labels; no ungranted feature or global extension follows by analogy.'})
    lore=[]
    for name in ['The Cosmology of Decennium Descent.docx','The Decennium Descent and the Matrix of Oblivion.docx',
                 'The_World_of_Aethel_Lore.docx','webpage.html','docs/mechanics/OWNER_COSMOLOGY_LOCKS_2026-07-30.md']:
        lore.append({'source':bind(G/name),'scope':'Complete original evidence; only explicit later owner corrections supersede it. No new soul identity,plane map or Hunt exception.'})
    for name in ['CURRENT_COSMOLOGY_READ_FIRST.md','PLANES_REVIEWED_01.md','OWNER_RECONCILIATION_REVIEWED_01.md',
                 'HEARTCELL_OWNER_UPDATE_02.md','SOULS_RESEARCH_REVIEWED_01.md','EPILOGUE_RELIC_NULL_REVIEWED_01.md','Q6_LATER_LOCK_REVIEWED_01.md','CREATION_ORIGINS_REVIEWED_01.md','GODS_PANTHEONS_REVIEWED_01.md','CHRONOLOGY_SOURCE_REVIEWED_01.md','CHRONOLOGY_RESEARCH_ROUTE_REVIEWED_01.md','EQUATION_LIBRARY_SOURCE_INVENTORY_01.md']:
        lore.append({'source':bind(R/'docs/director-only/cosmology'/name),'scope':'Current bounded operational/owner reconciliation; historical workflow labels are not new pending decisions.'})
    for name in ['planes_reviewed_01.json','owner_reconciliation_reviewed_01.json','heartcell_owner_update_02.json','souls_research_reviewed_01.json','epilogue_relic_null_reviewed_01.json','q6_later_lock_reviewed_01.json','creation_origins_reviewed_01.json','gods_pantheons_reviewed_01.json','chronology_source_reviewed_01.json','chronology_research_route_reviewed_01.json','equation_library_source_inventory_01.json']:
        bind(R/'data/director/cosmology'/name)
    pending=[]
    for name in ['rank7-mechanics16','life-matter5','rank9-catastrophe10','rank9-storm-control6']:
        group=next(g for g in queue['groups'] if g['group']==name);b=bind(G/group['candidate']['path'])
        ck('Exact pending comparison '+name,b==group['candidate'])
        ab=bind(G/group['archive']['path'])
        ck('Complete pending archive '+name,ab==group['archive'])
        pending.append({'group':name,'candidate':b,'completeConferenceArchive':ab,'identities':group['identities'],'qualification':'Complete pending comparison archive,not selected authority.'})
    rank8_context={}
    for name in ['DD_Rank8_Damage_6_Part5_Conference_Return_01.zip','rank8-damage6-part5-conference-return-01/MODEL.json','RANK8_DAMAGE6_PART5_RETURN_01_LOCAL_PREFLIGHT.json','RANK8_DAMAGE6_PART5_RETURN_01_SEMANTIC_REVIEW_59.json','DD_Rank8_Damage6_Local_Corrections_01.zip','RANK8_DAMAGE6_LOCAL_CORRECTIONS_01_PREPARATION.json','GPT_PART5_RANK8_DAMAGE_CORRECTIONS_11_REQUEST.txt','GPT_PART5_RANK8_DAMAGE_RETURN_01_NATIVE.json']:
        rank8_context[name]=bind(A/name)
    rank8_context['qualification']='Completed proposed Rank8 return with eight independent local findings and unsent correction request.559 integrity/replay checks are not semantic acceptance.96 finite diagnostics include four failures. None of these six procedures is added to39 accepted-but-unapplied,applied to canonical rules or used as general authority.'
    accepted={
        'illusion14Model':bind(A/'illusion-perception14-exact-13/SPELLS_MODEL.json'),
        'actualAcceptanceReceipt':bind(A/'GPT_PART5_PERTINENT_RETURNS_01_RECEIPT.json'),
        'control15Successor':bind(A/'copy-ready-preparation-only-part5-successor-01/successor/CONTROL15_READY_REFERENCE_SUCCESSOR14.json'),
        'control15LocalReceipt':bind(A/'CONTROL15_PART5_FULL_RETURN_02_LOCAL_RECEIPT.json'),
        'laterOwnerChoices':bind(A/'PERTINENT_GPT_DECISIONS_2026_10_20_02.json'),
        'copyReadyPolicy':bind(A/'copy-ready-preparation-only-part5-successor-01/POLICY_SELECTION.json'),
        'copyReadyReceipt':bind(A/'COPY_READY_PREPARATION_ONLY_PART5_01_LOCAL_PREFLIGHT.json'),
        'currentFeatSharedRules':bind(R/'data/public/feat_candidates/exact_01/shared_rules.json'),
        'copySourceAddendum':bind(A/'feat335-copy-release-source-addendum-01/FEAT335_COPY_RELEASE_SOURCE_ADDENDUM_01.json'),
        'qualification':'Accepted-but-unapplied complete Illusion/Control and owner-policy context. Actual TrueSeeing,MassSuggestion,Soulburn/Reservoir and preparation-only copied-feat Ready remain settled in their scopes. The751-check Ready receipt does not implement the full mechanic. These records do not select new impact/exile procedures or new cosmology. Keep the five independent positive-content holds and pending comparison sources distinct.'}
    questions=[{'id':i,'spellIds':ids,'exactSourceOrConflict':src,'options':opts,'recommendationAndConsequences':rec,'decisionSelected':False} for i,ids,src,opts,rec in Q]
    ck('26 unique unselected questions',len(questions)==len({q['id'] for q in questions})==26 and all(not q['decisionSelected'] for q in questions))
    ck('All four identities have questions',set().union(*(set(q['spellIds']) for q in questions))==set(IDS))
    risk=dict(Counter(r['riskTier'] for r in records))
    ck('Four tierC identities',risk=={'C':4})
    ck('Four identities four complete placements',len(records)==4 and sum(len(r['completeCurrentBookBindings']) for r in records)==4)
    findings=FINDINGS
    cases=CASES
    candidate={'id':'RANK9-IMPACT-EXILE4-SOURCE-CONFERENCE01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
        'status':'SOURCE_CONFERENCE_PREPARED_UNSENT','developmentDirection':'video-game-only','records':records,
        'historicalWorkflowQualification':'Original post-push-only questions remain unchanged. Actual authorized GitHub backup through checkpoint61 is verified; current source preparation includes owner corrections and exact impact/exile comparison evidence without selecting new canon or applying mechanics.',
        'currentAcceptedInterfaceComparisons':inherited,'completeAppliedCounterparts':counterparts,'completeCosmologySourcesAndAuthority':lore,
        'pendingComparisonsNotAuthority':pending,'unacceptedRank8DamageComparison':rank8_context,'acceptedContextUnapplied':accepted,'questions':questions,'riskCounts':risk,'sourceFindings':findings,
        'semanticDelta':[{'spellId':r['spellId'],'riskTier':r['riskTier'],'riskReason':r['riskReason'],'startingPoint':'Full native source and preserved earlier questions; no complete authored procedure/cases.','genuineQuestionIds':[q['id'] for q in questions if r['spellId'] in q['spellIds']]} for r in records],
        'futureCaseRequirements':cases,'earlierOperationalWorkedCases':[],'currentVectors':[],'countsUnchanged':deepcopy(index['authoredCounts']),
        'sourceBindings':list(sources.values()),'newRuleAdoptions':0,'runtimeTestsExecuted':0,'humanPlaytests':0,'sourceInformationDeleted':0,'cosmologyDecisions':0,'wholeGameComplete':False}
    root.mkdir();frozen=[]
    for b in sources.values():
        p=G/b['path'];ck('Current complete source '+b['path'],info(p)==b)
        dst=root/'sources'/b['path'];target=frozen_io(dst);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(p.read_bytes())
        ck('Frozen complete bytes '+b['path'],target.read_bytes()==p.read_bytes());frozen.append({**b,'frozenCopy':dst.relative_to(G).as_posix()})
    for p,raw in protected.items():ck('Protected authority unchanged '+p.name,p.read_bytes()==raw)
    out.write_bytes(encoded(candidate))
    check.write_bytes(encoded({'candidate':info(out),'checks':checks,'checkCount':len(checks),'sourceCount':len(sources),'sourceIdentities':4,'placements':4,'questions':26,'riskCounts':risk,'earlierCompleteProcedures':0,'earlierOperationalWorkedCases':0,'newCurrentVectors':0,'failures':0,'validationScope':'Full source/access/context preservation; no semantic adoption or game-engine test.'}))
    manifest=root/'MANIFEST.json';manifest.write_bytes(encoded({'candidate':info(out),'check':info(check),'files':list(sources.values()),'frozenSources':frozen,'sourceCount':len(sources),'newRuleAdoptions':0}))
    readme='Four full rank9 impact/exile identities,four native placements,26 unselected questions,thirteen complete applied counterparts and four full pending comparison archives. All tierC. Full unaccepted Rank8 return and eight local findings accompany original cosmology,website,owner corrections and actual damage,body,control,Falling and exile interfaces. No procedure,case,canon or runtime adoption.\n'
    (root/'README.md').write_text(readme,encoding='utf8',newline='\n')
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p,name in [(out,'CANDIDATE.json'),(check,'SOURCE_CHECK.json'),(manifest,'MANIFEST.json')]:z.write(p,name)
        z.writestr('README.md',readme)
        for b in sources.values():z.write(frozen_io(root/'sources'/b['path']),'sources/'+b['path'])
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist())) and z.read('CANDIDATE.json')==out.read_bytes()
        for b in sources.values():assert z.read('sources/'+b['path'])==(G/b['path']).read_bytes()
    ab=info(archive)
    request.write_text(f'Review {archive.name}, {ab["bytes"]} bytes SHA256 {ab["sha256"]}. Read four full identities/placements,all26 unselected questions,thirteen complete applied counterparts and four full pending comparison archives. Preserve Eternal Anvil massive hammer/5d12force/1roundStunned; Reverse Gravity Field everything in60ft radius lifted60ft with actual later fall damage; Transmute Flesh to Energy12d10chosen energy and no resistances; Planar Collapse area12d6force/Prone/banished. Resolve complete useful target,geometry,action,clock,body,defense,control,exile and return procedures. Do not substitute damage-only,an unusable weapon window,foreign fall damage or invented instant death/cosmology. Core class17/rank9/base26RP,actual distinct class schools and range60vs120 remain fixed. Full original manuscripts,website and owner corrections are supplied. The completed Rank8 return remains unaccepted with8 local findings and4 failed finite diagnostics; its full evidence/correction packet is comparison only. Return all choices,complete successor bytes,reversible operations,two fully source-qualified positive encounters per identity and meaningful independent branches. Keep real Ready concentration,ray/cover geometry,GreaterDispel captured applications and valid class/body facts. Preserve owner implementation reservation and separate source,semantic,arithmetic,engine,human,balance,canon and release gates.\n',encoding='utf8',newline='\n')
    prep.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PREPARED_UNSENT','candidate':info(out),'archive':ab,'manifest':info(manifest),'check':info(check),'request':info(request),'sourceCount':len(sources),'identityCount':4,'placementCount':4,'questionCount':26,'riskCounts':risk,'allArchiveMembersVerified':True,'newRuleAdoptions':0,'sourceInformationDeleted':0}))
    print(json.dumps({'preparation':info(prep),'candidate':info(out),'archive':ab,'sources':len(sources),'checks':len(checks),'questions':26,'failures':0}))

if __name__=='__main__':main()
