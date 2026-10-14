"""Apply the finite NWX editorial verdict and record its scoped fulfillment."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re, shutil, sys
sys.dont_write_bytecode = True
R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'
E = A / 'onboarding-exact-reviewer-files'
S = A / 'onboarding-submitted-v2'

def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p): return p.relative_to(G).as_posix()
def dump(p, d): p.write_text(json.dumps(d, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def link_check(paths):
    result=[]
    for p in paths:
        for label, url in re.findall(r'(?<!!)\[([^\]]*)\]\(([^)]+)\)', p.read_text(encoding='utf-8')):
            if '://' in url: continue
            dest, _, anchor = url.partition('#')
            target=(p.parent/dest).resolve()
            row={'from':rel(p),'label':label,'target':rel(target),'exists':target.exists()}
            if anchor:
                headings=re.findall(r'^#{1,6}\s+(.+?)\s*#*$', target.read_text(encoding='utf-8'), re.M)
                row.update(anchor=anchor,anchorExists=anchor in [re.sub(r'[^\w\- ]','',h.lower()).replace(' ','-') for h in headings])
            assert row['exists'] and row.get('anchorExists',True), row
            result.append(row)
    return result

def main():
    receipt_path=A/'ONBOARDING_CHARTER_EXACT_FULFILLMENT.json'
    backup=A/'onboarding-before-nwx-exact-amendments'
    assert not receipt_path.exists()
    if backup.exists():
        previous=read(backup/'MANIFEST.json')
        assert all(sha(backup/n)==h and sha(G/n)==h for n,h in previous.items()), 'Resume only from the verified pre-amendment versions'
    register=read(E/'evidence/NWX_CORRECTION_REGISTER.json')
    for n,m in read(E/'evidence/REVIEWER_OUTPUT_MANIFEST.json').items():
        assert (E/n).stat().st_size==m['bytes'] and sha(E/n)==m['sha256']
    audit=read(A/'onboarding-exact-local-audit/ONBOARDING_READ_ONLY_AUDIT.json')
    reviewer_audit=read(E/'evidence/ONBOARDING_READ_ONLY_AUDIT.json')
    assert audit['totalChecks']==200 and not audit['failedChecks']
    assert audit['checks']==reviewer_audit['checks']
    assert sha(A/register['archive'])==register['archiveSha256']
    manifest=read(S/'FILE_MANIFEST.json')
    assert len(manifest)==72
    assert all(sha(S/n)==m['sha256'] for n,m in manifest.items())
    manuscripts=[R/'docs/playtest'/f'{n}.md' for n in ['FIRST_BARD_WALKTHROUGH','SESSION_ZERO_PLAYTEST','NEWCOMER_PLAYER_GUIDE','NEWCOMER_DIRECTOR_GUIDE','RESONANCE_CHEATSHEET']]+[A/'DESIGN_CHARTER_CANDIDATE.md']
    start=G/'START_HERE.md'; handoff=A/'GPT_REVIEW_CONTINUATION_HANDOFF.md'
    editable={rel(p) for p in [*manuscripts,start]}
    protected={n:m['sha256'] for n,m in manifest.items() if n not in editable}
    assert all(sha(G/n)==h for n,h in protected.items())
    # Preserve interim source-confirmed drafts, then use the reviewed submission
    # plus the exact register. Extra interim Wound prose remains in its archive
    # and unchanged governing rules, rather than expanding this finite approval.
    touched=[*manuscripts,start,handoff]
    before={rel(p):sha(p) for p in touched}
    for p in touched:
        dest=backup/rel(p);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
    dump(backup/'MANIFEST.json',before)
    texts={rel(p):(S/rel(p)).read_text(encoding='utf-8') for p in manuscripts}
    texts[rel(start)]=start.read_text(encoding='utf-8')
    applications=[]
    for c in register['corrections']:
        for i,e in enumerate(c['edits'],1):
            assert e['operation']=='replace_exact_once'
            assert texts[e['path']].count(e['old'])==1,(c['id'],e['path'])
            texts[e['path']]=texts[e['path']].replace(e['old'],e['replacement'])
            applications.append({'id':f"{c['id']}.{i}",'path':e['path'],'section':e['section']})
    assert len(applications)==16
    for n,t in texts.items(): (G/n).write_text(t,encoding='utf-8')
    corrected_hashes={n:sha(G/n) for n in texts}
    for c in register['corrections']:
        for e in c['edits']: assert texts[e['path']].count(e['replacement'])==1
    # Execute additional finite arithmetic using the unchanged reference helpers.
    sys.path.insert(0,str(R/'tools'))
    import core_playtest_rules as core
    import spell_playtest_rules as spells
    catalog={s['id']:s for s in read(R/'data/public/spell_playtests/catalog.json')['spells']}
    kwargs=dict(available_spell_ids={'mage-light','message','shield','detect-magic'},rp=2,max_rp=2,dissonance=0,proficiency=2,casting_modifier=3)
    d=0;prev=None;refrain=0;sequence=[]
    for choice in ['mage-light','message','message',None,'message']:
        if choice is None:d=max(0,d-1)
        else:
            q=spells.quote_cast(catalog[choice],'Bard',1,**dict(kwargs,dissonance=d,previous_spell_id=prev,previous_refrain=refrain))
            d=q['dissonanceBeforeClassInterface'];prev=choice;refrain=q['refrain']
        sequence.append(d)
    after_short=spells.quote_cast(catalog['message'],'Bard',1,**dict(kwargs,previous_spell_id=prev,previous_refrain=refrain))
    after_long=spells.quote_cast(catalog['message'],'Bard',1,**kwargs)
    shield=spells.quote_cast(catalog['shield'],'Bard',1,**kwargs)
    try: spells.quote_cast(catalog['shield'],'Bard',1,**dict(kwargs,rp=1))
    except spells.SpellRuleError as err: unaffordable=str(err)
    else: unaffordable='Incorrectly permitted'
    numbers={'originalDissonance':sequence,'shortRestThenMessageDissonance':after_short['dissonanceBeforeClassInterface'],
             'shortRestThenMessageRefrain':after_short['refrain'],'longRestThenMessageDissonance':after_long['dissonanceBeforeClassInterface'],
             'C':max(1,3),'cleanChantHP':core.heal(core.LifeState(maximum_hp=10,hp=3),7).hp,
             'criticalChantHP':core.heal(core.LifeState(maximum_hp=10,hp=3,wounds=(None,None,None)),7).hp,
             'shieldDissonance':shield['dissonanceBeforeClassInterface'],'shieldAtOneRP':unaffordable,'shieldAC':13+5,'attack15Misses':15<18}
    assert numbers=={'originalDissonance':[0,0,1,0,2],'shortRestThenMessageDissonance':3,'shortRestThenMessageRefrain':3,'longRestThenMessageDissonance':0,'C':3,'cleanChantHP':10,'criticalChantHP':9,'shieldDissonance':1,'shieldAtOneRP':'Insufficient RP','shieldAC':18,'attack15Misses':True}
    judgments={
      'F01':'Player required-stance paragraph and Director prompt preserve selection before the first applicable event, or by turn end; no neutral stance is supplied.',
      'F02':'Mira steps1/5 explicitly choose Mobile, with step5 after the automatic Echo. No movement or opportunity attack occurs, so the retained AC13/Speed20 and damage arithmetic applies.',
      'F03':'Both summaries retain extra-turn stance and spent allowances. Actual stance restrictions still govern Reactions; the Shield fixture specifically uses Mobile.',
      'F04':'Existing calculator reproduces0/0/1/0/2. Supplying retained Message/repetition2 after Retune gives third repeat and3 Dissonance; the corrected rest prose states that retention.',
      'F05':'The long-rest paragraph explicitly clears name/counter. With that reset state the existing calculator gives0 Dissonance for the next Message.',
      'F06':'Director rest text expressly distinguishes an additional debt-clearing Rest Watch from a beneficial long rest; no resource/history reset is assigned to it.',
      'F07':'The kit alternative explicitly requires adjacent living dying target, Action, actual charge, access and available hand, with normal retrieval. A distant target, empty kit or occupied/inaccessible hand fails its actual prerequisites.',
      'F08':'Generic stabilization explicitly restores no HP. Mira emergency aid separately requires permitted Trauma Response recovery and preserves Prone/Wounds; Dead and independently unconscious states are not cured.',
      'F09':'The first-aid paragraph retains Action/DC10 Wisdom(Medicine) as a separate alternative, without a kit or new proficiency prerequisite.',
      'F10':'Mira notation expressly defines song dice S and max(1,CHA modifier) C. At CHA+3, C stays3 while the separate Crescendo changes0/1.',
      'F11':'The amended genuine-encounter fixture states voice/hearing/perception/line, clean recipient, no prior same-round Chant and starting resources. Existing healing arithmetic yields10HP; after2RP is paid the0RP cannot fund1RP maintenance or Echo.',
      'F12':'Existing Core healing applied to3HP/max10/threeWounds and7 healing yields9HP. The clean example excludes that cap rather than overriding it; other blockers keep their source procedures.',
      'F13':'Reference quote with2RP gives first-ranked-cast Dissonance1;1RP raises Insufficient RP.13+5=18 makes attack15 miss. The text independently requires held focus, legal components and permitted unspent Reaction.',
      'F14':'The corrected example preserves the actual Shield before-resolution window and forbids a free off-turn draw. No before-roll condition is introduced.',
      'F15':'All16 exact amendments retain687/433 and enumerate16 trades, leaving actual prerequisites, expedition/flow, runtime and balance open. Frozen submission and historical receipts remain unchanged.',
      'F16':'The amended charter assigns casualty/Supply/latest-return thresholds to the party expedition charter and expressly supplies no new number or withdrawal procedure.',
      'F17':'All active local entry links and anchors resolve. The main six-document teaching path uses public mechanics and the actual selected cards; explicitly marked Director/development links in the owner index are not a player distribution bundle.',
      'F18':'All72 frozen payloads and65 untouched current dependencies are hash-preserved. Interim drafts are separately archived. Final metadata below is scoped to teaching/editorial review and leaves DD01 and catalog/runtime/flow/delivery/cosmology gates unchanged.'}
    focused=read(E/'evidence/NWX_FOCUSED_REVIEW_EXPECTATIONS.json')['expectations']
    assert {e['id'] for e in focused}==set(judgments) and len(focused)==18
    # Only now normalize the labels authorized by the finite verdict.
    normalizations=[]
    def norm(path,old,new):
        n=rel(path);t=path.read_text(encoding='utf-8');assert t.count(old)==1,(n,old)
        path.write_text(t.replace(old,new),encoding='utf-8')
        normalizations.append({'path':n,'old':old,'replacement':new})
    status='**Reviewed authored teaching draft.** Human teaching/balance, runtime and final systemic consistency remain open.'
    bard,session,player,director,resonance,charter=manuscripts
    norm(bard,'**New teaching draft, awaiting joint review.**',status)
    norm(bard,'This walkthrough is ready for rules review;','This walkthrough has completed its authored teaching review;')
    norm(session,'**Playtest draft: new table procedure awaiting joint review.**',status)
    for p in [player,director,resonance]:
        title=p.read_text(encoding='utf-8').splitlines()[0]
        norm(p,title+'\n\n',title+'\n\n'+status+'\n\n')
    norm(charter,'**Source-grounded draft awaiting joint notebook review.**','**Reviewed source-grounded editorial synthesis.** This is not new mechanical authority; DD-01 final systemic consistency remains open.')
    norm(charter,'[session-zero draft]','[session-zero agreement]')
    norm(charter,'Both await their own exact review and supply no independent mechanical authority.','Both are reviewed authored teaching texts and supply no independent mechanical authority.')
    norm(charter,'DD-01 remains open until GPT reviews this synthesis and checks it against the final operational systems.','DD-01 remains open until this reviewed synthesis is checked against the final operational systems.')
    for p,prefix in [(start,'docs/audit/2026-10-08/full-game/'),(handoff,'')]:
        old=p.read_text(encoding='utf-8').splitlines()[2]
        assert old.startswith('**Current GPT review:**')
        new=f'**Onboarding review complete:** The five teaching guides and source-grounded design charter completed their first exact review in Calibration Review Part 2. All six NWX correction areas, 20 case dispositions and 18 focused checks are recorded in the [fulfillment receipt]({prefix}ONBOARDING_CHARTER_EXACT_FULFILLMENT.json). Human teaching/balance, runtime and final systemic consistency remain open. Next is the prepared [language and communication source review]({prefix}LANGUAGE_COMMUNICATION_V2_REVIEW_SCOPE.md); it has not yet been sent.'
        norm(p,old,new)
        norm(p,'Next: onboarding and design-charter review, then remaining systems.','Next: language and communication, then remaining systems.')
    norm(start,'a source-grounded draft awaiting joint review','a reviewed source-grounded editorial synthesis')
    norm(start,'a new draft awaiting joint review','a reviewed authored table agreement')
    norm(start,'new teaching draft awaiting joint review','reviewed authored teaching draft')
    # Show that acceptance labels add no further content edits to the manuscripts.
    for n in texts:
        t=(G/n).read_text(encoding='utf-8')
        for edit in reversed([x for x in normalizations if x['path']==n]):
            assert t.count(edit['replacement'])==1
            t=t.replace(edit['replacement'],edit['old'])
        assert t==texts[n],n
    assert all(sha(S/n)==m['sha256'] for n,m in manifest.items())
    assert all(sha(G/n)==h for n,h in protected.items())
    # The new navigation links to this receipt. Materialize an explicitly
    # incomplete record before checking that link, then replace it with the
    # full fulfillment only after every remaining check has passed.
    dump(receipt_path,{'status':'IN PROGRESS: final link and receipt verification pending'})
    links=link_check([*manuscripts,start])
    advanced=read(A/'ADVANCED_167_EXACT_PROMOTION_RECEIPT.json')
    assert all(sha(G/n)==h for n,h in advanced['finalArtifactHashes'].items())
    report={'status':'FULFILLED: first exact six-manuscript authored teaching review',
      'completedAtUtc':datetime.now(timezone.utc).isoformat(),'reviewId':register['reviewId'],
      'threadId':'6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b','turnId':'89ebb4cd-5076-4984-af86-53549cf5f9c2','replyId':'4c0345a8-06a0-4101-8649-c5485694cfeb',
      'verdictFile':rel(E/'NWX_Onboarding_and_Charter_Exact_Verdict.md'),'verdictSha256':sha(E/'NWX_Onboarding_and_Charter_Exact_Verdict.md'),
      'reviewerPackage':'DD_Onboarding_Charter_Exact_Reviewer_Verdict_and_Evidence.zip','reviewerPackageSha256':sha(A/'DD_Onboarding_Charter_Exact_Reviewer_Verdict_and_Evidence.zip'),
      'submissionArchive':register['archive'],'submissionSha256':register['archiveSha256'],
      'preservedSubmittedFiles':{n:m['sha256'] for n,m in manifest.items()},'unchangedCurrentDependencies':protected,
      'interimDraftBackup':rel(backup),'interimDraftHashes':before,
      'interimReconciliation':'The active manuscripts are the exact submitted text plus NWX-01–06 and authorized label normalization. Independent interim clarifications, including extra Wound explanation, remain preserved in backup and source receipts; their governing rules are unchanged.',
      'correctionApplications':applications,'correctedBeforeLabelsHashes':corrected_hashes,'labelNormalizations':normalizations,'labelOnlyInverseProof':True,
      'finalManuscriptHashes':{rel(p):sha(p) for p in manuscripts},'finalNavigationHashes':{rel(p):sha(p) for p in [start,handoff]},
      'sourceAudit':rel(A/'onboarding-exact-local-audit/ONBOARDING_READ_ONLY_AUDIT.json'),'sourceAuditSha256':sha(A/'onboarding-exact-local-audit/ONBOARDING_READ_ONLY_AUDIT.json'),
      'sourceAuditChecks':200,'sourceAuditCounts':audit['counts'],'sourceAuditMatchesReviewer':True,
      'focusedArithmetic':numbers,'focusedResults':[{**e,'disposition':'PASS','basis':judgments[e['id']],'executionStatus':'Authored semantic/static adjudication; numeric subresults use the existing reference helpers. Not live gameplay/runtime.'} for e in focused],
      'caseDispositions':register['caseDispositions'],'activeLinks':links,'activeLinksPass':len(links),
      'audienceCheck':'No new private rule, dossier or recipe membership was projected. The six-document teaching path uses actual selected public mechanics. START_HERE is the owner/development index with clearly named Director-only references, not a standalone player export. Publication/player packaging keeps its later audience gate.',
      'recipeReviewed':687,'publicRecipesReviewed':433,'advancedReceiptSha256':sha(A/'ADVANCED_167_EXACT_PROMOTION_RECEIPT.json'),
      'completionGateSatisfied':True,'newClassSpellFeatRecipeApprovals':0,'newMechanicalRules':0,'dd01Closed':False,
      'humanTeachingVerified':False,'balanceApproved':False,'runtimeCertified':False,'wholeGameFlowComplete':False,'githubPushPerformed':False,'cosmologyReviewed':False,'sourceInformationDeleted':0,
      'nextAction':'Notify GPT of fulfilled NWX gate and submit the prepared LA-01–16 source conference after checking unchanged dependencies.'}
    dump(receipt_path,report)
    dump(R/'docs/playtest/ONBOARDING_REVIEW_STATUS.json',{'status':report['status'],'receipt':rel(receipt_path),'receiptSha256':sha(receipt_path),'manuscriptHashes':report['finalManuscriptHashes'],'governingRulesChanged':False,'wholeGameFlowComplete':False})
    print(json.dumps({k:report[k] for k in ['status','sourceAuditChecks','activeLinksPass','completionGateSatisfied','dd01Closed','newClassSpellFeatRecipeApprovals']},indent=2))

if __name__=='__main__':main()
