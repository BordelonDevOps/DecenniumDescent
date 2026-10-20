"""Freeze complete casting/cost sources and explicit unselected review questions."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json, zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded
from prepare_ac5_current_interfaces_01 import at
from rank9_casting_cost_5_questions_01 import IDS,TIERS,Q,FINDINGS,CASES

def read(p):return json.loads(p.read_bytes())

def frozen_io(p):
    # Explicit extended Windows path only for this packet's nested preservation copies.
    return Path('\\\\?\\'+str(p.resolve()))

def main():
    stem='RANK9_CASTING_COST_5_SOURCE_CONFERENCE_01'
    root=A/'rank9-casting-cost5-source-conference-01-complete'
    out=R/'data/director/spell_review/rank9_casting_cost_5_source_conference_01.json'
    check,prep,request=[A/(stem+s) for s in ['_CHECK.json','_PREPARATION.json','_REQUEST.txt']]
    archive=A/'DD_Rank9_Casting_Cost_5_Source_Conference_01.zip'
    assert not any(p.exists() for p in [root,out,check,prep,request,archive])
    sources={};checks=[]
    def ck(label,ok):
        checks.append({'check':label,'passed':bool(ok)});assert ok,label
    def bind(p):
        b=info(p);sources[b['path']]=b;return b
    catp=R/'data/public/spell_playtests/catalog.json';ip=catp.parent/'authored_review_index.json'
    qp=R/'data/director/spell_review/remaining_work_queue_45.json'
    regp=R/'data/director/spell_review/accepted_interface_registry_06.json'
    cov=R/'data/playtest/game_development_coverage.json'
    protected={p:p.read_bytes() for p in [catp,ip,qp,regp,cov]}
    catalog,index,queue,registry=map(read,[catp,ip,qp,regp])
    olds=[A/(s+'_RANK9_SOURCE_PREPARATION.json') for s in ['TRANSMUTATION_UNIVERSAL','DIVINATION','NECROMANCY']]
    histories=[read(p) for p in olds]
    ck('Actual membership unchanged',index['authoredCounts']=={'reviewed':525,'pending':323} and index['representationCounts']['completeReviewedStandaloneProcedures']==249)
    ck('173 scoped interfaces',len(registry['entries'])==173)
    for p in [catp,ip,qp,regp,cov,*olds,Path(__file__),Path(__file__).with_name('rank9_casting_cost_5_questions_01.py'),
              A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_TIME_FATE_55.json',
              A/'PERTINENT_GPT_DECISIONS_2026_10_20_02.json',
              A/'GPT_PART5_PERTINENT_OWNER_CHOICES_2026_10_20_NATIVE.json',
              A/'GPT_UNITY_DEVELOPMENT_SETUP_2026_10_20_NATIVE.json',
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
    for name in ['VIDEO_GAME_ONLY_DIRECTIVE.md','CLASS_PLAYTEST_RULES.md','SPELL_INTEGRATION_RULES.md',
                 'COMBAT_ACTION_PLAYTEST.md','CORE_RESOLUTION_PLAYTEST.md','CONDITIONS_PLAYTEST.md',
                 'CONTROL_STATES_PLAYTEST.md','BODY_EQUIPMENT_PLAYTEST.md','CREATURE_LIFECYCLE_PLAYTEST.md',
                 'HEALING_DEATH_PLAYTEST.md','DAMAGE_SHARING_PLAYTEST.md','TRANSFORMATION_SPELL_PLAYTEST.md',
                 'FORM_TEMP_HP_PLAYTEST.md','MAXIMUM_HP_PLAYTEST.md','RESONANCE_CANON.md',
                 'COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md','FORM_TEMP_HP_SOURCE_BINDINGS.md',
                 'TRANSFORMATION_SPELL_SOURCE_VALIDATION.json','TRANSFORMATION_SPELL_PLAYTEST_VALIDATION.json']:
        bind(R/'docs/mechanics'/name)
    for name in ['healing_playtest_rules.py','form_temphp_playtest_rules.py',
                 'feat335_copy_capture.py','feat335_copy_release.py','feat335_copy_payloads.py','feat335_copy_class_release.py']:
        bind(R/'tools'/name)
    for cls in ['oracle','shaman','mirrorsage']:bind(R/('data/public/class_playtests/'+cls+'.json'))
    for name in ['candidate.json','shared_rules.json','supplements.json']:
        bind(R/'data/public/feat_candidates/exact_01'/name)
        bind(A/'copy-ready-preparation-only-part5-successor-01/successor/DescentReviewChanges/ReviewBible/data/public/feat_candidates/exact_01'/name)
    for name in ['POLICY_SELECTION.json','CODEX_HANDOFF.md','successor/CODEX_HANDOFF_RECONCILED.md',
                 'successor/IMPLEMENTATION_CASES_RECONCILED.json','successor/READY_GAP_MATRIX_RECONCILED.json',
                 'successor/SCOPED_DECISION_CONTINUITY_RECONCILED.json']:
        bind(A/'copy-ready-preparation-only-part5-successor-01'/name)
    inherited=[]
    for n in list(range(20))+[23,35,36,39,40,41,64,67,75,78,109,143]:
        e=registry['entries'][n];b=e['currentAuthoritativeSource'];actual=bind(G/b['path'])
        ck('Exact accepted interface '+str(n),all(actual[k]==b[k] for k in ['bytes','sha256']))
        inherited.append({'registryPointer':'/entries/'+str(n),'completeEntryUnchanged':deepcopy(e),
            'scopeLimit':'Only exact accepted scope. Any-spell invocation,instant ritual completion,historical learned-spell replay,all-available-RP pricing and demi-lich/free-necrotic casting require explicit new decisions. Lower scoped wrappers/discounts do not automatically narrow these printed promises.'})
    counterparts=[]
    for ident in ['counterspell','spellshift','ritual-anchor','delay-spell','spell-mirror','resonance-influence','resonance-nexus','resonance-forge','harmonic-bulwark','polymorph','shapechange','fleeting-flight']:
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
                 'HEARTCELL_OWNER_UPDATE_02.md','SOULS_RESEARCH_REVIEWED_01.md','EPILOGUE_RELIC_NULL_REVIEWED_01.md']:
        lore.append({'source':bind(R/'docs/director-only/cosmology'/name),'scope':'Current bounded operational/owner reconciliation; historical workflow labels are not new pending decisions.'})
    for name in ['planes_reviewed_01.json','owner_reconciliation_reviewed_01.json','heartcell_owner_update_02.json','souls_research_reviewed_01.json','epilogue_relic_null_reviewed_01.json']:
        bind(R/'data/director/cosmology'/name)
    pending=[]
    for name in ['magic-modifiers7','rank7-identity-casting5','rank8-resource6','time-cast5']:
        group=next(g for g in queue['groups'] if g['group']==name);b=bind(G/group['candidate']['path'])
        ck('Exact pending comparison '+name,b==group['candidate'])
        ab=bind(G/group['archive']['path'])
        ck('Complete pending archive '+name,ab==group['archive'])
        pending.append({'group':name,'candidate':b,'completeConferenceArchive':ab,'identities':group['identities'],'qualification':'Complete pending comparison archive,not selected authority.'})
    accepted={
        'illusion14Model':bind(A/'illusion-perception14-exact-13/SPELLS_MODEL.json'),
        'companion10Model':bind(A/'companion-life10-exact-05/SPELLS_MODEL.json'),
        'companion10Casebook':bind(A/'companion-life10-exact-05/CASEBOOK.json'),
        'companion10CompleteSubmittedSources':bind(A/'DD_Companion_Life_10_Exact_05.zip'),
        'actualAcceptanceReceipt':bind(A/'GPT_PART5_PERTINENT_RETURNS_01_RECEIPT.json'),
        'control15Successor':bind(A/'copy-ready-preparation-only-part5-successor-01/successor/CONTROL15_READY_REFERENCE_SUCCESSOR14.json'),
        'control15LocalReceipt':bind(A/'CONTROL15_PART5_FULL_RETURN_02_LOCAL_RECEIPT.json'),
        'laterOwnerChoices':bind(A/'PERTINENT_GPT_DECISIONS_2026_10_20_02.json'),
        'copyReadyPolicy':bind(A/'copy-ready-preparation-only-part5-successor-01/POLICY_SELECTION.json'),
        'copyReadyReceipt':bind(A/'COPY_READY_PREPARATION_ONLY_PART5_01_LOCAL_PREFLIGHT.json'),
        'currentFeatSharedRules':bind(R/'data/public/feat_candidates/exact_01/shared_rules.json'),
        'copySourceAddendum':bind(A/'feat335-copy-release-source-addendum-01/FEAT335_COPY_RELEASE_SOURCE_ADDENDUM_01.json'),
        'qualification':'Accepted-but-unapplied complete Illusion/Control context. TrueSeeing retains only actual recognized-benefit scope. The exact preparation-only copied-feat Ready successor passed751 local preservation/reconstruction/case-data checks and remains unapplied. The complete Companion10 model/cases preserve actual Soulburn and the owner latest limited Reservoir choice. No blanket refund permission follows. These sources do not select rank9 access,waiver,ritual or form behavior.'}
    questions=[{'id':i,'spellIds':ids,'exactSourceOrConflict':src,'options':opts,'recommendationAndConsequences':rec,'decisionSelected':False} for i,ids,src,opts,rec in Q]
    ck('32 unique unselected questions',len(questions)==len({q['id'] for q in questions})==32 and all(not q['decisionSelected'] for q in questions))
    ck('All five identities have questions',set().union(*(set(q['spellIds']) for q in questions))==set(IDS))
    risk=dict(Counter(r['riskTier'] for r in records))
    ck('All five tierC',risk=={'C':5})
    ck('Five identities five complete placements',len(records)==5 and sum(len(r['completeCurrentBookBindings']) for r in records)==5)
    findings=FINDINGS
    cases=CASES
    candidate={'id':'RANK9-CASTING-COST5-SOURCE-CONFERENCE01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
        'status':'SOURCE_CONFERENCE_PREPARED_UNSENT','developmentDirection':'video-game-only','records':records,
        'currentAcceptedInterfaceComparisons':inherited,'completeAppliedCounterparts':counterparts,'completeCosmologySourcesAndAuthority':lore,
        'pendingComparisonsNotAuthority':pending,'acceptedContextUnapplied':accepted,'questions':questions,'riskCounts':risk,'sourceFindings':findings,
        'semanticDelta':[{'spellId':r['spellId'],'riskTier':r['riskTier'],'riskReason':r['riskReason'],'startingPoint':'Full native source and preserved earlier questions; no complete authored procedure/cases.','genuineQuestionIds':[q['id'] for q in questions if r['spellId'] in q['spellIds']]} for r in records],
        'futureCaseRequirements':cases,'earlierOperationalWorkedCases':[],'currentVectors':[],'countsUnchanged':deepcopy(index['authoredCounts']),
        'sourceBindings':list(sources.values()),'newRuleAdoptions':0,'runtimeTestsExecuted':0,'humanPlaytests':0,'sourceInformationDeleted':0,'cosmologyDecisions':0,'wholeGameComplete':False}
    root.mkdir();frozen=[]
    for b in sources.values():
        p=G/b['path'];ck('Current complete source '+b['path'],info(p)==b)
        dst=root/'sources'/b['path'];target=frozen_io(dst)
        target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(p.read_bytes())
        ck('Frozen complete bytes '+b['path'],target.read_bytes()==p.read_bytes());frozen.append({**b,'frozenCopy':dst.relative_to(G).as_posix()})
    for p,raw in protected.items():ck('Protected authority unchanged '+p.name,p.read_bytes()==raw)
    out.write_bytes(encoded(candidate))
    check.write_bytes(encoded({'candidate':info(out),'checks':checks,'checkCount':len(checks),'sourceCount':len(sources),'sourceIdentities':5,'placements':5,'questions':32,'riskCounts':risk,'earlierCompleteProcedures':0,'earlierOperationalWorkedCases':0,'newCurrentVectors':0,'failures':0,'validationScope':'Full source/access/context preservation; no semantic adoption or game-engine test.'}))
    manifest=root/'MANIFEST.json';manifest.write_bytes(encoded({'candidate':info(out),'check':info(check),'files':list(sources.values()),'frozenSources':frozen,'sourceCount':len(sources),'newRuleAdoptions':0}))
    readme='Five complete rank9 casting/cost identities, five placements, 32 unselected questions, twelve applied counterparts and four full pending comparison archives. All five tier C. Source-only conference; no procedure or runtime adoption.\n'
    (root/'README.md').write_text(readme,encoding='utf8',newline='\n')
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p,name in [(out,'CANDIDATE.json'),(check,'SOURCE_CHECK.json'),(manifest,'MANIFEST.json')]:z.write(p,name)
        z.writestr('README.md',readme)
        for b in sources.values():z.write(frozen_io(root/'sources'/b['path']),'sources/'+b['path'])
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist())) and z.read('CANDIDATE.json')==out.read_bytes()
        for b in sources.values():assert z.read('sources/'+b['path'])==(G/b['path']).read_bytes()
    ab=info(archive)
    request.write_text(f'Review {archive.name},{ab["bytes"]}bytes SHA256{ab["sha256"]}. Read five full identities, five native placements, 32 unselected questions, twelve applied counterparts and four complete pending comparison archives. Preserve any-spell access and actual component/cost/time waiver,instant ritual completion despite the10-minute Core conflict,one formerly known spell asrank9,the literal all-available-RP price for a full minute,and useful demi-lich transformation with resistance to all,flight andfree necrotic spells. Inspect actual class permissions,current price order,paid-output spells,full Companion10/Soulburn context,latest owner choices and the exact unapplied Ready successor. Return finite useful wrapper and payment procedures,real source-qualified positive cases and explicit NEW decisions without silently importing narrower lower-rank contracts. Return explicit scoped decisions,full useful procedures and source-qualified positive encounters. Do not weaken benefits,import foreign rules or treat pending comparisons as authority. Preserve owner implementation reservation and separate source,semantic,runtime,human,balance,cosmology and release gates.\n',encoding='utf8',newline='\n')
    prep.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PREPARED_UNSENT','candidate':info(out),'archive':ab,'manifest':info(manifest),'check':info(check),'request':info(request),'sourceCount':len(sources),'identityCount':5,'placementCount':5,'questionCount':32,'riskCounts':risk,'allArchiveMembersVerified':True,'newRuleAdoptions':0,'sourceInformationDeleted':0}))
    print(json.dumps({'preparation':info(prep),'candidate':info(out),'archive':ab,'sources':len(sources),'checks':len(checks),'questions':32,'failures':0}))

if __name__=='__main__':main()
