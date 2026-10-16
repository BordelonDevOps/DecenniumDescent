"""Assemble complete current sources for first dedicated ordinary Banishment authoring."""
from datetime import datetime,timezone
from zipfile import ZipFile,ZIP_DEFLATED
import json
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    root=A/'banishment-current-review-01-input';archive=A/'DD_Banishment_Current_Review_01.zip';receipt=A/'BANISHMENT_CURRENT_REVIEW_01_PREPARATION.json'
    assert not any(p.exists() for p in [root,archive,receipt])
    old=read(A/'banishment-local-draft-01/PROPOSAL.json');classes=read(A/'ac4-current-review-01-input/CURRENT_REVIEW_INPUT.json')['currentClasses'];addendum=read(A/'BANISHMENT_CLASS_INTERFACE_ADDENDUM_02.json')
    sources={b['path']:info(G/b['path']) for b in old['sourceBindings']}
    for cls in classes:sources[cls['file']['path']]=info(G/cls['file']['path'])
    extra=[R/'data/public/spell_candidates/abjuration_conjuration_rank4_reviewed_03.json',R/'data/playtest/spell_candidates/abjuration_conjuration_rank4_cases_03.json',R/'docs/spells/candidates/ABJURATION_CONJURATION_RANK4_REVIEWED_03.md',A/'AC4_EXACT_ACCEPTANCE_03.json',A/'AC4_EXACT_ACCEPTANCE_03_RECEIPT.json',A/'AC4_EXACT_ACCEPTANCE_03_APPLICATION_CHECK.json',A/'CURRENT_SPELL_REVIEW_RECONCILIATION_02.json',A/'BANISHMENT_CLASS_INTERFACE_ADDENDUM_02.json',R/'docs/mechanics/COMPANION_COMMAND_PLAYTEST.md']
    # The companion guide's actual repository name is located explicitly below if absent.
    extra=[p for p in extra if p.name!='COMPANION_COMMAND_PLAYTEST.md' or p.exists()]
    for p in extra:sources[p.relative_to(G).as_posix()]=info(p)
    catalog=read(R/'data/public/spell_playtests/catalog.json');card=next(c for c in catalog['spells'] if c['id']=='banishment')
    index=read(R/'data/public/spell_playtests/authored_review_index.json');entry=next(e for e in index['entries'] if e['id']=='banishment')
    assert card==old['sourceCard'] and entry['authoredStatus']=='pending-authored-procedure'
    assert index['authoredCounts']=={'reviewed':434,'pending':414}
    comparisons=[]
    for ident in ['summon-spectral-steed','faction-portal','charm-person','counterspell','warding-bond']:
        i=next(i for i,c in enumerate(catalog['spells']) if c['id']==ident);comparisons.append({'id':ident,'file':info(R/'data/public/spell_playtests/catalog.json'),'pointer':f'/spells/{i}','completeRecord':catalog['spells'][i]})
    ac4path=R/'data/public/spell_candidates/abjuration_conjuration_rank4_reviewed_03.json';ac4=read(ac4path)
    for ident in ['dimensional-anchor','dimensional-door','resonance-beacon','spell-shield','summon-water-pet','faction-ally']:
        i=next(i for i,c in enumerate(ac4['spells']) if c['spellId']==ident);comparisons.append({'id':ident,'file':info(ac4path),'pointer':f'/spells/{i}','completeRecord':ac4['spells'][i],'sharedRules':ac4['sharedRules'],'profile':ac4['factionAllyProfile'] if ident=='faction-ally' else None})
    current_class_records=[]
    for r in addendum['exactComparisonCards']:
        current=info(G/r['file']['path']);assert current==r['file'];current_class_records.append(r)
    changes=[{'historical':b,'current':sources[b['path']]} for b in old['sourceBindings'] if b!=sources[b['path']]]
    questions=old['reviewQuestions']+[
      {'id':'BAN-07','question':'Reconcile actual Paladin No Escape and Verdict Absolute voluntary-only restrictions, Reign of Ashes cannot-benefit wording, ordinary soft movement locks, Oracle Fate-Bound save bonus and same-plane Chain of Duty rescue. Do not create blanket class immunity or apply historical unreviewed wording.'},
      {'id':'BAN-08','question':'Complete cell lifecycle when an independently legal visitor arrives OR a new creature is generated inside, including ordinary familiar/summon profiles. Explain actual entry/creation permission, terminal placement, cargo and consumed costs. No indefinite cell or missing body. If choosing a bounded admission rule, identify it as NEW and reconcile all actual sources.'},
      {'id':'BAN-09','question':'Avoid an unsourced universal interrupt/automatic rewind. If using pre-change return, specify exact source-local transition order for indivisible geometry/life events, newly applied Anchor, moved/destroyed support, large-body transformation, suppression and origin-plane loss. Replace the local draft mechanism if a more coherent complete source-preserving procedure is available.'},
      {'id':'BAN-10','question':'Separate current accepted AC4 authored scope from runtime selection and from the older pending labels retained in exact evidence. Review all complete source records rather than accepting lexical class hits as exhaustive coverage. Preserve all original18 and added10 scenario identities while giving finite operative adjudications.'}
    ]
    data={'id':'BANISHMENT-CURRENT-REVIEW-01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'First dedicated ordinary Banishment source-linked authoring conference; not adopted',
      'sourceCard':card,'currentAuthoredIndexEntry':entry,'currentAuthoredCounts':index['authoredCounts'],'historicalLocalDraft':old,
      'localDraftAuthority':'Unsubmitted discussion proposal, not binding design. Its source snapshot is preserved. Any old AC4-pending language is historical; current exact AC4 acceptance below controls.',
      'currentAc4Acceptance':read(A/'AC4_EXACT_ACCEPTANCE_03_RECEIPT.json'),'currentComparisonRecords':comparisons,
      'currentClasses':[{'class':c['class'],'file':info(G/c['file']['path']),'fullEnvelopeSupplied':True} for c in classes],
      'nonExhaustiveClassNavigation':current_class_records,'independentlyReadClassCount':addendum['independentlyReadCards'],'classNavigationWarning':addendum['nonExhaustiveWarning'],
      'reviewQuestions':questions,'originalAuthoredExamples':old['examples'],'additionalReviewScenarios':addendum['newAuthoredReviewScenarios'],
      'requiredAdditionalExamples':[{'id':'BAN-C29','requirement':'Another actual caster establishes an accepted Dimensional Anchor covering the original return endpoint while T is exiled; give finite source-coherent outcome with true cost/concentration/ordering, not indefinite removal.'},{'id':'BAN-C30','requirement':'A legally capable exiled target creates an actual Summon Spectral Steed or Water Pet inside the finite cell and then the Banishment source ends. Resolve every existing body, any actual escape, independent summon deadline and real cargo under the chosen complete procedure.'}],
      'hardRequirements':['Preserve the original ordinary spell identity, all7 class access rows, rank4/base7RP and printed Action60ftV/S/F, plus exact source Instantaneous metadata beside any NEW duration ruling.','Preserve temporarily sending one actual creature to another plane. Do not silently replace it with damage, a local illusion or ordinary restraint.','The draft isolated spell-cell is a NEW proposal, not approved cosmological canon; do not merge named dominions, wheel labels, afterlives, Heartcell origins, gods or identity holds.','Every live application needs finite entry/agency/clock/exit/return and terminal body/cargo rules. Expiry must not silently become indefinite hard denial.','Actual deaths, corpse identities, Hunt finality, ongoing conditions, concentration and resource/Opening/Horn clocks remain real. No resurrection or resource/gear duplication from transport.','No generic free actions, reaction windows, permission to target an unseen realm, global transport bypass or source-absent immunity.','Cleric Banish Unholy is a separate existing class technique; do not copy its WIS/damage/next-turn duration into the ordinary spell without an explicit independent proposal.','All examples are authored adjudications, not executed runtime or human/balance tests.'],
      'historicalSourceDrift':changes,'sourceBindings':list(sources.values()),'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'humanPlaytested':False,'newRulesAdopted':False}
    root.mkdir();(root/'CURRENT_REVIEW_INPUT.json').write_bytes(encoded(data));(root/'SOURCE_BINDINGS.json').write_bytes(encoded({'bindings':list(sources.values())}))
    for p in sorted((A/'banishment-local-draft-01').iterdir()):
        dest=root/'historical-local-draft'/p.name;dest.parent.mkdir(exist_ok=True);dest.write_bytes(p.read_bytes())
    request='''The AC4 exact acceptance is received and applied:434 reviewed ordinary spell identities/414 pending, with all848 index references reconciled. Thank you. Continue with a FIRST dedicated full ordinary Banishment authoring review. This is the next separate spell, not an addendum that changes the accepted15. Its old wait-for-push sequencing hold is satisfied; the owner-authorized backup and careful cosmology source review already occurred.

Read CURRENT_REVIEW_INPUT.json and all bound current sources. It supplies the complete source/access card, an explicitly unadopted local discussion draft, all17 full class envelopes, exact current AC4 and other spell comparisons, current planes/souls/owner locks, and class evidence including Paladin travel restrictions. The class keyword navigation is nonexhaustive; do not mistake38 lexical matches for full semantic coverage. The draft itself has unresolved return/visitor/atomic-geometry cases and must NOT be accepted as already runnable. You may replace its proposed mechanism where necessary while preserving the printed temporary-other-plane effect and all actual source constraints.

Confer on and independently disposition BAN-01..BAN-10. Author one complete provisional procedure with no unresolved operational hole: exact casting/save/control admission, finite destination, agency, time, concentration, custody, legal escape and entry, internally created creatures, suppression, return under current Anchor/blockers, body transformations, real death/vanishing, loose gear, and final cell closure. Avoid indefinite imprisonment, invented global interrupts, retroactive rewinds, crushing/duplication or silent source bypass. Any new local topology, admission rule or source exception must be explicitly NEW and narrowly scoped; it settles no named cosmology or soul/origin identity. Preserve the old source Instantaneous metadata as evidence if a finite concentration effect is authored. Distinguish the ordinary spell from Cleric Banish Unholy and actual Oracle/Paladin features.

Return DD_Banishment_Current_Review_01_Return.zip with exactly8 root files: REGISTER.json, SPELL_MODEL.json, PLAYER_CHAPTER.md, DIRECTOR_REVIEW.md, CASEBOOK.json, SOURCE_HASHES.json, VERDICT.md, EVIDENCE_MANIFEST.json. Keep full source/access evidence and dispositions for every question. Preserve the original18 draft examples and the10 additional scenario IDs/text in source fields; supply complete current adjudications for BAN-C01..BAN-C30, with actual costs/rolls/geometry/time and finite outcomes. Additional cases may be added if needed. If an actual source conflict cannot be resolved coherently, identify that exact conflict; do not claim a complete procedure by hiding it in an undefined future ruling.

Verify every bound source length/SHA256. Report final archive length/hash and a manifest of the7 other output files. Give the bounded authored verdict only; no runtime, human playtest, numerical balance, cosmological canon, whole-game or publication approval. Complete the downloadable files before reporting success.
'''
    (root/'README_REVIEW.txt').write_text(request,encoding='utf8',newline='\n')
    with ZipFile(archive,'w',ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(root.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(root).as_posix())
        for b in sources.values():z.write(G/b['path'],'sources/'+b['path'])
    req=A/'BANISHMENT_CURRENT_REVIEW_01_REQUEST.txt';req.write_text(request+'\nAttached: '+archive.name+'\n'+json.dumps(info(archive))+'\n',encoding='utf8',newline='\n')
    receipt.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'archive':info(archive),'request':info(req),'input':info(root/'CURRENT_REVIEW_INPUT.json'),'sources':len(sources),'fullClassEnvelopes':17,'exactCurrentSpellComparisons':len(comparisons),'classNavigationCards':len(current_class_records),'reviewQuestions':len(questions),'preservedOriginalExamples':18,'preservedAdditionalScenarios':10,'requestedNewExamples':2,'historicalSourceDrift':changes,'sourceInformationDeleted':0,'newRulesAdopted':False,'runtimeTestsExecuted':0,'actualGptSubmission':'Not yet submitted'}))
    print(json.dumps({'receipt':info(receipt),'archive':info(archive),'sources':len(sources),'questions':len(questions),'requestedCases':30,'sourceDrifts':len(changes)}))

if __name__=='__main__':main()
