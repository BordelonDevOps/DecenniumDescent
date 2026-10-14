"""Complete137-spell handoff refreshed with fulfilled LAX/NWX and eight proposals."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from datetime import datetime,timezone
import hashlib,json,re
R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(G).as_posix()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    archive=A/'DD_Low_Rank_Spells_137_Source_Prepared_v3.zip';out=A/'LOW_RANK_SPELL_FILE_HANDOFF_V3_PREPARATION.json'
    assert not archive.exists() and not out.exists()
    old=read(A/'LOW_RANK_SPELL_FILE_HANDOFF_V2_PREPARATION.json')
    assert sha(A/old['bundleFile'])==old['bundleSha256']
    assert all(sha(G/p)==h for p,h in old['currentFileHashes'].items())
    initial=read(A/'LOW_RANK_SPELL_FILE_HANDOFF_PREPARATION.json')
    catalog=read(R/'data/public/spell_playtests/catalog.json')
    pending={s['id'] for s in catalog['spells'] if s['operational'] is None and min(a['rank'] for a in s['classAccess'].values())<=3}
    assert pending=={s['spellId'] for s in initial['selectedMembership']} and len(pending)==137
    assert sum(s['operational'] is not None for s in catalog['spells'])==276
    fulfillment=read(A/'LANGUAGE_EXACT_FULFILLMENT.json');assert fulfillment['exactLanguageApproval']
    assert all(sha(G/p)==h for p,h in fulfillment['finalHashes'].items())
    nwx=read(R/'docs/playtest/ONBOARDING_REVIEW_STATUS.json')
    assert all(sha(G/p)==h for p,h in nwx['manuscriptHashes'].items())
    proposal=read(A/'LOW_RANK_SPELL_AUTHORING_PROPOSAL_INDEX.json')
    assert len(proposal['proposals'])==8 and {p['spellId'] for p in proposal['proposals']}<=pending
    assert all(sha(G/p['path'])==p['sha256'] for p in proposal['files'])
    files={G/p for p in old['currentFileHashes']}
    with ZipFile(A/'DD_Language_Communication_Exact_Review_v1.zip') as z:
        old_language=json.loads(z.read('FILE_MANIFEST.json'))
        files.update(G/p for p in old_language if (G/p).is_file())
    files.update(G/p for p in nwx['manuscriptHashes'])
    files.update([R/'docs/playtest/ONBOARDING_REVIEW_STATUS.json',R/'docs/mechanics/LANGUAGE_REVIEW_STATUS.json',
        A/'ONBOARDING_CHARTER_EXACT_FULFILLMENT.json',A/'DD_Language_Communication_Exact_Review_v1.zip',
        A/'DD_Language_Communication_Exact_Reviewer_Verdict_and_Evidence.zip',
        A/'LANGUAGE_EXACT_VERDICT_RECEIPT.json',A/'LANGUAGE_EXACT_FULFILLMENT.json',
        A/'LANGUAGE_EXACT_FULFILLMENT_PRE_LABEL.json',A/'LANGUAGE_EXACT_CORRECTION_APPLICATIONS.json',
        A/'LANGUAGE_EXACT_FULFILLMENT_SOURCE_460.json',A/'LANGUAGE_EXACT_FULFILLMENT_CANDIDATE_496.json',
        A/'LANGUAGE_EXACT_FULFILLMENT_FOCUSED_44.json',A/'LANGUAGE_EXACT_FULFILLMENT_PORTABLE_496.json',
        A/'LOW_RANK_SPELL_AUTHORING_PROPOSAL_INDEX.json',A/'LOW_RANK_LANGUAGE_SPELL_AUTHORING_PROPOSALS.json',
        A/'LOW_RANK_LANGUAGE_SPELL_AUTHORING_PROPOSALS.md',A/'ILLUSION_UTILITY_CANTRIP_AUTHORING_PROPOSALS.json',
        A/'ILLUSION_UTILITY_CANTRIP_AUTHORING_PROPOSALS.md',A/'LOW_RANK_SPELL_FILE_HANDOFF_PREPARATION.json',
        A/'LOW_RANK_SPELL_FILE_HANDOFF_V2_PREPARATION.json',A/'LOW_RANK_SPELL_FILE_HANDOFF_SOURCE_CHECK.json',
        R/'tools/fulfill_language_exact_review.py',Path(__file__).resolve()])
    for folder in ['language-exact-reviewer-files','language-lax-pre-label','onboarding-exact-reviewer-files']:
        files.update(p for p in (A/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    scope=A/'LOW_RANK_SPELL_FILE_HANDOFF_V3_SCOPE.md'
    scope.write_text('''# Remaining low-rank137 spells — complete source conference v3

This is the full existing source conference:137 actual identities,136 pre-push mechanical questions and Blink as one unchanged post-push receipt. It does not replace the137 with the eight proposal examples. All184 prior v2 payloads, including the original163 source files and141 book bindings, remain byte-identical. Full source records, all selected class access, original questions, comparison effects and governing chapters are included.

Read the six original SOURCE_PREPARATION.json files identified in LOW_RANK_SPELL_FILE_HANDOFF_PREPARATION.json: LOW_ILLUSION_SPELL (26), LOW_UNIVERSAL_SPELL (23), LOW_TRANSMUTATION_SPELL (29), LOW_NECROMANCY_SPELL (30), EVOCATION_RANK3 (8), REMAINING_RANK3_SPELL (21). Their scheduling/pending-prerequisite labels are historical. Use each actual spell/question identity; do not infer effects from an external game's shared title.

## Fulfilled governing gates

The language layer has completed LAX-01–03 under final reply12106bf1-18cf-41ee-b0df-8e5a8714d143. LANGUAGE_EXACT_FULFILLMENT.json records actual corrections,460 source/496 candidate/44 focused checks, standalone496 reproduction, corrected pre-label and final hashes and label-only proof. The current chapter, both envelopes,32 sequences, seven modified files and complete source/exact verdict packages are present. The immutable original language exact ZIP is also supplied for any bounded reproduction; do not run its pre-label assertion suite against final approved labels and report the intended flag change as a new mechanical defect. Both the pre-label snapshot and actual passing reports are included. Original LA source-direction exactApprovalGranted values stay false; only the scoped language-layer flag/status is promoted. There is no new language source queue.

LAX-01 uses exact links to already-supplied complete public collections. The unsent four-file reference addendum was not needed. LAX-02 makes provenance absent/null/value conditional. LAX-03 limits TI-04 commands to its actual controlled automata, restores noncombat Action start and preserves manual/trap/operator/TD-08 procedures. All original recipe records, class/spell/feat statuses and LA-16 receipt remain unchanged.

The six NWX teaching/charter manuscripts and their final fulfillment/status/authority are included. Completed recipe totals remain687/687, public433/433. Carry their settled acquisition, preparation, crafting, speech/literacy, teaching and device boundaries forward. A named ordinary spell is not merged with a class feature, ancestry route or recipe. Crafted storage does not settle a pending ordinary spell's missing effect.

## Concrete proposals to consider

LOW_RANK_SPELL_AUTHORING_PROPOSAL_INDEX.json links eight unapproved Codex proposals: Silent Echo/IL-02, Silence/IL-26, Blurred Visage/IL-05, Disguise Self (Minor)/IL-07, Phantom Footsteps/IL-08, Shadow Mark/IL-09, Magic Thread/UN-16 and Magic Mouth/UN-23. Both complete structured proposal files preserve their full source/access records,50 actual access bindings and32 authored boundary cases. Every additional number, cap or lifecycle decision is explicitly proposed NEW. Adopt, amend or reject each proposal with reasons from its actual source. They are not approved effects and every catalog operational field remains null.

## Required finite authoring result

For all136 mechanical identities, settle the original individual questions into sufficient operating directions to author the complete cards: actual class/rank/minimum-level access and RP/extra costs; cast time/components/material handling; target legality, range, geometry, line and movement; duration/concentration/expiry; attack/save/automatic resolution with all outcomes; each original effect clause and scaling; counters, interruption, suppression, recasts, identity/history, ending and shared costs/action limits. Label newly supplied rules NEW and preserve conflicting original source values beside the chosen interpretation. Use explicit bounded alternatives for actual conflicts instead of importing external spell rules or asking for another generic preliminary conference. Address copying/delay/echo recursion, two-Bonus-Action traps, corpse/body/custody/temporary-HP limits, transformation equipment/concentration, acoustic/illusion evidence and protected-information boundaries where actually relevant.

Map every disposition to the existing question ID and spell ID. Include worked boundary cases for disputed procedures, an exact-candidate checklist and complete machine-readable authoring register plus readable verdict. Distinguish substantive source choices from metadata cleanup and real missing controlling evidence. All ordinary spell totals remain276 operational drafts and572 pending until the later complete authored candidates and exact scoped review; no source-only promotion is requested here.

Blink remains a literal receipt. No cosmology, deeper setting meaning or deferred-language interpretation before the verified GitHub push. DD01, broader catalog/expedition/bestiary/Director integration, human teaching/balance, runtime and final whole-game flow remain open. Final joint whole-game flow precedes authorized push; verified remote commit precedes careful cosmology review. Nothing is deleted.
''',encoding='utf-8')
    files.add(scope)
    manifest={rel(p):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(files,key=rel)}
    assert all(not n.endswith('.png') for n in manifest)
    # Current language navigation is complete in the supplied actual tree.
    links=[]
    for name in ['docs/mechanics/LANGUAGE_COMMUNICATION_PLAYTEST.md','docs/mechanics/LANGUAGE_COMMUNICATION_WORKED_SEQUENCES.md','docs/director-only/LANGUAGE_COMMUNICATION_INTERNAL_CANDIDATE.md']:
        p=R/name
        for link in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
            if '://' in link:continue
            raw=link.partition('#')[0];target=(p.parent/raw).resolve() if raw else p
            links.append(rel(target));assert rel(target) in manifest
    assert len(links)==12
    with ZipFile(archive,'w',ZIP_DEFLATED,compresslevel=9) as z:
        z.writestr('README_SOURCE_REVIEW_V3.md','Read docs/audit/2026-10-08/full-game/LOW_RANK_SPELL_FILE_HANDOFF_V3_SCOPE.md first. The current governing language/NWX/crafting gates are fulfilled. Historical packages, scripts and receipts keep their original labels. Full137 sources, not an eight-spell sample. FILE_MANIFEST.json covers all complete current payload files.\n')
        z.writestr('FILE_MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
        for name in manifest:z.write(G/name,name)
    with ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(manifest)+2
        assert all(hashlib.sha256(z.read(p)).hexdigest()==e['sha256'] and len(z.read(p))==e['bytes'] for p,e in manifest.items())
    result={'preparedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'PASS complete v3 handoff; UNSENT','bundleFile':archive.name,'bundleBytes':archive.stat().st_size,'bundleSha256':sha(archive),'payloadFiles':len(manifest),'unchangedV2Payloads':184,'unchangedOriginalV1Payloads':163,'selectedIdentities':137,'mechanicalQuestions':136,'receiptOnlyIds':['blink'],'currentBookBindings':141,'unapprovedProposals':8,'proposalAccessBindings':50,'authoredProposalBoundaryCases':32,'languageGateFulfilled':True,'onboardingGateFulfilled':True,'advancedGateFulfilled':True,'currentFileHashes':{p:e['sha256'] for p,e in manifest.items()},'twelveCurrentLanguageLinksInArchive':links,'sent':False,'newSpellApprovals':0,'sourceInformationDeleted':0,'runtimeChanged':False,'cosmologyReviewed':False}
    write(out,result)
    prompt=f'''LAX-01–03 are now fulfilled in the actual repository under your final reply12106bf1-18cf-41ee-b0df-8e5a8714d143. I applied your exact replacement text/objects, conditional provenance assertion and complete LA-T30; reproduced460 source,496 candidate and44 focused checks plus496 in a standalone corrected tree; then normalized only the permitted language labels. The version-bound receipt, full current files, pre-label snapshot, final hashes, label-only proof, frozen submission and your complete final packages are included. Every original152 payload and all class/spell/feat/recipe records remain unchanged. Your exact LAX-01 link replacement was used; the independently prepared reference addendum remains unsent and unnecessary. Scope is reviewed authored language only. Please carry the fulfilled gate forward; raise a follow-up only for an actual finite discrepancy in this fulfillment.

Now please conduct the full remaining low-rank spell source-authoring conference. Attached {archive.name} is {archive.stat().st_size:,} bytes, SHA256 {sha(archive)}, {len(manifest)} complete payloads plus README and manifest. Read README_SOURCE_REVIEW_V3.md and LOW_RANK_SPELL_FILE_HANDOFF_V3_SCOPE.md. All184 prior v2 payloads including original163 complete source files are unchanged. Six preparations preserve137 exact spell identities and141 book bindings:136 mechanical questions and Blink receipt-only.

Discuss and settle every original mechanical question with concrete per-spell operating directions sufficient to author its complete card. Preserve actual class access, costs and every source clause; label new scope/timing/save/lifecycle decisions NEW. Confer on the eight explicitly unapproved proposals and their complete source records; they do not replace the other129 identities or grant adoption. Keep the fulfilled687/433 recipe, NWX and LA gates and actual class/source exceptions. Shared spell names do not merge ordinary, class, ancestry and recipe permissions.

Return a complete readable verdict, machine-readable authoring register mapped to every existing question/spell ID, conflict dispositions, worked boundaries and exact-candidate checklist. Give finite choices for actual gaps, not another generic preliminary conference. No card promotion is requested before full candidates/exact review. Preserve Blink and other incidental cosmology as receipts; final joint whole-game flow precedes authorized GitHub push, verified remote commit precedes careful cosmology review. Broader human, balance, runtime and DD01 gates remain open. No deletion or push has occurred.'''
    (A/'CODEX_LOW_RANK_SPELLS_V3_PROMPT.txt').write_text(prompt,encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ['currentFileHashes','twelveCurrentLanguageLinksInArchive']},indent=2))
if __name__=='__main__':main()
