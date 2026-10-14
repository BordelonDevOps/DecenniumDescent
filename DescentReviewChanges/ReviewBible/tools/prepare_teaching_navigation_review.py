"""Assemble six complete teaching/navigation drafts without changing reviewed rules.

This creates a staging manifest, not a frozen/uploaded archive. At actual dispatch,
recheck the manifest and refresh changed review-status/navigation context.
"""
from datetime import datetime, timezone
from pathlib import Path
from hashlib import sha256
import difflib
import json
import re
from urllib.parse import unquote

R=Path(__file__).resolve().parents[1]
G=R.parents[1]
A=G/'docs/audit/2026-10-08/full-game'


def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return sha256(p.read_bytes()).hexdigest()
def save(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def main():
    manifest_path=A/'TEACHING_NAVIGATION_REVIEW_STAGING.json'
    candidate=R/'docs/mechanics/CHARACTER_CREATION_NAVIGATION_CANDIDATE.md'
    assert not candidate.exists() and not manifest_path.exists(), 'Preserve previous prepared artifacts'
    protected=read(A/'LOW_RANK_SPELL_FILE_HANDOFF_V3_PREPARATION.json')['currentFileHashes']
    exact=read(A/'LOW_RANK_136_EXACT_V1_PREPARATION.json')['manifest']
    assert all(sha(G/p)==h for p,h in protected.items())
    active={p:e['sha256'] for p,e in exact.items() if (G/p).is_file()}
    assert all(sha(G/p)==h for p,h in active.items())
    proposals=read(A/'CHARACTER_ENTRYPOINT_EDITORIAL_FOLLOWUP.json')
    source=G/proposals['file']
    assert sha(source)==proposals['sourceSha256']
    original=source.read_text(encoding='utf-8')
    body=original
    for change in proposals['changes']:
        assert body.count(change['old'])==1, change['old']
        body=body.replace(change['old'],change['proposedReplacement'])
    banner='**NAVIGATION-ONLY REVIEW COPY — five progress-note updates await joint presentation review.** The reviewed foundation mechanics below are unchanged. The original chapter and exact old wording remain preserved; use its current reviewed source for governing rules.\n\n'
    first,rest=body.split('\n\n',1)
    candidate.write_text(first+'\n\n'+banner+rest,encoding='utf-8')
    # Reverse the five replacements independently to prove that only those notes
    # and the explicit candidate banner differ from the original chapter.
    restored=candidate.read_text(encoding='utf-8').replace(banner,'',1)
    for change in reversed(proposals['changes']):
        assert restored.count(change['proposedReplacement'])==1
        restored=restored.replace(change['proposedReplacement'],change['old'])
    assert restored==original
    diff=''.join(difflib.unified_diff(original.splitlines(keepends=True),candidate.read_text(encoding='utf-8').splitlines(keepends=True),fromfile=source.relative_to(G).as_posix(),tofile=candidate.relative_to(G).as_posix()))
    diff_path=A/'CHARACTER_CREATION_NAVIGATION_CANDIDATE.diff'
    diff_path.write_text(diff,encoding='utf-8')
    drafts=[R/'docs/playtest'/f for f in ['CHARACTER_LANGUAGE_WORKSHEET.md','PLAYTEST_TERMS_GLOSSARY.md','FIRST_CRAFT_WALKTHROUGH.md','INJURY_AND_AID_WALKTHROUGH.md','COMPANION_COMMAND_WALKTHROUGH.md']]+[candidate]
    sources=set(drafts+[source,diff_path,A/'CHARACTER_ENTRYPOINT_EDITORIAL_FOLLOWUP.json',Path(__file__)])
    report_fields=[('LANGUAGE_WORKSHEET_PREPARATION.json','protectedInputs'),
                   ('PLAYTEST_TERMS_GLOSSARY_SOURCE_MAP.json','referencedFileHashes'),
                   ('FIRST_CRAFT_WALKTHROUGH_SOURCE_CHECK.json','sourceHashes'),
                   ('INJURY_AND_AID_WALKTHROUGH_SOURCE_CHECK.json','sourceHashes'),
                   ('COMPANION_COMMAND_WALKTHROUGH_SOURCE_CHECK.json','sourceHashes')]
    source_checks=[]
    for name,key in report_fields:
        p=A/name; report=read(p); sources.add(p)
        for relative,expected in report[key].items():
            actual=G/relative
            assert sha(actual)==expected,(name,relative)
            sources.add(actual)
        source_checks.append({'report':p.relative_to(G).as_posix(),'allRecordedSourcesUnchanged':True,'sourceCount':len(report[key])})
    for f in proposals['authorities']: sources.add(G/f)
    for name in ['LANGUAGE_EXACT_FULFILLMENT.json','ONBOARDING_CHARTER_EXACT_FULFILLMENT.json','ADVANCED_167_EXACT_PROMOTION_RECEIPT.json','LOW_RANK_136_EXACT_V1_SUBMISSION.json','LOW_RANK_136_CANDIDATE_AUTHORING_RECEIPT.json']:
        sources.add(A/name)
    links=[]
    for manuscript in drafts:
        for raw in re.findall(r'\]\(([^)]+)\)',manuscript.read_text(encoding='utf-8')):
            target=unquote(raw.split('#',1)[0].strip('<>'))
            if not target or re.match(r'^[a-zA-Z]+:',target): continue
            p=(manuscript.parent/target).resolve()
            assert p.is_file(),(manuscript,raw)
            assert p.is_relative_to(G)
            sources.add(p)
            links.append({'from':manuscript.relative_to(G).as_posix(),'reference':raw,'target':p.relative_to(G).as_posix()})
    questions=[
        ('TE-01','All six complete draft files','Confirm these drafts explain only their cited reviewed rules. Retain the actual scope/status of every cited source and every stated scenario premise.'),
        ('TE-02','Language worksheet — forms 1–8','Check all eight reviewed record contracts and required fields, conditional values, cross-references and actual source authority. A blank, absent, null and empty value must remain distinct where relevant.'),
        ('TE-03','Language worksheet — actual grants','Check Mira’s Common and chosen Dwarvish, Human choice provenance, Nomadic no-addition and Battlefield Medic absent Languages field. No invented background grant, dialect, language or script relation.'),
        ('TE-04','Language worksheet — choices and courses','Check exhausted/unresolved choices, actual modes, tuition and active-time records, interruptions and no duplicated study/rest/Insight awards.'),
        ('TE-05','Language worksheet — text and communication','Check copy versus underlying evidence, three Insight plus eight active hours, 250-word scope, six-second speech, ordered interpretation and actual delivery/consent/channel requirements.'),
        ('TE-06','Language worksheet — audience and usability','Check which fields a player actually needs during play, source-register references on paper, and that private supporting meaning stays private. Propose exact presentation simplifications without erasing required source distinctions.'),
        ('TE-07','Glossary — 48 terms','Check every definition against its full cited procedure, especially attacks versus task degrees versus binary saves, critical dice, actual modifiers and proficiency.'),
        ('TE-08','Glossary — distinct clocks/resources','Check regular versus extra turn/Action, Recharge, genuine encounters, RP versus RC, Dissonance/Refrain and all three separate Strain/Exhaustion namespaces.'),
        ('TE-09','Glossary — class/recipe access','Check Base/Arch/Hero, L/S/M, trade versus character level, equipment grade versus crafting quality, and no same-name automatic access.'),
        ('TE-10','First craft — eligibility and physical setup','Check public recipe-200, Mira’s actual proficiency/trade initialization, formula gate, station and tools, no assistance, no Take 10, lawful acquired stock and separate scene budget.'),
        ('TE-11','First craft — material reservation and quality','Check four tier-2 Purified-water units plus one petal, seven reserved vials before roll, no catalyst/carrier invention, batch timing, quality options, failed recovery and all mass calculations.'),
        ('TE-12','First craft — XP and administration','Check four first-success trade XP, no level-up, repeat identity, Action administration, actual willing recipient, Poisoned versus its cause, ten-minute benefit versus one-hour open-vial clock and final inventory.'),
        ('TE-13','Injury — two incoming events','Check 10→4→0 HP, exactly two Wound saves, existing-Wound penalty, one linked Mobility Trauma Injury, no death failure on first reaching zero and current movement/incapacity.'),
        ('TE-14','Injury — stabilization and treatment clock','Check natural death save 8, automatic healer-kit stabilization, one actual charge, d4=2 deadline, eight active treatment hours/one Supply and 8.5 elapsed hours without duplicate rest or recovery.'),
        ('TE-15','Injury — independent boundaries','Check temporary absorption, critical hit while dying, Instant Death ordering, natural-20 death recovery, third-Wound healing ceiling and preservation of linked Wounds/Injuries/Prone.'),
        ('TE-16','Companions — three different subjects','Check Tinker1 Anacite versus two actual Tiny recipe-596 bodies, individual profiles, actual load/ownership, crafted roster limit and no class-feature inheritance.'),
        ('TE-17','Companions — lawful binding and control','Check ten minutes per body, real tools/INT6 minimum, actual visible channel, finite registered task, unchanged-task Action start and no authority from language or possession alone.'),
        ('TE-18','Companions — four-round sequence','Check one owner-wide command allowance and relevant offense, support-only distinction, attached phase after whole turn, no extra-turn reset, attack rolls/damage and no inactive body operation.'),
        ('TE-19','Companions — servicing and repair','Check separate paid service blocks, HP repair/recharge/RP versus actual service refill, Tiny maintenance pack value/mass, tool check and genuine new-encounter payment.'),
        ('TE-20','Character-creation navigation copy','Check the five full replacement progress notes against current ancestry/background/equipment/language review scopes. Reverse-diff restores the entire original chapter; no character rule, number or acquisition schedule changes.'),
        ('TE-21','Complete public handout content','Check that teaching text and directly displayed examples do not reveal private roster/recipe membership or invent campaign facts. The supporting review packet is internal and must not be mistaken for a public release.'),
        ('TE-22','Review and release scope','Separate authored presentation acceptance from human teaching trials/two-lookup usability, numeric balance, deployed companion behavior and all-game flow. Pending136 spell candidates remain unavailable until their exact gate; other pending spells/feats stay pending. Preserve final flow→authorized push→verified remote→careful cosmology order.'),
    ]
    checklist={'status':'prepared-unsent-presentation-review-questions','questions':[{'id':i,'subject':s,'question':q} for i,s,q in questions],
               'candidateFiles':[p.relative_to(G).as_posix() for p in drafts],
               'request':'Read every complete draft and its actual sources. Give exact replacement wording and affected paragraphs for bounded corrections, or scoped authored-presentation acceptance. Do not invent new mechanics or certify human use.'}
    checklist_path=A/'TEACHING_NAVIGATION_REVIEW_CHECKLIST.json';save(checklist_path,checklist);sources.add(checklist_path)
    candidate_receipt=A/'CHARACTER_CREATION_NAVIGATION_CANDIDATE_RECEIPT.json'
    save(candidate_receipt,{'status':'complete-separate-navigation-draft-unsent','original':source.relative_to(G).as_posix(),
        'originalSha256':sha(source),'candidate':candidate.relative_to(G).as_posix(),'candidateSha256':sha(candidate),
        'changes':proposals['changes'],'candidateBanner':banner,'reverseDiffRecreatesOriginalExactly':True,
        'foundationMechanicsChanged':False,'originalReplaced':False,'presentationApproved':False,'submitted':False})
    sources.add(candidate_receipt)
    notes='''# Teaching and navigation review — staging

Six complete drafts are ready for a bounded joint presentation review: the language worksheet,48-term glossary, first-craft example, injury/aid example, companion-command example and complete character-foundation navigation copy. Read TEACHING_NAVIGATION_REVIEW_CHECKLIST.json for22 exact subjects and TEACHING_NAVIGATION_REVIEW_STAGING.json for the full source file inventory.

This is UNSENT staging. The current GPT request is the separate136-spell exact review. Do not queue this prompt into that live response. At the next appropriate dispatch, check the current GPT result, refresh changed review-status/navigation context, verify every still-governing source hash and assemble a fresh complete archive from the manifest. No ZIP has been frozen for this teaching review yet.

The five original teaching drafts retain their prior source-check reports and pending presentation labels. The new full character-creation copy changes only five stale progress-note sentences plus an explicit review-copy banner. Its reverse transformation exactly reconstructs the original; the original remains untouched in the active spell review’s source evidence. The diff and complete original are included in the inventory.

Source-check reports distinguish arithmetic and existing reference helper checks from authored manual sequences. They do not certify all gameplay execution, actual inventory/control/scene premises or human learning. These are examples, not extra equipment/languages/crafting permissions or new source decisions. Current completed LAX/NWX/recipe scopes carry forward; remaining class/catalog and full-game integration remain open.

The staging inventory contains internal source evidence and is not a public release. Candidate handouts use only their authorized public examples. No historical source deletion, live catalog promotion, GitHub push or cosmology review has occurred.
'''
    readme=A/'TEACHING_NAVIGATION_REVIEW_README.md';readme.write_text(notes,encoding='utf-8');sources.add(readme)
    assert all(sha(G/p)==h for p,h in protected.items())
    assert all(sha(G/p)==h for p,h in active.items())
    receipt={'status':'complete-teaching-navigation-drafts-staged-unsent','preparedAtUtc':datetime.now(timezone.utc).isoformat(),
             'draftFiles':[p.relative_to(G).as_posix() for p in drafts],'draftCount':len(drafts),'reviewQuestions':len(questions),
             'existingSourceReportsVerified':source_checks,'originalCharacterChapterUnchanged':True,
             'activeSource342InputsUnchanged':True,'activeExactReviewDiskPayloadsUnchanged':len(active),
             'directLinkOccurrences':links,'sourceFiles':{p.relative_to(G).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(sources)},
             'archiveFrozen':False,'submitted':False,'presentationApproved':False,'newRules':False,
             'humanUsabilityVerified':False,'runtimeImplemented':False,'sourceInformationDeleted':0}
    save(manifest_path,receipt)
    print(json.dumps({'drafts':len(drafts),'reviewQuestions':len(questions),'sourceFiles':len(sources),'directLinks':len(links),'activeExactPayloadsUnchanged':len(active),'status':receipt['status']}))


if __name__=='__main__': main()
