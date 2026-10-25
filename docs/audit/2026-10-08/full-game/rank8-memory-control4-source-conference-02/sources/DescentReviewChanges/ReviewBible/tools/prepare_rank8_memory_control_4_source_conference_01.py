"""Freeze four exact rank-eight sources and their unselected mechanics questions."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json
import zipfile
from apply_di7_ap_as_01 import G, R, A, info, encoded
from prepare_ac5_current_interfaces_01 import at
from rank8_memory_control_4_questions_01 import IDS, TIERS, Q


def read(p):
    return json.loads(p.read_bytes())


def main():
    stem = 'RANK8_MEMORY_CONTROL_4_SOURCE_CONFERENCE_01'
    root = A/'rank8-memory-control4-source-conference-01'
    out = R/'data/director/spell_review/rank8_memory_control_4_source_conference_01.json'
    check,prep,request = [A/(stem+s) for s in ['_CHECK.json','_PREPARATION.json','_REQUEST.txt']]
    archive = A/'DD_Rank8_Memory_Control_4_Source_Conference_01.zip'
    assert not any(p.exists() for p in [root,out,check,prep,request,archive])
    sources,checks = {},[]
    def ck(name,value):
        checks.append({'check':name,'passed':bool(value)})
        assert value,name
    def bind(p):
        b = info(p)
        sources[b['path']] = b
        return b
    catp = R/'data/public/spell_playtests/catalog.json'
    ip = catp.parent/'authored_review_index.json'
    qp = R/'data/director/spell_review/remaining_work_queue_26.json'
    regp = R/'data/director/spell_review/accepted_interface_registry_06.json'
    oldp = A/'DIVINATION_ENCHANTMENT_RANK8_SOURCE_PREPARATION.json'
    catalog,index,queue,registry,old = map(read,[catp,ip,qp,regp,oldp])
    ck('525 reviewed323 pending',index['authoredCounts'] == {'reviewed':525,'pending':323})
    ck('173 accepted interfaces',len(registry['entries']) == 173)
    for p in [catp,ip,qp,regp,oldp,Path(__file__),Path(__file__).with_name('rank8_memory_control_4_questions_01.py'),R/'rulebook_output.txt',G/'docs/reference/Player_Rulebook_v6_source_text.txt',A/'ACTIVE_AUTHORING_CHECKPOINT_PART5_PROGRESS_33.json',A/'LOW_RANK_136_EXACT_FULFILLMENT.json',A/'LANGUAGE_EXACT_FULFILLMENT.json',A/'GPT_CONTROL_FINAL_REVIEW.md',A/'COMPANION_LIFE_10_EXACT05_PART5_SUBMISSION_01.json',A/'ILLUSION_PERCEPTION_14_PART5_RETURN_01_RECEIPT.json',R/'data/playtest/control_state_bindings.json',R/'data/playtest/condition_playtests.json',R/'data/playtest/language_communication_candidate_public.json',R/'data/playtest/bestiary_public_source_candidate.json',G/'docs/audit/2026-10-18/github-snapshot-part5-wards/PUSH_RECEIPT.json']:
        bind(p)
    lines = (R/'rulebook_output.txt').read_text('utf-16').splitlines()
    reference = (G/'docs/reference/Player_Rulebook_v6_source_text.txt').read_text('utf8').splitlines()
    records = []
    for ident in IDS:
        n = next(n for n,s in enumerate(old['selectedSpells']) if s['spellId'] == ident)
        historical = old['selectedSpells'][n]
        card = next(s for s in catalog['spells'] if s['id'] == ident)
        row = next(s for s in queue['rows'] if s['id'] == ident)
        entry = next(s for s in index['entries'] if s['id'] == ident)
        ck('Exact native source/access '+ident,historical['fullSourceAndCurrentAccessRecord'] == card == row['completeCurrentSourceAndAccess'])
        ck('No earlier complete procedure '+ident,row['currentGroup'] is None and not row['previousAuthoringMapRowUnchanged']['completeEarlierProposalRecords'])
        ck('Pending authored membership '+ident,entry['authoredStatus'] == 'pending-authored-procedure')
        ck('Rank8 actual15 and21RP '+ident,all(x['rank'] == 8 and x['minimumClassLevel'] == 15 and x['baseRpCost'] == 21 for x in card['classAccess'].values()))
        ck('Actual class set '+ident,set(card['classAccess']) == ({'Cleric','Wizard'} if ident == 'mind-ravel' else {'Wizard'}))
        book = [deepcopy(b) for b in old['currentBookBindings'] if b['spellId'] == ident]
        ck('One actual school placement '+ident,len(book) == len(card['source']['original']['placements']) == 1)
        for b in book:
            pos = b['currentBookRow']['line']-1
            ck('Both exact manuscript lines '+ident,lines[pos] == b['currentBookRow']['exactText'] == reference[pos])
        for kind in ['catalog','core']:
            ck('Underlying exact source '+ident+kind,bind(R/card['source'][kind+'Path'])['sha256'] == card['source'][kind+'Sha256'])
        ck('No historical alias merged '+ident,card['source']['possibleHistoricalAliases'] == [])
        records.append({'spellId':ident,'riskTier':TIERS[ident][0],'riskReason':TIERS[ident][1],'completeCurrentCatalogSourceAndAccess':deepcopy(card),'currentIndexEntry':deepcopy(entry),'originalQuestionSource':info(oldp),'originalQuestionPointer':'/selectedSpells/'+str(n),'completeOriginalSourceQuestionUnchanged':deepcopy(historical),'completeHistoricalCommonQuestionUnchanged':old['commonOperationalQuestion'],'completeHistoricalScopeExceptionUnchanged':old['commonQuestionException'],'completeCurrentBookBindings':book,'earlierCompleteProcedures':[],'earlierOperationalWorkedCases':[],'status':'Prepared source conference; no operative rule or case adopted.'})
    for cls in ['wizard','cleric','tinker','oracle','paladin']:
        bind(R/('data/public/class_playtests/'+cls+'.json'))
    for name in ['VIDEO_GAME_ONLY_DIRECTIVE.md','CLASS_PLAYTEST_RULES.md','SPELL_INTEGRATION_RULES.md','COMBAT_ACTION_PLAYTEST.md','CORE_RESOLUTION_PLAYTEST.md','CONDITIONS_PLAYTEST.md','CONTROL_STATES_PLAYTEST.md','CONTROL_SOURCE_BINDINGS.md','BODY_EQUIPMENT_PLAYTEST.md','CREATURE_LIFECYCLE_PLAYTEST.md','HEALING_DEATH_PLAYTEST.md','TRANSFORMATION_SPELL_PLAYTEST.md','CONDITION_RECOVERY_PLAYTEST.md','LANGUAGE_COMMUNICATION_PLAYTEST.md','ENCHANTMENT_CONTROL_INTEGRATION_PLAYTEST.md','ENCHANTMENT_RANK3_INTEGRATION_PLAYTEST.md','COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md']:
        bind(R/'docs/mechanics'/name)
    inherited = []
    for n in [0,1,3,4,7,8,11,19,36,39,40]+list(range(78,89))+[90,91,92]:
        e = registry['entries'][n]
        b = e['currentAuthoritativeSource']
        actual = bind(G/b['path'])
        ck('Exact current interface '+str(n),all(actual[k] == b[k] for k in ['bytes','sha256']))
        inherited.append({'registryPointer':'/entries/'+str(n),'completeEntryUnchanged':deepcopy(e),'scopeLimit':'Reuse actual casting, hard-control, timing, information and source-bound bridges only in their accepted scopes. Extending a named source bridge to these new spells needs an explicit per-card decision.'})
    counterparts = []
    counterpart_ids = ['disrupt-memory','dire-charm','dominate-person','confusion','erase-emotion','charm-monster','synaptic-static','antimagic-field-lesser','greater-dispel','protection-from-scrying']
    for ident in counterpart_ids:
        e = next(s for s in index['entries'] if s['id'] == ident)
        ck('Actual reviewed counterpart '+ident,e['authoredStatus'] == 'reviewed-authored-operational-playtest')
        path = (ip.parent/e['procedureFile']).resolve()
        doc = read(path)
        ptr = e.get('wholeCardPointer',e['procedurePointer'])
        b = bind(path)
        if e.get('completeEnvelopeBinding'):
            ck('Exact accepted envelope '+ident,b == e['completeEnvelopeBinding'])
        if e.get('authoredAcceptanceReceipt'):
            rb = e['authoredAcceptanceReceipt']
            ck('Exact actual acceptance '+ident,bind(G/rb['path']) == rb)
        for ref in e.get('caseSourceReferenceAliases',{}).values():
            bind(G/ref)
        card = deepcopy(at(doc,ptr))
        if 'operational' in card and isinstance(card['operational'],dict):
            for rel in card['operational'].get('sourceReview',[])+card['operational'].get('reviewEvidence',[]):
                bind(G/rel)
        counterparts.append({'spellId':ident,'source':b,'pointer':ptr,'completeCurrentCard':card,'completeSharedRules':deepcopy(doc.get('sharedRules',{})),'indexEntry':deepcopy(e),'qualification':'Exact actual reviewed scope only; no source-name analogy or historical candidate flag grants another spell approval.'})
    pending = []
    for groupname in ['memory2','control15','rank8-control5','rank8-ward5','companion-life10']:
        group = next(g for g in queue['groups'] if g['group'] == groupname)
        b = bind(G/group['candidate']['path'])
        ck('Exact full pending comparison '+groupname,b == group['candidate'])
        pending.append({'group':groupname,'candidate':b,'identities':group['identities'],'qualification':'Pending source/procedure comparison, not accepted authority. CompanionExact05 actual review is active at preparation; later review outcomes require a separate receipt.'})
    questions = [{'id':i,'spellIds':ids,'exactSourceOrConflict':src,'options':opts,'recommendationAndConsequences':rec,'decisionSelected':False} for i,ids,src,opts,rec in Q]
    ck('21 unique unselected questions',len(questions) == len({q['id'] for q in questions}) == 21 and all(not q['decisionSelected'] for q in questions))
    ck('Four identities and four placements',len(records) == 4 and sum(len(r['completeCurrentBookBindings']) for r in records) == 4)
    ck('Every identity covered',set().union(*(set(q['spellIds']) for q in questions)) == set(IDS))
    candidate = {'id':'RANK8-MEMORY-CONTROL4-SOURCE-CONFERENCE01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'SOURCE_CONFERENCE_PREPARED_UNSENT','developmentDirection':'video-game-only','records':records,'currentAcceptedInterfaceComparisons':inherited,'completeAcceptedCounterparts':counterparts,'pendingComparisonsNotAuthority':pending,'questions':questions,'riskCounts':{'C':4},'semanticDelta':[{'spellId':r['spellId'],'riskTier':r['riskTier'],'riskReason':r['riskReason'],'startingPoint':'Complete exact native sources; no previous complete procedure or operative cases.','genuineQuestionIds':[q['id'] for q in questions if r['spellId'] in q['spellIds']]} for r in records],'sourceFindings':['Erase Mind event/lookback and identity rider are undefined; no full-world history erasure is printed.','Feeblemind fixes actual INT/CHA scores to1, not modifiers. No initial save or named recovery is printed; its native Instantaneous duration must be reconciled with continuing restrictions.','Mass Dominate keeps up to3 actual CR<=10 creatures, WIS each turn and concentration minute; no guessed class-level-to-CR conversion or new finite-resource control.','Mind Ravel has exact last5minutes/WIS but no operational confusion lifetime; memory and control defenses/ending need separate treatment.','Disrupt Memory is accepted instantaneous firsthand loss with world-state preservation. Woven/Haze recovery remains pending and cannot silently become global.','Actual Dominate Person and Confusion complete native procedures and RNG/presentation scopes are supplied. Extending their named bridges requires specific concurrence.','Wizard prepared matrices, negative actual modifiers and Tinker controller prerequisites retain actual source timing; score changes are not automatic repertoire erasure or resource refunds.','Identity shaken is not a Unity Exposure, Corruption, alignment or cosmological identity change. No cosmology decision is made.'],'futureCaseRequirements':['At least two full deterministic cases per identity after choices, plus explicit independent branches for each consequential completion.','Erase Mind:known interval/unknown contents, event boundaries, overlap, later recalled older event, independent memory/rider protection, identity entitlement consumption and no world/resource rollback.','Feeblemind:actual score1/negative modifier, lawful underlying progression and competing score layers, Wizard preparation/cast/Ready/concentration timing, outgoing versus incoming communication, explicit device prerequisites, suppression and expiry without reset.','Mass Dominate:three distinct actual CR-qualified targets with separate saves/guards, real clocks, initial/current-turn timing, source-qualified companion budgets, instruction arbitration, failed replacement versus concentration commitment and independent cleanup.','Mind Ravel:real300second interval, private native confusion RNG, no initial duplicate save, independent hard-guard/memory defenses, confusion escape not memory restoration, no false memories or sixth DE4 presentation.','Hold any case whose required creature rating or event source remains absent; do not invent a profile or turn a conditional case into completed content.'],'earlierOperationalWorkedCases':[],'currentVectors':[],'gptCommunication':'Prepared while actual Part5 CompanionExact05 review remains live. Illusion repaired semantics have a separate actual acceptance; Exact13 rendering is queued. This new four-source conference has not been delivered or decided.','sourceBindings':list(sources.values()),'countsUnchanged':deepcopy(index['authoredCounts']),'newRuleAdoptions':0,'runtimeTestsExecuted':0,'humanPlaytests':0,'sourceInformationDeleted':0,'cosmologyDecisions':0,'wholeGameComplete':False}
    root.mkdir()
    frozen = []
    for b in sources.values():
        p = G/b['path']
        ck('Source unchanged '+b['path'],info(p) == b)
        dst = root/'sources'/b['path']
        dst.parent.mkdir(parents=True,exist_ok=True)
        dst.write_bytes(p.read_bytes())
        ck('Exact frozen source '+b['path'],dst.read_bytes() == p.read_bytes())
        frozen.append({**b,'frozenCopy':dst.relative_to(G).as_posix()})
    out.write_bytes(encoded(candidate))
    check.write_bytes(encoded({'candidate':info(out),'checks':checks,'checkCount':len(checks),'sourceCount':len(sources),'sourceIdentities':4,'placements':4,'earlierCompleteProcedures':0,'earlierOperationalWorkedCases':0,'newCurrentVectors':0,'questions':21,'riskCounts':{'C':4},'failures':0,'validationScope':'Source/access/hash/preservation and inherited-authority comparison only; no semantic adoption or runtime execution.'}))
    manifest = root/'MANIFEST.json'
    manifest.write_bytes(encoded({'candidate':info(out),'check':info(check),'files':list(sources.values()),'frozenSources':frozen,'sourceCount':len(sources),'newRuleAdoptions':0}))
    readme = 'Four exact rank8 memory/control sources and21 unselected questions. Read CANDIDATE.json and the full source files. All four are individually tierC. Exact accepted Disrupt Memory, Dominate Person, Confusion and other counterparts are supplied; pending memory2/control15/ward/control/companion comparisons grant no new authority. No external-game save, damage, recovery or rating is imported. No new procedure or case is adopted.\n'
    (root/'README.md').write_text(readme,encoding='utf8',newline='\n')
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        z.write(out,'CANDIDATE.json')
        z.write(check,'SOURCE_CHECK.json')
        z.write(manifest,'MANIFEST.json')
        z.writestr('README.md',readme)
        for b in sources.values():
            z.write(root/'sources'/b['path'],'sources/'+b['path'])
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist()) == len(set(z.namelist()))
        assert z.read('CANDIDATE.json') == out.read_bytes()
        for b in sources.values():
            assert z.read('sources/'+b['path']) == (G/b['path']).read_bytes()
    ab = info(archive)
    request.write_text(f'Review {archive.name}, {ab["bytes"]} bytes SHA256 {ab["sha256"]}. Four exact sources/placements,21 unselected questions and ten complete reviewed counterparts. Resolve Erase Mind episodic scope/identity rider; Feeblemind score1, spells, communication and recovery; Mass Dominate actual three CR<=10 targets and source-qualified control; Mind Ravel300second forgetting and native confusion. Preserve every printed benefit and actual Wizard/Cleric access. Inherit accepted interfaces within their scope, label all consequential new choices, preserve pending comparisons and absent-content holds. Return per-question decisions and source-specific next authoring directions; no unseen procedure, runtime, balance, cosmology or whole-game approval.\n',encoding='utf8',newline='\n')
    prep.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PREPARED_UNSENT','candidate':info(out),'archive':ab,'manifest':info(manifest),'check':info(check),'request':info(request),'sourceCount':len(sources),'identityCount':4,'placementCount':4,'questionCount':21,'riskCounts':{'C':4},'allArchiveMembersVerified':True,'newRuleAdoptions':0,'sourceInformationDeleted':0}))
    print(json.dumps({'preparation':info(prep),'candidate':info(out),'archive':ab,'sources':len(sources),'checks':len(checks),'questions':21,'failures':0}))


if __name__ == '__main__':
    main()
