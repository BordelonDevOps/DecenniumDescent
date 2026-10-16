"""Freeze full sources and all current consumable proposals for actual joint review."""
from datetime import datetime,timezone
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib,json
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()

REQUEST='''Decennium Descent — complete Core consumables source/proposal conference01.

This packet requests actual source-authoring and semantic review, not automatic endorsement of local drafts. All24 original records, prices/tiers/legal classes/dependence DCs and exact book bindings remain preserved. No item or common procedure here has been promoted. Current active guides remain unchanged.

First verify all27 current source bindings against the supplied exact source files. Read the complete original Core sections/tables retained in the source preparation, the current reviewed condition/recovery/Strain/healing/equipment/expedition/vision/language interfaces, and the actual source-qualified Bard cards. Do not treat prior pre-push deferral as a permanent ban: the progress push and careful cosmology review have occurred, but general cosmology review is not an individual item verdict.

Read COMMON_USE_MODEL.json and its14 explicit CU-01 proposals, COMMON_CASEBOOK.json(28 situations), ITEMS_MODEL.json and ITEM_CASEBOOK.json(52 situations:44 proposed item adjudications and8 unresolved source-boundary examples). All80 IDs must remain traceable in your returned casebook, with explicit corrections when needed. Local equality/arithmetic checks are not gameplay executions or semantic approval.

Resolve every shared-use choice: the two catalog families; actual servings/containers/ingestion and incomplete consumption; recipient substance identity; completed versus beneficial Long Rest as the epoch/maintenance boundary; second-dose and doubled-event save triggers; overdose frequency and advances-dependence meaning; rolling seven-day tolerance and exact equality; doubling without potency multiplication; independent dose/crash clocks; early ending versus suppression; finite one-use entitlements; maintenance and abstinence; separate Strain/Exhaustion/Intoxication/Unity/Wounds/HP; real provisions and information boundaries. Explicitly accept, replace or retain-open each choice. Do not silently rewrite approved condition/recovery text.

Challenge all20 locally authored individual envelopes for completeness and source fidelity. Missing text is NEW, not recovered canon. Inspect every original effect/crash clause, the cost and timing, source qualification, repeated use, overdose, prevention/cure and actual life pipeline. We need genuinely useful, coherent items as well as finite accounting. Review source-to-proposal changes such as Gatehouse repeated hydration/no-intoxication, Tidesilver's new cumulative motion episode, Embermark's literal1 flat reduction, Mooncap's voluntary emotional dream, fast Brandy, Cask's healing pipeline, Absinthe's actual Chant tags/Echo boundary, Redwake's selected CON penalty and post-crash lock, Null Salt's damage-source/flat group/RP scope, Choir Dust's finite public Unity interpretation, Spiral Ink's finite research/concentration crash, Deep Blue's fractional day accounting, Ash's real Hit Die and first-use dependence, and Wyrmspice's geometry/type/DC/recoil and new temporary complication table.

Four items remain explicitly held. Resolve them from actual evidence rather than silently substituting another game:
- CB-03 Stoneback Stout: first level of cold-weather exposure has no matching operational scale established in these bounded findings. Choose the actual source or author and label a complete coherent integration; do not equate it to global Exhaustion or the unrelated local sky-voyage hazard without a decision.
- CB-12 Sovereign Reserve: decide what final spoken sentence, every drinker, unique vintage and State-controlled price mean in a finite recording/access procedure. Be especially careful with true death, restoration, Hunt, distance, custody, protected speech/knowledge and source-specific cosmology. Preserve any unresolved owner-level issue rather than inventing canon.
- CS-02 Dreammilk: decide the causal first-failed-Wisdom-save wording explicitly. A next-save replacement changes the source and requires an editorial disposition; a conditional-dice model must actually handle advantage, rerolls, replacement windows and failure margins. Complete actual sleep/vision/rest endpoints, eligible existing Divination-related tasks, tolerance, player agency and overdose.
- CS-05 Ghostwine: establish real eligible ethereal/spiritual-residue profiles and the exact finite perception/fear procedure. A general soul/plane label is not automatic eligibility, creature targeting or absolute knowledge. Preserve the ten-minute benefit, one-minute fear source text, DC15 dependence and75gp.

The Mutation-table search inspected three named primary books. Its retained hits did not recover a full table; that is a bounded finding, not proof of universal absence. The six-row Wyrmspice table is therefore an explicit NEW proposal for review, not a quotation or Warrior mutation subsystem.

Return one archive DD_Core_Consumables_24_01_Return.zip containing exactly eight root files:
REGISTER.json, CONSUMABLE_MODEL.json, PLAYER_CHAPTER.md, DIRECTOR_CHAPTER.md, CASEBOOK.json, SOURCE_HASHES.json, VERDICT.md, EVIDENCE_MANIFEST.json.

REGISTER must disposition all14 shared choices and24 whole source items, distinguish original text/NEW authorship and cite exact source locations, with explicit remaining questions and reasons for changes. MODEL must contain the full resulting common rules and all24 complete individual profiles or honestly specified whole-item holds. Do not supply a patch-only fragment or claim a held item is usable. PLAYER_CHAPTER should be a readable, properly scoped item/use chapter with genuine audience boundaries. DIRECTOR_CHAPTER must include source decisions, acquisition/stock/price/legal constraints, hazards, overload outcomes, clocks, information predicates and integration instructions. CASEBOOK must retain/disposition all80 incoming IDs and add genuinely necessary situations. SOURCE_HASHES must identify all27 input sources exactly. VERDICT must separate authored candidate acceptance from runtime, human playtesting, balance, campaign-era, whole-game and publication gates. EVIDENCE_MANIFEST must give lengths/SHA256 for the other seven returned files, without a self-hash.

State the archive byte length and SHA256 in your final reply. Do not delete original records, silently change classes/approved guides, promote a crafting recipe or ordinary spell, assign cosmological identities, require player-private disclosure or report source checks as human gameplay tests. An honest unresolved owner choice is preferable to fabricated agreement, but develop every independently resolvable detail fully.
'''

