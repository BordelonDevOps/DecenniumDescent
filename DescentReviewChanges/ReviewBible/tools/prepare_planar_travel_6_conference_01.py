"""Prepare six travel source decisions after verified push, with no rule adoption."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json, zipfile
from apply_di7_ap_as_01 import G, R, A, info, encoded
from prepare_ac5_current_interfaces_01 import at
from planar_travel_6_questions_01 import IDS, TIERS, Q

def read(p): return json.loads(p.read_bytes())

def main():
    root = A / 'planar-travel6-source-conference-01'
    out = R / 'data/director/spell_review/planar_travel_6_source_conference_01.json'
    check = A / 'PLANAR_TRAVEL_6_SOURCE_CONFERENCE_01_CHECK.json'
    prep = A / 'PLANAR_TRAVEL_6_SOURCE_CONFERENCE_01_PREPARATION.json'
    request = A / 'PLANAR_TRAVEL_6_SOURCE_CONFERENCE_01_REQUEST.txt'
    archive = A / 'DD_Planar_Travel_6_Source_Conference_01.zip'
    assert not any(p.exists() for p in [root, out, check, prep, request, archive])
    sources = {}; checks = []
    def ck(n,v):
        checks.append({'check': n, 'passed': bool(v)}); assert v,n
    def bind(p):
        b = info(p); sources[b['path']] = b; return b
    cp = R/'data/public/spell_playtests/catalog.json'; ip = cp.parent/'authored_review_index.json'
    qp = R/'data/director/spell_review/remaining_work_queue_11.json'
    rp = R/'data/director/spell_review/accepted_interface_registry_06.json'
    pp = R/'data/director/cosmology/planes_reviewed_01.json'
    pushp = G/'docs/audit/2026-10-18/github-snapshot-damage25/PUSH_RECEIPT.json'
    lp = cp.parent/'candidate_low_rank_136.json'
    bp = R/'data/playtest/spell_drafts/low_rank_137_authored_boundaries.json'
    catalog,index,queue,registry,planes,push,low,boundaries = map(read,[cp,ip,qp,rp,pp,pushp,lp,bp])
    ck('Verified push precedes careful conference', push['commit']==push['remoteMain']=='3ece00cad106dfda0b86a6e84630b3d3e3253e1e' and push['trackedEntriesDeleted']==0)
    ck('Current membership remains525/323', index['authoredCounts']=={'reviewed':525,'pending':323})
    ck('Current173 scoped interfaces', len(registry['entries'])==173)
    for p in [cp,ip,qp,rp,pp,pushp,lp,bp,Path(__file__),Path(__file__).with_name('planar_travel_6_questions_01.py'),R/'rulebook_output.txt']:bind(p)
    originals = dict(zip(IDS,['REMAINING_RANK3_SPELL_SOURCE_PREPARATION.json','TRANSMUTATION_UNIVERSAL_RANK4_SOURCE_PREPARATION.json','UNIVERSAL_RANK5_SOURCE_PREPARATION.json','ILLUSION_NECROMANCY_RANK7_SOURCE_PREPARATION.json','ABJURATION_CONJURATION_RANK7_SOURCE_PREPARATION.json','TRANSMUTATION_UNIVERSAL_RANK7_SOURCE_PREPARATION.json']))
    lines = (R/'rulebook_output.txt').read_text('utf-16').splitlines(); records=[]
    for ident in IDS:
        originalp=A/originals[ident];original=read(originalp);bind(originalp)
        n=next(n for n,s in enumerate(original['selectedSpells']) if s['spellId']==ident);old=original['selectedSpells'][n]
        card=next(s for s in catalog['spells'] if s['id']==ident);row=next(s for s in queue['rows'] if s['id']==ident);entry=next(e for e in index['entries'] if e['id']==ident)
        ck('Unchanged source and access '+ident, old['fullSourceAndCurrentAccessRecord']==card==row['completeCurrentSourceAndAccess'])
        ck('No earlier full procedure '+ident, row['currentGroup'] is None and not row['previousAuthoringMapRowUnchanged']['completeEarlierProposalRecords'])
        ck('Pending or receipt identity '+ident, entry['authoredStatus']==('receipt-only-post-push-cosmology' if ident=='blink' else 'pending-authored-procedure'))
        bb=[deepcopy(b) for b in original['currentBookBindings'] if b['spellId']==ident]
        ck('Every school placement preserved '+ident,len(bb)==len(card['source']['original']['placements']))
        for b in bb:ck('Current book exact line '+ident+' '+str(b['currentBookRow']['line']),lines[b['currentBookRow']['line']-1]==b['currentBookRow']['exactText'])
        for k in ['catalog','core']:ck('Underlying full source '+ident+k,bind(R/card['source'][k+'Path'])['sha256']==card['source'][k+'Sha256'])
        records.append({'spellId':ident,'riskTier':TIERS[ident][0],'riskReason':TIERS[ident][1],'completeCurrentCatalogSourceAndAccess':deepcopy(card),'currentIndexEntry':deepcopy(entry),'originalQuestionSource':info(originalp),'originalQuestionPointer':f'/selectedSpells/{n}','completeOriginalSourceQuestionUnchanged':deepcopy(old),'completeHistoricalCommonQuestionUnchanged':original['commonOperationalQuestion'],'completeHistoricalScopeExceptionUnchanged':original['commonQuestionException'],'completeCurrentBookBindings':bb,'earlierCompleteProcedures':[],'earlierOperationalWorkedCases':[],'historicalReceiptCases':[],'status':'Source conference prepared, no procedure/case adoption.'})
    blink=next(s for s in low['spells'] if s['id']=='blink');bn=next(n for n,c in enumerate(boundaries['cases']) if c.get('authoredExpectation',{}).get('spellId')=='blink')
    records[0]['completeExistingReceiptUnchanged']={'source':info(lp),'pointer':'/spells/'+str(low['spells'].index(blink)),'record':deepcopy(blink)}
    records[0]['historicalReceiptCases']=[{'source':info(bp),'pointer':f'/cases/{bn}','completeCase':deepcopy(boundaries['cases'][bn])}]
    ck('Blink existing receipt remains null/unavailable',blink['operationalCandidate'] is None and blink['selectionEnabled'] is False)
    # Preserve original manuscripts and saved website, separately from current review annotations.
    original_paths=['The Cosmology of Decennium Descent.docx','The Decennium Descent and the Matrix of Oblivion.docx','The_World_of_Aethel_Lore.docx','books/player/Decennium_Descent_Player_Rulebook_v6.docx','docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx','docs/mechanics/OWNER_COSMOLOGY_LOCKS_2026-07-30.md','docs/mechanics/APPENDIX_B_FOLK_RELIGION.md','webpage.html','src/data/cosmology-lore.json']
    original_proofs=[]
    for path in original_paths:
        prior=next(b for b in planes['sourceBindings'] if b['path']==path);actual=bind(G/path)
        ck('Original planes source unchanged '+path,actual==prior);original_proofs.append({'priorReviewedBinding':prior,'currentBinding':actual})
    for p in [G/planes['localVerification']['path'],G/planes['reviewArchive']['path'],A/'COSMOLOGY_PLANES_SOURCE_CONCORDANCE_01.json',A/'COSMOLOGY_PLANES_TRANSIT_DEPENDENCY_READING_01.json',A/'COSMOLOGY_PLANES_REVIEWED_COUNTERPART_READING_01.json',A/'COSMOLOGY_PLANES_DIRECTOR_AND_RECEIPT_READING_01.json',A/'COSMOLOGY_SAVED_WEBSITE_SOURCE_CHECK_01.json',A/'LOW_RANK_136_EXACT_FULFILLMENT.json',R/'data/public/Decennium_Descent_Bard_Playtest_v0_1.json',R/'data/public/expedition_candidate/complete_candidate.json',R/'data/playtest/equipment_acquisition_candidate.json',R/'docs/canon/PLAYER_DIRECTOR_BOUNDARY.md']:
        bind(p)
    for name in ['CURRENT_COSMOLOGY_READ_FIRST.md','PLANES_REVIEWED_01.md','HEARTCELL_OWNER_UPDATE_02.md','OWNER_RECONCILIATION_REVIEWED_01.md','Q6_LATER_LOCK_REVIEWED_01.md','SOULS_RESEARCH_REVIEWED_01.md','CHRONOLOGY_SOURCE_REVIEWED_01.md']:
        bind(R/'docs/director-only/cosmology'/name)
    for name in ['heartcell_owner_update_02.json','q6_later_lock_reviewed_01.json']:bind(R/'data/director/cosmology'/name)
    for name in ['wizard','cleric','druid','mage','shaman','mirrorsage','tinker','paladin','monk','thief','crimson-agent']:bind(R/f'data/public/class_playtests/{name}.json')
    for name in ['VIDEO_GAME_ONLY_DIRECTIVE.md','CLASS_PLAYTEST_RULES.md','SPELL_INTEGRATION_RULES.md','COMBAT_ACTION_PLAYTEST.md','CORE_RESOLUTION_PLAYTEST.md','CONDITIONS_PLAYTEST.md','CONTROL_STATES_PLAYTEST.md','BODY_EQUIPMENT_PLAYTEST.md','CREATURE_LIFECYCLE_PLAYTEST.md','DEVICE_LIFECYCLE_PLAYTEST.md','HEALING_DEATH_PLAYTEST.md','CHARACTER_CREATION_PLAYTEST.md']:
        bind(R/'docs/mechanics'/name)
    inherited=[]
    for n in [0,1,2,3,4,7,8,11,12,13,14,22,28,30,32,33,36,38,39,40,42,43,44,45,46,47,48,56,57,59,60,65,66,67,68,77]:
        e=registry['entries'][n];b=e['currentAuthoritativeSource'];actual=bind(G/b['path'])
        ck('Accepted interface source '+str(n),all(actual[k]==b[k] for k in ['bytes','sha256']))
        inherited.append({'registryPointer':f'/entries/{n}','completeEntryUnchanged':deepcopy(e),'scopeLimit':'Reuse exact accepted scope only; spell-specific transport classifications and terminal exceptions are not global permissions.'})
    counterparts=[]
    for ident in ['faction-portal','alignment-portal','banishment','dimensional-anchor','planar-protection','planar-barrier','forbiddance','arcane-portal','planar-window','blink-step','antimagic-field-lesser','greater-dispel','alignment-nexus']:
        e=next(e for e in index['entries'] if e['id']==ident);ck('Reviewed counterpart '+ident,e['authoredStatus']=='reviewed-authored-operational-playtest')
        path=(ip.parent/e['procedureFile']).resolve();doc=read(path);ptr=e.get('wholeCardPointer',e['procedurePointer'])
        counterparts.append({'spellId':ident,'source':bind(path),'pointer':ptr,'completeCurrentCard':deepcopy(at(doc,ptr)),'completeSharedRules':deepcopy(doc.get('sharedRules',{})),'indexEntry':deepcopy(e)})
    questions=[{'id':i,'spellIds':ids,'exactSourceOrConflict':src,'options':opts,'recommendationAndConsequences':rec,'decisionSelected':False} for i,ids,src,opts,rec in Q]
    ck('17 unique explicit questions',len(questions)==len({q['id'] for q in questions})==17)
    ck('All6 identities have questions',set().union(*(set(q['spellIds']) for q in questions))==set(IDS))
    ck('Six identities eight placements',len(records)==6 and sum(len(r['completeCurrentBookBindings']) for r in records)==8)
    risk=dict(Counter(r['riskTier'] for r in records));ck('Per-spell risk5C1B',risk=={'C':5,'B':1})
    candidate={'id':'PLANAR-TRAVEL-6-SOURCE-CONFERENCE-01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'POST_PUSH_SOURCE_CONFERENCE_PREPARED_UNSENT','developmentDirection':'video-game-only','records':records,'currentAcceptedInterfaceComparisons':inherited,'completeAcceptedCounterparts':counterparts,'questions':questions,'riskCounts':risk,'semanticDelta':[{'spellId':r['spellId'],'riskTier':r['riskTier'],'riskReason':r['riskReason'],'startingPoint':'Full original source only; Blink additionally retains its nonoperative receipt boundary. No historical operational procedure is invented.','genuineQuestionIds':[q['id'] for q in questions if r['spellId'] in q['spellIds']]} for r in records],'cosmologyAuthority':{'currentPlanesReference':info(pp),'completeQualifiedRegisterUnchanged':deepcopy(planes['register']),'completeCurrentQualificationUnchanged':deepcopy(planes['currentQualification']),'originalSourceProofs':original_proofs,'verifiedPriorPush':info(pushp),'interpretation':'Read originals with explicit owner corrections first. The planes register is a dated source review: its old pending Banishment statement is superseded only by the separately supplied exact accepted Banishment source. Other old labels are history, not present approval. No master topology, public revelation, campaign epoch, planar-time engine or missing entity identity is adopted here. The full saved website is included as its own authored presentation.'},'originalOperationalWorkedCases':[],'historicalReceiptCaseCount':1,'currentVectors':[],'futureCaseRequirements':['At least two full current operational cases per actual accessible spell profile, with all genuine branches. Preserve the existing Blink receipt case alongside new cases.','Complete actual caster, access, repertoire, resources, components, counters, Dissonance/Refrain and source-specific class hooks; actual bodies, cargo, loads, occupied volumes, support and complete chronology.','Actual registered place/endpoint and geometry evidence; any missing named-plane relationship is a declared conditional prerequisite, not an invented map.','Exercise distinct transport predicates, known/hidden failure, moving/occupied target space, expiry equality, suppression/return and inherited effects without duplication or replay.','No runtime, human-playtest, balance or full-domain completion claim from authored arithmetic or source checks.'],'countsUnchanged':deepcopy(index['authoredCounts']),'sourceBindings':list(sources.values()),'newRuleAdoptions':0,'runtimeTestsExecuted':0,'humanPlaytests':0,'newCosmologyDecisions':0,'sourceInformationDeleted':0}
    # Freeze only after preflight and all original/source comparisons pass.
    root.mkdir();frozen=[]
    for b in sources.values():
        path=G/b['path'];ck('Source unchanged '+b['path'],info(path)==b);dst=root/'sources'/b['path'];dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(path.read_bytes())
        ck('Frozen equality '+b['path'],dst.read_bytes()==path.read_bytes());frozen.append({**b,'frozenCopy':dst.relative_to(G).as_posix()})
    out.write_bytes(encoded(candidate))
    check.write_bytes(encoded({'candidate':info(out),'checks':checks,'checkCount':len(checks),'sourceCount':len(sources),'sourceIdentities':6,'placements':8,'earlierCompleteProcedures':0,'earlierOperationalWorkedCases':0,'historicalReceiptCases':1,'newCurrentVectors':0,'questions':17,'riskCounts':risk,'failures':0,'validationScope':'Source, exact authority, access, book binding and preservation only; no semantic acceptance or executed gameplay.'}))
    (root/'MANIFEST.json').write_bytes(encoded({'candidate':info(out),'check':info(check),'files':list(sources.values()),'frozenSources':frozen,'sourceCount':len(sources),'newRuleAdoptions':0}))
    (root/'README.md').write_text('# Six travel spells: source conference\n\nRead all six complete source records, eight school placements, seventeen new questions, thirteen full accepted counterparts and current scoped interfaces. This follows a verified preservation push and the existing carefully qualified planes review. It does not reopen source authority or promote the mortal Wheel, saved website or operational plane keys into a universal cosmology. Original manuscripts and the saved website are present.\n\nFive records have individually justified tier C risk; Teleport is tier B. Preserve every original question and the nonoperative Blink receipt/case. There are no earlier complete operational procedures or new current cases for this cohort. Return complete source-linked proposed procedures, per-question dispositions and explicit missing-content holds; author actual complete cases only after the design choices are settled.525 reviewed /323 pending remain unchanged. Old reference counts/statuses are history; the live index and exact receipts control. No source deletion, game-wide interface expansion, runtime/balance/human/cosmology/campaign-epoch or75-domain closure.\n',encoding='utf8',newline='\n')
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in ['README.md','MANIFEST.json']:z.write(root/name,name)
        z.write(out,'CANDIDATE.json');z.write(check,'PREFLIGHT.json')
        for b in frozen:z.write(G/b['frozenCopy'],'sources/'+b['path'])
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and z.read('CANDIDATE.json')==out.read_bytes()
        for b in frozen:assert z.read('sources/'+b['path'])==(G/b['frozenCopy']).read_bytes()
    b=info(archive)
    request.write_text(f'Please conduct the six-spell post-push travel source conference using {archive.name}, {b["bytes"]} bytes, SHA256 {b["sha256"]}. Read all six full sources, eight placements,17 explicit new questions, current accepted interfaces and full original cosmology manuscripts with owner corrections. Five individually assessed tier C spells and one tier B; no blanket risk classification. Preserve Blink\'s old null receipt and receipt case. Return complete proposed procedures, exact question dispositions, provenance and genuine missing-content holds. Do not infer old pending labels override newer exact accepted sources, or a prior push/planes review approves these spells. No master topology, public revelation, identity/epoch decision, global clock exception, source deletion or acceptance is inferred.525/323 membership remains unchanged.\n',encoding='utf8',newline='\n')
    prep.write_bytes(encoded({'archive':b,'candidate':info(out),'manifest':info(root/'MANIFEST.json'),'check':info(check),'request':info(request),'sourceCount':len(sources),'allArchiveSourcesVerified':True,'riskCounts':risk,'status':'Prepared UNSENT; no actual GPT decision on this packet yet.','newRuleAdoptions':0}))
    print(json.dumps({'archive':b,'candidate':info(out),'sources':len(sources),'checks':len(checks),'questions':17,'riskCounts':risk,'operationalCases':0,'historicalReceiptCases':1}))

if __name__=='__main__':main()
