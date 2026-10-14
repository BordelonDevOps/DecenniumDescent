"""Record the worksheet draft and current spell queue; preserve reviewed inputs."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re,shutil,subprocess,sys
R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(G).as_posix()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    receipt=A/'LANGUAGE_WORKSHEET_PREPARATION.json';assert not receipt.exists()
    worksheet=R/'docs/playtest/CHARACTER_LANGUAGE_WORKSHEET.md'
    contract_path=R/'data/playtest/language_communication_candidate_public.json'
    contract=read(contract_path);assert contract['exactLanguageApproval']
    body=worksheet.read_text(encoding='utf-8')
    links=[]
    for link in re.findall(r'\]\(([^)]+)\)',body):
        if '://' in link:continue
        target=(worksheet.parent/link.partition('#')[0]).resolve();assert target.is_file();links.append(rel(target))
    sections={'competency':'1. Languages and modes','choice':'2. Language choices','temporaryEffect':'3. Temporary communication and current restrictions',
              'learning':'4. Learning and literacy','textEvidence':'5. Texts, translations and evidence','scribingLedger':'6. Language Insight',
              'communicationEvent':'7. Communication when order matters','provenance':'8. Source record kept with the sheet'}
    assert set(sections)==set(contract['recordSchema']['definitions'])
    field_map=[]
    for name,title in sections.items():
        assert '## '+title in body
        definition=contract['recordSchema']['definitions'][name]
        field_map.append({'contractDefinition':name,'worksheetSection':title,'sourceRequiredFields':definition['required'],'sourceDeclaredFields':list(definition['fields']),
                          'conditionalValueRulePreserved':name=='provenance','scope':'Paper record corresponding to the reviewed contract; no new runtime schema'})
    protected=[contract_path,R/'data/director/language_communication_candidate_internal.json',R/'docs/mechanics/LANGUAGE_COMMUNICATION_PLAYTEST.md',
               R/'docs/mechanics/LANGUAGE_REVIEW_STATUS.json',R/'docs/playtest/FIRST_BARD_WALKTHROUGH.md',R/'docs/playtest/ONBOARDING_REVIEW_STATUS.json',
               R/'docs/mechanics/CHARACTER_CREATION_PLAYTEST.md',R/'docs/mechanics/ANCESTRY_BACKGROUND_PLAYTEST.md',R/'docs/mechanics/EQUIPMENT_ACQUISITION_PLAYTEST.md']
    protected_hashes={rel(p):sha(p) for p in protected}
    active=read(A/'LOW_RANK_SPELL_FILE_HANDOFF_V3_PREPARATION.json')['currentFileHashes']
    assert all(sha(G/p)==h for p,h in active.items())
    report={'preparedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'Authored worksheet draft; presentation not jointly reviewed; UNSENT',
            'worksheet':rel(worksheet),'worksheetSha256':sha(worksheet),'governingReview':'LAX-EXACT-2026-10-11 fulfilled',
            'definitionToFormMap':field_map,'localLinks':links,'protectedInputs':protected_hashes,
            'contentChecks':['Eight existing record definitions have corresponding forms','Actual absent/null/value distinction retained','All local worksheet links resolve','Mira example retains only Human Common/chosen Dwarvish; Nomadic and Battlefield Medic add no language','Original language/candidate/source/runtime files unchanged'],
            'scopeLimit':'Field coverage and link checks are documentation checks, not game tests or human usability proof. Final joint presentation review remains.',
            'newRules':0,'newApprovals':0,'runtimeImplemented':False,'sourceInformationDeleted':0,'submitted':False}
    write(receipt,report)
    # Note stale editorial checkpoints without changing a currently reviewed governing file.
    char=R/'docs/mechanics/CHARACTER_CREATION_PLAYTEST.md';text=char.read_text(encoding='utf-8')
    pairs=[
      ('Full ancestry traits, background packages and equipment records still need their own reconciliation; this foundation does not certify a complete ready-to-play character or live companion parity.',
       'Use the later reviewed ancestry/background and equipment guides for their stated scopes, and the reviewed language chapter for language grants and records. Remaining option dependencies and live companion parity are still separate work.'),
      ('Full mechanical reconciliation of the 14 ancestries is still pending.',
       'Use the reviewed ancestry/background integration and complete source bindings for all14 base ancestries and45 variants; apply the reviewed language chapter to their actual language grants.'),
      ('Complete background procedures remain a separate source pass.',
       'Use the reviewed ancestry/background guide and complete source bindings for the20 background packages; its named outstanding interfaces remain outstanding.'),
      ('The equipment pass must still settle missing profiles, prices and eligibility tags.',
       'Use the reviewed equipment/acquisition guide, complete item procedures and starting-package records; keep any actually unresolved entry visible.'),
      ('Next dependencies are the complete 14-ancestry and 20-background mechanical pass, equipment and feat acquisition, remaining spells, the expedition-to-Haven loop and final joint flow review.',
       'Next dependencies are the remaining selectable-content and named ancestry/background/equipment interfaces, feat acquisition, remaining spells, the expedition-to-Haven loop and final joint flow review.')]
    for old,new in pairs:assert text.count(old)==1
    write(A/'CHARACTER_ENTRYPOINT_EDITORIAL_FOLLOWUP.json',{'status':'Five proposed stale-checkpoint replacements, UNSENT and UNAPPLIED; preserve active source packet bytes',
          'file':rel(char),'sourceSha256':sha(char),'changes':[{'old':a,'proposedReplacement':b,'kind':'Current-state navigation only; no mechanical change proposed'} for a,b in pairs],
          'authorities':[rel(R/'docs/mechanics/ANCESTRY_BACKGROUND_REVIEW_STATUS.json'),rel(R/'docs/mechanics/EQUIPMENT_REVIEW_STATUS.json'),rel(R/'docs/mechanics/LANGUAGE_REVIEW_STATUS.json')],
          'next':'Carry into bounded entrypoint/worksheet presentation review after the active spell source conference; do not alter frozen source evidence to hide historical checkpoints.','sourceInformationDeleted':0})

    paths=[G/'START_HERE.md',A/'PREPARED_SPELL_SOURCE_INDEX.md',A/'GPT_REVIEW_CONTINUATION_HANDOFF.md',A/'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json',R/'data/playtest/game_development_coverage.json',R/'docs/mechanics/GAME_DEVELOPMENT_COVERAGE.md']
    b=A/'navigation-before-language-worksheet';assert not b.exists();b.mkdir()
    before={rel(p):sha(p) for p in paths}
    for p in paths:
        target=b/p.relative_to(G);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
    write(b/'FILE_MANIFEST.json',before)
    start=paths[0].read_text(encoding='utf-8');old=next(x for x in start.splitlines() if x.startswith('| Spells |'))
    start=start.replace(old,'| Spells | [All44 prepared cohorts](docs/audit/2026-10-08/full-game/PREPARED_SPELL_SOURCE_INDEX.md) preserve572 pending identities/627 book bindings:524 mechanical questions and48 post-push receipts. The first six cohorts,137 identities, are [with GPT now](docs/audit/2026-10-08/full-game/LOW_RANK_SPELLS_V3_SUBMISSION.json) in the full342-file v3 packet. The remaining38 cohorts/435 identities have an [unsent v2 handoff](docs/audit/2026-10-08/full-game/HIGHER_RANK_SPELL_FILE_HANDOFF_V2_PREPARATION.json); include current language and subsequent content decisions before dispatch. Source preparation and a live conference grant no spell approval. |')
    anchor='| Detailed interfaces and remaining work |'
    assert start.count(anchor)==1
    start=start.replace(anchor,'| Record languages on a character sheet | [Language worksheet draft](DescentReviewChanges/ReviewBible/docs/playtest/CHARACTER_LANGUAGE_WORKSHEET.md): eight forms based on the reviewed language contract; presentation review remains pending |\n'+anchor)
    paths[0].write_text(start,encoding='utf-8')
    index=paths[1].read_text(encoding='utf-8')
    old='**44 packets prepared; none sent or approved.**'
    assert old in index
    index=index.replace(old,'**44 source cohorts prepared. The first six (137 identities) are in the active GPT source conference; the other38 (435 identities) remain unsent. No new spell approval.**',1)
    first=next(x for x in index.splitlines() if x.startswith('The first six cohorts are also consolidated'))
    index=index.replace(first,'The first six cohorts were [submitted once](LOW_RANK_SPELLS_V3_SUBMISSION.json) in `DD_Low_Rank_Spells_137_Source_Prepared_v3.zip`:137 identities,136 mechanical questions and the unchanged Blink receipt,141 current-book bindings and342 complete payloads. The [v3 preparation](LOW_RANK_SPELL_FILE_HANDOFF_V3_PREPARATION.json) retains all163 original source files and all184 v2 files, adding fulfilled LAX/NWX/crafting evidence and eight unapproved proposals. Request `537ffef3-e65b-4d54-b1f2-5479667c5fd6` is active; wait for its actual final verdict. Original [v1](DD_Low_Rank_Spells_137_Source_Prepared_v1.zip) and [source verification](LOW_RANK_SPELL_FILE_HANDOFF_PREPARATION.json) remain preserved. No spell is promoted by dispatch.')
    second=next(x for x in index.splitlines() if x.startswith('The remaining38 cohorts are consolidated'))
    index=index.replace(second,second+' The later [v2 refresh](HIGHER_RANK_SPELL_FILE_HANDOFF_V2_PREPARATION.json) supplies353 complete files with completed crafting/teaching authority. It remains unsent; add current completed language and intervening content authority before dispatch.')
    paths[1].write_text(index,encoding='utf-8')
    note='''**Independent preparation during the live137-spell conference:** the [character language worksheet draft](../../../../DescentReviewChanges/ReviewBible/docs/playtest/CHARACTER_LANGUAGE_WORKSHEET.md) provides eight forms from the already-reviewed contracts, including Mira's actual Human choice and the absent Medic field. [Preparation/field map](LANGUAGE_WORKSHEET_PREPARATION.json) records full source hashes and scope; no new rule or runtime change. [Five character-entrypoint editorial follow-ups](CHARACTER_ENTRYPOINT_EDITORIAL_FOLLOWUP.json) preserve exact old text and proposed updates to obsolete pending-pass labels. These are UNSENT/UNAPPLIED pending their bounded presentation review. All342 active spell-packet input files remain unchanged. Current start-page/source-index labels now distinguish six submitted cohorts from38 unsent cohorts; historical versions are preserved.

'''
    paths[2].write_text(note+paths[2].read_text(encoding='utf-8'),encoding='utf-8')
    observation=read(paths[3]);observation['independentWorksheetDraft']=rel(receipt);observation['entrypointEditorialFollowup']=rel(A/'CHARACTER_ENTRYPOINT_EDITORIAL_FOLLOWUP.json');observation['atUtc']=datetime.now(timezone.utc).isoformat()
    observation['verifiedLiveFindings']=['GPT verified342 payloads and LAX hashes','GPT reading full source preparations, including duration/alias/copying/delay and Invisibility/Quick-Cast timing conflicts'];write(paths[3],observation)
    ledger=read(paths[4]);gates={x['id']:{k:x[k] for k in ['acceptanceGate','closure','humanEvidence']} for x in ledger['aspects']}
    for row in ledger['aspects']:
        if row['id'] not in ['DD-05','DD-46','DD-60','DD-66']:continue
        for p in [rel(worksheet),rel(receipt),rel(A/'CHARACTER_ENTRYPOINT_EDITORIAL_FOLLOWUP.json')]:
            if p not in row['draftEvidence']:row['draftEvidence'].append(p)
        row['openIssues'].append('A paper language worksheet now maps all eight reviewed record definitions. Its presentation and five proposed stale character-entrypoint labels await bounded joint review; no new mechanics, source-card promotion, save migration or live character-builder parity is claimed.')
    assert gates=={x['id']:{k:x[k] for k in ['acceptanceGate','closure','humanEvidence']} for x in ledger['aspects']}
    write(paths[4],ledger)
    subprocess.run([sys.executable,'-X','utf8',str(R/'tools/build_game_coverage.py')],check=True)
    assert all(sha(G/p)==h for p,h in protected_hashes.items())
    assert all(sha(G/p)==h for p,h in active.items())
    # Check the actual newly edited entry paths, with no gameplay claim.
    nav_links=0
    for path in [paths[0],paths[1],worksheet]:
        for link in re.findall(r'\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
            if '://' in link:continue
            target=(path.parent/link.partition('#')[0]).resolve();assert target.exists(),link;nav_links+=1
    write(A/'LANGUAGE_WORKSHEET_NAVIGATION_RECEIPT.json',{'before':before,'after':{rel(p):sha(p) for p in paths},'linkOccurrencesResolved':nav_links,'all342ActiveSpellPayloadsUnchanged':True,'reviewedLanguageInputsUnchanged':True,'all75AcceptanceGatesClosuresHumanEvidenceUnchanged':True,'newApprovals':0,'sourceInformationDeleted':0})
    print(json.dumps({'status':'Worksheet drafted and mapped; stale queue navigation corrected','forms':len(sections),'declaredContractFields':sum(len(x['sourceDeclaredFields']) for x in field_map),'linksResolved':nav_links,'activeSpellPayloadsUnchanged':342,'newApprovals':0},indent=2))
if __name__=='__main__':main()
