"""Build the complete post-conference persistent20 exact authored candidate; no adoption."""
from copy import deepcopy
from datetime import datetime,timezone
import hashlib,json,zipfile
from apply_di7_ap_as_01 import G,R,A,info,encoded
from prepare_ac5_current_interfaces_01 import at
from package_damage_control25_exact_09 import render,strings


def main():
    root=A/'persistent-damage20-exact-rebound-07';archive=A/'DD_Persistent_Damage_20_Exact_Rebound_07.zip'
    prep=A/'PERSISTENT_DAMAGE_20_EXACT_REBOUND_07_PREPARATION.json';request=A/'PERSISTENT_DAMAGE_20_EXACT_REBOUND_07_REQUEST.txt';check=A/'PERSISTENT_DAMAGE_20_EXACT_REBOUND_07_CHECK.json'
    assert all(not p.exists() for p in [root,archive,prep,request,check])
    source=R/'data/director/spell_proposals/persistent_damage_20_current_07.json';d=json.loads(source.read_bytes())
    reviewp=A/'persistent-damage20-conference-06-review/REVIEW.json';review=json.loads(reviewp.read_bytes())
    returned=A/'PERSISTENT_DAMAGE_20_CONFERENCE_06_RECEIPT.json';replayp=A/'PERSISTENT_DAMAGE_20_CURRENT_07_REPLAY_CHECK.json';replay=json.loads(replayp.read_bytes())
    localp=A/'PERSISTENT_DAMAGE_20_CURRENT_07_LOCAL_DELTAS.json';local=json.loads(localp.read_bytes())
    checks=[];buffers={};paths={}
    def ck(n,v):checks.append({'name':n,'passed':bool(v)});assert v,n
    def put(n,b):assert n not in buffers;buffers[n]=b
    def planned(n):return {'name':n,'bytes':len(buffers[n]),'sha256':hashlib.sha256(buffers[n]).hexdigest()}
    ck('Candidate matches exact replay receipt',info(source)==replay['candidate'])
    ck('Actual conference returned20 procedure and24 question dispositions',len(review['procedureDispositions'])==20 and len(review['questionDispositions'])==24)
    ck('Nine operations verified forward and reverse',replay['nineOperations']==9 and replay['forwardAndReverseReplayVerified'] and replay['failures']==0)
    catalogp=R/'data/public/spell_playtests/catalog.json';catalog=json.loads(catalogp.read_bytes());catalogbyid={s['id']:s for s in catalog['spells']}
    for s in d['spells']:ck('Exact existing source/access '+s['id'],s['completeSourceAndAccess']==catalogbyid[s['id']])
    groups=['currentExamples','currentSupplementalExamples','adversarialVectors04'];cases=[deepcopy(c) for k in groups for c in d[k]]
    ck('57 distinct current cases',len(cases)==len({c['id'] for c in cases})==57)
    ck('40 original texts retained',len(d['originalExamplesUnchanged'])==40)
    model={'schemaVersion':'1.0','moduleId':'PERSISTENT-DAMAGE20-EXACT07','status':'PENDING actual exact authored acceptance; video game only','candidate':info(source),'sharedRules':deepcopy(d['sharedRules']),'spells':deepcopy(d['spells']),'sharedContractRouting':deepcopy(d['sharedContractRouting06']),'fullCurrentCounterparts':deepcopy(d['fullCounterparts06']),'iceStormMixedDefenseOption':deepcopy(d['iceStormMixedDefenseOption04']),'actualConferenceReceipt':info(returned),'actualFullConferenceReview':info(reviewp),'actualProcedureDispositions':deepcopy(review['procedureDispositions']),'actualQuestionDispositions':deepcopy(review['questionDispositions']),'historicalStatusRouting':'Preserved source/proposal status and remainingDecisions fields record their earlier authorship. Actual Conference06 dispositions above control what was jointly discussed; only the complete Current07/current artifact set is now offered for exact acceptance. No local case repair has actual GPT concurrence yet.','localCaseRepairs':info(localp),'runtimeSelectionEnabled':False,'runtimeImplemented':False,'runtimeTestsExecuted':0,'newRuleAdoptions':0,'humanPlaytested':False,'numericalBalanceApproved':False,'cosmologyCanonModified':False,'sourceInformationDeleted':0}
    casebook={'id':'PERSISTENT-DAMAGE20-CASEBOOK07','status':'Authored cases with explicit conditional/composition limits; zero executed runtime tests','cases':cases,'categories':[{'sourceArray':k,'count':len(d[k]),'ids':[c['id'] for c in d[k]]} for k in groups],'originalExamplesUnchanged':deepcopy(d['originalExamplesUnchanged']),'completeLocalBeforeAfter':deepcopy(local),'actualNineOperationSource':info(A/'persistent-damage20-conference-06-review/PROPOSED_CORRECTIONS.json'),'runtimeTestsExecuted':0,'sourceInformationDeleted':0}
    base='# Persistent damage spells — proposed video game rules\n\n**Pending exact authored acceptance.** Twenty existing spell identities retain their original access. The full source-specific procedures below include the actual conference corrections. Runtime and balance remain separate.\n\n## Shared procedures\n\n'+render(d['sharedRules'])
    for s in d['spells']:
        base+='## '+s['name']+'\n\n| Class | School | Rank | Minimum class level | Base RP |\n|---|---|---:|---:|---:|\n'
        for cl,a in s['completeSourceAndAccess']['classAccess'].items():base+=f"| {cl} | {a['school']} | {a['rank']} | {a['minimumClassLevel']} | {a['baseRpCost']} |\n"
        base+='\n'+s['procedure']+'\n\n### Damage ownership and continuing effects\n\n'+render(s['damageRootProposal'],4)
    player=base+'## Scope\n\nThese procedures do not grant their conditional counterpart spells, unprinted creature abilities, public access to hidden dice, additional Fate presentations, material economies or cosmology. All earlier sources and scenarios remain preserved.\n'
    director=base+'## Actual conference dispositions\n\n'+render(review['procedureDispositions'])+render(review['questionDispositions'])+'## Local changes awaiting concurrence\n\n'+render(d['conference06Application07'])+'## Complete current cases\n\n'
    for c in cases:director+='### '+c['id']+'\n\n```json\n'+json.dumps(c,ensure_ascii=False,indent=2)+'\n```\n\n'
    director+='## All original scenarios, unchanged\n\n```json\n'+json.dumps(d['originalExamplesUnchanged'],ensure_ascii=False,indent=2)+'\n```\n'
    for name,text in [('PLAYER_CHAPTER.md',player),('DIRECTOR_REVIEW.md',director)]:
        for s in d['spells']:
            ck(name+' full procedure '+s['id'],s['procedure'] in text)
            for leaf in strings(s['damageRootProposal']):ck(name+' source root '+s['id'],leaf in text)
        for key,value in d['sharedRules'].items():
            for leaf in strings(value):ck(name+' shared '+key,leaf in text)
    put('SPELLS_MODEL.json',encoded(model));put('CASEBOOK.json',encoded(casebook));put('PLAYER_CHAPTER.md',player.encode());put('DIRECTOR_REVIEW.md',director.encode())
    oldmanifestp=A/'persistent-damage-20-conference-06/MANIFEST.json';oldmanifest=json.loads(oldmanifestp.read_bytes())
    for b in oldmanifest['files']:
        p=G/b['path'];ck('Exact previous full source '+b['path'],info(p)==b);paths[p]=b
    for p in [source,catalogp,reviewp,returned,replayp,localp,oldmanifestp,R/'tools/apply_persistent20_conference06_to_draft07.py',R/'tools/package_persistent20_exact_07.py',R/'docs/mechanics/classes/warrior.md',R/'docs/mechanics/CHARACTER_CREATION_PLAYTEST.md',R/'docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md',R/'data/public/spell_playtests/authored_review_index.json']:
        paths[p]=info(p)
    for p in (A/'persistent-damage20-conference-06-review').iterdir():
        if p.is_file():paths[p]=info(p)
    pointers=[]
    def walk(v,caseid):
        if isinstance(v,dict):
            if isinstance(v.get('path'),str) and isinstance(v.get('pointer'),str) and v['pointer'].startswith('/'):
                p=G/v['path']
                if p.is_file() and p.suffix.lower()=='.json':
                    at(json.loads(p.read_bytes()),v['pointer']);pointers.append({'caseId':caseid,'path':v['path'],'pointer':v['pointer']});paths[p]=info(p)
            for x in v.values():walk(x,caseid)
        elif isinstance(v,list):
            for x in v:walk(x,caseid)
    for c in cases:walk(c,c['id'])
    put('SOURCE_HASHES.json',encoded({'bindings':[b for p,b in sorted(paths.items(),key=lambda x:x[1]['path'])],'scope':'Complete raw source bytes, actual returned review and reversible correction evidence; no source-only dependency becomes approved.'}))
    register={'id':'PERSISTENT-DAMAGE20-EXACT07-REGISTER','status':'PENDING actual exact acceptance; no adoption','candidate':info(source),'spellIds':[s['id'] for s in d['spells']],'placementCount':sum(len(s['completeSourceAndAccess']['source']['original']['placements']) for s in d['spells']),'originalScenarios':40,'currentCases':57,'existingPriorCaseIds':55,'newConferenceCases':2,'actualConferenceReceipt':info(returned),'actualReplayReceipt':info(replayp),'localCorrectionsRequiringConcurrence':['P20-X05: actual Ranger Beast HP-only, immediate ordinary death and bond ending; no ordinary Wound or death save.','EV6-03-B: GPT suppressor overlapped the mortar. Ccenter[20,-11,3], fieldpoint[20,-2,2.5] are clear, within10ft, cover entire mortar and keep hostile caster6ft from it for the later ranged shot.','P20-C07-02: source-derived Warrior d12 HP105 is correct; add explicit12+3+9*(7+3) derivation without numeric change.'],'applicationPlan':{'preconditions':'Actual GPT exact acceptance of all eight supplied files, then independent preservation/current-membership checks before any byte-identical copy.','canonicalByteCopies':{'SPELLS_MODEL.json':'DescentReviewChanges/ReviewBible/data/public/spell_candidates/persistent_damage_20_reviewed_07.json','CASEBOOK.json':'DescentReviewChanges/ReviewBible/data/playtest/spell_candidates/persistent_damage_20_cases_07.json','PLAYER_CHAPTER.md':'DescentReviewChanges/ReviewBible/docs/spells/candidates/PERSISTENT_DAMAGE_20_REVIEWED_07.md','DIRECTOR_REVIEW.md':'DescentReviewChanges/ReviewBible/docs/director-only/spells/PERSISTENT_DAMAGE_20_REVIEWED_07.md'},'membership':'Add only these20 still-pending identities after actual acceptance. Recompute from actual live index at application time: this frozen snapshot is480 reviewed/368 pending/204 standalone; applying only this cohort would be500/348/224. A separately accepted/applied cohort changes the real baseline and cannot be ignored. No blind hardcoded counter overwrite.','acceptedSources':'No source catalog, AC5/AC6/DE4 guide or unrelated procedure rewrite. Registry/discovery updates require their own explicit byte-preserving application evidence.','runtimeSelectionEnabled':False},'newRuleAdoptions':0,'sourceInformationDeleted':0}
    ck('21 actual printed placements',register['placementCount']==21);put('REGISTER.json',encoded(register))
    notes='''# Persistent20 local exact-review notes

The actual GPT Conference06 review, assistant0d6f943a-dd04-4129-9af8-cab561c62fc8, is preserved with its verified117073-byte return archive. All nine proposed operations replay exactly to the supplied canonical checksum and reverse to Current06. The current candidate adds complete Freezing Rain contact-loss timing, Ice-Storm-only mixed-defense selection/allocation, a consistent Enervation continuing-creature predicate, complete mortar Ready timing, corrected real Storm bodies and two new operating cases. All20 root mappings and24 question dispositions are supplied in full; none is inferred from a summary.

Three local changes need actual concurrence. P20-X05 had retained an ordinary Wound roll on the actual HP-only Ranger Beast despite the review noticing that exception; its full corrected case now preserves ordinary death/corpse/bond and Null Disabled separately. The returned mortar fixture placed its suppressing caster inside the new cannon. Current07 moves that caster to[20,-11,3] and the fieldpoint to[20,-2,2.5]; center range squared81.25<100, all cannon corners at most32.75<100, and actual caster/cannon body gap6ft avoids accidental ranged close quarters. All paid Ready/cast/command/shot/expiry obligations survive. Warrior10 CON16 HP105 needs no numeric correction: d12 first15 plus nine fixed10 gains gives105; its exact source derivation is now explicit.

The full before/after local delta preserves all earlier values. Forty original scenarios and55 prior current IDs remain; two new GPT supplements bring the casebook to57. Conditional travel, supplied damage, missing bestiary or pending source branches remain limited authored compositions. No runtime, human playtest, numerical balance, cosmology, general environment rule or75-domain closure is claimed. The acceptance request concerns the eight current files only; no unseen later index/registry bytes are preapproved.
''';put('LOCAL_REVIEW_NOTES.md',notes.encode())
    put('EVIDENCE_MANIFEST.json',encoded({'id':'PERSISTENT-DAMAGE20-EXACT07-MANIFEST','files':[planned(n) for n in sorted(buffers)],'selfHashConvention':'The seven companion files are bound here; outer preparation binds this manifest.','pendingActualExactAcceptance':True}))
    root.mkdir()
    for n,b in buffers.items():(root/n).write_bytes(b)
    check.write_bytes(encoded({'candidate':info(source),'checks':checks,'checkCount':len(checks),'failureCount':0,'sourcePointerChecks':pointers,'sourcePointerCount':len(pointers),'fullSources':len(paths),'currentCases':57,'newRuleAdoptions':0,'runtimeTestsExecuted':0}))
    readme='''# Persistent20 exact rebound07

Read current/REGISTER.json and LOCAL_REVIEW_NOTES.md, then the complete model, casebook and both manuscripts. Source files include all69 original conference authorities, actual final review and every full correction. Current07 includes the exact nine GPT operations and three explicitly separate local source/geometry/evidence repairs. All20 complete procedures,21 placements,40 original scenarios,57 current cases and24 actual question dispositions are supplied.

Confirm the full rule/source flow and local repairs. If coherent, return exact bounded authored acceptance of all EIGHT current files, each actual name/bytes/SHA256. Otherwise supply minimal complete before/after corrections with exact pointers and preserve history. Do not approve unseen future membership/registry payloads or unrelated pending sources. All declared hypothetical/composition branches remain limited evidence, not completed game executions. No runtime, gameplay, balance, cosmology, domain closure or release approval is requested.
''';(root/'README.md').write_text(readme,encoding='utf8',newline='\n')
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        z.write(root/'README.md','README.md');z.write(check,'LOCAL_ARTIFACT_CHECK.json')
        for n in sorted(buffers):z.write(root/n,'current/'+n)
        for p,b in sorted(paths.items(),key=lambda x:x[1]['path']):z.write(p,'sources/'+b['path'])
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for n,b in buffers.items():assert z.read('current/'+n)==b
        for p,b in paths.items():assert z.read('sources/'+b['path'])==p.read_bytes()
    b=info(archive);request.write_text(f'Please review {archive.name} ({b["bytes"]} bytes; SHA256 {b["sha256"]}) for exact bounded authored acceptance of persistent20. Your actual Conference06 nine operations replayed/reversed exactly. All20 full procedures,21 placements,40 originals,55 preserved current IDs plus2 new cases and24 actual dispositions are supplied, with eight current artifacts. Three explicit local changes need concurrence: Ranger Beast P20-X05 no ordinary Wound/death-save, mortar suppressor moved off cannon to[20,-11,3] with field[20,-2,2.5] and6ft body gap, and correct Warrior10/CON16 HP105 derivation. All full before/after objects survive. If coherent return ACCEPT_BYTE_IDENTICAL_FOR_PROVISIONAL_AUTHORED_PERSISTENT_DAMAGE20_VIDEO_GAME_CANDIDATE with exact name/bytes/SHA256 for all eight files; otherwise minimal complete corrections. No unseen future integration, unrelated source adoption, hidden-RNG expansion, runtime, balance, cosmology or75-domain closure.\n',encoding='utf8',newline='\n')
    prep.write_bytes(encoded({'archive':b,'candidate':info(source),'currentFiles':[info(root/n) for n in sorted(buffers)],'sourceCount':len(paths),'artifactCheck':info(check),'request':info(request),'allArchiveMembersVerified':True,'status':'Prepared UNSENT. Actual companion/life10 review active; queue for subsequent GPT review.','newRuleAdoptions':0,'runtimeTestsExecuted':0}))
    print(json.dumps({'archive':b,'currentFiles':len(buffers),'sources':len(paths),'checks':len(checks),'sourcePointers':len(pointers),'preparation':info(prep)}))


if __name__=='__main__':main()