def main():
    root=A/'core-consumable-conference-01';archive=A/'DD_Core_Consumables_24_Proposals_01.zip';receipt=A/'CORE_CONSUMABLE_CONFERENCE_01_PREPARATION.json'
    assert all(not p.exists() for p in [root,archive,receipt])
    common=A/'core-consumable-use-local-draft-01';items=A/'core-consumable-items-local-draft-01'
    model=read(items/'ITEMS_MODEL.json');bindings=model['sourceBindings'];assert len(bindings)==27
    refinement=A/'CORE_CONSUMABLE_ITEMS_DRAFT_01A_REFINEMENT.json';f=read(refinement)
    assert f['model']==info(items/'ITEMS_MODEL.json') and f['casebook']==info(items/'CASEBOOK.json')
    assert read(common/'CASEBOOK.json')['count']==28 and read(items/'CASEBOOK.json')['count']==52
    ids=[x['id'] for x in read(common/'CASEBOOK.json')['cases']+read(items/'CASEBOOK.json')['cases']];assert len(set(ids))==80
    root.mkdir()
    payloads={
        'COMMON_USE_MODEL.json':common/'USE_MODEL.json','COMMON_CASEBOOK.json':common/'CASEBOOK.json',
        'COMMON_DISCUSSION.md':common/'DISCUSSION.md','COMMON_LOCAL_CHECKS.json':common/'LOCAL_CHECKS.json',
        'ITEMS_MODEL.json':items/'ITEMS_MODEL.json','ITEM_CASEBOOK.json':items/'CASEBOOK.json',
        'DIRECTOR_DISCUSSION.md':items/'DIRECTOR_DISCUSSION.md','ITEM_LOCAL_CHECKS.json':items/'LOCAL_CHECKS.json',
        'ITEM_REFINEMENT_01A.json':refinement,
        'INITIAL_ITEM_PREPARATION.json':A/'CORE_CONSUMABLE_ITEMS_DRAFT_01_PREPARATION.json',
        'COMMON_PREPARATION.json':A/'CORE_CONSUMABLE_USE_DRAFT_01_PREPARATION.json'}
    for name,p in payloads.items():(root/name).write_bytes(p.read_bytes())
    for row in bindings:
        p=G/row['path'];assert info(p)==row
        dest=root/'sources'/row['path'];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(p.read_bytes())
        assert len(dest.read_bytes())==row['bytes'] and sha(dest.read_bytes())==row['sha256']
    (root/'SOURCE_BINDINGS.json').write_bytes(encoded(bindings));(root/'REQUEST.txt').write_text(REQUEST,encoding='utf-8',newline='\n')
    context={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'prepared-not-submitted','originalItems':24,'individualProcedureProposals':20,'sourceDecisionHolds':['CB-03','CB-12','CS-02','CS-05'],'sharedProposedDecisions':14,'commonCases':28,'itemCases':52,'totalStableAuthoredCases':80,'itemBoundaryOnlyCases':8,'sourceCount':27,'currentSharedModel':info(common/'USE_MODEL.json'),'currentItemModel':info(items/'ITEMS_MODEL.json'),'currentItemCases':info(items/'CASEBOOK.json'),'scope':'Current local proposals and full sources for independent actual GPT discussion. No new rule/item adoption or runtime/human test.','jointReviewComplete':False,'newRulesAdopted':False,'sourceInformationDeleted':0}
    (root/'CURRENT_REVIEW_CONTEXT.json').write_bytes(encoded(context))
    manifest=[{'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(root.rglob('*')) if p.is_file()]
    (root/'PACKAGE_MANIFEST.json').write_bytes(encoded({'files':manifest}))
    with ZipFile(archive,'w',ZIP_DEFLATED) as z:
        for p in sorted(root.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(root).as_posix())
    with ZipFile(archive) as z:
        assert set(z.namelist())=={x['path'] for x in manifest}|{'PACKAGE_MANIFEST.json'}
        for x in manifest:
            raw=z.read(x['path']);assert len(raw)==x['bytes'] and sha(raw)==x['sha256']
    receipt.write_bytes(encoded({**context,'archive':info(archive),'request':info(root/'REQUEST.txt'),'manifest':info(root/'PACKAGE_MANIFEST.json'),'payloadFilesVerified':len(manifest),'submitted':False,'dependency':'Restore actual GPT exchange before review/adoption. No blind resubmission of prior completed cosmology authoring.'}))
    print(json.dumps({'preparation':info(receipt),'archive':info(archive),'sources':27,'cases':80,'payloads':len(manifest),'submitted':False}))

if __name__=='__main__':main()
