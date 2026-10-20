"""Freeze complete defense/form sources and explicit unselected review questions."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json, zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded
from prepare_ac5_current_interfaces_01 import at
from rank9_defense_form_8_questions_01 import IDS,TIERS,Q

def read(p):return json.loads(p.read_bytes())

def main():
    stem='RANK9_DEFENSE_FORM_8_SOURCE_CONFERENCE_01'
    root=A/'rank9-defense-form8-source-conference-01'
    out=R/'data/director/spell_review/rank9_defense_form_8_source_conference_01.json'
    check,prep,request=[A/(stem+s) for s in ['_CHECK.json','_PREPARATION.json','_REQUEST.txt']]
    archive=A/'DD_Rank9_Defense_Form_8_Source_Conference_01.zip'
    assert not any(p.exists() for p in [root,out,check,prep,request,archive])
    sources={};checks=[]
    def ck(label,ok):
        checks.append({'check':label,'passed':bool(ok)});assert ok,label
    def bind(p):
        b=info(p);sources[b['path']]=b;return b
    catp=R/'data/public/spell_playtests/catalog.json';ip=catp.parent/'authored_review_index.json'
    qp=R/'data/director/spell_review/remaining_work_queue_40.json'
    regp=R/'data/director/spell_review/accepted_interface_registry_06.json'
    cov=R/'data/playtest/game_development_coverage.json'
    protected={p:p.read_bytes() for p in [catp,ip,qp,regp,cov]}
    catalog,index,queue,registry=map(read,[catp,ip,qp,regp])
    olds=[A/(s+'_RANK9_SOURCE_PREPARATION.json') for s in ['ABJURATION','ILLUSION','TRANSMUTATION_UNIVERSAL']]
    histories=[read(p) for p in olds]
    ck('Actual membership unchanged',index['authoredCounts']=={'reviewed':525,'pending':323} and index['representationCounts']['completeReviewedStandaloneProcedures']==249)
    ck('173 scoped interfaces',len(registry['entries'])==173)
    for p in [catp,ip,qp,regp,cov,*olds,Path(__file__),Path(__file__).with_name('rank9_defense_form_8_questions_01.py'),
              A/'ACTIVE_AUTHORING_CHECKPOINT_RANK9_DEATH_RECOVERY_49.json',
              A/'PERTINENT_GPT_DECISIONS_2026_10_20_01.json',
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
        ck('Every full native placement '+ident,len(books)==len(card['source']['original']['placements'])==1)
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
                 'CONTROL_STATES_PLAYTEST.md','BODY_EQUIPMENT_PLAYTEST.md','CREATURE_LIFECYCLE_PLAYTEST.md','HEALING_DEATH_PLAYTEST.md',
                 'DAMAGE_SHARING_PLAYTEST.md','TRANSFORMATION_SPELL_PLAYTEST.md','FORM_TEMP_HP_PLAYTEST.md',
                 'MAXIMUM_HP_PLAYTEST.md','RESONANCE_CANON.md','COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md']:
        bind(R/'docs/mechanics'/name)
    for name in ['healing_playtest_rules.py','form_temphp_playtest_rules.py']:bind(R/'tools'/name)
    for cls in ['oracle','shaman']:bind(R/('data/public/class_playtests/'+cls+'.json'))
    inherited=[]
    for n in list(range(12))+[13,14,20,22,37,39,40]+list(range(108,117))+list(range(143,152)):
        e=registry['entries'][n];b=e['currentAuthoritativeSource'];actual=bind(G/b['path'])
        ck('Exact accepted interface '+str(n),all(actual[k]==b[k] for k in ['bytes','sha256']))
        inherited.append({'registryPointer':'/entries/'+str(n),'completeEntryUnchanged':deepcopy(e),
            'scopeLimit':'Only exact accepted scope. New immunity,permanent stacking,reflection,body,time and closed-boundary extensions require explicit per-spell decisions.'})
    counterparts=[]
    for ident in ['elemental-resistance','protection-from-energy','protective-sphere','wall-of-force','dimensional-anchor','gaseous-form','haste','slow','greater-dispel','antimagic-field-lesser']:
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
    for name in ['rank8-ward5','rank8-life-form4','rank8-control5','rank9-storm-control6']:
        group=next(g for g in queue['groups'] if g['group']==name);b=bind(G/group['candidate']['path'])
        ck('Exact pending comparison '+name,b==group['candidate'])
        pending.append({'group':name,'candidate':b,'identities':group['identities'],'qualification':'Prepared source comparison only,not selected authority.'})
    temporal=next(row for row in queue['rows'] if row['id']=='time-stop')
    th=next(h for h in histories if any(x['spellId']=='time-stop' for x in h['selectedSpells']))
    ts=next(x for x in th['selectedSpells'] if x['spellId']=='time-stop')
    tb=[deepcopy(b) for b in th['currentBookBindings'] if b['spellId']=='time-stop']
    ck('Complete pending TimeStop dependency',ts['fullSourceAndCurrentAccessRecord']==temporal['completeCurrentSourceAndAccess'] and len(tb)==3)
    for b in tb:
        n=b['currentBookRow']['line']-1
        ck('Exact pending TimeStop manuscript '+str(n),lines[n]==b['currentBookRow']['exactText']==reference[n])
    pending.append({'spellId':'time-stop','fullSourceAndCurrentAccess':deepcopy(temporal['completeCurrentSourceAndAccess']),
        'completeOriginalSourceQuestionUnchanged':deepcopy(ts),'completeCurrentBookBindings':tb,
        'qualification':'Complete unselected three-placement dependency only; no operational TimeStop or global personal-time rule is adopted.'})
    accepted={
        'illusion14Model':bind(A/'illusion-perception14-exact-13/SPELLS_MODEL.json'),
        'actualAcceptanceReceipt':bind(A/'GPT_PART5_PERTINENT_RETURNS_01_RECEIPT.json'),
        'control15Successor':bind(A/'control15-full-conference-part5-return-02/successor/CONTROL15_REVIEWED_SUCCESSOR13.json'),
        'control15LocalReceipt':bind(A/'CONTROL15_PART5_FULL_RETURN_02_LOCAL_RECEIPT.json'),
        'laterOwnerChoices':bind(A/'PERTINENT_GPT_DECISIONS_2026_10_20_01.json'),
        'qualification':'Accepted-but-unapplied complete Illusion/Control context. TrueSeeing retains only actual recognized-benefit scope. Later preparation-only copied-feat Ready supersedes older both-round wording; exact successor review is active. These sources do not automatically select new immunity,reflection,time or barrier behavior.'}
    questions=[{'id':i,'spellIds':ids,'exactSourceOrConflict':src,'options':opts,'recommendationAndConsequences':rec,'decisionSelected':False} for i,ids,src,opts,rec in Q]
    ck('26 unique unselected questions',len(questions)==len({q['id'] for q in questions})==26 and all(not q['decisionSelected'] for q in questions))
    ck('All eight identities have questions',set().union(*(set(q['spellIds']) for q in questions))==set(IDS))
    risk=dict(Counter(r['riskTier'] for r in records))
    ck('Two B six C',risk=={'C':6,'B':2})
    ck('Eight identities eight complete placements',len(records)==8 and sum(len(r['completeCurrentBookBindings']) for r in records)==8)
    findings=['All eight native actual routes are rank9/minimumclasslevel17/base26RP,Action/V/S/F; preserve actual school access and Touch versus ranged distinctions.', 'AbsoluteImmunity preserves all damage and condition immunity for1minute. Current named-condition immunity suppresses active consequences while clocks continue,without curing underlying0HP/death or refunding prior actions/concentration.', 'AstralShell preserves ordinary resistance across damage types for1minute. Illusion is not automatic disbelief failure or TrueSeeing removal; read exact source-specific recognized-benefit scopes.', 'DivineShield retains every eligible ally in30-footradius and BOTHone damage-type immunity andone condition immunity. Snapshot/aura,choice and finite duration remain explicit questions.', 'EternalProtection is permanent/until dispelled,not an invented short buff. Multiple paid types and same-name replacement need a substantive explicit policy.', 'ElementalShell must retain positive50percentreflection despite its own elemental immunity. Pre-immunity basis,real source attribution,defenses and shared causal ledger need new scoped decisions.', 'BodytoVoid must supply an actual useful energy-body state ANDautomatic attack misses for3rounds; no AC-only substitute,unearned spell-component waiver or silent generic nonattack immunity.', 'TimelessForm retains aging/TimeStop/Haste/Slow immunity for1minute. Full existing Haste and both Slow modes are included; complete TimeStop source remains a dependency,not implemented time mechanics.', 'InvulnerableSphere needs complete useful closed geometry and actual cannot-enter/exit behavior. Light,sound,air,teleportation,externalmagic,admission,real agency,clocks and suppression/occupied boundary are explicit; weaker barriers do not define its exceptions.', 'The owner SNES-style exploration/tactical/management direction is retained without prematurely selecting global time conversions,engine implementation or lore identities.']
    cases=['After decisions,at least two complete actual source-qualified cases per identity plus every substantive immunity,body,time,reflection and barrier branch; retain real access/components/26RP/cadence and original source ownership.', 'All cases need whole3D bodies,actual positions,target legality,HP/tempHP/conditions,damage types,allRNG,exact phases,intermediate transitions and final state. No invented creature profile or generic class-feature grant.', 'AbsoluteImmunity: actual multiple condition consequences,existing clocks,suppression/resumption,0HP/death boundary,source-specific transferred post-defense and directcost distinctions.', 'AstralShell: whole damage-type scope,ordinary nonstacking resistance and exact TrueSeeing interaction; do not use a generic Illusion-dispel assertion.', 'DivineShield: multiple allied recipients,both immunity choices,exact geometry,aura/snapshot transition,source ending and no recreated action or status history.', 'EternalProtection: permanent source through casterdeath/rest/save-load,legal dispel and chosen multiple-type/replacement policy.', 'ElementalShell: positive reflection while immune,oddrounding,existing defense,mixed damage,environmental/noncreature source and reciprocal/redirected causal branches without duplicate root damage.', 'BodytoVoid: actual energy-form locomotion/perception/agency,legal attacks automatically missing,nonattack effects,real gear/HP persistence and occupied/unsupported reversion.', 'TimelessForm: new/existing Haste/Slow effects,endingcost/spentAction history and positive TimeStop dependency; no global clock or free-turn invention.', 'InvulnerableSphere: complete closed boundary,lawful creation,meaningful contained agency,blocked entry/exit and actual source ending/suppression/resumption with no crushing,stasis or generic escape loophole.', 'Preserve save/load and mode-transition ownership and histories; source,semantic,arithmetic,engine/runtime,human,balance,cosmology and release gates remain separate.']
    candidate={'id':'RANK9-DEFENSE-FORM8-SOURCE-CONFERENCE01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
        'status':'SOURCE_CONFERENCE_PREPARED_UNSENT','developmentDirection':'video-game-only','records':records,
        'currentAcceptedInterfaceComparisons':inherited,'completeAppliedCounterparts':counterparts,'completeCosmologySourcesAndAuthority':lore,
        'pendingComparisonsNotAuthority':pending,'acceptedContextUnapplied':accepted,'questions':questions,'riskCounts':risk,'sourceFindings':findings,
        'semanticDelta':[{'spellId':r['spellId'],'riskTier':r['riskTier'],'riskReason':r['riskReason'],'startingPoint':'Full native source and preserved earlier questions; no complete authored procedure/cases.','genuineQuestionIds':[q['id'] for q in questions if r['spellId'] in q['spellIds']]} for r in records],
        'futureCaseRequirements':cases,'earlierOperationalWorkedCases':[],'currentVectors':[],'countsUnchanged':deepcopy(index['authoredCounts']),
        'sourceBindings':list(sources.values()),'newRuleAdoptions':0,'runtimeTestsExecuted':0,'humanPlaytests':0,'sourceInformationDeleted':0,'cosmologyDecisions':0,'wholeGameComplete':False}
    root.mkdir();frozen=[]
    for b in sources.values():
        p=G/b['path'];ck('Current complete source '+b['path'],info(p)==b)
        dst=root/'sources'/b['path'];dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(p.read_bytes())
        ck('Frozen complete bytes '+b['path'],dst.read_bytes()==p.read_bytes());frozen.append({**b,'frozenCopy':dst.relative_to(G).as_posix()})
    for p,raw in protected.items():ck('Protected authority unchanged '+p.name,p.read_bytes()==raw)
    out.write_bytes(encoded(candidate))
    check.write_bytes(encoded({'candidate':info(out),'checks':checks,'checkCount':len(checks),'sourceCount':len(sources),'sourceIdentities':8,'placements':8,'questions':26,'riskCounts':risk,'earlierCompleteProcedures':0,'earlierOperationalWorkedCases':0,'newCurrentVectors':0,'failures':0,'validationScope':'Full source/access/context preservation; no semantic adoption or game-engine test.'}))
    manifest=root/'MANIFEST.json';manifest.write_bytes(encoded({'candidate':info(out),'check':info(check),'files':list(sources.values()),'frozenSources':frozen,'sourceCount':len(sources),'newRuleAdoptions':0}))
    readme='Eight full defense/form identities,eight placements,26 unselected questions,ten applied counterparts and complete pending TimeStop dependency. Two tierB,six tierC. All sources preserved. Source-only conference,not procedure/vector/runtime/cosmology adoption.\n'
    (root/'README.md').write_text(readme,encoding='utf8',newline='\n')
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p,name in [(out,'CANDIDATE.json'),(check,'SOURCE_CHECK.json'),(manifest,'MANIFEST.json')]:z.write(p,name)
        z.writestr('README.md',readme)
        for b in sources.values():z.write(root/'sources'/b['path'],'sources/'+b['path'])
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist())) and z.read('CANDIDATE.json')==out.read_bytes()
        for b in sources.values():assert z.read('sources/'+b['path'])==(G/b['path']).read_bytes()
    ab=info(archive)
    request.write_text(f'Review {archive.name},{ab["bytes"]}bytes SHA256{ab["sha256"]}. Read all eight complete sources,eight native placements,26 unselected questions,ten applied counterparts,full pending TimeStop and accepted-but-unapplied Illusion/Control context. Preserve full immunity/resistance,permanence,positive reflection,real energy form,temporal protection and closed containment. Return explicit source-faithful choices,complete useful procedures and qualified positive cases. Do not replace benefits with convenient weaker effects or adopt unreviewed clocks/lore. Keep owner-reserved implementation and all validation gates distinct.\n',encoding='utf8',newline='\n')
    prep.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PREPARED_UNSENT','candidate':info(out),'archive':ab,'manifest':info(manifest),'check':info(check),'request':info(request),'sourceCount':len(sources),'identityCount':8,'placementCount':8,'questionCount':26,'riskCounts':risk,'allArchiveMembersVerified':True,'newRuleAdoptions':0,'sourceInformationDeleted':0}))
    print(json.dumps({'preparation':info(prep),'candidate':info(out),'archive':ab,'sources':len(sources),'checks':len(checks),'questions':26,'failures':0}))

if __name__=='__main__':main()
